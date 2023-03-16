import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

# incorporate data into app
import zipfile

zf = zipfile.ZipFile("/Users/nathan/Downloads/plays.csv.zip")
plays = pd.read_csv(zf.open("plays.csv"))

plays = plays.query(
        "pff_passCoverage == 'Cover-0' or pff_passCoverage == 'Cover-1' or pff_passCoverage == 'Cover-2' or pff_passCoverage == 'Cover-3' or pff_passCoverage == '2-Man'")




# Build your components
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])
app.layout = dbc.Container([

    dbc.Row(
        dbc.Col(html.H1("NFL Defensive Coverages Dashboard",
                        className='text-center text-primary mb-4'),
                width=12)
    ),

    dbc.Row([

        dbc.Col([
            dcc.Dropdown(id='my-dpd1', multi = True, options=[{'label': x, 'value': x}
                                  for x in sorted(plays['defensiveTeam'].unique())],
                         value=['TB','NO'],  # initial value displayed when page first loads
                         clearable=False),
            dcc.Graph(id = 'barfig1', figure={})
        ], width={'size':5, 'offset':1, 'order':1},
           xs=12, sm=12, md=12, lg=5, xl=5
        ),

        dbc.Col([
            dcc.Dropdown(id='my-dpdn2', multi=False, value='TB',
                         options=[{'label':x, 'value':x}
                                  for x in sorted(plays['defensiveTeam'].unique())],
                         clearable = False),
            dcc.Graph(id='barfig2', figure={})
        ], width={'size':5, 'offset':0, 'order':2},
           xs=12, sm=12, md=12, lg=5, xl=5
        ),

    ], justify='start'),

    dbc.Row([
            dbc.Col([
                html.P("Select Offense:",
                       style={"textDecoration": "underline"}),
                dcc.Dropdown(id='my-dpdn3', multi=False, value='TB',
                             options=[{'label': x, 'value': x}
                                      for x in sorted(plays['defensiveTeam'].unique())],
                             clearable=False),
                dcc.Graph(id='barfig3', figure={}),
            ], width={'size':8, 'offset':1},
               xs=12, sm=12, md=12, lg=8, xl=8
            ),
        ])

])

# Callback allows components to interact
@app.callback(
    Output('barfig1', component_property='figure'),
    Input('my-dpd1', component_property='value')
)
def update_graph(teamnames):  # function arguments come from the component property of the Input
    teams_cvg = plays.groupby(["defensiveTeam", "pff_passCoverage"]).size().to_frame().reset_index()

    teams_cvg = teams_cvg.rename(columns={0: 'plays'})
    teams_cvg1 = teams_cvg[teams_cvg['defensiveTeam'].isin(teamnames)]
    cvgbar1 =px.bar(
        data_frame=teams_cvg1,
        x='defensiveTeam',
        y="plays",
        color="pff_passCoverage",  # differentiate color of marks
        opacity=0.9,  # set opacity of markers (from 0 to 1)
        orientation="v",  # 'v','h': orientation of the marks
        barmode='group',
        template='seaborn')
    return cvgbar1

@app.callback(
    Output('barfig2', 'figure'),
    Input('my-dpdn2', 'value')
)
def update_graph(teamname):
    teams_cvg2 = plays.groupby(["defensiveTeam", "down", "pff_passCoverage"]).size().to_frame().reset_index()

    teams_cvg2 = teams_cvg2.rename(columns={0: 'plays'})

    teams_cvg3 = teams_cvg2[teams_cvg2['defensiveTeam'] == teamname]
    cvgbar2 = px.bar(
        data_frame=teams_cvg3,
        x='down',
        y="plays",
        color="pff_passCoverage",  # differentiate color of marks
        opacity=0.9,  # set opacity of markers (from 0 to 1)
        orientation="v",  # 'v','h': orientation of the marks
        barmode='group',
        template='seaborn')
    return cvgbar2

@app.callback(
    Output('barfig3', 'figure'),
    Input('my-dpdn3', 'value')
)

def update_graph(offense):
    teams_cvg4 = plays.groupby(["possessionTeam", "defensiveTeam", "pff_passCoverage"]).size().to_frame().reset_index()

    teams_cvg4 = teams_cvg4.rename(columns={0: 'plays'})

    teams_cvg5 = teams_cvg4[teams_cvg4['possessionTeam'] == offense]
    cvgbar3 = px.bar(
        data_frame=teams_cvg5,
        x='defensiveTeam',
        y="plays",
        color="pff_passCoverage",  # differentiate color of marks
        opacity=0.9,  # set opacity of markers (from 0 to 1)
        orientation="v",  # 'v','h': orientation of the marks
        barmode='group',
        template='seaborn',
        title="Defenses Faced by Selected Offense")
    return cvgbar3

 # returned objects are assigned to the component property of the Output


# Run app
if __name__=='__main__':
    app.run_server(port=8053)