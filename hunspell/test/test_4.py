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
    distinct_suffixes_for_word_form = jps.get_distinct_suffixes_for_word_form()
    return distinct_suffixes_for_word_form

def test_suffixes_counts(distinct_suffixes_for_word_form):
    c = Counter(itertools.chain.from_iterable(distinct_suffixes_for_word_form.values()))
    print (c)
    assert 1 == 2
                
