from vocab import *

print(get_available_tests())

number_of_questions = int(input ('How many questions do you want? '))
tag_filter = input('Tag filter: ')
if number_of_questions > 0:
    base_v = Vocabulary('dict.yaml')
    test_v = base_v.clone(tag_filter=tag_filter)

    #verb conjugation using new vocabulary
    my_test = LanguageTest(number_of_questions,"translation",test_v,True)

    my_test.run()

