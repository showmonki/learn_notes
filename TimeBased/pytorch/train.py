import torch
import torch.nn as nn
import torch.optim as optim
from LSTMmodel import LSTMModule, training_loop
import argparse


torch.set_default_dtype(torch.float64)
torch.manual_seed(925)
torch.autograd.set_detect_anomaly(True)

parser = argparse.ArgumentParser()
parser.add_argument('--resume', type=str, default=None, help='path to resume weights file')
opt = parser.parse_args()

if __name__ == '__main__':
	# opt.resume = './checkpoints/best_model.pth'
	# opt.resume = './checkpoints/checkpoint.pth'
	model = LSTMModule()
	if opt.resume:
		model.load_state_dict(torch.load(opt.resume))


	loss_func = nn.MSELoss()
	# optimiser = optim.Adam(model.parameters(), lr=0.01, weight_decay=1e-4)
	optimiser = optim.SGD(model.parameters(), lr=0.01, weight_decay=1e-4)
	exp_lr_scheduler = optim.lr_scheduler.StepLR(optimiser, step_size=10, gamma=0.1)
	print(model)
	train_val = torch.load('./datasets/trainval_data.pt')
	train_loader = train_val['train']
	val_loader = train_val['val']
	resume_loader = train_val['resume']
	# for name, param in model.named_parameters():
	# 	print(name, param.type(), param.dtype, param.shape)
	training_loop(n_epochs=600, epoch_print=50, optimiser=optimiser, model=model,
		loss_fn=loss_func, train_loader=train_loader, val_loader=val_loader)
	# first train
	# training_loop(n_epochs=600, epoch_print=50, optimiser=optimiser, model=model,
	#               loss_fn=loss_func, train_loader=val_loader, val_loader=resume_loader)
	# resume train
	print('Training done')
