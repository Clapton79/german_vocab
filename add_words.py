from vocab import *
from os import environ
from pprint import pprint

title = '* Word adding *'
debug = True
print('#' * 86)
print('#', ' ' * 15, title, ' ' * (80-15-len(title)), '#')
print('#' * 86)

environ['VOCAB_LOGLEVEL'] = 'ERROR'
environ['VOCAB_LOG_TO_SCREEN']='True'


def is_numeric(variable):
    try:
        var=int(variable)
        return True
    except:
        return False
    


vv = Vocabulary('dict.yaml')    # open the main vocabulary file
print(f"Used main tags: {[x for x in vv.tags() if x.startswith('_')]}")

cnt = input('How many words would you like to register? (1):')
if not is_numeric(cnt):
    print("Invalid input. Please enter a number.")
    exit(1)

cnt = 1 if cnt == '' else cnt 
if cnt == 0:
    exit(0)
words_added_to_vocabulary = 0


try:
    cnt = int(cnt)
except:
    print("Invalid input. Please enter a number.")
    exit(1)

default_tags = input('Default tags to add to the words: (comma separated list)')
if default_tags and isinstance(default_tags, list):
    default_tags = default_tags.split(',')
if default_tags and isinstance(default_tags, str):
    default_tags = [default_tags]

v = Vocabulary()  # create a new vocabulary
word_classes = ['verb','noun','adjective','adverb','conjunction','phrase','preposition']

for i in range(cnt):
    
    word_class_selection = input("Select word class: " + str([': '.join ([str(i+1),x]) for i,x in enumerate(word_classes)]))
    if word_class_selection is None or word_class_selection == '':
        word_class_selection = 1

    if word_class_selection == 0:
        print("Skipping word.")
        continue
    
    if word_class_selection not in [str(i+1) for i in range(len(word_classes))]:
        print("Invalid selection. Please select a valid word class.")
        continue

    word_class = word_classes[int(word_class_selection)-1]
    
    w = Word(word_class)
    w.update()
    if word_class == 'noun':
        w.get_definite_article()
    elif word_class == 'verb':
        w.get_conjugations()
    
    if len(default_tags)>0:
        w.word_data['tags'] = w.word_data['tags'] + default_tags
            
    print(f"Word {w.word_text} \n Details:")
    pprint(w.convert_to_dict())
    
    do_save = input("Do you want to save it? (Enter/n): ")
    do_save = True if len(do_save) == 0 else False
    if do_save:
        
        v.add(w,overwrite=True)
        words_added_to_vocabulary += 1
    
    # always save the vocabulary before moving to the next word
    v.save('new_dict.yaml', overwrite=True)
    
# open the main vocabulary file
# merge the vocabulary into the main vocabulary file
merge_vocabulary(v,vv,overwrite=True)

# back up the vocabulary file before saving
vv.backup()
vv.save(overwrite=True)


print(f"{words_added_to_vocabulary} new words have been added to the cache vocabulary and merged to the main one.")
print(f"Number of words in main dict: {len(vv.vocab.keys())}")
