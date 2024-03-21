import database, api, file_data, html_parse, scrap
from tools.save_raw import save_as_csv
import os
import sys
from ..tools.path_ok import path_ok

def extract_all(output_folder_path:str)->None:
    """
    Extracts Data from 4 different sources : 
    - API
    - Database
    - Scrapping
    - File Download
    
    *Big Data Application is executed independantly

    For usage : 
    please set manually the URL of the file you wish to download 
    &
    the URL to scrap along with its parsing
    & 
    in the api.py file set the json parsing and api url to request
    """


    #---0. Normalize output_path--------------------------------------------------------------------------------------
    

    output_folder_path = path_ok(output_folder_path)
    
    #---1. Data Extraction --------------------------------------------------------------------------------------------------------

    # 1.1 API
    raw_df_api = api.api_extraction()
    save_as_csv(raw_df_api,output_folder_path+"raw_api.csv")

    # 1.2 DB
    raw_df_db = database.database_extraction()
    save_as_csv(raw_df_db,output_folder_path+"raw_db.csv")

    # 1.3 HTML
    url_scrapped = "https://fr.wikiversity.org/wiki/Polonais/Vocabulaire/Se_pr%C3%A9senter"
    html_scrapped = scrap.web_scrapping(url_scrapped,"utils/msedgedriver.exe")
    raw_df_scrap = html_parse.parse_html(html_scrapped,url_scrapped)
    save_as_csv(raw_df_scrap,output_folder_path+"raw_scrap.csv")

    # 1.4 FILE

    url_file_download = f"https://tatoeba.org/fr/exports/download/43062/Paires%20de%20phrases%20en%20fran%C3%A7ais-breton%20-%202023-12-19.tsv"
    output_path = output_folder_path+"raw_file.csv"
    file_data.download_file(url_file_download, output_path)

    # 1.5 System Big Data => Please see : bigdata.py in the parent directory

extract_all(sys.argv[1])

