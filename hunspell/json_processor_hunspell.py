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

def get_all_words_for_hunspell():
    # 1. Get the unique entries from the json files
    all_entries_as_list = jp.get_all_entries_as_list()

    # 2. Remove those that are not going to be used
    base_words = list(set(all_entries_as_list) - set(hpk_adjustments.remove_these))

    # 3. Add those that will be used
    base_words = base_words + hpk_adjustments.add_these

    # 4. Get suffixed words and make them unique
    distinct_suffixes_for_word_form = jps.get_distinct_suffixes_for_word_form()
    all_suffixed_words = []
    for k, v in distinct_suffixes_for_word_form.items():
        for suffix in v:
            if suffix.startswith('-'):
                suffixed_word = k + suffix[1:]
                all_suffixed_words.append(suffixed_word)
    all_distinct_suffixed_words = list(set(all_suffixed_words))

    # 5. Get irregular verbs and make them unique
    all_irregular_suffixes = jps.get_all_irregular_suffixes()
    all_irregular_verbs = list(all_irregular_suffixes.values())

    # squash from a list of lists to a list
    all_irregular_verbs = list(itertools.chain.from_iterable(all_irregular_verbs))

    # make unique
    all_distinct_irregular_verbs = list(set(all_irregular_verbs))

    # 6. 
    all_words = base_words + all_distinct_suffixed_words + all_distinct_irregular_verbs

    # 7.
    all_words_for_hunspell = list(set(all_words))
    return sorted(all_words_for_hunspell, key=mw.get_list_sort_key)

if __name__ == '__main__':
    result = get_all_words_for_hunspell()

