# Trendbi

A Django app used to visualize micro trends about search term on google, youtube and twitter

## Packages Used for Data

#### For Google and Youtube
pytrends - search index data

#### For Twitter
snscrape - for scraping tweets from Twitter
https://github.com/VinAIResearch/BERTweet - used for sentiment analysis

#### For visualization
plotly - line and bar charts
WordCloud - for the positive and negative sentiment wordcloud

## Installation
Create a virtual environment for Python on your machine
run pip install -r requirements.txt
run py manage.py runserver

## Sample run on the app

![Input](input.JPG?raw=true "Example of using the app")
![Input](Googlechart.JPG?raw=true "Sample result chart")
![Input](wordcloud.JPG?raw=true "Sample result wordcloud")

