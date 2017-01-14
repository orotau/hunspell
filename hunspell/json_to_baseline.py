'''
Create 2 baseline files
1) hpk.dic
2) baseline.aff
'''
import config
import os
import query_yes_no
import sys

cf = config.ConfigFile()
baseline_files_path = (cf.configfile[cf.computername]['baseline_files_path'])

if sys.argv[1] == "create_hpk_dic_file":
    file_name = "hpk.dic"
elif sys.argv[1] == "create_baseline_aff_file":
    file_name = "baseline.aff"
else:
    file_name = "oops.oops"

baseline_file_path = baseline_files_path + file_name

if os.path.isfile(baseline_file_path):
    # file exists, check to see if it should be overridden
    file_exists = True
    overwrite_file = query_yes_no.query_yes_no("OVERWRITE the existing file?")
else:
    file_exists = False

def create_hpk_dic_file():

    if file_exists and not overwrite_file:
        print("Existing file left as is")
        return None

    if file_exists and overwrite_file:
        # delete existing file
        os.remove(baseline_file_path)

    # write the file
    import json_processor_hunspell as jph
    all_words_for_hunspell = jph.get_all_words_for_hunspell()
    with open(baseline_file_path, "a", encoding = 'utf-8') as myfile:
        myfile.write(str(len(all_words_for_hunspell)) + "\n")
        for word in all_words_for_hunspell:
            myfile.write(word + "\n")
    return True
    

def create_baseline_aff_file():

    if file_exists and not overwrite_file:
        print("Existing file left as is")
        return None

    if file_exists and overwrite_file:
        # delete existing file
        os.remove(baseline_file_path)

    #create the file
    from datetime import datetime
    dt = datetime.now().strftime('%d %b %Y, %H:%M:%S')
    aff_lines = []

    aff_lines.append('# Release ' + "'" + "000_baseline" + "'")
    aff_lines.append('#    Date ' + "'" + dt + "'")
    aff_lines.append('# Contact ' + "'" + "pangakupu@gmail.com" + "'")
    aff_lines.append('')
    aff_lines.append('SET UTF-8')
    aff_lines.append('BREAK 0')
    aff_lines.append('NOSPLITSUGS')
    aff_lines.append('')

    aff_lines.append('MAP 5')
    aff_lines.append('MAP aā')
    aff_lines.append('MAP eē')
    aff_lines.append('MAP iī')
    aff_lines.append('MAP oō')
    aff_lines.append('MAP uū')
    aff_lines.append('')

    aff_lines.append('REP 10')
    aff_lines.append('REP aa ā')
    aff_lines.append('REP ā aa')
    aff_lines.append('REP ee ē')
    aff_lines.append('REP ē ee')
    aff_lines.append('REP ii ī')
    aff_lines.append('REP ī ii')
    aff_lines.append('REP oo ō')
    aff_lines.append('REP ō oo')
    aff_lines.append('REP uu ū')
    aff_lines.append('REP ū uu')

    # write the file
    with open(baseline_file_path, "a") as myfile:
        for aff_line in aff_lines:
            myfile.write(aff_line + "\n")
    return True


if __name__ == '__main__':

    import sys
    import argparse
    import ast

    # create the top-level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # create the parser for the create_hpk_dic_file function
    create_hpk_dic_file_parser = subparsers.add_parser('create_hpk_dic_file')
    create_hpk_dic_file_parser.set_defaults(function = create_hpk_dic_file)

    # create the parser for the create_baseline_aff_file function
    create_baseline_aff_file_parser = subparsers.add_parser('create_baseline_aff_file')
    create_baseline_aff_file_parser.set_defaults(function = create_baseline_aff_file)

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
