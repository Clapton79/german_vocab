import vocabularizer as v
import os
import time
from tests import *

test_4(5)
test_5(10)

files = [x for x in os.listdir('data/vocabularies') if 'Hun' in x]

for file in files :
    output_decorator("FILE: {0}".format(file), 2)
    v.load_file(f'data/vocabularies/{file}')
    
    test_2('n', 15)
    test_2('a', 15)
    test_2('v', 15)
    test_2('s', 15)
    test_2('adv', 15)

    test_3(25)
    test_1('', 15)
    v.unload_vocabulary()
    if file != files[-1]:
            print("10 seconds till the next round.")
            time.sleep(10)
    

