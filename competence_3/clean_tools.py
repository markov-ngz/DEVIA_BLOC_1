import pandas as pd
import numpy as np 
import re
from datetime import datetime

def str_clean(x):
    """
    
    """
    bad_caracs = ["\n"]
    bad_exprs = [r"\(.*\)",r"\[.*\]",r"{.*}"]

    for bad_carac in bad_caracs : 
        x = x.replace(bad_carac,"")
        
    for bad_expr in bad_exprs:
        x = re.sub(bad_expr,"",x)
    return x

def cleaning(raw_df:pd.DataFrame,str_func, text_cols:list =["text_origin","text_target"])->pd.DataFrame:
    """
    """
    # check if any specified cols are not in the df 
    for col in text_cols:
        if col not in raw_df.columns:
            raise ValueError(f"Incorrect text_cols arguments : \n Column {col} not found in the provided df columns : \n {raw_df.columns.values}")

    # line to make it bit prettier
    line = "\n-------------------------------------------------------------------------------------- "

    temp_df = raw_df.copy()

    # Remove null's
    print(f"Nombre de données manquantes par colonnes dans le jeu : {temp_df.isnull().sum()} {line}")
    temp_df.dropna(subset=["text_origin","text_target","lang_origin","lang_target"],inplace=True)

    # rapply cleaning value fonction to the specified columns
    for col in text_cols :
        temp_df[col] = temp_df[col].map(str_func)

    # don't word any particle or else : 
    for col in text_cols :
        len_col = "len_"+col
        temp_df[len_col] = temp_df[col].map(lambda x: len(x))
        temp_df = temp_df[temp_df[len_col] > 2]
        temp_df.drop(columns=len_col, inplace=True)
    return temp_df



def read_raw_csv(tsv_path:str,lang_origin, lang_target, url_source:str=None,raw_source:str="tatoeba",src_type="file")->pd.DataFrame:

    # today's date : "YYYY-MM-DD"
    now = datetime.now().strftime("%Y-%m-%d")
    
    if raw_source == "tatoeba":
        if not url_source:
            url_source = "https://tatoeba.org/fr/downloads"
        # pattern column is id, text , id , text => text, text
        df_raw = pd.read_csv(tsv_path, sep="\t", header=None)[[1,3]]
        # rename columns 1 , 3 to "text_origin","text_target"
        df_raw.columns = ["text_origin","text_target"]
    elif raw_source == "OPUS_NLP":
        if not url_source:
            url_source="https://opus.nlpl.eu/"
        df_raw = pd.read_csv(tsv_path, quotechar="¤",on_bad_lines="skip",header=None)
        df_raw.columns = ["text_origin","text_target","lang_origin","lang_target"]
        
    df_raw["lang_origin"] = lang_origin
    df_raw["lang_target"] = lang_target
    df_raw["source"] = url_source
    df_raw["source_type"] = src_type
    df_raw["created_at"] = now

    return df_raw

def save_as_csv(df:pd.DataFrame, output_path:str,quotechar="")->None:
    """

    """
    now = datetime.now().strftime("%Y-%m-%d")
    output_path_timed = output_path[:-4]+ "_" + now + ".csv"
    try :
        # save as csv add quoting to put it into db easily
        df.to_csv(output_path_timed,index=False,quotechar=quotechar,header=False)
        
    except Exception as e :

        raise FileNotFoundError(f"Output path does not exist !")
    
    else : 
        print(f"[Success] Dataframe saved as csv at location : {output_path_timed}")



