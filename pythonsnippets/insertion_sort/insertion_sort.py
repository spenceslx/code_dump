#Language - PYTHON
#Insertion- Sort demo

def Insertion_Sort(li):
    '''Sorting algorithm that uses the insertion method, good for small lists'''
    #start by sorting the second element, comparing with the first elements from left
    #to right
    for j in range(1, len(li)):
        key = li[j]
        i = j - 1
        while i>=0 and li[i]>key:
            li[i+1] = li[i]
            i = i-1
            li[i+1] = key
    return li[:]


