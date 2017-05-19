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



#wishlist
#iteration, keep track of the changes between each iteration
#with an array of the same size. Once each element has a small
#enough value per iteration, say 0.01, then convergence has been
#reached

#partial_converge_array: Array [listof Numbers] [listof Numbers] -> Array
#   smooths array while fixing the row indexed by Number1,
#   and the column indexed by Number2. If either one not
#   necessary, just input -1 in place and it will not be fixed.
#   i.e. imagine a wall thats at a certain potential, it should
#   remain unchanged.
def partial_converge_array (ar, row_fix, col_fix):
    size = ar.shape
    rmax = size[0]
    cmax = size[1]
    new_ar = numpy.zeros(size, dtype = float)
    for r in range(rmax):
        for c in range(cmax):
            try:
                if r in row_fix or c in col_fix:
                    new_ar[r,c] = ar[r,c]
                    continue
            except:   #case where either is an int; TypeError
                if r==row_fix or c==col_fix:
                    new_ar[r,c] = ar[r,c]
                    continue
            new_ar[r,c] = posn_average(ar, (r,c))
    return new_ar


#entire_converge_array: Array -> Array
#   smooths entire array though the averaging of each value
#   with the surrounding values. One iteration
def entire_converge_array (ar):
    size = ar.shape
    rmax = size[0]
    cmax = size[1]
    new_ar = numpy.zeros(size, dtype = float)
    for r in range(rmax):
        for c in range(cmax):
            new_ar[r,c] = posn_average(ar, (r,c))
    return new_ar


#posn_average: Array Posn -> Number
#   averages the number of the posn and the surrounding elements
#   Prereq: posn must be inside of matrix
def posn_average (ar, posn):
    dat = posn_sum(ar, posn)
    if dat[1] != 0:
        avg = dat[0]/dat[1]
        return avg
    else:
        return 0


#sum: Array Posn -> (sum, #_elements)
#   adds values of posn and surrounding positions, but also determines
#   whether or not they are valid values (ie edge or corner)
def posn_sum (ar, posn):
    size = ar.shape #tuple (x,y)
    sum = (0.0,0.0)

    if posn_inside_huh(ar, posn, size):
        itself = ar[posn[0], posn[1]]
        sum = (sum[0] + itself, sum[1] +1)
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

print partial_converge_array(array1, (0,1), (-1))
