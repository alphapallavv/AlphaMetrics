import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go

# App Title
st.set_page_config(page_title="ALPHAMETRICS", layout="wide")
st.title("ALPHAMETRICS")

# Sidebar
st.sidebar.title("Navigation")
st.sidebar.markdown("[Connect on LinkedIn](https://www.linkedin.com/in/pallav-ukey-4364a1301/)", unsafe_allow_html=True)

# Ticker Input
ticker_symbol = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA, MSFT)", "AAPL")

# Date Range
start_date = st.date_input("Start Date", pd.to_datetime("2023-01-01"))
end_date = st.date_input("End Date", pd.to_datetime("today"))

# Load data
@st.cache_data
def load_data(symbol, start, end):
    data = yf.download(symbol, start=start, end=end)
    return data

try:
    data = load_data(ticker_symbol, start_date, end_date)

    if data.empty:
        st.warning("No data found for the selected ticker and date range.")
    else:
        st.subheader(f"Stock Price Data for {ticker_symbol.upper()}")
        st.dataframe(data.tail())

        # Candlestick chart
        st.subheader("Candlestick Chart")
        fig = go.Figure(data=[go.Candlestick(x=data.index,
                                             open=data['Open'],
                                             high=data['High'],
                                             low=data['Low'],
                                             close=data['Close'])])
        fig.update_layout(xaxis_rangeslider_visible=False, height=600)
        st.plotly_chart(fig, use_container_width=True)
except Exception as e:
    st.error(f"An error occurred: {e}")
