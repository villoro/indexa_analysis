"""
    Dash app
"""

import dash_core_components as dcc
import dash_html_components as html

import constants as c


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


def get_layout():
    """ Creates the dash layout """

    return html.Div([
        # Header
        html.Div([
            html.H1(c.DASH_TITLE, id="title", style={"color": "white"})
        ], style=c.STYLE_HEADER),

        # Sidebar
        html.Div(
            create_sidebar([
                ("Size", dcc.Checklist(
                    id="drop_size", options=[
                        {'label': 'menos de 10k', 'value': 'A'},
                        {'label': 'de 10k a 100k', 'value': 'B'},
                        {'label': 'más de 100k', 'value': 'C'}
                    ]
                )),
            ]), id="sidebar", style=c.STYLE_SIDEBAR
        ),

        # Body
        html.Div(
            [

            ], id="body", style=c.STYLE_BODY
        ),
    ])
