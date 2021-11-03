<h3># Cryptocurrency Comparison and Sentiment Analysis Tool: Project Overview</h3> <br>
* Created a web app using python dash to compare prices between two cryptocurrencies side-by-side and simultaneously search tweets about the cryptocurrencies to perform a basic negative/positive sentiment analysis.<br>
* The purpose of the app is to assist in short-term trading strategy by getting a feel of the most recent price trends and feelings on Twitter. <br>
* Dash web application houses the data and includes a dropdown list of all current products available on Coinbase Pro that have a USD trading pair.<br>
* Selecting cryptocurrencies from the dropdown lists automatically updates the price chart and tweet sentiment analysis.<br>
* The tool dynamically brings in 24 hours worth of historical data using the Coinbase Pro API python library cbpro.<br>
* Using tweepy, tool dynamically brings in the most recent 100 tweets and who tweeted, their follower count, and the Positive/Neutral/Negative sentiment analysis of their tweet using TextBlob.<br>
<br>
<br>
**Python Version** 3.6.8 <br>
**Packages** pandas, numpy, re, matplotlib, datetime, plotly, dash, dash_bootstrap_components, tweepy, textblob, wordcloud, cbpro <br>
**Accessing Twitter API** https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api <br>
**Coinbase Pro API** - https://github.com/danpaquin/coinbasepro-python <br>
**Tweepy documentation** - https://docs.tweepy.org/en/latest/ <br>
**Twitter Sentiment Analysis** - 'Computer Science' youtube channel - https://www.youtube.com/watch?v=ujId4ipkBio <br>
**Dash/Plotly Web App** - 'Charming Data' youtube channel - https://www.youtube.com/watch?v=hSPmj7mK6ng&list=LL&index=17&t=1553s <br>
**Dash bootstrap components** - https://dash-bootstrap-components.opensource.faculty.ai/ <br>
**Boostrap 4 Cheat Sheet** - https://hackerthemes.com/bootstrap-cheatsheet/#align-baseline <br>
**Bootstrap themes** - https://www.bootstrapcdn.com/bootswatch/ <br>
