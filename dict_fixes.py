from vocab import *
from pprint import pprint
import vocab_utilities as vu

vv = Vocabulary('new_dict.yaml')

new=load_file('new_dict.json','json')
for k,v in new.items():
    print(f'importing {k}')
    print(f"class: {v.get('class')}")
    word = Word(v.get('class'))
    word.update_from_dict({k:new[k]})
    vv.add(word)
    
vv.save(overwrite=True)    
# my_test = LanguageTest(10,
#                            'verb conjugation', test_v, True)
# my_test.run()
    
# base_v = Vocabulary('dict.yaml')

# source_v = Vocabulary('new_dict.yaml')

# merge_vocabulary(source_v,base_v,overwrite=True)
# base_v.backup()
# base_v.save()
# print([x for x in base_v.tags() if x.startswith('_speak')])
