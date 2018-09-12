"""
    Get "indexa capital" data
"""

import os
import requests

import pandas as pd

URI_DF = "../data/indexa.xlsx"
URI_STOCKS = "../data/stocks.xlsx"
URI_DATA = "../data/data.xlsx"
URL = 'https://api.indexacapital.com/plans/mutual/{risk}/history/{size}'
SIZES = {"A": 1000, "B": 10000, "C": 100000}


def get_indexa_real(token=None):
    """ Retrives indexa funds historic data """

    if not token:
        token = os.environ["INDEXA_TOKEN"]

    dfg = pd.DataFrame()
    for pref, size in SIZES.items():
        for risk in range(1, 11):
            res = requests.get(URL.format(size=size, risk=risk), headers={'X-AUTH-TOKEN': token})
            df = pd.DataFrame(res.json()["history_data"]).T.set_index("date")[["return"]]
            df.columns = ["{}{}R".format(pref, risk)]
            dfg = pd.concat([dfg, df], axis=1)

        print("Funds of size {} downloaded".format(size))

    dfg.index = pd.to_datetime(dfg.index)

    dfg = dfg.iloc[-1, :]/dfg
    return dfg.fillna(method="ffill")


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


def get_indexa_calc(df_in):
    """ Get fund prices """
    dist = pd.read_excel(URI_STOCKS, sheet_name="Distribution", index_col=0)
    
    last_v = df_in.iloc[-1, :]

    dfg = pd.DataFrame()

    for size in dist["Size"].unique():
        for i in range(1, 11):
            df = df_in.copy()
            
            percents = dist[dist["Size"] == size].to_dict()
            for x, perc in percents[i].items():
                df[x] = perc*df[x]/100
                
            # Keep only etf presents in plan
            df = (df/last_v)[list(percents[10].keys())]

            df = pd.DataFrame(1/df.sum(axis=1))
            df.columns = ["{}{}C".format(size, i)]

            dfg = pd.concat([dfg, df], axis=1)
        
    return dfg


def main():
    """ Store indexa data """

    dfr = get_indexa_real()
    dfc = get_indexa_calc(get_prices_etfs())

    df = pd.concat([dfr, dfc], axis=1)

    df.to_excel(URI_DF)
    print("Indexa data stored")



if __name__ == '__main__':
    main()
