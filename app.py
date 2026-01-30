import streamlit as st
import yfinance as yf
import plotly.express as px

st.set_page_config(page_title="Stock Dashboard", layout="wide")

st.title("📈 Real-Time Stock Market Dashboard")
st.write("Track live stock prices and trends easily")

# Sidebar
st.sidebar.header("Stock Selection")
stock_symbol = st.sidebar.text_input("Enter Stock Symbol", "AAPL")
period = st.sidebar.selectbox("Select Time Period", ["7d", "1mo", "3mo"])
interval = st.sidebar.selectbox("Select Interval", ["1d", "1h"])

try:
    data = yf.download(stock_symbol, period=period, interval=interval)

    if data.empty:
        st.error("No data found")
    else:
        # ✅ FIX: flatten column names
        data.columns = data.columns.get_level_values(0)

        st.success(f"Showing data for {stock_symbol}")

        latest_price = float(data["Close"].iloc[-1])
        previous_price = float(data["Close"].iloc[-2])
        price_change = latest_price - previous_price
        volume = int(data["Volume"].iloc[-1])

        col1, col2, col3 = st.columns(3)
        col1.metric("📌 Latest Price", round(latest_price, 2))
        col2.metric("📉 Price Change", round(price_change, 2))
        col3.metric("📊 Volume", volume)

        # Line chart
        fig = px.line(
            data,
            x=data.index,
            y="Close",
            title="Closing Price Trend"
        )
        st.plotly_chart(fig, use_container_width=True)

        # Moving average
        st.subheader("📉 Moving Average")
        ma = data["Close"].rolling(10).mean()
        fig2 = px.line(
            x=data.index,
            y=[data["Close"], ma],
            labels={"value": "Price"},
            title="Price with Moving Average"
        )
        st.plotly_chart(fig2, use_container_width=True)

        st.subheader("📄 Recent Data")
        st.dataframe(data.tail())

except Exception as e:
    st.error("Something went wrong!")
    st.code(e)
