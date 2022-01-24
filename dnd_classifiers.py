#Part of a package to scrape through the DM's Guild's adventures, and retrieve uselful information for Machine Learning applications

#Russell Abraira

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from bs4 import BeautifulSoup
import requests
from time import perf_counter
from matplotlib import pyplot as plt
from scipy import stats
import sklearn as skl
from sklearn import model_selection
from sklearn.linear_model import LinearRegression
from sklearn.naive_bayes import CategoricalNB as cnb
from sklearn.neighbors import KNeighborsClassifier as knc
from sklearn.pipeline import make_pipeline as mp
from sklearn.preprocessing import StandardScaler as ss
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsRegressor as knr
from sklearn.tree import DecisionTreeClassifier as dtc

# =============================================================================
# Import data, then start stripping and cleaning. Made my initial data of Jan 23rd 2022 go from over 9285 entries to 4866.
# N.B. This means nearly half of all modules don't have a (rating and pagecount). Should investigate if there's a relationship here
# =============================================================================
dataset = pd.read_csv(r'dms_guild_adventures_master.csv')
dataset = dataset[dataset['Stars'] != (-1)]
dataset = dataset[dataset['Page Count'] != (-1)]
dataset['StarCat'] = dataset['Stars']

# =============================================================================
# I think I did this inneficiently... Making a list to house my arbitrary categorization.
# I believe there's a pd map function which achieves this more elegantly
# =============================================================================
starcat = []
for i in dataset['StarCat']:
   
    if i == 5.0 or i == 4.9:
        starcat.append('Masterful')
    elif i == 4.8 or i == 4.7 or i == 4.6:
        starcat.append('Excellent')
    elif i == 4.5 or i == 4.4 or i == 4.3:
        starcat.append('Very Good')
    elif i == 4.2 or i == 4.1 or i == 4.0:
        starcat.append('Good')
    elif i < 4.0 and i >= 3.0:
        starcat.append('Okay')
    else: #less than 3.0
        starcat.append('Pass')
        
dataset['Starcat'] = starcat

# =============================================================================
# Doing something similar here, assigning a category depending on cost per page. 
# A somewhat arbitrary categorization, since it assumes every page is of equal quality, still, not bad predictor
# =============================================================================
dataset['Cost/page'] = dataset['Cost']/dataset['Page Count']
cost_per_page = plt.hist(dataset['Cost/page'], bins=np.linspace(0, dataset['Cost/page'].max(), 140))
value = []
for i in dataset['Cost/page']:
    if i == 0:
        value.append('Free')
    elif i <= 0.10:
        value.append('Fantastic')
    elif i <= 0.20:
        value.append('Decent')
    elif i <= 0.30:
        value.append('High')
    else: #High cost per page
        value.append('Steep')
        
dataset['Value'] = value

# =============================================================================
# Converting the price/page to a categorical matrix, of 1 or 0. The cool kids call this  'one hot encoding'
# =============================================================================
h = pd.get_dummies(dataset['Value'])
dataset = dataset.join(h)

#I want to predict based on these categories, I wish I had made these column names variables... eg HIGH = 'High'
#
predictor_columns = ['Free', 'Fantastic', 'Decent', 'High', 'Steep', 'Levels 1-4','Levels 5-10','Levels 11-16','Levels 17+']

# =============================================================================
# Data preparation For the models. Using a 33-67 split of data
# =============================================================================
train, test = skl.model_selection.train_test_split(dataset, test_size=0.33)

train_x = np.asarray(train[['Page Count', 'Cost', 'Reviewers']])
train_y = train['Stars']

test_x = np.asarray(test[predictor_columns])
test_y = test['Starcat']

# =============================================================================
# K nearest neighbor classification
# =============================================================================
model_knc = knc().fit(np.asarray(train[predictor_columns]), np.asarray(train['Starcat']))

precit_knc = model_knc.predict(test_x)

score_knc = np.round(model_knc.score(test_x, test_y.to_numpy().reshape(-1,1)), 3)


# =============================================================================
# Decision tree classification
# =============================================================================
model_dtc = dtc().fit(np.asarray(train[predictor_columns]), np.asarray(train['Starcat']))

predcit_dtc = model_dtc.predict(test_x)

score_dtc = np.round(model_dtc.score(test_x, test_y.to_numpy().reshape(-1,1)), 3)


# =============================================================================
# Naive Bayes classifier
# =============================================================================
model_cnb = cnb().fit(np.asarray(train[predictor_columns]), np.asarray(train['Starcat']))

predcit_cnb = model_cnb.predict(test_x)

score_cnb = np.round(model_cnb.score(test_x, test_y.to_numpy().reshape(-1,1)), 3)




# =============================================================================
# From my first run with these models, given my data. My predictors were (in decreasing order)
# 
# Naive Bayes :   ~42.5%
# Decision Tree:  ~41.0%
# K. Nearest N.:  ~29.5%
# 
# These based on a few test runs, nothing too rigorous, will try regressive models
# =============================================================================

