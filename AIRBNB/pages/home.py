import dash
from dash import html

dash.register_page(__name__, path="/")

layout = html.Div(
    style={"backgroundColor": "#1b1202", "padding": "40px"},
    children=[
        html.H1("Risk Vs. Rent: The Airbnb Safety Index", style={"color": "#cdd6d3", "textAlign": "center"}),
        html.P(
            "This dashboard lets you explore Airbnb listings and crime data for New York City and Los Angeles. Each city page features interactive maps and charts to help you understand price trends, and compare them to crime incidents.",
            style={"color": "#cdd6d3", "fontSize": "22px", "textAlign": "center", "marginBottom": "30px"}
        ),
        html.Ul([
            html.Li([
                html.B("New York City: ", style={"color": "#15c1e8"}),
                "View Airbnb price distributions and a map of 2024 shooting incidents in NYC. Use filters to focus on specific room types or price ranges."
            ], style={"color": "#cdd6d3", "fontSize": "18px", "marginBottom": "15px"}),
            html.Li([
                html.B("Los Angeles: ", style={"color": "#15c1e8"}),
                "Explore LA Airbnb prices and see a map of crime incidents from the past 12 months. Filter by crime category to see patterns in different types of incidents."
            ], style={"color": "#cdd6d3", "fontSize": "18px", "marginBottom": "15px"})
        ], style={"marginLeft": "40px"}),
        html.P(
            "Navigate using the menu above. Each page offers interactive controls to filter listings by room type, price, or crime category (LA only).",
            style={"color": "#cdd6d3", "fontSize": "20px", "textAlign": "center", "marginTop": "40px"}
        ),
        html.P(
            "This dashboard is designed for figuring out which areas offer the best balance of affordability and safety.",
            style={"color": "#cdd6d3", "fontSize": "18px", "textAlign": "center", "marginTop": "20px"}
        )
    ]
)
