import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
import graphviz
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import model_to_dot
from tensorflow.keras.initializers import glorot_uniform

st.title('Streamlit Stock Dashboard')

ticker = st.sidebar.text_input('Ticker')
start_date = st.sidebar.date_input('Start Date')
end_date = st.sidebar.date_input('End Date')

data = yf.download(ticker, start=start_date, end=end_date)

fig = px.line(data, x=data.index, y=data['Adj Close'], title=ticker)
st.plotly_chart(fig)

pricing_data, fundamental_data, news, model_summary = st.columns(4)

with pricing_data:
    st.header("Price Movements")
    data2 = data.copy()
    data2['% Change'] = data2['Adj Close'] / data2['Adj Close'].shift(1) - 1
    data2.dropna(inplace=True)
    st.write(data2)
    annual_return = data2['% Change'].mean() * 252 * 100
    st.write('Annual Return is ', annual_return, '%')
    stdev = np.std(data2['% Change']) * np.sqrt(252)
    st.write('Standard Deviation is ', stdev * 100, '%')
    st.write('Risk Adj. Return is ', annual_return / (stdev * 100))

from alpha_vantage.fundamentaldata import FundamentalData   
with fundamental_data:
    key = '92T3GUUYXY4KHTGG'  # Replace this with your actual API key
    fd = FundamentalData(key, output_format='pandas')
    st.subheader('Balance Sheet')
    balance_sheet = fd.get_balance_sheet_annual(ticker)[0]
    bs = balance_sheet.T[2:]
    bs.columns = list(balance_sheet.T.iloc[0])
    st.write(bs)
    st.subheader('Income Statement')
    income_statement = fd.get_income_statement_annual(ticker)[0]
    is1 = income_statement.T[2:]
    is1.columns = list(income_statement.T.iloc[0])
    st.write(is1)
    st.subheader('Cash Flow Statement')
    cash_flow = fd.get_cash_flow_annual(ticker)[0]
    cf = cash_flow.T[2:]
    cf.columns = list(cash_flow.T.iloc[0])
    st.write(cf)

from stocknews import StockNews
with news:
    st.header(f'News of {ticker}')
    sn = StockNews(ticker, save_news=False)
    df_news = sn.read_rss()
    for i in range(10):
        st.subheader(f'News {i+1}')
        st.write(df_news['published'][i])
        st.write(df_news['title'][i])
        st.write(df_news['summary'][i])
        title_sentiment = df_news['sentiment_title'][i]
        st.write(f'Title Sentiment {title_sentiment}')
        news_sentiment = df_news['sentiment_summary'][i]
        st.write(f'News Sentiment {news_sentiment}')

with model_summary:
    st.header('Keras Model Summary')

    # Load the Keras model with modified initializer
    model = load_model('keras_model.h5', custom_objects={'Orthogonal': glorot_uniform()})

    # Display model summary
    model_summary_str = []
    model.summary(print_fn=lambda x: model_summary_str.append(x))
    model_summary_str = "\n".join(model_summary_str)
    st.text(model_summary_str)

    # Visualize model architecture
    dot = model_to_dot(model, show_shapes=True, show_layer_names=True)
    st.graphviz_chart(dot.to_string())

