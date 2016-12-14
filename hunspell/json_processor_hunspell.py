import itertools
import json_processor as jp
import json_processor_suffixes as jps
import hpk_adjustments
import maoriword as mw

'''
1. Get the unique entries from the json files
2. Remove those that are not going to be used
3. Add those that will be used
   This is the list of *base words* for hunspell
4. Get suffixed words and make them unique
5. Get irregular verbs and make them unique
6. Add (1+2+3) to 4 and 5
7. Make them unique and sort Maori order - this is the list for hunspell
'''

def get_all_base_words():
    # 1. Get the unique entries from the json files
    all_entries_as_list = jp.get_all_entries_as_list() #unique

    # 2. Remove those that are not going to be used
    base_words = list(set(all_entries_as_list) - set(hpk_adjustments.remove_these))

    # 3. Add those that will be used
    all_base_words = base_words + hpk_adjustments.add_these    

    return all_base_words


def get_all_suffixed_words():
    # 4. Get suffixed words and make them unique
    distinct_suffixes_for_word_form = jps.get_distinct_suffixes_for_word_form()
    all_suffixed_words = []
    for k, v in distinct_suffixes_for_word_form.items():
        for suffix in v:
            if suffix.startswith('-'):
                suffixed_word = k + suffix[1:]
                all_suffixed_words.append(suffixed_word)
    all_distinct_suffixed_words = list(set(all_suffixed_words))
    return all_suffixed_words, all_distinct_suffixed_words


def get_all_irregular_verbs():

    # 5. Get irregular verbs and make them unique
    all_irregular_suffixes = jps.get_all_irregular_suffixes()
    all_irregular_verbs = list(all_irregular_suffixes.values())

    # squash from a list of lists to a list
    all_irregular_verbs = list(itertools.chain.from_iterable(all_irregular_verbs))

    # make unique
    all_distinct_irregular_verbs = list(set(all_irregular_verbs))
    return all_irregular_verbs, all_distinct_irregular_verbs


def get_all_words_for_hunspell():    
    # 6. 
    all_words = get_all_base_words() + \
                get_all_suffixed_words()[1] + \
                get_all_irregular_verbs()[1]

    # 7.
    all_words_for_hunspell = list(set(all_words))
    return sorted(all_words_for_hunspell, key=mw.get_list_sort_key)

def get_problem_words_in_compounds():
    # a problem word is one that is part of either
    # an open compound or a mixed compound
    # that doesn't appear in the dictionary
    problem_words_in_compounds = []
    all_words_for_hunspell = get_all_words_for_hunspell()   
    for word in all_words_for_hunspell:
        if " " in word:
            #get parts
            compound_word_parts = word.split(" ")
            for compound_word_part in compound_word_parts:
                if compound_word_part not in all_words_for_hunspell:
                    problem_words_in_compounds.append(compound_word_part)

    # make unique
    unique_problem_words_in_compounds = list(set(problem_words_in_compounds))
    unique_problem_words_in_compounds = sorted(unique_problem_words_in_compounds, 
                                               key=mw.get_list_sort_key)
    print(unique_problem_words_in_compounds)
    return(unique_problem_words_in_compounds)
                    

if __name__ == '__main__':
    import sys
    import argparse
    import ast
    import config  

    # create the top-level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # create the parser for the get_all_base_words function
    get_all_base_words_parser = subparsers.add_parser('get_all_base_words')
    get_all_base_words_parser.set_defaults(function = get_all_base_words)

    # create the parser for the get_all_suffixed_words function
    get_all_suffixed_words_parser = subparsers.add_parser('get_all_suffixed_words')
    get_all_suffixed_words_parser.set_defaults(function = get_all_suffixed_words)

    # create the parser for the get_all_irregular_verbs function
    get_all_irregular_verbs_parser = subparsers.add_parser('get_all_irregular_verbs')
    get_all_irregular_verbs_parser.set_defaults(function = get_all_irregular_verbs)

    # create the parser for the get_all_words_for_hunspell function
    get_all_words_for_hunspell_parser = subparsers.add_parser('get_all_words_for_hunspell')
    get_all_words_for_hunspell_parser.set_defaults(function = get_all_words_for_hunspell)

    # create the parser for the problem_words_in_compounds function
    get_problem_words_in_compounds_parser = \
        subparsers.add_parser('get_problem_words_in_compounds')
    get_problem_words_in_compounds_parser.set_defaults(function = \
        get_problem_words_in_compounds)

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
        #remove the function entry
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
    print(len(result))

