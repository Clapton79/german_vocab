# browse dictionary and get info on dictionary data

from vocab import Vocabulary
from vocab_utilities import bcolors
import os
from pprint import pprint

def word_finder(vc:Vocabulary):
    word = input("Type a word: ")
    result = vc.__getitem__(word)
    pprint(result)
    
def conjugator (vc:Vocabulary):
    word = input("Type a word: ")
    result = vc.__getitem__(word)
    if result is not None:
        pprint(result['conjugations'])
    else:
        print (f'{bcolors.FAIL}Word {word} was not found.{bcolors.ENDC}')
    
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
        "Conjugator": conjugator
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