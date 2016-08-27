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
        all_word_forms = []

        # write the file
        with open(text_file_path, "a") as myfile:
            for candidate_word in all_word_forms:
                if " " in candidate_word:
                    # remove non-compound words
                    compound_word = candidate_word                    
                    myfile.write(compound_word + "\n")
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
