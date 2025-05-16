
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests

# Function to fetch real-time stock price from the Flask API
def get_stock_price(ticker):
    try:
        response = requests.get(f"http://localhost:5000/price?ticker={ticker}")
        data = response.json()
        return data['price']
    except Exception as e:
        st.error(f"Error fetching price for {ticker}: {e}")
        return None

# Initialize session state for portfolio data
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = []

# Function to add asset to the portfolio
def add_asset(name, asset_type, quantity, price):
    st.session_state.portfolio.append({
        'Name': name,
        'Type': asset_type,
        'Quantity': quantity,
        'Price': price,
        'Total Value': quantity * price
    })

# Streamlit app layout
st.title("Portfolio Management AI Agent")

# Input form for adding assets
with st.form("add_asset_form"):
    name = st.text_input("Asset Name (e.g., Apple, Bitcoin)")
    asset_type = st.selectbox("Asset Type", ["Stock", "Crypto", "Real Estate", "Other"])
    quantity = st.number_input("Quantity", min_value=0.0, step=0.01)
    ticker = st.text_input("Stock Ticker (optional, for real-time price)")
    manual_price = st.number_input("Price per Unit (if no ticker)", min_value=0.0, step=0.01)
    
    # Fetch real-time price if ticker is provided
    if ticker:
        price = get_stock_price(ticker)
        if price:
            st.write(f"Real-time price for {ticker}: {price}")
        else:
            price = manual_price
    else:
        price = manual_price
    
    submitted = st.form_submit_button("Add Asset")
    if submitted:
        add_asset(name, asset_type, quantity, price)
        st.success(f"Added {quantity} units of {name} at {price} per unit.")

# Display portfolio summary
if st.session_state.portfolio:
    df = pd.DataFrame(st.session_state.portfolio)
    st.subheader("Portfolio Summary")
    st.dataframe(df)
    
    # Display total portfolio value
    total_value = df['Total Value'].sum()
    st.write(f"**Total Portfolio Value:** {total_value}")
    
    # Display asset allocation pie chart
    st.subheader("Asset Allocation")
    allocation = df.groupby('Type')['Total Value'].sum()
    fig, ax = plt.subplots()
    ax.pie(allocation, labels=allocation.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)
