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
def sb0n_filepath():
    SB0N_AFF_FILE = "sb0n.aff"   
    return os.path.join(test_dicaff_files_path, SB0N_AFF_FILE)

@pytest.fixture(scope="module")
def sb0n_REP01_filepath():
    SB0N_REP01_AFF_FILE = "sb0n_REP01.aff"   
    return os.path.join(test_dicaff_files_path, SB0N_REP01_AFF_FILE)

@pytest.fixture(scope="module")
def sb0n_REP11_filepath():
    SB0N_REP11_AFF_FILE = "sb0n_REP11.aff"   
    return os.path.join(test_dicaff_files_path, SB0N_REP11_AFF_FILE)

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


@pytest.mark.xfail
def test_rep_1(hpk_dic_words, hpk_dic_filepath, sb0n_filepath,sb0n_REP01_filepath):
    hobj_sb0n = hunspell.HunSpell(hpk_dic_filepath, sb0n_filepath)
    hobj_sb0n_REP01 = hunspell.HunSpell(hpk_dic_filepath, sb0n_REP01_filepath)
    for word in hpk_dic_words:
        if not " " in word and not "-" in word:
            # Just test non-compound words, its easier
            sb0n_suggestions = [x.decode() for x in hobj_sb0n.suggest(word)]
            sb0n_REP01_suggestions = [x.decode() for x in \
                                      hobj_sb0n_REP01.suggest(word)]  
            print(word, "sb0n_suggestions", sb0n_suggestions)
            print(word, "sb0n_REP01_suggestions", sb0n_REP01_suggestions)
            assert sorted(sb0n_suggestions) == sorted(sb0n_REP01_suggestions)


@pytest.mark.xfail
def test_rep_2(hpk_dic_words, hpk_dic_filepath, sb0n_filepath, sb0n_REP11_filepath):
    hobj_sb0n = hunspell.HunSpell(hpk_dic_filepath, sb0n_filepath)
    hobj_sb0n_REP11 = hunspell.HunSpell(hpk_dic_filepath, sb0n_REP11_filepath)
    for word in hpk_dic_words:
        if not " " in word and not "-" in word:
            # Just test non-compound words, its easier
            sb0n_suggestions = [x.decode() for x in hobj_sb0n.suggest(word)]
            sb0n_REP11_suggestions = [x.decode() for x in \
                                      hobj_sb0n_REP11.suggest(word)]  
            print(word, "sb0n_suggestions", sb0n_suggestions)
            print(word, "sb0n_REP11_suggestions", sb0n_REP11_suggestions)
            assert sorted(sb0n_suggestions) == sorted(sb0n_REP11_suggestions)        
