from dash import html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas  as pd

from app import *
from dash_bootstrap_templates import ThemeSwitchAIO

# styles
template_theme1 = 'vapor'
template_theme2 = 'flatly'
url_theme1 = dbc.themes.VAPOR
url_theme2 = dbc.themes.FLATLY



# Reading data
df = pd.read_csv('data_clean.csv')
state_options = [{'label': x, 'value': x } for x in df['ESTADO'].unique()]


# layout
app.layout = dbc.Container(children=[
    dbc.Row([
        dbc.Col([
            ThemeSwitchAIO(aio_id='theme', themes = [url_theme1, url_theme2] ),
            html.H3('Preço x Estado'),
            dcc.Dropdown(
                id = 'estados',
                value =[state['label']for state in state_options[:3]],
                multi = True,
                options=state_options),
            dcc.Graph(id='line_graph')
        ],sm=12),
    ]),
    #Row2
    dbc.Row([
        # Drop 1
        dbc.Col([
            dcc.Dropdown(
                id='estado1',
                value = state_options[1]['label'],
                options = state_options
            )            
        ], sm = 12, md = 6),
        #Drop 2 
        dbc.Col([
            dcc.Dropdown(
                id = 'estado2',
                value=state_options[3]['label'],
                options=state_options),
        ], sm = 12, md = 6),
        #Graph 1 
        dbc.Col([
            dcc.Graph(id='indicator1')
        ], sm=6),
        #Graph 2
        dbc.Col([
            dcc.Graph(id='indicator2')
        ],sm=6)

    ])
])

# Callbacks
@app.callback(
    Output('line_graph', 'figure'),
    Input('estados','value'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value')
)

def line(estados, toggle):
    template = template_theme1 if toggle else template_theme2
    
    df_data = df.copy(deep=True)
    mask = df_data['ESTADO'].isin(estados)
    fig = px.line(df_data[mask],x = 'DATA', y= 'VALOR REVENDA (R$/L)',
                   color = 'ESTADO', template = template)

    return fig


# Indicators
@app.callback(
    Output('indicator1','figure'),
    Output('indicator2', 'figure'),
    Input('estado1', 'value'),
    Input('estado2', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def indicators(estado1, estado2, toggle):
    template = template_theme1 if toggle else template_theme2

    df_data = df.copy(deep=True)
    data_estado1 = df_data[df_data.ESTADO.isin([estado1])]
    data_estado2 = df_data[df_data.ESTADO.isin([estado2])]

    initial_date = str(int(df_data['ANO'].min()) -1)
    final_date = df_data['ANO'].max()

    iterable = [(estado1, data_estado1), (estado2, data_estado2)]
    indicators = []

    for estado, data in iterable:
        fig = go.Figure()
        fig.add_trace(go.Indicator(
            mode = 'number+delta',
            title={"text": f"<span>{estado}</span><br><span style='font-size:0.7em'>{initial_date} - {final_date}</span>"},
            value=data.at[data.index[-1], 'VALOR REVENDA (R$/L)'],
            number={'prefix':'R$', 'valueformat': '.2f'},
            delta={'relative':True,'valueformat': '.1%','reference':data.at[data.index[0], 'VALOR REVENDA (R$/L)']}
        ))

        fig.update_layout(template=template)
        indicators.append(fig)

    return indicators



# Run server
if __name__ == '__main__':
    app.run_server(debug=True)