import numpy as np
import ParallelRegression as PR

#From PR, using functions: localGradient, f, estimateGrad

if __name__ == "__main__":
    y = 1.0
    x = np.array([np.cos(t) for t in range(5)])
    beta =  np.array([np.sin(t) for t in range(5)])

    local_gradient = PR.localGradient(x,y,beta)
    estimate_gradient = PR.estimateGrad(lambda param: PR.f(x,y,param), \
                                        beta, 0.001)

    print local_gradient
    print estimate_gradient
