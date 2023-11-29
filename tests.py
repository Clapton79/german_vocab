import vocabularizer as v

v.get_version()
v.load_file(f'vocabularies/German_English_202311.csv')
v.load_file(f'vocabularies/German_English_202309.csv')
v.load_file(f'vocabularies/German_English_202310.csv')
#v.inspect_vocabulary()
v.test_3(25)