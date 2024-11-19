from vocab import *
from os import environ

environ['VOCAB_LOGLEVEL'] = 'DEBUG'

cnt = input('How many words would you like to register?: ')
cnt = 1 if cnt == '' else cnt 
    
try:
    cnt = int(cnt)
except:
    print("Invalid input. Please enter a number.")
    exit(1)

if cnt == 0:
    exit(0)
#create a new vocabulary
v = Vocabulary('dict.yaml')
word_classes = ['verb','noun','adjective','adverb','conjunction','phrase','preposition']

for i in range(cnt):
    
    word_class_selection = input("Select word class: " + str([': '.join ([str(i+1),x]) for i,x in enumerate(word_classes)]))
    word_class = word_classes[int(word_class_selection)-1]
    w = Word(word_class)
    w.update()
    if word_class == 'noun':
        w.get_definite_article()
    elif word_class == 'verb':
        w.get_conjugations()
    
    print(w.convert_to_dict())
    v.add(w,overwrite=True)
   


