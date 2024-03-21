import requests
from datetime import datetime

def download_file(url:str,output_path:str)->None:
    """
    
    """
    created_at = datetime.now().strftime("%Y-%m-%d")

    complete_output_path =  output_path[:-4] + "_" + created_at + output_path[-4:]

    response = requests.get(url)
    if response.status_code == 200:
        with open(complete_output_path, 'wb') as f:
            f.write(response.content)
        print('File downloaded successfully.')
    else:
        raise Exception(f" File not available at the URL : { url} , Status code : { response.status_code }")