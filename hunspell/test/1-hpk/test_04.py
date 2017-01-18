import pytest
import itertools
from collections import Counter
import json_processor_suffixes as jps
import pū
import hpk_statistics as hpks

'''
Check the counts of the regular and irregular suffixes themselves
Note that I haven't counted these by hand
So this test shall act as a baseline
'''

@pytest.fixture(scope="module")
def distinct_suffixes_for_word_form():
    return jps.get_distinct_suffixes_for_word_form()


@pytest.fixture(scope="module")
def kount(distinct_suffixes_for_word_form):
    '''
    A dictionary counting the number of times each regular and irregular
    suffix occurs.
    Note this fixture uses another fixture
    '''
    return Counter(itertools.chain.from_iterable(distinct_suffixes_for_word_form.values()))


def test_regular_suffixes_counts(kount):      
    regular_suffixes = {k: v for k, v in kount.items() if k.startswith('-')}
    for k, v in regular_suffixes.items():
        assert hpks.suffix_counts[k] == v
    
    # check the total number of regular suffixes
    assert sum(regular_suffixes.values()) == 12904           


def test_irregular_suffixes(kount):
    irregular_suffixes_counts = {k: v for k, v in kount.items() if not k.startswith('-')}

    # get the values
    irregular_suffixes_source = list(hpks.verbs_and_irregular_suffixes.values())

    # squash from a list of lists to a list
    irregular_suffixes_source = list(itertools.chain.from_iterable(irregular_suffixes_source))

    # check that the source count matches the count we have
    assert Counter(irregular_suffixes_source) == irregular_suffixes_counts

    # check the total number of words that have irregular suffixes
    assert len(hpks.verbs_and_irregular_suffixes) == 117

    # check total number of irregular suffixes
    assert sum(irregular_suffixes_counts.values()) == 139

    # check total number of unique irregular suffixes
    assert len(irregular_suffixes_counts) == 128
