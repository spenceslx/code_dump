#Python 3.6.1

import classes

def bayes (A, B):
    '''bayes: Event Event -> Float
    Probability of Event A given that Event B has occured.
    Currently only independent events work correctly.'''
    D = (A.prob * B.suchthat(A)) + (A.c_prob * B.suchthat(A,c=True))
    pab = (A.prob * B.suchthat(A)) / D
    return pab


#problem I'm running into is that in prob 1.30 from prob and stoch hw1, The
#prob of event B is not given, rather it is the prob B.suchthat(A) is given
#written as P[B|A], P[testpass|Disease], giving P[testpass|noDisease]. Will update
