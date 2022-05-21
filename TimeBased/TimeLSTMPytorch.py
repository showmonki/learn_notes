import torch
import torch.nn as nn
import tushare as ts
import torch.nn.functional as F
import time
import torch.optim as optim
import json
import numpy as np
from torch.utils.data import DataLoader,TensorDataset
torch.set_default_dtype(torch.float64)
torch.manual_seed(925)
torch.autograd.set_detect_anomaly(True)


def get_daily(ts_code='', trade_date='', start_date='', end_date=''):
    for _ in range(3):
        try:
            if trade_date:
                df = pro.daily(ts_code=ts_code, trade_date=trade_date)
            else:
                df = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
        except:
            time.sleep(1)
        else:
            return df


class LSTMModule(nn.Module):
    def __init__(self):
        super().__init__()
        # self.batch_size = 4
        self.input_shape = 8
        self.hidden_size = 50
        self.drop_out = 0.2
        self.output_size = 1
        self.num_layers = 2
        self.lstm = nn.LSTM(input_size=self.input_shape, hidden_size=self.hidden_size, num_layers=self.num_layers, batch_first=True,dropout=self.drop_out)
        self.fc = nn.Linear(self.hidden_size, self.output_size)


    def forward(self,input_seq):
        hidden_cell = (torch.zeros(self.num_layers, input_seq.size(0), self.hidden_size).requires_grad_(),
                            torch.zeros(self.num_layers, input_seq.size(0), self.hidden_size).requires_grad_())
        # h0 = torch.zeros()
        # c0 = torch.randn()
        lstm_out, _ = self.lstm(input_seq.view(len(input_seq),1,-1), hidden_cell) # _ 的重要性
        out = self.fc(lstm_out.view(len(input_seq), self.hidden_size))
        return out.squeeze(-1)


def plot_losses(train_loss, val_loss):
    import matplotlib.pyplot as plt
    plt.plot(train_loss, label="Training loss")
    plt.plot(val_loss, label="Validation loss")
    plt.legend()
    plt.title("Losses")
    plt.show()
    plt.close()


def training_loop(n_epochs,epoch_print, optimiser, model, loss_fn,train_loader, val_loader):
    # train_losses, val_losses = [], []
    for epoch in range(1, n_epochs + 1):
        batch_losses = []
        for x_batch, y_batch in train_loader:
            model.train()
            output_train = model(x_batch)  # forwards pass
            loss_train = loss_fn(output_train, y_batch)  # calculate loss
            batch_losses.append(loss_train.item())  # losss need backward, then pass item to calcualte avg loss
            optimiser.zero_grad()  # set gradients to zero
            loss_train.backward()  # backwards pass
            optimiser.step()  # update model parameters
        train_loss = np.mean(batch_losses)

        with torch.no_grad():
            batch_val_losses = []
            for x_val, y_val in val_loader:
                model.eval()
                output_val = model(x_val)
                loss_val = loss_fn(output_val, y_val)
                batch_val_losses.append(loss_val.item())
            val_loss = np.mean(batch_val_losses)
        if epoch == 1 or epoch % epoch_print == 0:
            print(f"Epoch {epoch}, Training loss {train_loss:.4f},"
                  f" Validation loss {val_loss:.4f}")
    # plot_losses()

with open('token.json') as token_file:
    token = json.load(token_file)['token']

pro = ts.pro_api(token)

# 不要开梯子获取数据，返回空
raw_df = pro.daily(exchange='SSE',ts_code='600812.SH',start_date='20200101', end_date='20220510')
target_df = raw_df[:-int(len(raw_df)*0.1)]
pred_df = raw_df[-int(len(raw_df)*0.1):]
target_cols = list(target_df.columns)
target_cols.remove('close')
target_cols.remove('ts_code')
target_cols.remove('trade_date')
X_stocks = target_df[target_cols]
y_stocks = target_df.close

split_ratio = 0.2
split_idx = -int(len(target_df)*split_ratio)

train_x, train_y = X_stocks[:split_idx], y_stocks[:split_idx]
test_x, test_y = X_stocks[split_idx:], y_stocks[split_idx:]

train_x = torch.from_numpy(train_x.values)
train_y = torch.from_numpy(train_y.values)
test_x = torch.from_numpy(test_x.values)
test_y = torch.from_numpy(test_y.values)
train_data = TensorDataset(train_x,train_y)
val_data = TensorDataset(test_x,test_y)
train_loader = DataLoader(train_data, batch_size=32, shuffle=False)
val_loader = DataLoader(val_data, batch_size=32, shuffle=False)
pred_loader = DataLoader(TensorDataset(torch.from_numpy(pred_df[target_cols].values), torch.from_numpy(pred_df.close.values)), batch_size=1, shuffle=False)


model = LSTMModule()
loss_func = nn.MSELoss()
optimiser = optim.Adam(model.parameters(), lr=0.001)
# optimiser = optim.SGD(model.parameters(), lr=0.1)
print(model)


for name, param in model.named_parameters():
    print(name, param.type(), param.dtype, param.shape)
# X,y = next(iter(train_loader))
# batch_size, n_features = 4, 8
# for epoch in range(300):
#     model.train()
#     for x_batch, y_batch in train_loader:
#         model.zero_grad()
#         # x_batch = x_batch.view([batch_size, -1, n_features])  # .to(device)
#         # y_batch = y_batch  # .to(device)
#         result = model(x_batch)
#         # result = result.detach()
#         loss = loss_func(result, y_batch)
#         loss.backward(retain_graph=True)
#         optimiser.step()
#         print(loss)
#%%
# optimiser = optim.SGD(seq_model.parameters(), lr=1e-3)
training_loop(
    n_epochs = 500,epoch_print=50,
    optimiser = optimiser,
    model = model,
    loss_fn = loss_func,
    train_loader=train_loader,
    val_loader=val_loader)
print('done')


# # Prediction

def predict(pred_data, model):
    model.eval()
    with torch.no_grad():
        output = []
        true_vals = []
        for x_test, y_test in pred_data:
            model.eval()
            y_pred = model(x_test)
            output.append(y_pred.detach().numpy())
            true_vals.append(y_test.detach().numpy())
    return output, true_vals
#%%
import pandas as pd
outputs, true_vals = predict(val_loader,model)
pred_df = pd.DataFrame(data={'pred':np.concatenate(outputs,axis=0).ravel(),'real':np.concatenate(true_vals,axis=0).ravel()})
import matplotlib.pyplot as plt
pred_df.plot()
plt.show()