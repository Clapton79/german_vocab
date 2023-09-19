import vocabularizer as v
import os

def daily_routine():
    files = os.listdir('vocabularies')
    for file in files:
        v.output_decorator("FILE: {0}".format(file), 2)
        v.load_file(f'vocabularies/{file}')
        v.word_memorizer(20)
        v.test_2(15)
        v.test_1(10)
        v.unload_vocabulary()

daily_routine()