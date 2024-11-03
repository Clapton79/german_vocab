from scrape import *

verb = input('Type the verb: ')
conjugation = webquery_conjugation(verb)
for row in conjugation:
    print(row)