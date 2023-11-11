from vocabularizer import load_file, test_2, output_decorator, word_memorizer, test_1, unload_vocabulary
import os
import time

def daily_routine():
    files = os.listdir('vocabularies')
    for file in files:
        output_decorator("FILE: {0}".format(file), 2)
        load_file(f'vocabularies/{file}')
        word_memorizer(20,3,'last')
        test_2('n', 15)
        test_2('a', 15)
        test_2('v', 15)
        test_2('s', 15)
        test_2('adv', 15)

        test_1('', 15)
        unload_vocabulary()
        if file != files[-1]:
                print("10 seconds till the next round.")
                time.sleep(10)
 
daily_routine()