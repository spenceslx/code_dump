import numpy as np
import ParallelRegression as PR
from pyspark import SparkContext

#from PR, using readData, localGradient, F, gradient

if __name__ == "__main__":
    sc = SparkContext('local[20]')
    data = PR.readData("data/small.test", sc)
    n = data.count()
    lam = 1
    beta =  np.array([np.sin(t) for t in range(50)])

    estimate_gradient = PR.estimateGrad(lambda param: PR.F(data,param,lam), \
                                        beta, 0.0001)

    print [float("%.5f" % x) for x in estimate_gradient]
    print [float("%.5f" % x) for x in PR.gradient(data,beta,lam)]
