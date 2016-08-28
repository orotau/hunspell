'''
The purpose of this module is to create text files
for hunspell, primarily the .dic and .aff files.

Each file will have a name to allow it to be referenced

Before the file is created an existing version will be checked for
If it is found then the user will be asked if they wish to overwrite

'''
import config
import os

def query_yes_no(question, default="no"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

def create_text_file(file_id):
    #create a text file with the name file_id.AFF-OR-DIC_EXTENSION
    #returns None if the text file exists and the user decides to cancel

    AFF_EXTENSION = "aff"
    AFF_FILE_ID = "mi_aff" # duplicated with the choices in the call
    DIC_EXTENSION = "dic"
    DIC_FILE_ID = "mi_dic" # duplicated with the choices in the call

    cf = config.ConfigFile()
    text_files_path = (cf.configfile[cf.computername]['text_files_path'])
    
    if file_id == AFF_FILE_ID:
        file_extension = AFF_EXTENSION
    elif file_id == DIC_FILE_ID:
        file_extension = DIC_EXTENSION
    else:
        file_extension = "ERROR"
    text_file_path = text_files_path + file_id + os.extsep + file_extension

    if os.path.isfile(text_file_path):
        # file exists, check to see if it should be overridden
        file_exists = True
        overwrite_file = query_yes_no("Do you want to OVERWRITE the existing file?")
    else:
        file_exists = False

    if file_exists and not overwrite_file:
        print("Existing file left as is")
        return None

    if file_exists and overwrite_file:
        # delete existing file
        os.remove(text_file_path)

    #time to create the file
    if file_id == AFF_FILE_ID:
        #http://linux.die.net/man/4/hunspell mainly as ref
        from datetime import datetime
        dt = datetime.now().strftime('%d %b %Y, %H:%M:%S')
        aff_lines = {}

        # Part 1
        aff_lines['0001'] = '###############################'
        aff_lines['0002'] = '# Māori affix file - Creation #'
        aff_lines['0003'] = '#### ' + dt + ' ####'
        aff_lines['0004'] = '##### pangakupu@gmail.com #####'
        aff_lines['0005'] = '###############################'
        aff_lines['0006'] = ''
        aff_lines['0007'] = '######################'
        aff_lines['0008'] = '#### part 1 of 5 #####'
        aff_lines['0009'] = '### General Options ##'
        aff_lines['0010'] = '######################'
        aff_lines['0011'] = ''
        aff_lines['0012'] = '##### set #####'
        aff_lines['0013'] = 'SET UTF-8'
        aff_lines['0014'] = '### end set ###'
        aff_lines['0015'] = ''

        # This rule says
        # Each affix rule will be identified by an integer
        aff_lines['0016'] = '##### flag #####'
        aff_lines['0017'] = 'FLAG num'
        aff_lines['0018'] = '### end flag ###'
        aff_lines['0019'] = ''

        # Part 2
        aff_lines['0020'] = '##############################'
        aff_lines['0021'] = '######## part 2 of 5 #########'
        aff_lines['0022'] = '### Options for suggestion ###
        aff_lines['0023'] = '##############################
        aff_lines['0024'] = ''

        aff_lines['0025'] = '##### key #####'
        aff_lines['0026'] = 'KEY qwertyuiop|asdfghjkl|zxcvbnm'
        aff_lines['0027'] = '### end key ###'
        aff_lines['0028'] = ''

        aff_lines['0029'] = '##### try #####'
        aff_lines['0030'] = '# TO BE ADDED'
        aff_lines['0031'] = '### end try ###'
        aff_lines['0032'] = ''

        # What does this rule do in practice?
        # ANSWER HERE
        aff_lines['0033'] = '##### maxngramsugs #####'
        aff_lines['0034'] = 'MAXNGRAMSUGS 0'
        aff_lines['0035'] = '### end maxngramsugs ###'
        aff_lines['0036'] = ''

        # What does this rule do in practice?
        # ANSWER HERE
        aff_lines['0037'] = '##### nosplitsugs #####'
        aff_lines['0038'] = 'NOSPLITSUGS'
        aff_lines['0039'] = '### end nosplitsugs ###'
        aff_lines['0040'] = ''

        aff_lines['0041'] = '##### rep #####'
        aff_lines['0042'] = 'REP 10'
        aff_lines['0043'] = 'REP a ā'
        aff_lines['0044'] = 'REP ā a'
        aff_lines['0045'] = 'REP e ē'
        aff_lines['0046'] = 'REP ē e'
        aff_lines['0047'] = 'REP i ī'
        aff_lines['0048'] = 'REP ī i'
        aff_lines['0049'] = 'REP o ō'
        aff_lines['0050'] = 'REP ō o'
        aff_lines['0051'] = 'REP u ū'
        aff_lines['0052'] = 'REP ū u'
        aff_lines['0053'] = '### end rep ###'
        aff_lines['0054'] = ''

        aff_lines['0055'] = '##### map #####'
        aff_lines['0056'] = 'MAP 5'
        aff_lines['0057'] = 'MAP aā'
        aff_lines['0058'] = 'MAP eē'
        aff_lines['0059'] = 'MAP iī'
        aff_lines['0060'] = 'MAP oō'
        aff_lines['0061'] = 'MAP uū'
        aff_lines['0062'] = '### end map ###'
        aff_lines['0063'] = ''

        # Part 3
        aff_lines['0064'] = '################################'
        aff_lines['0065'] = '######### part 3 of 5 ##########'
        aff_lines['0066'] = '### Options for comppounding ###'
        aff_lines['0067'] = '################################'
        aff_lines['0068'] = ''

        # What does this rule do in practice?
        # ANSWER HERE
        aff_lines['0069'] = '##### break #####'
        aff_lines['0070'] = 'BREAK 0'
        aff_lines['0071'] = '### end break ###'
        aff_lines['0072'] = ''

        # Part 4
        aff_lines['0073'] = '########################'
        aff_lines['0074'] = '##### part 4 of 5 ######'
        aff_lines['0075'] = '### regular suffixes ###'
        aff_lines['0076'] = '########################'
        aff_lines['0077'] = ''

        # regular suffixes
        LAST_LINE = '0077' # Match with whatever is above
        import suffixes

        # write the file
        with open(text_file_path, "a") as myfile:
            for line in sorted(aff_lines.keys()):
                myfile.write(aff_lines[line] + "\n")
        return True


    if file_id == DIC_FILE_ID:
        dic_candidates = []

        # write the file
        with open(text_file_path, "a") as myfile:
            for candidate_word in dic_candidates:
                myfile.write(candidate_word + "\n")
        return True
         


if __name__ == '__main__':

    import sys
    import argparse
    import ast

    # create the top-level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # create the parser for the get_all_entries function
    create_text_file_parser = subparsers.add_parser('create_text_file')
    create_text_file_parser.add_argument('file_id', choices = ['mi_aff',
                                                               'mi_dic'])
    create_text_file_parser.set_defaults(function = create_text_file)

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
