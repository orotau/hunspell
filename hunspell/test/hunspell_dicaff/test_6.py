import os
import sys
import hunspell
import pytest

'''
Test Structure of .aff file
'''

@pytest.fixture(scope="module")
def hpk_dic_filepath():
    DIC_FILE = "hpk.dic"
    # goo.gl/LIkNeC (how to get a file in current directory)    
    return os.path.join(sys.path[0], DIC_FILE)

@pytest.fixture(scope="module")
def test_aff_filepath():
    AFF_FILE = "test.aff"
    # goo.gl/LIkNeC (how to get a file in current directory)    
    return os.path.join(sys.path[0], AFF_FILE)

@pytest.fixture(scope="module")
def test_aff_empty_filepath():
    AFF_FILE_EMPTY = "test_empty.aff"
    # goo.gl/LIkNeC (how to get a file in current directory)    
    return os.path.join(sys.path[0], AFF_FILE_EMPTY)

@pytest.fixture(scope="module")
def test_aff_break_0_filepath():
    AFF_FILE_BREAK_0 = "test_break_0.aff"
    # goo.gl/LIkNeC (how to get a file in current directory)    
    return os.path.join(sys.path[0], AFF_FILE_BREAK_0)

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
  

def test_dic_file_encoding(hpk_dic_filepath, test_aff_empty_filepath):
    hobj = hunspell.HunSpell(hpk_dic_filepath, test_aff_empty_filepath)
    assert hobj.get_dic_encoding() == "banana"

def test_break_default(hpk_dic_filepath, test_aff_empty_filepath):
    # This shows the importance of setting BREAK 0 in the .aff file
    # The default results in 'new' words being marked ok
    # in this case "awa-kai" and "kai-awa"    
    hobj = hunspell.HunSpell(hpk_dic_filepath, test_aff_empty_filepath)
    assert hobj.spell("awa") == True
    assert hobj.spell("kai") == True    
    assert hobj.spell("awa-kai") == True
    assert hobj.spell("kai-awa") == True

def test_break_0(hpk_dic_filepath, test_aff_break_0_filepath):
    # This shows the importance of setting BREAK 0 in the .aff file
    # The BREAK 0 results in 'new' words being marked WRONG
    # in this case "awa-kai" and "kai-awa"    
    hobj = hunspell.HunSpell(hpk_dic_filepath, test_aff_break_0_filepath)
    assert hobj.spell("awa") == True
    assert hobj.spell("kai") == True    
    assert hobj.spell("awa-kai") == False
    assert hobj.spell("kai-awa") == False

def test_open_compound(hpk_dic_filepath, test_aff_empty_filepath):
    hobj = hunspell.HunSpell(hpk_dic_filepath, test_aff_empty_filepath)
    assert hobj.spell("au") == True
    assert hobj.spell("mārō") == True    
    assert hobj.spell("au mārō") == True
    assert hobj.spell("au-mārō") == True







    
                        
