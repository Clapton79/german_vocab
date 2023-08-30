import vocabularizer as v

v.load_file('vocabularies/German_English_basic.csv')
print(v.df)
v.test_1()
print(v.df)