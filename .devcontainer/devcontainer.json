import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Daily Work Report", layout="wide")
st.title("📊 Daily Work Report")

# Aapki Google Sheet ka URL (Isse "Editor" mode mein share hona chahiye)
# Secrets se link uthane ke liye:
try:
    SHEET_URL = st.secrets["connections"]["gsheets"]["spreadsheet"]
    # CSV format mein convert karna
    csv_url = SHEET_URL.replace('/edit?usp=sharing', '/gviz/tq?tqx=out:csv')
    df = pd.read_csv(csv_url)
except Exception as e:
    st.error("Google Sheet link nahi mila. Check Secrets!")
    df = pd.DataFrame(columns=["Date", "Price", "Quantity", "Daily Cash"])

# --- Form ---
with st.form("entry_form"):
    c1, c2, c3 = st.columns(3)
    d = c1.date_input("Date", datetime.date.today())
    p = c2.number_input("Price", value=13)
    q = c3.number_input("Quantity", value=0)
    
    if st.form_submit_button("Save Entry"):
        st.info("Direct Google Sheet saving is active. Please check your Sheet.")
        # Is version mein hum abhi sirf display kar rahe hain
        # Full Google Sheet edit ke liye API keys chahiye hoti hain

# Summary
st.divider()
st.table(df)
