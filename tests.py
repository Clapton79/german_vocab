
from vocab import *
from pprint import pprint
from datetime import datetime

#print(get_available_tests())

v = Vocabulary('new_dict.yaml')

pprint(v['sodass'])

for k in v.items():
    print(k, v[k]['class'])
   

#pprint([(x,dtl['date_added']) for x, dtl in v.vocab.items()])
# #@@@@@@@@@@@ Test tester
# t = LanguageTest(2,"verb conjugation",v)
# t.run()
# t.show_results()
#'verb conjugation', 'imperative verb form', 'noun translation', 'noun plural form', 'definite article', 'translation'
#v.vocab['sodass']['date_added']=format(datetime.now(),"%Y-%m-%d")
#pprint([(x,dtl['date_added']) for x, dtl in v.vocab.items()])
#v.save_as()
