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


### Part 2: intersect arrays ###

# Task 0: read in sample fasta files 

# define datasets
use_big_fasta_files = True
# choose datasets
if use_big_fasta_files:
    fasta_a = "big_A.fa"
    fasta_b = "big_B.fa"
else:
    fasta_a = "A.fa"
    fasta_b = "B.fa"
# parse fasta into a list
def get_fasta_id(input_file): 
	return [ fasta.id for fasta in SeqIO.parse(open(input_file),'fasta')]
# create two Bio.seq objects
arrayA = get_fasta_id(fasta_a)
arrayB = get_fasta_id(fasta_b)

# Task 1: naive algorithm

# input: array1 and array2 to intersect
# output: array of intersections

# define function
def intersection_brute(array1, array2):
    intersection = []
    for element1 in array1:
        for element2 in array2:
            if element2 == element1:
                intersection.append(element1)
    return intersection
# execution
intersection_1 = intersection_brute(arrayA, arrayB)


# Task 2: intersection on sorted arrays

# input: array1 and array2 to intersect
# output: array of intersections

def intersection_sorted(array1, array2):
    intersection = []
    i = 0
    j = 0
    while (i < len(array1) and j < len(array2)):
        if (array1[i] > array2[j]):
            j += 1
        elif (array2[j] > array1[i]):
            i += 1
        else:
            intersection.append(array1[i])
            i += 1
            j += 1
    return intersection

# sort arrays
arrayA_sorted = sorted(arrayA)
arrayB_sorted = sorted(arrayB)
# execution
intersection_2 = intersection_sorted(arrayA_sorted,arrayB_sorted)


# Task 3: intersection using hashes

# read array1 into dictionary
# input: array1 to be hashed
# output: array1 hashed in form of dictionary 

def fill_hash(array1):
    new_dict_arrayA = dict()
    for i in range(len(arrayA)):
        new_dict_arrayA[arrayA[i]]=i
	return new_dict_arrayA

# function intersection hash 
# input: hashed array1, unhashed array2
# output: array of intersections

def intersection_hash(harray1, array2):
    intersection = []
    for i in array2:
        if(harray1.has_key(i)):
            intersection.append(i)
    return intersection

hash_arrayA = fill_hash(arrayA)

# execution
intersection_3 = intersection_hash(hash_arrayA,arrayB)


# Task 4: speed check 

# Task 4.1:  What is the speed of the intersection function itself in comparison?
print(test_modules.time_it(intersection_brute, arrayA, arrayB))
print(test_modules.time_it(intersection_sorted, arrayA_sorted, arrayA_sorted))
print(test_modules.time_it(intersection_hash, hash_arrayA, arrayB))

# Task 4.2: What is the speed of the intersection function with the sorting and the initilisation of the hash in comparison?
print(test_modules.time_it(intersection_brute, arrayA, arrayB))
print(test_modules.time_it(sorted, arrayA)+test_modules.time_it(sorted, arrayB)+test_modules.time_it(intersection_sorted, arrayA_sorted, arrayA_sorted))
print(test_modules.time_it(fill_hash,arrayA)+test_modules.time_it(intersection_hash, hash_arrayA, arrayB))

# Task 4.3: Time complexity
# Intersection brute force: O(n*m)
# Intersection on sorted arrays: O(n+m)
# Intersection hash best case: O(n)
