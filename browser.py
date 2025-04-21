# browse dictionary and get info on dictionary data

from vocab import Vocabulary
from vocab_utilities import bcolors
import os
from pprint import pprint
import re

def vocab_summary(vc:Vocabulary):
    
    types=[y['class'] for x,y in vc.vocab.items()]
    
    for item in list(set(types)):
       print(f'{item.ljust(15," ")}: {len([x for x in types if x==item])}')
    
    print(f'{"TOTAL".ljust(15," ")}: {len(types)}')
    
def word_finder(vc:Vocabulary):
    rx = input("Type a regex: ")
    pattern = re.compile(rx)
    result=[x for x in vc.vocab.keys() if pattern.match(x)]
    if len(result)>0:
        report=([f'({vc[x]["class"][0]}){x.ljust(25," ")} {vc[x]["translations"]["hungarian"]}' for x in result])
        for item in report: 
            print(item)
    else:
        print(f'{bcolors.FAIL}No word matched pattern {rx}{bcolors.ENDC}')

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