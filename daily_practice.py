import vocabularizer as v
import os

def daily_routine():
    files = os.listdir('vocabularies')
    for file in files:
        v.output_decorator("FILE: {0}".format(file), 2)
        v.load_file(f'vocabularies/{file}')
        v.word_memorizer(3)
        v.test_2(3)
        v.test_1(5)
        v.unload_vocabulary()

daily_routine()