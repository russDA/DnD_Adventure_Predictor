#Part of a package to scrape through the DM's Guild's adventures, and retrieve uselful information for Machine Learning applications

#Russell Abraira

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests

# =============================================================================
# A general function to create an entry
# =============================================================================
def add_entry(title, rating, reviews, price, pages, first, second, third, fourth):
    return {'Title':title, 'Stars':rating, 'Reviewers': reviews, 'Cost':price, 'Page Count':pages, 'Levels 1-4':first, 'Levels 5-10':second, 'Levels 11-16':third, 'Levels 17+':fourth}

# =============================================================================
# A function to make an entry based on the url of a page
# 
# Modify this if ever need to scrape again for other info, such as date of publication, or author, etc
# =============================================================================
def make_entry_from(url):   
   
    #Set generic values, just in case. Will drop in machine learning models, anyways.
    #
    title=''
    rating = -1
    reviews = 0
    price = 0
    pages = -1
    first = 0
    second = 0
    third = 0
    fourth = 0
    
    #Just in case it's a junk link, had at least one in the ~9000 entries. Return junk if link leads to garbage
    #
    try:
        site = requests.get(url)
        
        soup = BeautifulSoup(site.text, features='lxml')
    except:
        return add_entry(title, rating, reviews, price, pages, first, second, third, fourth)
    
    #Get adventure title
    #
    title = soup.find('span', {'itemprop':'name'}).text
    print(f'Getting title: {title}')
    
    #Finding the tiers (What level si the adventure for)
    #
    levels = soup.find('meta', {'name':'keywords'})
    
    #Containted in meta data as a string, splitting the string.
    #Fetching the end of the left strings, which contains 1st, 2nd, etc.
    #
    splitted = str.split(levels['content'], ' Tier')
    del splitted[-1]
    
    #Whenever it contains the relevant tier of gameplay, will assign a 1 to that value. Default is 0 (i.e. not for that tier)
    #Will make it easier for future Machine learning classification models, this way
    #
    print(x.text for x in splitted)
    for x in splitted:
        if x[-3:] == '1st':
            first=1
        if x[-3:] == '2nd':
            second=1
        if x[-3:] == '3rd':
            third=1
        if x[-3:] == '4th':
            fourth=1
        
    #Obtaining the rating, straightforward
    #
    if soup.find('meta', {'itemprop':'ratingValue'}) !=None:
        stars = soup.find('meta', {'itemprop':'ratingValue'})
        
        rating = float(stars['content'])
    
    #Obtaining number of reviews, also straightforward
    #
    if soup.find('meta', {'itemprop':'reviewCount'}) !=None:
        reviewers = soup.find('meta', {'itemprop':'reviewCount'})
        
        reviews = int(reviewers['content'])
    
    #Obtaining the price, again, straightforward
    #taking the string after the zeroth element, since that is the '$' sign. And then converting to float
    #
    if soup.find('div', {'id':'product-price'}) != None:
        price = float(soup.find('div', {'id':'product-price'}).text[1:])
    
    #Finding the widget element which houses page numbers, tricky since they all have same name
    #
    length = soup.find_all('div', {'class':'widget-information-item-content'})
    
    #Can't target the div I want, so cycle through all.
    #The page count is after the edition, loop to target the edition, then copy the next value as an int
    #
    break_next = False
    
    for x in length:
        
        if break_next:
            try:
                a = int(x.text)
            except:
                break
            pages=int(x.text)
            break
        
        if x.text==' 5th Edition ':
            break_next=True
    
# =============================================================================
#     Finally return the entry. This will return junk info if the page leads to such, thanks to initialization of variables
# =============================================================================
    return add_entry(title, rating, reviews, price, pages, first, second, third, fourth)


















