# -*- coding: utf-8 -*-
import numpy as np
import argparse
from time import time
from SparseVector import SparseVector
from LogisticRegression import readBeta,writeBeta,gradLogisticLoss,logisticLoss,lineSearch
from operator import add
from pyspark import SparkContext

def readDataRDD(input_file,spark_context):
    """  Read data from an input file. Each line of the file contains tuples of the form

                    (x,y)

         x is a dictionary of the form:

           { "feature1": value, "feature2":value, ...}

         and y is a binary value +1 or -1.

         The return value is an RDD containing tuples of the form
                 (SparseVector(x),y)

    """
    return spark_context.textFile(input_file)\
                        .map(eval)\
                        .map(lambda (x,y):(SparseVector(x),y))



def getAllFeaturesRDD(dataRDD):
    """ Get all the features present in grouped dataset dataRDD.

	The input is:
            - dataRDD: containing pairs of the form (SparseVector(x),y).

        The return value is a list containing the keys of the union of all unique features present in sparse vectors inside dataRDD.
    """
    features = SparseVector({})
    sparseDict = dataRDD.map(lambda (x,y): x).reduce(add)
    return sparseDict.keys()

def totalLossRDD(dataRDD,beta,lam = 0.0):
    """ Computes the regularized total logistic loss of the dataset and a SparseVector beta:
    The input is:
            - dataRDD: containing pairs of the form (SparseVector(x),y)
            - beta: a sparse vector β
            - lam: the regularization parameter λ
    The return value is a scalar
    """
    return dataRDD.map(lambda (x,y): logisticLoss(beta, x, y)).reduce(add) + lam * beta.dot(beta)


def gradTotalLossRDD(dataRDD,beta,lam = 0.0):
    """ Computes the gradient of the regularized total logistic loss of the dataset and a SparseVector beta:
    The input is:
            - dataRDD: containing pairs of the form (SparseVector(x),y)
            - beta: a sparse vector β
            - lam: the regularization parameter λ
    The return value is a scalar
    """
    return dataRDD.map(lambda (x,y): gradLogisticLoss(beta, x, y)).reduce(add) + 2 * lam * beta



def test(dataRDD,beta):
    """ Computes the accuracy, precision, and recall of the prediction of labels in a dataset given our trained beta.
    The input is:
            - dataRDD: containing pairs of the form (SparseVector(x), y)
            - beta: a SparseVector beta
    The return value are the scalars ACC, PRE, and REC"""
    Prdd = dataRDD.filter(lambda (x,y): beta.dot(x) > 0).cache()
    Nrdd = dataRDD.filter(lambda (x,y): beta.dot(x) <= 0).cache()

    TP = float(Prdd.filter(lambda (x,y): y == 1).count())
    FP = float(Prdd.filter(lambda (x,y): y == -1).count())
    TN = float(Nrdd.filter(lambda (x,y): y == -1).count())
    FN = float(Nrdd.filter(lambda (x,y): y == 1).count())

    ACC = (TP + TN) / (Prdd.count() + Nrdd.count())
    PRE = TP / (TP + FP)
    REC = TP / (TP + FN)

    return ACC, PRE, REC



def train(dataRDD,beta_0,lam,max_iter,eps,test_data=None):
    """ Train a logistic classifier from deta.

	The function minimizes:

               L(β) = Σ_{(x,y) in data}  l(β;x,y)  + λ ||β||_2^2

        using gradient descent.

        Inputs are:
            - dataRDD: containing pairs of the form (SparseVector(x), y)
            - beta_0: an initial sparse vector β_0
            - lam: the regularization parameter λ
            - max_iter: the maximum number of iterations
            - eps: the tolerance ε
            - test_data (optional): data over which model β is tested in each iteration w.r.t. accuracy, precision, and recall

        The return values are:
            - beta: the trained β, as a sparse vector
            - gradNorm: the norm ||∇L(β)||_2
            - k: the number of iterations

    """
    k = 0
    gradNorm = 2*eps
    beta = beta_0
    start = time()
    while k<max_iter and gradNorm > eps:
        obj = totalLossRDD(dataRDD,beta,lam)

        grad = gradTotalLossRDD(dataRDD,beta,lam)
        gradNormSq = grad.dot(grad)
        gradNorm = np.sqrt(gradNormSq)

        fun = lambda x: totalLossRDD(dataRDD,x,lam)
        gamma = lineSearch(fun,beta,grad,obj,gradNormSq)

        beta = beta - gamma * grad
        if test_data == None:
            print 'k = ',k,'\tt = ',time()-start,'\tL(β_k) = ',obj,'\t||∇L(β_k)||_2 = ',gradNorm,'\tgamma = ',gamma
        else:
            acc,pre,rec = test(test_data,beta)
            print 'k = ',k,'\tt = ',time()-start,'\tL(β_k) = ',obj,'\t||∇L(β_k)||_2 = ',gradNorm,'\tgamma = ',gamma,'\tACC = ',\
            acc,'\tPRE = ',pre,'\tREC = ',rec
        k = k + 1

    return beta,gradNorm,k

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Logistic Regression.',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('traindata',default=None, help='Input file containing (x,y) pairs, used to train a logistic model')
    parser.add_argument('--testdata',default=None, help='Input file containing (x,y) pairs, used to test a logistic model')
    parser.add_argument('--beta', default='beta', help='File where beta is stored (when training) and read from (when testing)')
    parser.add_argument('--lam', type=float,default=0.0, help='Regularization parameter λ')
    parser.add_argument('--max_iter', type=int,default=100, help='Maximum number of iterations')
    parser.add_argument('--eps', type=float, default=0.1, help='ε-tolerance. If the l2_norm gradient is smaller than ε, gradient descent terminates.')
    parser.add_argument('--N',type=int,default=2,help='Level of parallelism')

    verbosity_group = parser.add_mutually_exclusive_group(required=False)
    verbosity_group.add_argument('--verbose', dest='verbose', action='store_true')
    verbosity_group.add_argument('--silent', dest='verbose', action='store_false')
    parser.set_defaults(verbose=True)

    args = parser.parse_args()
    sc = SparkContext(appName='Parallel Logistic Regression')

    if not args.verbose :
        sc.setLogLevel("ERROR")


    print 'Reading training data from',args.traindata
    traindata = readDataRDD(args.traindata, sc).repartition(args.N).cache()
    print 'Read',traindata.count(),'data points with',len(getAllFeaturesRDD(traindata)),'features in total'

    if args.testdata is not None:
        print 'Reading test data from',args.testdata
        testdata = readDataRDD(args.testdata, sc).cache()
        print 'Read',testdata.count(),'data points with',len(getAllFeaturesRDD(testdata)),'features'
    else:
        testdata = None

    beta0 = SparseVector({})

    print 'Training on data from',args.traindata,'with λ =',args.lam,', ε =',args.eps,', max iter = ',args.max_iter
    beta, gradNorm, k = train(traindata,beta_0=beta0,lam=args.lam,max_iter=args.max_iter,eps=args.eps,test_data=testdata)
    print 'Algorithm ran for',k,'iterations. Converged:',gradNorm<args.eps
    print 'Saving trained β in',args.beta
    writeBeta(args.beta,beta)
