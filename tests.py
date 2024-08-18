#import vocabularizer as v
import verbs as vb

#print(f"Vocabularizer verison {v.library_version}")
print(f"Verbs version {vb.library_version}")

#v.load_all_files()
#v.get_word('putzen')
# v.load_file(f'vocabularies/German_English_202309.csv')
# v.load_file(f'vocabularies/German_English_202310.csv')
# #v.inspect_vocabulary()
# v.test_3(25)

# import verbs as vb

# vb.load_file('verbs/verbs.csv')
# print(vb.df)


#################
# verbs tests
#################

#print(vb.conjugate_verb('betreten'))
#print(vb.conjugate_verb_one_mode('betreten','Perfekt'))
vb.conjugation_table('betreten')