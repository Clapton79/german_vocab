import sys
import vocab as v
from vocab_utilities import bcolors
import os
from applogger import logger


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
    w = vocabulary.filter_by_class_and_tag('noun')
    return len(next(w)) > 0
   
def test_05_vocabulary_returns_verbs() -> bool:
    vocabulary = v.Vocabulary(vocabulary_file)
    w = vocabulary.filter_by_class_and_tag('verb')
    return len(next(w)) > 0
    
def test_06_vocabulary_saves() -> bool:
    try:
        vocabulary = v.Vocabulary(vocabulary_file)
        vocabulary.save()
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
    
# def test_08_vocabulary_has_no_data_quality_issues() -> bool:
#     vocabulary = v.Vocabulary(vocabulary_file)
#     return vocabulary.check_structure()
    
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
        print(str(e))
        return False
    
#'verb conjugation', 'imperative verb form', 'noun translation', 'noun plural form', 'definite article', 'translation'
#v.vocab['sodass']['date_added']=format(datetime.now(),"%Y-%m-%d")
#pprint([(x,dtl['date_added']) for x, dtl in v.vocab.items()])
#v.save_as()

os.environ['VOCAB_LOGLEVEL']= 'DEBUG'


current_module = sys.modules[__name__]
all_attributes = dir(current_module)
callable_methods = [attr for attr in all_attributes if callable(getattr(current_module, attr)) and not attr.startswith("__") and attr != 'setup_logger' and not attr.startswith("bcolor")]

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
    
os.environ['VOCAB_LOGLEVEL']= 'ERROR'
