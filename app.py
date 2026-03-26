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
    # Add to history (unique ID ke liye timestamp use kiya hai)
    entry_id = datetime.now().timestamp()
    entry = {"id": entry_id, "Date": date_today.strftime("%Y-%m-%d"), "Amount": total_amount}
    st.session_state.history.append(entry)
    
    # Keep only last 10 days
    if len(st.session_state.history) > 10:
        st.session_state.history.pop(0)
    st.rerun()

# --- History Section ---
st.divider()
st.subheader("📜 Last 10 Days History")

if st.session_state.history:
    # History ko list mein dikhayenge taaki delete button add kar sakein
    for index, item in enumerate(reversed(st.session_state.history)):
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            st.write(f"📅 {item['Date']}")
        with col2:
            st.write(f"💰 ₹{item['Amount']}")
        with col3:
            # Har entry ke liye ek alag Delete button
            if st.button("❌", key=f"del_{index}_{item['id']}"):
                # Original list se item remove karna (reversed index ko handle karte hue)
                actual_index = len(st.session_state.history) - 1 - index
                st.session_state.history.pop(actual_index)
                st.rerun()
    
    st.divider()
    total_sum = sum(item['Amount'] for item in st.session_state.history)
    st.metric("Total (Last 10 Days)", f"₹{total_sum}")
else:
    st.write("Abhi tak koi history nahi hai.")
