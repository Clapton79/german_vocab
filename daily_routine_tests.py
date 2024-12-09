from vocab import *

print(get_available_tests())

number_of_questions = int(input ('How many questions do you want? '))

base_v = Vocabulary('dict.yaml')
print(base_v.tags())
tag_filter = input('Tag filter: ')
test_v = base_v.clone(tag_filter=tag_filter)
print(f"vocabulary rowset: {len(test_v.vocab.keys())} words")
print(test_v.words())
if number_of_questions > 0:
    #verb conjugation using new vocabulary
    my_test = LanguageTest(number_of_questions,
                           "translation",test_v,True)

    my_test.run()

    # verb conjugation using new vocabulary
    my_test = LanguageTest(number_of_questions,
                           'definite article', test_v, True)

    my_test.run()
