import pytest
import json_processor_hunspell as jph
import hpk_statistics as hpks

'''
Test Words for Hunspell
'''

@pytest.fixture(scope="module")
def basewords():
    all_basewords = jph.get_all_base_words()
    assert len(all_basewords) == 13392
    return all_basewords

@pytest.fixture(scope="module")
def suffixed_words():
    all_suffixed_words, all_distinct_suffixed_words = jph.get_all_suffixed_words()   
    return all_suffixed_words, all_distinct_suffixed_words

@pytest.fixture(scope="module")
def irregular_verbs():
    all_irregular_verbs, all_distinct_irregular_verbs = jph.get_all_irregular_verbs()   
    return all_irregular_verbs, all_distinct_irregular_verbs

@pytest.fixture(scope="module")
def all_words_for_hunspell():
    return jph.get_all_words_for_hunspell()   

def test_basewords_unique(basewords):
    assert len(basewords) == len(set(basewords))

def test_suffixed_words(suffixed_words):
    assert len(suffixed_words[0]) >= len(suffixed_words[1])
    assert len(suffixed_words[0]) == sum(hpks.suffix_counts.values())

    # this test assume that each duplicate occurs only twice (no more)
    assert len(suffixed_words[1]) == sum(hpks.suffix_counts.values()) - \
                                     len(hpks.duplicated_suffixed_words)

def test_irregular_verbs(irregular_verbs):
    assert len(irregular_verbs[0]) >= len(irregular_verbs[1])
    # the numbers have already been tested

def test_intersection_basewords_suffixed_words(basewords, suffixed_words):
    assert len(set(basewords) & set(suffixed_words[1])) == 206 # computed number

def test_intersection_basewords_irregular_verbs(basewords, irregular_verbs):
    assert len(set(basewords) & set(irregular_verbs[1])) == 25 # computed number 

def test_intersection_suffixed_words_irregular_verbs(suffixed_words, irregular_verbs):
    assert len(set(suffixed_words[1]) & set(irregular_verbs[1])) == 40 # computed number

def test_intersection_all(basewords, suffixed_words, irregular_verbs):
    assert len(set(suffixed_words[1]) & \
               set(basewords) & \
               set(irregular_verbs[1])) == 7 # computed number

def test_all_words_for_hunspell(all_words_for_hunspell):
    assert len(all_words_for_hunspell) == 1
    
                        
