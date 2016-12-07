import pytest
import json_processor
import pū
import hpk_statistics as hpks

'''
Test Headword Counts
'''

@pytest.fixture(scope="module")
def headwords():
    headwords = json_processor.get_headwords()
    assert len(headwords) == 13358
    return headwords

def test_headword_counts_vowels(headwords):
    for letter in tuple(set(pū.vowels) & set(pū.dictionary_letters)): 
        # (A, E, I, O, U) and their macronised equivalents
        letter_group = [x[0] for x in headwords if \
                        x[0].lower().startswith(letter.lower())]

        # include the macronised version too
        index_of_letter = pū.vowels.index(letter)
        macronised_letter = pū.macronised_vowels[index_of_letter]
        macronised_letter_group = [x[0] for x in headwords if \
                                   x[0].lower().startswith(macronised_letter.lower())] 
        vowel_letter_group = letter_group + macronised_letter_group
        assert len(vowel_letter_group) == hpks.headwords_counts[letter]


def test_headword_counts_digraphs(headwords):
    for letter in tuple(set(pū.digraphs) & set(pū.dictionary_letters)): 
        # (Ng, Wh)
        letter_group = [x[0] for x in headwords if \
                        x[0].lower().startswith(letter.lower())]
        assert len(letter_group) == hpks.headwords_counts[letter]


def test_headword_counts_consonants(headwords):
    # MUST be run AFTER test_headword_counts_digraphs because
    # we are relying on the results of that being OK to do this test
    for letter in tuple(set(pū.consonants) & set(pū.dictionary_letters)): 
        # ('H', 'K', 'M', 'N', 'P', 'R', 'T', 'W')
        letter_group = [x[0] for x in headwords if \
                        x[0].lower().startswith(letter.lower())]

        # 2 adjustments are necessary
        # 1 
        # So far this will undercount 'N' and 'R' due to the presence of 
        # -nei, -nā, rā which are included in the manual headword count
        # but are omitted at this point in the logic.

        
        # 2
        # So far this will overcount for 'W' and 'N'
        # because it will include 'Wh' and 'Ng' respectively

        # We are going to use the expected counts for Ng and Wh 
        # We are assuming they have already been tested as ok

        if letter == "W":
            letter_group_length = len(letter_group) - hpks.headwords_counts["Wh"]
        elif letter == "R":
            letter_group_length = len(letter_group) + 1
        elif letter == "N":
            letter_group_length = len(letter_group) - hpks.headwords_counts["Ng"]
            letter_group_length = letter_group_length + 2        
        else:
            letter_group_length = len(letter_group)             
        assert letter_group_length == hpks.headwords_counts[letter]
                        
