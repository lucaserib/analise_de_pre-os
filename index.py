from dash import html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas  as pd

from app import *
from dash_bootstrap_templates import ThemeSwitchAIO

# Reading data
df = pd.read_csv('data_clean.csv')


# layout
app.layout = dbc.Container([
    html.H3('Teste')
])

# Rodar os servidor

if __name__ == '__main__':
    app.run_server(debug=True, port = '8051')