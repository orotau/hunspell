'''
An internal release has as its starting point
a .dic file and a .aff file

If we are *running for the first time*
then we will be using hpk.dic and baseline.aff as the starting point
There will be no .words file in this case

If we are running for the *second or subsequent times*
then we will be using the most recent .dic and .aff as the starting point

In addition we will have a .words file which contains the words that will
be added as part of the release

I am unsure whether to allow (or not) an empty words file
Leaning towards not allowing.
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

baseline_files_path = cf.configfile[cf.computername]['baseline_files_path']

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


def get_release_name(folder_or_path_name):

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
    

def get_most_recent_internal_release():

    '''
    look in the internal releases files path at all the subfolders (if any)
    find the most recent internal release (based on number)
    return as tuple    release number, release name

    In the event that the most recent internal release has not yet been 
    successfully tested (indicated by the fact that the folder name begins
    with "ir_") then return a ValueError.
    '''    

    internal_releases_folders = os.listdir(internal_releases_files_path)
    internal_releases_folders_paths = ([os.path.join(internal_releases_files_path, x) 
                                        for x in internal_releases_folders])

    if internal_releases_folders:
        # check that there are only directories (no files)
        assert all(os.path.isdir(x) for x in internal_releases_folders_paths)

        # get the number of the most recent internal release
        number_of_most_recent_internal_release = max([get_internal_release_number(x) for x in \
                                                 internal_releases_folders])

        # get the name of the most recent internal release
        most_recent_internal_release_folder = \
            sorted(internal_releases_folders, key=get_internal_release_number)[-1]

        if most_recent_internal_release_folder.startswith(IR + "_"):
            raise ValueError("Most recent internal 'release' not yet successfully tested")

        name_of_most_recent_internal_release = \
            get_release_name(most_recent_internal_release_folder)

    else:
        # no internal releases as of yet
        return None

    return str(number_of_most_recent_internal_release).zfill(3), \
           name_of_most_recent_internal_release    


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


def create_internal_release(internal_release_name=RELEASE_001_NAME):

    # 1. check that the release name chosen meets the criteria
    if not internal_release_name_ok(internal_release_name):
        return False

    # 2. check that the release name chosen has not been used before
    internal_releases_folders = os.listdir(internal_releases_files_path)
    internal_release_names = [get_release_name(x) for x in internal_releases_folders]
    if internal_release_name in internal_release_names:
        print ("The internal release name " + internal_release_name + " has been used before")
        print ("Here are the names of the previous internal releases")
        for irn in internal_release_names:
            print (irn)
        return False

    # 3. get the most recent internal release
    most_recent_internal_release = get_most_recent_internal_release()

    # get the .dic and .aff files we will be using
    if most_recent_internal_release is None:
        current_dic_filepath = os.path.join(baseline_files_path, "hpk.dic")
        current_aff_filepath = os.path.join(baseline_files_path, "baseline.aff")
    else:
        most_recent_internal_release_folder_name = \
            most_recent_internal_release[0] + "_" + most_recent_internal_release[1]
        current_dic_filepath = os.path.join(internal_releases_files_path, 
                                            most_recent_internal_release_folder_name,
                                            "hpk.dic")
        current_aff_filepath = os.path.join(internal_releases_files_path, 
                                            most_recent_internal_release_folder_name,
                                            "baseline.aff")

    # create the internal release folder
    if most_recent_internal_release is None:
        internal_release_number = "001"
    else:
        internal_release_number = str((int(most_recent_internal_release[0]) + 1)).zfill(3)

    internal_release_folder_name = IR + "_" + \
                                   internal_release_number + "_" + \
                                   internal_release_name
  
    os.mkdir(os.path.join(internal_releases_files_path, 
                          internal_release_folder_name))
    

    # read in the current .dic file
    current_dic_words = []
    with open(current_dic_filepath, "r") as f:
        for line in f:
            line_to_add = line.replace('\n', '')
            try:
                # first line should contain an integer
                current_dic_words_count = int(line_to_add) 
            except:
                current_dic_words.append(line_to_add)
    
    # belt and braces check on the current dic
    assert current_dic_words_count == len(current_dic_words)

    # find those "open compound" or "mixed compound" words
    # that contain 1 or more words (which could be hyphenated compounds)
    # that are not in the .dic file - known as "supplemental words"
    supplemental_words = get_supplemental_words(current_dic_words)    

    # create and write the new internal release .dic file
    new_dic_filename = internal_release_folder_name + ".dic"
    new_dic_filepath = os.path.join(internal_releases_files_path, 
                                    internal_release_folder_name,
                                    new_dic_filename)
 
    new_dic_words_count = current_dic_words_count + len(supplemental_words)
    new_dic_words = sorted(current_dic_words + supplemental_words,
                           key=mw.get_list_sort_key)

    with open(new_dic_filepath, "a", encoding = 'utf-8') as myfile:
        myfile.write(str(new_dic_words_count) + "\n")
        for word in new_dic_words:
            myfile.write(word + "\n")


    # read in the current .aff file
    current_aff_lines = []
    with open(current_aff_filepath, "r") as f:
        for line in f:
            line_to_add = line.replace('\n', '')
            current_aff_lines.append(line_to_add)

    # get the open compounds (for use in the .aff file)
    # there can be no open compounds in the supplemental words
    # so only look in dic_words
    open_compounds = []
    for word in current_dic_words:
        if " " in word and not "-" in word:
            open_compounds.append(word)

    open_compounds = sorted(open_compounds, key=mw.get_list_sort_key)

    # create and write the new internal release .aff file
    RELEASE_NAME_LINE = 1
    DATE_LINE = 2
    REP_NUMBER_LINE = 16
    RELEASE_NAME_LINE_TEXT = '# Release '
    DATE_LINE_TEXT = '#    Date '
    REP_NUMBER_LINE_TEXT = "REP "
  
    new_aff_filename = internal_release_folder_name + ".aff"
    new_aff_filepath = os.path.join(internal_releases_files_path, 
                                    internal_release_folder_name,
                                    new_aff_filename)

    # write the file
    with open(new_aff_filepath, "a") as myfile:
        for line_number, current_aff_line in enumerate(current_aff_lines, 1):
            if line_number == RELEASE_NAME_LINE:                
                myfile.write(RELEASE_NAME_LINE_TEXT + "'" + 
                             internal_release_folder_name + "'" + "\n")

            elif line_number == DATE_LINE:
                dt = datetime.now().strftime('%d %b %Y, %H:%M:%S')
                myfile.write(DATE_LINE_TEXT + "'" + dt + "'" + "\n")

            elif line_number == REP_NUMBER_LINE:
                current_rep_number = int(current_aff_line.split(REP_NUMBER_LINE_TEXT, 1)[1])
                new_rep_number = str(current_rep_number + len(open_compounds))
                myfile.write(REP_NUMBER_LINE_TEXT + new_rep_number + "\n")

            else:
                myfile.write(current_aff_line + "\n")

        # add the REP entries
        for open_compound in open_compounds:
            myfile.write(REP_NUMBER_LINE_TEXT + 
                         open_compound.replace(" ", "-") + " " +  
                         open_compound.replace(" ", "_") +  "\n")

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

    # create the parser for the get_release_name function
    get_release_name_parser = subparsers.add_parser('get_release_name')
    get_release_name_parser.add_argument('file_or_path_name')
    get_release_name_parser.set_defaults (function = get_release_name)

    # create the parser for the get_most_recent_internal_release function
    get_most_recent_internal_release_parser = \
        subparsers.add_parser('get_most_recent_internal_release')
    get_most_recent_internal_release_parser.set_defaults \
        (function = get_most_recent_internal_release)

    # create the parser for the create_internal_release function
    create_internal_release_parser = subparsers.add_parser('create_internal_release')
    create_internal_release_parser.add_argument('-internal_release_name')
    create_internal_release_parser.set_defaults(function = create_internal_release)

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
