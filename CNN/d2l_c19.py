import torch
from torch import nn

def corr2d(X, K):
	"""

	:param X: Input data
	:param K: kernel
	:return: Output
	"""
	h,w = K.shape
	Y = torch.zeros((X.shapes(0) - h + 1, X.shapes[1] - w + 1))
	for i in range(Y.shapes[0]):
		for j in range(Y.shapes[1]):
			Y[i,j] = (X[i:i+h, j:j+w] * K).sum()
	return Y