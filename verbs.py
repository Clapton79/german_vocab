import csv 
import random

verbs={}
verbsfile="verbs/verbs.csv"
verbsfile_loaded = False

def load_file(**kwargs):
    global verbsfile_loaded
    global verbsfile
    global verbs
    try:
        force=bool(kwargs['force'])
    except KeyError:
        force=False
    except ValueError:
        force=False
    if verbsfile_loaded and not force:
        return verbs

    with open(verbsfile,'r') as reader:
        for line in csv.DictReader(reader):
            if line['verb'] not in verbs.keys():
                verbs[line['verb']] = {}
            try:
                tags = verbs[line['verb']]['tags']
            except KeyError:
                tags = []

            verbs[line['verb']]['tags'] = list(set([x for x in tags+line['tags'].split(';') if x !='']))
            
            try:
                conjugation = verbs[line['verb']]['conjugation']
            except KeyError:
                verbs[line['verb']]['conjugation'] = {}

            verbs[line['verb']]['conjugation'][line['tense']]=line['conjugation'].split(';')

    verbsfile_loaded = True
    return verbs

def conjugate(verb):
    v = load_file()
    conj = v[verb]['conjugation']
    return conj

def test_1(iterations,immediate_feedback=False):
    v = load_file()
    correct_responses=0
    test_verbs = random.sample(list(v.keys()),iterations)
    for test_verb in test_verbs:
        test_tense = random.choice(list(v[test_verb]['conjugation'].keys()))
    
        test_response = str(input(f'What is the conjugation of {test_verb} in {test_tense}? ')).split(',')
        solution = v[test_verb]['conjugation'][test_tense]
        if test_response == solution:
            if immediate_feedback:
                print('Correct.')
            correct_responses+=1
        else:
            if immediate_feedback:
                print(f'The correct answer is {solution}. Your answer was {test_response}')

    print(f'Result: {round(float(correct_responses)/float(iterations),4)*100}%')

test_1(5,True)