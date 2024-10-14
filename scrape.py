
import requests
from bs4 import BeautifulSoup

def imperative_format(word: str) -> str:
    """
    Formats a German verb in imperative form.
    """
    return f"{word[0].upper()}{word[1:].lower().replace(' ','')}!"
    

def webquery_conjugation(verb):
    url = f"https://conjugator.reverso.net/conjugation-german-verb-{verb}.html"
    sess = requests.session()
    sess.headers.update({'User-Agent': 'EventParser PowerShell/7.3.4'})
    page = sess.get(url, verify=False)
    soup = BeautifulSoup(page.content, "html.parser")

    # imperative 
    imperative = soup.find_all('div', class_='blue-box-wrap alt-tense')
    for c in imperative:
        title = c['mobile-title']
        if title == 'Imperativ Präsens':
            verb_imperative = c.find('i', class_='verbtxt')
            verb_imperative = verb_imperative.text
            verb_imperative = imperative_format(verb_imperative)

    # conjugation
    conjugation = soup.find_all('div', class_='blue-box-wrap')
    output = []
    for c in conjugation:
        title = c['mobile-title']
        if title[0:9] == 'Indikativ' and title.split(' ')[1] in ['Präsens', 'Präteritum', 'Perfekt']:
            res_tense = c.p.string
            res_tags = verb_imperative
           
            for conjugation_block in c.find_all('ul', class_='wrap-verbs-listing'):
                conj_data = []
                for row in conjugation_block.children:
                    conj_data.append(' '.join(row.text.split(' ')[1:])) # remove the personal pronoun
                output.append(','.join([verb,res_tense,res_tags,';'.join(conj_data)]))      
    return output
    

                    
            
                        
                    
                    
                    
      

