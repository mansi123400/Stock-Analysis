import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Page Configuration
st.set_page_config(
    page_title="Stock Market Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Look
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stMetric {
        background-color: #1e2130;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #313348;
    }
    [data-testid="stSidebar"] {
        background-color: #161b22;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.header("🛠️ Configuration")

# Ticker Input
ticker_symbol = st.sidebar.text_input("Stock Ticker Symbol", value="AAPL").upper()

# Date Range Selector (Default last 1 year)
end_date = datetime.now()
start_date_default = end_date - timedelta(days=365)
start_date = st.sidebar.date_input("Start Date", value=start_date_default)
end_date_input = st.sidebar.date_input("End Date", value=end_date)

# Chart Type Selector
chart_type = st.sidebar.selectbox("Choose Chart Type", options=["Candlestick", "Line"])

st.sidebar.markdown("---")
st.sidebar.markdown("Built with ❤️ using Streamlit & yfinance")

# --- MAIN PAGE ---
st.title("📈 Stock Market Dashboard")

# Fetch Data
@st.cache_data(ttl=3600)
def load_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end)
    return data

@st.cache_data(ttl=3600)
def get_ticker_info(ticker):
    return yf.Ticker(ticker).info

try:
    with st.spinner(f"Loading data for {ticker_symbol}..."):
        df = load_data(ticker_symbol, start_date, end_date_input)
        info = get_ticker_info(ticker_symbol)

    if df.empty:
        st.error(f"❌ No data found for ticker '{ticker_symbol}'. Please check the symbol and try again.")
    else:
        # Flatten MultiIndex columns if they exist (common in recent yfinance versions)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
            
        # Ensure we have a standard index for calculations
        df = df.copy()

        # --- ROBUST LOGO FETCHING (Base64 Embedding) ---
        import base64
        import requests
        from io import BytesIO

        def get_company_logo_base64(info, ticker):
            urls_to_try = []
            website = info.get("website", "")
            
            # Layer 1: yfinance logo_url
            logo = info.get("logo_url", "")
            if logo and str(logo).startswith("http"):
                urls_to_try.append(logo)

            # Extract domain cleanly
            domain = ""
            if website:
                domain = website.lower().replace("https://","").replace("http://","").replace("www.","").split("/")[0].split("?")[0]

            # Layer 2: Clearbit
            if domain:
                urls_to_try.append(f"https://logo.clearbit.com/{domain}")

            # Layer 3: logo.dev
            clean_ticker = ticker.lower().split(".")[0] # Get base ticker
            urls_to_try.append(f"https://img.logo.dev/ticker/{clean_ticker}?token=pk_free")

            # Layer 4: Google favicon as last resort
            if domain:
                urls_to_try.append(f"https://www.google.com/s2/favicons?domain={domain}&sz=128")

            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

            for url in urls_to_try:
                try:
                    response = requests.get(url, timeout=5, headers=headers)
                    # Lower threshold to 500 bytes to allow smaller but valid logos
                    if response.status_code == 200 and len(response.content) > 500:
                        encoded = base64.b64encode(response.content).decode("utf-8")
                        # Basic mime type detection
                        mime = "image/png"
                        if "image/svg" in response.headers.get("Content-Type", ""): mime = "image/svg+xml"
                        elif "image/jpeg" in response.headers.get("Content-Type", ""): mime = "image/jpeg"
                        elif "image/x-icon" in response.headers.get("Content-Type", ""): mime = "image/x-icon"
                        
                        return f"data:{mime};base64,{encoded}"
                except:
                    continue

            return None  # All failed

        logo_b64 = get_company_logo_base64(info, ticker_symbol)

        col1, col2 = st.columns([1, 8])

        with col1:
            if logo_b64:
                st.markdown(
                    f'<img src="{logo_b64}" width="70" style="border-radius:10px; margin-top:8px;">',
                    unsafe_allow_html=True
                )
            else:
                st.markdown("<h2 style='margin-top: 8px;'>🏢</h2>", unsafe_allow_html=True)

        with col2:
            company_name = info.get("longName", ticker_symbol)
            sector = info.get("sector", "N/A")
            industry = info.get("industry", "N/A")
            st.markdown(f"## {company_name}")
            st.caption(f"Sector: {sector} | Industry: {industry}")

        # Key Metrics
        st.markdown("### 📊 Market Overview")
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        
        # Get latest day data and ensure they are scalars
        latest_day = df.iloc[-1]
        prev_day = df.iloc[-2] if len(df) > 1 else latest_day
        
        current_price = float(latest_day['Close'])
        price_diff = float(current_price - float(prev_day['Close']))
        price_pct = float((price_diff / float(prev_day['Close'])) * 100)

        m_col1.metric("Current Price", f"${current_price:.2f}", f"{price_diff:.2f} ({price_pct:.2f}%)")
        m_col2.metric("Day High", f"${float(latest_day['High']):.2f}")
        m_col3.metric("Day Low", f"${float(latest_day['Low']):.2f}")
        m_col4.metric("Volume", f"{int(latest_day['Volume']):,.0f}")

        # --- TECHNICAL INDICATORS CALCULATIONS ---
        # SMAs (already calculated)
        df['SMA20'] = df['Close'].rolling(window=20).mean()
        df['SMA50'] = df['Close'].rolling(window=50).mean()

        # Bollinger Bands
        df['BB_Mid'] = df['Close'].rolling(window=20).mean()
        df['BB_Std'] = df['Close'].rolling(window=20).std()
        df['BB_Upper'] = df['BB_Mid'] + (df['BB_Std'] * 2)
        df['BB_Lower'] = df['BB_Mid'] - (df['BB_Std'] * 2)

        # RSI (14-day)
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))

        # MACD
        exp1 = df['Close'].ewm(span=12, adjust=False).mean()
        exp2 = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = exp1 - exp2
        df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        df['MACD_Hist'] = df['MACD'] - df['MACD_Signal']

        # Daily Returns
        df['Returns'] = df['Close'].pct_change()

        # --- TABS SECTION ---
        tab1, tab2, tab3 = st.tabs(["📊 Technical Indicators", "📉 Bollinger Bands", "📈 Returns Analysis"])

        with tab1:
            st.markdown("### RSI & MACD")
            
            # RSI Chart
            fig_rsi = go.Figure()
            fig_rsi.add_trace(go.Scatter(x=df.index, y=df['RSI'], name='RSI', line=dict(color='#8e44ad')))
            fig_rsi.add_hline(y=70, line_dash="dash", line_color="red")
            fig_rsi.add_hline(y=30, line_dash="dash", line_color="green")
            fig_rsi.update_layout(template='plotly_white', height=300, title="RSI (14)", yaxis_range=[0, 100])
            st.plotly_chart(fig_rsi, use_container_width=True)

            # MACD Chart
            fig_macd = go.Figure()
            fig_macd.add_trace(go.Scatter(x=df.index, y=df['MACD'], name='MACD', line=dict(color='blue')))
            fig_macd.add_trace(go.Scatter(x=df.index, y=df['MACD_Signal'], name='Signal', line=dict(color='orange')))
            fig_macd.add_trace(go.Bar(x=df.index, y=df['MACD_Hist'], name='Histogram', marker_color='gray'))
            fig_macd.update_layout(template='plotly_white', height=300, title="MACD (12, 26, 9)")
            st.plotly_chart(fig_macd, use_container_width=True)

        with tab2:
            st.markdown("### Bollinger Bands Overlay")
            fig_bb = go.Figure()
            
            # Price
            fig_bb.add_trace(go.Scatter(x=df.index, y=df['Close'], name='Close Price', line=dict(color='#1f77b4')))
            
            # BB Bands
            fig_bb.add_trace(go.Scatter(x=df.index, y=df['BB_Upper'], name='Upper Band', line=dict(color='rgba(255, 0, 0, 0.2)', dash='dash')))
            fig_bb.add_trace(go.Scatter(x=df.index, y=df['BB_Lower'], name='Lower Band', line=dict(color='rgba(0, 255, 0, 0.2)', dash='dash'), fill='tonexty', fillcolor='rgba(128, 128, 128, 0.1)'))
            fig_bb.add_trace(go.Scatter(x=df.index, y=df['BB_Mid'], name='Middle Band (SMA 20)', line=dict(color='gray', dash='dot')))
            
            fig_bb.update_layout(template='plotly_white', height=600, yaxis_title="Price (USD)")
            st.plotly_chart(fig_bb, use_container_width=True)

        with tab3:
            st.markdown("### Returns Analysis")
            
            # Stats
            avg_return = df['Returns'].mean()
            std_return = df['Returns'].std()
            sharpe_ratio = (avg_return / std_return) * (252**0.5) if std_return != 0 else 0
            
            s_col1, s_col2, s_col3 = st.columns(3)
            s_col1.metric("Mean Daily Return", f"{avg_return:.4%}")
            s_col2.metric("Std Dev (Risk)", f"{std_return:.4%}")
            s_col3.metric("Annualized Sharpe Ratio", f"{sharpe_ratio:.2f}")

            # Histogram
            fig_hist = go.Figure()
            fig_hist.add_trace(go.Histogram(x=df['Returns'].dropna(), nbinsx=50, name='Returns', marker_color='#2ecc71'))
            fig_hist.update_layout(template='plotly_white', height=400, title="Distribution of Daily Returns", xaxis_title="Daily Return", yaxis_title="Frequency")
            st.plotly_chart(fig_hist, use_container_width=True)

        # Main Chart (Primary selection)
        st.markdown("---")
        st.markdown(f"### 📊 Primary Chart: {ticker_symbol}")
        
        from plotly.subplots import make_subplots
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1, row_heights=[0.7, 0.3])
        
        if chart_type == "Candlestick":
            fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='OHLC'), row=1, col=1)
        else:
            fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Close Price', fill='tozeroy', line=dict(color='#1f77b4', width=2), fillcolor='rgba(31, 119, 180, 0.2)'), row=1, col=1)

        fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name='Volume', marker_color='rgba(100, 100, 100, 0.5)'), row=2, col=1)
        fig.update_layout(template='plotly_white', xaxis_rangeslider_visible=False, height=600, margin=dict(l=20, r=20, t=20, b=20), yaxis_title="Price (USD)")
        st.plotly_chart(fig, use_container_width=True)

        # --- COMPARE STOCKS SECTION ---
        st.markdown("---")
        st.markdown("### 🔍 Compare Stocks")
        compare_tickers = st.multiselect("Select up to 5 tickers to compare relative performance", 
                                       options=["AAPL", "TSLA", "GOOGL", "MSFT", "AMZN", "META", "NVDA", "NFLX"], 
                                       default=[ticker_symbol] if ticker_symbol not in ["AAPL", "TSLA"] else ["AAPL", "MSFT"],
                                       max_selections=5)

        if compare_tickers:
            with st.spinner("Fetching comparison data..."):
                comp_data = yf.download(compare_tickers, start=start_date, end=end_date_input)['Close']
                
                if len(compare_tickers) == 1:
                    comp_data = comp_data.to_frame()
                    comp_data.columns = compare_tickers

                # Normalize to 100
                normalized_df = (comp_data / comp_data.iloc[0]) * 100
                
                fig_comp = go.Figure()
                for col in normalized_df.columns:
                    fig_comp.add_trace(go.Scatter(x=normalized_df.index, y=normalized_df[col], name=col, mode='lines'))
                
                fig_comp.update_layout(template='plotly_white', title="Relative Performance (Normalized to 100)", 
                                     yaxis_title="Normalized Price", height=500)
                st.plotly_chart(fig_comp, use_container_width=True)

        # --- DATA TABLE & EXPORT ---
        st.markdown("---")
        st.markdown("### 📋 Detailed Data & Export")
        
        # Style the dataframe
        def style_returns(val):
            color = 'green' if val > 0 else 'red' if val < 0 else 'black'
            return f'color: {color}'

        display_df = df.copy()
        display_df['Daily Change %'] = display_df['Returns'] * 100
        
        # Format and show styled dataframe
        styled_df = display_df.sort_index(ascending=False).style.map(style_returns, subset=['Daily Change %']).format({'Daily Change %': '{:.2f}%', 'Close': '{:.2f}', 'Open': '{:.2f}', 'High': '{:.2f}', 'Low': '{:.2f}'})
        
        st.dataframe(styled_df, use_container_width=True)

        # Download Button
        csv = display_df.to_csv().encode('utf-8')
        st.download_button(
            label="📥 Download Data as CSV",
            data=csv,
            file_name=f"{ticker_symbol}_stock_data.csv",
            mime="text/csv",
        )

        # Company Description
        st.markdown("---")
        st.markdown("### ℹ️ About the Company")
        st.write(info.get('longBusinessSummary', 'No description available.'))

except Exception as e:
    st.error(f"An error occurred: {e}")
    st.info("Tip: Make sure the ticker symbol is correct (e.g., AAPL, TSLA, MSFT).")