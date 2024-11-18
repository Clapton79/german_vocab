import vocab as v
import os
import applogger 

vocabulary_file = "dict.yaml"
os.environ['VOCAB_LOG_TO_SCREEN']="True"
vc = v.Vocabulary(vocabulary_file)
vc.check_structure()