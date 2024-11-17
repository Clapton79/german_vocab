from vocab import *

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
v = Vocabulary('vocab.yaml')
word_classes = ['verb','noun','adjective','adverb','conjunction','phrase','preposition']

for i in range(cnt):
    
    word_class = input("Select word class: " + str([': '.join ([str(i+1),x]) for i,x in enumerate(word_classes)]))
    word_class = int(word_class)-1
    w = Word(word_classes[word_class])
    w.update()
    w.get_definite_article()
    v.add(w)
   

# merge vocabulary in to the standard one
vs = Vocabulary('dict.yaml')
vs.backup()
merge_vocabulary(v, vs)
vs.save()
 
