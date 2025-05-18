from vocab import *
import os
v = Vocabulary('new_dict.yaml')
vv = Vocabulary('dict.yaml')

vv.backup()

merge_vocabulary(v,vv,overwrite=True)
vv.save(overwrite=True)
os.remove('new_dict.yaml')