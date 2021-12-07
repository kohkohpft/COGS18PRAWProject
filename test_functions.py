"""Test for my functions.

References
----------
.all() to test dataframe columns 
    https://stackoverflow.com/a/59954228
"""

from my_module.Reddit_Scraper import RedditScraper
from my_module.bar_graph import bar_graph

"""Create generic instances of the RedditScraper class"""
test = RedditScraper('Pennystocks', 5)
test_df = test.create_dataframe()

def test_dataframe():
    """Tests for correct dataframe shape."""

    assert test_df.shape[0] == 5
    assert((test_df['comments']%1 == 0).all() == True)
    
def test_watchlist_functions():
    """Tests that watchlist functions are working."""
   
    assert callable(test.add_ticker)
    assert callable(test.remove_ticker)
    assert callable(test.list_tickers)
    
def test_watchlist():
    """More watchlist function tests and duplicate dropping"""
    
    test.add_ticker('GOOGL')
    test.add_ticker('GOOGL')

    assert len(test.list_tickers()) == len(set(test.list_tickers()))
        
def test_bar_graph():
    """Test if bar graph function is callable"""
  
    assert callable(bar_graph)

    



                 
    