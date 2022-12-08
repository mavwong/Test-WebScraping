##########################################
#   ___ __  __ ___  ___  ___ _____ ___   #
#  |_ _|  \/  | _ \/ _ \| _ |_   _/ __|  #
#   | || |\/| |  _| (_) |   / | | \__ \  #
#  |___|_|  |_|_|  \___/|_|_\ |_| |___/  #
#                                        #
##########################################

import pandas as pd
from pathlib import Path
from typing import List

import httpx
from selectolax.parser import HTMLParser
from dataclasses import asdict

from data_req import Product
from utils import flatten_lists

#############################################
#   ___ _____ _   _  _ ___   _   ___ ___    #
#  / __|_   _/_\ | \| |   \ /_\ | _ |   \   #
#  \__ \ | |/ _ \| .` | |) / _ \|   | |) |  #
#  |___/ |_/_/ \_|_|\_|___/_/ \_|_|_|___/   #
#                                           #
#############################################

PATH_CWD = Path.cwd()
PATH_OUTPUT = PATH_CWD / "output"
FILE_OUTPUT = PATH_OUTPUT / "products.csv"

EXPORT_CSV = False
VERBOSE = True
TEST = True

#########################################################
#   ___  ___ ___ ___ _  _ ___ _____ ___ ___  _  _ ___   #
#  |   \| __| __|_ _| \| |_ _|_   _|_ _/ _ \| \| / __|  #
#  | |) | _|| _| | || .` || |  | |  | | (_) | .` \__ \  #
#  |___/|___|_| |___|_|\_|___| |_| |___\___/|_|\_|___/  #
#                                                       #
#########################################################

    
def get_thomann_html(page_no:int = 1) -> HTMLParser:
    url = f"https://www.thomann.de/gb/search_GF_electric_guitars.html?ls=100&og={page_no}&hl=BLOWOUT"
    response = httpx.get(url)
    return HTMLParser(response.text)

def parse_product(html: HTMLParser) -> List[dict]:
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


######################################
#   ___ ___  ___   ___ ___ ___ ___   #
#  | _ | _ \/ _ \ / __| __/ __/ __|  # 
#  |  _|   | (_) | (__| _|\__ \__ \  #
#  |_| |_|_\\___/ \___|___|___|___/  #
#                                    #
######################################


def main() -> None:
    results = []
    for page in range(1,4):
        html = get_thomann_html(page)
        result = parse_product(html)
        results.append(result)
        
    # Process data and transfer to dataframe
    flattened_results = flatten_lists(results)
    df_products = pd.DataFrame.from_dict(flattened_results)
    
    if VERBOSE:
        print(df_products.head(10))
    
    if EXPORT_CSV:
        df_products.to_csv(PATH_OUTPUT)
        

if __name__ == "__main__":
    main()
    
    print("-"*50)
    print("File Executed... ")
    print("-"*50)