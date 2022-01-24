#Part of a package to scrape through the DM's Guild's adventures, and retrieve uselful information for Machine Learning applications

#Russell Abraira

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
from time import perf_counter

import dnd_optimal as dndo
import dnd_185 as dndn

#This is the common name of every dmsguild page which has, at the bottom, 50 entries, except last page
#
generic_url = 'https://www.dmsguild.com/browse.php?filters=0_0_45393_0_0_0_0_0&src=fid45393&page='

# =============================================================================
# Make an int/str list from 1-186, useful throughout the fetching of data. 
# 
# WARNING! as this is hardcoded, would need to be changed in the future, when more modules are added, or if repurposed for different set of modules
# 
# =============================================================================
pages = np.linspace(1,186, 186)
pages = pages.astype(int).astype(str)

#making empty list which will house the urls which are appended with a string int from 1-186
#
broad_page_urls = []
for p in pages:
    broad_page_urls.append(generic_url+p)

#Fun to see how long this process takes.
#
time_start = perf_counter()


#Inititalize some elements
#
list_of_dfs = []
df = pd.DataFrame()
counter=0

#Cycle through the number of pages, 186, and take the Dataframes of size 50, obtained via dnd_185 file
#
for p in pages.astype(int):
    
    #This takes a while, fun to see something in the Console
    #
    list_of_dfs.append(dndn.take_page(broad_page_urls[p-1]))
    print('\n Gone Through a page \n')

#Create a master df, the concat of the list of all other dfs
#
master_df = pd.concat(list_of_dfs, ignore_index=True)
    
#Save it into a csv, so you don't have to run a long-ass program every time you want to use the data :,)
#
master_df.to_csv('dms_guild_adventures_master.csv', index=False)

# =============================================================================
# How long does this process take? 
# The first time I (successfully) ran this program, to generate 9285 entries, took 223.81 Minutes.
# Achieved on Jan 23rd 2022
# =============================================================================
time_stop = perf_counter()
total_time = time_stop-time_start
total_time = total_time/60
print(f'To scrape through over 9000 entries of DMs Guild Adventures, it took: {total_time} minutes')










