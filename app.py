import streamlit as st
import pandas as pd
from datetime import datetime

# App Configuration
st.set_page_config(page_title="Daily Work Report", layout="centered")

# Title
st.title("📝 Daily Work Report")

# Initialize Session State for History
if 'history' not in st.session_state:
    st.session_state.history = []

# --- Input Section ---
st.subheader("Aaj Ka Kaam")
date_today = st.date_input("Date", datetime.now())
rate = st.number_input("Rate (per unit)", min_value=0.0, step=1.0, value=0.0)
quantity = st.number_input("Quantity", min_value=0.0, step=1.0, value=0.0)

# Auto Calculation
total_amount = rate * quantity
st.info(f"**Total Calculation: ₹{total_amount}**")

if st.button("Save Entry"):
    # Add to history
    entry = {"Date": date_today.strftime("%Y-%m-%d"), "Amount": total_amount}
    st.session_state.history.append(entry)
    
    # Keep only last 10 days
    if len(st.session_state.history) > 10:
        st.session_state.history.pop(0)
        
    st.success("Entry Saved Successfully!")

# --- History Section ---
st.divider()
st.subheader("📜 Last 10 Days History")

if st.session_state.history:
    # Show newest first
    history_df = pd.DataFrame(st.session_state.history[::-1])
    st.table(history_df)
    
    total_sum = sum(item['Amount'] for item in st.session_state.history)
    st.metric("Total (Last 10 Days)", f"₹{total_sum}")
else:
    st.write("Abhi tak koi history nahi hai.")
    
