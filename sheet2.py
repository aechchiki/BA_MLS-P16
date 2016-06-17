### Part 0: import libraries  ###

import test_modules
from Bio import SeqIO

### Part 1: binary search ###

# Task 0: read in sample fasta files 

fasta_a = "small_A.fa" 	# names of fasta files with small dataset 
fasta_b = "big_A.fa"	# function to parse fasta file into a list
# parse fasta into a list
def get_fasta_id(input_file):
	return [ fasta.id for fasta in SeqIO.parse(open(input_file),'fasta')]
# create array of ids
arrayA = get_fasta_id(fasta_a)
arrayB =get_fasta_id(fasta_b)


# Task 1: Create a loop search function

# input: array1 = array to be searched, item = element to be searched in array
# output: found = true or false

def loop_search(array1, item):
	found = False   
	for i in array1:
	    if i == item:
	        found = True
	return found
# example 
loop_search(arrayA, "sp|Q9BTT0|AN32E_HUMAN")
loop_search(arrayA, "ZN7XX_HUMAN")


# Task 2: Implement a binary search function

# input: array1 = sorted array to be searched, item = element to be searched in array
# output: found = true or false

def binary_search(array1, item):
	found = False   
	first = 0
	last = len(array1)-1
	while first <= last and not found:
	    midpoint = (first + last)//2
	    if array1[midpoint] == item:
	        found = True
	    else:
	        if item < array1[midpoint]:
	            last = midpoint-1
	        else:
	            first = midpoint+1
	return found
# sort input array 
sortedA = sorted(arrayA)
sortedB = sorted(arrayB)

# example
binary_search(sortedA, "sp|Q9BTT0|AN32E_HUMAN")
binary_search(sortedA, "ZN7XX_HUMAN")


# Task 3: What is the running time of the different functions

# Task 3.1: test time on small dataset
print(test_modules.time_it(loop_search, sortedA, "sp|Q9BTT0|AN32E_HUMAN"))
print(test_modules.time_it(binary_search, sortedA, "sp|Q9BTT0|AN32E_HUMAN"))

# Task 3.2: test time on bigger dataset
print(test_modules.time_it(loop_search, sortedB, "sp|Q9BTT0|AN32E_HUMAN"))
print(test_modules.time_it(binary_search, sortedB, "sp|Q9BTT0|AN32E_HUMAN"))

