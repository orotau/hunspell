import os
import config
from random import shuffle
import hunspell
import pytest

cf = config.ConfigFile()
test_dicaff_files_path = (cf.configfile[cf.computername]['test_dicaff_files_path'])

'''
Test Case
Want to ensure (if possible) that any Capitalised words do not allow in their
uncapitalised equivalents (unless they are in the dic too).

We *don't* want to do the reverse because the lower case word could be capitalised
because it is the first in a sentence.

The 2 tests below appear to show that the default behaviour is fine
'''

@pytest.fixture(scope="module")
def foo_filepath():
    foo_DIC_FILE = "foo.dic"
    return os.path.join(test_dicaff_files_path, foo_DIC_FILE)

@pytest.fixture(scope="module")
def Foo_filepath():
    Foo_DIC_FILE = "Foo.dic"
    return os.path.join(test_dicaff_files_path, Foo_DIC_FILE)

@pytest.fixture(scope="module")
def empty_aff_filepath():
    EMPTY_AFF_FILE = "test_empty.aff"   
    return os.path.join(test_dicaff_files_path, EMPTY_AFF_FILE)

def test_foo(foo_filepath, empty_aff_filepath):
    hobj = hunspell.HunSpell(foo_filepath, empty_aff_filepath)
    assert hobj.spell("foo") == True
    assert hobj.spell("Foo") == True
    assert hobj.spell("FOO") == True

def test_Foo(Foo_filepath, empty_aff_filepath):
    hobj = hunspell.HunSpell(Foo_filepath, empty_aff_filepath)
    assert hobj.spell("foo") == False
    assert hobj.spell("Foo") == True
    assert hobj.spell("FOO") == True

