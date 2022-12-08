##########################################
#   ___ __  __ ___  ___  ___ _____ ___   #
#  |_ _|  \/  | _ \/ _ \| _ |_   _/ __|  #
#   | || |\/| |  _| (_) |   / | | \__ \  #
#  |___|_|  |_|_|  \___/|_|_\ |_| |___/  #
#                                        #
##########################################

#########################################################
#   ___  ___ ___ ___ _  _ ___ _____ ___ ___  _  _ ___   #
#  |   \| __| __|_ _| \| |_ _|_   _|_ _/ _ \| \| / __|  #
#  | |) | _|| _| | || .` || |  | |  | | (_) | .` \__ \  #
#  |___/|___|_| |___|_|\_|___| |_| |___\___/|_|\_|___/  #
#                                                       #
#########################################################

#############################################
#   ___ _____ _   _  _ ___   _   ___ ___    #
#  / __|_   _/_\ | \| |   \ /_\ | _ |   \   #
#  \__ \ | |/ _ \| .` | |) / _ \|   | |) |  #
#  |___/ |_/_/ \_|_|\_|___/_/ \_|_|_|___/   #
#                                           #
#############################################

######################################
#   ___ ___  ___   ___ ___ ___ ___   #
#  | _ | _ \/ _ \ / __| __/ __/ __|  # 
#  |  _|   | (_) | (__| _|\__ \__ \  #
#  |_| |_|_\\___/ \___|___|___|___/  #
#                                    #
######################################


import httpx
from selectolax.parser import HTMLParser
from dataclasses import dataclass, asdict

from pprint import pprint
import pandas as pd

@dataclass
class Product:
    manufacturer: str
    title: str
    price: str
    
def get_html(page):
    url = f"https://www.thomann.de/gb/search_GF_electric_guitars.html?ls=100&og={page}&hl=BLOWOUT"
    resp = httpx.get(url)
    return HTMLParser(resp.text)



def get_thomann_html(page_no:int=1) -> HTMLParser:
    # Convert the integer input into string.
    if isinstance(page_no, int):
        page_no = str(page_no)
    
    url = f"https://www.thomann.de/gb/search_GF_electric_guitars.html?ls=100&og={page_no}&hl=BLOWOUT"
    response = httpx.get(url)
    return HTMLParser(response)


def parse_product(html):
    products = html.css("div.product")
    
    results = []
    for item in products:
        new_item = Product(
            manufacturer = item.css_first("span.title__manufacturer").text(),
            title = item.css_first("span.title__name").text(),
            price = item.css_first("div.product__price").text().strip()
        )
        results.append(asdict(new_item))
    return results

EXPORT_CSV = False


def main() -> None:
    
    # Given page number get the items in the page.
    html = get_html(1)
    result = parse_product(html)
    
    # Transfer to pandas dataframe then csv.
    df = pd.DataFrame.from_dict(result)
    if EXPORT_CSV:
        df.to_csv("sample.csv")
        
    print(df.head(20))
    

if __name__ == "__main__":
    main()
    
    print("-"*50)
    print("File Executed... ")
    print("-"*50)