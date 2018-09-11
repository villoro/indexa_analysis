"""
    Get "indexa capital" data
"""

import os
import requests

import pandas as pd
import plotly.graph_objs as go
import plotly.offline as py

from upalette import get_colors


URI_DF = "../data/indexa.xlsx"
URI_PLOT = "../results/indexa_api.html"
URL = 'https://api.indexacapital.com/plans/mutual/{risk}/history/{size}'
SIZES = {"A": 1000, "B": 10000, "C": 100000}


def get_indexa_funds_data(token=None):
    """ Retrives indexa funds historic data """

    if not token:
        token = os.environ["INDEXA_TOKEN"]

    dfg = pd.DataFrame()
    for pref, size in SIZES.items():
        for risk in range(1, 11):
            res = requests.get(URL.format(size=size, risk=risk), headers={'X-AUTH-TOKEN': token})
            df = pd.DataFrame(res.json()["history_data"]).T.set_index("date")[["return"]]
            df.columns = ["{}{}".format(pref, risk)]
            dfg = pd.concat([dfg, df], axis=1)

        print("Funds of size {} downloaded".format(size))

    dfg = dfg.iloc[-1, :]/dfg
    return dfg.fillna(method="ffill")


def plot_indexa_api(df=None):
    """ plot indexa calc """
    if df is not None:
        df = pd.read_excel(URI_DF)

    colors = {"A": "orange", "B": "light blue", "C": "green"}

    data = []
    for size, c_name in colors.items():
        for x in range(10):
            name = "{}{}".format(size, x + 1)
            color = get_colors((c_name, max(50, x*100)))
            data.append(go.Scatter(x=df.index, y=df[name], name=name, marker={"color": color}))

    py.plot(data, filename=URI_PLOT)
    print("Plot {} saved".format(URI_PLOT))


def main():
    """ Store indexa data """

    df = get_indexa_funds_data()
    df.to_excel(URI_DF)
    print("Indexa data stored")

    plot_indexa_api(df)



if __name__ == '__main__':
    main()
