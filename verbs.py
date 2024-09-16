import csv 
import random
from functions import *

library_version = "1.1.0"

pronouns = ['ich','du','er/sie/es','wir','ihr','sie/Sie']
verbs={}
verbsfile="data/verbs.csv"
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

def conjugate_verb(verb:str) -> list:
    v = load_file()
    conj = v[verb]['conjugation']
    return conj

def conjugate_verb_one_mode(verb:str,mode:str) -> list:
    conj = conjugate_verb(verb)
    return conj[mode]

def conjugation_table(verb:str):
    padding = 10
    conj = conjugate_verb(verb)

    line = ['Pronoun'] + list(conj.keys())
    print(str([x.ljust(padding, ' ') for x in line]).replace('[','').replace(']','').replace(',','').replace("'",""))
    for i in range(len(pronouns)):
        line = [pronouns[i]]
        for k in conj.keys():
            line.append(conj[k][i])
        print(str([x.ljust(padding,' ') for x in line]).replace('[','').replace(']','').replace(',','').replace("'",""))
       
def conjugation_test_1(iterations):
    v = load_file()
    correct_responses=0
    test_verbs = random.sample(list(v.keys()),iterations)

    responses = []
    solutions = []
    for test_verb in test_verbs:
        test_tense = random.choice(list(v[test_verb]['conjugation'].keys()))
    
        test_response = str(input(f'What is the conjugation of {test_verb} in {test_tense}? ')).split(',')
        
        solution = v[test_verb]['conjugation'][test_tense]
        if len(test_response) == 0:
            test_response = ["" for x in range(len(solution))]

        if len(test_response) != len(solution):
            test_response = [list_find(test_response,x) for x in range(len(solution))]


        responses.append(test_response)
        solutions.append(solution)
         
        if test_response == solution:
            correct_responses+=1
            
    for i in range(len(responses)):
        compare_two_lists(responses[i], solutions[i],"Response","Solution")
        print ("")
        
    print(f'Result: {round(float(correct_responses)/float(iterations),4)*100}%')
