"""Script to track the most mentioned stocks in the past 150 posts in r/pennystocks.

References
----------
Dictionary into bar graph
    https://www.kite.com/python/answers/how-to-plot-a-bar-chart-using-a-dictionary-in-matplotlib-in-python
Splitting strings
    https://www.freecodecamp.org/news/the-string-strip-method-in-python-explained/
"""

# This adds the directory above to our Python path
#   This is so that we can add import our custom python module code into this script
import sys
sys.path.append('../')

# Imports
from my_module.Reddit_Scraper import RedditScraper
import matplotlib.pyplot as plt 
import pandas as pd 



# PYTHON SCRIPT HERE
def bar_graph(sub, number):
    """
    Creates a bar graph based on data from specified stock subreddit.
    
    Parameters
    ----------
    sub : string
        Specific subreddit to explore.
    number : integer
        Amount of posts to scrape from the subreddit.
        
    Returns
    -------
    plt.show() : bar plot
        Shows the most mentioned stocks symbols in the subreddit. 
    """
    
    bar_graph_data = RedditScraper(sub, number)
    bar_graph_df = bar_graph_data.create_dataframe()
    
    #Separate post titles into a list of words in a new column 
    #Makes it easier to iterate through a loop and identify stock symbols
    bar_graph_df['word list'] = bar_graph_df.title.str.strip().str.split('[\W_]+')
    bar_graph_df.drop(['body'], axis = 1)
    
    #Words commonly confused as stock symbols in the data
    skip_list = ['YOLO', 'GDP', 'NYSE', 'SEC', 'OTC', 'THE', 
                 'NASDAQ', 'PUTS', 'CALLS', 'IPO', 'ETF']

    symbol_dict = {}
    
    #Iterate through each list of words from the dataframe
    for word_list in bar_graph_df['word list']:
        
        #Iterate through each word within that list 
        for word in word_list:
            if word in skip_list:
                continue
                
            #Rely on assumption that symbols are all uppercase
            #Assume symbols are less than 5 letters, more than 2
            if word.isupper() == True:
                if len(word) > 2 and len(word) <= 5:
                    if word not in symbol_dict:
                        symbol_dict[word] = 0
                    symbol_dict[word] += 1
                    symbol_counts = symbol_dict
    
    #Limit data to only include symbols mentioned 
    #multiple times
    for symbol in list(symbol_dict.keys()):
        if symbol_dict[symbol] < 3:
            del symbol_dict[symbol]
        

    keys = symbol_dict.keys()
    values = symbol_dict.values()
    
    #Create a box plot with a dynamic title 
    #depending on the subreddit specified
    plt.figure(figsize =(15,4))
    plt.title('Top Mentioned in r/' + str(sub))
    plt.bar(keys,values)
    plt.show()

pass
