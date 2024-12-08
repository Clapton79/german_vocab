# this file helps explore the contents of the main vocabulary.
from vocab import *
from vocab_utilities import bcolors

# load the main vocabulary
v = Vocabulary('dict.yaml')
errors = v.data_quality_errors()
pprint(errors)

# v_err = v.clone(words_filter=list(errors.keys()))

# for word in v_err.vocab.keys():
#     wrd = Word(v.vocab[word]['class'])
#     wrd.update_from_dict({word: v_err.vocab[word]})
#     if wrd.word_class == 'verb':
#         wrd.get_conjugations()
#     if wrd.word_class == 'noun':
#         wrd.get_definite_article()
    
#     print(wrd.convert_to_dict())
    
    
# merge_vocabulary(v_err,v,overwrite=True)
# v.backup()
# v.save()
        