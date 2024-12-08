from vocab import *
from vocab_utilities import *

v = Vocabulary('dict.yaml')
print(v.tags())
vv = v.clone(tag_filter='haben')
# vv.append_tag_to_words(tag='_speakEasy_page002')
# vv.remove_tags_from_words(tag='haben')
# # print(vv.tags())

# # print(f"{vv.count()} words")
# # print (vv.words())
# # print(vv.tags())
# # vv.remove_tags_from_words(tag='')
# # print(vv.tags())
# merge_vocabulary(vv, v,overwrite=True)
# # print(v.tags())
# v.backup()
# v.save()