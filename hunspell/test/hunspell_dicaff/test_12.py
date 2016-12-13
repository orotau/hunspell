import os
import config
from random import shuffle
import hunspell
import pytest

cf = config.ConfigFile()
test_dicaff_files_path = (cf.configfile[cf.computername]['test_dicaff_files_path'])

'''
Test Suggestions
'''

@pytest.fixture(scope="module")
def hpk_dic_filepath():
    DIC_FILE = "hpk.dic"
    return os.path.join(test_dicaff_files_path, DIC_FILE)

@pytest.fixture(scope="module")
def baseline_aff_filepath():
    BASELINE_AFF_FILE = "baseline.aff"   
    return os.path.join(test_dicaff_files_path, BASELINE_AFF_FILE)

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

def test_closed_compound_sugs(hpk_dic_words, hpk_dic_filepath, baseline_aff_filepath):
    hobj = hunspell.HunSpell(hpk_dic_filepath, baseline_aff_filepath)
    for word in hpk_dic_words:
        if "-" in word and not " " in word:
            # closed compounds
            word_with_spaces = word.replace("-"," ")
            suggestions = [x.decode() for x in hobj.suggest(word_with_spaces)]
            for suggestion in suggestions:
                if suggestion.lower() in [x.lower() for x in hpk_dic_words]:
                    print(word_with_spaces, suggestion)
                else:
                    if hobj.spell(suggestion) == True:
                        print("Not in dic but deemed OK", suggestion) 
                        assert False
            
