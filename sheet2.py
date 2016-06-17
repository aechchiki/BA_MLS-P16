### Part 0: import libraries  ###

import test_modules
from Bio import SeqIO
import time
import utils as util
from pylab import imshow, show, get_cmap

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


### Part 2: exact sequence matching ###


# Task 0: extract fasta file subset

def extract_subseq(fasta_record, start, end, output_file_name):
    fasta_record.seq = records[0].seq[start:end]
    handle = open(output_file_name, "w")
    SeqIO.write(fasta_record, handle, "fasta")
    handle.close()
    
    
# Task 1: Implement a function that converts a word (e.g. 'acg' ) into a position in the array

# input: nuc_string= string of nucleotide sequences in lower case
# output: position within an array

def get_pos(nuc_string):
    alphabet_map = {'a':'00', 'c':'01', 'g':'10', 't':'11'}
    binary_result =''
    for i in nuc_string:
        binary_result = binary_result + alphabet_map[i]
    position = int(binary_result,2)
    return position


# Task 2: Implement a function that counts and saves the occurences of words

# input: biopython object seqRecords= string to analyze, kmerLength=length of the word
# output: array= array with occurrences of the word and its hash

def calc_kmer_freq(seqRecords, kmerLength):
    results = []
    results = [0] * 4**kmerLength # loop through all sequences
    for i in range(len(seqRecords)): # use a sliding window of kmer length through the sequence
        for j in range(len(seqRecords[i].seq)-kmerLength+1):
        # since some genomes contain cap sequences 'N' check whether key exists and add 1 if it does
            pos = get_pos(seqRecords[i].seq[j:j+kmerLength].lower())
            if pos>=0:
                results[pos] += 1
    return results
    
    
# Task 3: Use your functions to obtain the fractal images

# choose genome file
fasta_a = "short_c.fas"

# define parameters 
kmer_length = 7 # set kmer_length
cmap_color = "gray" # set cmap color scheme
array_binary = calc_kmer_freq(records,kmer_length) #create the array

# process array for plotting
words = util.convert_arraybinary_2_dictionnary(array_binary,kmer_length) # convert the custom array into a dictionnary
matrix = util.create_matrix_occurence(kmer_length, words) # convert the dictionnary[word]:occurences into a matrix
imshow(matrix, cmap=get_cmap(cmap_color), interpolation="nearest") # print the matrix as a pixel art 
show()


# Task 4: generate all permutations using a recursive function

# input: length = biopython seq object, alphabet = kmer length, prefix = start prefi
# output: all_result = list of all possible permutations

def gen_permutations(length, alphabet, prefix):
    all_results = []
    def permutations(length, alphabet, prefix):
        if len(prefix) == length:
            all_results.append(prefix)
            return prefix
        result = []
        for x in alphabet:
            extended = prefix + x
            result.append(permutations(length, alphabet, extended))
        return result
    permutations(length, alphabet, prefix)
    return all_results

# input: seqRecords = biopython seq object, kmerLength = kmer length
# output: kmer_dict = dictonary with kmers as keys and their frequencies as values

def calc_kmer_freq_dict(seqRecords, kmerLength):
    # create a list with all possible permutations of a given word length of nucleotides
    #permutations = list(itertools.product(['a','c','g','t'], repeat=kmerLenght))
    permutations = gen_permutations(kmerLength, ('a','c','g','t'), '')
    # read all possible permutations in a dictionary and set their frequencies to 0
    kmer_dict = dict()
    for i in range(len(permutations)):
        kmer_dict[permutations[i]]=0
    # loop through all sequences
    for i in range(len(seqRecords)):
        # use a sliding window of kmer length through the sequence of each record
        for j in range(len(seqRecords[i].seq)-kmerLength+1):
            # since some genomes contain cap sequences 'N' check whether key exists and add 1 if it does
            if seqRecords[i].seq[j:j+kmerLength].lower() in kmer_dict:
                kmer_dict[seqRecords[i].seq[j:j+kmerLength].lower()] += 1
    return kmer_dict
print (calc_kmer_freq_dict(records,2))

# convert to matrix and visualize 

kmer_length = 7
words = calc_kmer_freq_dict(records,kmer_length)
matrix = util.create_matrix_occurence(kmer_length, words)
imshow(matrix, cmap=get_cmap("gray"), interpolation="nearest")
show()

