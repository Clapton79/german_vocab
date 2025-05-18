# browse dictionary and get info on dictionary data

from vocab import *
from vocab_utilities import bcolors
import os
from pprint import pprint
import re

def daily_test(vc:Vocabulary):

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
    else:
        test_v = base_v.clone()
        adj_v = base_v.clone(word_class_filter='adjective')
        verbs_v = base_v.clone(word_class_filter='verb')

    print(f"vocabulary rowset: {len(test_v.vocab.keys())} words")

    if number_of_questions > 0:
        # verb conjugation using new vocabulary
        my_test = LanguageTest(number_of_questions,
                            "translation", test_v, True)

        my_test.run()
        # verb conjugation using new vocabulary
        my_test = LanguageTest(number_of_questions,
                            'definite article', test_v, True)

        my_test.run()
        my_test = LanguageTest(number_of_questions,
                            "translation", adj_v, True)

        my_test.run()
        # verb conjugation using new vocabulary
        my_test = LanguageTest(number_of_questions,
                            'verb conjugation', test_v, True)
        my_test.run()
    
def vocab_summary(vc:Vocabulary):
    
    types=[y['class'] for x,y in vc.vocab.items()]
    
    for item in list(set(types)):
       print(f'{item.ljust(15," ")}: {len([x for x in types if x==item])}')
    
    print(f'{"TOTAL".ljust(15," ")}: {len(types)}')
    
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
        
def list_words_for_tag (vc:Vocabulary):
    tag = input("Type a tag: ")
    result = list(vc.filter_by_tag())
    if len(result)>0:
        print(f'Words with tag {tag}:')
        print(result)
    else:
        print(f'No words with tag {tag}')
        
def conjugator (vc:Vocabulary):
    word = input("Type a word: ")
    result = vc.__getitem__(word)
    if result is not None or result['class']!='verb':
        report={}
        pprint(result['conjugations'])
    else:
        print (f'{bcolors.FAIL}Word {word} was not found or is not a verb.{bcolors.ENDC}')
    
def browser_menu(vc:Vocabulary):

    print(f'{bcolors.OKCYAN}####################################################################{bcolors.ENDC}')
    print(f'#                   {bcolors.OKBLUE}Vocabulary Browser{bcolors.ENDC}')
    print(f'{bcolors.OKCYAN}####################################################################{bcolors.ENDC}')
    print("")
    print("")
    
    print(f'Loaded vocabulary: {vc.filename}')
    
    no_return = False
    
    browser_functions = {
        "Word finder": word_finder,
        "Conjugator": conjugator,
        "Words with tag": list_words_for_tag,
        "Daily test": daily_test,
        "Vocabulary summary": vocab_summary
        }
    keys = list(browser_functions.keys())
    for k,dtl in enumerate(browser_functions):
        print(k+1,'-',dtl)
    
    print(f'{len(browser_functions)+1} - Exit')
    
    response = int(input("Choose option: "))-1
    if response == len(keys): #last item, exit selected
        os.system('clear')
        
    else:
        browser_functions[keys[response]](vc)
        input("Press enter to continue...")
        
        os.system('clear')
        browser_menu(vc)

def main():

    vocabulary_file = "dict.yaml"
    v = Vocabulary(vocabulary_file)
    browser_menu(v)

main()