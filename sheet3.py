### Part 0: import libraries  ###

import numpy
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from scipy.stats import gumbel_r

### Part 1: Needleman-Wunsch ###

# Task 1: Implement the Needleman-Wunsch algorithm

# input: seq1 = Sequence 1 to align
#         seq2 = Sequence 2 to align
#         match_award = score for aligning identical caracters
#         gap_penalty = penalty for including a gap in the alignment
#         mismatch_penalty = penalty for aligning two different caracters
#         compute_aligment_string = Boolean to compute or not the aligmed sequences
#  output: dictionary:result = alignment score, aligned sequences 1 and 2(seq with gap "-"), perfectly aligment caracters) 

def needleman_wunsch_global(seq1,seq2, match_award, gap_penalty, mismatch_penalty, compute_aligment_string):
    results = {}
    # get length of two sequences
    m = len(seq1) # rows
    n = len(seq2) # columns
    # FIRST PART: Matrix initialization
    # Generate the empty matrix u
    matrix = numpy.zeros((m+1, n+1))
    # Fill the first column
    for i in range(0, m + 1):
        matrix[i][0] = gap_penalty * i
    # Fill the first row
    for j in range(0, n + 1):
        matrix[0][j] = gap_penalty * j
    # SECOND PART: Calculate alignment matrix
    for i in range(1, m + 1): # from the second row to the bottom
        for j in range(1, n + 1): # from second column to the right 
            # fill the matrix[i][j] cell with the highest score (diagonal,top,left) 
            if seq1[i-1] == seq2[j-1]:
                diagonal = match_award 
            else:
                diagonal = mismatch_penalty 
            score_diagonal = matrix[i - 1][j - 1] + diagonal
            score_delete = matrix[i - 1][j] + gap_penalty
            score_insert = matrix[i][j - 1] + gap_penalty
            matrix[i][j] = max(score_diagonal, score_delete, score_insert)
    results['score'] = matrix[m,n]
    # THIRD PART: Traceback to create alignment
    if compute_aligment_string:        
        # Traceback of the alignment 
        align1 =''
        align2 = ''
        # start from the bottom right cell
        i=m
        j=n 
        while i > 0 and j > 0: # end when it reachs the top or the left edge
            # find the neighbour cell (diagonal,top,left) with the highest score and move to this cell (modifying i and j)
             if seq1[i-1] == seq2[j-1]:
                diagonal = match_award 
            else:
                diagonal = mismatch_penalty            
            score_diagonal = matrix[i - 1][j - 1] + diagonal
            score_current = matrix[i][j]
            score_up = matrix[i][j-1]
            score_left = matrix[i-1][j]
            if score_current == score_diagonal:
                align1 += seq1[i-1]
                align2 += seq2[j-1]
                i -= 1
                j -= 1
            elif score_current == score_left + gap_penalty:
                align1 += seq1[i-1]
                align2 += '-'
                i -= 1
            elif score_current == score_up + gap_penalty:
                align1 += '-'
                align2 += seq2[j-1]
                j -= 1
        # Finish tracing up to the top left cell, do almost the same as before in case one aligned sequence is bigger than the other one)
       while i > 0:
            align1 += seq1[i-1]
            align2 += '-'
            i -= 1
        while j > 0:
            align1 += '-'
            align2 += seq2[j-1]
            j -= 1
        results["align1"] = align1
        results["align2"] = align2
    return results
    
    
# Task 2: Test the implementation

# define parameters
match_award      = 1
mismatch_penalty = -1
gap_penalty      = -1 

# define sequences to be aligned
seq1 ='FNMADSTEPNLPDSQESFSEFWCSSLQTNDFPNIVIDESALPATSNWQTYTTMAPVCSLLDIGAQINHGDDTGLFDFNVEAGELLGRRVVS'
seq2 ='MAVADTSELNFPDSQESFSDFWMNTLSENNELPSWQTDLNQEYDQCKETVDVLQLDTTKANDIEFPVSEFLTSSQASQQSIGDLFAQSLPS'

# test results 
results = needleman_wunsch_global(seq1,seq2,match_award,mismatch_penalty,gap_penalty, True)
reference_score = results['score']
for res, value in results.items():
    print(res, value)
    

