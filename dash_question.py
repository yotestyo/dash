import dash
from dash import dcc
from dash import html
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output
from settings_dash import desired_cols
from plotly.subplots import make_subplots
import plotly.graph_objs as go

colors = {
    'background': '#111111',
    'text': 'red'
}

def generate_table(dataframe):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(len(dataframe))
        ])
    ])

df = pd.read_csv("file")
available_indicators = [i for i in df.columns if i in desired_cols]

app = dash.Dash(__name__)


app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Biomonitoring Dashboard',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Dash: A web application framework for your data.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    html.Div([
        html.Div([
            dcc.Dropdown(
                id='yaxis',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value = "CO2",
                multi = True,
        
            ),
            dcc.RadioItems(
                id='yaxis_type',
                options=[{'label': i, 'value': i} for i in ['linear', 'log']],
                value='linear',
                labelStyle={'display': 'inline-block'},
                style = {"color" : colors["text"]},
                
                
            )
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='secondary_yaxis',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value =  "CO2",
                multi = True
            ),
            dcc.RadioItems(
                id='secondary_yaxis_type',
                options=[{'label': i, 'value': i} for i in ['linear', 'log']],
                value='linear',
                labelStyle={'display': 'inline-block'},
                style = {"color" : colors["text"]}
            )
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(
        id = "example_graph",
        figure={} 

    ),


    html.Div([
        html.H4(children='measurement data', style = {"color" : colors["text"]}),
        generate_table(df)
    ])
])


@app.callback(
    Output("example_graph", "figure"),
    Input("yaxis", "value"),
    Input("secondary_yaxis", "value"),
    Input("yaxis_type", "value"),
    Input("secondary_yaxis_type", "value")

)
def update_figure(selected_cols, secondary_yaxis, yaxis_type, secondary_yaxis_type):

    if selected_cols is not None:
        if type(selected_cols) is list:
            pass
        elif type(selected_cols) is str:
            selected_cols = [selected_cols]
    else:
        selected_cols = []

    if secondary_yaxis is not None:
        if type(secondary_yaxis) is list:
            pass
        elif type(secondary_yaxis) is str:
            secondary_yaxis = [secondary_yaxis]
    else:
        secondary_yaxis = [] 

    filtered_df = df.filter(items = selected_cols)


    
    fig = make_subplots(specs = [[{"secondary_y" : True}]])
    column_dict = {"BASET_rate" : "cyan", "cX" : "red", "cS" : "green", "cE" : "blue", "CO2" : "orange"}
    for col in filtered_df:
        secondary_y_flag = col in secondary_yaxis

        fig.add_trace(
            go.Scatter(x=filtered_df.index, y=filtered_df[col], name = str(col), mode = "markers", marker = dict(color = column_dict[col], size = 5, symbol = "x")
            )
            , secondary_y= secondary_y_flag
        )

    cols_y1 = [col for col in selected_cols if col not in secondary_yaxis]            
    cols_y2 = [col for col in selected_cols if col in secondary_yaxis]
    fig.update_yaxes(title_text= str(cols_y1), secondary_y=False , title_standoff = 20 , type = yaxis_type)
    fig.update_yaxes(title_text= str(cols_y2), secondary_y=True, title_standoff = 20, type = secondary_yaxis_type)




    #fig = visualize(filtered_df, secondary_y_cols= secondary_yaxis, yaxis_type = yaxis_type, sec_yaxis_type = secondary_yaxis_type )
    fig.update_layout(transition_duration=500)


    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port = 6799)

# visit http://127.0.0.1:6799/ in your web browser.

