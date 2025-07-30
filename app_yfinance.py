import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

st.set_page_config(page_title="Stock Analysis App", layout="centered")

st.title("📈 Stock Analysis Dashboard")

# User input
ticker = st.text_input("Enter Company Ticker (e.g. TSLA, AAPL, MSFT):", value="TSLA")

if ticker:
    stock = yf.Ticker(ticker)

    # Basic Info
    info = stock.info
    st.subheader("📊 Company Info")
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
    monthly_volume = hist['Volume'].resample('M').sum()

    fig, ax = plt.subplots(figsize=(6,6))
    ax.pie(monthly_volume, labels=monthly_volume.index.strftime('%b %Y'),
           autopct='%1.1f%%', colors=plt.cm.Paired.colors)
    ax.set_title(f'{ticker} - Monthly Volume Distribution')
    st.pyplot(fig)
