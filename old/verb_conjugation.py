from scrape import *

verb = input('Type the verb: ')
conjugation = get_conjugation(verb)
for row in conjugation:
    print(row)