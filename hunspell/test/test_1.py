import pytest
import pataka
import pū
import hpk_statistics

@pytest.fixture
def headwords():
    return pataka.get_headwords()

def test_1(headwords):
    for letter in pū.dictionary_letters:
          
    assert 1 == 2
