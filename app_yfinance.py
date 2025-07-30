import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="ALPHA METRICS (Stock Analysis) -by Pallav", layout="wide")

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## 🔍 **ALPHAMETRICS**", unsafe_allow_html=True)

    st.markdown(
        """
        <a href='https://www.linkedin.com/in/YOUR_LINKEDIN' target='_blank' style='text-decoration: none;'>
            <span style='font-size: 16px;'>🔗 <strong>LinkedIn Profile</strong></span>
        </a>
        """, unsafe_allow_html=True
    )

    st.markdown("---")

    st.subheader("📈 Stock Ticker Input")
    st.write("Enter a valid stock ticker (e.g., AAPL, TSLA, MSFT, BMW.DE, BLK)")
    ticker = st.text_input("Ticker Symbol", "AAPL")

    st.subheader("📆 Select Time Period")
    period = st.selectbox("Time Period", ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"], index=4)

    st.subheader("⏱️ Select Interval")
    interval = st.selectbox("Interval", ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1d", "5d", "1wk", "1mo", "3mo"], index=7)

# --- Main Content ---
st.title(f"📊 ALPHA METRICS - Stock Analysis for {ticker.upper()} -by Pallav")

# User input
ticker = st.text_input("Enter Company Ticker (e.g. TSLA, AAPL, MSFT):", value="TSLA")

try:
    data = yf.download(ticker, period=period, interval=interval)

    # 👉 Fix for MultiIndex columns
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(1)

    if data is not None and not data.empty:
        st.success(f"Data for {ticker.upper()} fetched successfully.")
        st.dataframe(data.tail())

        # Moving Average
        st.subheader("Moving Average")
        ma_days = st.slider("Select Moving Average Window (days)", min_value=5, max_value=50, value=20)

        if "Close" in data.columns and len(data) >= ma_days:
            data[f"MA_{ma_days}"] = data["Close"].rolling(window=ma_days).mean()
            st.line_chart(data[[f"MA_{ma_days}", "Close"]].dropna(), use_container_width=True)
        else:
            st.warning("Not enough data for Moving Average or 'Close' column missing.")
    else:
        st.warning("No data found. Please check the ticker, period, or interval.")

except Exception as e:
    st.error(f"Error fetching data: {str(e)}")
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
