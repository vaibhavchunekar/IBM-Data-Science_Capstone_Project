import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# -----------------------
# Load data
# -----------------------
spacex_df = pd.read_csv("spacex_launch_dash.csv")

launch_sites = spacex_df['Launch Site'].unique()
min_payload = spacex_df['Payload Mass (kg)'].min()
max_payload = spacex_df['Payload Mass (kg)'].max()

# -----------------------
# Create app
# -----------------------
app = dash.Dash(__name__)

# -----------------------
# Layout
# TASK 1: Add a Launch Site Drop-down Input Component 
# -----------------------
app.layout = html.Div([

    html.H1("SpaceX Launch Dashboard"),
 #  TASK 1 — Launch Site Drop-down
    # Dropdown
    dcc.Dropdown(
        id='site-dropdown',
        options=[{'label': 'All Sites', 'value': 'ALL'}] +
                [{'label': site, 'value': site} for site in launch_sites],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),

    dcc.Graph(id='success-pie-chart'),

    html.Br(),

    # Range slider
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        marks={i: str(i) for i in range(0, 10001, 2000)},
        value=[min_payload, max_payload]
    ),

    dcc.Graph(id='success-payload-scatter-chart')
])

# -----------------------
# TASK 2: Add a callback function to render success-pie-chart based on selected site dropdown 
# TASK 2 — Callback for success pie chart

# Requirement: Pie chart changes based on dropdown
# Callback 1 (Pie chart)
# -----------------------
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def get_pie_chart(entered_site):

    if entered_site == 'ALL':
        fig = px.pie(
            spacex_df,
            names='Launch Site',
            values='class',
            title='Total Successful Launches by Site'
        )
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]

        fig = px.pie(
            filtered_df,
            names='class',
            title=f'Success vs Failure for {entered_site}'
        )

    return fig


# -----------------------
#TASK 3: Add a Range Slider to Select Payload 
# TASK 3 — Range Slider

#Requirement: Payload slider
# Callback 2 (Scatter)
# -----------------------
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter(selected_site, payload_range):

    low, high = payload_range

    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]

    if selected_site != 'ALL':
        filtered_df = filtered_df[
            filtered_df['Launch Site'] == selected_site
        ]

    fig = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title='Payload vs Launch Outcome'
    )

    return fig


# -----------------------
# TASK 4 — Scatter callback
#TASK 4: Add a callback function to render the success-payload-scatter-chart scatter plot
# Requirement: Scatter updates with site + payload
# Run
# -----------------------
if __name__ == '__main__':
    app.run(debug=True)
