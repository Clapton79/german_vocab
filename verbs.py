import csv 
import json
import pandas as pd


verbsfile="verbs/verbs.csv"

pronoun_types=["S1","S2","S3","P1","P2","P3"]

def load_file(verbsfile):
    verbs = {}
    with open(verbsfile,'r') as reader:
        for line in csv.DictReader(reader):
            conjugation=line['conjugation'].split(';')
            if line['tense'] not in verbs.keys():
                verbs[line['tense']] = {}
            if line['verb'] not in dict(verbs[line['tense']]).keys():
                verbs[line['tense']][line['verb']]={}
            verbs[line['tense']][line['verb']] = conjugation
    return verbs

def convert_to_json(verbsfile):
    v = load_file(verbsfile)

    with open(verbsfile.replace('.csv','.json'), 'w',encoding='utf8') as f:
        json.dump(v,f,ensure_ascii=False)