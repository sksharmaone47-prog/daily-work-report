import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# App Configuration
st.set_page_config(page_title="Daily Work Report", layout="centered")

# Custom CSS for Styling
st.markdown("""
    <style>
    div[data-testid="stTable"] table { margin-left: auto; margin-right: auto; width: 100%; }
    th { text-align: center !important; background-color: #f0f2f6; color: black; }
    td { text-align: center !important; }
    .total-box { 
        padding: 15px; 
        background-color: #e1f5fe; 
        border-radius: 10px; 
        text-align: center; 
        font-size: 18px; 
        font-weight: bold;
        color: #01579b;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize Session State
if 'history' not in st.session_state: st.session_state.history = []
if 'report_name' not in st.session_state: st.session_state.report_name = ""
if 'fixed_rate' not in st.session_state: st.session_state.fixed_rate = 0.0

# --- Sidebar / Settings ---
with st.sidebar:
    st.header("⚙️ Settings")
    st.session_state.report_name = st.text_input("Naam Likhein:", value=st.session_state.report_name)
    st.session_state.fixed_rate = st.number_input("Rate Fix Karein:", value=st.session_state.fixed_rate, step=1.0)
    if st.button("Save Settings"): st.rerun()

# --- Main App ---
st.title("📝 Daily Work Report")
if st.session_state.report_name:
    st.subheader(f"👤 {st.session_state.report_name}")
st.info(f"💰 Fixed Rate: ₹{st.session_state.fixed_rate:.2f}")

# --- Entry Section ---
with st.expander("➕ Nayi Entry Karein", expanded=True):
    date_today = st.date_input("Date Select Karein", datetime.now())
    quantity = st.number_input("Quantity", min_value=0, step=1, value=0)
    total_amount = float(st.session_state.fixed_rate * quantity)
    
    if st.button("Save Entry"):
        entry_id = datetime.now().timestamp()
        entry = {
            "ID": entry_id, "Date": date_today.strftime("%Y-%m-%d"), 
            "Day": date_today.day, "Quantity": int(quantity),
            "Month": date_today.strftime("%B %Y"), "Amount": total_amount
        }
        st.session_state.history.append(entry)
        st.success("Entry Saved!")
        st.rerun()

st.divider()

# --- View History ---
if st.session_state.history:
    st.subheader("📊 View History")
    col1, col2 = st.columns(2)
    with col1:
        all_months = sorted(list(set(item['Month'] for item in st.session_state.history)))
        selected_month = st.selectbox("Month:", all_months)
    with col2:
        day_range = st.radio("Days Slot:", ["1 to 10", "11 to 20", "21 to 31", "Full Month"], horizontal=True)

    # Filtering Logic
    month_data = [item for item in st.session_state.history if item['Month'] == selected_month]
    if day_range == "1 to 10":
        filtered_data = [item for item in month_data if 1 <= item['Day'] <= 10]
    elif day_range == "11 to 20":
        filtered_data = [item for item in month_data if 11 <= item['Day'] <= 20]
    elif day_range == "21 to 31":
        filtered_data = [item for item in month_data if item['Day'] >= 21]
    else:
        filtered_data = month_data

    if filtered_data:
        df = pd.DataFrame(filtered_data)[["Date", "Quantity", "Amount"]]
        df = df.sort_values(by="Date", ascending=False)
        
        # --- Totals Display (Jaise aapne manga tha) ---
        total_qty = df["Quantity"].sum()
        total_amt = df["Amount"].sum()
        
        st.markdown(f"""
            <div class="total-box">
                Total Quantity = {total_qty} &nbsp; | &nbsp; Total Amount = ₹{total_amt:.2f}
            </div>
            """, unsafe_allow_html=True)
        
        # --- Table below totals ---
        st.table(df.style.format({"Amount": "{:.2f}"}))

        # WhatsApp Share
        report_text = f"*Daily Work Report - {st.session_state.report_name}*\n📅 {selected_month} ({day_range})\n\n"
        for _, row in df.iterrows():
            report_text += f"• {row['Date']} | Qty: {row['Quantity']} | ₹{row['Amount']:.2f}\n"
        report_text += f"\n*Total Quantity = {total_qty}*\n*Total Amount = ₹{total_amt:.2f}*"
        
        encoded_text = urllib.parse.quote(report_text)
        st.link_button("Share on WhatsApp ✅", f"https://wa.me/?text={encoded_text}")

    # Delete Section
    with st.expander("🗑️ Entry Delete Karein"):
        all_options = {f"{item['Date']} - Qty:{item['Quantity']}": item['ID'] for item in month_data}
        to_delete = st.selectbox("Chunein:", options=list(all_options.keys()))
        if st.button("Confirm Delete"):
            st.session_state.history = [item for item in st.session_state.history if item['ID'] != all_options[to_delete]]
            st.rerun()
else:
    st.write("Abhi koi data nahi hai.")
        
