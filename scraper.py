import requests 
import bs4  
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
from applogger import logger

disable_warnings(InsecureRequestWarning)
def get_definite_article(noun:str=None) -> str:
    logger.debug(f'get_definite_article for {noun}')
    if noun is None:
        raise ValueError("Noun is required")
        
    articles = ['der','die','das']
    for article in articles:
        response = requests.get(f"https://der-artikel.de/{article}/{noun}.html", verify=False)
        if response.status_code == 200:
            return article

    return ''
    
def webquery_conjugation(verb):
    logger.debug(f'webquery_conjugation for {verb}')
    url = f"https://conjugator.reverso.net/conjugation-german-verb-{verb}.html"
    sess = requests.session()
    sess.headers.update({'User-Agent': 'EventParser PowerShell/7.3.4'})
    page = sess.get(url, verify=False)
    soup = bs4.BeautifulSoup(page.content, "html.parser")
    output = {'conjugations':{}, 'imperative':''}
    # imperative 
    imperative = soup.find_all('div', class_='blue-box-wrap alt-tense')
    for c in imperative:
        title = c['mobile-title']
        if title == 'Imperativ Präsens':
            verb_imperative = c.find('i', class_='verbtxt')
            output['imperative'] = verb_imperative.text

    # conjugation
    conjugation = soup.find_all('div', class_='blue-box-wrap')
    
    for c in conjugation:
        title = c['mobile-title']
        if title[0:9] == 'Indikativ' and title.split(' ')[1] in ['Präsens', 'Präteritum', 'Perfekt']:
            res_tense = c.p.string
            output['conjugations'][res_tense] = []
            for conjugation_block in c.find_all('ul', class_='wrap-verbs-listing'):
                conj_data = []
                for row in conjugation_block.children:
                    conj_data.append(' '.join(row.text.split(' ')[1:])) # remove the personal pronoun
                
                #output.append(','.join([verb,res_tense,res_tags,';'.join(conj_data)]))    
                output['conjugations'][res_tense] = conj_data
    return output
   
    