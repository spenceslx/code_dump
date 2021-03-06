#Python3
################################################################################
# Example neural net using pytorch on classifying the Iris dataset

import argparse
import os
from time import time
from random import randint
from DataRead import *
import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F



class Net(nn.Module):
    """ Building the three layer neural network to classify Iris dataset
        -- input:
            - n_feature: number of input features (int)
            - n_out: number of output features (int)
            - n_hidden (optional): number nodes in hidden layer (int)
        -- output: a nn.autograd.Variable of size n_out
    """
    def __init__(self, n_feature, n_out, n_hidden=10):
        super(Net, self).__init__()
        self.l1 = nn.Linear(n_feature, n_hidden)
        self.l2 = nn.Linear(n_hidden, n_hidden)
        self.l3 = nn.Linear(n_hidden, n_out)

    def forward(self, x):
        x = F.relu(self.l1(x))
        x = F.relu(self.l2(x))
        x = F.sigmoid(self.l3(x)) #[0,1] activation, for BCELoss
        return x

def predict(var):
    """ Converts Net output Variable into a onehot encoding
        for classification
    """
    _, indicies = var.data.max(0)
    x = torch.zeros(len(var.data))
    #pick a randome maximum (if there is one)
    x[indicies[randint(0, len(indicies)-1)]] = 1
    return Variable(x)

def metrics(outputs, labels):
    """ Takes list of outputs for a train/test set, as well as the labels, and
        computes the Accuracy, Recall, and Precision
        -- outputs: list of Variables representing the output of the neural net
        -- labels: list of Variables representing the labels of the inputs

        returns accuracy, error rate
    """
    #classify outputs based on one-hot encoding
    outputs = [predict(x) for x in outputs]

    total = float(len(outputs))
    TP = 0.0
    for datapoint in range(0, len(outputs)):
        if torch.equal(outputs[datapoint], labels[datapoint]):
            TP += 1
    accuracy = TP/total
    error_rate = 1 - accuracy
    return accuracy, error_rate


def train(data, epochs=20, learning_rate=0.02):
    """ Train model (net) over kfolds:
        -- data.folds:        The folds containing data to cross validate (dict)
        -- data.labels:       The corresponding labels to each fold (dict)
        -- epochs:       The number of times to run through one training set and
                         update net
       -- learning_rate: The gradient step size for learning

       returns the best Net
    """
    time_start = time()
    net = Net(n_feature=4, n_out=3, n_hidden=10)
    #save best net params [net,fold#,accuracy]
    best_net = [net, 0, 0]
    accuracies = [0 for x in range(0,data.num_folds)]
    #iterate over k folds with validation
    for k in range(0,data.num_folds):
        #train a new net for each kfold cross validation
        net = Net(n_feature=4, n_out=3, n_hidden=10)
        train_set = [data.folds[x] for x in range(0,data.num_folds) if x!=k]
        train_set = [y for x in train_set for y in x] #flatten list
        train_labels = [data.labels[x] for x in range(0,data.num_folds) if x!=k]
        train_labels = [y for x in train_labels for y in x] #flatten list
        test_set = data.folds[k]
        test_labels = data.labels[k]

        #convert to variables for Net
        train_set = [Variable(x) for x in train_set]
        train_labels = [Variable(x) for x in train_labels]
        test_set = [Variable(x) for x in test_set]
        test_labels = [Variable(x) for x in test_labels]

        optimizer = torch.optim.SGD(net.parameters(), lr=learning_rate)
        loss_func = torch.nn.BCELoss()

        #iterate through training set for epochs, save net params between epochs
        #compute losses from training set, save outputs for predictions
        for epoch_num in range(0,epochs):
            #train
            outputs = [0 for x in range(0,len(train_set))]
            for datapoint in range(0,len(train_set)):
                output = net(train_set[datapoint])
                outputs[datapoint] = output    #save output
                target = train_labels[datapoint]
                loss = loss_func(output, target)
                optimizer.zero_grad()
                loss.backward()     #backpropogate and compute the gradients
                optimizer.step()    #apply gradients
            accuracy, error_rate = metrics(outputs, train_labels)
            print("Fold %i Epoch %i TRAINING Accuracy=%f Error-Rate=%f" %
                  (k, epoch_num, accuracy, error_rate))

            #test
            outputs = [0 for x in range(0,len(test_set))]
            for datapoint in range(0,len(test_set)):
                output = net(test_set[datapoint])
                outputs[datapoint] = output    #save output
            accuracy, error_rate = metrics(outputs, test_labels)
            print("Fold %i Epoch %i TESTING Accuracy=%f Error-Rate=%f" %
                  (k, epoch_num, accuracy, error_rate))

        #log final Accuracy
        accuracies[k] = accuracy

        #save best network
        if accuracy > best_net[-1]:
            best_net = [net, k, accuracy]
    print("Average accuracy: %f" % (sum(accuracies)/len(accuracies)))
    print("Saving Best Network:")
    print("<network from fold%i with accuracy %f and error-rate %f>"
          % (best_net[1], best_net[2], 1-best_net[2]))
    print("Total Time = %fs" % (time() - time_start))

    return best_net[0]


if __name__ == "__main__":

    net = Net(n_feature=4, n_out=3)
    #print net architecture
    print(net)
    params = list(net.parameters())

    #create data class
    data = DataRead(input_directory='data/folds')
    data.onehot(labels_inc=['Iris-setosa','Iris-versicolor','Iris-virginica'])
    data.tensify()

    net = train(data, epochs=50)
