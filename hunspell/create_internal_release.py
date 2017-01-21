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
import release_utilities as ru

RELEASE_001_NAME = "hpk"
IR = "ir"

cf = config.ConfigFile()
internal_releases_files_path = (
    cf.configfile[cf.computername]['internal_releases_files_path'])

baseline_files_path = cf.configfile[cf.computername]['baseline_files_path']
new_words_file_path = cf.configfile[cf.computername]['new_words_file_path']


def create_internal_release(internal_release_name=RELEASE_001_NAME):

    # 1. check that the release name chosen meets the criteria
    if not ru.internal_release_name_ok(internal_release_name):
        return False

    # 2. check that the release name chosen has not been used before
    internal_releases_folders = os.listdir(internal_releases_files_path)
    internal_release_names = [ru.get_internal_release_name(x) for x in internal_releases_folders]
    if internal_release_name in internal_release_names:
        print ("The internal release name " + internal_release_name + " has been used before")
        print ("Here are the names of the previous internal releases")
        for irn in internal_release_names:
            print (irn)
        return False

    # 3. get the most recent successfully tested internal release (s.t.i.r)
    most_recent_stir = ru.get_most_recent_stir()

    # get the .dic and .aff files we will be using
    if most_recent_stir is None:
        current_dic_filepath = os.path.join(baseline_files_path, "empty.dic")
        current_aff_filepath = os.path.join(baseline_files_path, "baseline.aff")
    else:
        most_recent_stir_folder_name = \
            most_recent_stir[0] + "_" + most_recent_stir[1]
        current_dic_filename = most_recent_stir_folder_name + ".dic"
        current_aff_filename = most_recent_stir_folder_name + ".aff"
        current_dic_filepath = os.path.join(internal_releases_files_path, 
                                            most_recent_stir_folder_name,
                                            current_dic_filename)
        current_aff_filepath = os.path.join(internal_releases_files_path, 
                                            most_recent_stir_folder_name,
                                            current_aff_filename)

    # create the internal release folder
    if most_recent_stir is None:
        internal_release_number = "001"
    else:
        internal_release_number = str((int(most_recent_stir[0]) + 1)).zfill(3)

    internal_release_folder_name = IR + "_" + \
                                   internal_release_number + "_" + \
                                   internal_release_name
  
    os.mkdir(os.path.join(internal_releases_files_path, 
                          internal_release_folder_name))


    # read in the current .dic file
    current_dic_words = ru.read_words_file(current_dic_filepath)

    # get the new words that will be added to this release
    new_words = ru.get_new_words()   

    # combine the new words with the current .dic words
    combined_dic_words = list(set(current_dic_words) | set(new_words)) # union

    # the new words that are already in the current dic
    dup_dic_words = list(set(current_dic_words) & set(new_words)) # intersection

    # the new words that will be added
    add_dic_words = list(set(new_words) - set(dup_dic_words))  


    # find those "open compound" or "mixed compound" words
    # that contain 1 or more words (which could be hyphenated compounds)
    # that are not in the dic words to be added - known as "supplemental words"
    supplemental_words = ru.get_supplemental_words(add_dic_words)    

    # create and write the new internal release .dic file
    ru.create_internal_release_words_file(internal_release_folder_name,
                                          "dic",
                                          combined_dic_words + supplemental_words)

    # create and write the new internal release .sup file
    ru.create_internal_release_words_file(internal_release_folder_name,
                                          "sup",
                                          supplemental_words)

    # create and write the new internal release .add file
    ru.create_internal_release_words_file(internal_release_folder_name,
                                          "add",
                                          add_dic_words)

    # create and write the new internal release .dup file
    ru.create_internal_release_words_file(internal_release_folder_name,
                                          "dup",
                                          dup_dic_words)

    # read in the current .aff file
    current_aff_lines = ru.read_aff_file(current_aff_filepath)

    # get the open compounds (for use in the .aff file)
    # there can be no open compounds in the supplemental words
    # so only look in add_dic_words
    open_compounds = ru.get_open_compounds(add_dic_words)

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

    # write the new aff file
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
