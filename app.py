import requests
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.io as poi
poi.renderers.default = 'browser'
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

""" Read data """

response = requests.get('http://asterank.com/api/kepler?query={}&limit=2000')
df = pd.json_normalize(response.json())
df = df[df['PER'] > 0]

# creating Star size category

bins = [0, 0.8, 1.2, 100]
names = ['smaller', 'similar', 'bigger']
df['star_size'] = pd.cut(df['RSTAR'], bins, labels = names)

star_size_selector = dcc.Dropdown(
	id = 'star_selector',
	options = [{'label' : 'smaller', 'value':'smaller'},
				{'label' : 'similar', 'value' : 'similar'},
				{'label' : 'bigger', 'value' : 'bigger'}],
	value = ['smaller', 'similar', 'bigger'],
	multi = True

	)

# Temperature Bins
tp_bins = [0, 200, 400, 500, 5000]
tp_labels = ['low', 'optimal', 'high', 'extreme']
df['temp'] = pd.cut(df['TPLANET'], tp_bins, labels = tp_labels)

# Size bins
rp_bins = [0, 0.5, 2, 4, 100]
rp_labels = ['low', 'optimal', 'high', 'extreme']
df['gravity'] = pd.cut(df['RPLANET'], rp_bins, labels = rp_labels)

# Creating Planet category 

df['planet_suitability'] = np.where((df['temp'] == 'optimal') &
					  (df['gravity'] == 'optimal'),
					  'promising', None)

df.loc[:, 'planet_suitability'] = np.where((df['temp'] == 'optimal') &
					  (df['gravity'].isin(['low', 'high'])),
					  'challenging', df['planet_suitability'])

df.loc[:, 'planet_suitability'] = np.where((df['gravity'] == 'optimal') &
					  (df['temp'].isin(['low', 'high'])),
					  'challenging', df['planet_suitability'])

df['planet_suitability'] = df.planet_suitability.fillna('extreme')

# Creating radius filter

rplanet_selector = dcc.RangeSlider(
	id = 'slider',
	min = df.RPLANET.min(),
	max = df.RPLANET.max(),
	marks = {10 : '10', 20 : '20', 30 : '30', 40 : '40', 50 : '50', 60 : '60', 70 : '70'},
	step = 1,
	value = [0, 50]

	)


app = dash.Dash(__name__,
				external_stylesheets = [dbc.themes.SOLAR])

""" LayOut """

app.layout = html.Div([
	# header
	dbc.Row(html.H1('NASA\'s Kepler Project dash'),
			style = {'margin-bottom':40}),
	# filters
	dbc.Row([
		dbc.Col([
			html.Div('Select planetary radius'),
			html.Br(),
			html.Div(rplanet_selector, style = {'width':'300px'}),
			html.Br()
			],
				width = {'size':2}),
		dbc.Col([
			html.Div('Select star size (compared to Sun)'),
			html.Br(),
			html.Div(star_size_selector),
			],
				width = {'size':3, 'offset':2}),
			dbc.Col(dbc.Button('Apply', id = 'submit', n_clicks=0, 
								className = 'mr-2'))

		], style = {'margin-bottom':40}),
	# Plots
	dbc.Row([
		dbc.Col([
			html.Div(id = 'dist_temp_plot')	
			],
				width = {'size':6}),
		dbc.Col([
			html.Div(id = 'coordinates_plot')
			],
				width = {'size':6})
		], style = {'margin-bottom':40})
	],
style = {'margin-left' : '80px', 
         'margin-right' : '80px'})


""" Callbacks"""


@app.callback(
	Output(component_id = 'dist_temp_plot', component_property = 'children'),
	Output(component_id = 'coordinates_plot', component_property = 'children'),
	[Input(component_id = 'submit', component_property = 'n_clicks')],
	[State(component_id = 'slider', component_property = 'value'),
	 State(component_id = 'star_selector', component_property = 'value')]
)

def update_plot(n, radius_range, star_size):
	data = df[(df['RPLANET'] > radius_range[0]) &
	 			(df['RPLANET'] < radius_range[1]) &
	 			(df['star_size'].isin(star_size))]

	if len(data) == 0:
	 	return html.Div('Please select parameters'), html.Div()

	fig1 = px.scatter(data, x = 'TPLANET', y = 'A', color = 'star_size')

	html1 = [html.Div('Dependence of the planet\'s distance from its star and temperature (k)'),
			dcc.Graph(figure = fig1)]
	
	fig2 = px.scatter(data, x = 'RA', y = 'DEC', size = 'RPLANET', color = 'planet_suitability')

	html2 = [html.Div('Coordinates on the Celestial Sphere and planet category (compared to Earth\'s gravity and temperature)'),
			dcc.Graph(figure = fig2)]

	return html1, html2


if __name__ == '__main__':
	app.run_server(debug=True)