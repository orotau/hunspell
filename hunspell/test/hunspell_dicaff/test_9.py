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
def sb0n_REP20_filepath():
    SB0N_REP20_AFF_FILE = "sb0n_REP20.aff"   
    return os.path.join(test_dicaff_files_path, SB0N_REP20_AFF_FILE)

@pytest.fixture(scope="module")
def sb0n_REP10_filepath():
    SB0N_REP10_AFF_FILE = "sb0n_REP10.aff"   
    return os.path.join(test_dicaff_files_path, SB0N_REP10_AFF_FILE)

@pytest.fixture(scope="module")
def sb0n_REP10_MAP5_filepath():
    SB0N_REP10_MAP5_AFF_FILE = "sb0n_REP10_MAP5.aff"   
    return os.path.join(test_dicaff_files_path, SB0N_REP10_MAP5_AFF_FILE)

@pytest.fixture(scope="module")
def sb0n_REP10D_MAP5_filepath():
    SB0N_REP10D_MAP5_AFF_FILE = "sb0n_REP10D_MAP5.aff"   
    return os.path.join(test_dicaff_files_path, SB0N_REP10D_MAP5_AFF_FILE)

@pytest.fixture(scope="module")
def sb0n_MAP5_REP10D_filepath():
    SB0N_MAP5_REP10D_AFF_FILE = "sb0n_MAP5_REP10D.aff"   
    return os.path.join(test_dicaff_files_path, SB0N_MAP5_REP10D_AFF_FILE)

@pytest.fixture(scope="module")
def sb0n_REP20_MAP5_filepath():
    SB0N_REP20_MAP5_AFF_FILE = "sb0n_REP20_MAP5.aff"   
    return os.path.join(test_dicaff_files_path, SB0N_REP20_MAP5_AFF_FILE)

@pytest.fixture(scope="module")
def sb0n_MAP5_filepath():
    SB0N_MAP5_AFF_FILE = "sb0n_MAP5.aff"   
    return os.path.join(test_dicaff_files_path, SB0N_MAP5_AFF_FILE)

@pytest.fixture(scope="module")
def sb0n_REP20_MAP10_filepath():
    SB0N_REP20_MAP10_AFF_FILE = "sb0n_REP20_MAP10.aff"   
    return os.path.join(test_dicaff_files_path, SB0N_REP20_MAP10_AFF_FILE)

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

'''
@pytest.mark.xfail
def test_map(hpk_dic_words, hpk_dic_filepath, sb0n_REP20_filepath, sb0n_REP20_MAP5_filepath):
    hobj_sb0n_REP20 = hunspell.HunSpell(hpk_dic_filepath, sb0n_REP20_filepath)
    hobj_sb0n_REP20_MAP5 = hunspell.HunSpell(hpk_dic_filepath, sb0n_REP20_MAP5_filepath)
    for word in hpk_dic_words:
        if not " " in word and not "-" in word:
            word_as_list = list(word)
            shuffle(word_as_list)
            jumbled_word = ''.join(word_as_list)
            if jumbled_word not in hpk_dic_words:
            # Just test non-compound words, its easier
                sb0n_REP20_suggestions = [x.decode() for x in \
                                          hobj_sb0n_REP20.suggest   (jumbled_word)]
                sb0n_REP20_MAP5_suggestions = [x.decode() for x in \
                                               hobj_sb0n_REP20_MAP5.suggest(jumbled_word)]  
                print(jumbled_word, "sb0n_REP20_suggestions", sb0n_REP20_suggestions)
                print(jumbled_word, "sb0n_REP20_MAP5_suggestions", sb0n_REP20_MAP5_suggestions)
                assert sorted(sb0n_REP20_suggestions) == sorted(sb0n_REP20_MAP5_suggestions)  

@pytest.mark.xfail
def test_map(hpk_dic_words, hpk_dic_filepath, sb0n_REP20_MAP5_filepath, sb0n_REP20_MAP10_filepath):
    hobj_sb0n_REP20_MAP5 = hunspell.HunSpell(hpk_dic_filepath, sb0n_REP20_MAP5_filepath)
    hobj_sb0n_REP20_MAP10 = hunspell.HunSpell(hpk_dic_filepath, sb0n_REP20_MAP10_filepath)
    for word in hpk_dic_words:
        if not " " in word and not "-" in word:
            word_as_list = list(word)
            shuffle(word_as_list)
            jumbled_word = ''.join(word_as_list)
            if jumbled_word not in hpk_dic_words:
            # Just test non-compound words, its easier
                sb0n_REP20_MAP5_suggestions = [x.decode() for x in \
                                               hobj_sb0n_REP20_MAP5.suggest(jumbled_word)]
                sb0n_REP20_MAP10_suggestions = [x.decode() for x in \
                                               hobj_sb0n_REP20_MAP10.suggest(jumbled_word)]  
                print(jumbled_word, "sb0n_REP20_MAP5_suggestions", sb0n_REP20_MAP5_suggestions)
                print(jumbled_word, "sb0n_REP20_MAP10_suggestions", sb0n_REP20_MAP10_suggestions)
                assert sorted(sb0n_REP20_MAP5_suggestions) == sorted(sb0n_REP20_MAP10_suggestions)  
''' 

'''
Some examples of where test_map fails
Clearly we need MAP5

If we have MAP5 do we need REP10?
ānō
nōā sb0n_REP10_suggestions ['nō', 'nā', 'ānō'] - show stopper no 'noa'
nōā sb0n_MAP5_suggestions ['noa', 'nō', 'nā', 'ānō']

akitō
kiatō sb0n_REP10_suggestions ['kiato', 'akitō'] - show stopper no 'kīato'
kiatō sb0n_MAP5_suggestions ['kiato', 'kīato', 'akitō']

āwhā
hāwā sb0n_REP10_suggestions ['āwhā', 'wāwā'] - show stopper no 'hawa'
hāwā sb0n_MAP5_suggestions ['hawa', 'āwhā']


@pytest.mark.xfail
def test_map(hpk_dic_words, hpk_dic_filepath, sb0n_REP10_filepath, sb0n_MAP5_filepath):
    hobj_sb0n_REP10 = hunspell.HunSpell(hpk_dic_filepath, sb0n_REP10_filepath)
    hobj_sb0n_MAP5 = hunspell.HunSpell(hpk_dic_filepath, sb0n_MAP5_filepath)
    for word in hpk_dic_words:
        if not " " in word and not "-" in word:
            word_as_list = list(word)
            shuffle(word_as_list)
            jumbled_word = ''.join(word_as_list)
            if jumbled_word not in hpk_dic_words:
            # Just test non-compound words, its easier
                sb0n_REP10_suggestions = [x.decode() for x in \
                                          hobj_sb0n_REP10.suggest(jumbled_word)]
                sb0n_MAP5_suggestions = [x.decode() for x in \
                                         hobj_sb0n_MAP5.suggest(jumbled_word)]  
                print(word)
                print(jumbled_word, "sb0n_REP10_suggestions", sb0n_REP10_suggestions)
                print(jumbled_word, "sb0n_MAP5_suggestions", sb0n_MAP5_suggestions)
                assert sorted(sb0n_REP10_suggestions) == sorted(sb0n_MAP5_suggestions)
'''

'''
map_2 below show the same results from 
MAP5 and REP10_MAP5 so MAP5 by itself is all that is needed

Note that when I originally did this test the set up of the file
REP10_MAP5 had 'REP 20' - This made the file misbehave.
Need to put in place something to check that the number of REPs is as 
advertised.



@pytest.mark.xfail
def test_map_2(hpk_dic_words, hpk_dic_filepath, sb0n_REP10_MAP5_filepath, sb0n_MAP5_filepath):
    hobj_sb0n_REP10_MAP5 = hunspell.HunSpell(hpk_dic_filepath, sb0n_REP10_MAP5_filepath)
    hobj_sb0n_MAP5 = hunspell.HunSpell(hpk_dic_filepath, sb0n_MAP5_filepath)
    for word in hpk_dic_words:
        if not " " in word and not "-" in word:
            word_as_list = list(word)
            shuffle(word_as_list)
            jumbled_word = ''.join(word_as_list)
            if jumbled_word not in hpk_dic_words:
            # Just test non-compound words, its easier
                sb0n_REP10_MAP5_suggestions = [x.decode() for x in \
                                          hobj_sb0n_REP10_MAP5.suggest(jumbled_word)]
                sb0n_MAP5_suggestions = [x.decode() for x in \
                                         hobj_sb0n_MAP5.suggest(jumbled_word)]  
                print(word)
                print(jumbled_word, "sb0n_REP10_MAP5_suggestions", sb0n_REP10_MAP5_suggestions)
                print(jumbled_word, "sb0n_MAP5_suggestions", sb0n_MAP5_suggestions)
                assert sorted(sb0n_REP10_MAP5_suggestions) == sorted(sb0n_MAP5_suggestions)
'''

'''
ama
maa sb0n_REP10D_MAP5_suggestions ['mā', 'ama']
maa sb0n_MAP5_suggestions ['ama', 'maua'] - Show stopper, no 'mā'


@pytest.mark.xfail
def test_map_2(hpk_dic_words, hpk_dic_filepath, sb0n_REP10D_MAP5_filepath, sb0n_MAP5_filepath):
    hobj_sb0n_REP10D_MAP5 = hunspell.HunSpell(hpk_dic_filepath, sb0n_REP10D_MAP5_filepath)
    hobj_sb0n_MAP5 = hunspell.HunSpell(hpk_dic_filepath, sb0n_MAP5_filepath)
    for word in hpk_dic_words:
        if not " " in word and not "-" in word:
            word_as_list = list(word)
            shuffle(word_as_list)
            jumbled_word = ''.join(word_as_list)
            if jumbled_word not in hpk_dic_words:
            # Just test non-compound words, its easier
                sb0n_REP10D_MAP5_suggestions = [x.decode() for x in \
                                          hobj_sb0n_REP10D_MAP5.suggest(jumbled_word)]
                sb0n_MAP5_suggestions = [x.decode() for x in \
                                         hobj_sb0n_MAP5.suggest(jumbled_word)]  
                print(word)
                print(jumbled_word, "sb0n_REP10D_MAP5_suggestions", sb0n_REP10D_MAP5_suggestions)
                print(jumbled_word, "sb0n_MAP5_suggestions", sb0n_MAP5_suggestions)
                assert sorted(sb0n_REP10D_MAP5_suggestions) == sorted(sb0n_MAP5_suggestions)
'''

'''
This test shows that the order of the MAP and the REP is irrelevant
@pytest.mark.xfail
def test_map_2(hpk_dic_words, hpk_dic_filepath, sb0n_REP10D_MAP5_filepath, sb0n_MAP5_REP10D_filepath):
    hobj_sb0n_REP10D_MAP5 = hunspell.HunSpell(hpk_dic_filepath, sb0n_REP10D_MAP5_filepath)
    hobj_sb0n_MAP5_REP10D = hunspell.HunSpell(hpk_dic_filepath, sb0n_MAP5_REP10D_filepath)
    for word in hpk_dic_words:
        if not " " in word and not "-" in word:
            word_as_list = list(word)
            shuffle(word_as_list)
            jumbled_word = ''.join(word_as_list)
            if jumbled_word not in hpk_dic_words:
            # Just test non-compound words, its easier
                sb0n_REP10D_MAP5_suggestions = [x.decode() for x in \
                                          hobj_sb0n_REP10D_MAP5.suggest(jumbled_word)]
                sb0n_MAP5_REP10D_suggestions = [x.decode() for x in \
                                         hobj_sb0n_MAP5_REP10D.suggest(jumbled_word)]  
                print(word)
                print(jumbled_word, "sb0n_REP10D_MAP5_suggestions", sb0n_REP10D_MAP5_suggestions)
                print(jumbled_word, "sb0n_MAP5_REP10D_suggestions", sb0n_MAP5_REP10D_suggestions)
                assert sorted(sb0n_REP10D_MAP5_suggestions) == sorted(sb0n_MAP5_REP10D_suggestions)
'''
