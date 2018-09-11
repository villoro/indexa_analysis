"""
    Get "indexa capital" data
"""

import pandas as pd
import plotly.graph_objs as go
import plotly.offline as py

from upalette import get_colors


URI_STOCKS = "../data/stocks.xlsx"
URI_DATA = "../data/data.xlsx"
URI_PLOT = "../results/indexa_calc.html"
URL = 'https://api.indexacapital.com/plans/mutual/{risk}/history/{size}'
SIZES = {"A": 1000, "B": 10000, "C": 100000}


def get_prices_etfs():
    """ Get base etfs prices """
    df = pd.read_excel(URI_STOCKS, sheet_name="List", index_col=1)
    stocks = df["Name"].to_dict()
    
    dfg = pd.DataFrame()

    for stock in stocks.keys():
        df = pd.read_excel(URI_DATA, sheet_name=stock, index_col=0)[["Close"]]
        df.columns = [stock]

        # Add data for all days
        df_aux = pd.DataFrame(index=pd.date_range(df.index.min(), df.index.max()))
        df = pd.concat([df_aux, df], axis=1).fillna(method='ffill')

        dfg = pd.concat([dfg, df], axis=1)

    dfg.dropna(inplace=True)
    
    return dfg[dfg.index.is_month_end]


def get_prices_funds(df_in):
    """ Get fund prices """
    dist = pd.read_excel(URI_STOCKS, sheet_name="Distribution", index_col=0).to_dict()
    
    last_v = df_in.iloc[-1, :]
    
    dfg = pd.DataFrame()

    for i in range(1, 11):
        df = df_in.copy()

        for x, perc in dist[i].items():
            df[x] = perc*df[x]/100

        df = pd.DataFrame(1/(df/last_v).sum(axis=1))
        df.columns = ["B{}".format(i)]

        dfg = pd.concat([dfg, df], axis=1)
        
    return dfg

def plot_indexa_calc(df):
    data = []

    for x in df.columns:
        color = get_colors(("blue", max(50, (int(x[1:]) - 1)*100)))
        data.append(go.Scatter(x=df.index, y=df[x], name=x, marker={"color": color}))

    py.plot(data, filename=URI_PLOT)
    print("Plot {} saved".format(URI_PLOT))


def main():
    """ Store indexa data """

    df = get_prices_funds(get_prices_etfs())
    print("Indexa data calculated")
    plot_indexa_calc(df)



if __name__ == '__main__':
    main()
