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
from utils import flatten_lists, print_section, validate_dir

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

EXPORT_CSV = True
VERBOSE = True
TEST = True

# Extract til what page
PAGE_END = 3

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

def parse_product(html: HTMLParser, page_number: int) -> List[dict]:
    products = html.css("div.product")
    results = []
    for item in products:
        new_item = Product(
            page_no = page_number,
            manufacturer = item.css_first("span.title__manufacturer").text(),
            title = item.css_first("span.title__name").text(),
            description = item.css_first("div.product__description").text().strip(),
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

import matplotlib.pyplot as plt

def main() -> None:
    results = []
    for page_no in range(1,PAGE_END+1):
        html = get_thomann_html(page_no)
        result = parse_product(html, page_no)
        results.append(result)
        
    # Process data and transfer to dataframe
    flattened_results = flatten_lists(results)
    df_products = pd.DataFrame.from_dict(flattened_results)
    
    if VERBOSE:
        print(df_products.head(5))
    
    if EXPORT_CSV:
        df_products.to_csv(FILE_OUTPUT)
        

if __name__ == "__main__":
    print_section("File Commencing")
    validate_dir(PATH_OUTPUT)
    
    main()
    print_section("File Commenced")