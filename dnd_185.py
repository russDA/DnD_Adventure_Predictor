#Part of a package to scrape through the DM's Guild's adventures, and retrieve uselful information for Machine Learning applications

#Russell Abraira

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests

import dnd_optimal as dndo

# =============================================================================
# This will go through all the pages which contain the modules at the bottom, that would be 186 pages as of Jan 23rd 2022
# =============================================================================
def take_page(url):
    
# =============================================================================
#     The adventures, 50 per page, are housed in html table, best way was to access the ~50 <tr>s per page
# =============================================================================
    site = requests.get(url)
    soup = BeautifulSoup(site.text, features='lxml')
    trs = soup.find_all('tr', {'class':'dtrpgListing-row'})
    
# =============================================================================
#   store the url to each different module in a list, from that page, the url can always be found in the first <a> of each <tr>
# =============================================================================
    urls_in_page = []
    for tr in trs:
        urls_in_page.append(tr.find('a', {'class':'product_listing_link'})['href'])
        
# =============================================================================
#     create an entry from the url obtained from above list. Append using dnd_scan .py
# =============================================================================
    full_page_entries = []
    for url in urls_in_page:
        full_page_entries.append(dndo.make_entry_from(url))
        
# =============================================================================
#     At the end, return a dataframe of the ~50 entries created per page
# =============================================================================
    return pd.DataFrame(full_page_entries)
        
    
    
    
    
    
    
    
    
    
    
    
    