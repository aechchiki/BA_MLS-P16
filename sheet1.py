### Part 1: populate arrays ###

# import libraries 
import random
import test_modules
from Bio import SeqIO

# Task 1: Write a function that preallocates an array of a given size and populates the array with random values

# preallocated array
# input: len_array = lenght of array to be filled with random integers
# output: array of integers

def fill_preallocate_array(len_array):
    arrayA = [None] * len_array			
    for idxA in range(len_array):		
        arrayA[idxA] =  random.randint(0,len_array)
    return arrayA
# example
fill_preallocate_array(10)


# Task 2: Write a function that dynamically adds a new random value at the end of an array without preallocating the size of the array

# Task 2.1: nested for loops

# dynamic array 
# input: len_array = lenght of array to be filled with random integers
# output: array of integers

def append_array_manual(len_array):
    arrayA = [random.randint(0,len_array)]
    for j in range(1,len_array+1):
        tmp_array = [None] * j
        for i in range(len(arrayA)):
            tmp_array[i] = arrayA[i]
        tmp_array[len(tmp_array)-1] = random.randint(0,len_array)
        arrayA = tmp_array
    return arrayA
# example 
append_array_manual(10)

# Task 2.2: use prebuilt append 

# built-in dynamic array
# input: len_array = lenght of array to be filled with random integers
# output: array of integers

def append_array(len_array):
    arrayA = []
    for idxA in range(len_array):
        arrayA.append(random.randint(0,len_array))
    return arrayA
# example 
append_array(10)


# Task 3: Test the speed of your functions to allocate arrays

array_length = 100000
print(test_modules.time_it(fill_preallocate_array, array_length))
print(test_modules.time_it(append_array_manual, array_length))
print(test_modules.time_it(append_array, array_length))

# For small values of array_length both the given append algorithm and the pre-allocated array show similar performace in terms of computation time. However, our own append algorithm does not perform comparably. This is due to the fact that the append algorithm, which is part of python is always doubling the number of preallocations and only extending the array again once the doubling is filled. 

