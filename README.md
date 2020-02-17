# Smith-Waterman 
> As part of a speech recognition project to extract usable training data from speech data with noisy reference transcriptions, I reimplemented the (striped) Smith-Waterman (SSW) that was used to create the LibriSpeech corpus. There's a lot of copy pasta from other implementations and the only change I made was that I needed the implementation to work on lists instead of a string of characters which is common because the algorithm was invented to align DNA sequences.


## Install

`pip install smithwaterman`

## How to use

A single function exposes the necessary functionality:

`startposition, aligned_subsequences = smith_waterman(hypothesis, reference, match_score=3, gap_cost=2)`
e.g.

```python
start_position, aligned = smithwaterman('Den uheldige politimand fanger aldrig sin lykkes smed'.split(),
                                         'Den uheldige postmand finder aldrig sin lykkes smed'.split())
```

`start_position` is the start of the first aligned subsequence and `aligned` is a list of aligned sub sequences:

```python
for i, subsequence in enumerate(aligned):
    pretty = ' '.join(subsequence)
    print(f'Sub sequence {i}: {pretty}')
```

    Sub sequence 0: DEN UHELDIGE
    Sub sequence 1: SIN LYKKES SMED


The `smithwaterman()` function is designed to work on list, but will also work on strings:

```python
start_position, aligned = smithwaterman('Den uheldige politimand fanger aldrig sin lykkes smed',
                                         'Den uheldige postmand finder aldrig sin lykkes smed')
[''.join(string) for string in aligned]
```




    ['DEN UHELDIGE PO', 'AND F', 'N', 'ER ALDRIG SIN LYKKES SMED']



## Optional arguments

The `match_score` and `gap_cost` arguments are parameters that can be used to tweak the alignment. Increasing `match_score` and decreasing `gap_cost` improves the word alignment in our example:

```python
start_position, aligned = smithwaterman('Den uheldige politimand fanger aldrig sin lykkes smed'.split(),
                                         'Den uheldige postmand finder aldrig sin lykkes smed'.split(),
                                      match_score=4, gap_cost=1)
[' '.join(string) for string in aligned]
```




    ['DEN UHELDIGE', 'ALDRIG SIN LYKKES SMED']



Decreasing `match_score` and increasing the `gap_cost` will reduce the number of aligned subsequences:

```python
start_position, aligned = smithwaterman('Den uheldige politimand fanger aldrig sin lykkes smed',
                                         'Den uheldige postmand finder aldrig sin lykkes smed',
                                      match_score=1, gap_cost=4)
[''.join(string) for string in aligned]
```




    ['DEN UHELDIGE PO', ' ALDRIG SIN LYKKES SMED']



So a high `match_score` vs. low `gap_cost` will cause the algorithm to align more/longer sequences and a low `match_score` vs. high `gap_cost` will result in fewer aligned sequences. However, the alignments are likely better.

`gap_cost` is an umbrella term for deletions and insertions (think edit distance) and here the gap costs are linear, i.e. the costs for both operations are the same.
