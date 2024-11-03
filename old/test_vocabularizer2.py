from vocabularizer2 import *
import pprint


my_vocab = load_file('data/vocabularies/German_Hungarian_A2.2_13.csv')
pprint.pprint(my_vocab)

my_verbs = load_file('data/verbs.csv')
pprint.pprint(my_verbs)