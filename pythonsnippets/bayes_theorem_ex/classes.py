#Python 3.6.1


class Event(object):
    '''An Event is an event that can occur. It is delcared with a probability
    of occurence. The probability MUST be lower than 1.0. Currently Events
    must be independent'''
    def __init__(self,probability,name='Generic', ind=True):
        self.name = name
        self.probability=self.prob = probability
        self.c_probability=self.c_prob = 1 - probability
        self.ind=self.independence = ind

    def suchthat(self, event_b, c=False):
        '''suchthat: returns the probability of P[A|B]. Currently only works with
        independent events'''
        #check independence
        if self.ind and event_b.ind and (not c):
            return self.prob * event_b.prob
        elif self.ind and event_b and c:
            return self.prob * event_b.c_prob

    def __str__(self):      #overloads string function
        return 'Event %s has a probability of: %10.5f' % \
                (self.name, self.probability)
