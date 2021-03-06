# AUTOGENERATED! DO NOT EDIT! File to edit: 00_core.ipynb (unless otherwise specified).

__all__ = ['words2ints', 'traceback', 'matrix', 'smithwaterman']

# Cell
import itertools
import numpy as np

# Cell
def words2ints(list_of_strings):
    """Map unique words to integer IDs"""
    wordlist = set([])
    for strings in list_of_strings:
        wordlist.update(strings.split())
    w2i = {k: str(v) for v, k in enumerate(wordlist)}
    return w2i

# Cell
def traceback(score_matrix, sequence_b, aligned_sequence=None, old_i=0):
    """Trace back the best alignments for subsequences of a and b sequences"""
    if aligned_sequence is None:
        aligned_sequence = [[]]
    # flip H to get index of **last** occurrence of score_matrix.max() with np.argmax()
    matrix_flip = np.flip(np.flip(score_matrix, 0), 1)
    # np.argmax() returns an index into a flattened array
    # np.unravel_index translates that into a coordinate into matrix_flip
    i_flip, j_flip = np.unravel_index(matrix_flip.argmax(), matrix_flip.shape)
    # Translate the coordinates into matrix_flip into coordinates into
    # score_matrix: (i, j) are the last indexes of H.max()
    # np.subtract is element-wise
    i, j = np.subtract(score_matrix.shape, (i_flip + 1, j_flip + 1))
    # Termination: we reached a gap in the alignment
    if score_matrix[i, j] == 0:
        # be will be the string that has been
        # compiled during the recursion below
        return [seq[::-1] for seq in aligned_sequence[::-1]], j
    # Traceback happens
    if old_i - i > 1:
        # A delete or insert operation == gap
        # aligned_sequence = sequence_b[j - 1] + '-' + aligned_sequence
        aligned_sequence.append([sequence_b[j - 1]])
    else:
        # Alignment continues
        # aligned_sequence = sequence_b[j - 1] + aligned_sequence
        aligned_sequence[-1].append(sequence_b[j - 1])

    # Recurse
    return traceback(score_matrix[0:i, 0:j], sequence_b, aligned_sequence, i)

# Cell
def matrix(sequence_a, sequence_b, match_score=3, gap_cost=2):
    """Create a score matrix from the two sequences that we are aligning. Define the
    match score and gap cost, then fill the matrix.
    The gap cost is linear: delete and insert operations cost the same"""

    # Everything that is not a match is a zero
    # Why do we make the length of the sequences longer?
    score_matrix = np.zeros((len(sequence_a) + 1, len(sequence_b) + 1), np.int)

    for i, j in itertools.product(range(1, score_matrix.shape[0]), range(1, score_matrix.shape[1])):
        # add match_score if the previous elements in the sequences match else subtract match_score
        match = score_matrix[i - 1, j - 1] \
            + (match_score if sequence_a[i - 1] == sequence_b[j - 1] else - match_score)
        # subtract the gap_cost - insertions/deletions depends on which
        # is the source and which is the target sequence
        delete = score_matrix[i - 1, j] - gap_cost
        insert = score_matrix[i, j - 1] - gap_cost
        # Insert the highest score as the value for the traceback
        score_matrix[i, j] = max(match, delete, insert, 0)
    return score_matrix

# Cell
def smithwaterman(hypothesis, reference, match_score=3, gap_cost=2):
    """High-level function that implements SW alignment with linear
    gap cost. Returns all local alignments"""
    hypo, ref = [h.upper() for h in hypothesis], [r.upper() for r in reference]
    score_matrix = matrix(hypo, ref, match_score, gap_cost)
    aligned_sequence_with_gaps, pos = traceback(score_matrix, ref)
    return pos, aligned_sequence_with_gaps