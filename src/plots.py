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


def plot_one_invest(df):
    """ Plot stock evolution with one invest at the begging """

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
        title="Realizando sólo una inversión inicial"
    )
    return go.Figure(data=data, layout=layout)


def plot_per_invest(df):
    """ Plot stock evolution with periodics invests over time """

    data = []
    for x in df.columns:
        df_aux = df[[x]].sort_index(ascending=False).dropna()
        df_aux = df_aux.rolling(df.shape[0], min_periods=1).mean()
        data.append(
            go.Scatter(
                x=df_aux.index, y=100*df_aux[x], name=x, marker={"color": get_color_from_name(x)}
            )
        )

    layout = go.Layout(
        xaxis={"title": "Fecha de inversión"},
        yaxis={"title": "Porcentaje ganancias"},
        title="Sólo con aportaciones mensuales (misma cantidad cada mes)"
    )
    return go.Figure(data=data, layout=layout)
