'''
Create a test aff file for testing which will be used
with the file hpk.dic 

'''
import config
import os
import query_yes_no
import sys

print()

cf = config.ConfigFile()
test_dicaff_files_path = (cf.configfile[cf.computername]['test_dicaff_files_path'])

if sys.argv[1] == "create_test_dic_file":
    file_name = "hpk.dic"
elif sys.argv[1] == "create_test_aff_file":
    file_name = "test.aff"
else:
    file_name = "oops.oops"

test_dicaff_file_path = test_dicaff_files_path + file_name

if os.path.isfile(test_dicaff_file_path):
    # file exists, check to see if it should be overridden
    file_exists = True
    overwrite_file = query_yes_no.query_yes_no("OVERWRITE the existing file?")
else:
    file_exists = False

def create_test_dic_file():

    if file_exists and not overwrite_file:
        print("Existing file left as is")
        return None

    if file_exists and overwrite_file:
        # delete existing file
        os.remove(test_dicaff_file_path)

    # write the file
    import json_processor_hunspell as jph
    all_words_for_hunspell = jph.get_all_words_for_hunspell()
    with open(test_dicaff_file_path, "a", encoding = 'utf-8') as myfile:
        myfile.write(str(len(all_words_for_hunspell)) + "\n")
        for word in all_words_for_hunspell:
            myfile.write(word + "\n")
    return True
    

def create_test_aff_file():

    if file_exists and not overwrite_file:
        print("Existing file left as is")
        return None

    if file_exists and overwrite_file:
        # delete existing file
        os.remove(test_dicaff_file_path)


    #time to create the file
    #http://linux.die.net/man/4/hunspell mainly as ref
    from datetime import datetime
    dt = datetime.now().strftime('%d %b %Y, %H:%M:%S')
    aff_lines = []

    # Part 1
    aff_lines.append('###############################')
    aff_lines.append('# Māori affix file - Creation #')
    aff_lines.append('#### ' + dt + ' ####')
    aff_lines.append('##### pangakupu@gmail.com #####')
    aff_lines.append('###############################')
    aff_lines.append('')
    aff_lines.append('######################')
    aff_lines.append('#### part 1 of 3 #####')
    aff_lines.append('### General Options ##')
    aff_lines.append('######################')
    aff_lines.append('')
    aff_lines.append('##### set #####')
    aff_lines.append('SET UTF-8')
    aff_lines.append('### end set ###')
    aff_lines.append('')

    # Part 2
    aff_lines.append('##############################')
    aff_lines.append('######## part 2 of 3 #########')
    aff_lines.append('### Options for suggestion ###')
    aff_lines.append('##############################')
    aff_lines.append('')

    aff_lines.append('##### key #####')
    aff_lines.append('KEY qwertyuiop|asdfghjkl|zxcvbnm')
    aff_lines.append('### end key ###')
    aff_lines.append('')

    #aff_lines.append('##### try #####')
    #aff_lines.append('# Nothing looks ok at moment #')
    #aff_lines.append('### end try ###')
    #aff_lines.append('')

    # What does maxngramsugs do in practice?
    # If we set maxngramsugs to 0 then the word 'man' will
    # get no suggestions, which is unacceptable.

    # If we set this to 999 then the word 'manākitanga' gets these 9 suggestions
    # 'manaakitanga', 'makitatanga', 'tamarikitanga', 'matanātanga', 
    # 'mangaekatanga', 'mamangatanga', 'mangamangatanga', 'mairangatanga', 'kiritangata'
    # which seems a bit over the top
    # 
    aff_lines.append('##### maxngramsugs #####')
    aff_lines.append('# USE DEFAULT')
    aff_lines.append('### end maxngramsugs ###')
    aff_lines.append('')

    # What does this rule do in practice?
    # ANSWER HERE
    aff_lines.append('##### nosplitsugs #####')
    aff_lines.append('NOSPLITSUGS')
    aff_lines.append('### end nosplitsugs ###')
    aff_lines.append('')

    aff_lines.append('##### rep #####')
    aff_lines.append('REP 20')
    aff_lines.append('REP a ā')
    aff_lines.append('REP ā a')
    aff_lines.append('REP e ē')
    aff_lines.append('REP ē e')
    aff_lines.append('REP i ī')
    aff_lines.append('REP ī i')
    aff_lines.append('REP o ō')
    aff_lines.append('REP ō o')
    aff_lines.append('REP u ū')
    aff_lines.append('REP ū u')
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
    aff_lines.append('### end rep ###')
    aff_lines.append('')

    aff_lines.append('##### map #####')
    aff_lines.append('MAP 5')
    aff_lines.append('MAP aā')
    aff_lines.append('MAP eē')
    aff_lines.append('MAP iī')
    aff_lines.append('MAP oō')
    aff_lines.append('MAP uū')
    aff_lines.append('### end map ###')
    aff_lines.append('')

    # Part 3
    aff_lines.append('################################')
    aff_lines.append('######### part 3 of 3 ##########')
    aff_lines.append('### Options for comppounding ###')
    aff_lines.append('################################')
    aff_lines.append('')

    # What does this rule do in practice?
    # This prevents foo-bar or bar-foo from being 'ok' if
    # foo and bar are in the dictionary but not foo-bar or bar-foo
    aff_lines.append('##### break #####')
    aff_lines.append('BREAK 0')
    aff_lines.append('### end break ###')
    aff_lines.append('')


    # write the file
    with open(test_dicaff_file_path, "a") as myfile:
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

    # create the parser for the create_test_dic_file function
    create_test_dic_file_parser = subparsers.add_parser('create_test_dic_file')
    create_test_dic_file_parser.set_defaults(function = create_test_dic_file)

    # create the parser for the create_test_aff_file function
    create_test_aff_file_parser = subparsers.add_parser('create_test_aff_file')
    create_test_aff_file_parser.set_defaults(function = create_test_aff_file)

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
