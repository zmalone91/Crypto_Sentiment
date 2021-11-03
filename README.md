Cryptocurrency Comparison and Sentiment Analysis Tool

Project Overview:
* Created a web app using python dash to compare prices between two cryptocurrencies side-by-side and simultaneously search tweets about the cryptocurrencies and perform a basic negative/positive sentiment analysis.
* Dash web application houses the data and includes a dropdown list of all current products available on Coinbase Pro that have a USD trading pair.
* Selecting cryptocurrencies from the dropdown lists automatically updates the price chart and tweet sentiment analysis.
* The tool dynamically brings in 24 hours worth of historical data using the Coinbase Pro API python library cbpro.
* Using tweepy, tool dynamically brings in the most recent 100 tweets and who tweeted, their follower count, and the Positive/Neutral/Negative sentiment analysis of their tweet using TextBlob.



**Python Version** 3.6.8
**Packages** pandas, numpy, re, matplotlib, datetime, plotly, dash, dash_bootstrap_components, tweepy, textblob, wordcloud, cbpro
**Accessing Twitter API** https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api
**Coinbase Pro API** - https://github.com/danpaquin/coinbasepro-python
**Tweepy documentation** - https://docs.tweepy.org/en/latest/
**Twitter Sentiment Analysis** - 'Computer Science' youtube channel - https://www.youtube.com/watch?v=ujId4ipkBio 
**Dash/Plotly Web App** - 'Charming Data' youtube channel - https://www.youtube.com/watch?v=hSPmj7mK6ng&list=LL&index=17&t=1553s 
**Dash bootstrap components** - https://dash-bootstrap-components.opensource.faculty.ai/ 
**Boostrap 4 Cheat Sheet** - https://hackerthemes.com/bootstrap-cheatsheet/#align-baseline
**Bootstrap themes** - https://www.bootstrapcdn.com/bootswatch/
