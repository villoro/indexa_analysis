"""
    Dash app
"""

import pandas as pd
from dash import Dash
from dash.dependencies import Input, Output

import plots
import constants as c
from layout import get_layout

APP = Dash("auth")
APP.config.supress_callback_exceptions = True

APP.title = c.DASH_TITLE
APP.layout = get_layout()

SERVER = APP.server

DF = pd.read_excel("data/indexa.xlsx")

@APP.callback(Output("plot_evo", "figure"),
              [Input("drop_method", "values"),
               Input("drop_size", "values"),
               Input("drop_risk", "values")])
#pylint: disable=unused-variable,unused-argument
def update_plot_evolution(method, sizes, risks):
    """ Updates the evolution plot """

    cols = []
    for x in DF.columns:
        if (x[0] in sizes) and (int(x[1:-1]) in risks) and (x[-1] in method):
            cols.append(x)

    return plots.plot_evolution(DF[cols])


if __name__ == '__main__':
    APP.run_server(debug=True)
