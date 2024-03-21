from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
import requests

def web_scrapping(url:str, driver_path:str)->str:
    """
    From a URL and the path  to the Driver that will scrap the html
    Return a str with all the html from the given page 
    """

    # driver monitor ( start / close )
    service = Service(executable_path=driver_path)

    # driver window instantiation
    driver = webdriver.Edge(service=service)

    try : 
        r = requests.get(url)
        r.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("Bad request:",err)
    else:
        # browser + GET to url 
        driver.get(url)
        # "html" -> str
        html = driver.page_source
        # wait 1 seconds 
        WebDriverWait(driver, timeout=1) 

        return html
    finally:
        driver.quit()