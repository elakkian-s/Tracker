
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Initialize session state for portfolio data
if 'portfolio' not in st.session_state:
    st.session_state['portfolio'] = []

# Function to add asset to portfolio
def add_asset(name, asset_type, quantity, price):
    st.session_state['portfolio'].append({
        'Name': name,
        'Type': asset_type,
        'Quantity': quantity,
        'Price': price,
        'Total Value': quantity * price
    })

# Streamlit app layout
st.title("Personal Portfolio Management AI Agent")

# Input form for adding assets
st.header("Add Asset")
with st.form(key='add_asset_form'):
    name = st.text_input("Asset Name")
    asset_type = st.selectbox("Asset Type", ["Stock", "Crypto", "Real Estate", "Other"])
    quantity = st.number_input("Quantity", min_value=0.0, format="%.2f")
    price = st.number_input("Price per Unit", min_value=0.0, format="%.2f")
    submit_button = st.form_submit_button(label='Add Asset')
    
    if submit_button:
        add_asset(name, asset_type, quantity, price)
        st.success(f"Asset {name} added to portfolio!")

# Display portfolio summary
st.header("Portfolio Summary")
if st.session_state['portfolio']:
    df = pd.DataFrame(st.session_state['portfolio'])
    st.dataframe(df)
    
    # Display total portfolio value
    total_value = df['Total Value'].sum()
    st.write(f"**Total Portfolio Value:** ${total_value:.2f}")
    
    # Plot asset allocation pie chart
    st.header("Asset Allocation")
    asset_allocation = df.groupby('Type')['Total Value'].sum()
    fig, ax = plt.subplots()
    ax.pie(asset_allocation, labels=asset_allocation.index, autopct='%1.1f%%')
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig)
else:
    st.write("No assets in portfolio. Please add assets to see the summary.")
