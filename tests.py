import sys
import vocab as v
from vfunctions import bcolors



#################################################################
# Tests
#################################################################

def test_get_available_tests():
    try:
        output = v.get_available_tests()
        if len(output) == 0:
            raise ValueError
        return True
    except:
        return False
    

# v = Vocabulary('new_dict.yaml')


# # w = Word('noun')
# # w.update()
# # pprint(w.items())
# # v.add(w)

# # v.save()
# # v.backup()
# #print(list(v.filter_by_class('noun')))
# # w = v.filter_by_class_and_tag('noun')
# words = ['Hause','Gegend']
# tags = ['land']
# v.append_tags_to_words(words,tags)
# # v.save()
 
#print(list(v.filter_by_class_and_tag('noun','land')))
# print(list(v.filter_by_class_and_tag('noun')))
#print(list(v.filter_by_topic_and_class('noun','building')))

#pprint([(x,dtl['date_added']) for x, dtl in v.vocab.items()])
#@@@@@@@@@@@ Test tester

def test_languagetest_class():
    vc = v.Vocabulary('new_dict.yaml')
    t = v.LanguageTest(2,"imperative verb form",vc)
    return t.test_load_success
    

#'verb conjugation', 'imperative verb form', 'noun translation', 'noun plural form', 'definite article', 'translation'
#v.vocab['sodass']['date_added']=format(datetime.now(),"%Y-%m-%d")
#pprint([(x,dtl['date_added']) for x, dtl in v.vocab.items()])
#v.save_as()

current_module = sys.modules[__name__]
all_attributes = dir(current_module)
callable_methods = [attr for attr in all_attributes if callable(getattr(current_module, attr)) and not attr.startswith("__") and not attr.startswith("bcolor")]

print ("####################################################################")
print ("#                   Library Unit Tests")
print ("####################################################################")

# Dynamically call each method
for method_name in callable_methods:
    method = getattr(current_module, method_name)
    test_result = method()  # Call the method
    bcolor = bcolors.OKGREEN if test_result else bcolors.FAIL
    print(f"Method: {method_name.ljust(36, ' ')} Result: {bcolor}{test_result}{bcolors.ENDC}")