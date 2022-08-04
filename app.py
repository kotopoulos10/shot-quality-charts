from turtle import color
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)
application = app.server

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_json('game5.json')
df_team = df
df_team['SQ_Points_Total'] = df_team.groupby('Team')['SQ_Points'].cumsum()

fig = px.line(
        df,
        x="Unnamed: 0",
        y="SQ_Points_Total",
        color="Team",
        markers=True,
        custom_data=["SQ_Points", "Players", "Play_run", "Possession_Quality", "Minutes", "Seconds", "Period"],
        title="Shot Quality Score",
        labels={
                     "Unnamed: 0": "Play #",
                     "SQ_Points_Total": "Shot Quality Score"
                 },
    )

fig.update_traces(
        hovertemplate="<br>".join([
            "Posession #: %{x}",
            "SQ Total Points: %{y}",
            "SQ Points : %{customdata[0]}",
            "Action: %{customdata[1]} %{customdata[2]}",
            "Posession Quality: %{customdata[3]}",
            "Q %{customdata[6]} - %{customdata[4]}:%{customdata[5]}"
        ])
    ),

app.layout = html.Div([
    html.H1(children='Shot Quality'),

    html.H2(children='Game Chart'),

    dcc.Graph(
        id='game-graph',
        figure=fig
    ),

    html.H2(children='Player Chart'),

    dcc.Dropdown(
        id='player-dropdown',
        options=[
            {'label':i, 'value':i} for i in df['Players'].unique()
        ],
        multi=True
    ),
    dcc.Graph(id = "game-chart")
])

@app.callback(
    Output('game-chart', 'figure'),
    [Input('player-dropdown', 'value')])
def update_player_chart(selected_players):
    df_players = df
    df_players['SQ_Points_Total'] = df_players.groupby('Players')['SQ_Points'].cumsum()
    
    if selected_players: 
        df_players_filtered = df_players[df_players['Players'].isin(selected_players)]
    else:
        df_players_filtered = df_players
        
    fig = px.line(
        df_players_filtered,
        x="Unnamed: 0",
        y="SQ_Points_Total",
        color="Players",
        markers=True,
        custom_data=["SQ_Points", "Players", "Play_run", "Possession_Quality"]
    )

    fig.update_traces(
        hovertemplate="<br>".join([
            "Posession #: %{x}",
            "SQ Total Points: %{y}",
            "SQ Points : %{customdata[0]}",
            "Action: %{customdata[1]} %{customdata[2]}",
            "Posession Quality: %{customdata[3]}"
        ])
    )

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)