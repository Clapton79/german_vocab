# from fileoperations import *
from  pprint import pprint
# my_vocab = load_file ('new_dict.yaml')

# #print(my_vocab.keys())
# my_vocab = my_vocab['words']
# my_verb = my_vocab['erzählen']
# pprint(my_verb.keys())
# #write_vocab_file ('my_second_dict.yaml', my_vocab)
# #backup_file('new_dict.yaml')

#from charting import *

#example
# scatter_plot([("2-jun",3),("3-jun",2.25),("4-jun",3.56)],'My stats',"number of tests")

from vocab import *
###########################
# List of available tests:
###########################
print(get_available_tests())


v = Vocabulary('new_dict.yaml')

t = Test(1,"verb conjugation",v)

t.run()
t.show_results()