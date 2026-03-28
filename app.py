import streamlit as st
import pandas as pd
import datetime
from streamlit_gsheets import GSheetsConnection

# Page Setup
st.set_page_config(page_title="Daily Work Report", layout="wide")
st.title("📊 Daily Work Report (Cloud Saved)")

# Google Sheets Se Connect Karna
# Iske liye Streamlit ke 'Secrets' mein sheet ka URL dalna hoga
conn = st.connection("gsheets", type=GSheetsConnection)

# Data Read Karna
df = conn.read(worksheet="Sheet1")

# --- Form Section ---
with st.form(key="work_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        date = st.date_input("Date", datetime.date.today())
    with col2:
        price = st.number_input("Rate", min_value=0, value=13)
    with col3:
        qty = st.number_input("Quantity", min_value=0, step=1)
    
    submit_button = st.form_submit_button(label="Save Entry to Google Sheet")

if submit_button:
    new_data = pd.DataFrame([{
        "Date": str(date),
        "Price": price,
        "Quantity": qty,
        "Daily Cash": price * qty
    }])
    
    # Purane data mein naya data jodna
    updated_df = pd.concat([df, new_data], ignore_index=True)
    
    # Google Sheet ko update karna
    conn.update(worksheet="Sheet1", data=updated_df)
    st.success("Data Google Sheet mein save ho gaya!")
    st.rerun()

# --- Display Section ---
st.divider()
if not df.empty:
    st.subheader("Summary Table")
    st.dataframe(df, use_container_width=True)
    
    total_q = df["Quantity"].sum()
    total_c = df["Daily Cash"].sum()
    st.metric("Total Quantity", total_q)
    st.metric("Total Payout", f"₹{total_c}")
    
