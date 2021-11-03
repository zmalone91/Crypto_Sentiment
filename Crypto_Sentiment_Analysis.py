# Import general libraries
import pandas as pd 
import numpy as np 
import re
import matplotlib.pyplot as plt 
from datetime import datetime, date

# Import Dash components
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from dash import dash_table as dt
import dash_bootstrap_components as dbc
import plotly.express as px

# Import Twitter API Sentiment Analysis components
import tweepy
from tweepy import Stream
from textblob import TextBlob
from wordcloud import WordCloud
# Saved API keys in twitter_keys.py module in site-packages folder
from twitter_keys import consumer_key, consumer_secret, access_token, access_token_secret
# Create authentication object using OAuth 2
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# Set the access token and access token secret
auth.set_access_token(access_token, access_token_secret)
# Create API object and pass in auth information
api = tweepy.API(auth, wait_on_rate_limit=True)

# Import Coinbase Pro API
import cbpro
cb = cbpro.PublicClient()
# Create a list of all current products with a USD trading pair to feed app dropdown lists
products = pd.DataFrame(cb.get_products())
cb_symbols = products[products['quote_currency']=='USD']['id'].tolist()




# Create a df to house the cryptocurrency symbols with a USD trading pair

df = pd.DataFrame(cb_symbols, columns=['Symbol']) 

# Dash Web App
# To view app, run .py file and build Dash app
# Navigate to local port http://127.0.0.1:8050/ in web browser to view the app

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY])

app.layout = dbc.Container([
	dbc.Row([
		dbc.Col(html.H1('Crypto Sentiment Analysis',
			className='text-center text-primary mb-4'),
			width=12)
	]),

	dbc.Row([
		dbc.Col([
			dcc.Dropdown(id='my-dropdown', multi=False, value='SHIB-USD',
						options=[{'label':x, 'value':x}
						for x in sorted(df['Symbol'].unique())])
		],width={'size':6}),
		dbc.Col([
			dcc.Dropdown(id='my-dropdown-2', multi=False, value='DOGE-USD',
						options=[{'label':x, 'value':x}
						for x in sorted(df['Symbol'].unique())])	
		],width={'size':6})	
	]),

	dbc.Row([
		dbc.Col([
			html.Div(id='output-graph')], width={'size':6}),
		dbc.Col([
			html.Div(id='output-graph-2')], width={'size':6})
	]),

	dbc.Row([
		dbc.Col([
			html.Div(id='output-table', className='table table-bordered table-primary')],
			width={'size':6}),
		dbc.Col([
			html.Div(id='output-table-2', className='table table-bordered table-primary')],
			width={'size':6})
	])

], fluid=True)


@app.callback(
	Output(component_id='output-graph', component_property='children'),
	Input(component_id='my-dropdown', component_property='value')
)
def update_graph(input_data):
	
	df_2 = pd.DataFrame(cb.get_product_historic_rates(product_id=input_data))
	df_2.columns= ['Date','Open','High','Low','Close','Volume']
	df_2['Date']= pd.to_datetime(df_2['Date'], unit='s')
	df_2.set_index('Date', inplace=True)
	df_2.sort_values(by='Date', ascending=True, inplace=True)
	try:
		return dcc.Graph(id='example-graph',
				figure ={
					'data': [
						{'x':df_2.index, 'y':df_2.Close, 'type':'line', 'name': input_data}
						],
					'layout' : {
						'title':input_data
						}
				})
	except:
		return "Type in a valid stock ticker"

@app.callback(
	Output(component_id='output-graph-2', component_property='children'),
	Input(component_id='my-dropdown-2', component_property='value')
)
def update_graph(input_data):
	
	df_3 = pd.DataFrame(cb.get_product_historic_rates(product_id=input_data))
	df_3.columns= ['Date','Open','High','Low','Close','Volume']
	df_3['Date']= pd.to_datetime(df_3['Date'], unit='s')
	df_3.set_index('Date', inplace=True)
	df_3.sort_values(by='Date', ascending=True, inplace=True)
	try:
		return dcc.Graph(id='example-graph',
				figure ={
					'data': [
						{'x':df_3.index, 'y':df_3.Close, 'type':'line', 'name': input_data}
						],
					'layout' : {
						'title':input_data
						}
				})
	except:
		return "Type in a valid stock ticker"
	
@app.callback(
	Output(component_id='output-table', component_property='children'),
	Input(component_id='my-dropdown', component_property='value')
)	
def get_Tweets(input_data):
	# Collect Twitter Data

	search_words = ['$' + input_data[:len(input_data)-4]]

	tweets = api.search_tweets(q=search_words, count=15)

	twt_df = pd.DataFrame( [(tweet.id, tweet.text, api.get_status(tweet.id).created_at, tweet.user.screen_name, tweet.user.followers_count, tweet.user.friends_count, tweet.user.verified) for tweet in tweets], columns=['Tweet_ID', 'Tweet_Text', 'Created', 'Screen_Name', 'Followers', 'Following', 'Verified'] )

	# Create a function to identify the day of the week
	def weekDay(created):
	    i = created.weekday()
	    if i == 0:
	        return 'Sunday'
	    elif i == 1:
	        return 'Monday'
	    elif i == 2:
	        return 'Tuesday'
	    elif i == 3:
	        return 'Wednesday'
	    elif i == 4:
	        return 'Thursday'
	    elif i == 5:
	        return 'Friday'
	    else:
	        return 'Saturday' 

	twt_df['Day'] = twt_df['Created'].apply(weekDay)

	# Clean text using RegEx

	def cleanText(text):
	    text = re.sub(r'@[A-Za-z0-9_]+', '', text)
	    text = re.sub(r'#', '', text)
	    text = re.sub(r'RT[\s]+', '', text)
	    text = re.sub(r'https?:\/\/\S+', '', text)
	    text = re.sub(r':', '', text)
	    
	    return text

	twt_df['Tweet_Text'] = twt_df['Tweet_Text'].apply(cleanText)

	# Create a function to bring in the subjectivity

	def getSubjectivity(text):
	    return TextBlob(text).sentiment.subjectivity

	def getPolarity(text):
	    return TextBlob(text).sentiment.polarity

	# Create two new columns, Subjectivity and Polarity

	twt_df['Subjectivity'] = twt_df['Tweet_Text'].apply(getSubjectivity)

	twt_df['Polarity'] = twt_df['Tweet_Text'].apply(getPolarity)


	# Create a function to determine positive, negative, and neutral analysis

	def getAnalysis(score):
	    if score < 0:
	        return 'Negative'
	    elif score == 0:
	        return 'Neutral'
	    else:
	        return 'Positive'

	twt_df['Analysis'] = twt_df['Polarity'].apply(getAnalysis)

	twt_df = twt_df[['Analysis','Tweet_Text','Screen_Name', 'Followers']].sort_values(by=['Followers'],ascending=False)

	# Create final df before table creation function
	def generate_table(dataframe, max_rows=10):
	    return html.Table([
	        html.Thead(
	            html.Tr([html.Th(col) for col in dataframe.columns]),
	            style={'text-align':'center'}
	        ),
	        html.Tbody([
	            html.Tr([
	                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
	            ]) for i in range(min(len(dataframe), max_rows))
	        ])
	    ])

	return generate_table(twt_df)

# The code for the callback functions (chart and tweets) repeats for each column, if the user wishes to make changes to the search style, # of tweets, etc.

@app.callback(
	Output(component_id='output-table-2', component_property='children'),
	Input(component_id='my-dropdown-2', component_property='value')
)	
def get_Tweets(input_data):
	# Collect Twitter Data

	search_words = ['$' + input_data[:len(input_data)-4]]

	tweets = api.search_tweets(q=search_words, count=15)

	twt_df = pd.DataFrame( [(tweet.id, tweet.text, api.get_status(tweet.id).created_at, tweet.user.screen_name, tweet.user.followers_count, tweet.user.friends_count, tweet.user.verified) for tweet in tweets], columns=['Tweet_ID', 'Tweet_Text', 'Created', 'Screen_Name', 'Followers', 'Following', 'Verified'] )

	# Create a function to identify the day of the week
	def weekDay(created):
	    i = created.weekday()
	    if i == 0:
	        return 'Sunday'
	    elif i == 1:
	        return 'Monday'
	    elif i == 2:
	        return 'Tuesday'
	    elif i == 3:
	        return 'Wednesday'
	    elif i == 4:
	        return 'Thursday'
	    elif i == 5:
	        return 'Friday'
	    else:
	        return 'Saturday' 

	twt_df['Day'] = twt_df['Created'].apply(weekDay)

	# Clean text using RegEx

	def cleanText(text):
	    text = re.sub(r'@[A-Za-z0-9_]+', '', text)
	    text = re.sub(r'#', '', text)
	    text = re.sub(r'RT[\s]+', '', text)
	    text = re.sub(r'https?:\/\/\S+', '', text)
	    text = re.sub(r':', '', text)
	    
	    return text

	twt_df['Tweet_Text'] = twt_df['Tweet_Text'].apply(cleanText)

	# Create a function to bring in the subjectivity

	def getSubjectivity(text):
	    return TextBlob(text).sentiment.subjectivity

	def getPolarity(text):
	    return TextBlob(text).sentiment.polarity

	# Create two new columns, Subjectivity and Polarity

	twt_df['Subjectivity'] = twt_df['Tweet_Text'].apply(getSubjectivity)

	twt_df['Polarity'] = twt_df['Tweet_Text'].apply(getPolarity)


	# Create a function to determine positive, negative, and neutral analysis

	def getAnalysis(score):
	    if score < 0:
	        return 'Negative'
	    elif score == 0:
	        return 'Neutral'
	    else:
	        return 'Positive'

	twt_df['Analysis'] = twt_df['Polarity'].apply(getAnalysis)

	# Create final df before table creation function
	twt_df = twt_df[['Analysis','Tweet_Text','Screen_Name', 'Followers']].sort_values(by=['Followers'],ascending=False)

	def generate_table(dataframe, max_rows=10):
	    return html.Table([
	        html.Thead(
	            html.Tr([html.Th(col) for col in dataframe.columns]),
	            style={'text-align':'center'}
	        ),
	        html.Tbody([
	            html.Tr([
	                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
	            ]) for i in range(min(len(dataframe), max_rows))
	        ])
	    ], )

	return generate_table(twt_df)

if __name__ == '__main__':
	app.run_server(debug=True)

