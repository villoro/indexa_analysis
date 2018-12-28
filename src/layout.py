"""
    Dash app
"""

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

import constants as c

PLOT_CONFIG = {
    "displaylogo": False,
    "modeBarButtonsToRemove": ["sendDataToCloud", "select2d", "lasso2d", "resetScale2d"]
}

def create_sidebar(elements):
    """
        Creates the sidebar given a list of elements.
        Each element should have a title and some data
    """

    def _get_sidebar_elem(title, data):
        """
            Creates an element for the sidebar

            Args:
                title:  name to display
                data:   what to include in the element

            Return:
                html div with the element
        """

        aux = html.H6(title + ":")
        children = [aux] + data if isinstance(data, list) else [aux, data]

        return html.Div(children, style=c.STYLE_SIDEBAR_ELEM)

    return [_get_sidebar_elem(title, data) for title, data in elements]


def create_body(datalist):
    """
        Creates an element for the body

        Args:
            datalist:   what to include in the body

        Return:
            html div with the element
    """
    return [html.Div(data, className="row", style=c.STYLE_DIV_CONTROL_IN_BODY) for data in datalist]


def get_layout():
    """ Creates the dash layout """

    navbar = dbc.Navbar(
        [],
        brand=c.DASH_TITLE,
        brand_href="/",
        sticky="top",
        color="success"
    )

    filters = html.Div(
        create_sidebar([
            ("Tamaño", dcc.Checklist(
                id="drop_size", values=["B"], options=[
                    {'label': 'A: menos de 10.000€', 'value': 'A'},
                    {'label': 'B: de 10.000€ a 100.000€', 'value': 'B'},
                    {'label': 'C: más de 100.000€', 'value': 'C'}
                ]
            )),
            ("Riesgo", dcc.Checklist(
                id="drop_risk", values=[1, 5, 10],
                options=[{'label': x, 'value': x} for x in range(1, 11)]
            )),
            ("Datos", dcc.Checklist(
                id="drop_method", values=["R"],
                options=[
                    {'label': 'C: Calculados con los ETFs', 'value': 'C'},
                    {'label': 'R: Con datos de indexa (API)', 'value': 'R'},
                ]
            )),
        ]), id="sidebar"
    )

    content = html.Div(
        create_body([
            dcc.Graph(id="plot_one_invest", config=PLOT_CONFIG),
            dcc.Graph(id="plot_per_invest", config=PLOT_CONFIG),
            html.H6(
                """* Las etiquetas de las series siguen el formato TRD.
                Dónde T indica el tamaño (A, B o C), R el riesgo (entre 1 i 10) y D los datos (C o R).
                """
            )
        ]), id="body"
    )

    return html.Div([navbar, filters, content])
