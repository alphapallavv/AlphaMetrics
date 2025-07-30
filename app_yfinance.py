import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# App Config
st.set_page_config(page_title="ALPHAMETRICS (Stock Analysis)-by Pallav", layout="wide")

# Sidebar
with st.sidebar:
    st.title("🔍 ALPHAMETRICS")
    st.markdown("[Visit my LinkedIn](https://www.linkedin.com/in/pallav-ukey-4364a1301/)", unsafe_allow_html=True)
    st.write("---")
    st.header("Stock Ticker Input")
    ticker = st.text_input("Enter a valid stock ticker (e.g., AAPL, TSLA, MSFT, BMW.DE, BLK)", value="AAPL")
    period = st.selectbox("Select Time Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=2)
    interval = st.selectbox("Select Interval", ["1d", "1h", "1wk"], index=0)

# Main
st.title("📈 Stock Price Dashboard")
st.subheader(f"Showing data for: `{ticker.upper()}`")

try:
    data = yf.download(ticker, period=period, interval=interval)

    if not data.empty:
        st.success("Data fetched successfully.")
        st.dataframe(data.tail())

        # Plot
        st.line_chart(data["Close"], use_container_width=True)

        # Moving Average
        ma_days = st.slider("Select Moving Average Window (days)", min_value=5, max_value=50, value=20)
        data[f"MA_{ma_days}"] = data["Close"].rolling(window=ma_days).mean()

        st.line_chart(data[[f"MA_{ma_days}", "Close"]], use_container_width=True)
    else:
        st.warning("No data found. Please check the ticker symbol.")

except Exception as e:
    st.error("Error fetching data. Please ensure the ticker is correct.")
