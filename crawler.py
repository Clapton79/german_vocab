import requests 

def get_definite_article(noun:str=None):
    if noun is None:
        raise ValueError("Noun is required")
        
    articles = ['der','die','das']
    for article in articles:
        response = requests.get(f"https://der-artikel.de/{article}/{noun}.html")
        if response.status_code == 200:
            return article

    return None
    
    