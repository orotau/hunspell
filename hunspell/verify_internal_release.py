'''
The testing has 2 parts 
a) The basic mechanics of the file creation that has been done
b) The spellcheck part

At the end we update file and folder names
and update the .aff file
'''

import os
import config
import hunspell
from datetime import datetime
import release_utilities as ru
import maoriword as mw
import common_word_division_errors as cwde

IR = "ir"

cf = config.ConfigFile()
internal_releases_files_path = (
    cf.configfile[cf.computername]['internal_releases_files_path'])
baseline_files_path = cf.configfile[cf.computername]['baseline_files_path']

def verify_internal_release():
    
    # get the internal release folder (to be tested)
    untested_release = ru.get_untested_release()

    if untested_release is None:
        print("No release found to test")
        return False
    else:    
        untested_release_folder_name = IR + "_" + untested_release[0] + "_" + \
                                       untested_release[1]
        untested_release_path = os.path.join(internal_releases_files_path, 
                                             untested_release_folder_name)

        dic_file_name = untested_release_folder_name + ".dic"
        add_file_name = untested_release_folder_name + ".add"
        dup_file_name = untested_release_folder_name + ".dup"
        sup_file_name = untested_release_folder_name + ".sup"
        aff_file_name = untested_release_folder_name + ".aff"

        dic_file_path = os.path.join(untested_release_path, dic_file_name)
        add_file_path = os.path.join(untested_release_path, add_file_name)
        dup_file_path = os.path.join(untested_release_path, dup_file_name)
        sup_file_path = os.path.join(untested_release_path, sup_file_name)
        aff_file_path = os.path.join(untested_release_path, aff_file_name)
    
        # read in the dic file
        dic_words = ru.read_words_file(dic_file_path)

        # read in the add file
        add_words = ru.read_words_file(add_file_path)

        # read in the dup file
        dup_words = ru.read_words_file(dup_file_path)

        # read in the sup file
        sup_words = ru.read_words_file(sup_file_path)

        # read in the aff file
        aff_lines = ru.read_aff_file(aff_file_path)


    # get the most recent stir
    most_recent_stir = ru.get_most_recent_stir()

    if most_recent_stir is None:
        # we are verifying the first release (ir_001_hpk)
        previous_dic_file_name = "empty.dic"
        previous_aff_file_name = "baseline.aff"

        previous_dic_file_path = os.path.join(baseline_files_path, 
                                              previous_dic_file_name)
        previous_aff_file_path = os.path.join(baseline_files_path, 
                                              previous_aff_file_name)
    else:    
        most_recent_stir_folder_name = most_recent_stir[0] + "_" + \
                                       most_recent_stir[1]
        most_recent_stir_path = os.path.join(internal_releases_files_path, 
                                             most_recent_stir_folder_name)

        previous_dic_file_name = most_recent_stir_folder_name + ".dic"
        previous_aff_file_name = most_recent_stir_folder_name + ".aff"

        previous_dic_file_path = os.path.join(most_recent_stir_path, 
                                              previous_dic_file_name)
        previous_aff_file_path = os.path.join(most_recent_stir_path, 
                                              previous_aff_file_name)

    # read in the previous stir dic file
    previous_dic_words = ru.read_words_file(previous_dic_file_path)

    # read in the previous stir aff file
    previous_aff_lines = ru.read_aff_file(previous_aff_file_path)

    #########################
    ### Verify Word Lists ###
    #########################
    word_lists = []
    word_lists.append(dic_words)
    word_lists.append(add_words)
    word_lists.append(dup_words)
    word_lists.append(sup_words)
    word_lists.append(previous_dic_words)

    ### ASSERTION - uniqueness ###
    for word_list in word_lists:
        assert len(word_list) == len(set(word_list)) 

    ### ASSERTION - word form and sort order ###
    for word_list in word_lists:
        assert word_list == sorted(word_list, key=mw.get_list_sort_key) 

    ### ASSERTION - basic relationship ###
    assert set(previous_dic_words + add_words + sup_words) == set(dic_words)

    ### ASSERTION - any word in dup_words not in add_words ###
    for dup_word in dup_words:
        assert dup_word not in add_words

    ### ASSERTION - any word in dup_words in previous_dic_words ###
    for dup_word in dup_words:
        assert dup_word in previous_dic_words 

    ########################
    ### Verify aff files ###
    ########################
    REP_NUMBER_LINE = 16
    REP_NUMBER_LINE_TEXT = "REP "
    previous_rep_number = int(previous_aff_lines[REP_NUMBER_LINE - 1].split \
                              (REP_NUMBER_LINE_TEXT, 1)[1])
    current_rep_number = int(aff_lines[REP_NUMBER_LINE - 1].split \
                             (REP_NUMBER_LINE_TEXT, 1)[1])

    open_compounds_added = ru.get_open_compounds(add_words)

    ### ASSERTION ###
    # assert the REP number has been updated correctly
    assert previous_rep_number + len(open_compounds_added) == current_rep_number 

    ### ASSERTION ###
    # assert each REP line for the open compounds has been updated correctly
    # start at the end and go backwards (rather than find the start point)
    for open_compound_added, aff_line in \
        zip(reversed(open_compounds_added), reversed(aff_lines)):
        open_compound_with_dashes = open_compound_added.replace(" ", "-")
        open_compound_with_underscores = open_compound_added.replace(" ", "_")
        assert aff_line == REP_NUMBER_LINE_TEXT + \
                           open_compound_with_dashes + " " + \
                           open_compound_with_underscores
       
    ###########################
    ### SPELLING ASSERTIONS ###
    ###########################
    # get the hunspell object
    hobj = hunspell.HunSpell(dic_file_path, aff_file_path)

    ### ASSERTION ###
    # assert all open compound words that are erroneously entered as
    # hyphenated compounds get the open compound word in the suggestions
    for word in dic_words:
        if " " in word and not "-" in word:
            word_with_dashes = word.replace(" ", "-")            
            suggestions = hobj.suggest(word_with_dashes)
            assert word in suggestions

    ### ASSERTION ###
    # assert all suggestions that are not in the dictionary are regarded
    # as being spelt wrongly.
    # note that I have just made use of the compound words to generate
    # suggestions (they could have come from anywhere)
    # Note also that if say 'Foo' is *not* in the dic_words but 'foo' is
    # then 'Foo' will be regarded as ok (see test_10).
    for word in dic_words:
        if " " in word and not "-" in word:
            word_with_dashes = word.replace(" ", "-")            
            suggestions = hobj.suggest(word_with_dashes)
            for suggestion in suggestions:
                if suggestion in dic_words or suggestion.lower() in dic_words:
                    pass
                else:
                    assert hobj.spell(suggestion) == False

    ### ASSERTION - every word in the dic is spelled correctly! ###
    for word in dic_words:
        assert hobj.spell(word) == True

    ### ASSERTION ###
    # assert all common word division spelling errors get the correct word suggested 
    for wrong, right in cwde.wrong_right:
        suggestions = hobj.suggest(wrong)
        assert right in suggestions    
    
    # if we get this far all of the tests have passed
    # update the file and folder names by removing the IR_
    text_to_remove = IR + "_"

    tested_release_folder_name = untested_release_folder_name[len(text_to_remove):]
    tested_release_path = os.path.join(internal_releases_files_path, 
                                       tested_release_folder_name)

    tested_dic_file_name = tested_release_folder_name + ".dic"
    tested_add_file_name = tested_release_folder_name + ".add"
    tested_dup_file_name = tested_release_folder_name + ".dup"
    tested_sup_file_name = tested_release_folder_name + ".sup"
    tested_aff_file_name = tested_release_folder_name + ".aff"

    # note that the path will be changed later
    tested_dic_file_path = os.path.join(untested_release_path, tested_dic_file_name)
    tested_add_file_path = os.path.join(untested_release_path, tested_add_file_name)
    tested_dup_file_path = os.path.join(untested_release_path, tested_dup_file_name)
    tested_sup_file_path = os.path.join(untested_release_path, tested_sup_file_name)
    tested_aff_file_path = os.path.join(untested_release_path, tested_aff_file_name)

    # files
    os.rename(dic_file_path, tested_dic_file_path)
    os.rename(add_file_path, tested_add_file_path)
    os.rename(dup_file_path, tested_dup_file_path)
    os.rename(sup_file_path, tested_sup_file_path)
    os.rename(aff_file_path, tested_aff_file_path)

    # folder
    os.rename(untested_release_path, tested_release_path)

    # also need to update the first two lines of the .aff file
    RELEASE_NAME_LINE = 1
    DATE_LINE = 2 
    RELEASE_NAME_LINE_TEXT = '# Release '
    DATE_LINE_TEXT = '#    Date '
    tested_aff_file_path = os.path.join(tested_release_path, tested_aff_file_name)
    with open(tested_aff_file_path, "w") as myfile:
        for line_number, aff_line in enumerate(aff_lines, 1):
            if line_number == RELEASE_NAME_LINE:                
                myfile.write(RELEASE_NAME_LINE_TEXT + "'" + 
                             tested_release_folder_name + "'" + "\n")

            elif line_number == DATE_LINE:
                dt = datetime.now().strftime('%d %b %Y, %H:%M:%S')
                myfile.write(DATE_LINE_TEXT + "'" + dt + "'" + "\n")

            else:
                myfile.write(aff_line + "\n") 
    return True


if __name__ == '__main__':

    import sys
    import argparse
    import ast

    # create the top-level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # create the parser for the verify_internal_release function
    verify_internal_release_parser = subparsers.add_parser('verify_internal_release')
    verify_internal_release_parser.set_defaults(function = verify_internal_release)

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
