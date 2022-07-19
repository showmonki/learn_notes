import torch
import pandas as pd
import numpy as np
from LSTMmodel import LSTMModule
import matplotlib.pyplot as plt
torch.set_default_dtype(torch.float64)
# 不加这个哪怕train 设置了64， 但predict会报错 RuntimeError: expected scalar type Double but found Float


def predict(pred_data, trained_model):
    trained_model.eval()
    with torch.no_grad():
        output = []
        true_val = []
        for x_test, y_test in pred_data:
            trained_model.eval()
            y_pred = trained_model(x_test)
            output.append(y_pred.detach().numpy())
            true_val.append(y_test.detach().numpy())
    return output, true_val


model_checkpoint = './checkpoints/best_model.pth'
model = LSTMModule()
model.load_state_dict(torch.load(model_checkpoint))
pred_loader = torch.load('./datasets/pred_loader.pt')
# train_val = torch.load('./datasets/trainval_data.pt')
# pred_loader = train_val['train']
# pred_loader = train_val['val']
# pred_loader = train_val['resume']

outputs, true_vals = predict(pred_loader, model)
pred_df = pd.DataFrame(data={'pred':np.concatenate(outputs,axis=0).ravel(),'real':np.concatenate(true_vals,axis=0).ravel()})
pred_df.plot()
plt.yticks(np.arange(0, pred_df.values.max())+1)
plt.show()
plt.close()
