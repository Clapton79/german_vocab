from vocab import *

cnt = input('How many words would you like to register?:')

try:
    cnt = int(cnt)
except:
    print("Invalid input. Please enter a number.")
    exit(1)


v = Vocabulary()

for i in range(cnt):
    word_class = input("Input word class: ")
    if word_class not in ['verb','noun','adjective','adverb','conjunction','phrase','preposition']:
       print ("Invalid word class")
       break

    w = Word(word_class)
    w.update()
    v.add(w)
    
print(v.check_structure())

savefile = input('Name the dictionary file:')
v.save(savefile)
    
