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

teams_cvg = plays.groupby(["defensiveTeam","pff_passCoverage"]).size().to_frame().reset_index()

teams_cvg = teams_cvg.rename(columns = {0:'plays'})

teams_cvg =teams_cvg.query("pff_passCoverage == 'Cover-0' or pff_passCoverage == 'Cover-1' or pff_passCoverage == 'Cover-2' or pff_passCoverage == 'Cover-3' or pff_passCoverage == '2-Man'")



# Build your components

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
mytitle = dcc.Markdown(children='# Defensive Coverages by Team')
mygraph = dcc.Graph(figure={})
dropdown = dcc.Dropdown(options=[{'label':x, 'value':x}
                                  for x in sorted(teams_cvg['defensiveTeam'].unique())],
                        value='TB',  # initial value displayed when page first loads
                        clearable=False)

# Customize your own Layout
app.layout = dbc.Container([mytitle, mygraph, dropdown])
# Callback allows components to interact
@app.callback(
    Output(mygraph, component_property='figure'),
    Input(dropdown, component_property='value')
)
def update_graph(teamname):  # function arguments come from the component property of the Input
    teams_cvg1 = teams_cvg[teams_cvg['defensiveTeam'] == teamname]
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

 # returned objects are assigned to the component property of the Output


# Run app
if __name__=='__main__':
    app.run_server(port=8053)