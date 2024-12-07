from vocab import *

# #load main vocabulary
base_v = Vocabulary('dict.yaml')

# # #load new vocabulary to merge
# new_v = Vocabulary('new_dict.yaml')

# merge_vocabulary(new_v, base_v,overwrite=True)
# base_v.backup()
# base_v.save()


# display all tags
print(base_v.tags())
# filter words into a new vocabulary
filtered_v = base_v.clone('verb')
print(f"Filtered items: {len(filtered_v.vocab)}")
#verb conjugation using new vocabulary
my_test = LanguageTest(5,"verb conjugation",filtered_v,True)

my_test.run()

