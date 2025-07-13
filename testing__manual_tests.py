from vocab import *
import os

os.environ['VOCAB_LOG_LEVEL'] = "DEBUG"
os.environ['VOCAB_LOG_TO_SCREEN'] = "True"
vv = Vocabulary('dict.yaml')

#data_selector_noun_translation(3, vv)
number_of_questions=3
if vv is not None and len(vv.vocab.keys()) > 0:
    print(f'Dictionary elements: {len(vv.vocab.keys())}')
    my_test = LanguageTest(number_of_questions,
                        'verb conjugation', vv, True)
    my_test.run()
else:
    print(f'{bcolors.FAIL}No verbs found in vocabulary for conjugation test.{bcolors.ENDC}')

 