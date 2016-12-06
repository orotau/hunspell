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
