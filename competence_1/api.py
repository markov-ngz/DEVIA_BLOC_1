import pandas as pd
import requests
import time
from dotenv import load_dotenv
import os
from datetime import datetime
from tools.save_raw import save_as_csv

load_dotenv()

def api_extraction()->pd.DataFrame:
    
    # get french data 
    df = pd.read_csv("utils/frnech_sentence.csv")
    sentences_fr = df.french_text.values

    # container 
    language_dict = {
        "french_text":sentences_fr,
        "polish_text":[]
    }

    # requests params
    url = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-fr-pl"

    API_TOKEN = os.environ["AUTH_TOKEN_HF_API"]
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    # make a translation request every sentence
    for sentence in language_dict["french_text"]:

        # Content
        payload ={
        "inputs": sentence,
        "wait_for_model":True
        }

        # post request -> json -> dict
        response_json = requests.post(url, headers=headers, json=payload).json()
        
        # extract the content 
        polish_translation = response_json[0]["translation_text"]
        
        # append it
        language_dict["polish_text"].append(polish_translation)

        time.sleep(1)

    df = pd.DataFrame(language_dict)
    df["created_at"] = datetime.now().strftime("%Y-%m-%d")
    df["source"] = url
    df["source_type"] = "API"

    return df
