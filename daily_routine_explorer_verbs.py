# this file helps explore the contents of the main vocabulary.
from pprint import pprint
from vocab import *
from vocab_utilities import bcolors

pagefilter = "_speakEasy_page002"
# load the main vocabulary  
v = Vocabulary('dict.yaml')
print('Verbs in vocabulary:')
print([x for x in v.filter_by_class_and_tag(word_class = 'verb', tag=pagefilter)])

answer = input("Enter a verb: ")

if answer in v.vocab.keys():
    print(f"{answer} - {v.vocab[answer]['translations']['hungarian']}")
    if v.vocab[answer]['class'] == 'verb':
        print("Conjugations:")
        for key in v.vocab[answer]['conjugations']:
            print(f"\t{key}")
            for c in v.vocab[answer]['conjugations'][key]:
                print(f"\t\t{c}")
        print("")
        print(f"Imperative: {str(v.vocab[answer]['imperative']).title()}!")
else:
    print(f"{bcolors.FAIL}{answer} is not in the vocabulary.{bcolors.ENDC}")