import pytest
import json_processor_suffixes as jps
import pū
import hpk_statistics as hpks

'''
Check the counts of those words that have at least 1 suffix
Note that I haven't counted these by hand
So this test shall act as a baseline
'''

@pytest.fixture(scope="module")
def distinct_suffixes_for_word_form():
    distinct_suffixes_for_word_form = jps.get_distinct_suffixes_for_word_form()
    assert len(distinct_suffixes_for_word_form) == 6567
    return distinct_suffixes_for_word_form

def test_suffixes_counts_vowels(distinct_suffixes_for_word_form):
    for letter in tuple(set(pū.vowels) & set(pū.dictionary_letters)): 
        # (A, E, I, O, U) and their macronised equivalents
        letter_group = ([k for k in distinct_suffixes_for_word_form.keys() 
                         if k.lower().startswith(letter.lower())])

        index_of_letter = pū.vowels.index(letter)
        macronised_letter = pū.macronised_vowels[index_of_letter]
        macronised_letter_group = ([k for k in distinct_suffixes_for_word_form.keys() 
                                    if k.lower().startswith(macronised_letter.lower())])
        vowel_letter_group = letter_group + macronised_letter_group
        assert len(vowel_letter_group) == hpks.words_with_suffix_counts[letter]


def test_suffixes_counts_digraphs(distinct_suffixes_for_word_form):
    for letter in tuple(set(pū.digraphs) & set(pū.dictionary_letters)): 
        # (Ng, Wh)
        letter_group = ([k for k in distinct_suffixes_for_word_form.keys() 
                         if k.lower().startswith(letter.lower())])
        assert len(letter_group) == hpks.words_with_suffix_counts[letter]

def test_suffixes_counts_consonants(distinct_suffixes_for_word_form):
    # MUST be run AFTER test_headword_counts_digraphs because
    # we are relying on the results of that being OK to do this test
    for letter in tuple(set(pū.consonants) & set(pū.dictionary_letters)): 
        # ('H', 'K', 'M', 'N', 'P', 'R', 'T', 'W')
        letter_group = ([k for k in distinct_suffixes_for_word_form.keys() 
                         if k.lower().startswith(letter.lower())])

        # 1 adjustment is necessary
        # 1
        # So far this will overcount for 'W' and 'N'
        # because it will include 'Wh' and 'Ng' respectively

        # We are going to use the expected counts for Ng and Wh 
        # We are assuming they have already been tested as ok

        if letter == "W":
            letter_group_length = len(letter_group) - hpks.words_with_suffix_counts["Wh"]
        elif letter == "N":
            letter_group_length = len(letter_group) - hpks.words_with_suffix_counts["Ng"]     
        else:
            letter_group_length = len(letter_group) 
           
        assert letter_group_length == hpks.words_with_suffix_counts[letter]               
