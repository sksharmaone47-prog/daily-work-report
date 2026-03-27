import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse
from PIL import Image
import io
from streamlit_gsheets import GSheetsConnection

# App Configuration
st.set_page_config(page_title="Work Report Pro", layout="centered", page_icon="📝")

# --- Google Sheets Connection ---
# Yahan apni Google Sheet ka URL dalein
url = "https://docs.google.com/spreadsheets/d/13IfQR6C-n1UtIa75au5CtSukamVW45W6QY-WvwFngms/edit?usp=drivesdk"

conn = st.connection("gsheets", type=GSheetsConnection)

def get_data():
    return conn.read(spreadsheet=url, usecols=[0,1,2,3,4,5], ttl="0")

# --- CSS Styling ---
st.markdown("""
    <style>
    .profile-container { display: flex; justify-content: center; margin-bottom: -20px; margin-top: 10px; }
    .official-header { background-color: #004085; padding: 20px; border-radius: 12px; color: white; text-align: center; margin-bottom: 25px; }
    .dashboard-container { display: flex; justify-content: space-around; background: #ffffff; padding: 18px; border-radius: 10px; border: 1px solid #dee2e6; margin-bottom: 20px; }
    .dashboard-value { font-size: 22px; font-weight: bold; color: #007bff; }
    </style>
    """, unsafe_allow_html=True)

# Initialize Session State for non-sheet data
if 'report_name' not in st.session_state: st.session_state.report_name = "Employee"
if 'fixed_rate' not in st.session_state: st.session_state.fixed_rate = 0.0
if 'profile_pic' not in st.session_state: st.session_state.profile_pic = None

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Settings")
    st.session_state.report_name = st.text_input("Name:", st.session_state.report_name)
    st.session_state.fixed_rate = st.number_input("Rate (₹):", value=st.session_state.fixed_rate, step=1.0)
    uploaded_file = st.file_uploader("Upload Photo", type=['jpg', 'png', 'jpeg'])
    if uploaded_file: st.session_state.profile_pic = uploaded_file.read()
    if st.button("Save Profile"): st.rerun()

# --- Profile & Header ---
if st.session_state.profile_pic:
    img = Image.open(io.BytesIO(st.session_state.profile_pic))
    st.markdown('<div class="profile-container">', unsafe_allow_html=True)
    st.image(img, width=120)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f'<div class="official-header"><h2>📝 WORK REPORT PRO</h2><h4>{st.session_state.report_name}</h4></div>', unsafe_allow_html=True)

# --- Entry Section ---
with st.expander("📝 Add New Work Entry", expanded=True):
    col1, col2 = st.columns(2)
    with col1: date_today = st.date_input("Date", datetime.now())
    with col2: quantity = st.number_input("Quantity", min_value=1, step=1, value=1)
    
    total_amount = float(st.session_state.fixed_rate * quantity)
    
    if st.button("SAVE TO CLOUD ✅", use_container_width=True):
        if st.session_state.fixed_rate > 0:
            # Sheet se purana data laao
            existing_data = get_data()
            new_entry = pd.DataFrame([{
                "ID": str(datetime.now().timestamp()),
                "Date": date_today.strftime("%d-%m-%Y"),
                "Day": int(date_today.day),
                "Quantity": int(quantity),
                "Month": date_today.strftime("%B %Y"),
                "Amount": total_amount
            }])
            updated_df = pd.concat([existing_data, new_entry], ignore_index=True)
            conn.update(spreadsheet=url, data=updated_df)
            st.success("Data Google Sheet mein save ho gaya!")
            st.rerun()
        else:
            st.error("Rate set karein!")

# --- Display Section ---
df = get_data()
if not df.empty:
    st.markdown("### 📊 Work Record (From Cloud)")
    all_months = sorted(df["Month"].unique())
    selected_month = st.selectbox("Month", all_months)
    
    filtered_df = df[df["Month"] == selected_month]
    
    if not filtered_df.empty:
        t_qty = filtered_df["Quantity"].astype(int).sum()
        t_amt = filtered_df["Amount"].astype(float).sum()
        
        st.markdown(f'<div class="dashboard-container"><div class="dashboard-value">Qty: {t_qty}</div><div class="dashboard-value">Total: ₹{t_amt:.2f}</div></div>', unsafe_allow_html=True)
        st.table(filtered_df[["Date", "Quantity", "Amount"]])
        
        # WhatsApp Share logic (same as before)
        report_text = f"*WORK REPORT PRO*\nOwner: {st.session_state.report_name}\nMonth: {selected_month}\nTotal Qty: {t_qty}\nTotal Amt: ₹{t_amt:.2f}"
        st.link_button("Share Report", f"https://wa.me/?text={urllib.parse.quote(report_text)}")
            
