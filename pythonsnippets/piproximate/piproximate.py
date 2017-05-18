#######################################
#Little program used to approximate Pi#
#using probability. Simply drawing an #
#equivalent quarter cirlce within a   #
#square and plotting random points    #
#######################################

import numpy
import random
import math
import decimal

#decimal precision
decimal.getcontext().prec = 30

#define constants
side_length = 100000 #length of probability square

#total number of "dice rolls"
num_rolls = input("Enter in a number of rolls:")

#coord_gen: Null -> Array
#Generates a random coordinate within the
#the side_lengths of our probability square
def coord_gen():
    rand_coord = numpy.array([random.randrange(side_length), random.randrange(side_length)])
    return rand_coord

#dist_from_orgin: Array -> Number
#Generates the distance of a coord from
#the center of the probability square
def dist_from_orgin(ar):
    r = math.sqrt((ar[0])**2 + (ar[1])**2)
    return r

#in_circle: Array -> Boolean
#Is the coord in the probability circle?
def in_circle(ar):
    if dist_from_orgin(ar) < side_length:
        return True
    else:
        return False

#prob_to_pi: Number Number -> Number
#converts the number of hits in the probability circle
#and the total number of "rolls" to generate an
#approximation of Pi
def prob_to_pi(count, rolls):
    pi = (decimal.Decimal(4) * decimal.Decimal(count)) / decimal.Decimal(rolls)
    return pi

#main: Number -> Number
#approximates Pi by counting the hits that are inside the
#probability circle within the probability square
def main(rolls):
    count = 0
    for x in range (0, rolls):
        if in_circle(coord_gen()):
            count += 1
    probability = decimal.Decimal(count)/decimal.Decimal(rolls)
    print "Hits: ", count
    print "Probability: ", probability
    return prob_to_pi(count, rolls)

#run main with given input
print(main(num_rolls))
