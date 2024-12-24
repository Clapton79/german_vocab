from vocab import *

v = Vocabulary('new_dict.yaml')
vv = Vocabulary('dict.yaml')

vv.backup()

merge_vocabulary(v,vv,overwrite=True)
vv.save()
