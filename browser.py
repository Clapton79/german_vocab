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
            test_v = base_v.clone(tag_filter=tag_filter)
            adj_v = base_v.clone(word_class_filter='adjective', tag_filter=tag_filter)
            verbs_v = base_v.clone(word_class_filter='verb', tag_filter=tag_filter)
            nouns_v = base_v.clone(word_class_filter='noun', tag_filter=tag_filter)
        else:
            test_v = base_v.clone()
            adj_v = base_v.clone(word_class_filter='adjective')
            verbs_v = base_v.clone(word_class_filter='verb')
            nouns_v = base_v.clone(word_class_filter='noun')


        if number_of_questions > 0:
            # verb conjugation using new vocabulary
            try:
                if test_v is not None and len(test_v.vocab.keys()) > 0:
                    print(f"vocabulary rowset: {len(test_v.vocab.keys())} words")
                    my_test = LanguageTest(number_of_questions,
                                        "translation", test_v, True)
                    my_test.run()
                else:
                    print(f'{bcolors.FAIL}No words found in vocabulary for translation test.{bcolors.ENDC}')
            except Exception as e:
                print(f'Error creating translation test: {str(e)}')
                return

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

            try:
                if adj_v is not None and len(adj_v.vocab.keys()) > 0:
                    print(f'Dictionary elements: {len(adj_v.vocab.keys())}')
                    my_test = LanguageTest(number_of_questions,
                                    "translation", adj_v, True)
                    my_test.run()
                else:
                    print(f'{bcolors.FAIL}No adjectives found in vocabulary for translation test.{bcolors.ENDC}')
            except Exception as e:
                print(f'Error creating translation test: {str(e)}')
            
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
        rx = input("Type a regex: ")
        pattern = re.compile(rx)
        result=[x for x in vc.vocab.keys() if pattern.match(x)] # search in words
        result2=[x for x in vc.vocab.keys() if pattern.match(json.dumps(vc.vocab[x]))]
        result +=result2
        #result_c = [x for x,detail in vc.vocab.items() if pattern.match(json.dumps(detail))] # search in conjugation
        if len(result)>0:
            report=([f'({vc[x]["class"][0]}){x.ljust(25," ")} {", ".join(vc[x]["translations"]["hungarian"])}' for x in result])
            for item in report: 
                print(item)
        else:
            print(f'{bcolors.FAIL}No word matched pattern {rx}{bcolors.ENDC}')

    except Exception as e: 
        print(f'Search error({str(e)}')
  
def add_new_words(vc:Vocabulary):
    try:
        add_words(vc)
    except Exception as e:
        print(f'Error during adding new words: {str(e)}')
        return

def list_words_for_tag (vc:Vocabulary):
    try:
        tag = input("Type a tag: ")
        result = list(vc.filter_by_tag(tag))
        if len(result)>0:
            print(f'Number of words with tag {tag}: {len(result)}')
            print(result)
        else:
            print(f'No words with tag {tag}')
    except Exception as e:
        print(f'Error during tag search: {str(e)}')
def list_words_for_tag_and_class(vc:Vocabulary):
    try:
        tag = input("Type a tag: ")
        word_class = input("Type a word class: ")
        result =  list(vc.filter_by_class_and_tag(word_class, tag))
        if len(result)==0:
            print(f'No {word_class}s with tag {tag}')
            
        else:
            print(f'Number of {word_class}s with tag {tag}: {len(result)}')
            print(result)
    except Exception as e:
        print(f'Error during tag and class search: {str(e)}')

def conjugator (vc:Vocabulary):
    try:
        word = input("Type a word: ")
        result = vc.__getitem__(word)
        if result is not None or result['class']!='verb':
            report={}
            pprint(result['conjugations'])
        else:
            print (f'{bcolors.FAIL}Word {word} was not found or is not a verb.{bcolors.ENDC}')

    except Exception as e:
        print(f'Conjugation error: {str(e)}')
    
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

def test_verb_conjugation(vc:Vocabulary):
    try: 
        number_of_questions = input('How many questions do you want?')
        if not number_of_questions.isdigit():
            raise ValueError(f'{bcolors.FAIL}Invalid input. Please enter a number.{bcolors.ENDC}')

        number_of_questions = int(number_of_questions)
        tag_filter = input('Tag filter: ')
        if len(tag_filter) == 0:
            raise ValueError("Tag filter cannot be empty.")
       
        va = vc.clone(word_class_filter='verb')
        if va is not None and len(va.vocab.keys()) > 0:
            print(f"vocabulary rowset: {len(va.vocab.keys())} words")
            my_test = LanguageTest(number_of_questions,
                                'verb conjugation', va, True)
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
            raise ValueError("Tag filter cannot be empty.")
       
        va = vc.clone(word_class_filter='noun')
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
def test_noun_translation(vc:Vocabulary):
    try: 
        number_of_questions = input('How many questions do you want?')
        if not number_of_questions.isdigit():
            raise ValueError(f'{bcolors.FAIL}Invalid input. Please enter a number.{bcolors.ENDC}')

        number_of_questions = int(number_of_questions)
        tag_filter = input('Tag filter: ')
        if len(tag_filter) == 0:
            raise ValueError("Tag filter cannot be empty.")
       
        va = vc.clone(word_class_filter='noun')
        if va is None or len(va.vocab.keys()) == 0:
            raise IndexError(f'{bcolors.FAIL}No nouns found in vocabulary for noun translation test.{bcolors.ENDC}')
        if va is not None and len(va.vocab.keys()) > 0:
            print(f"vocabulary rowset: {len(va.vocab.keys())} words")
            my_test = LanguageTest(number_of_questions,
                                'noun translation', va, True)
            my_test.run()
        else:
            raise IndexError(f'{bcolors.FAIL}No nouns found in vocabulary for noun translation test.{bcolors.ENDC}')

    except Exception as e:
        print(f'Error in noun translation test: {str(e)}')
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
            "Conjugator": conjugator,
            "Words with tag": list_words_for_tag,
            "Words with tag of class": list_words_for_tag_and_class,
            "Add words": add_new_words,
            "Daily test": daily_test,
            "Vocabulary summary": vocab_summary,
            "Tags in vocabulary": tags_in_vocabulary,
            "Test: verb conjugation": test_verb_conjugation,
            "Test: definite article": test_definite_article,
            "Test: noun translation": test_noun_translation
            }
        keys = list(browser_functions.keys())
        
        # print menu
        print(f'0 - Exit')
        for k,dtl in enumerate(browser_functions):
            print(k+1,'-',dtl)
        
        response = int(input("Choose option: "))
        if response == 0: #last item, exit selected
            os.system('clear')
            
        else:
            browser_functions[(keys[response-1])](vc)
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