"""
    Dash app
"""

from dash import Dash
from dash.dependencies import Input, Output

import constants as c
from layout import get_layout

APP = Dash("auth")

APP.title = c.DASH_TITLE
APP.layout = get_layout()

SERVER = APP.server


if __name__ == '__main__':
    APP.run_server(debug=True)
