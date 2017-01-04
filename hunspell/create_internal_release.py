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
import maoriword as mw

RELEASE_001_NAME = "hpk"

cf = config.ConfigFile()
internal_releases_files_path = (
    cf.configfile[cf.computername]['internal_releases_files_path'])

baseline_files_path = cf.configfile[cf.computername]['baseline_files_path']

def get_internal_release_number(internal_release_name=RELEASE_001_NAME):
    if internal_release_name == RELEASE_001_NAME:
        return "001"
    else:
        # look at the subfolders in the internal releases folder
        # they are of the form "release_number"_"release_name"
        # we need the highest release number and then add 1 to it
        internal_releases_folders = os.listdir(internal_releases_files_path)
        internal_releases_folders_paths = ([os.path.join(internal_releases_files_path, x) 
                                            for x in internal_releases_folders])

        if internal_releases_folders == []:
            # the directory is empty
            print("The first release can only be " + '"' + RELEASE_001_NAME + '"')
            return False
        else:
            # check that there are only directories (no files)
            assert all(os.path.isdir(x) for x in internal_releases_folders_paths)

        # get the number of the last release (works up to 999)
        number_of_last_release = max([int(x[:3]) for x in internal_releases_folders])
        number_of_this_release = 1 + number_of_last_release

        return str(number_of_this_release).zfill(3)       


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
        return False    


def create_internal_release(internal_release_name=RELEASE_001_NAME):

    internal_release_number = get_internal_release_number(internal_release_name)

    if not internal_release_number:
        return False

    if internal_release_number == "001":

        # find those "open compound" or "mixed compound" words
        # that contain 1 or more words (which could be hyphenated compounds)
        # that are not in the .dic file
        # known as "supplemental words"

        BASELINE_DIC_FILE_NAME = "hpk.dic"
        BASELINE_AFF_FILE_NAME = "baseline.aff"

        dic_file_path = os.path.join(baseline_files_path, BASELINE_DIC_FILE_NAME)

        dic_words = []

        # read in the .dic file
        with open(dic_file_path, 'r') as f:
            for line in f:
                dic_words.append(line.replace('\n', ''))

        # get the supplemental words
        supplemental_words = get_supplemental_words(dic_words)

        return supplemental_words
    
    else:
        # look for .words file
        pass
    

if __name__ == '__main__':

    import sys
    import argparse
    import ast

    # create the top-level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # create the parser for the get_internal_release_number function
    get_internal_release_number_parser = subparsers.add_parser('get_internal_release_number')
    get_internal_release_number_parser.add_argument('-internal_release_name')
    get_internal_release_number_parser.set_defaults(function = get_internal_release_number)

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
