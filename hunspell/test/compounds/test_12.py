import os
import config
from random import shuffle
import hunspell
import pytest

cf = config.ConfigFile()
test_dicaff_files_path = (cf.configfile[cf.computername]['test_dicaff_files_path'])

'''
foo bar
'''

@pytest.fixture(scope="module")
def foo_bar_dic_filepath():
    FOO_BAR_DIC_FILE = "foo_bar.dic"
    return os.path.join(test_dicaff_files_path, FOO_BAR_DIC_FILE)

@pytest.fixture(scope="module")
def foo_bar_aff_filepath():
    FOO_BAR_AFF_FILE = "foo_bar.aff"   
    return os.path.join(test_dicaff_files_path, FOO_BAR_AFF_FILE)

@pytest.mark.skip(reason="needs fixing up")
def test_map(foo_bar_dic_filepath, foo_bar_aff_filepath):
    hobj = hunspell.HunSpell(foo_bar_dic_filepath, foo_bar_aff_filepath)
    print(hobj.spell("foo-rab"))
    print([x.decode() for x in hobj.suggest("foo-bar")])


