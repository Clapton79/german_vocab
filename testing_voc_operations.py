from vocab import *
from vocab_utilities import *
import os

v = Vocabulary('dict.yaml')
# print(v.tags())
vv = v.clone(words_filter=["hässlich","hübsch","vollschlank","Bauch","seltsam","traurig","frölich","Kravatte","Schlips","Fliege","schließlich","eigen","gemeinsam","berühmten","ähnlich","Einkaufstasche","Tüte"])
print(vv.words())
# cwd = os.getcwd()
# files = os.listdir(cwd)
# files = [x for x in files if x.endswith('.bak')]
# print(files)
# zip_files(files,'backups.zip')
vv.append_tag_to_words(tag='_speakEasy_page003')
# vv.remove_tags_from_words(tag='haben')
# # print(vv.tags())

# # print(f"{vv.count()} words")
# # print (vv.words())
# # print(vv.tags())
# # vv.remove_tags_from_words(tag='')
# # print(vv.tags())
merge_vocabulary(vv, v,overwrite=True)
# # print(v.tags())
v.backup()
v.save()