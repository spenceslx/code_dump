#Python3
import argparse
import os
from random import randint
from DataRead import *
import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F


class Net(nn.Module):
    """ Building the three layer neural network to classify Iris dataset
        -- input:
            - n_feature: number of input features
            - n_out: number of output features
            - n_hidden (optional): number nodes in hidden layer
        -- output: a tensor of size n_out
    """

    def __init__(self, n_feature, n_out, n_hidden=10):
        super(Net, self).__init__()
        self.l1 = nn.Linear(n_feature, n_hidden)
        self.l2 = nn.Linear(n_hidden, n_out)

    def forward(self, x):
        x = F.relu(self.l1(x))
        #x = self.l2(x)
        x = F.relu(self.l2(x))
        return x


#def onehot(var):
#    """ Converts Net output Variable into a onehot encoding
#        for classification
#    """
#    values, indicies = var.data.max(0)
#    x = torch.zeros(len(var.data))
#    #pick a randome maximum (if there is one)
#    x[indicies[randint(0, len(indicies)-1)]] = 1
#    return Variable(x)


if __name__ == "__main__":
    net = Net(n_feature=4, n_out=3).onehot()

    #print net architecture
    print(net)

    inp = Variable(torch.randn(4))
    print(inp)
    out = net(inp)
    print(out)


    #create data class
    data = DataRead(input_directory='data/folds')
    data.onehot(labels_inc=['Iris-setosa','Iris-versicolor','Iris-virginica'])
    data.tensify()
    print(len(data.folds[0]))
    print(len(data.labels[0]))

    optimizer = torch.optim.SGD(net.parameters(), lr=0.02)
    loss_func = torch.nn.MSELoss()
