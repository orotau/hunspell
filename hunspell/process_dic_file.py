'''
This module contains the functions used to process the
dictionary candidates text files.
'''

import config
from collections import Counter

unwanted_characters = [".", "(", ")", ",", "'"]


# we have to decide on these entries ...
'''
Āe, āe
Leave as is

e ai . . .
Convert to a ai

e ai ki . . .
Convert to e ai ki

E koe (E koe e koe)
Convert to E koe and E koe e koe

E nge.
Convert to E nge

He meka, he meka
Leave as is

hohou (i te) rongo
Convert to hohou i te rongo and hohou rongo

ka mahi . . .
Convert to ka mahi

kawititanga o te ringa(ringa)
Convert to kawititanga o te ringa and kawititanga o te ringaringa

kīhai ki . . .
Convert to kīhai ki

mataono (rite)
Convert to mataono and mataono rite

tahi (i te) tahua
Convert to tahi tahua and tahi i te tahua

takahi (i te) whare
Convert to takahi i te whare and takahi whare

tū atu, tū mai
leave as is
'''

def get_letter_frequency():

    '''
    Get the dic candidates and return a list of
    letter frequencies, highest to lowest, as a dictionary.

    Then the list sorted from highest to lowest

    Will initially include punctuation
    '''

    DIC_CANDIDATES_FILE_NAME = "mi_dic_candidates.txt"

    cf = config.ConfigFile()
    candidate_text_files_path = (cf.configfile[cf.computername]
                                              ['candidate_text_files_path'])

    letters = []
    letters_and_count = {}
    letter_frequency = []

    dic_candidates_file_path = \
    candidate_text_files_path + DIC_CANDIDATES_FILE_NAME
 
    with open(dic_candidates_file_path, 'r') as f:
        for line in f:
            if set(line) & set(unwanted_characters): # intersection
                print(line)
            else:
                letters.extend(list(line.replace('\n', '')))

    # print(letters)
    letters_and_count = Counter(letters).most_common()
    letter_frequency = [x[0] for x in letters_and_count]

    return letters_and_count, ''.join(letter_frequency)

if __name__ == '__main__':

    import sys
    import argparse
    import ast

    # create the top-level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # create the parser for the get_letter_frequency function
    get_letter_frequency_parser = subparsers.add_parser('get_letter_frequency')
    get_letter_frequency_parser.set_defaults(function = get_letter_frequency)

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
    
    


