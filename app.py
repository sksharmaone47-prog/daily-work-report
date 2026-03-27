import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# App Configuration
st.set_page_config(
    page_title="Work Report Pro", 
    layout="centered", 
    page_icon="📝" # Naya Browser Icon
)

# --- Official Layout CSS (Including New Logo Styles) ---
st.markdown("""
    <style>
    /* New Official Header & Logo Styling */
    .official-header {
        background-color: #004085; /* Professional Dark Blue */
        padding: 25px;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 8px;
    }
    .logo-container {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .main-logo {
        font-size: 38px;
    }
    .title-text {
        font-size: 28px;
        font-weight: bold;
        letter-spacing: 1.5px;
    }
    .sub-title {
        font-size: 13px;
        opacity: 0.8;
    }

    /* Table & Centering Styling */
    div[data-testid="stTable"] table { margin-left: auto; margin-right: auto; width: 100%; border-collapse: collapse; }
    th { text-align: center !important; background-color: #f8f9fa; color: #333; font-weight: bold; padding: 12px !important; }
    td { text-align: center !important; padding: 10px !important; border-bottom: 1px solid #eee; }
    
    /* Dashboard Style Totals */
    .dashboard-container {
        display: flex;
        justify-content: space-around;
        background: #ffffff;
        padding: 18px;
        border-radius: 10px;
        border: 1px solid #dee2e6;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }
    .dashboard-item { text-align: center; }
    .dashboard-label { font-size: 11px; color: #6c757d; text-transform: uppercase; font-weight: bold;}
    .dashboard-value { font-size: 22px; font-weight: bold; color: #007bff; }
    </style>
    """, unsafe_allow_html=True)

# --- Official Header with New Logo ---
st.markdown("""
    <div class="official-header">
        <div class="logo-container">
            <span class="main-logo">📝💼</span> <span class="title-text">WORK REPORT PRO</span>
        </div>
        <div class="sub-title">Daily Operations Management System</div>
    </div>
    """, unsafe_allow_html=True)

# Initialize Session State
if 'history' not in st.session_state: st.session_state.history = []
if 'report_name' not in st.session_state: st.session_state.report_name = ""
if 'fixed_rate' not in st.session_state: st.session_state.fixed_rate = 0.0

# --- Sidebar / Settings Section ---
with st.sidebar:
    st.markdown("### ⚙️ Official Settings")
    st.session_state.report_name = st.text_input("Report Owner Name:", value=st.session_state.report_name, placeholder="e.g. Sandeep Sharma")
    st.session_state.fixed_rate = st.number_input("Standard Rate (₹):", value=st.session_state.fixed_rate, step=1.0)
    
    if st.button("Update Profile", use_container_width=True):
        st.rerun()

# --- Employee Info Bar ---
if st.session_state.report_name:
    st.markdown(f"**👤 Employee:** {st.session_state.report_name} | **💰 Rate:** ₹{st.session_state.fixed_rate:.2f}/unit")
else:
    st.info("Set report owner name in settings (sidebar) to start.")
st.divider()

# --- Entry Input Section ---
with st.expander("📝 Add New Work Entry", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        date_today = st.date_input("Date", datetime.now())
    with col2:
        quantity = st.number_input("Quantity", min_value=0, step=1, value=0)
    
    # Check rate
    if st.session_state.fixed_rate <= 0:
        st.warning("Please set a standard rate in settings first.")
        total_amount = 0.0
    else:
        total_amount = float(st.session_state.fixed_rate * quantity)
        st.write(f"Calc: {quantity} x ₹{st.session_state.fixed_rate:.2f} = **₹{total_amount:.2f}**")

    if st.button("SAVE ENTRY", use_container_width=True):
        if st.session_state.fixed_rate > 0:
            entry_id = datetime.now().timestamp()
            entry = {
                "ID": entry_id, "Date": date_today.strftime("%d-%m-%Y"), 
                "Day": date_today.day, "Quantity": int(quantity),
                "Month": date_today.strftime("%B %Y"), "Amount": total_amount
            }
            st.session_state.history.append(entry)
            st.success("Entry saved to official records.")
            st.rerun()
        else:
            st.error("Rate must be set before saving.")

# --- View History / Records ---
if st.session_state.history:
    st.markdown("### 📊 Official Records")
    c1, c2 = st.columns([2, 3])
    with c1:
        all_months = sorted(list(set(item['Month'] for item in st.session_state.history)))
        selected_month = st.selectbox("Month Filter", all_months)
    with c2:
        day_range = st.radio("Days Slot Filter:", ["1-10", "11-20", "21-31", "Full Month"], horizontal=True, index=3)

    # Filter Logic
    month_data = [item for item in st.session_state.history if item['Month'] == selected_month]
    if day_range == "1-10": filtered_data = [item for item in month_data if 1 <= item['Day'] <= 10]
    elif day_range == "11-20": filtered_data = [item for item in month_data if 11 <= item['Day'] <= 20]
    elif day_range == "21-31": filtered_data = [item for item in month_data if item['Day'] >= 21]
    else: filtered_data = month_data

    # Display Records
    if filtered_data:
        df = pd.DataFrame(filtered_data)[["Date", "Quantity", "Amount"]]
        df['dt_obj'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
        df = df.sort_values(by="dt_obj", ascending=False).drop(columns=['dt_obj'])
        
        total_qty = df["Quantity"].sum()
        total_amt = df["Amount"].sum()
        
        # --- Official Dashboard Totals ---
        st.markdown(f"""
            <div class="dashboard-container">
                <div class="dashboard-item">
                    <div class="dashboard-label">Total Quantity</div>
                    <div class="dashboard-value">{total_qty}</div>
                </div>
                <div class="dashboard-item" style="border-left: 1px solid #dee2e6; padding-left: 20px;">
                    <div class="dashboard-label">Total Earning</div>
                    <div class="dashboard-value">₹{total_amt:.2f}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # --- Records Table ---
        st.table(df.style.format({"Amount": "{:.2f}"}))

        # WhatsApp Share formatting
        st.divider()
        report_text = f"*WORK REPORT PRO - {st.session_state.report_name}*\n"
        report_text += f"📅 {selected_month} ({day_range})\n\n"
        for _, row in df.iterrows():
            report_text += f"• {row['Date']} | Qty: {row['Quantity']} | ₹{row['Amount']:.2f}\n"
        report_text += f"\n*Grand Total Qty: {total_qty}*\n*Grand Total Amount: ₹{total_amt:.2f}*"
        
        st.link_button("Share Official Report ✅", f"https://wa.me/?text={urllib.parse.quote(report_text)}", use_container_width=True)

    else:
        st.warning("No records found for the selected month/slot.")

    # Delete Section
    with st.expander("🗑️ Manage Records (Remove Entry)"):
        all_options = {f"{item['Date']} - Qty:{item['Quantity']}": item['ID'] for item in month_data}
        to_delete = st.selectbox("Select entry to remove:", options=list(all_options.keys()))
        if st.button("Delete Selected Entry", use_container_width=True):
            st.session_state.history = [item for item in st.session_state.history if item['ID'] != all_options[to_delete]]
            st.rerun()
else:
    st.info("No records to display. Use the form above to add an entry.")
        
