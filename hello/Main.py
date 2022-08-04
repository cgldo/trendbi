import pandas as pd
import pytrends
from pytrends.request import TrendReq
from pytrends import dailydata
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from random import randint

colors = []
n = 100

for i in range(n):
    colors.append('#%06X' % randint(0, 0xFFFFFF))

def get_graph(word): #word need to be a list
    pytrend = TrendReq()
    KEYWORDS = word
    KEYWORDS_CODES=[pytrend.suggestions(keyword=i)[0] for i in KEYWORDS] 
    df_CODES= pd.DataFrame(KEYWORDS_CODES)
    df_CODES

    EXACT_KEYWORDS=df_CODES['mid'].to_list()
    DATE_INTERVAL='2020-01-01 2021-01-01'
    COUNTRY=["US","GB", "DE", "CN"] #Use this link for iso country code
    CATEGORY=0 # Use this link to select categories
    SEARCH_TYPE='' #default is 'web searches',others include 'images','news','youtube','froogle' (google shopping)

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
    for word in KEYWORDS:
        for country in COUNTRY:
            column.append(word +'-' + country)
    
            
    df_trends.columns=['date'] + column
    #result = df_trends.plot(figsize = (12,8),x="date", y=column, kind="line", title = KEYWORDS[0] + " Google Trends")
    #result.set_xlabel('Date')
    #result.set_ylabel('Trends Index')
    #result.tick_params(axis='both', which='both', labelsize=10)
    return df_trends, column


fig = go.Figure()
chart, label = get_graph(["Genshin Impact"])
for i in range(len(label)):
    fig.add_trace(go.Scatter(x=chart.date, y=chart[label[i]], name=label[i],
                         line=dict(color=colors[i], width=4)))

fig.show()
