import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# App Configuration
st.set_page_config(page_title="Daily Work Report", layout="centered")

# Title
st.title("📝 Daily Work Report")

# Initialize Session State
if 'history' not in st.session_state:
    st.session_state.history = []

# --- Input Section ---
with st.expander("➕ Nayi Entry Karein", expanded=True):
    date_today = st.date_input("Date", datetime.now())
    # Name Option Add Kiya Gaya
    name = st.text_input("Kaam/Vyakti Ka Naam", placeholder="Jaise: Sunil, Site Work, etc.")
    rate = st.number_input("Rate (per unit)", min_value=0.0, step=1.0, value=0.0)
    # Quantity se point hatane ke liye step=1 aur value=0 (Integer)
    quantity = st.number_input("Quantity", min_value=0, step=1, value=0)
    
    total_amount = rate * quantity
    st.info(f"**Total Calculation: ₹{total_amount}**")

    if st.button("Save Entry"):
        if not name:
            st.error("Kripya Naam bharein!")
        else:
            entry_id = datetime.now().timestamp()
            entry = {
                "ID": entry_id, 
                "Date": date_today, 
                "Name": name,
                "Month": date_today.strftime("%B %Y"),
                "Amount": total_amount
            }
            st.session_state.history.append(entry)
            st.success(f"{name} ki entry save ho gayi!")
            st.rerun()

st.divider()

# --- Filter & History Section ---
if st.session_state.history:
    all_months = sorted(list(set(item['Month'] for item in st.session_state.history)))
    selected_month = st.selectbox("Month Select Karein:", all_months)

    filtered_data = [item for item in st.session_state.history if item['Month'] == selected_month]
    
    # History Table (Ab Name bhi dikhega)
    display_df = pd.DataFrame(filtered_data)[["Date", "Name", "Amount"]]
    display_df = display_df.sort_values(by="Date", ascending=False)
    st.table(display_df)

    month_total = sum(item['Amount'] for item in filtered_data)
    st.metric(f"Total ({selected_month})", f"₹{month_total}")

    # --- WhatsApp Share Section ---
    st.subheader("📲 Share Report")
    
    report_text = f"*Daily Work Report - {selected_month}*\n\n"
    for _, row in display_df.iterrows():
        # WhatsApp message mein Name bhi jayega
        report_text += f"📅 {row['Date']} | 👤 {row['Name']}: ₹{row['Amount']}\n"
    report_text += f"\n*Total Amount: ₹{month_total}*"
    
    encoded_text = urllib.parse.quote(report_text)
    whatsapp_url = f"https://wa.me/?text={encoded_text}"
    
    st.link_button("Share on WhatsApp ✅", whatsapp_url)

    # --- Delete Section ---
    st.divider()
    with st.expander("🗑️ Entry Delete Karein"):
        delete_options = {f"{item['Date']} - {item['Name']} (₹{item['Amount']})": item['ID'] for item in filtered_data}
        to_delete = st.selectbox("Kaunsi entry hatani hai?", options=list(delete_options.keys()))
        
        if st.button("Confirm Delete"):
            target_id = delete_options[to_delete]
            st.session_state.history = [item for item in st.session_state.history if item['ID'] != target_id]
            st.warning("Entry Deleted!")
            st.rerun()
else:
    st.write("Abhi tak koi data nahi hai.")
    
