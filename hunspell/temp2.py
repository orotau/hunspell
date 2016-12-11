import json_processor_hunspell as jph
all_words_for_hunspell = jph.get_all_words_for_hunspell()
for word in all_words_for_hunspell:
    if " " in word and not "-" in word:
        # open compound
        for part in word.split(" "):
            if part not in all_words_for_hunspell:
                print(part)
            
