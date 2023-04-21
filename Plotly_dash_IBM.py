import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

color_palette = px.colors.qualitative.Antique

spacex_df = pd.read_csv("SpaceX_dashboard_CSV.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    dcc.Dropdown(id='site-dropdown',
                 options=[
                     {'label': 'All Sites', 'value': 'ALL'},
                     {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                     {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                     {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                     {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                 ],
                 value='ALL',
                 placeholder="Select a Launch Site",
                 searchable=True),
    html.Br(),
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    html.P("Payload Range (kg):"),
    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=1000,
                    value=[min_payload, max_payload],
                    marks={0: '0', 2500: '2500', 5000: '5000',
                           7500: '7500', 10000: '10000'}),
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'))
def update_success_pie_chart(site_dropdown):
    if site_dropdown == 'ALL':
        piechart = px.pie(data_frame=spacex_df, names='Launch Site', values='class',
                          title='Total Launches for All Sites', color_discrete_sequence=color_palette)
        return piechart
    else:
        specific_df = spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        piechart = px.pie(data_frame=specific_df, names='class',
                          title=f'Total Launches for {site_dropdown}', color_discrete_sequence=color_palette)
        return piechart

@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')])
def update_success_payload_scatter_chart(site_dropdown, payload_slider):
    if site_dropdown == 'ALL':
        filtered_data = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_slider[0])
                                  & (spacex_df['Payload Mass (kg)'] <= payload_slider[1])]
        scatterplot = px.scatter(data_frame=filtered_data, x="Payload Mass (kg)", y="class",
                                 color="Booster Version Category", color_discrete_sequence=color_palette,
                                 size_max=20, size="Payload Mass (kg)",
                                 title='Payload vs Outcome for All Sites')
        return scatterplot
    else:
        specific_df = spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        filtered_data = specific_df[(specific_df['Payload Mass (kg)'] >= payload_slider[0])
                                    & (specific_df['Payload Mass (kg)'] <= payload_slider[1])]
        scatterplot = px.scatter(data_frame=filtered_data, x="Payload Mass (kg)", y="class",
                                 color="Booster Version Category", color_discrete_sequence=color_palette,
                                 size_max=20, size="Payload Mass (kg)",
                                 title=f'Payload vs Outcome for {site_dropdown}')
        return scatterplot

if __name__ == '__main__':
    app.run_server()