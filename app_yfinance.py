import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="ALPHA METRICS (Stock Analysis) -by Pallav", layout="wide")

# --- SIDEBAR ---
with st.sidebar:
    ticker = st.text_input("Ticker Symbol", "AAPL")
    period = st.selectbox("Time Period", [...])
    interval = st.selectbox("Interval", [...])

# Check for empty ticker
if not ticker:
    st.warning("Please enter a valid ticker symbol.")
    st.stop()

# Try fetching data
try:
    data = yf.download(ticker, period=period, interval=interval)
    ...

# App title
st.title("📊 ALPHAMETRICS (Stock Analysis Dashboard) -by Pallav")
st.subheader(f"Showing data for: `{ticker.upper()}`")

# User input
ticker = st.text_input("Enter Company Ticker (e.g. TSLA, AAPL, MSFT):", value="TSLA")

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

if ticker:
    stock = yf.Ticker(ticker)

    # Basic Info
    info = stock.info
    st.subheader("🏢 Company Info")
    st.write(f"**Name:** {info.get('longName', 'N/A')}")
    st.write(f"**Sector:** {info.get('sector', 'N/A')}")
    st.write(f"**Industry:** {info.get('industry', 'N/A')}")
    st.write(f"**Market Cap:** {info.get('marketCap', 'N/A')}")
    st.write(f"**P/E Ratio:** {info.get('trailingPE', 'N/A')}")

    # Historical Data
    st.subheader("📉 Historical Data (since 1999)")
    data = yf.download(ticker, start='1999-01-01', end='2025-07-27')
    st.dataframe(data.tail())

    # Real-time price
    price = stock.history(period='2d')['Close'][0]
    st.metric(label=f"{ticker} Real-Time Price (Close)", value=f"${price:.2f}")

    # Financial Statements
    st.subheader("📑 Financials")
    st.write("**Balance Sheet:**")
    st.dataframe(stock.balance_sheet)

    st.write("**Income Statement:**")
    st.dataframe(stock.financials)

    # Monthly Volume Pie Chart
    st.subheader("📦 Monthly Trading Volume (Last 6 Months)")
    hist = stock.history(period="6mo")
    monthly_volume = hist['Volume'].resample('ME').sum()

    fig, ax = plt.subplots(figsize=(6,6))
    ax.pie(monthly_volume, labels=monthly_volume.index.strftime('%b %Y'),
           autopct='%1.1f%%', colors=plt.cm.Paired.colors)
    ax.set_title(f'{ticker} - Monthly Volume Distribution')
    st.pyplot(fig)
