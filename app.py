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
with st.expander("➕ Nayi Entry Karein", expanded=True):
    date_today = st.date_input("Date", datetime.now())
    rate = st.number_input("Rate (per unit)", min_value=0.0, step=1.0, value=0.0)
    quantity = st.number_input("Quantity", min_value=0.0, step=1.0, value=0.0)
    
    total_amount = rate * quantity
    st.info(f"**Total Calculation: ₹{total_amount}**")

    if st.button("Save Entry"):
        entry_id = datetime.now().timestamp()
        entry = {
            "ID": entry_id, 
            "Date": date_today, 
            "Month": date_today.strftime("%B %Y"),
            "Amount": total_amount
        }
        st.session_state.history.append(entry)
        st.success("Entry Saved!")
        st.rerun()

st.divider()

# --- Filter & History Section ---
st.subheader("📜 History & Reports")

if st.session_state.history:
    # 1. Month Filter
    all_months = sorted(list(set(item['Month'] for item in st.session_state.history)))
    selected_month = st.selectbox("Month Select Karein:", all_months)

    # Filter data based on month
    filtered_data = [item for item in st.session_state.history if item['Month'] == selected_month]
    
    # 2. Display Table (Single Line Format)
    display_df = pd.DataFrame(filtered_data)[["Date", "Amount"]]
    display_df = display_df.sort_values(by="Date", ascending=False)
    st.table(display_df)

    # 3. Total for the selected month
    month_total = sum(item['Amount'] for item in filtered_data)
    st.metric(f"Total ({selected_month})", f"₹{month_total}")

    # 4. Delete Option (Dropdown to keep layout clean)
    st.divider()
    with st.expander("🗑️ Entry Delete Karein"):
        delete_options = {f"{item['Date']} - ₹{item['Amount']}": item['ID'] for item in filtered_data}
        to_delete = st.selectbox("Kaunsi entry hatani hai?", options=list(delete_options.keys()))
        
        if st.button("Confirm Delete"):
            target_id = delete_options[to_delete]
            st.session_state.history = [item for item in st.session_state.history if item['ID'] != target_id]
            st.warning("Entry Deleted!")
            st.rerun()
else:
    st.write("Abhi tak koi data nahi hai.")
    
