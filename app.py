import dash
import dash_bootstrap_components as dbc

url_prefix = "/app/SWAPIT/"
app = dash.Dash(__name__, use_pages=True, url_base_pathname=url_prefix, external_stylesheets=[dbc.themes.BOOTSTRAP])

navbar = dbc.NavbarSimple(
    dbc.DropdownMenu(
        [
            dbc.DropdownMenuItem(page["name"], href=url_prefix + page["path"])
            for page in dash.page_registry.values()
            if page["module"] != "pages.not_found_404"
        ],
        nav=True,
        label="Navigation",
    ),
    brand="Multi Page App Demo",
    color="primary",
    dark=True,
    className="mb-2",
)

app.layout = dbc.Container(
    [navbar, dash.page_container],
    fluid=True,
)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
