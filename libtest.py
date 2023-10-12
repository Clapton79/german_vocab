import vocabularizer as v
import os

files = os.listdir('vocabularies')
for file in files:
    v.output_decorator("FILE: {0}".format(file), 2)
    v.load_file(f'vocabularies/{file}')
    v.test_2('n', 5)
    v.test_2('a', 5)
    v.test_2('v', 5)
    v.test_2('s', 5)

    v.unload_vocabulary()

    