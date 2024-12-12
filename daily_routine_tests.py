from vocab import *

print(get_available_tests())

number_of_questions = input ('How many questions do you want? (10)')

if number_of_questions == '':
    number_of_questions = 10
else:
    number_of_questions = int(number_of_questions)
    

base_v = Vocabulary('dict.yaml')

print(base_v.tags())
tag_filter = input('Tag filter: ')
if len(tag_filter)>0:
    test_v = base_v.clone(tag_filter=tag_filter)
    adj_v = base_v.clone(word_class_filter='adjective', tag_filter=tag_filter)
    verbs_v = base_v.clone(word_class_filter='verb', tag_filter=tag_filter)
else:
    test_v = base_v.clone()
    adj_v = base_v.clone(word_class_filter='adjective')
    verbs_v = base_v.clone(word_class_filter='verb')


    
print(f"vocabulary rowset: {len(test_v.vocab.keys())} words")

if number_of_questions > 0:
    #verb conjugation using new vocabulary
    my_test = LanguageTest(number_of_questions,
                           "translation",test_v,True)

    my_test.run()
    # verb conjugation using new vocabulary
    my_test = LanguageTest(number_of_questions,
                           'definite article', test_v, True)

    my_test.run()
    my_test = LanguageTest(number_of_questions,
                           "translation",adj_v,True)

    my_test.run()
    # verb conjugation using new vocabulary
    my_test = LanguageTest(number_of_questions,
                           'verb conjugation', test_v, True)
    my_test.run()
