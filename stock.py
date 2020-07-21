import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from stockstats import StockDataFrame as Sdf
import dash_bootstrap_components as dbc
import dash_table as dt
import yahoo_fin.stock_info as yf
from datetime import datetime, timedelta, date
import plotly.graph_objs as go
import pickle
import numpy as np
import pandas as pd
import random
import numpy



# defining style color
colors = {"background": "#333333", "text": "#00FFFF"}

with open("tickers.pickle", "rb") as f:
    ticker_list = pickle.load(f)



# gainers of the day data and graph
gainer_data = []
gainers_df = yf.get_day_gainers()
g_layout = {
    "plot_bgcolor": colors["background"],
    "paper_bgcolor": colors["background"],
    "font": {"color": colors["text"]},
}
gainer_data.append(go.Bar(x=list(gainers_df.Symbol),
                          y=list(gainers_df["% Change"])))


# loosers of the day data and graph
loosers_data = []
loosers_df = yf.get_day_losers()
l_layout = {
    "plot_bgcolor": colors["background"],
    "paper_bgcolor": colors["background"],
    "font": {"color": colors["text"]},
}
loosers_data.append(go.Bar(x=list(loosers_df.Symbol),
                           y=list(loosers_df["% Change"])))


external_stylesheets = [dbc.themes.DARKLY]


# adding css
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(
    [
        # header
        html.Br(),
        html.Br(),
        dbc.Col(
            html.Header(
                [
                    html.H1(
                        "Stock Dashboard",
                        style={"textAlign": "center", "color": colors["text"]},
                    )
                ],
                className="h1",
            ),
            width={"size": 10, "offset": 1},
        ),
        html.Div(html.Br()),
        html.Div(html.Br()),
        html.Div(html.Br()),
        html.Div(html.Br()),
        # dropdowns
        # ticker input
        dbc.Col(
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Dropdown(
                            id="stock_name",
                            options=[
                                {
                                    "label": str(ticker_list[i]),
                                    "value": str(ticker_list[i]),
                                }
                                for i in range(len(ticker_list))
                            ],
                            searchable=True, 
                            value=str(random.choice(
                                ['tsla', 'GOOGL', 'F', 'GE', 'AAL', 'DIS', 'DAL', 'AAPL', 'MSFT', 'CCL', 'GPRO', 'ACB', 'PLUG', 'AMZN'])),
                            placeholder="enter stock name",
                            style = {'color':'#000000'}
                        ),
                        width={"size": 3},

                    ),
                    # Graph selection dropdown
                    dbc.Col(
                        dcc.Dropdown(
                            id="chart",
                            options=[
                                {"label": "line", "value": "Line"},
                                {"label": "candlestick", "value": "Candlestick"},
                                {"label": "Simple moving average", "value": "SMA"},
                                {"label": "Exponential moving average",
                                    "value": "EMA"},
                                {"label": "MACD", "value": "MACD"},
                                {"label": "RSI", "value": "RSI"},
                                {"label": "OHLC", "value": "OHLC"},
                            ],
                            value="Line",
                            style = {'color':'#000000'}
                        ),
                        width={"size": 3},
                    ),
                    # submit button
                    dbc.Col(
                        dbc.Button('Plot',
                                   id="submit-button-state",
                                   className="mr-1",
                                   n_clicks=1,
                                   ),
                        width={"size": 1},
                    )
                ],
                justify="center",
            ),
            width={"size": 10, "offset": 1},

        ),
        # Graph
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="graph"), width={"size": 9}),
                # Stock info table
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(dcc.Graph(id="live price")),
                            dbc.CardBody(
                                [
                                    dt.DataTable(
                                        id="info",
                                        style_table={"height": 500},
                                        style_cell={
                                            "white_space": "normal",
                                            "height": "auto",
                                            "backgroundColor": colors["background"],
                                            "color": "white",
                                            "font_size": "15px",
                                        },
                                        style_data={"border": "#4d4d4d"},
                                        style_header={
                                            "backgroundColor": colors["background"],
                                            "fontWeight": "bold",
                                            "border": "#4d4d4d",
                                        },
                                        style_cell_conditional=[
                                            {'if': {'column_id': 'attribute'},
                                             'width': '140'},
                                            {'if': {'column_id': 'value'},
                                             'width': '150'}
                                        ]
                                    )
                                ]
                            ),

                        ]
                    ),
                ),
            ]
        ),
        html.Div(html.Br()),
        # Gainers of the day
        # header
        html.Div(
            html.H2(
                "Top Gainers of the day",
                style={"textAlign": "center", "color": colors["text"]},
            )
        ),
        # Data table
        html.Div(
            dbc.Col(
                dt.DataTable(
                    id="gainers",
                    columns=[{"name": i, "id": i} for i in gainers_df.columns],
                    data=gainers_df.to_dict("records"),
                    fixed_rows={"headers": True},
                    style_table={"height": 400},
                    style_cell={
                        "white_space": "normal",
                        "height": "auto",
                        "backgroundColor": colors["background"],
                        "color": "white",
                        "font_size": "15px",
                    },
                    style_data={"border": "#4d4d4d"},
                    style_header={
                        "backgroundColor": colors["background"],
                        "fontWeight": "bold",
                        "border": "#4d4d4d",
                    },
                ),
                width={"size": 12},
            )
        ),
        html.Br(),
        html.Br(),
        # Gainers graph
        html.Div(
            dbc.Col(
                dcc.Graph(
                    id="gainers_graph", figure={"data": gainer_data, "layout": g_layout}
                ),
                width={"size": 12},
            )
        ),
        html.Div(html.Br()),
        # loosers of the day
        # header
        html.Div(
            html.H2(
                "Top Loosers of the day",
                style={"textAlign": "center", "color": colors["text"]},
            )
        ),
        # Data table
        html.Div(
            dbc.Col(
                dt.DataTable(
                    id="loosers",
                    columns=[{"name": i, "id": i} for i in gainers_df.columns],
                    data=loosers_df.to_dict("records"),
                    fixed_rows={"headers": True},
                    style_table={"height": 400},
                    style_cell={
                        "white_space": "normal",
                        "height": "auto",
                        "backgroundColor": colors["background"],
                        "color": "white",
                        "font_size": "15px",
                    },
                    style_data={"border": "34d4d4d"},
                    style_header={
                        "backgroundColor": colors["background"],
                        "fontWeight": "bold",
                        "border": "#4d4d4d",
                    },
                ),
                width={"size": 10, "offset": 1},
            )
        ),
        html.Br(),
        html.Br(),
        # Loosers graph
        html.Div(
            dbc.Col(
                dcc.Graph(
                    id="loosers_graph",
                    figure={"data": loosers_data, "layout": l_layout},
                ),
                width={"size": 10, "offset": 1},
            )
        ),
    ]
)


# Callback main graph
@app.callback(
    # output
    [Output("graph", "figure"), Output("live price", "figure")],
    # input
    [Input("submit-button-state", "n_clicks")],
    # state
    [State("stock_name", "value"), State("chart", "value")],
)
def graph_genrator(n_clicks, ticker, chart_name):

    if n_clicks >= 1:  # Checking for user to click submit button

        # loading data
        start_date = datetime.now().date() - timedelta(days=5 * 365)
        end_data = datetime.now().date()
        df = yf.get_data(
            ticker, start_date=start_date, end_date=end_data, interval="1d"
        )
        stock  = Sdf(df)

        # selecting graph type

        # line plot
        if chart_name == "Line":
            fig = go.Figure(
                data=[
                    go.Scatter(
                        x=list(df.index), y=list(df.close), fill="tozeroy", name="close"
                    )
                ],
                layout={
                    "height": 900,
                    "title": chart_name,
                    "showlegend": True,
                    "plot_bgcolor": colors["background"],
                    "paper_bgcolor": colors["background"],
                    "font": {"color": colors["text"]},
                },
            )

            fig.update_xaxes(
                rangeslider_visible=True,
                rangeselector=dict(activecolor = 'blue',bgcolor = colors['background'],
                    buttons=list(
                        [
                            dict(count=7, label="10D",
                                 step="day", stepmode="backward"),
                            dict(
                                count=15, label="15D", step="day", stepmode="backward"
                            ),
                            dict(
                                count=1, label="1m", step="month", stepmode="backward"
                            ),
                            dict(
                                count=3, label="3m", step="month", stepmode="backward"
                            ),
                            dict(
                                count=6, label="6m", step="month", stepmode="backward"
                            ),
                            dict(count=1, label="1y", step="year",
                                 stepmode="backward"),
                            dict(count=5, label="5y", step="year",
                                 stepmode="backward"),
                            dict(count=1, label="YTD",
                                 step="year", stepmode="todate"),
                            dict(step="all"),
                        ]
                    )
                ),
            )

        # Candelstick
        if chart_name == "Candlestick":
            fig = go.Figure(
                data=[
                    go.Candlestick(
                        x=list(df.index),
                        open=list(df.open),
                        high=list(df.high),
                        low=list(df.low),
                        close=list(df.close),
                        name="Candlestick",
                    )
                ],
                layout={
                    "height": 900,
                    "title": chart_name,
                    "showlegend": True,
                    "plot_bgcolor": colors["background"],
                    "paper_bgcolor": colors["background"],
                    "font": {"color": colors["text"]},
                },
            )

            fig.update_xaxes(
                rangeslider_visible=True,
                rangeselector=dict(activecolor = 'blue',bgcolor = colors['background'],
                    buttons=list(
                        [
                            dict(count=7, label="10D",
                                 step="day", stepmode="backward"),
                            dict(
                                count=15, label="15D", step="day", stepmode="backward"
                            ),
                            dict(
                                count=1, label="1m", step="month", stepmode="backward"
                            ),
                            dict(
                                count=3, label="3m", step="month", stepmode="backward"
                            ),
                            dict(
                                count=6, label="6m", step="month", stepmode="backward"
                            ),
                            dict(count=1, label="1y", step="year",
                                 stepmode="backward"),
                            dict(count=5, label="5y", step="year",
                                 stepmode="backward"),
                            dict(count=1, label="YTD",
                                 step="year", stepmode="todate"),
                            dict(step="all"),
                        ]
                    )
                ),
            )

        # simple oving average
        if chart_name == "SMA":
            close_ma_10 = df.close.rolling(10).mean()
            close_ma_15 = df.close.rolling(15).mean()
            close_ma_30 = df.close.rolling(30).mean()
            close_ma_100 =df.close.rolling(100).mean()
            fig = go.Figure(
                data=[
                    go.Scatter(
                        x=list(close_ma_10.index), y=list(close_ma_10), name="10 Days"
                    ),
                    go.Scatter(
                        x=list(close_ma_15.index), y=list(close_ma_15), name="15 Days"
                    ),
                    go.Scatter(
                        x=list(close_ma_30.index), y=list(close_ma_15), name="30 Days"
                    ),
                    go.Scatter(
                        x=list(close_ma_100.index), y=list(close_ma_15), name="100 Days"
                    ),
                ],
                layout={
                    "height": 900,
                    "title": chart_name,
                    "showlegend": True,
                    "plot_bgcolor": colors["background"],
                    "paper_bgcolor": colors["background"],
                    "font": {"color": colors["text"]},
                },
            )

            fig.update_xaxes(
                rangeslider_visible=True,
                rangeselector=dict(activecolor = 'blue',bgcolor = colors['background'],
                    buttons=list(
                        [
                            dict(count=7, label="10D",
                                 step="day", stepmode="backward"),
                            dict(
                                count=15, label="15D", step="day", stepmode="backward"
                            ),
                            dict(
                                count=1, label="1m", step="month", stepmode="backward"
                            ),
                            dict(
                                count=3, label="3m", step="month", stepmode="backward"
                            ),
                            dict(
                                count=6, label="6m", step="month", stepmode="backward"
                            ),
                            dict(count=1, label="1y", step="year",
                                 stepmode="backward"),
                            dict(count=5, label="5y", step="year",
                                 stepmode="backward"),
                            dict(count=1, label="YTD",
                                 step="year", stepmode="todate"),
                            dict(step="all"),
                        ]
                    )
                ),
            )

        # Open_high_low_close
        if chart_name == "OHLC":
            fig = go.Figure(
                data=[
                    go.Ohlc(
                        x=df.index,
                        open=df.open,
                        high=df.high,
                        low=df.low,
                        close=df.close,
                    )
                ],
                layout={
                    "height": 900,
                    "title": chart_name,
                    "showlegend": True,
                    "plot_bgcolor": colors["background"],
                    "paper_bgcolor": colors["background"],
                    "font": {"color": colors["text"]},
                },
            )

            fig.update_xaxes(
                rangeslider_visible=True,
                rangeselector=dict(activecolor = 'blue',bgcolor = colors['background'],
                    buttons=list(
                        [
                            dict(count=7, label="10D",
                                 step="day", stepmode="backward"),
                            dict(
                                count=15, label="15D", step="day", stepmode="backward"
                            ),
                            dict(
                                count=1, label="1m", step="month", stepmode="backward"
                            ),
                            dict(
                                count=3, label="3m", step="month", stepmode="backward"
                            ),
                            dict(
                                count=6, label="6m", step="month", stepmode="backward"
                            ),
                            dict(count=1, label="1y", step="year",
                                 stepmode="backward"),
                            dict(count=5, label="5y", step="year",
                                 stepmode="backward"),
                            dict(count=1, label="YTD",
                                 step="year", stepmode="todate"),
                            dict(step="all"),
                        ]
                    )
                ),
            )

        # Exponential moving average
        if chart_name == "EMA":
            close_ema_10 =df.close.ewm(span = 10).mean
            close_ema_15 = df.close.ewm(span = 15).mean
            close_ema_30 = df.close.ewm(span = 30).mean
            close_ema_100 = df.close.ewm(span = 100).mean
            fig = go.Figure(
                data=[
                    go.Scatter(
                        x=list(close_ema_10.index), y=list(close_ema_10), name="10 Days"
                    ),
                    go.Scatter(
                        x=list(close_ema_15.index), y=list(close_ema_15), name="15 Days"
                    ),
                    go.Scatter(
                        x=list(close_ema_30.index), y=list(close_ema_30), name="30 Days"
                    ),
                    go.Scatter(
                        x=list(close_ema_100.index),
                        y=list(close_ema_100),
                        name="100 Days",
                    ),
                ],
                layout={
                    "height": 900,
                    "title": chart_name,
                    "showlegend": True,
                    "plot_bgcolor": colors["background"],
                    "paper_bgcolor": colors["background"],
                    "font": {"color": colors["text"]},
                },
            )

            fig.update_xaxes(
                rangeslider_visible=True,
                rangeselector=dict(activecolor = 'blue',bgcolor = colors['background'],
                    buttons=list(
                        [
                            dict(count=7, label="10D",
                                 step="day", stepmode="backward"),
                            dict(
                                count=15, label="15D", step="day", stepmode="backward"
                            ),
                            dict(
                                count=1, label="1m", step="month", stepmode="backward"
                            ),
                            dict(
                                count=3, label="3m", step="month", stepmode="backward"
                            ),
                            dict(
                                count=6, label="6m", step="month", stepmode="backward"
                            ),
                            dict(count=1, label="1y", step="year",
                                 stepmode="backward"),
                            dict(count=5, label="5y", step="year",
                                 stepmode="backward"),
                            dict(count=1, label="YTD",
                                 step="year", stepmode="todate"),
                            dict(step="all"),
                        ]
                    )
                ),
            )

        # Moving average convergence divergence
        if chart_name == "MACD":
            df["MACD"], df["signal"], df["hist"] = stock['macd'],stock['macds'],stock['macdh']
            fig = go.Figure(
                data=[
                    go.Scatter(x=list(df.index), y=list(df.MACD), name="MACD"),
                    go.Scatter(x=list(df.index), y=list(
                        df.signal), name="Signal"),
                    go.Scatter(
                        x=list(df.index),
                        y=list(df["hist"]),
                        line=dict(color="royalblue", width=2, dash="dot"),
                        name="Hitogram",
                    ),
                ],
                layout={
                    "height": 900,
                    "title": chart_name,
                    "showlegend": True,
                    "plot_bgcolor": colors["background"],
                    "paper_bgcolor": colors["background"],
                    "font": {"color": colors["text"]},
                },
            )

            fig.update_xaxes(
                rangeslider_visible=True,
                rangeselector=dict(activecolor = 'blue',bgcolor = colors['background'],
                    buttons=list(
                        [
                            dict(count=7, label="10D",
                                 step="day", stepmode="backward"),
                            dict(
                                count=15, label="15D", step="day", stepmode="backward"
                            ),
                            dict(
                                count=1, label="1m", step="month", stepmode="backward"
                            ),
                            dict(
                                count=3, label="3m", step="month", stepmode="backward"
                            ),
                            dict(
                                count=6, label="6m", step="month", stepmode="backward"
                            ),
                            dict(count=1, label="1y", step="year",
                                 stepmode="backward"),
                            dict(count=5, label="5y", step="year",
                                 stepmode="backward"),
                            dict(count=1, label="YTD",
                                 step="year", stepmode="todate"),
                            dict(step="all"),
                        ]
                    )
                ),
            )

            # Relative strength index
        if chart_name == "RSI":
           rsi_6 = stock['rsi_6']
           rsi_12 = stock['rsi_12']
           fig = go.Figure(
                data=[
                    go.Scatter(x=list(df.index), y=list(rsi_6), name="RSI 6 Day"),
                    go.Scatter(x=list(df.index), y=list(rsi_12), name="RSI 12 Day")
                    ],
                layout={
                    "height": 900,
                    "title": chart_name,
                    "showlegend": True,
                    "plot_bgcolor": colors["background"],
                    "paper_bgcolor": colors["background"],
                    "font": {"color": colors["text"]},
                },
            )
           fig.update_xaxes(rangeslider_visible=True,
                rangeselector=dict(activecolor = 'blue',bgcolor = colors['background'],
                    buttons=list(
                        [
                            dict(count=7, label="10D",
                                 step="day", stepmode="backward"),
                            dict(
                                count=15, label="15D", step="day", stepmode="backward"
                            ),
                            dict(
                                count=1, label="1m", step="month", stepmode="backward"
                            ),
                            dict(
                                count=3, label="3m", step="month", stepmode="backward"
                            ),
                            dict(
                                count=6, label="6m", step="month", stepmode="backward"
                            ),
                            dict(count=1, label="1y", step="year",
                                 stepmode="backward"),
                            dict(count=5, label="5y", step="year",
                                 stepmode="backward"),
                            dict(count=1, label="YTD",
                                 step="year", stepmode="todate"),
                            dict(step="all"),
                        ]
                    )
                ),
            )

    end_data = datetime.now().date()
    start_date = datetime.now().date() - timedelta(days=30)
    res_df = yf.get_data(ticker, start_date=start_date,
                         end_date=end_data, interval="1d")
    price = yf.get_live_price(ticker)
    prev_close = res_df.close.iloc[0]
    prev_high = np.array(res_df.high).max()
    prev_low = np.array(res_df.low).min()

    live_price = go.Figure(
        data=[
            go.Indicator(
                domain={"x": [0, 1], "y": [0, 1]},
                value=price,
                mode="gauge+number+delta",
                title={"text": "Price"},
                delta={"reference": prev_close},
                gauge={
                    "axis": {"range": [None, prev_high + 300], "tickcolor": "blue"},
                    "bar": {"color": "blue"},
                    "bgcolor": "white",
                    "borderwidth": 2,
                    "bordercolor": "gray",
                    "steps": [
                        {"range": [0, prev_low], "color": "red"},
                        {"range": [prev_close - 100, prev_high],
                            "color": "green"},
                    ],
                    "threshold": {
                        "line": {"color": "red", "width": 4},
                        "thickness": 0.75,
                        "value": 490,
                    },
                },
            )
        ],
        layout={
            "height": 300,
            "showlegend": True,
            "plot_bgcolor": colors["background"],
            "paper_bgcolor": colors["background"],
            "font": {"color": colors["text"]},
        },
    )

    return fig, live_price


@app.callback(
    # output
    [Output("info", "columns"), Output("info", "data")],
    # input
    [Input("submit-button-state", "n_clicks")],
    # state
    [State("stock_name", "value")],
)
def quotes_genrator(n_clicks, ticker):
    # info table
    current_stock = yf.get_quote_table(ticker, dict_result=False)
    columns = [{"name": i, "id": i} for i in current_stock.columns]
    t_data = current_stock.to_dict("records")

    # price

    return columns, t_data


if __name__ == "__main__":
    app.run_server(debug=False)

