#quick python example#
#primepairs.py: find the pairs of prime numbers#
#between a minimum value and a maximum value   #


range_min = input("Enter in a minimum value: ")
range_max = input("Enter in a maximum value: ")

#isa_prime_num: Int -> Boolean
#is this a prime number?
def isa_prime_num(num):
    if (num==0)|(num==1):
        return False #we don't consider 0|1 to be prime
    for n in range (2,(num-1)):
        if ((num%n) == 0):
            return False
    else:
        return True


for n in range (range_min,range_max):
    if isa_prime_num(n):
        if isa_prime_num(n+2):
            print n," ", (n+2)
