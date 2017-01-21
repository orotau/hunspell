'''
Release utilities used in the release and testing process
'''

import config
import os
import re
from datetime import datetime
import maoriword as mw

RELEASE_001_NAME = "hpk"
IR = "ir"

cf = config.ConfigFile()
internal_releases_files_path = (
    cf.configfile[cf.computername]['internal_releases_files_path'])
new_words_file_path = (
    cf.configfile[cf.computername]['new_words_file_path'])

def read_words_file(file_path):

    words = []
    with open(file_path, "r") as f:
        for line_number, line in enumerate(f, 1):
            line_to_add = line.replace('\n', '')
            if line_number == 1:
                try:
                    # first line should contain an integer
                    words_count = int(line_to_add)
                except ValueError:
                    return ValueError(filepath, "Number of words needed on line 1")                                
            else:
                words.append(line_to_add)

    if words_count == len(words):
        return words
    else:
        return False

def read_aff_file(file_path):

    aff_lines = []
    with open(file_path, "r") as f:
        for line in f:
            line_to_add = line.replace('\n', '')
            aff_lines.append(line_to_add)

    return aff_lines


def internal_release_name_ok(internal_release_name):

    # The internal release name must be all one word lower case (hyphenated ok)
    # Note that this regex excludes an underscore (_) and fullstop (.)
    # which is essential as the internal_release_name will be parsed using them.
    
    internal_release_name_regex = r"""

    (
    [a-zāēīōū]+     # one word (1 or more letters)
    )

    (  
    -               # dash
    [a-zāēīōū]+     # one word (1 or more letters)
    )
    *               # zero, one or more times
              
    """

    is_fullmatch = re.fullmatch(internal_release_name_regex, 
                                internal_release_name, 
                                re.VERBOSE)

    if is_fullmatch:
        return True
    else:
        print ("The release name must be lower case, it can contain dashes")
        return False     


def get_internal_release_name(folder_or_path_name):

    '''
    Given the folder name or the path name 
    (It can be either because we are looking from the right)
    return the release name

    e.g 016_banana should return 'banana'
    '''   
    
    try:
        release_name = folder_or_path_name.rsplit("_", 1)[1]    
    except IndexError:
        print ("No underscore (_) found in the folder or path name")
        return False
    else: 
        return release_name

def get_internal_release_number(folder_or_path_name):

    '''
    Given the folder name or the path name 
    (It can be either because we are looking from the right)
    return the internal release number (as integer)
    It is returned as integer because we need to use it as a key
    for sorting and key = int(get_internal_release_number) didn't work in 
    'sorted'
    e.g 016_banana should return 16

    Works up to 999
    '''   
    
    try:
        left_of_underscore = folder_or_path_name.rsplit("_", 1)[0]    
    except IndexError:
        print ("No underscore (_) found in the folder or path name")
        return False

    internal_release_number = int(left_of_underscore[-3:])

    return internal_release_number    
    

def get_most_recent_stir():

    '''
    We are looking for the most recent "Successfully Tested Internal Release"
    that is where the word 'stir' comes from

    A stir is idetified by a folder name without the prefix "ir_"

    look in the internal releases files path at all the subfolders (if any)
    find the most recent internal release (based on number)
    return as tuple    release number, release name

    In the event that the most recent internal release has not yet been 
    successfully tested (indicated by the fact that the folder name begins
    with "ir_") then return the previous release (if any).
    '''    

    internal_releases_folders = os.listdir(internal_releases_files_path)
    internal_releases_folders_paths = ([os.path.join(internal_releases_files_path, x) 
                                        for x in internal_releases_folders])

    if internal_releases_folders:
        # check that there are only directories (no files)
        assert all(os.path.isdir(x) for x in internal_releases_folders_paths)

        # get the *number* of the most recent internal release
        number_of_most_recent_internal_release = max([get_internal_release_number(x) for x in \
                                                 internal_releases_folders])

        # get the *name* of the most recent internal release
        most_recent_internal_release_folder = \
            sorted(internal_releases_folders, key=get_internal_release_number)[-1]

        name_of_most_recent_internal_release = \
            get_internal_release_name(most_recent_internal_release_folder)

        # has it been successfully tested (i.e is it a stir?)
        if not most_recent_internal_release_folder.startswith(IR + "_"):
            # it has been successfully tested
            number_of_most_recent_stir = number_of_most_recent_internal_release
            name_of_most_recent_stir = name_of_most_recent_internal_release
        else:
            # it has *not* been successfully tested
            if len(internal_releases_folders) == 1:
                return None
            else:
                number_of_most_recent_stir = number_of_most_recent_internal_release - 1
                most_recent_stir_folder = sorted(internal_releases_folders, 
                                                 key=get_internal_release_number)[-2]
                name_of_most_recent_stir = get_internal_release_name(most_recent_stir_folder)
    else:
        # no internal releases as of yet
        return None

    return str(number_of_most_recent_stir).zfill(3), \
               name_of_most_recent_stir


def get_untested_release():
      
    internal_releases_folders = os.listdir(internal_releases_files_path)
    internal_releases_folders_paths = ([os.path.join(internal_releases_files_path, x) 
                                        for x in internal_releases_folders])

    if internal_releases_folders:
        # check that there are only directories (no files)
        assert all(os.path.isdir(x) for x in internal_releases_folders_paths)

        untested_internal_release_folder = \
            [x for x in internal_releases_folders if x.startswith(IR + "_")]

        assert len(untested_internal_release_folder) == 1
        
        untested_internal_release_number = get_internal_release_number(
                                               untested_internal_release_folder[0])
        untested_internal_release_name = get_internal_release_name(
                                             untested_internal_release_folder[0])
    else:
        # no internal releases as of yet
        return None

    return str(untested_internal_release_number).zfill(3), \
               untested_internal_release_name


def get_new_words():

    new_words = []
    # there can only be 1 file in the new_words folder
    # filter out any temporary files (ending in ~)
    directory_contents = [x for x in os.listdir(new_words_file_path) \
                          if not x.endswith('~')]
    if len(directory_contents) != 1:
        return ValueError("Only 1 lonely file can be in here")
    else:
        content = os.path.join(new_words_file_path, directory_contents[0])
        if os.path.isdir(content):
            return ValueError("A file is needed, not a directory")
        else:
            # we have a lonely file - check its not empty
            if os.stat(content).st_size == 0:
                return ValueError("The file is empty")
            else:
                with open(content, "r") as f:
                    for line_number, line in enumerate(f, 1):
                        line_to_add = line.replace('\n', '')
                        if line_number == 1:
                            try:
                                # first line should contain an integer
                                new_words_count = int(line_to_add)
                            except ValueError:
                                return ValueError("Number of words needed on line 1")                                
                        else:
                            new_words.append(line_to_add)    

            # belt and braces check on the file
            # number at start of file = number of words
            assert new_words_count == len(new_words)

            # uniqueness
            assert len(set(new_words)) == len(new_words)

            return sorted(new_words, key=mw.get_list_sort_key)

def get_open_compounds(list_of_words):
    # an open compound is a word separated by 1 or more spaces
    # that does not contain a dash
    open_compounds = []
    for word in list_of_words:
        if " " in word and not "-" in word:
            open_compounds.append(word)

    return sorted(open_compounds, key=mw.get_list_sort_key)


def get_supplemental_words(list_of_words):
    '''
    This function takes a list of words
    "Open compounds", e.g. "foo bar" (components 'foo' and 'bar')
    "Mixed compounds", e.g. "foo-bar baz" (components 'foo-bar' and 'baz')

    Each of these compound word types is split (by space) and the components
    are searched for in the "list_of_words" input.

    If they are not in the "list_of_words" input then they will be added to
    the list of words to be returned (supplemental_words)

    Finally the list is made unique and ordered in Māori order and returned
    '''
    supplemental_words = []
    for word in list_of_words:
        if " " in word:
            components = word.split(" ")
            for c in components:
                if not c in list_of_words:
                    supplemental_words.append(c)

    if supplemental_words:
        # make unique
        supplemental_words = list(set(supplemental_words))        

        # sort the list in Māori order
        return sorted(supplemental_words, key=mw.get_list_sort_key)

    else:
        return [] 


def create_internal_release_words_file(folder_name, extension, words):  

    filename = folder_name + "." + extension
    filepath = os.path.join(internal_releases_files_path, folder_name, filename) 
    words_count = len(words)
    words = sorted(words, key=mw.get_list_sort_key)

    with open(filepath, "a", encoding = 'utf-8') as myfile:
        myfile.write(str(words_count) + "\n")
        for word in words:
            myfile.write(word + "\n") 

    return True




if __name__ == '__main__':

    import sys
    import argparse
    import ast

    # create the top-level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # create the parser for the internal_release_name_ok function
    internal_release_name_ok_parser = \
        subparsers.add_parser('internal_release_name_ok')
    internal_release_name_ok_parser.add_argument('internal_release_name')
    internal_release_name_ok_parser.set_defaults \
        (function = internal_release_name_ok)

    # create the parser for the get_internal_release_name function
    get_internal_release_name_parser = subparsers.add_parser('get_internal_release_name')
    get_internal_release_name_parser.add_argument('file_or_path_name')
    get_internal_release_name_parser.set_defaults (function = get_internal_release_name)

    # create the parser for the get_most_recent_stir function
    get_most_recent_stir_parser = subparsers.add_parser('get_most_recent_stir')
    get_most_recent_stir_parser.set_defaults (function = get_most_recent_stir)

    # create the parser for the get_untested_release function
    get_untested_release_parser = subparsers.add_parser('get_untested_release')
    get_untested_release_parser.set_defaults (function = get_untested_release)

    # create the parser for the get_new_words function
    get_new_words_parser = subparsers.add_parser('get_new_words')
    get_new_words_parser.set_defaults (function = get_new_words)

    # parse the arguments
    arguments = parser.parse_args()
    arguments = vars(arguments) #convert from Namespace to dict

    #attempt to extract and then remove the function entry
    try:
        function_to_call = arguments['function'] 
    except KeyError:
        print ("You need a function name. Please type -h to get help")
        sys.exit()
    else:
        #remove the function entry as we are only passing arguments
        del arguments['function']
    
    if arguments:
        #remove any entries that have a value of 'None'
        #We are *assuming* that these are optional
        #We are doing this because we want the function definition to define
        #the defaults (NOT the function call)
        arguments = { k : v for k,v in arguments.items() if v is not None }

        #alter any string 'True' or 'False' to bools
        arguments = { k : ast.literal_eval(v) if v in ['True','False'] else v 
                                              for k,v in arguments.items() }       

    result = function_to_call(**arguments) #note **arguments works fine for empty dict {}
   
    print (result)
