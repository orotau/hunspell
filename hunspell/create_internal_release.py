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

RELEASE_001_NAME = "hpk"

cf = config.ConfigFile()
internal_releases_files_path = (
    cf.configfile[cf.computername]['internal_releases_files_path'])

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


def create_internal_release(internal_release_name=RELEASE_001_NAME):
    internal_release_number = get_internal_release_number(internal_release_name)

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
