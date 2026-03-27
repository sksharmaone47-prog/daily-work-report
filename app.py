import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse
from PIL import Image
import io

# App Configuration
st.set_page_config(page_title="Work Report Pro", layout="centered", page_icon="📝")

# --- Google Sheet Setup ---
# APNA LINK YAHAN PASTE KAREIN (Make sure it is set to 'Anyone with link can EDITOR')
SHEET_URL = "https://docs.google.com/spreadsheets/d/13IfQR6C-n1UtIa75au5CtSukamVW45W6QY-WvwFngms/edit?usp=drivesdk"
# Form Response link (Isse hum direct data bhej sakte hain agar Sheets API use na karni ho)
# Lekin asaan tarike ke liye hum Session State + CSV Download feature use karte hain

# --- CSS Styling ---
st.markdown("""
    <style>
    .profile-container { display: flex; justify-content: center; margin-bottom: -20px; margin-top: 10px; }
    .official-header { background-color: #004085; padding: 20px; border-radius: 12px; color: white; text-align: center; margin-bottom: 25px; }
    .dashboard-container { display: flex; justify-content: space-around; background: #ffffff; padding: 18px; border-radius: 10px; border: 1px solid #dee2e6; margin-bottom: 20px; }
    .dashboard-value { font-size: 22px; font-weight: bold; color: #007bff; }
    </style>
    """, unsafe_allow_html=True)

# Data Persistence (Local for now to avoid Connection Errors)
if 'history' not in st.session_state: st.session_state.history = []
if 'report_name' not in st.session_state: st.session_state.report_name = ""
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
    
    if st.button("SAVE ENTRY ✅", use_container_width=True):
        if st.session_state.fixed_rate > 0:
            new_entry = {
                "Date": date_today.strftime("%d-%m-%Y"),
                "Quantity": int(quantity),
                "Amount": total_amount,
                "Month": date_today.strftime("%B %Y")
            }
            st.session_state.history.append(new_entry)
            st.success("Entry Saved Successfully!")
            st.rerun()
        else:
            st.error("Rate set karein!")

# --- Display Section ---
if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    st.markdown("### 📊 Work Record")
    
    all_months = sorted(df["Month"].unique())
    selected_month = st.selectbox("Month Filter", all_months)
    
    filtered_df = df[df["Month"] == selected_month]
    
    t_qty = filtered_df["Quantity"].sum()
    t_amt = filtered_df["Amount"].sum()
    
    st.markdown(f'<div class="dashboard-container"><div class="dashboard-value">Total Qty: {t_qty}</div><div class="dashboard-value">Total: ₹{t_amt:.2f}</div></div>', unsafe_allow_html=True)
    st.table(filtered_df[["Date", "Quantity", "Amount"]])
    
    # WhatsApp Share
    report_text = f"*WORK REPORT PRO - {st.session_state.report_name}*\n📅 {selected_month}\n\n"
    for _, row in filtered_df.iterrows():
        report_text += f"• {row['Date']} | Qty: {row['Quantity']} | ₹{row['Amount']:.2f}\n"
    report_text += f"\n*Total Qty: {t_qty}*\n*Total Amount: ₹{t_amt:.2f}*"
    
    st.link_button("Share on WhatsApp ✅", f"https://wa.me/?text={urllib.parse.quote(report_text)}", use_container_width=True)

    # Permanent Backup Option
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Excel/CSV Backup Download", data=csv, file_name=f"work_report_{datetime.now().strftime('%d_%m_%Y')}.csv", mime='text/csv', use_container_width=True)
    
