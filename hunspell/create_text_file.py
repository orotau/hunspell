'''
The purpose of this module is to create text files
for hunspell, primarily the .dic and .aff files.

Each file will have a name to allow it to be referenced

Before the file is created an existing version will be checked for
If it is found then the user will be asked if they wish to overwrite

'''
import config
import os
import aff_suffixes
import dic_suffixes

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

    # mi_dic_words.txt is the file that contains the final words
    # to which will be added the /number, number information (below)
    DIC_WORDS_EXTENSION = "txt"
    DIC_WORDS_FILE_ID = "mi_dic_words" # duplicated with the choices in the call

    # mi_dic.dic is the final dictionary with /number, number added to those
    # entries that have suffixes or prefixes (mutually exclusive)
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
        aff_lines = []

        # Part 1
        aff_lines.append('###############################')
        aff_lines.append('# Māori affix file - Creation #')
        aff_lines.append('#### ' + dt + ' ####')
        aff_lines.append('##### pangakupu@gmail.com #####')
        aff_lines.append('###############################')
        aff_lines.append('')
        aff_lines.append('######################')
        aff_lines.append('#### part 1 of 5 #####')
        aff_lines.append('### General Options ##')
        aff_lines.append('######################')
        aff_lines.append('')
        aff_lines.append('##### set #####')
        aff_lines.append('SET UTF-8')
        aff_lines.append('### end set ###')
        aff_lines.append('')

        # This rule says
        # Each affix rule will be identified by an integer
        aff_lines.append('##### flag #####')
        aff_lines.append('FLAG num')
        aff_lines.append('### end flag ###')
        aff_lines.append('')

        # Part 2
        aff_lines.append('##############################')
        aff_lines.append('######## part 2 of 5 #########')
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

        # What does this rule do in practice?
        # If we set this to 0 then the word 'man' will
        # get no suggestions, which is unacceptable.
        # If we set this to 999 then the word 'manākitanga' gets these 9 suggestions
        # 'manaakitanga', 'makitatanga', 'tamarikitanga', 'matanātanga', 
        # 'mangaekatanga', 'mamangatanga', 'mangamangatanga', 'mairangatanga', 'kiritangata'
        # which seems a bit over the top
        # 
        #aff_lines.append('##### maxngramsugs #####')
        #aff_lines.append('# Default')
        #aff_lines.append('### end maxngramsugs ###')
        #aff_lines.append('')

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
        aff_lines.append('######### part 3 of 5 ##########')
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

        # Part 4
        aff_lines.append('########################')
        aff_lines.append('##### part 4 of 5 ######')
        aff_lines.append('### regular suffixes ###')
        aff_lines.append('########################')
        aff_lines.append('')

        # regular suffixes
        '''
        Each entry will have 5 lines as follows
        ##### 001 of 140 #####
        SFX 1 N 1
        SFX 1 0 a
        ### end 001 of 140 ###

        '''        
        total_of_suffixes = (
            len(aff_suffixes.regular_suffixes) +
            len(aff_suffixes.irregular_suffixes)
            )

        total_of_suffixes = str(total_of_suffixes).rjust(3, '0')
        

        for index, suffix in enumerate(aff_suffixes.regular_suffixes):
            suffix_number = index + 1

            # first line
            aff_lines.append(
                "##### " + 
                str(suffix_number).rjust(3, '0') +
                " of " +
                total_of_suffixes + 
                " #####"
                )

            # second line
            aff_lines.append(
                "SFX " + str(suffix_number) + " N 1"
                )
        
            # third line 
            aff_lines.append(
                "SFX " + str(suffix_number) + " 0 " + suffix[1:]    
                ) 
                        
            # fourth line
            aff_lines.append(
                "### end " + 
                str(suffix_number).rjust(3, '0') +
                " of " +
                total_of_suffixes + 
                " ###"
                )

            # fifth line
            aff_lines.append('')

        # Part 5
        aff_lines.append('########################')
        aff_lines.append('##### part 5 of 5 ######')
        aff_lines.append('## irregular suffixes ##')
        aff_lines.append('########################')
        aff_lines.append('')     

        aff_lines.append('##### fullstrip #####')
        aff_lines.append('FULLSTRIP')
        aff_lines.append('### end fullstrip ###')
        aff_lines.append('') 

        # irregular suffixes
        '''
        Each entry will have 5 or MORE lines as follows
        ##### 123 of 140 #####
        SFX 123 N 2
        SFX 123 kukume kumea .
        SFX 123 kukume kumenga .
        ### end 123 of 140 ###

        '''
        for index, (k, v) in enumerate(aff_suffixes.irregular_suffixes.items()):
            suffix_number = len(aff_suffixes.regular_suffixes) + index + 1

            # first line
            aff_lines.append(
                "########### " + 
                str(suffix_number).rjust(3, '0') +
                " of " +
                total_of_suffixes + 
                " ###########"
                )

            # second line
            aff_lines.append(
                "SFX " + str(suffix_number) + " N " + str(len(v))
                )
        
            # third plus line(s)
            for word in v:
                aff_lines.append(
                    "SFX " + 
                    str(suffix_number) + " " +
                    k + " " +
                    word + " "
                    "."    
                ) 
                        
            # penultimate line
            aff_lines.append(
                "######### end " + 
                str(suffix_number).rjust(3, '0') +
                " of " +
                total_of_suffixes + 
                " #########"
                )

            # last line
            aff_lines.append('')

        aff_lines.append(aff_lines[0])
        aff_lines.append(aff_lines[1])
        aff_lines.append(aff_lines[2])
        aff_lines.append(aff_lines[3])
        aff_lines.append(aff_lines[4])

        # write the file
        with open(text_file_path, "a") as myfile:
            for aff_line in aff_lines:
                myfile.write(aff_line + "\n")
        return True


    if file_id == DIC_WORDS_FILE_ID:
        
        '''
        We take the dic candidates text file and do various things to it
        a) Deal with the 'unusual' entries in HPK
        b) Add back in anything that was manually removed initially
        c) Add words that are in the 'tauira' but not in the dictionary
           How this will be done exactly is still to be decided.  
        d) Possibly add other words (again to be decided)
           Maybe some tech words e.g. 'Pukamata', maybe some placenames          
        '''
        dic_words = []
        dic_candidates_text_file_path = (
            cf.configfile[cf.computername]['dic_candidates_text_file_path']
            )

        # read the candidates file
        with open(dic_candidates_text_file_path, "r") as candidates_file:
            for line in candidates_file:
                candidate_word = line.replace('\n', '')           



    if file_id == DIC_FILE_ID:
        
        dic_file = []
        dic_candidates_text_file_path = (
            cf.configfile[cf.computername]['UPDATE']
            )

        # read the candidates file
        with open(dic_candidates_text_file_path, "r") as candidates_file:
            for line in candidates_file:
                candidate_word = line.replace('\n', '')

                try:
                    suffixes = dic_suffixes.words_and_suffixes[candidate_word]              
                    
                except KeyError:
                    # the word has no suffixes
                    dic_file.append(candidate_word)

                else:
                    # the candidate word has at least one suffix
                    # each regular suffix will have 1 number associated with it
                    # in the dic file

                    # if there are any irregular suffixes they will be grouped together
                    # and the group will have one number associated with it in the dic file

                    suffix_numbers = []

                    irregular_suffix_found = False                
                    for suffix in suffixes:
                        if suffix.startswith('-'):
                            # we have a regular suffix
                            suffix_numbers.append(aff_suffixes.regular_suffixes.index(suffix) + 1)                        
                        else:
                            # we have an irregular suffix
                            if not irregular_suffix_found:
                                irregular_suffix_number = (
                                    list(aff_suffixes.irregular_suffixes.keys()).index(candidate_word) + 
                                    1 + len(aff_suffixes.regular_suffixes)
                                    )
                                suffix_numbers.append(irregular_suffix_number)
                                irregular_suffix_found = True
                            else:
                                pass # already processed one irregular suffix

                    suffix_text = "/"+ ','.join(str(x) for x in sorted(suffix_numbers))
                    dic_file_text = candidate_word + suffix_text
                    dic_file.append(dic_file_text)                
                    
        # write the file
        with open(text_file_path, "a") as myfile:
            myfile.write(str(len(dic_file)) + "\n")
            for dic_file_line in dic_file:
                myfile.write(dic_file_line + "\n")
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
                                                               'mi_dic_words',
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
