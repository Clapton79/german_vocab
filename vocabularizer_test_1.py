import vocabularizer as v

def daily_routine():
    v.load_file('vocabularies/German_English_A11Chapter1.csv')
    v.word_memorizer(15)
    v.test_2(30)
    v.test_1(15)

daily_routine()
