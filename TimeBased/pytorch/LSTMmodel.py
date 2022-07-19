import torch
import torch.nn as nn
import numpy as np
import shutil
import logging
from tensorboardX import SummaryWriter

logging.basicConfig(format='%(asctime)s [%(levelname)-8s] %(message)s', filename = './log_LSTM_train.log')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
trainlog_dir = 'logs'
writer = SummaryWriter(logdir=trainlog_dir)


class LSTMModule(nn.Module):
    def __init__(self):
        super().__init__()
        # self.batch_size = 4
        self.input_shape = 8
        self.hidden_size = 50
        self.drop_out = 0.2
        self.output_size = 1
        self.num_layers = 3
        self.lstm = nn.LSTM(input_size=self.input_shape, hidden_size=self.hidden_size, num_layers=self.num_layers, batch_first=True,dropout=self.drop_out)
        self.fc = nn.Linear(self.hidden_size, self.output_size)

    def forward(self, input_seq):
        hidden_cell = (torch.zeros(self.num_layers, input_seq.size(0), self.hidden_size).requires_grad_(),
                            torch.zeros(self.num_layers, input_seq.size(0), self.hidden_size).requires_grad_())
        lstm_out, _ = self.lstm(input_seq.view(len(input_seq),1,-1), hidden_cell)  # _ 的重要性
        out = self.fc(lstm_out.view(len(input_seq), self.hidden_size))
        return out.squeeze(-1)


def plot_losses(train_loss, val_loss):
    import matplotlib.pyplot as plt
    plt.plot(train_loss, '.-', label="Training loss", markevery=20)
    plt.plot(val_loss, '*-', label="Validation loss", markevery=20)
    plt.legend()
    plt.title("Model Performance")
    plt.savefig('./train_val_loss.png')
    plt.show()
    plt.close()


def training_loop(n_epochs,epoch_print, optimiser, model, loss_fn,train_loader, val_loader):
    train_losses, val_losses = [], []
    lowest_loss = 10000
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
        train_losses.append(train_loss)
        writer.add_scalar('data/trainloss', train_loss, epoch)

        with torch.no_grad():
            batch_val_losses = []
            for x_val, y_val in val_loader:
                model.eval()
                output_val = model(x_val)
                loss_val = loss_fn(output_val, y_val)
                batch_val_losses.append(loss_val.item())
            val_loss = np.mean(batch_val_losses)
        val_losses.append(val_loss)
        writer.add_scalar('data/valloss', val_loss, epoch)
        save_path = './checkpoints/checkpoint.pth'
        best_path = './checkpoints/best_model.pth'
        torch.save(model.state_dict(), save_path)
        is_best_loss = train_loss < lowest_loss
        lowest_loss = min(train_loss, lowest_loss)
        logger.info(f"Epoch {epoch}, Training loss {train_loss:.4f},"
              f" Validation loss {val_loss:.4f}; Current lowest loss {lowest_loss:.4f}")
        if is_best_loss:
            shutil.copyfile(save_path, best_path)
        if epoch == 1 or epoch % epoch_print == 0:
            print(f"Epoch {epoch}, Training loss {train_loss:.4f},"
                  f" Validation loss {val_loss:.4f}; Current lowest loss {lowest_loss:.4f}")

    writer.close()
    plot_losses(train_losses, val_losses)
