from vocab import *

for i in range(10):
    word_class = input("Input word class: ")
    if word_class not in ['verb','noun','adjective','adverb','conjunction','phrase']:
        raise ValueError ("Invalid word class")

    w = Word(word_class)
    w.update()