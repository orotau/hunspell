import os
import config
import hunspell
import pytest

cf = config.ConfigFile()
test_dicaff_files_path = (cf.configfile[cf.computername]['test_dicaff_files_path'])

'''
Test number of entries in the dic file hpk.dic = number at top of file
Test Best Structure of .aff file
Coding and Break being tested
'''

@pytest.fixture(scope="module")
def hpk_dic_filepath():
    DIC_FILE = "hpk.dic"
    return os.path.join(test_dicaff_files_path, DIC_FILE)

@pytest.fixture(scope="module")
def test_aff_filepath():
    AFF_FILE = "test.aff"   
    return os.path.join(test_dicaff_files_path, AFF_FILE)

@pytest.fixture(scope="module")
def test_aff_empty_filepath():
    AFF_FILE_EMPTY = "test_empty.aff"
    return os.path.join(test_dicaff_files_path, AFF_FILE_EMPTY)

@pytest.fixture(scope="module")
def test_aff_set_only_filepath():
    AFF_FILE_SET_ONLY = "test_set_only.aff"
    return os.path.join(test_dicaff_files_path, AFF_FILE_SET_ONLY)

@pytest.fixture(scope="module")
def test_aff_break_0_only_filepath():
    AFF_FILE_BREAK_0_ONLY = "test_break_0_only.aff"
    return os.path.join(test_dicaff_files_path, AFF_FILE_BREAK_0_ONLY)

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
def test_dic_file_encoding(hpk_dic_filepath, test_aff_empty_filepath):
    hobj = hunspell.HunSpell(hpk_dic_filepath, test_aff_empty_filepath)
    assert hobj.get_dic_encoding() == 'ISO8859-1' # default

@pytest.mark.skip(reason="Test used in creating the baseline aff file")
def test_dic_file_encoding(hpk_dic_filepath, test_aff_set_only_filepath):
    hobj = hunspell.HunSpell(hpk_dic_filepath, test_aff_set_only_filepath)
    assert hobj.get_dic_encoding() == 'UTF-8'

@pytest.mark.skip(reason="Test used in creating the baseline aff file")
def test_break_default(hpk_dic_filepath, test_aff_empty_filepath):
    # This shows the importance of setting BREAK 0 in the .aff file
    # The default results in 'new' words being marked ok
    # in this case "awa-kai" and "kai-awa"    
    hobj = hunspell.HunSpell(hpk_dic_filepath, test_aff_empty_filepath)
    assert hobj.spell("awa") == True
    assert hobj.spell("kai") == True    
    assert hobj.spell("awa-kai") == True
    assert hobj.spell("kai-awa") == True

@pytest.mark.skip(reason="Test used in creating the baseline aff file")
def test_break_0(hpk_dic_filepath, test_aff_break_0_only_filepath):
    # This shows the importance of setting BREAK 0 in the .aff file
    # The BREAK 0 results in 'new' words being marked WRONG (desired behaviour)
    # in this case "awa-kai" and "kai-awa"    
    hobj = hunspell.HunSpell(hpk_dic_filepath, test_aff_break_0_only_filepath)
    assert hobj.spell("awa") == True
    assert hobj.spell("kai") == True    
    assert hobj.spell("awa-kai") == False
    assert hobj.spell("kai-awa") == False

@pytest.mark.skip(reason="Test used in creating the baseline aff file")
def test_encoding(hpk_dic_filepath, \
                  test_aff_set_only_filepath, \
                  test_aff_empty_filepath):

    hobj_no_encoding = hunspell.HunSpell(hpk_dic_filepath, test_aff_empty_filepath)
    with pytest.raises(ValueError):
        assert hobj_no_encoding.spell("ā") == True
    hobj_encoding = hunspell.HunSpell(hpk_dic_filepath, test_aff_set_only_filepath)
    assert hobj_encoding.spell("ā") == True                        
