from vocab import *
import os

os.environ['VOCAB_LOG_LEVEL'] = "DEBUG"
os.environ['VOCAB_LOG_TO_SCREEN'] = "True"
vv = Vocabulary('dict.yaml')
print(len(vv.filter(word_class='verb', tag='_Csilla')))
print(len(vv.filter(word='bekommen')))
print(len(vv.filter(word='trennen', tag='sich')))
print(len(vv.filter(word='trennen', tag='sich', word_class='verb')))