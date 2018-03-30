#Python3
import os
import torch

class DataRead():
    """ Read data from input folds directory (run FoldsGenerator.py first)
        -- input_directory: Directory containing all of the Folds
        -- labels_inc: List of possible labels in the data file, will onehot encode
        -- label_pos: Position of label in csv lines (default at the end)

        self.folds: A dict containing the data points, each key is a fold [0,k]
                    and each value is a list of data points, where each data point
                    is represented by a list

        self.labels: A dict containing the datapoint labels, each key is a
                     fold [0,k] and each value is a list of labels, position
                     corresponding to the datapoint in folds

        self.num_folds: The number of folds

        self.labels_inc: The actual labels (after onehot encoded)

    """
    def __init__(self, input_directory, labels_pos=-1):
        if (os.path.exists(input_directory) == False):
            raise ValueError("Data directory doesn't exist")
        self.num_folds = len([name for name in os.listdir(input_directory)
            if os.path.isfile(os.path.join(input_directory, name))])
        folds = {}
        labels = {}
        for kfold in range(0,self.num_folds):
            file_name = input_directory + '/fold' + str(kfold)
            with open(file_name) as f:
                content = f.readlines()
            content = [line.strip().split(',') for line in content]
            content_labels = list(range(0,len(content)))
            for line in range(0,len(content)):
                content[line] = [eval(x) for x in content[line]]
                content_labels[line] = content[line][-1]
                content[line] = content[line][:-1]
            folds[kfold] = content
            labels[kfold] = content_labels
        self.folds = folds
        self.labels = labels

    def onehot(self, labels_inc):
        """ Converts the labels into onehot encoding based on the elements in
            labels_inc.
            For ex:
                labels_inc = ['Iris-setosa','Iris-versicolor','Iris-virginica']
                A datapoint with label 'Iris-versicolor' will have onehot label of
                [0.0, 1.0, 0.0]
        """
        labels = {}
        for kfold in range(0,self.num_folds):
            labels[kfold] = self.labels[kfold]
            for c in range(0,len(labels_inc)):
                onehot = [0.0 for x in range(0,len(labels_inc))]
                onehot[c] = 1.0
                labels[kfold] = [onehot if x==labels_inc[c] else x
                                for x in labels[kfold]]
            for x in labels[kfold]:
                if isinstance(x, list) == False:
                    raise ValueError("Missing a label in labels_inc")
        self.labels = labels
        self.labels_inc = labels_inc

    def tensify(self):
        """ Converts the dicts of list of lists (folds, labels) into
            dicts of list of pytorch tensors. Do .onehot() first!
        """
        folds = {}
        labels = {}
        try:
            for kfold in range(0, self.num_folds):
                folds[kfold] = [torch.Tensor(x) for x in self.folds[kfold]]
                labels[kfold] = [torch.Tensor(x) for x in self.labels[kfold]]
            self.folds = folds
            self.labels = labels
        except:
            raise ValueError("Data may not be floats, make sure to .onehot() first")
