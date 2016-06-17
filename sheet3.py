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
    
    
### Part 2: Alignment signifiance using permutation test and Gumble distribution ### 

# Task 1: Randomly shuffle a given sequence string
def shuffle_sequence(string):
    return ''.join(random.sample(string,len(string)))
    
# Task 2: Generate a reference score and calculate the score for 1000 randomly shuffled sequences

# use previously defined parameters and sequences

reference_score = results['score']
permutation_scores = []

# calcuate the permutation scores for 1000 times reshuffeled sequences
for i in range(0,1000):
    shuffle_seq1 = shuffle_sequence(seq1)
    shuffle_seq2 = shuffle_sequence(seq2)
    shuffle_results = needleman_wunsch_global(shuffle_seq1,shuffle_seq2,match_award,mismatch_penalty,gap_penalty, False)
    permutation_scores.append(shuffle_results['score'])
print(permutation_scores[0])

# Task 3: Plot a histogram of the calculated permutation scores

plt.hist(permutation_scores)
plt.title("Score distribution")
plt.xlabel("Score")
plt.ylabel("Frequency")
plt.axvline(reference_score)
plt.show()

# Task 4: Compute the associate p-value for the reference score
# estimate whether our reference score is part of scores produced when randomly shuffeling the sequences, we will estimate its p-value

# p_value = number of samples bigger than the reference + 1 for the reference / numbers of samples + 1 for the reference

number_value_smaller = 0
# calculate the number of samples smaller than the reference score
for score in permutation_scores:
    if score < reference_score:
        number_value_smaller +=1
# estimate the number of total samples + 1
number_samples = len(permutation_scores) +1
# calculate the p-value
p_value = 1-(float(number_value_smaller) / float(number_samples))
print(p_value )

# Task 5: Compute the associate p-value using an estimated gumble distribution

# estimate the parameter loc and scale using the fit function
loc,scale = gumbel_r.fit(permutation_scores)

# calculate the p-value
p_value = 1-gumbel_r.cdf(reference_score, loc=loc, scale=scale )
print(p_value)


# Task 6: Plot the histogram and the fitted probability density function with the reference score as vertical line

fig, ax = plt.subplots(1, 1)
x = np.linspace(gumbel_r.ppf(0.01,loc=loc, scale=scale),gumbel_r.ppf(0.99,loc=loc, scale=scale), 1000)

ax.plot(x, gumbel_r.pdf(x, loc=loc, scale=scale), 'k-', lw=2, label='frozen pdf')
ax.hist(permutation_scores, normed=True, histtype='stepfilled', alpha=0.2)
ax.legend(loc='best', frameon=False)
ax.axvline(reference_score)
plt.show()
