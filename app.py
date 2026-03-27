import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# App Configuration
st.set_page_config(page_title="Daily Work Report", layout="centered", page_icon="📊")

# --- Official Layout CSS ---
st.markdown("""
    <style>
    /* Header styling */
    .main-header {
        background-color: #002b36;
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .logo-text {
        font-size: 35px;
        font-weight: bold;
        letter-spacing: 2px;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 15px;
    }
    .sub-title {
        font-size: 14px;
        opacity: 0.8;
        margin-top: 5px;
    }
    /* Table Centering */
    div[data-testid="stTable"] table { margin-left: auto; margin-right: auto; width: 100%; border-collapse: collapse; }
    th { text-align: center !important; background-color: #f0f2f6; color: #333; font-weight: bold; padding: 12px !important; }
    td { text-align: center !important; padding: 10px !important; border-bottom: 1px solid #eee; }
    
    /* Total Dashboard Style */
    .total-container {
        display: flex;
        justify-content: space-around;
        background: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .total-item { text-align: center; }
    .total-label { font-size: 12px; color: #666; text-transform: uppercase; }
    .total-value { font-size: 20px; font-weight: bold; color: #007bff; }
    </style>
    """, unsafe_allow_html=True)

# --- Official Logo & Header ---
st.markdown("""
    <div class="main-header">
        <div class="logo-text">💼 WORK REPORT PRO</div>
        <div class="sub-title">Official Daily Management System</div>
    </div>
    """, unsafe_allow_html=True)

# Initialize Session State
if 'history' not in st.session_state: st.session_state.history = []
if 'report_name' not in st.session_state: st.session_state.report_name = ""
if 'fixed_rate' not in st.session_state: st.session_state.fixed_rate = 0.0

# --- Settings (Sidebar) ---
with st.sidebar:
    st.markdown("### ⚙️ Official Settings")
    st.session_state.report_name = st.text_input("Report Owner Name:", value=st.session_state.report_name)
    st.session_state.fixed_rate = st.number_input("Standard Rate (₹):", value=st.session_state.fixed_rate, step=1.0)
    if st.button("Update Profile"): st.rerun()

# --- Info Bar ---
if st.session_state.report_name:
    st.markdown(f"**👤 Employee:** {st.session_state.report_name} | **💰 Fixed Rate:** ₹{st.session_state.fixed_rate:.2f}")
st.divider()

# --- Entry Section ---
with st.expander("📝 Add New Work Entry", expanded=True):
    col_date, col_qty = st.columns(2)
    with col_date:
        date_today = st.date_input("Select Date", datetime.now())
    with col_qty:
        quantity = st.number_input("Enter Quantity", min_value=0, step=1, value=0)
    
    total_amount = float(st.session_state.fixed_rate * quantity)
    
    if st.button("SAVE ENTRY", use_container_width=True):
        entry_id = datetime.now().timestamp()
        entry = {
            "ID": entry_id, "Date": date_today.strftime("%d-%m-%Y"), 
            "Day": date_today.day, "Quantity": int(quantity),
            "Month": date_today.strftime("%B %Y"), "Amount": total_amount
        }
        st.session_state.history.append(entry)
        st.success("Entry registered in official records.")
        st.rerun()

# --- Records & History ---
if st.session_state.history:
    st.markdown("### 📊 Official Work Records")
    c1, c2 = st.columns([1, 2])
    with c1:
        all_months = sorted(list(set(item['Month'] for item in st.session_state.history)))
        selected_month = st.selectbox("Select Month", all_months)
    with c2:
        day_range = st.radio("Slot Filter:", ["1-10", "11-20", "21-31", "All"], horizontal=True)

    # Filter Logic
    month_data = [item for item in st.session_state.history if item['Month'] == selected_month]
    if day_range == "1-10": filtered_data = [item for item in month_data if 1 <= item['Day'] <= 10]
    elif day_range == "11-20": filtered_data = [item for item in month_data if 11 <= item['Day'] <= 20]
    elif day_range == "21-31": filtered_data = [item for item in month_data if item['Day'] >= 21]
    else: filtered_data = month_data

    if filtered_data:
        df = pd.DataFrame(filtered_data)[["Date", "Quantity", "Amount"]]
        df['dt_obj'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
        df = df.sort_values(by="dt_obj", ascending=False).drop(columns=['dt_obj'])
        
        total_qty = df["Quantity"].sum()
        total_amt = df["Amount"].sum()
        
        # --- Official Dashboard Totals ---
        st.markdown(f"""
            <div class="total-container">
                <div class="total-item">
                    <div class="total-label">Total Quantity</div>
                    <div class="total-value">{total_qty}</div>
                </div>
                <div class="total-item" style="border-left: 1px solid #eee; padding-left: 20px;">
                    <div class="total-label">Total Earnings</div>
                    <div class="total-value">₹{total_amt:.2f}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # --- Data Table ---
        st.table(df.style.format({"Amount": "{:.2f}"}))

        # WhatsApp Share (Single Line Formatting)
        report_text = f"*WORK REPORT PRO - {st.session_state.report_name}*\n"
        report_text += f"📅 {selected_month} ({day_range})\n\n"
        for _, row in df.iterrows():
            report_text += f"• {row['Date']} | Qty: {row['Quantity']} | ₹{row['Amount']:.2f}\n"
        report_text += f"\n*Grand Total Qty: {total_qty}*\n*Grand Total Amount: ₹{total_amt:.2f}*"
        
        st.link_button("Share Official Report ✅", f"https://wa.me/?text={urllib.parse.quote(report_text)}", use_container_width=True)

    # Delete Section
    with st.expander("🗑️ Remove Entry"):
        all_options = {f"{item['Date']} - Qty:{item['Quantity']}": item['ID'] for item in month_data}
        to_delete = st.selectbox("Select entry to remove:", options=list(all_options.keys()))
        if st.button("Delete Selected Entry"):
            st.session_state.history = [item for item in st.session_state.history if item['ID'] != all_options[to_delete]]
            st.rerun()
else:
    st.info("No records found. Start by adding your first entry above.")
    
