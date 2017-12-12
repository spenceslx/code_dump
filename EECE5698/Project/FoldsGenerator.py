#Python 3
#FoldsGenerator: run using argparse to split dataset for k-folds cross validation

import argparse
import os
import io

data = []

#argparse arguments
parser = argparse.ArgumentParser(description='Generating Folds from a CSV',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('input',default=None, help='Input file csv to be split into a directory containing k folds')
parser.add_argument('--kfolds',default=None, help='Number of folds to create from input CSV')
parser.add_argument('--dirname', default=None, help='Name of directory of output folds. Files will be named fold0, fold1,...')
args = parser.parse_args()

#read data
input_file = io.open(args.input, 'r', encoding="utf-8", errors='ignore')
for line in input_file:
    #avoid strange characters, python doesnt like it
    data.append(line)
input_file.close()

#make directory for folds
if (os.path.exists(args.dirname) == False):
    os.makedirs(args.dirname)
    
#write folds in directory
segment_size = int(len(data)/int(args.kfolds))
folds = [segment_size*x for x in range(0,int(args.kfolds))] #need to build [0, 3619, 7832, ... ]
folds.append(len(data))
for k in range(0,int(args.kfolds)):
    print("printing in fold%i" % k)
    out = "%s/fold%i" % (args.dirname, k)
    output_file = open(out,'w')
    print("data from ", folds[k], " to ", folds[k+1])
    for line in range(folds[k], folds[k+1]):

        output_file.write(data[line])

    output_file.close()
