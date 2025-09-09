from dash import html, dcc, register_page, callback, Input, Output
import pandas as pd
import plotly.express as px
from pathlib import Path
import json

register_page(__name__, path="/NYC", name = "New York City")
# Load NYC crime data
crime_data_path = Path(__file__).parent.parent / "data" / "NYC_YTD_Crime.csv"

# Load NYC data
DataPath = Path(__file__).parent.parent / "data" / "listingsNYC.csv"
df = pd.read_csv(DataPath)
df = df[df['price'].notnull()]
df['price'] = df['price'].replace(r'[\$,]', '', regex=True).astype(float)
df = df[df['room_type'] != 'Hotel room']
neighborhood_counts = df['neighbourhood'].value_counts().reset_index()
neighborhood_counts.columns = ['neighbourhood', 'count']

# Load NYC GeoJSON
GeoPath = Path(__file__).parent.parent / "data" / "neighbourhoodsNYC.geojson"
with open(GeoPath, "r") as f:
    nyc_geojson = json.load(f)

layout = html.Div(
    style={"backgroundColor": "#1b1202", "padding": "20px"},
    children=[
        html.Div([
            html.Div([
                html.H3("Price Distribution", style={"color": "#cdd6d3", "textAlign": "center"}),
                dcc.Dropdown(
                    id="room-type-dropdown-nyc",
                    options=[{"label": rt, "value": rt} for rt in df["room_type"].unique() if rt != "Hotel room"],
                    value=[rt for rt in df["room_type"].unique() if rt != "Hotel room"][0],
                    clearable=False,
                    style={"marginBottom": "20px"}
                ),
                dcc.Slider(
                    id="price-slider-nyc",
                    min=int(df["price"].min()),
                    max=600,
                    value=min(600, int(df["price"].max())),
                    marks={str(p): str(p) for p in range(int(df["price"].min()), 601, 100)},
                    step=1,
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
                dcc.Graph(id="price-histogram-nyc", style={"height": "400px"})
            ], style={"flex": "1", "marginRight": "20px", "minHeight": "500px"}),
            html.Div([
                html.H3("Average Airbnb Price by Neighborhood", style={"color": "#cdd6d3", "textAlign": "center"}),
                dcc.Graph(id="choropleth-map-nyc", style={"height": "500px"})
            ], style={"flex": "1", "marginLeft": "20px", "minHeight": "500px"})
        ], style={"display": "flex", "alignItems": "flex-start"}),
        html.Div([
            html.H3("NYC Shooting Incidents (Raw Data Points)", style={"color": "#cdd6d3", "textAlign": "center", "marginTop": "40px"}),
            dcc.Graph(id="bar-chart-nyc-crime", style={"height": "500px"})
        ])
    ]
)

@callback(
    Output("bar-chart-nyc-crime", "figure"),
    Input("room-type-dropdown-nyc", "value")
)
def update_bar_chart_nyc_crime(selected_room_type):
    # Load new shooting incident data
    shooting_path = Path(__file__).parent.parent / "data" / "NYPD_Shooting_Incident_Data__Historic__20250909.csv"
    shooting_df = pd.read_csv(shooting_path)
    shooting_df = shooting_df[(shooting_df["Latitude"].notnull()) & (shooting_df["Longitude"].notnull())]
    # Filter for 2024 only
    shooting_df = shooting_df[shooting_df["OCCUR_DATE"].str.contains("/2024")]  # MM/DD/YYYY format
    # Create density/concentration map
    fig = px.scatter_mapbox(
        shooting_df,
        lat="Latitude",
        lon="Longitude",
        color=None,
        hover_data=["OCCUR_DATE", "OCCUR_TIME", "PRECINCT", "LOCATION_DESC"],
        mapbox_style="carto-darkmatter",
        zoom=9,
        center={"lat": 40.7128, "lon": -74.0060},
        opacity=0.7,
    )
    fig.update_layout(
        paper_bgcolor="black",
        font_color="white",
        margin=dict(l=10, r=10, t=50, b=10)
    )
    return fig

@callback(
    Output("price-histogram-nyc", "figure"),
    Input("room-type-dropdown-nyc", "value"),
    Input("price-slider-nyc", "value")
)
def update_histogram_nyc(selected_room_type, max_price):
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
    Output("choropleth-map-nyc", "figure"),
    Input("room-type-dropdown-nyc", "value")
)
def update_choropleth_nyc(selected_room_type):
    d = df[(df["room_type"] == selected_room_type) & (df["price"] <= 150) & (df["price"] > 0)]
    # Remove outliers using IQR method
    Q1 = d["price"].quantile(0.25)
    Q3 = d["price"].quantile(0.75)
    IQR = Q3 - Q1
    d = d[(d["price"] >= Q1 - 1.5 * IQR) & (d["price"] <= Q3 + 1.5 * IQR)]
    neighborhood_avg = d.groupby("neighbourhood")["price"].mean().reset_index()
    fig = px.choropleth_mapbox(
        neighborhood_avg,
        geojson=nyc_geojson,
        locations="neighbourhood",
        featureidkey="properties.neighbourhood",
        color="price",
        color_continuous_scale="Viridis",
        range_color=(0, 150),
        mapbox_style="carto-darkmatter",
        zoom=9,
        center={"lat": 40.7128, "lon": -74.0060},
        opacity=0.6,
        labels={"price": "Average Price"},
    )
    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, paper_bgcolor="black", font_color="white")
    return fig