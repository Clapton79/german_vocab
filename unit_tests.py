import sys
import vocab as v
from vfunctions import bcolors
import os
from applogger import logger

os.environ['VOCAB_LOGLEVEL']= 'DEBUG'

#################################################################
# Variables needed to run the unit tests
#################################################################
vocabulary_file = "new_dict.yaml"
#################################################################
# Tests
#################################################################
def available_tests_display() -> bool:
    try:
        output = v.get_available_tests()
        if len(output) == 0:
            raise ValueError
        return True
    except:
        return False
    
def vocabulary_loads() -> bool:
    vocabulary = v.Vocabulary(vocabulary_file)
    return vocabulary.load_success
    
def a_word_can_be_added_to_vocabulary() -> bool:
    try:
        vocabulary = v.Vocabulary(vocabulary_file)
        w = v.Word('noun')
        vocabulary.add(w)
        return True
    except: 
        return False

def vocabulary_returns_nouns() -> bool:
    vocabulary = v.Vocabulary(vocabulary_file)
    w = vocabulary.filter_by_class_and_tag('noun')
    return len(next(w)) > 0
   
def vocabulary_returns_verbs() -> bool:
    vocabulary = v.Vocabulary(vocabulary_file)
    w = vocabulary.filter_by_class_and_tag('verb')
    return len(next(w)) > 0
    
def vocabulary_saves() -> bool:
    try:
        vocabulary = v.Vocabulary(vocabulary_file)
        vocabulary.save()
        return True
    except: 
        return False
        
def vocabular_backs_up() -> bool:
    try:
        vocabulary = v.Vocabulary(vocabulary_file)
        vocabulary.backup()
        backup_file = vocabulary.last_backupfile
        if backup_file is None:
            return False
        else:
            os.remove(backup_file)
            return True
    except:
        return False
    
# words = ['Hause','Gegend']
# tags = ['land']
# v.append_tags_to_words(words,tags)
# # v.save()
 
#print(list(v.filter_by_class_and_tag('noun','land')))
# print(list(v.filter_by_class_and_tag('noun')))
#print(list(v.filter_by_topic_and_class('noun','building')))

#pprint([(x,dtl['date_added']) for x, dtl in v.vocab.items()])
#@@@@@@@@@@@ Test tester

def language_test_loads():
    vc = v.Vocabulary(vocabulary_file)
    t = v.LanguageTest(2,"imperative verb form",vc)
    return t.test_load_success
    

#'verb conjugation', 'imperative verb form', 'noun translation', 'noun plural form', 'definite article', 'translation'
#v.vocab['sodass']['date_added']=format(datetime.now(),"%Y-%m-%d")
#pprint([(x,dtl['date_added']) for x, dtl in v.vocab.items()])
#v.save_as()

current_module = sys.modules[__name__]
all_attributes = dir(current_module)
callable_methods = [attr for attr in all_attributes if callable(getattr(current_module, attr)) and not attr.startswith("__") and attr != 'setup_logger' and not attr.startswith("bcolor")]

print ("####################################################################")
print ("#                   Library Unit Tests")
print ("####################################################################")

# Dynamically call each method
for method_name in callable_methods:
    logger.info(f"Running unit test: {method_name}")  # Log the test name to the logger
    method = getattr(current_module, method_name)
    test_result = method()  # Call the method
    bcolor = bcolors.OKGREEN if test_result else bcolors.FAIL
    print(f"Method: {method_name.ljust(36, ' ')} Result: {bcolor}{test_result}{bcolors.ENDC}")
    
os.environ['VOCAB_LOGLEVEL']= 'ERROR'
