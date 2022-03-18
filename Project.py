import pandas as pd
import plotly.express as px
import plotly.offline as pyo
import plotly.graph_objs as go
import dash
from dash import dcc,html,callback_context
import dash_bootstrap_components as dbc
from dash.dependencies import Output,Input
# pyo.init_notebook_mode(connected=True)

yearlyTransmission=pd.read_csv("/home/abhishek/IdeaProjects/TrainingProject/data/Outputs/yearlyTransmission.csv")
transmissionType = pd.read_csv("/home/abhishek/IdeaProjects/TrainingProject/data/Outputs/transmissionType.csv")
mileageData=pd.read_csv("/home/abhishek/IdeaProjects/TrainingProject/data/Outputs/mileageData.csv")
brandModelPrice = pd.read_csv("/home/abhishek/IdeaProjects/TrainingProject/data/Outputs/brandModelPrice.csv")
brandPrice= pd.read_csv("/home/abhishek/IdeaProjects/TrainingProject/data/Outputs/brandPrice.csv")
fuelTypePrice= pd.read_csv("/home/abhishek/IdeaProjects/TrainingProject/data/Outputs/fuelTypePrice.csv")
fuelTypeBrandPrice= pd.read_csv("/home/abhishek/IdeaProjects/TrainingProject/data/Outputs/fuelTypeBrandPrice.csv")
yearWiseBrandPrice= pd.read_csv("/home/abhishek/IdeaProjects/TrainingProject/data/Outputs/yearWiseBrandPrice.csv")
carsInEachBrand=pd.read_csv("/home/abhishek/IdeaProjects/TrainingProject/data/Outputs/carsInEachBrand.csv")
carsInEachBrand.set_index("brand", inplace = True)
totalCars=pd.read_csv("/home/abhishek/IdeaProjects/TrainingProject/data/Outputs/totalCars.csv")
totalCars.set_index("brand", inplace = True)
bestSellingModels=pd.read_csv("/home/abhishek/IdeaProjects/TrainingProject/data/Outputs/bestSellingModel.csv")
bestSellingModels.set_index("brand", inplace = True)
worstSellingModels=pd.read_csv("/home/abhishek/IdeaProjects/TrainingProject/data/Outputs/worstSellingModel.csv")
worstSellingModels.set_index("brand", inplace = True)

lists=brandModelPrice.brand.unique().tolist()
lists.sort()
lists.insert(0,'overall')
animationList=["Average Price Change of All Brands","Change in Transmission Type"]
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

CARD_TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#0074D9'
}
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '20%',
    'padding': '20px 10px',
    'background-color': '#f8f9fa'
}

# the style arguments for the main content page.
CONTENT_STYLE = {
    'margin-left': '25%',
    'margin-right': '5%',
    'top': 0,
    'padding': '20px 10px'
}

TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#191970'
}
BUTTON_STYLE={
  'background-color': '#4CAF50',
'margin-right': '4%',
   'border': '2px solid #f44336',
    'border-radius': '8px',
  'color': 'white',
  'padding': '15px 32px',
  'text-align': 'center',
  'text-decoration': 'none',
  'display': 'inline-block',
  'font-size': '16px',
}
sidebar = dbc.Card(
    [
        # dbc.CardImg(src="/assets/ball_of_sun.jpg", top=True, bottom=False,
        #             title="Image by Kevin Dinkel", alt='Learn Dash Bootstrap Card Component'),
        dbc.CardBody(
            [
                html.H1("Car Data ", className="card-title"),
                # html.P("ㅤ",className='card-text'),
                html.Hr(),
                # html.H6("Graph 1:", className="card-subtitle"),
                html.H3(
                    "Brand Wise Data",
                    className="card-text text-success",
                ),
                dcc.Dropdown(id='user_choice', options=[{'label': brand.upper(), "value": brand} for brand in lists],
                             value='overall', clearable=False, style={"color": "#000000"}),
                html.H1("ㅤ",className='card-text'),
                html.Hr(),
                html.H3(
                    "Price Based On",
                    className="card-text text-success",
                ),
                html.Button('FuelType', id='btn-nclicks-1', n_clicks=0,style=BUTTON_STYLE),
                html.Button('Mileage', id='btn-nclicks-2', n_clicks=0,style=BUTTON_STYLE),

                html.H1("ㅤ", className='card-text'),
                html.Hr(),
                html.H3(
                    "Animations",
                    className="card-text text-success",
                ),
                dcc.Dropdown(id='animation', options=[{'label': choose, "value": choose} for choose in animationList],
                             value='Average Price Change of All Brands', clearable=False, style={"color": "#000000"}),
            ]
        ),
    ],
    color="dark",   # https://bootswatch.com/default/ for more card colors
    inverse=True,   # change color of text (black or white)
    outline=False,
    style=SIDEBAR_STYLE# True = remove the block colors from the background and header
)


total_cars = dbc.Card(
    [
        dbc.CardBody([
            html.H5("Total Cars", className="card-title text-white"),
            dbc.ListGroup(
                [
                    dbc.ListGroupItem(html.Label(id='total_cars',className="h1 text-warning ")),
                ], flush=True,
            ),

        ]),
    ], color="dark",
    style=CARD_TEXT_STYLE,
)

modelInEachBrand = dbc.Card(
    [
        dbc.CardBody([
            html.H5("Total Models", className="card-title text-white"),
            dbc.ListGroup(
                [
                    dbc.ListGroupItem(html.Label(id='modelInEachBd',className="h1 text-warning ")),
                ], flush=True,
            ),

        ]),
    ], color="dark",
    style=CARD_TEXT_STYLE,
)

bestSellingModel = dbc.Card(
    [
        dbc.CardBody([
            html.H5("Best Selling Model", className="card-title text-white"),
            dbc.ListGroup(
                [
                    dbc.ListGroupItem(html.Label(id='bestSellingMod',className="h1 text-success ")),
                ], flush=True,
            ),
        ]),
    ], color="dark",
    style=CARD_TEXT_STYLE,
)


worstSellingModel = dbc.Card(
    [
        dbc.CardBody([
            html.H5("Worst Selling Model", className="card-title text-white"),
            dbc.ListGroup(
                [
                    dbc.ListGroupItem(html.Label(id='worstSellingMod',className="h1 text-danger ")),
                ], flush=True,
            ),
        ]),
    ], color="dark",
    style=CARD_TEXT_STYLE,
)
card_graph1 = dbc.Card(
        dcc.Graph(id='graph1', figure={}), body=True, color="secondary",
)
card_graph2 = dbc.Card(
        dcc.Graph(id='graph2', figure={}), body=True, color="secondary",
)
card_graph3 = dbc.Card(
        dcc.Graph(id='graph3', figure={}), body=True, color="secondary",
)
card_graph4 = dbc.Card(
        dcc.Graph(id='graph4', figure={}), body=True, color="secondary",
)
content = html.Div([
    dbc.Row(
        [
            dbc.Col(total_cars, md=3),
            dbc.Col(modelInEachBrand, md=3),
            dbc.Col(bestSellingModel, md=3),
            dbc.Col(worstSellingModel, md=3),
        ], justify="around",
        style=CONTENT_STYLE
    ),  # justify="start", "center", "end", "between", "around"

    dbc.Row(
        [
            dbc.Col(card_graph1,md=6),
            dbc.Col(card_graph2,md=6),
        ],
        style=CONTENT_STYLE
    ),
    dbc.Row(
        [
            dbc.Col(card_graph3,md=12),
        ], justify="around",
            style=CONTENT_STYLE
    ),
    dbc.Row(
        [
            dbc.Col(card_graph4, md=12),
        ], justify="around",
        style=CONTENT_STYLE
    ),

])

app.layout = html.Div([sidebar, content])
@app.callback(
    Output("graph1", "figure"),
    Output('total_cars','children'),
    Output('modelInEachBd','children'),
    Output('bestSellingMod','children'),
    Output('worstSellingMod','children'),
    Output("graph2","figure"),
    [Input("user_choice", "value")]
)
def update_graph(value):
    # fig = px.scatter(df.query("year=={}".format(str(value))), x="gdpPercap", y="lifeExp",
    #                  size="pop", color="continent", title=str(value),
    #                  hover_name="country", log_x=True, size_max=60).update_layout(showlegend=True, title_x=0.5)
    if value != 'overall':
        tests = brandModelPrice[brandModelPrice['brand'] == value]
        transmissionTypes = transmissionType[transmissionType['brand'] == value]
        fig = px.bar(
            data_frame=tests,
            x='model',
            y='Average Price',
            color='model',
            orientation='v',
            hover_name='brand',
            hover_data={
                'brand': False,
                'Average Price': True,
                'Min Price': True,
                'Max Price': True
            },
            title='Model Wise Average Price',
            labels={
                'brand': 'Brand',
                'model': 'Models'

            },
            template='plotly_dark',
        )

        fig.update_layout(
            hoverlabel=dict(
                bgcolor='black',
                font_size=16,
                font_family="Rockwell"
            )
        )

        fig1 = px.pie(
            data_frame=transmissionTypes,
            values='count',
            names='transmission',
            title='Brand Wise Transmission Type',
            template='plotly_dark',

        )
        fig1.update_layout(
            hoverlabel=dict(
                bgcolor='black',
                font_size=16,
                font_family="Rockwell"
            )
        )
        children = totalCars.loc[value]["count"]
        children2 = carsInEachBrand.loc[value]["count"]
        children3= bestSellingModels.loc[value]["model"]
        if children3=='Combo Life':
            children3='C. Life'
        if children3=='Grand C-MAX':
            children3='G. C-Max'
        children4 = worstSellingModels.loc[value]["model"]

        return fig,children,children2,children3,children4,fig1
    else:
        children1=totalCars["count"].sum()
        children2 = carsInEachBrand["count"].sum()
        children3= bestSellingModels.loc["vw"]["model"]
        children4 = worstSellingModels.loc["hyundi"]["model"]
        fig = px.bar(
            data_frame=brandPrice,
            x='brand',
            y='Average Price',
            color='brand',
            text='Average Price',
            hover_name='brand',
            hover_data={
                'brand': False,
                'Min Price': True,
                'Max Price': True
            },
            title='Brand Wide Average Price',
            labels={
                'brand': 'Brand'
            },
            template='plotly_dark',

        )
        fig.update_layout(
            hoverlabel=dict(
                bgcolor='black',
                font_size=16,
                font_family="Rockwell"
            )
        )
        fig1 = px.pie(
            data_frame=transmissionType,
            values='count',
            names='transmission',
            title='Brand Wise Transmission Type',
            template='plotly_dark',

        )
        fig1.update_layout(
            hoverlabel=dict(
                bgcolor='black',
                font_size=16,
                font_family="Rockwell"
            )
        )

        return fig,children1,children2,children3,children4,fig1


@app.callback(
    Output('graph3', 'figure'),
    Input('btn-nclicks-1', 'n_clicks'),
    Input('btn-nclicks-2', 'n_clicks'),
)
def displayClick(btn1, btn2):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'btn-nclicks-1' in changed_id:
        fig3 = px.scatter(
            data_frame=fuelTypeBrandPrice,
            x='brand',
            y='Average Price',
            color='brand',
            size='Average Price',
            hover_name='Average Price',
            hover_data={
                'Average Price': False,
                'Min Price': True,
                'Max Price': True
            },
            title='Type of Cars & Their Average Price',
            labels={
                'fuelType': 'Type of Car',

            },
            template='plotly_dark',
            facet_col='fuelType',

        )

        fig3.update_layout(
            hoverlabel=dict(
                #         bgcolor='yellow',
                font_size=16,
                font_family="Rockwell"
            ),
        )

    else:
        fig3 = px.scatter(
            data_frame=mileageData,
            x='price',
            y='mileage',
            size='price',
            color='brand',
            title='Mileage vs Price',
            template='plotly_dark',
            hover_name='brand',
            hover_data={
                'brand': False
            },
        )
        fig3.update_layout(
            hoverlabel=dict(
                bgcolor='black',
                font_size=16,
                font_family="Rockwell"
            )
        )

    return fig3
@app.callback(
    Output('graph4','figure'),
    [Input("animation", "value")]
)
def animation(value):
    if value=="Average Price Change of All Brands":
        fig4 = px.bar(
            data_frame=yearWiseBrandPrice,
            x='Average Price',
            y='brand',
            color='brand',
            animation_frame='year',
            range_x=[0, 70000],
            orientation='h',
            hover_name='Average Price',
            hover_data={
                #         'brand':False,
                'Average Price': False,
                'Min Price': True,
                'Max Price': True
            },
            title='Average Price of Brands Over 20 Years',
            labels={
                'brand': 'Brand',

            },
            template='plotly_dark',
        )

        fig4.update_layout(
            hoverlabel=dict(
                #         bgcolor='yellow',
                font_size=16,
                font_family="Rockwell"
            ),
        )
    else:
        fig4 = px.bar(
            data_frame=yearlyTransmission,
            x='count',
            y='transmission',
            color='transmission',
            animation_frame='year',
            range_x=[0, 500],
            hover_name='transmission',
            hover_data={
                'transmission': False,
            },
            title='Change in transmission over 20 Years',
            template='plotly_dark',

        )

        fig4.update_layout(
            hoverlabel=dict(
                font_size=16,
                font_family="Rockwell"
            ),

        )
    return fig4

if __name__ == "__main__":
    app.run_server(debug=True)
