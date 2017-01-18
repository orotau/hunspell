import os
import config
from random import shuffle
import hunspell
import pytest

cf = config.ConfigFile()
test_dicaff_files_path = (cf.configfile[cf.computername]['dicaff_files_path'])

'''
Test Best Structure of .aff file
NOSPLITSUGS being tested
'''

@pytest.fixture(scope="module")
def hpk_dic_filepath():
    DIC_FILE = "hpk.dic"
    return os.path.join(test_dicaff_files_path, DIC_FILE)

@pytest.fixture(scope="module")
def test_set_break_0_filepath():
    AFF_FILE = "test_set_break_0.aff"   
    return os.path.join(test_dicaff_files_path, AFF_FILE)

@pytest.fixture(scope="module")
def hpk_dic_words(hpk_dic_filepath):
    hpk_dic_words = []
    # Open the .dic file and read all lines *except the first* into a list
    # Check that the number of words = The Number in the first line
    with open(hpk_dic_filepath, "r") as f:
        for line in f:
            line_to_add = line.replace('\n', '')
            try:
                int(line_to_add) # first line should contain an integer
            except:
                hpk_dic_words.append(line_to_add)
            else:
                first_line = int(line_to_add)
    assert len(hpk_dic_words) == first_line
    return hpk_dic_words

@pytest.mark.skip(reason="Test used in creating the baseline aff file")
@pytest.mark.xfail
def test_splitsugs(hpk_dic_words, hpk_dic_filepath, test_set_break_0_filepath):
    # This shows the problem of *not* setting NOSPLITSUGS - i.e using default
    # we get suggestions that are not in the dictionary
    hobj = hunspell.HunSpell(hpk_dic_filepath, test_set_break_0_filepath)
    for word in hpk_dic_words:
        if not " " in word and not "-" in word:
            # Just test non-compound words, its easier
            word_as_list = list(word)
            shuffle(word_as_list)
            jumbled_word = ''.join(word_as_list)
            suggestions = [x.decode() for x in hobj.suggest(jumbled_word)]
            for suggestion in suggestions:
                if hobj.spell(suggestion) == True:
                    # sugggestion in dictionary
                    pass
                else:
                    print("Not in dictionary", suggestion)
                    assert False          
