import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# App Configuration
st.set_page_config(page_title="Daily Cash Report", layout="centered")

# Custom CSS for Centering
st.markdown("""
    <style>
    div[data-testid="stTable"] table { margin-left: auto; margin-right: auto; width: 100%; }
    th { text-align: center !important; background-color: #f0f2f6; }
    td { text-align: center !important; }
    </style>
    """, unsafe_allow_html=True)

# Initialize Session State
if 'history' not in st.session_state:
    st.session_state.history = []
if 'report_name' not in st.session_state:
    st.session_state.report_name = "User"
if 'fixed_rate' not in st.session_state:
    st.session_state.fixed_rate = 0.0

# --- Sidebar / Settings Section ---
with st.sidebar:
    st.header("⚙️ Settings")
    new_name = st.text_input("Name Badlein:", value=st.session_state.report_name)
    new_rate = st.number_input("Rate Fix Karein:", value=st.session_state.fixed_rate, step=1.0)
    
    if st.button("Save Settings"):
        st.session_state.report_name = new_name
        st.session_state.fixed_rate = new_rate
        st.success("Settings Updated!")
        st.rerun()

# --- Main App ---
st.title("📝 Daily Cash Report")
st.subheader(f"👤 Report For: {st.session_state.report_name}")
st.info(f"💰 Fixed Rate: ₹{st.session_state.fixed_rate:.2f}")

# --- Input Section ---
with st.expander("➕ Nayi Entry Karein", expanded=True):
    date_today = st.date_input("Date Select Karein", datetime.now())
    quantity = st.number_input("Quantity", min_value=0, step=1, value=0)
    
    # Auto Calculation using fixed rate
    total_amount = float(st.session_state.fixed_rate * quantity)
    st.write(f"Calculation: {quantity} Qty x ₹{st.session_state.fixed_rate} = **₹{total_amount:.2f}**")

    if st.button("Save Entry"):
        entry_id = datetime.now().timestamp()
        entry = {
            "ID": entry_id, 
            "Date": date_today, 
            "Day": date_today.day,
            "Quantity": int(quantity),
            "Month": date_today.strftime("%B %Y"),
            "Amount": total_amount
        }
        st.session_state.history.append(entry)
        st.success("Entry Saved!")
        st.rerun()

st.divider()

# --- Filter Section ---
if st.session_state.history:
    st.subheader("📊 View History")
    col1, col2 = st.columns(2)
    
    with col1:
        all_months = sorted(list(set(item['Month'] for item in st.session_state.history)))
        selected_month = st.selectbox("Month:", all_months)
    
    with col2:
        day_range = st.radio("Days Slot:", ["1 to 10", "11 to 20", "21 to 31", "Full Month"], horizontal=True)

    # Filter by Month
    month_data = [item for item in st.session_state.history if item['Month'] == selected_month]
    
    # Filter by Day Slot
    if day_range == "1 to 10":
        filtered_data = [item for item in month_data if 1 <= item['Day'] <= 10]
    elif day_range == "11 to 20":
        filtered_data = [item for item in month_data if 11 <= item['Day'] <= 20]
    elif day_range == "21 to 31":
        filtered_data = [item for item in month_data if item['Day'] >= 21]
    else:
        filtered_data = month_data

    # Display Table
    if filtered_data:
        display_df = pd.DataFrame(filtered_data)[["Date", "Quantity", "Amount"]]
        display_df = display_df.sort_values(by="Date", ascending=False)
        st.table(display_df.style.format({"Amount": "{:.2f}"}))

        month_total = sum(item['Amount'] for item in filtered_data)
        st.metric(f"Total Amount ({day_range})", f"₹{month_total:.2f}")

        # WhatsApp Share
        report_text = f"*Daily Cash Report - {st.session_state.report_name}*\n📅 {selected_month} ({day_range})\n\n"
        for _, row in display_df.iterrows():
            report_text += f"• {row['Date']} | Qty: {row['Quantity']} | ₹{row['Amount']:.2f}\n"
        report_text += f"\n*Total: ₹{month_total:.2f}*"
        
        encoded_text = urllib.parse.quote(report_text)
        whatsapp_url = f"https://wa.me/?text={encoded_text}"
        st.link_button("Share on WhatsApp ✅", whatsapp_url)
    else:
        st.warning("Is slot mein koi data nahi hai.")

    # Delete Section
    st.divider()
    with st.expander("🗑️ Entry Delete Karein"):
        all_options = {f"{item['Date']} - Qty:{item['Quantity']} (₹{item['Amount']:.2f})": item['ID'] for item in month_data}
        to_delete = st.selectbox("Delete karne ke liye chunein:", options=list(all_options.keys()))
        if st.button("Confirm Delete"):
            target_id = all_options[to_delete]
            st.session_state.history = [item for item in st.session_state.history if item['ID'] != target_id]
            st.rerun()
else:
    st.write("Abhi koi data nahi hai. Nayi entry karein.")
    
