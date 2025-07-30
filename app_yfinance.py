import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="ALPHA METRICS (Stock Analysis) - by Pallav", layout="wide")

# --- SIDEBAR with custom CSS ---
with st.sidebar:
    # Inject custom styles
    st.markdown(
        """
        <style>
        .sidebar-logo {
            display: flex;
            align-items: center;
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 15px;
        }
        .sidebar-logo span {
            margin-left: 8px;
        }
        .linkedin-link {
            font-size: 16px;
            margin-bottom: 25px;
            display: flex;
            align-items: center;
            text-decoration: none;
            color: #339af0;
        }
        .linkedin-link:hover {
            color: #1d7ed2;
        }
        hr {
            margin: 20px 0;
            border: 1px solid #555;
        }
        label, p {
            color: #ffffff !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Logo and title
    st.markdown(
        """
        <div class="sidebar-logo">
            🔍 <span>ALPHAMETRICS</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # LinkedIn link
    st.markdown(
        """
        <a class="linkedin-link" href="https://www.linkedin.com/in/pallav-ukey-4364a1301/" target="_blank">
            🔗 LinkedIn Profile
        </a>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<hr>", unsafe_allow_html=True)

    # Ticker input
    st.subheader("📈 Stock Ticker Input")
    st.markdown("Enter a valid stock ticker (e.g., AAPL, TSLA, MSFT, BMW.DE, BLK)")
    ticker = st.text_input(" ", value="AAPL")

    # Time Period
    st.markdown("Select Time Period")
    period = st.selectbox(" ", options=["1d", "5d", "1mo", "3mo", "6mo", "1y", "5y", "10y", "ytd", "max"], index=4)

    # Interval
    st.markdown("Select Interval")
    interval = st.selectbox(" ", options=["1m", "5m", "15m", "30m", "1h", "1d", "5d", "1wk", "1mo"], index=5)

# --- MAIN APP ---

try:
    data = yf.download(ticker, period=period, interval=interval)

    if not data.empty:
        st.success("✅ Data fetched successfully.")
        st.dataframe(data.tail())

        # Close price chart
        st.line_chart(data["Close"], use_container_width=True)

        # Moving Average
        ma_days = st.slider("Select Moving Average Window (days)", min_value=5, max_value=50, value=20)
        data[f"MA_{ma_days}"] = data["Close"].rolling(window=ma_days).mean()

        st.line_chart(data[[f"MA_{ma_days}", "Close"]], use_container_width=True)
    else:
        st.warning("⚠️ No data found. Please check the ticker symbol.")

except Exception as e:
    st.error("🚨 Error fetching data. Please ensure the ticker is correct.")

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
    historical = yf.download(ticker, start='1999-01-01', end='2025-07-27')
    st.dataframe(historical.tail())

    # Real-time price
    try:
        price = stock.history(period='2d')['Close'].iloc[-1]
        st.metric(label=f"{ticker.upper()} Real-Time Price (Close)", value=f"${price:.2f}")
    except:
        st.warning("Real-time price not available.")

    # Financials
    st.subheader("📑 Financials")
    st.write("**Balance Sheet:**")
    st.dataframe(stock.balance_sheet)

    st.write("**Income Statement:**")
    st.dataframe(stock.financials)

    # Pie Chart of Monthly Volume
    st.subheader("📦 Monthly Trading Volume (Last 6 Months)")
    hist = stock.history(period="6mo")
    monthly_volume = hist['Volume'].resample('M').sum()

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(monthly_volume, labels=monthly_volume.index.strftime('%b %Y'),
           autopct='%1.1f%%', colors=plt.cm.Paired.colors)
    ax.set_title(f'{ticker.upper()} - Monthly Volume Distribution')
    st.pyplot(fig)
