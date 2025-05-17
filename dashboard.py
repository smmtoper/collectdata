import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output, callback

df = pd.read_csv('characters.csv')
df = df.rename(columns={'Имя': 'Name', 'Power': 'Power', 'Speed': 'Speed', 
                        'Precision': 'Precision', 'Endurance': 'Endurance', 
                        'Home Reality': 'Universe', 'Status': 'Status'})

universes = df['Universe'].value_counts().index[:10]
df_universe = df[df['Universe'].isin(universes)]
df_status = df[df['Status'].isin(["Alive", "Deceased"])]
occupation_counts = df['Occupation'].value_counts().head(10).reset_index()
occupation_counts.columns = ['Occupation', 'Count']
stats_cols = ["Power", "Speed", "Precision", "Endurance"]
df_stats = df.set_index('Name')[stats_cols].transpose()
app = Dash(__name__)
app.layout = html.Div([
    html.H1("Spider-Verse Characters Dashboard", style={'textAlign': 'center'}),
    html.Div([
        html.Div([
            html.H3("Распределение по вселенным"),
            dcc.Graph(
                figure=px.pie(
                    df_universe, names='Universe', title='Персонажи по вселенным',
                    color_discrete_sequence=px.colors.qualitative.Pastel, hole=0.3
                )
            )
        ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),
        html.Div([
            html.H3("Распределение по статусу"),
            dcc.Graph(
                figure=px.pie(
                    df_status, names='Status', title='Статус персонажей',
                    color_discrete_sequence=px.colors.qualitative.Set2, hole=0.3
                )
            )
        ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'})
    ]),
    html.Div([
        html.H3("Род деятельности персонажей"),
        dcc.Graph(
            figure=px.bar(
                occupation_counts, x='Occupation', y='Count',
                labels={'Occupation': 'Род деятельности', 'Count': 'Количество'},
                color='Occupation', title='Топ 10 профессий персонажей',
                text_auto=True
            ).update_layout(showlegend=False)
        )
    ], style={'padding': '10px'}),

    html.Div([
        html.H2("Character Stats Comparison", style={'textAlign': 'center'}),
        dcc.Dropdown(
            id='dropdown-selection1',
            options=[{'label': name, 'value': name} for name in df['Name']],
            value='Abel Tesfaye',
            style={"height": "50px", "margin-bottom": "10px"}
        ),
        dcc.Dropdown(
            id='dropdown-selection2',
            options=[{'label': name, 'value': name} for name in df['Name']],
            value='Gwen Stacy',
            style={"height": "50px"}
        ),
        html.Div(id='text-output', style={"height": "50px", "margin": "10px 0"}),
        dcc.Graph(id='radar-chart', style={"height": "500px"})
    ], style={"border": "1px solid #dee2e6", "border-radius": "10px", "padding": "15px", "background": "white"}),

    html.Div([
        html.H2("Character Information", style={'textAlign': 'center'}),
        dcc.Graph(id='info-table', style={"height": "300px", "margin-top": "20px"})
    ], style={"border": "1px solid #dee2e6", "border-radius": "10px", "padding": "15px", "background": "white"}),

    html.Div([
        html.H3("Выберите персонажа для подробной информации"),
        dcc.Dropdown(
            id='char-dropdown',
            options=[{'label': name, 'value': name} for name in df['Name']],
            value='Abel Tesfaye',
            clearable=False
        ),
        html.Div(id='char-info', style={'margin-top': '20px'})
    ], style={'padding': '20px'})
])
@callback(
    Output('radar-chart', 'figure'),
    Output('text-output', 'children'),
    Output('info-table', 'figure'),
    Input('dropdown-selection1', 'value'),
    Input('dropdown-selection2', 'value')
)
def update_comparison(char1, char2):
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=df_stats[char1].values, theta=stats_cols, fill='toself', name=char1))
    fig.add_trace(go.Scatterpolar(r=df_stats[char2].values, theta=stats_cols, fill='toself', name=char2))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 6])), showlegend=True)
    char1_data, char2_data = df[df['Name'] == char1].iloc[0], df[df['Name'] == char2].iloc[0]
    text_output = f"Comparing {char1} ({char1_data['Universe']}) vs {char2} ({char2_data['Universe']})"
    table_fig = go.Figure(data=[go.Table(
        header=dict(values=["Attribute", char1, char2], fill_color='#f8f9fa', align='left'),
        cells=dict(values=[
            ["Universe", "Appeared in", "Power", "Speed", "Precision", "Endurance"],
            [char1_data[attr] for attr in ["Universe", "Appeared in", "Power", "Speed", "Precision", "Endurance"]],
            [char2_data[attr] for attr in ["Universe", "Appeared in", "Power", "Speed", "Precision", "Endurance"]]
        ], fill_color='white', align='left'))
    ])
    return fig, text_output, table_fig

if __name__ == '__main__':
    app.run(debug=True)
