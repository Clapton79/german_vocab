import csv 
import random
from functions import *
import coloring 

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
            imperative = [x for x in verbs[line['verb']]['tags'] if x[-1] == '!']
            if len(imperative)>0:
                imperative = imperative[0]
            else:
                imperative = ''
                
            verbs[line['verb']]['imperative'] = imperative
            try:
                conjugation = verbs[line['verb']]['conjugation']
            except KeyError:
                verbs[line['verb']]['conjugation'] = {}

            verbs[line['verb']]['conjugation'][line['tense']]=line['conjugation'].split(';')

    verbsfile_loaded = True
    return verbs

def conjugate_verb(verb:str) -> list:
    v = load_file()
    try:
        conj = v[verb]['conjugation']
    except KeyError:
        conj = {}
    return conj

def conjugate_verb_one_mode(verb:str,mode:str) -> list:
    conj = conjugate_verb(verb)
    return conj[mode]

def conjugation_table(verb:str):
    padding = 15
    conj = conjugate_verb(verb)
    
    if len(conj)>0:
        print(f"{bcolors.OKGREEN}{bcolors.BOLD}{str(verb.upper()).rjust(padding,' ')}{bcolors.ENDC}")
        print('----------------------------------------------------------------')
        line = ['Pronoun'] + list(conj.keys())
        line_print=(str([x.ljust(padding, ' ') for x in line]).replace('[','').replace(']','').replace(',','').replace("'",""))
        print(f"{bcolors.BOLD}{line_print}{bcolors.ENDC}")
        
        for i in range(len(pronouns)):
            line = [pronouns[i]]
            for k in conj.keys():
                line.append(conj[k][i])
            line_print = str([x.ljust(padding, ' ') for x in line]).replace('[', '').replace(']', '').replace(',', '').replace("'", "")
            print(line_print)
        print('================================================================')
    else:
        print(f'No conjugation data found for {verb}')
        

