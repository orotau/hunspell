import pytest
import json_processor
import pū
import hpk_statistics as hpks

'''
Check the subentry (aka twig) counts
Note that I haven't counted these by hand
So this test shall act as a baseline
'''

@pytest.fixture(scope="module")
def twigs():
    twigs = json_processor.get_twigs(words_only = False)
    assert len(twigs) == 1522
    return twigs

def test_twigs_counts_vowels(twigs):
    for letter in tuple(set(pū.vowels) & set(pū.dictionary_letters)): 
        # (A, E, I, O, U) and their macronised equivalents
        letter_group = ([k.twig for k in twigs.keys() 
                         if k.trunk.lower().startswith(letter.lower())])

        index_of_letter = pū.vowels.index(letter)
        macronised_letter = pū.macronised_vowels[index_of_letter]
        macronised_letter_group = ([k.twig for k in twigs.keys() 
                                    if k.trunk.lower().startswith(macronised_letter.lower())])
        vowel_letter_group = letter_group + macronised_letter_group
        assert len(vowel_letter_group) == hpks.twigs_counts[letter]


def test_twigs_counts_digraphs(twigs):
    for letter in tuple(set(pū.digraphs) & set(pū.dictionary_letters)): 
        # (Ng, Wh)
        letter_group = ([k.twig for k in twigs.keys() 
                         if k.trunk.lower().startswith(letter.lower())])
        assert len(letter_group) == hpks.twigs_counts[letter]

def test_twigs_counts_consonants(twigs):
    # MUST be run AFTER test_headword_counts_digraphs because
    # we are relying on the results of that being OK to do this test
    for letter in tuple(set(pū.consonants) & set(pū.dictionary_letters)): 
        # ('H', 'K', 'M', 'N', 'P', 'R', 'T', 'W')
        letter_group = ([k.twig for k in twigs.keys() 
                         if k.trunk.lower().startswith(letter.lower())])

        # 1 adjustment is necessary
        # 1
        # So far this will overcount for 'W' and 'N'
        # because it will include 'Wh' and 'Ng' respectively

        # We are going to use the expected counts for Ng and Wh 
        # We are assuming they have already been tested as ok

        if letter == "W":
            letter_group_length = len(letter_group) - hpks.twigs_counts["Wh"]
        elif letter == "N":
            letter_group_length = len(letter_group) - hpks.twigs_counts["Ng"]     
        else:
            letter_group_length = len(letter_group) 
        print(letter)            
        assert letter_group_length == hpks.twigs_counts[letter]                     
