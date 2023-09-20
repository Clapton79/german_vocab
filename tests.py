import vocabularizer as v

v.get_version()
v.load_file(f'vocabularies/German_English_A11Chapter1.csv')
v.test_1('a',5)


v.unload_vocabulary()