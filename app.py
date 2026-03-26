import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# App Configuration
st.set_page_config(page_title="Daily Cash Report", layout="centered")

# --- Custom CSS for Centering Table Content ---
st.markdown("""
    <style>
    div[data-testid="stTable"] table {
        margin-left: auto;
        margin-right: auto;
    }
    th {
        text-align: center !important;
    }
    td {
        text-align: center !important;
    }
    </style>
    """, unsafe_layout=True)

# --- Header Section ---
st.title("📝 Daily Cash Report")

# Global Name Option
report_name = st.text_input("Kiske liye report hai? (Naam)", placeholder="Yahan naam likhein...")

# Initialize Session State
if 'history' not in st.session_state:
    st.session_state.history = []

# --- Input Section ---
with st.expander("➕ Nayi Entry Karein", expanded=True):
    date_today = st.date_input("Date", datetime.now())
    rate = st.number_input("Rate (per unit)", min_value=0.0, step=1.0, value=0.0)
    quantity = st.number_input("Quantity", min_value=0, step=1, value=0)
    
    total_amount = float(rate * quantity)
    st.info(f"**Total Calculation: ₹{total_amount:.2f}**")

    if st.button("Save Entry"):
        entry_id = datetime.now().timestamp()
        entry = {
            "ID": entry_id, 
            "Date": date_today.strftime("%Y-%m-%d"), 
            "Quantity": int(quantity),
            "Month": date_today.strftime("%B %Y"),
            "Amount": total_amount
        }
        st.session_state.history.append(entry)
        st.success(f"Entry Saved! (Qty: {quantity})")
        st.rerun()

st.divider()

# --- Filter & History Section ---
if st.session_state.history:
    all_months = sorted(list(set(item['Month'] for item in st.session_state.history)))
    selected_month = st.selectbox("Month Select Karein:", all_months)

    filtered_data = [item for item in st.session_state.history if item['Month'] == selected_month]
    
    if report_name:
        st.subheader(f"👤 Report For: {report_name}")

    # History Table (Centering Applied via CSS above)
    display_df = pd.DataFrame(filtered_data)[["Date", "Quantity", "Amount"]]
    display_df = display_df.sort_values(by="Date", ascending=False)
    
    # Rendering Table
    st.table(display_df.style.format({"Amount": "{:.2f}"}))

    month_total = sum(item['Amount'] for item in filtered_data)
    st.metric(f"Total ({selected_month})", f"₹{month_total:.2f}")

    # --- WhatsApp Share Section ---
    st.subheader("📲 Share Report")
    
    name_header = f"*Daily Cash Report*"
    if report_name:
        name_header = f"*Daily Cash Report - {report_name}*"
        
    report_text = f"{name_header}\n📅 Month: {selected_month}\n\n"
    for _, row in display_df.iterrows():
        report_text += f"• {row['Date']} | Qty: {row['Quantity']} | ₹{row['Amount']:.2f}\n"
    report_text += f"\n*Total Amount: ₹{month_total:.2f}*"
    
    encoded_text = urllib.parse.quote(report_text)
    whatsapp_url = f"https://wa.me/?text={encoded_text}"
    
    st.link_button("Share on WhatsApp ✅", whatsapp_url)

    # --- Delete Section ---
    st.divider()
    with st.expander("🗑️ Entry Delete Karein"):
        delete_options = {f"{item['Date']} - Qty: {item['Quantity']} (₹{item['Amount']:.2f})": item['ID'] for item in filtered_data}
        to_delete = st.selectbox("Kaunsi entry hatani hai?", options=list(delete_options.keys()))
        
        if st.button("Confirm Delete"):
            target_id = delete_options[to_delete]
            st.session_state.history = [item for item in st.session_state.history if item['ID'] != target_id]
            st.warning("Entry Deleted!")
            st.rerun()
else:
    st.write("Abhi tak koi data nahi hai.")
