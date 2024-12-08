from vocab import *

print(get_available_tests())

base_v = Vocabulary('dict.yaml')
test_v = base_v.clone(tag_filter="_speakEasy_page002")

#verb conjugation using new vocabulary
my_test = LanguageTest(5,"translation",test_v,True)

my_test.run()

