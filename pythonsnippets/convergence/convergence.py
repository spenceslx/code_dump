#Designing a system to operate on a set of data points
#Until there is a convergence.
#Idea is taken from Electricity and Magnetism
#Spring 2017

#from array import *
import numpy
import unittest

#set initial conditions in data file
indata = open("data.txt", "r") #reading from data file
outdata = open("convergence.txt", "w") #output file

#print indata.read() #for testing

#An array is a ArrayIdentifier = array(typecode, [Initializers])
array1 = numpy.array([[4,5,6], [1,2,3]])
array2 = numpy.array([[2,1,5],[7,10,3],[3,4,0]])
array3 = numpy.array(numpy.mat('1 2; 3 4')) #can create array from subclasses

#A Posn is a tuple = (a,b)
posn1 = (0,0)
posn2 = (2,3)
posn3 = (-1, 20)
posn4 = (4,20)


#posn_average: Array Array -> Number
#   averages the number of the surrounding elements
#   Prereq: posn must be inside of matrix
def posn_average (ar, posn):
    dat = posn_sum(ar, posn)
    if dat[1] != 0:
        avg = dat[0]/dat[1]
        return avg
    else:
        return 0


#sum: Array Posn -> (sum, #_elements)
#   adds surrounding positions, but also determines
#   whether or not they are valid values (ie edge or corner)
def posn_sum (ar, posn):
    size = ar.shape #tuple (x,y)
    sum = (0.0,0.0)

    if posn_inside_huh(ar, (posn[0] - 1,posn[1]), size): #up
        up = ar[posn[0] - 1, posn[1]]
        sum = (sum[0] + up, sum[1] + 1)
    if posn_inside_huh(ar, (posn[0]+1,posn[1]), size): #down
        down = ar[posn[0] + 1, posn[1]]
        sum = (sum[0] + down, sum[1] + 1)
    if posn_inside_huh(ar, (posn[0],posn[1] - 1), size): #left
        left = ar[posn[0], posn[1] - 1]
        sum = (sum[0] + left, sum[1] + 1)
    if posn_inside_huh(ar, (posn[0],posn[1] + 1), size): #right
        right = ar[posn[0], posn[1] + 1]
        sum = (sum[0] + right, sum[1] + 1)

    return sum

#posn_edge_huh: Array Posn Tuple -> Boolean
#   if the posn is inside of array, return true
#   else, false
def posn_inside_huh (ar, posn, size):
    x = posn[0]
    y = posn[1]
    xsize = size[0] - 1
    ysize = size[1] - 1

    if x < 0 or x > xsize:
        return False
    elif y < 0 or y > ysize:
        return False
    else:
        return True
