import pandas as pd
import numpy as np 
import os
import re
from cleaner import *

# PATH FILES 
RAW_DATA_FOLDER_PATH = "../competence_1/raw_data/"

RAW_SCRAP_PATH = RAW_DATA_FOLDER_PATH + "raw_scrap_2023-12-25.csv"
RAW_API_PATH = RAW_DATA_FOLDER_PATH+ "raw_api_2023-12-25.csv"
RAW_DB_PATH = RAW_DATA_FOLDER_PATH + f"raw_db_2023-12-25.csv" 
RAW_FILE_PATH = RAW_DATA_FOLDER_PATH + f"raw_file_2023-12-19.csv"
RAW_BIGDATA_PATH = RAW_DATA_FOLDER_PATH + "raw_bigdata_2023-12-26.csv"

def main():

    # 1. Read the different data
    raw_scrap = pd.read_csv(RAW_SCRAP_PATH)
    raw_api = pd.read_csv(RAW_API_PATH)
    raw_db = pd.read_csv(RAW_DB_PATH)
    raw_file = read_raw_csv(RAW_FILE_PATH,"french","breton")
    raw_bigdata = read_raw_csv(RAW_BIGDATA_PATH,
                           "french",
                           "polish",
                           url_source="https://object.pouta.csc.fi/OPUS-NLLB/v1/tmx/fr-pl.tmx.gz",
                           raw_source="OPUS_NLP",
                           src_type="bigdata")
    
    # 2. Cleaning

    scrap_cleaned = cleaning(raw_scrap,str_clean,["text_origin","text_target"])
    api_cleaned = cleaning(raw_api, str_func=str_clean)
    db_cleaned = cleaning(raw_db, str_func=str_clean)
    file_cleaned = cleaning(raw_file, str_func=str_clean)
    bigdata_cleaned = cleaning(raw_bigdata,str_clean) # ~11 sec

    # 3. Aggregation

    cleaned_dfs = [api_cleaned, db_cleaned,scrap_cleaned,file_cleaned,bigdata_cleaned]
    aggregate_df = pd.concat(cleaned_dfs)
    aggregate_df.reset_index(inplace=True)
    aggregate_df.drop(columns="index", inplace=True)

    # 4. Save

    save_as_csv(aggregate_df[:15000],"../competence_4/reduced_aggregated.csv",quotechar="}")

