import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px

st.set_page_config(layout="wide")
st.title('📈 Streamlit Stock Dashboard')

# ---------------- Sidebar ----------------
ticker = st.sidebar.text_input('Ticker', 'AAPL').upper()
start_date = st.sidebar.date_input('Start Date')
end_date = st.sidebar.date_input('End Date')

# ---------------- Validation ----------------
if start_date >= end_date:
    st.error("❌ End date must be after start date")
    st.stop()

# ---------------- Data Fetch ----------------
@st.cache_data(show_spinner=False)
def load_data(ticker, start, end):
    return yf.download(ticker, start=start, end=end, progress=False)

data = load_data(ticker, start_date, end_date)

if data.empty:
    st.error("❌ No data found. Possible reasons:\n- Market closed day\n- Invalid ticker\n- Same start & end date\n- Yahoo API issue")
    st.stop()

# ---------------- Column Fix ----------------
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

# ---------------- Adj Close Fallback ----------------
price_col = None
if 'Adj Close' in data.columns:
    price_col = 'Adj Close'
elif 'Close' in data.columns:
    price_col = 'Close'
else:
    st.error("❌ No price column found (Adj Close / Close missing)")
    st.stop()

# ---------------- Chart ----------------
fig = px.line(
    data,
    x=data.index,
    y=price_col,
    title=f"{ticker} Price Chart",
)
st.plotly_chart(fig, use_container_width=True)

# ---------------- Tabs ----------------
pricing_data, fundamental_data, news = st.tabs(["📊 Pricing Data", "📑 Fundamental Data", "📰 Top News"])

# ================= Pricing Tab =================
with pricing_data:
    st.header("📊 Price Movements")

    data2 = data.copy()
    data2['% Change'] = data2[price_col].pct_change()
    data2.dropna(inplace=True)

    st.dataframe(data2.tail(200), use_container_width=True)

    annual_return = data2['% Change'].mean() * 252 * 100
    stdev = np.std(data2['% Change']) * np.sqrt(252)

    col1, col2, col3 = st.columns(3)
    col1.metric("Annual Return (%)", round(annual_return, 2))
    col2.metric("Volatility (%)", round(stdev*100, 2))
    col3.metric("Risk Adjusted Return", round(annual_return/(stdev*100), 2))

# ================= Fundamentals =================
with fundamental_data:
    st.header("📑 Fundamental Data")

    try:
        from alpha_vantage.fundamentaldata import FundamentalData

        key = 'Q6S1E03BJZP9TBBN'
        fd = FundamentalData(key, output_format='pandas')

        st.subheader('Balance Sheet')
        balance_sheet = fd.get_balance_sheet_annual(ticker)[0]
        bs = balance_sheet.T[2:]
        bs.columns = list(balance_sheet.T.iloc[0])
        st.dataframe(bs, use_container_width=True)

        st.subheader('Income Statement')
        income_statement = fd.get_income_statement_annual(ticker)[0]
        is1 = income_statement.T[2:]
        is1.columns = list(income_statement.T.iloc[0])
        st.dataframe(is1, use_container_width=True)

        st.subheader('Cash Flow Statement')
        cash_flow = fd.get_cash_flow_annual(ticker)[0]
        cf = cash_flow.T[2:]
        cf.columns = list(cash_flow.T.iloc[0])
        st.dataframe(cf, use_container_width=True)

    except Exception as e:
        st.error("❌ Fundamental data error")
        st.code(str(e))

# ================= News =================
with news:
    st.header(f'📰 News of {ticker}')

    try:
        from stocknews import StockNews
        sn = StockNews(ticker, save_news=False)
        df_news = sn.read_rss()

        if df_news.empty:
            st.info("No news found.")
        else:
            max_news = min(10, len(df_news))
            for i in range(max_news):
                st.subheader(f'News {i+1}')
                st.write(df_news['published'].iloc[i])
                st.write(df_news['title'].iloc[i])
                st.write(df_news['summary'].iloc[i])
                st.write(f"Title Sentiment: {df_news['sentiment_title'].iloc[i]}")
                st.write(f"News Sentiment: {df_news['sentiment_summary'].iloc[i]}")
                st.divider()

    except Exception as e:
        st.error("❌ News system error")
        st.code(str(e))