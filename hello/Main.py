import pandas as pd
import pytrends
from pytrends.request import TrendReq
from pytrends import dailydata
import matplotlib.pyplot as plt, mpld3
import plotly.graph_objects as go
from plotly.offline import plot
from random import randint
from plotly import tools
import re
import pandas as pd
import snscrape.modules.twitter as sntwitter
import itertools
from wordcloud import WordCloud
import urllib

from transformers import pipeline


google_search = ['','youtube','images','news','froogle']
colors = []
n = 100

for i in range(n):
    colors.append('#%06X' % randint(0, 0xFFFFFF))


def scrape_google(word, date, search_type):
    result_trace = []
    for j in range(len(search_type)):
        if search_type[j]:
            pytrend = TrendReq()
            KEYWORDS = word
            print(KEYWORDS)
            KEYWORDS_CODES=[pytrend.suggestions(keyword=i)[0] for i in KEYWORDS] 
            df_CODES= pd.DataFrame(KEYWORDS_CODES)
            df_CODES
            
            EXACT_KEYWORDS=df_CODES['mid'].to_list()
            DATE_INTERVAL=date
            COUNTRY=["US"] #Use this link for iso country code
            CATEGORY=0 # Use this link to select categories
            SEARCH_TYPE=google_search[j] #default is 'web searches',others include 'images','news','youtube','froogle' (google shopping)
            
            
            Individual_EXACT_KEYWORD = list(zip(*[iter(EXACT_KEYWORDS)]*1))
            Individual_EXACT_KEYWORD = [list(x) for x in Individual_EXACT_KEYWORD]
            dicti = {}
            i = 1
            for Country in COUNTRY:
                for keyword in Individual_EXACT_KEYWORD:
                    pytrend.build_payload(kw_list=keyword, 
                                        timeframe = DATE_INTERVAL, 
                                        geo = Country, 
                                        cat=CATEGORY,
                                        gprop=SEARCH_TYPE) 
                    dicti[i] = pytrend.interest_over_time()
                    i+=1
            df_trends = pd.concat(dicti, axis=1)

            df_trends.columns = df_trends.columns.droplevel(0) #drop outside header
            df_trends = df_trends.drop('isPartial', axis = 1) #drop "isPartial"
            df_trends.reset_index(level=0,inplace=True) #reset_index
            column = []

            for w in KEYWORDS:
                for country in COUNTRY:
                    column.append(w +'-' + country)
            
                    
            df_trends.columns=['date'] + column
            #result = df_trends.plot(figsize = (12,8),x="date", y=column, kind="line", title = KEYWORDS[0] + " Google Trends")
            #result.set_xlabel('Date')
            #result.set_ylabel('Trends Index')
            #result.tick_params(axis='both', which='both', labelsize=10)
            for k in range(len(column)):
                result_trace.append(go.Scatter(x=df_trends.date, y=df_trends[column[k]], name=column[k], line=dict(color=colors[k], width=4)))

    return result_trace


specific_model = pipeline(model="finiteautomata/bertweet-base-sentiment-analysis")
pos = 0
neg = 0
neu = 0

def get_sentiment(text):
    global pos, neg, neu
    sentiment = (specific_model(text)[0])["label"]
    if sentiment == 'NEG':
            neg += 1
    elif sentiment == 'POS':
        pos += 1
    else:
        neu += 1
    return sentiment

def cleaner(tweet):
    tweet = re.sub("@[A-Za-z0-9]+","",tweet) #Remove @ sign
    tweet = re.sub(r"(?:\@|http?\://|https?\://|www|bit.ly|twitch.)\S+", "", tweet) #Remove http links
    tweet = " ".join(tweet.split())
    tweet = tweet.replace("#", "").replace("_", " ") #Remove hashtag sign but keep the text
    #tweet = " ".join(w for w in nltk.wordpunct_tokenize(tweet) if w.lower() in words or not w.isalpha())
    return tweet

def twitter_sentiment(term, num = 500):
    global pos, neg, neu
    pos = 0
    neg = 0
    neu = 0
    df = pd.DataFrame(itertools.islice(sntwitter.TwitterSearchScraper(
        term +' lang:"en-US"').get_items(), num))[['date', 'renderedContent']] 

    df['tweet_clean'] = df['renderedContent'].apply(cleaner)
    df['sentiment'] = df['tweet_clean'].apply(get_sentiment)

    positive = df[df['sentiment']=='POS']
    wordcloud = WordCloud(max_font_size=50, max_words=500, background_color="white").generate(str(positive['tweet_clean']))

    df = pd.DataFrame()
    df['Sentiment'] = ['Positive', 'Negative', 'Neutral']
    df['Total'] = [pos, neg, neu]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['Sentiment'],y=df['Total']))
    
    plot_fig = plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    return [plot(fig, output_type='div'), mpld3.fig_to_html(plot_fig)]




def get_graph(word, date, google = True, youtube = False, twitter = False, number_tweet = 500): #word need to be a list
    result_trace = []
    result_twitter = []
    if google or youtube:
        result_trace = scrape_google(word, date, [google, youtube])
    
    if twitter:
        result_twitter = twitter_sentiment(word[0], number_tweet)
    fig = tools.make_subplots(rows=len(result_trace),cols=1, vertical_spacing=0.5)
    #print(len(result_trace))
    for i in range(len(result_trace)):
        fig.add_trace(result_trace[i], row = i + 1, col = 1)
    
    return [plot(fig, output_type='div'), result_twitter]

