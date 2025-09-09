from dash import html, dcc, register_page, callback, Input, Output
import pandas as pd
import plotly.express as px
from pathlib import Path
import json

register_page(__name__, path="/LA", name = "Los Angeles")

# Load LA data
DataPath = Path(__file__).parent.parent / "data" / "listingsLA.csv"
df = pd.read_csv(DataPath)
df = df[df['price'].notnull()]
df['price'] = df['price'].replace(r'[\$,]', '', regex=True).astype(float)
df = df[df['room_type'] != 'Hotel room']
neighborhood_counts = df['neighbourhood'].value_counts().reset_index()
neighborhood_counts.columns = ['neighbourhood', 'count']

# Load LA GeoJSON
GeoPath = Path(__file__).parent.parent / "data" / "neighbourhoodsLA.geojson"
with open(GeoPath, "r") as f:
    la_geojson = json.load(f)

crime_data_path = Path(__file__).parent.parent / "data" / "LA_YTD_Crimes.csv"
crime_df = pd.read_csv(crime_data_path, low_memory=False)
crime_df = crime_df[crime_df['UNIT_NAME'].notnull()]
crime_counts = crime_df['UNIT_NAME'].value_counts().reset_index()
crime_counts.columns = ['UNIT_NAME', 'crime_count']

layout = html.Div(
    style={"backgroundColor": "#1b1202", "padding": "20px"},
    children=[
        html.Div([
            html.Div([
                html.H3("Price Distribution", style={"color": "#cdd6d3", "textAlign": "center"}),
                dcc.Dropdown(
                    id="room-type-dropdown-la",
                    options=[{"label": rt, "value": rt} for rt in df["room_type"].unique() if rt != "Hotel room"],
                    value=[rt for rt in df["room_type"].unique() if rt != "Hotel room"][0],
                    clearable=False,
                    style={"marginBottom": "20px"}
                ),
                dcc.Slider(
                    id="price-slider-la",
                    min=int(df["price"].min()),
                    max=600,
                    value=min(600, int(df["price"].max())),
                    marks={str(p): str(p) for p in range(int(df["price"].min()), 601, 100)},
                    step=1,
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
                dcc.Graph(id="price-histogram-la", style={"height": "400px"})
            ], style={"flex": "1", "marginRight": "20px", "minHeight": "500px"}),
            html.Div([
                html.H3("Average Airbnb Price by Neighborhood", style={"color": "#cdd6d3", "textAlign": "center"}),
                dcc.Graph(id="choropleth-map-la", style={"height": "500px"})
            ], style={"flex": "1", "marginLeft": "20px", "minHeight": "500px"})
        ], style={"display": "flex", "alignItems": "flex-start"}),
        html.Div([
            html.H3("LA Crime by Type of Incident", style={"color": "#cdd6d3", "textAlign": "center", "marginTop": "40px"}),
            dcc.Dropdown(
                id="crime-category-dropdown-la",
                options=[{"label": cat, "value": cat} for cat in sorted(crime_df["CATEGORY"].dropna().unique())],
                value=None,
                placeholder="Filter by crime category",
                style={"marginBottom": "20px"}
            ),
            dcc.Graph(id="choropleth-map-la-crime", style={"height": "500px"})
        ])
    ]
)
@callback(
    Output("choropleth-map-la-crime", "figure"),
    Input("room-type-dropdown-la", "value"),
    Input("crime-category-dropdown-la", "value")
)
def update_choropleth_la_crime(selected_room_type, selected_category):
    # Crime density/concentration map
    crime_points = crime_df[(crime_df['LONGITUDE'].notnull()) & (crime_df['LATITUDE'].notnull())]
    if selected_category:
        crime_points = crime_points[crime_points["CATEGORY"] == selected_category]
    fig = px.scatter_mapbox(
        crime_points,
        lat="LATITUDE",
        lon="LONGITUDE",
        color="CATEGORY" if selected_category is None else None,
        hover_name="UNIT_NAME",
        hover_data=["CATEGORY", "STAT_DESC"],
        mapbox_style="carto-darkmatter",
        zoom=9,
        center={"lat": 34.0522, "lon": -118.2437},
        opacity=0.7,
        title="LA Crime Incidents (Raw Points)"
    )
    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, paper_bgcolor="black", font_color="white")
    return fig

@callback(
    Output("price-histogram-la", "figure"),
    Input("room-type-dropdown-la", "value"),
    Input("price-slider-la", "value")
)
def update_histogram_la(selected_room_type, max_price):
    d = df[(df["room_type"] == selected_room_type) & (df["price"] <= max_price)]
    fig = px.histogram(
        d,
        x="price",
        nbins=50,
        title=f"Price Distribution for {selected_room_type} (up to ${max_price})",
        labels={"price": "Price (USD)"},
        color_discrete_sequence=["#15c1e8"]
    )
    fig.update_layout(
        paper_bgcolor="black",
        font_color="white",
        margin=dict(l=10, r=10, t=50, b=10),
        xaxis=dict(range=[0, 600])
    )
    return fig

@callback(
    Output("choropleth-map-la", "figure"),
    Input("room-type-dropdown-la", "value")
)
def update_choropleth_la(selected_room_type):
    d = df[(df["room_type"] == selected_room_type) & (df["price"] <= 150) & (df["price"] > 0)]
    # Remove outliers using IQR method
    Q1 = d["price"].quantile(0.25)
    Q3 = d["price"].quantile(0.75)
    IQR = Q3 - Q1
    d = d[(d["price"] >= Q1 - 1.5 * IQR) & (d["price"] <= Q3 + 1.5 * IQR)]
    neighborhood_avg = d.groupby("neighbourhood")["price"].mean().reset_index()
    fig = px.choropleth_mapbox(
        neighborhood_avg,
        geojson=la_geojson,
        locations="neighbourhood",
        featureidkey="properties.neighbourhood",
        color="price",
        color_continuous_scale="Viridis",
        range_color=(0, 150),
        mapbox_style="carto-darkmatter",
        zoom=9,
        center={"lat": 34.0522, "lon": -118.2437},
        opacity=0.6,
        labels={"price": "Average Price"},
    )
    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, paper_bgcolor="black", font_color="white")
    return fig