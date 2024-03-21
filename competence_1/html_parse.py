from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def parse_html(html:str,from_url:str)->pd.DataFrame:
    """
    Parse the html of the specific url : 
    "https://fr.wikiversity.org/wiki/Polonais/Vocabulaire/Se_pr%C3%A9senter"
    
    """
    # container 
    language_dict = {
        "text_origin":[],
        "text_target":[]
    }

    # html soup to parse
    soup  =  BeautifulSoup(html, 'html.parser')

    tables = soup.find_all("table")

    for table in tables:
        if "polonais" not in table.tbody.find_all("tr")[0].text :
            continue
        rows = table.tbody.find_all("tr")
        for row in rows[1:]: # no header
            tds = row.find_all("td")
            if len(tds) == 2:
                pl_text = tds[0].text
                fr_text = tds[1].text
                language_dict["text_origin"].append(fr_text)
                language_dict["text_target"].append(pl_text)

    df = pd.DataFrame(language_dict)
    df["created_at"] = datetime.now().strftime("%Y-%m-%d")
    df["source"] = from_url
    df["source_type"] = "scrapping"
    df["lang_origin"] = "french"
    df["lang_target"] = "polish"
    
    return df