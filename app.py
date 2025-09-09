from dash import Dash, dcc, html, page_container
import dash_bootstrap_components as dbc


#initialize the app
app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True, 
           title = "Multiple Pages App", external_stylesheets=[dbc.themes.LUX])
server = app.server# for deployment

app.layout = html.Div([
    dbc.NavbarSimple(
        children=[
            dbc.NavLink("Home", href="/", active="exact"),
            dbc.NavLink("New York City", href="/NYC", active="exact"),
            dbc.NavLink("Los Angeles", href="/LA", active="exact"),
            ],
        brand="Airbnb Listings & Crime Explorer"
    ),
    page_container
])

if __name__ == '__main__':
    app.run(debug=True)
