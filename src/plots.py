"""
    Plots
"""

import plotly.graph_objs as go

from upalette import get_colors


def get_color_from_name(name):
    """ Assign color based on encoded name """
    colors = {
        "C": {"A": "amber", "B": "light blue", "C": "light green"},
        "R": {"A": "orange", "B": "blue", "C": "green"}
    }
    size, risk, method = name[0], name[1:-1], name[-1]
    return get_colors((colors[method][size], max(50, (int(risk) - 1)*100)))


def plot_evolution(df):
    """ Plot stock evolution """

    data = []
    for x in df.columns:
        data.append(
            go.Scatter(
                x=df.index, y=100*df[x], name=x, marker={"color": get_color_from_name(x)}
            )
        )

    layout = go.Layout(
        xaxis={"title": "Fecha de inversión"},
        yaxis={"title": "Porcentaje ganancias"},
        title="Porcentaje de ganancias obtenidas en función de la fecha de inversión"
    )

    return go.Figure(data=data, layout=layout)
