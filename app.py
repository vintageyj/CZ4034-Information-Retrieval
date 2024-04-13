import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
from indexers import LeaderIndexer
from encoders import TermFrequencyEncoder
from retrievers import BaseRetriever
from enums import EncoderType, IndexerType
import time
import plotly.graph_objs as go
import plotly.express as px
import dash_bootstrap_components as dbc
from datetime import datetime
from spellchecker import SpellChecker

from retrievers import ElasticRetriever

ELASTIC_PWD = 'changeme'

data_path = "data/location.csv"

indexer_type = IndexerType("ElasticSearchIndexer")
index_name = "location"

start_indexing = time.time()
retriever = ElasticRetriever(indexer_type, data_path, elastic_pwd=ELASTIC_PWD, index_name = index_name, fresh_instance = True) # fresh_instance = True to delete existing index and create a new index
end_indexing = time.time()
print(f"Building of Index: time taken for indexing: {end_indexing - start_indexing}s")

global df_raw
global country_name
country_name=None

df_raw = pd.read_csv("data/new_sg_companies_reviews_UID.csv")
df = pd.read_csv("data/location.csv")

# For use in dropdown lists for Company Name and Location
unique_companies = df_raw['Company Name'].unique()
unique_locations = df_raw['Location'].unique()

# Initialization of date slider
init_min_date = pd.to_datetime(df_raw['Review Date'].min())
init_max_date = pd.to_datetime(df_raw['Review Date'].max())

# Creating key:value pairs for slider marking. marks = {int: datetime, int: datetime, ...} where int is used to index and datetime is displayed on UI
# Indexing of string (str(i[:10])) is done as each TimeStamp is represetned as "YYYY-MM-DDT00:00:00" => in order to get rid of the timestamp at the tail
init_marks = {int(i.timestamp()): str(i)[:10] for i in pd.date_range(init_min_date, init_max_date, freq = 'Y')}
init_marks[int(init_min_date.timestamp())] = str(init_min_date)[:10]
init_marks[int(init_max_date.timestamp())] = str(init_max_date)[:10]

# For debugging ----------------------------------------------------------
print('-'*100)
print("init_min_date", init_min_date, type(init_min_date))
print('-'*100)
print("init_max_date", init_max_date, type(init_max_date))    
print('-'*100)
print(init_marks)
print('-'*100)
# For debugging ----------------------------------------------------------


######################################################################################################################################################################################################
map_df = px.data.gapminder().query("year==2007")
continent_colors = {'Asia': '#52688F', 'Europe': '#ddf2fd', 'Africa': '#9ac0cd', 'Americas': '#BBC8DE', 'Oceania': '#427d9d'}
map_df['continent_color'] = map_df['continent'].map(continent_colors)

fig = go.Figure()

for continent, color in continent_colors.items():
    fig.add_trace(go.Choropleth(
        locations=map_df[map_df['continent'] == continent]['iso_alpha'],
        z=[1]*len(map_df[map_df['continent'] == continent]),
        text=map_df[map_df['continent'] == continent]['country'],
        hoverinfo='text',
        showscale=False,
        name=continent,
        marker_line_color='rgba(0,0,0,0)',
        marker_line_width=0.5,
        autocolorscale=False,
        colorscale=[[0, color], [1, color]],
    ))

fig.update_geos(projection_type="equirectangular", bgcolor='rgba(0,0,0,0)', showcountries=True, countrycolor="white", lakecolor='black')
fig.update_layout(margin={"r":0, "t":0, "l":0, "b":0},paper_bgcolor='rgba(0,0,0,0)', geo_bgcolor='rgba(0,0,0,0)')

######################################################################################################################################################################################################


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY],prevent_initial_callbacks="intial_duplicate")

button_style_unclicked={'display': 'inline-block','height': '200px','margin':'5px','background-color':'#303030','border-color':'transparent'}
button_style_clicked={'display': 'inline-block','height': '200px','margin':'5px','background-color':'#444444','border-color':'transparent'}


def get_review_highlight(relevant_rows, row):
    positions=eval(relevant_rows.iloc[row]['position'])
    sentiments=eval(relevant_rows.iloc[row]['sentiment'])

    pos_to_sentiment = {}
    for pos_list, sentiment in zip(positions, sentiments):
        for pos in pos_list:
            pos_to_sentiment[pos] = sentiment

    text=relevant_rows.iloc[row]['Overall Review with Title']
    words = text.split()
    def get_style(index):
        sentiment = pos_to_sentiment.get(index)
        if sentiment == 'Positive':
            return {"background-color": "lightgreen",'color':'black'}
        elif sentiment == 'Negative':
            return {"background-color": "lightcoral",'color':'black'}
        elif sentiment == 'Neutral':
            return {"background-color": "yellow",'color':'black'}
        else:
            return {}
    
    highlighted_text_parts = []

    # Split the text based on "//" and apply highlighting to each part separately
    for part in text.split('//'):
        part_words = part.split()
        highlighted_part = [html.Span(word + " ", style=get_style(index)) for index, word in enumerate(part_words)]
        highlighted_text_parts.append(highlighted_part)

    return highlighted_text_parts


######################################################################################################################################################################################################

def generate_search_card(button_clicked, page, relevant_rows):
    if not page: page=1
    titles = ["Company Name", "Job Title", "Review Date", "Job Details", "Location"]

    row=int(button_clicked)+ 5*(page - 1)
    card_content = []
    for title in titles:
        card_content.append(html.H6(title, className="card-subtitle mb-2 text-muted"))
        card_content.append(html.P(relevant_rows.iloc[row][title], className="card-text"))
    
    rating=int(float(relevant_rows.iloc[row]['Overall Rating']))

    card=dbc.Card(
            [
                dbc.CardHeader(html.H5("Job Review", className="card-title")),
                dbc.CardBody(
                    [
                        html.H6('Review Title', className="card-subtitle mb-2 text-muted"),
                        html.P(get_review_highlight(relevant_rows, row)[0])
                    ]+
                    card_content+
                    [
                        html.Hr(),
                        html.H6("Review", className="card-subtitle mb-2 text-muted"),
                        html.Ul([html.Li(get_review_highlight(relevant_rows, row)[1])],style={'maxHeight': '300px','overflowY': 'scroll'}),
                        html.Hr(),
                        html.H6("Overall Rating", className="card-subtitle mb-2 text-muted"),
                        html.H1(str(rating)+'/5', className="card-text")
                    ]
                ),
            ],
            style={"width": "100%",'height':'1040px','margin':'5px'},
        )
    return card


app.layout = html.Div([
    dbc.Navbar(
        dbc.Container(
            [
                dbc.NavbarBrand("CZ4034 Group 31", href="#"),
                dbc.Nav(
                    [
                        dbc.NavItem(dbc.NavLink("Home", href="#")),
                        dbc.NavItem(dbc.NavLink("About", href="#")),
                        dbc.NavItem(dbc.NavLink("Contact", href="#")),
                    ],className="ml-auto", navbar=True,
            )]
        ),color="dark", dark=True,
    ),

    html.Div([
        html.H1("Job Retrieval Information System", style={'margin-top': '70px', 'color': 'white', 'textAlign': 'center'}),  # System name
    ]),

    dbc.Row([
        dbc.Col(dbc.Input(id='query-input', type='text', placeholder='Enter your query...', value='',style={'margin': '5px', 'width': '100%'}), width=5),
        dbc.Col(dbc.Input(id='job-title-input', type='text', placeholder='All Job Titles', value='',style={'margin': '5px', 'width': '100%'}), width=3),
        dbc.Col(dcc.Dropdown(id='company-name-dropdown',options=[{'label': company, 'value': company} for company in unique_companies],placeholder='All Companies',multi=True,style={'margin': '5px', 'width': '100%', 'color': 'black'} ), width=3),
        dbc.Col(dbc.Button("Search", id="search-button", n_clicks=0,style={'margin': '5px', 'width': '100%'}), width=1),
        dbc.Col(dbc.Button("Show Filters", id="filter-show", n_clicks=0,style={'margin': '5px', 'width': '100%', 'background-color':'#303030', 'border-color':'#303030'}), width=6),
        dbc.Col(dbc.Button("Apply Filters", id="filter-apply", n_clicks=0,style={'margin': '5px', 'width': '100%', 'background-color':'#303030', 'border-color':'#303030'}), width=6),
    ], style={'padding': '50px','padding-bottom': '0px','justify-content': 'center'}),
    
    dbc.Row([
        dbc.Col(html.Div(id='spell-corrected-query'), width=12)
    ]),

    dbc.Container([
        dbc.Card([
            dbc.CardHeader("Filter Options", className="text-center"),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col(html.Div([html.H6("Filter by Location", className="text-center")]), width=12),
                ]),

                dbc.Row([
                    dbc.Col(dbc.Container([
                        dcc.Graph(id='world-map', figure=fig),
                    ], fluid=True), width=12),
                ]),

                dbc.Row([
                    dbc.Col(html.Div([html.H6("Filter by Date", className="text-center")],style={'margin-top':'20px'}), width=12),
                ]),

                dbc.Row(id='date-range-slider-outer-row', 
                    children=[
                        dbc.Col(dcc.RangeSlider(
                            id='date-range-slider',
                            marks=init_marks,
                            min=int(init_min_date.timestamp()),
                            max=int(init_max_date.timestamp()),
                            value=[int(init_min_date.timestamp()), int(init_max_date.timestamp())],
                            step=None,
                            allowCross=False,
                        ), width=12)
                    ],
                ),
            ]),
        ], style={'background-color':'#303030'}),
    ], fluid=True, id='filter-options', style={"display": "none"}),

    dbc.Row([
        dbc.Col(html.Div(id='query-runtime', style={'margin-top':'20px'}), width=12)
    ]),
    
    dbc.Row([
        dbc.Container([
            dbc.Card([
                dbc.CardHeader("Search Results", className="text-center"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col(html.Div([dcc.Graph(id='fig-predicted-sentiment', style={'display': 'none'})]), md=6),
                        dbc.Col(html.Div([dcc.Graph(id='fig-overall-rating', style={'display': 'none'})]), md=6)
                    ], style={'padding': '20px'})  # Adjusted padding to better fit within the card
                ])
            ], className="mb-3"),  # Added margin-bottom for spacing if needed
        ], fluid=True, id="visualizations", style={"display": "none"})
    ], style = {'padding': '45px', 'padding-bottom':'0px'}),    
    
    dbc.Row([
        dbc.Col([dbc.Row(dbc.Button("", id=f"button-{i+1}", style={'display':'none'})) for i in range(5)], width=6),
        dbc.Col([dbc.Row(html.Div(id='display-info'))],width=6),
    ], style={'padding': '50px', 'padding-top':'0px', 'padding-bottom':'10px'}),

    dbc.Pagination(id='pages',max_value=5, first_last=True, previous_next=True,className="custom-pagination",
        style={'display':'none'}),
])

@app.callback(
    Output('world-map', 'figure'),
    [Input('world-map', 'clickData')],
    [dash.dependencies.State('world-map', 'figure')]
)
def highlight_country(clickData, figure):
    if clickData:
        iso_code = clickData['points'][0]['location']
        country_name = clickData['points'][0]['text']
        print(f"Country selected: {country_name}")  # Print the name of the selected country in the terminal
        
        # Re-create the figure to reset previously clicked countries
        new_fig = go.Figure()

        # Add all countries with continent-based colors
        for continent, color in continent_colors.items():
            new_fig.add_trace(go.Choropleth(
                locations=map_df[map_df['continent'] == continent]['iso_alpha'],
                z=[1]*len(map_df[map_df['continent'] == continent]),  # Dummy value for uniform color
                text=map_df[map_df['continent'] == continent]['country'],
                hoverinfo='text',
                showscale=False,
                name=continent,
                marker_line_color='rgba(0,0,0,0)',
                marker_line_width=0.5,
                autocolorscale=False,
                colorscale=[[0, color], [1, color]],
            ))
        
        new_fig.add_trace(go.Choropleth(
            locations=[iso_code],
            z=[2], 
            text=[country_name],
            hoverinfo='text',
            showscale=False,
            autocolorscale=False,
            colorscale=[[0, '#591ee3'], [1, '#591ee3']],
            marker_line_color='rgba(0,0,0,0)',
            marker_line_width=1,
        ))

        new_fig.update_geos(projection_type="equirectangular", bgcolor='rgba(0,0,0,0)', showcountries=True, countrycolor="white", lakecolor='black')
        new_fig.update_layout(margin={"r":0, "t":0, "l":0, "b":0}, paper_bgcolor='rgba(0,0,0,0)', geo_bgcolor='rgba(0,0,0,0)')
        
        return new_fig
    else:
        raise dash.exceptions.PreventUpdate
    
@app.callback(
    [Output("filter-options", "style"),
     Output("filter-show", "children")],
    [Input("filter-show", "n_clicks")],
    [dash.dependencies.State('query-input', 'value')]
)
def toggle_filters_visibility(n_clicks,query):
    if query and (n_clicks % 2 == 0) or not query:  # If even, hide the container
        return [{"display": "none", 'padding':'50px'}, "Show Filters"]
    else:  # If odd, show the container
        return [{"display": "block", 'padding':'50px'}, "Hide Filters"]

@app.callback(
    
    [Output("filter-options", "style",allow_duplicate=True),
     Output("filter-show", "children",allow_duplicate=True),
     Output('visualizations','style'),
     Output('fig-overall-rating', 'figure'),
     Output('fig-predicted-sentiment', 'figure')]+
    # Date Range Slider update
    [Output('date-range-slider', 'marks')]+
    [Output('date-range-slider', 'min')]+
    [Output('date-range-slider', 'max')]+
    
    [Output('query-runtime', 'children')]+
    [Output('display-info', 'children')]+
    [Output(f"button-{i+1}",'children') for i in range(5)]+
    [Output(f"button-{i+1}",'style') for i in range(5)]+
    [Output('pages','style')],
    
    # Date Range Slider Update  
    [dash.dependencies.State('company-name-dropdown', 'value')],
    [dash.dependencies.State('date-range-slider', 'value')],
    
    [Input('search-button', 'n_clicks'),
     Input('pages', 'active_page'),
     Input("filter-apply", "n_clicks")],
    [dash.dependencies.State('query-input', 'value'),
     dash.dependencies.State('job-title-input', 'value'),
     dash.dependencies.State('pages', 'active_page'),]
)
def update_results(selected_companies, selected_dates, n_clicks, page_click, apply_click, query, job_titles, page):
    
    # Condition 1: n_clicks > 0 - Require click to search
    # Condition 2: query - Require query to be non-empty for results to appear
    if (n_clicks > 0 or page_click or apply_click>0) and query : 
        # Querying start timer 
        start_time = time.time()

        #..........................................................................................................................................................
        #..........................................................................................................................................................
        

        print(selected_dates) # For debugging
        
        # Input values from date slider are returned as a list: [start_date, end_date]
        start_date = selected_dates[0]
        end_date = selected_dates[1]

        date_datetime = datetime.utcfromtimestamp(start_date)
        formatted_start_date = date_datetime.strftime('%Y-%m-%d')
        
        date_datetime = datetime.utcfromtimestamp(end_date)
        formatted_end_date = date_datetime.strftime('%Y-%m-%d')
        
        if job_titles:
            query_dict = {'Overall Review with Title': query, 
                        'Job Title': job_titles, 
                        'Review Date': f'{formatted_start_date}|{formatted_end_date}',
                        }
        else:
            query_dict = {'Overall Review with Title': query, 
                        'Review Date': f'{formatted_start_date}|{formatted_end_date}',
                        }
        
        start_retrieving = time.time()
        results = retriever.retrieve_results(query_dict, pagination=(0,10000), operator="must")
        end_retrieving = time.time()
        print(f"time taken for retrieval: {end_retrieving - start_retrieving}s")
        # The first element of the list is the total number of hits
        print("Total Hits: ", results[0])
        # The second element of the list is the dataframe of the results
        results = results[1]
        print(results.columns)
        # min and max date should be post-company-filtering min and max dates
        min_date = pd.to_datetime(results['Review Date'].min())
        max_date = pd.to_datetime(results['Review Date'].max())
        date_range = pd.date_range(min_date, max_date, freq = 'D')
        num_ticks = 10
        marks = {int(date_range[i].timestamp()): str(date_range[i])[:10] for i in range(0, len(date_range)-1, int((len(date_range)-1)/num_ticks))}
        
        #..........................................................................................................................................................
        #..........................................................................................................................................................

        # Calculate querying time in ms
        time_taken = round((time.time() - start_time) * 1000, 5)
        
        global relevant_rows
        relevant_rows = results

        # Filter based on selected companies
        if selected_companies: 
            filtered_rows=relevant_rows[relevant_rows['Company Name'].isin(selected_companies)]
            if len(filtered_rows)>25: relevant_rows=filtered_rows
        # Filter based on country
        if country_name!=None: 
            filtered_rows=relevant_rows[relevant_rows['Country']==country_name]
            if len(filtered_rows)>25: relevant_rows=filtered_rows
        
        # There was a need to convert the entire df['Review Title'] into pd.TimeStamp for the date slider to work
        # The following step is done as the Review Date is displayed as "2024-02-12T00:00:00" in the output.
        relevant_rows['Review Date'] = relevant_rows['Review Date'].apply(lambda x: str(x)[:10])

        results_display=[]

        if not page: page=1
        for i in range(5*(page-1),5*(page)):
            results_display.append(
                html.Div([
                    html.H4(relevant_rows.iloc[i]['Company Name'] + ' | '+ relevant_rows.iloc[i]['Job Title']), 
                    html.H5(relevant_rows.iloc[i]['Job Details']),
                    html.P(relevant_rows.iloc[i]['Review Title'])
                ])
            )
        card=generate_search_card(0, page, relevant_rows)


        sentiment_counts = relevant_rows['Predicted Sentiment'].value_counts()
        sentiment_data = pd.DataFrame({
            'Sentiment': sentiment_counts.index,
            'Count': sentiment_counts.values
        })
        
        # Calculate percentage of Pos/Neg
        sentiment_data['Percentage'] = (sentiment_data['Count'] / sentiment_data['Count'].sum()) * 100
        
        # Donut chart for 'Predicted Sentiment'
        fig_predicted_sentiment = px.pie(sentiment_data, values='Percentage', names='Sentiment', hole=0.5, 
                                        title=f'Predicted Sentiment Distribution (N = {len(relevant_rows)})',
                                        color_discrete_sequence=['yellowgreen', 'lightcoral'],
                                        hover_data=['Count'])
        fig_predicted_sentiment.update_layout(font=dict(color='#FFFFFF'), paper_bgcolor='rgba(0,0,0,0)')
        

        # Histogram for 'Overall Rating'
        bin_colors = ['#D01110', '#F6A21E', '#F7DA42', '#478C5C', '#104210']  # Lighter red/orange, light green are adjusted

        # Create a list of bin counts for ratings 1 to 5
        relevant_rows['Overall Rating'] = relevant_rows['Overall Rating'].astype(float).astype(int)
        bin_counts = [relevant_rows['Overall Rating'].tolist().count(i) for i in range(1, 6)]

        # Create an empty figure
        fig_overall_rating = go.Figure(data=[
            go.Bar(
                x=[str(i) for i in range(1, 6)],  # X-axis categories (as strings for discrete bars)
                y=bin_counts,  # Y-axis values
                marker_color=bin_colors,  # Bar colors
                marker_line_color='rgba(0,0,0,0)' 
            )
        ])

        # Add a little space between the bars
        fig_overall_rating.update_traces(marker_line_width=1.5, marker_line_color='rgb(255, 255, 255)')

        # Update layout
        fig_overall_rating.update_layout(
            title='Overall Rating Distribution',
            font=dict(color='#FFFFFF'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title='Overall Rating'),
            yaxis=dict(title='Count'),
            bargap=0.05  # Space between bars
        )

        return [{"display": "none", 'padding':'50px'}, "Show Filters",{},fig_overall_rating,fig_predicted_sentiment]  + [marks] + [min_date.timestamp()]+ [max_date.timestamp()] + [html.Div(f"Querying Time: {time_taken} ms",style={'display': 'flex', 'justify-content': 'center'})]+[html.Div(card)]+results_display+[button_style_clicked]+([button_style_unclicked]*4)+[{'display':'flex', 'padding-left':'50px','padding-right':'50px','justify-content': 'center'}]
    return dash.no_update

@app.callback(
    Output('spell-corrected-query', 'children'),
    [Input('query-input', 'value')],
    [Input('search-button', 'n_clicks')]
)
def suggest_spell_correction(query, n_clicks):
    if n_clicks > 0:
        spell = SpellChecker()
        misspelled = spell.unknown(query.split())
        
        if misspelled:
            df = pd.DataFrame(query.split(), columns = ['Original'])
            df['Corrected'] = df['Original'].apply(lambda x: spell.correction(x))
            corrected = ""
            for word in df['Corrected'].values:
                corrected+=word
                corrected+=" "
    
            corrected = corrected[:len(corrected)-1]
            return html.Div(f"Did you mean: {corrected}",style={'display': 'flex', 'justify-content': 'center', 'padding': '50px'})
        else:
            return html.Div()

@app.callback(
    Output('fig-overall-rating', 'style'),
    Output('fig-predicted-sentiment', 'style'),
    Output('date-range-slider-outer-row', 'style'),
    [Input('search-button', 'n_clicks')]
)
def show_distribution_plot(n_clicks):
    if n_clicks:
        return {'display': 'block'}, {'display': 'block'}, {'padding': '50px', 'display': 'block'}  # Show plot when search button is clicked
    else:
        return {'display': 'none'}, {'display': 'none'}, {'padding': '50px', 'display': 'none'}  # Hide plot otherwise

@app.callback(
    [Output('display-info', 'children',allow_duplicate=True)]+
    [Output(f'button-{i+1}', 'style',allow_duplicate=True) for i in range(5)],
    [Input(f'button-{i+1}', 'n_clicks_timestamp') for i in range(5)],
    [dash.dependencies.State('pages', 'active_page')]
)

def display_results(b1,b2,b3,b4,b5,page):
    timestamps = {"0":b1, "1":b2, "2":b3, "3":b4, "4":b5}
    timestamps = {k: v for k, v in timestamps.items() if v is not None}
    if timestamps!={}:
        button_clicked=max(timestamps,key=timestamps.get)
        card=generate_search_card(button_clicked,page, relevant_rows)
        button_click_style=[button_style_unclicked]*5
        button_click_style[int(button_clicked)]=button_style_clicked

        return [html.Div(card)]+button_click_style
    return dash.no_update


######################################################################################################################################################################################################

if __name__ == '__main__':
    app.run_server(debug=True)

