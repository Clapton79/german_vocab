# browse dictionary and get info on dictionary data

from vocab import *
from vocab_utilities import bcolors
from add_words import add_words
import os
from pprint import pprint
import re

def test(vc:Vocabulary):
    try:
        my_test = LanguageTest(number_of_questions,
                                    'definite article', test_v, True)
        my_test.run()
    except Exception as e:
        print(f'Error in test function: {str(e)}')
def daily_test(vc:Vocabulary):
    try:
        print(get_available_tests())

        number_of_questions = input('How many questions do you want? (10)')

        if number_of_questions == '':
            number_of_questions = 10
        else:
            number_of_questions = int(number_of_questions)

        base_v = vc

        print(base_v.tags())
        tag_filter = input('Tag filter: ')
        if len(tag_filter) > 0:
            print(f'Using tag filter: {tag_filter}')
            print("Creating test vocabulary...")
            test_v = base_v.clone(tag_filter=tag_filter)
            print ("Creating test vocabulary for adjectives...")
            adj_v = base_v.clone(word_class_filter='adjective', tag_filter=tag_filter)
            print("Creating test vocabulary for verbs...")
            verbs_v = base_v.clone(word_class_filter='verb', tag_filter=tag_filter)
            print("Creating test vocabulary for nouns...")
            nouns_v = base_v.clone(word_class_filter='noun', tag_filter=tag_filter)
            print("Creating test vocabulary for adverbs...")
            adv_v = base_v.clone(word_class_filter='adverb', tag_filter=tag_filter)
            print("Creating test vocabulary for phrases...")
            phrase_v = base_v.clone(word_class_filter='phrase', tag_filter=tag_filter)

        else:
            test_v = base_v.clone()
            adj_v = base_v.clone(word_class_filter='adjective')
            verbs_v = base_v.clone(word_class_filter='verb')
            nouns_v = base_v.clone(word_class_filter='noun')
            adv_v = base_v.clone(word_class_filter='adverb')
            phrase_v= base_v.clone(word_class_filter='phrase')



        if number_of_questions > 0:
            # noun translation test
            try:
                if nouns_v is not None and len(nouns_v.vocab.keys()) > 0:
                    print(f"vocabulary rowset: {len(nouns_v.vocab.keys())} words")
                    my_test = LanguageTest(number_of_questions,
                                        "translation", nouns_v, True)
                    my_test.run()
                else:
                    print(f'{bcolors.FAIL}No words found in vocabulary for translation test.{bcolors.ENDC}')
            except Exception as e:
                print(f'Error creating translation test: {str(e)}')
                return

            # adjective translation test
            try:
                if adj_v is not None and len(adj_v.vocab.keys()) > 0:
                    print(f"vocabulary rowset: {len(adj_v.vocab.keys())} words")
                    my_test = LanguageTest(number_of_questions,
                                        "translation", adj_v, True)
                    my_test.run()
                else:
                    print(f'{bcolors.FAIL}No words found in vocabulary for adjective translation test.{bcolors.ENDC}')
            except Exception as e:
                print(f'Error creating translation test: {str(e)}')
                return

            # adverb translation test
            try:
                if adv_v is not None and len(adv_v.vocab.keys()) > 0:
                    print(f"vocabulary rowset: {len(adv_v.vocab.keys())} words")
                    my_test = LanguageTest(number_of_questions,
                                        "translation", adv_v, True)
                    my_test.run()
                else:
                    print(f'{bcolors.FAIL}No words found in vocabulary for adverb translation test.{bcolors.ENDC}')
            except Exception as e:
                print(f'Error creating translation test: {str(e)}')
                return

            # phrase translation test
            try:
                if phrase_v is not None and len(phrase_v.vocab.keys()) > 0:
                    print(f"vocabulary rowset: {len(phrase_v.vocab.keys())} words")
                    my_test = LanguageTest(number_of_questions,
                                        "translation", phrase_v, True)
                    my_test.run()
                else:
                    print(f'{bcolors.FAIL}No words found in vocabulary for phrase translation test.{bcolors.ENDC}')
            except Exception as e:
                print(f'Error creating translation test: {str(e)}')
                return

            # verb translation test
            try:
                if verbs_v is not None and len(verbs_v.vocab.keys()) > 0:
                    print(f"vocabulary rowset: {len(verbs_v.vocab.keys())} words")
                    my_test = LanguageTest(number_of_questions,
                                        "translation", verbs_v, True)
                    my_test.run()
                else:
                    print(f'{bcolors.FAIL}No words found in vocabulary for verb translation test.{bcolors.ENDC}')
            except Exception as e:
                print(f'Error creating translation test: {str(e)}')
                return

            # noun definite article
            try:
                if nouns_v is not None and len(nouns_v.vocab.keys()) > 0:
                    print(f'Dictionary elements: {len(nouns_v.vocab.keys())}')
                    my_test = LanguageTest(number_of_questions,
                                        'definite article', nouns_v, True)
                    my_test.run()
                else:
                    print(f'{bcolors.FAIL}No nouns found in vocabulary for definite article test.{bcolors.ENDC}')
            except Exception as e:
                print(f'Error creating definite article test: {str(e)}')
                return

            # verb conjugation
            try:
                if verbs_v is not None and len(verbs_v.vocab.keys()) > 0:
                    print(f'Dictionary elements: {len(verbs_v.vocab.keys())}')
                    my_test = LanguageTest(number_of_questions,
                                        'verb conjugation', verbs_v, True)
                    my_test.run()
                else:
                    print(f'{bcolors.FAIL}No verbs found in vocabulary for conjugation test.{bcolors.ENDC}')
            except Exception as e:
                print(f'Error creating verb conjugation test: {str(e)}')
                return
            
            # verb imperative
            try:
                if verbs_v is not None and len(verbs_v.vocab.keys()) > 0:
                    print(f'Dictionary elements: {len(verbs_v.vocab.keys())}')
                    my_test = LanguageTest(number_of_questions,
                                        'imperative verb form', verbs_v, True)
                    my_test.run()
                else:
                    print(f'{bcolors.FAIL}No verbs found in vocabulary for imperative verb form test.{bcolors.ENDC}')
            except Exception as e:
                print(f'Error creating verb imperative verb form test: {str(e)}')
                return

            # inverse translation test
            try:
                if test_v is not None and len(test_v.vocab.keys()) > 0:
                    print(f"vocabulary rowset: {len(test_v.vocab.keys())} words")
                    my_test = LanguageTest(number_of_questions,
                                        "inverse translation", test_v, True)
                    my_test.run()
                else:
                    print(f'{bcolors.FAIL}No words found in vocabulary for inverse translation test.{bcolors.ENDC}')
            except Exception as e:
                print(f'Error creating inverse translation test: {str(e)}')
                return

    except Exception as e:
        print(f'Error during daily test: {str(e)}')
        return

def vocab_summary(vc:Vocabulary):
    try:
        types=[y['class'] for x,y in vc.vocab.items()]
        
        for item in list(set(types)):
            print(f'{item.ljust(15," ")}: {len([x for x in types if x==item])}')
        
        print(f'{"TOTAL".ljust(15," ")}: {len(types)}')
    except Exception as e:
        print(f'Error during vocabulary summary: {str(e)}')
        return
def word_finder(vc:Vocabulary):
    try:
        rx = input("Type a filter: ")

        result=[x for x in vc.vocab.keys() if rx in x]                                                  # search in words
        result2=[x for x in vc.vocab.keys() if rx in vc.vocab[x]['translations']['hungarian'][0]]       # search in the first translations
        result=list(set(result+result2))

        if 0<len(result)<20:
            print('='*120)
            report=[(x,f'({vc[x]["class"][0]}){vc[x].get("definite_article", "")} {x.ljust(35," ")} {", ".join(vc[x]["translations"]["hungarian"])}') for x in result]
            print(' ')
            for item in report: 
                print(f'Word:   {item[1]}')
                if vc.vocab[item[0]]['class']=='verb':
                    conjugation_table(vc,item[0])
            
                print('')
                print('='*120)
                print('')
            print(f'Number of words matching pattern {rx}: {len(result)} (of {len(vc.vocab)})')
        if len(result)==0:
            print(f'{bcolors.FAIL}No word matched pattern {rx}{bcolors.ENDC}')
        if 20<=len(result)<len(vc.vocab.keys()):
            print(f'{bcolors.WARNING}Too many words matched pattern {rx}: {len(result)} (of {len(vc.vocab)}){bcolors.ENDC}')
        elif len(result)==len(vc.vocab.keys()):
            print(f'{bcolors.OKGREEN}All words in dictionary matched pattern {rx}.{bcolors.ENDC}')

    except Exception as e: 
        print(f'Search error: {str(e)}')
  
def add_new_words(vc:Vocabulary):
    try:
        add_words(vc)
    except Exception as e:
        print(f'Error during adding new words: {str(e)}')
        return

def list_words_for_tags (vc:Vocabulary):
    """
    Lists all words for that have all the given tags
    """
    try:
        tags = input("Type tags (separate items by comma): ")
        tags = tags.split(',')
        if len(tags) == 0:
            print(f'{bcolors.FAIL}No tags entered.{bcolors.ENDC}')
            return
        result = []
        for i, tag in enumerate(tags):
            if i == 0:
                result = vc.filter(tag=tag)
            
            filter = vc.filter(tag=tag)
            result = [word for word in result if word in filter]
       
        if len(result)>0:
            print(result)
            print(f'Number of words with these tags: {len(result)}')
        else:
            print(f'No words with entered tags')
    except Exception as e:
        print(f'Error during tag search: {str(e)}')

def list_words_for_tag (vc:Vocabulary):
    """
    Lists all words for a given tag.
    """
    try:
        tag = input("Type a tag: ")
        if len(tag) == 0:
            print(f'{bcolors.FAIL}No tag entered.{bcolors.ENDC}')
            return
        result = list(vc.filter(tag=tag))
        if len(result)>0:
            print(result)
            print(f'Number of words with this tag: {len(result)}')
        else:
            print(f'No words with tag {tag}')
    except Exception as e:
        print(f'Error during tag search: {str(e)}')
def list_words_for_tag_and_class(vc:Vocabulary):
    try:
        tag = input("Type a tag: ")
        word_class = input("Type a word class: ")
        result =  list(vc.filter(word_class=word_class, tag=tag))
        if len(result)==0:
            print(f'No {word_class}s with tag {tag}')
            
        else:
            print(f'Number of {word_class}s with tag {tag}: {len(result)}')
            print(result)
    except Exception as e:
        print(f'Error during tag and class search: {str(e)}')


def tags_in_vocabulary(vc:Vocabulary):
    try:
        tags = vc.tags()
        if len(tags) > 0:
            print("Tags in vocabulary:")
            for tag in tags:
                print(f"- {tag}")
        else:
            print("No tags found in vocabulary.")
    except Exception as e:
        print(f'Error retrieving tags: {str(e)}')

def test_verb_conjugation_Perfekt(vc:Vocabulary):
    try: 
        number_of_questions = input('How many questions do you want?')
        if not number_of_questions.isdigit():
            raise ValueError(f'{bcolors.FAIL}Invalid input. Please enter a number.{bcolors.ENDC}')

        number_of_questions = int(number_of_questions)
        tag_filter = input(f'Tag filter: ')
        if len(tag_filter) == 0:
            tag_filter = None
            va = vc.clone(word_class_filter='verb')
        else:
            va = vc.clone(word_class_filter='verb', tag_filter=tag_filter)

        if va is not None and len(va.vocab.keys()) > 0:
            print(f"vocabulary rowset: {len(va.vocab.keys())} words")
            my_test = LanguageTest(number_of_questions,
                                'verb conjugation Perfekt', va, True)
            my_test.run()
        else:
            raise IndexError(f'{bcolors.FAIL}No verbs found in vocabulary for conjugation test.{bcolors.ENDC}')

    except Exception as e:
        print(f'Error in verb translation test: {str(e)}')
        return

def test_definite_article(vc:Vocabulary):
    try: 
        number_of_questions = input('How many questions do you want?')
        if not number_of_questions.isdigit():
            raise ValueError(f'{bcolors.FAIL}Invalid input. Please enter a number.{bcolors.ENDC}')

        number_of_questions = int(number_of_questions)
        tag_filter = input('Tag filter: ')
        if len(tag_filter) == 0:
            va = vc.clone(word_class_filter='noun')
        else:
            va = vc.clone(word_class_filter='noun', tag_filter=tag_filter)
        if va is None or len(va.vocab.keys()) == 0:
            raise IndexError(f'{bcolors.FAIL}No nouns found in vocabulary for noun translation test.{bcolors.ENDC}')

        if va is not None and len(va.vocab.keys()) > 0:
            print(f"vocabulary rowset: {len(va.vocab.keys())} words")
            my_test = LanguageTest(number_of_questions,
                                'definite article', va, True)
            my_test.run()
        else:
            raise IndexError(f'{bcolors.FAIL}No nouns found in vocabulary for definite article test.{bcolors.ENDC}')

    except Exception as e:
        print(f'Error in definite article test: {str(e)}')
        return
def test_adjective_translation(vc:Vocabulary):
    try: 
        number_of_questions = input('How many questions do you want?')
        if not number_of_questions.isdigit():
            raise ValueError(f'{bcolors.FAIL}Invalid input. Please enter a number.{bcolors.ENDC}')

        number_of_questions = int(number_of_questions)
        tag_filter = input('Tag filter: ')
        if len(tag_filter) == 0:
            va = vc.clone(word_class_filter='adjective')
        else:
            va = vc.clone(word_class_filter='adjective', tag_filter=tag_filter)

        if va is None or len(va.vocab.keys()) == 0:
            raise IndexError(f'{bcolors.FAIL}No adjectives found in vocabulary for adjective translation test.{bcolors.ENDC}')
        if va is not None and len(va.vocab.keys()) > 0:
            print(f"vocabulary rowset: {len(va.vocab.keys())} words")
            my_test = LanguageTest(number_of_questions,
                                'translation', va, True)
            my_test.run()
        else:
            raise IndexError(f'{bcolors.FAIL}No adjectives found in vocabulary for adjective translation test.{bcolors.ENDC}')

    except Exception as e:
        print(f'Error in noun translation test: {str(e)}')
        return
def test_adverb_translation(vc:Vocabulary):
    try: 
        number_of_questions = input('How many questions do you want?')
        if not number_of_questions.isdigit():
            raise ValueError(f'{bcolors.FAIL}Invalid input. Please enter a number.{bcolors.ENDC}')

        number_of_questions = int(number_of_questions)
        tag_filter = input('Tag filter: ')
        if len(tag_filter) == 0:
            va = vc.clone(word_class_filter='adverb')
        else:
            va = vc.clone(word_class_filter='adverb', tag_filter=tag_filter)
        if va is None or len(va.vocab.keys()) == 0:
            raise IndexError(f'{bcolors.FAIL}No adverbs found in vocabulary for adverb translation test.{bcolors.ENDC}')
        if va is not None and len(va.vocab.keys()) > 0:
            print(f"vocabulary rowset: {len(va.vocab.keys())} words")
            my_test = LanguageTest(number_of_questions,
                                'translation', va, True)
            my_test.run()
        else:
            raise IndexError(f'{bcolors.FAIL}No nouns found in vocabulary for noun translation test.{bcolors.ENDC}')

    except Exception as e:
        print(f'Error in noun translation test: {str(e)}')
        return
def test_noun_translation(vc:Vocabulary):
    try: 
        number_of_questions = input('How many questions do you want?')
        if not number_of_questions.isdigit():
            raise ValueError(f'{bcolors.FAIL}Invalid input. Please enter a number.{bcolors.ENDC}')

        number_of_questions = int(number_of_questions)
        tag_filter = input('Tag filter: ')
        if len(tag_filter) == 0:
            va = vc.clone(word_class_filter='noun')
        else:
            va = vc.clone(word_class_filter='noun', tag_filter=tag_filter)
        if va is None or len(va.vocab.keys()) == 0:
            raise IndexError(f'{bcolors.FAIL}No nouns found in vocabulary for noun translation test.{bcolors.ENDC}')
        if va is not None and len(va.vocab.keys()) > 0:
            print(f"vocabulary rowset: {len(va.vocab.keys())} words")
            my_test = LanguageTest(number_of_questions,
                                'translation', va, True)
            my_test.run()
        else:
            raise IndexError(f'{bcolors.FAIL}No nouns found in vocabulary for noun translation test.{bcolors.ENDC}')

    except Exception as e:
        print(f'Error in noun translation test: {str(e)}')
        return
def test_verb_translation(vc:Vocabulary):
    try: 
        number_of_questions = input('How many questions do you want?')
        if not number_of_questions.isdigit():
            raise ValueError(f'{bcolors.FAIL}Invalid input. Please enter a number.{bcolors.ENDC}')

        number_of_questions = int(number_of_questions)
        tag_filter = input('Tag filter: ')
        if len(tag_filter) == 0:
            va = vc.clone(word_class_filter='verb')
        else:
            va = vc.clone(word_class_filter='verb', tag_filter=tag_filter)
        if va is None or len(va.vocab.keys()) == 0:
            raise IndexError(f'{bcolors.FAIL}No verbs found in vocabulary for verb translation test.{bcolors.ENDC}')
        if va is not None and len(va.vocab.keys()) > 0:
            print(f"vocabulary rowset: {len(va.vocab.keys())} words")
            my_test = LanguageTest(number_of_questions,
                                'translation', va, True)
            my_test.run()
        else:
            raise IndexError(f'{bcolors.FAIL}No verbs found in vocabulary for verb translation test.{bcolors.ENDC}')

    except Exception as e:
        print(f'Error in noun translation test: {str(e)}')
        return
def test_verb_conjugation_praet(vc:Vocabulary):
    try: 
        number_of_questions = input('How many questions do you want?')
        if not number_of_questions.isdigit():
            raise ValueError(f'{bcolors.FAIL}Invalid input. Please enter a number.{bcolors.ENDC}')

        number_of_questions = int(number_of_questions)
        # tag_filter = input('Tag filter: ')
        # if len(tag_filter) == 0:
        #     raise ValueError("Tag filter cannot be empty.")
       
        va = vc.clone(word_class_filter='verb')
        if va is None or len(va.vocab.keys()) == 0:
            raise IndexError(f'{bcolors.FAIL}No verbs found in vocabulary for verb translation test.{bcolors.ENDC}')
        if va is not None and len(va.vocab.keys()) > 0:
            print(f"vocabulary rowset: {len(va.vocab.keys())} words")
            my_test = LanguageTest(number_of_questions,
                                'verb conjugation Präteritum', va, True)
            my_test.run()
        else:
            raise IndexError(f'{bcolors.FAIL}No verbs found in vocabulary for verb translation test.{bcolors.ENDC}')

    except Exception as e:
        print(f'Error in verb conjugation Präteritum test: {str(e)}')
        return

def filter_words(vc:Vocabulary):
    try:
        tag_filter = input('Tag filter: ')
        word_class_filter = input('Word class filter: ')

        if len(tag_filter)==0:
            tag_filter = None
        if len(word_class_filter)==0:
            word_class_filter = None

        result=vc.filter(word_class=word_class_filter, tag=tag_filter)
        if len(result)==0:
            print(f'{bcolors.FAIL}No words found for the specified filters.{bcolors.ENDC}')
        elif len(result)==len(vc.vocab.keys()):
            print(f'{bcolors.OKGREEN}All words match the specified filters.{bcolors.ENDC}')
        else:
            print(f'{len(result)} words found.')
            print(result)

    except Exception as e:
        print(f'Error in filter words: {str(e)}')
        return

def conjugation_table(vc:Vocabulary,word:str):
    try:
        print(f'{bcolors.OKCYAN}###############################################################{bcolors.ENDC}')
        print(f'#                   {bcolors.OKBLUE}Conjugation{bcolors.ENDC}')
        print(f'{bcolors.OKCYAN}###############################################################{bcolors.ENDC}')
        print("")
        
        margin = 15
        if word not in vc.vocab.keys():
            raise IndexError(f'{bcolors.FAIL}This word is not found in vocabulary.{bcolors.ENDC}')
        word_class = vc.vocab[word].get('class', 'No class')
        if word_class != 'verb':
            raise ValueError(f'{bcolors.FAIL}This word is not a verb ({word_class}){bcolors.ENDC}')
        # Generate conjugation table
        table = []
        pronouns = ['ich', 'du', 'er/sie/es', 'wir', 'ihr', 'sie/Sie']
        conjugations_prae = vc.vocab[word].get('conjugations', {}).get('Präsens', [])
        conjugations_prae = conjugations_prae[:6]  # Limit to 6 forms
        conjugations_praet = vc.vocab[word].get('conjugations',{}).get('Präteritum',[])
        conjugations_praet = conjugations_praet[:6]  # Limit to 6 forms
        conjugations_perf = vc.vocab[word].get('conjugations',{}).get('Perfekt',[])
        conjugations_perf = conjugations_perf[:6]  # Limit to 6 forms

        # vowel journey across tenses
        vowel_journey = f'{"Präsens -> Präteritum -> Perfekt:".ljust(35," ")} {get_first_vowel(conjugations_prae[0])} -> {get_first_vowel(conjugations_praet[0])} -> {get_first_vowel(conjugations_perf[0].replace("ge","").split(" ")[-1])}'
        print(vowel_journey)
        print('')
        # vowel journey across pronouns
        vowel_journey = f'{"ich -> du -> er/sie/es:".ljust(35," ")} {get_first_vowel(conjugations_prae[0])} -> {get_first_vowel(conjugations_prae[1])} -> {get_first_vowel(conjugations_prae[2])}'
        print(vowel_journey)
        print('')
        imperative = vc.vocab[word].get('imperative', "").capitalize()
        if len(imperative) > 0:
            print(f'Imperative: {imperative}!')

        print('')
        header='     '.join(['Präsens'.ljust(margin, ' '), 'Präteritum'.ljust(margin, ' '), 'Perfekt'.ljust(margin, ' ')])
        print(header)
        print('-' * len(header))
        for i in range(6):
            print('     '.join([conjugations_prae[i].ljust(margin, ' '), conjugations_praet[i].ljust(margin, ' '), conjugations_perf[i].ljust(margin, ' ')]))

    except Exception as e:
        print(f'Error in conjugation_table: {str(e)}')
        return

def reload_vocabulary(vc:Vocabulary):
    try:
        tag_filter = input('Tag filter: ')
        word_class_filter = input('Word class filter: ')
        ve=vc.clone(word_class_filter=word_class_filter, tag_filter=tag_filter)
        if ve is None:
            raise IndexError(f'{bcolors.FAIL}No words found for the specified filters.{bcolors.ENDC}')
        else:
            browser_menu(ve)
    except Exception as e:
        print(f'Error in reload menu: {str(e)}')
        return


def browser_menu(vc:Vocabulary):
    try:
        print(f'{bcolors.OKCYAN}####################################################################{bcolors.ENDC}')
        print(f'#                   {bcolors.OKBLUE}Vocabulary Browser{bcolors.ENDC}')
        print(f'{bcolors.OKCYAN}####################################################################{bcolors.ENDC}')
        print("")
        print("")

        print(f"Loaded vocabulary: {vc.filename} ({vc.custom_data['language']})")
        print("")
        no_return = False
        
        browser_functions = {
            "Word finder": word_finder,
            "Reload vocabulary with filter": reload_vocabulary,
            "Filter words": filter_words,
            "Add words": add_new_words,
            "Daily test": daily_test,
            "Vocabulary summary": vocab_summary,
            "Tags in vocabulary": tags_in_vocabulary,
            "Test: verb conjugation Perfekt": test_verb_conjugation_Perfekt,
            "Test: verb conjugation Präteritum": test_verb_conjugation_praet,
            "Test: definite article": test_definite_article,
            "Test: noun translation": test_noun_translation,
            "Test: verb translation": test_verb_translation,
            "Test: adverb translation": test_adverb_translation,
            "Test: adjective translation": test_adjective_translation,
            "Conjugation table": conjugation_table,
            "List words for a tag": list_words_for_tag,
            }
        keys = list(browser_functions.keys())
        
        # print menu
        print(f'0 - Exit')
        for k,dtl in enumerate(browser_functions):
            print(k+1,'-',dtl)

        response = input("Choose option: ")
        if not response.isdigit() or int(response) < 0 or int(response) > len(browser_functions):
            browser_menu(vc)
        if int(response) == 0: #last item, exit selected
            os.system('clear')
            
        else:
            browser_functions[(keys[int(response)-1])](vc)
            input("Press enter to continue...")
            
            os.system('clear')
            browser_menu(vc)
    
    except Exception as e:
        print(f'Error in browser menu: {str(e)}')
        return

def main():
    try:
        vocabulary_file = "dict.yaml"
        v = Vocabulary(vocabulary_file)
        browser_menu(v)
    except Exception as e:
        print(f'Error in main: {str(e)}')
        return  

main()