import vocabularizer as v
import os 
import pandas as pd

files = os.listdir('vocabularies')

for file in files:
    v.load_file(f'vocabularies/{file}')
    v.output_decorator("FILE: {0}".format(file), 2)
   
    v.output_decorator("Words without mode info",6)
    a=v.df[pd.isnull(v.df['mode'])]
    print(len(a))
    if len(a)>0:
        print(a)

    v.output_decorator("Words with punctuation but not of the sentence type",6)
    a=v.df[v.df['translation'].str.contains('[\.\!\?]',regex=True, na=False)][v.df['mode']!='s']
    print(len(a))
    if len(a)>0:
        print(a)

    v.output_decorator("Sentences with no punctuation",6)
    a = v.df[~v.df['translation'].str.contains('[\.\!\?]',regex=True, na=False)][v.df['mode']=='s']
    print(len(a))
    if len(a)>0:
        print(a)

    v.unload_vocabulary()
