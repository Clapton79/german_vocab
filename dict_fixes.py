from vocab import *
from pprint import pprint
import vocab_utilities as vu

test_v = Vocabulary('dict.yaml')
results = test_v.data_quality_errors()
pprint(results)
# my_test = LanguageTest(10,
#                            'verb conjugation', test_v, True)
# my_test.run()
    
# base_v = Vocabulary('dict.yaml')

# source_v = Vocabulary('new_dict.yaml')

# merge_vocabulary(source_v,base_v,overwrite=True)
# base_v.backup()
# base_v.save()
# print([x for x in base_v.tags() if x.startswith('_speak')])
