"""Module contains Class and Functions to scrape post data from a designated subreddit.

Functions
---------
add_ticker() 
    Adds stock symbols to a watchlist. 
list_tickers()
    View list of symbols on the watchlist. 
remove_ticker()
    Remove a symbol from the watchlist. 
create_dataframe()
    Create a dataframe to view information about recent posts on a subreddit.
filter_dataframe()
    Filter the general dataframe using the list of symbols on the watchlist. 

References
----------
PRAW Documentation 
    https://praw.readthedocs.io/en/latest/code_overview/models/subreddit.html

Blogpost with some pseudocode and API Access Information
    https://medium.datadriveninvestor.com/scraping-wallstreetbets-for-stocks-signals-414e63ace210

Any() to check if string contains an element from a list
    https://stackoverflow.com/questions/28047349/check-if-string-contains-any-elements-from-list
    
set() to remove duplicates from a list
    https://favtutor.com/blogs/remove-duplicates-from-list-python
"""
    
    
    
import praw
import pandas as pd


reddit = praw.Reddit(client_id='*****', \
                     client_secret='*****', \
                     user_agent='COGS18', \
                     username='*****', \
                     password='*****')



class RedditScraper: 
    
    Purpose = "Create a list of stock symbols and filter posts that include them."
    
    def __init__(self, sub, post_number):
        """Input specific subreddit and number of posts to scrape.
        Initializes blank list to be used for specific stock symbol screening.

        Parameters
        ----------
        sub : string
            Specific subreddit to target. 
        post_number : integer 
            Amount of posts to scrape from the subreddit. 
        """
        
        self.tickers = ['HITI', 'XSPA', 'TNXP', 'TELL', 'CTXR', 'APPL', 
                        'GME', 'AMC', 'BABA', 'ADXS', 'RIVN' ]
        self.sub = sub
        self.post_number = post_number
        
   
    def add_ticker(self, symbol):
        """Adds stock symbols to a watchlist. 
        
        Parameters
        ----------
        symbol : string 
            Abbreviated stock symbol.
        """
        if symbol == '':
            return 'You tried to input an invalid symbol.'
        else:
            self.tickers.append(symbol)
            self.tickers = list(set(self.tickers))
            return self.tickers
        
    
    def list_tickers(self):
        """View list of symbols on the watchlist. 
        
        Returns
        -------
        out : list
            List of stocks on the watchlist.
        """
        out = self.tickers
        return out
       
        
    def remove_ticker(self, symbol):
        """Remove a symbol from the watchlist.
        
        Returns
        -------
        out : list
            New watchlist with removed symbol.
        """
        
        if symbol in self.tickers: 
            self.tickers.remove(symbol)
            return self.tickers
        
     
    def create_dataframe(self):
        """Create a dataframe to view information about recent posts on a subreddit.
        
        Returns
        ----------
        df_content : dataframe
            Dataframe containing titles, scores, comment number, and body text of reddit posts. 
        """
    
        subreddit = reddit.subreddit(self.sub)
        new_subreddit = subreddit.new(limit = self.post_number)
        
        content_dict = { "title":[], "score":[], 
                        "comments": [], "body":[] }

        for submission in new_subreddit:
            
            content_dict["title"].append(submission.title)
            content_dict["score"].append(submission.score)
            content_dict["comments"].append(submission.num_comments)
            content_dict["body"].append(submission.selftext)

        df_content = pd.DataFrame(content_dict)
    
        return df_content
    
    
    def filter_dataframe(self):
        """Filter the general dataframe using the list of symbols on the watchlist.
        
        Returns
        -------
        df_filtered : dataframe
            Dataframe of posts that mention symbols on the watchlist.
        error : string
            Notification that no posts were found mentioning symbols on the watchlist. 
        """
        
        subreddit = reddit.subreddit(self.sub)
        new_subreddit = subreddit.new(limit = self.post_number)
        
        filtered_dict = { "title":[], "score":[], "comments": [],
                         "body":[], "url":[] }
        
        for submission in new_subreddit:
            
                if any(ticker in submission.title for ticker in self.tickers):
                    filtered_dict["title"].append(submission.title)
                    filtered_dict["score"].append(submission.score)
                    filtered_dict["comments"].append(submission.num_comments)
                    filtered_dict["body"].append(submission.selftext)
                    filtered_dict["url"].append(submission.url)
                else:
                    continue
                    
        df_filtered = pd.DataFrame(filtered_dict)
        error = "There are no submissions that match your requirements."
        
        if df_filtered.shape[0] > 0:
            return df_filtered
        else:
            return error
