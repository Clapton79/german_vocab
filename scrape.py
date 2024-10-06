
import requests
from bs4 import BeautifulSoup

def conjugate_verb(verb):
    url =  f"https://conjugator.reverso.net/conjugation-german-verb-{verb}.html"
    sess = requests.session()
    sess.headers.update({'User-Agent': 'EventParser PowerShell/7.3.4'})
    page = sess.get(url)
    soup = BeautifulSoup(page.content,"html.parser")

    conjugation = soup.find_all('div', class_='blue-box-wrap')
    for c in conjugation:
        title = c['mobile-title']
        if title[0:9] == 'Indikativ' and title.split(' ')[1] in ['Präsens', 'Präteritum','Perfekt']:
            
            res_tense = c.p.string
            res_tags = ''
            for k in c.find_all('ul', class_='wrap-verbs-listing'):
                m= k.find_all('i',class_='graytxt')
                n = k.find_all('i', class_='verbtxt')
                a = k.find_all('i', class_='particletxt')
                aux = k.find_all('i', class_='auxgraytxt')
                if len(aux) == 0:
                    aux = ['' for x in n]
                else:
                    aux = [x.text for x in aux]
                if len(a) == 0:
                    a = ['' for x in n]
                else:
                    a = [x.text for x in a]
                my_list = []
            
                for i in range(len(m)):
                    my_list.append("".join([aux[i],a[i],n[i].text]))
                res_conj = ';'.join(my_list[0:6])
        
            res_row = ','.join ([verb,res_tense,res_tags,res_conj])       
            print(res_row)
      
    
            
