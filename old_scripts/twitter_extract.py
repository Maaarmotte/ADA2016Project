import os
import pandas as pd

LANGUAGE = 'en'
COLUMNS = ['source_location', 'sentiment']

def pre_allocate_df(raw):
    tweets = raw._source
    ids = raw._id
    ids.name = 'id'

    # Loop on all tweets to get all different fields
    columns = set()
    for tweet in tweets:
        if tweet.keys() is not None:
            columns.update(tweet.keys())
    columns = list(columns)

    # Pre-allocate the DataFrame, otherwise it takes too much time to fill
    # Don't use the tweets IDs for filling the DF as they are not unique !
    df = pd.DataFrame(columns=columns, index=range(len(ids)))

    return df

def preprocess_raw(raw, df):
    tweets = raw._source
    ids = raw._id
    
    for i in range(len(tweets)):
        for key, value in tweets[i].items():
            # Convert lists to strings
            if type(value) == list:
                tweets[i][key] = ' '.join(value)

        df.loc[i] = pd.Series(tweets[i])

    # Give the tweets their original IDs
    df.index = ids

    return df

def parse_month(month_txt, month_nb):
    month_df = pd.DataFrame()
    
    for i in range(31):
        day = str(i+1).zfill(2)       # Pad with zero
        file_path = 'data/{}/harvest3r_twitter_data_{}-{}_0.json'.format(month_txt, day, month_nb)
        if os.path.isfile(file_path):
            print('Parsing {}...'.format(file_path))
            
            data = pd.read_json(file_path)
            df = pre_allocate_df(data)
            df = preprocess_raw(data, df)
            
            # Only keep one language 
            df = df[df.lang == LANGUAGE]
            
            # And only a few columns
            df = pd.DataFrame(df[COLUMNS].groupby(COLUMNS).size())
            
            month_df = pd.concat([month_df, df], copy=False)
            
    return month_df.reset_index().groupby(COLUMNS).sum()
