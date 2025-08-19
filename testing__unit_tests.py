import sys
import vocab as v
from vocab_utilities import bcolors, get_conjugation, get_definite_article
import os
from applogger import setup_logger
from weights import *

#################################################################
# Variables needed to run the unit tests
#################################################################
vocabulary_file = "dict.yaml"
#################################################################
# Tests
#################################################################
def test_01_available_tests_display() -> bool:
    try:
        output = v.get_available_tests()
        if len(output) == 0:
            raise ValueError
        return True
    except:
        return False
    
def test_02_vocabulary_loads() -> bool:
    vocabulary = v.Vocabulary(vocabulary_file)
    return vocabulary.load_success
    
def test_03_a_word_can_be_added_to_vocabulary() -> bool:
    try:
        vocabulary = v.Vocabulary(vocabulary_file)
        w = v.Word('noun')
        vocabulary.add(w)
        return True
    except: 
        return False

def test_04_vocabulary_returns_nouns() -> bool:
    vocabulary = v.Vocabulary(vocabulary_file)
    w = vocabulary.filter_by_class('noun')
    return len(w) > 0
   
def test_05_vocabulary_returns_verbs() -> bool:
    vocabulary = v.Vocabulary(vocabulary_file)
    w = vocabulary.filter_by_class('verb')
    return len(w) > 0

def test_06_vocabulary_saves() -> bool:
    try:
        vocabulary = v.Vocabulary(vocabulary_file)
        vocabulary.save(overwrite=True)
        return True
    except: 
        return False
        
def test_07_vocabular_backs_up() -> bool:
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
    
def test_09_vocabulary_returns_all_tags() -> bool:
    vocabulary = v.Vocabulary(vocabulary_file)
    tags = vocabulary.tags()
    return len(tags) > 0

def test_10_language_test_loads():
    vc = v.Vocabulary(vocabulary_file)
    t = v.LanguageTest(2,"imperative verb form",vc)
    return t.test_load_success
    
def test_11_two_vocabularies_can_be_merged():
    try:
        vc = v.Vocabulary(vocabulary_file)
        vc_word_count = len(vc.vocab.keys())
        ve = v.Vocabulary('new_words.yaml')
        ve_word_count = len(ve.vocab.keys())
        v.merge_vocabulary(vc, ve)
        return True 
    except: 
        return False
        
def test_12_vocabulary_word_can_be_updated():
    try:
        vc = v.Vocabulary(vocabulary_file)
        #get a verb
        verbs = list(vc.filter_by_class_and_tag('verb'))
        verb = verbs[0]
        w = vc.vocab[verb]
        ww = v.Word('verb')
        ww.update_from_dict({verb : w})
        ww.word_data['tags']= ['tag1','tag2']
        vc.add(ww,overwrite=True)
        return True
    except Exception as e:
        return False
    
def test_13_webquery_returns_definite_article():
    try:
        word = 'Auto'
        definite_article = get_definite_article(word)
        if definite_article == 'das':
            return True
        else:
            return False
    except Exception as e:
        return False

def test_14_webquery_returns_conjugations():
    try:
        word = 'erzählen'
        conjugations = get_conjugation(word)
        if len(conjugations) > 0:
            return True
        else:
            return False
    except Exception as e:
        return False

def test_15_create_weights():
    try:
        v = Vocabulary('dict.yaml')
        wt = Weight()
        wt.create_schema_for_words(v.words())
        wt.save('test_weights.yaml', overwrite=True)
        return True
    except:
        return False
    
    
os.environ['VOCAB_LOGLEVEL']= 'ERROR'
os.environ['VOCAB_LOG_TO_SCREEN'] = "False"
logger=setup_logger()

current_module = sys.modules[__name__]
all_attributes = dir(current_module)
callable_methods = [attr for attr in all_attributes if callable(getattr(current_module, attr)) and attr.startswith('test')]

print ("####################################################################")
print ("#                   Library Unit Tests")
print ("####################################################################")
print ("")
print (f"Vocabulary file: {vocabulary_file}")
print ("")
print ("")
# Dynamically call each method
for method_name in callable_methods:
    logger.info(f"Running unit test: {method_name.replace('_',' ').capitalize()}")  # Log the test name to the logger
    method = getattr(current_module, method_name)
    try:
        test_result = method()  # Call the method
    except: 
        test_result = False
        
    bcolor,message = (bcolors.OKGREEN,'Pass') if test_result else (bcolors.FAIL,'Failed')
    print(f"{method_name.replace('_',' ').capitalize().ljust(46, ' ')} Result: {bcolor}{message}{bcolors.ENDC}")
