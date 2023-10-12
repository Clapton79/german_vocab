import vocabularizer as v
import os

def daily_routine():
    files = os.listdir('vocabularies')
    for file in files:
        v.output_decorator("FILE: {0}".format(file), 2)
        v.load_file(f'vocabularies/{file}')
        v.word_memorizer(20,3,'last')
        v.test_2('n', 15)
        v.test_2('a', 15)
        v.test_2('v', 15)
        v.test_2('s', 15)

        v.test_1('', 15)
        # v.test_1('a', 15)
        # v.test_1('v', 15)
        # v.test_1('s', 15)
        v.unload_vocabulary()
        if file != files[-1]:
                print("5 seconds till the next round.")
                time.sleep(5)
        

daily_routine()