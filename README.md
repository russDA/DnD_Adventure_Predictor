# DnD_Adventure_Predictor
Files to scrape Dungeon Master's Guild. An online collection of user-created D&amp;D Adventures.

Here are the python files I used to create a dataset of every single adventure available on the Dungeon Master's Guild, a collection of adventures by users.
The data was scraped with BeautifulSoup, and ordered in Pandas Dataframes, before lastly being saved as a CSV file. The data scraped was the player-levels of the adventure, price, reviews etc. Could easily be modified to scrape something else (e.g. release-date) and then re-run for more data.

*WARNING* I hardcoded a URL, and the 186 pages containing 50 entries/page. There are more details in dnd_all_pages.py.

The application takes a little over 1 second/adventure, to scrape and make an entry. At over 9000 entries, that's over 3 hours.
Generating the first successful CSV took 3 hours and 43 mins.
Could/should be optimized, emphasis should be put on dnd_optimal.py (aptly named). 
Any time reduction factor would ostensibly change total run time by the same factor.

The CSV I generated will be left in this repo., the dataset should be sufficiently large for Machine Learning purposes. 
If I ever update, I'll leave time-stamped versions on this repo.
