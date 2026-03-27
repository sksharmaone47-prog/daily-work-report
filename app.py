import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse
from PIL import Image
import io

# App Configuration
st.set_page_config(page_title="Work Report Pro", layout="centered", page_icon="📝")

# --- CSS for Professional Look ---
st.markdown("""
    <style>
    .profile-container { display: flex; justify-content: center; margin-top: 10px; }
    .official-header { background-color: #004085; padding: 20px; border-radius: 12px; color: white; text-align: center; margin-bottom: 25px; }
    .dashboard-container { display: flex; justify-content: space-around; background: #ffffff; padding: 18px; border-radius: 10px; border: 1px solid #dee2e6; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .dashboard-value { font-size: 20px; font-weight: bold; color: #007bff; }
    div[data-testid="stTable"] table { margin-left: auto; margin-right: auto; width: 100%; }
    th, td { text-align: center !important; }
    </style>
    """, unsafe_allow_html=True)

# --- Data Persistence (Session State) ---
if 'history' not in st.session_state: st.session_state.history = []
if 'report_name' not in st.session_state: st.session_state.report_name = ""
if 'fixed_rate' not in st.session_state: st.session_state.fixed_rate = 0.0
if 'profile_pic' not in st.session_state: st.session_state.profile_pic = None

# --- Sidebar (Settings) ---
with st.sidebar:
    st.header("⚙️ Official Settings")
    st.session_state.report_name = st.text_input("Employee Name:", st.session_state.report_name)
    st.session_state.fixed_rate = st.number_input("Standard Rate (₹):", value=st.session_state.fixed_rate, step=1.0)
    
    # Large Photo Upload
    uploaded_file = st.file_uploader("Upload Profile Photo", type=['jpg', 'png', 'jpeg'])
    if uploaded_file: st.session_state.profile_pic = uploaded_file.read()
    
    if st.button("Update Profile", use_container_width=True): st.rerun()
    st.info("💡 Tip: Hafte mein ek baar niche diye gaye Backup button se Excel file save kar lein.")

# --- Profile Section ---
if st.session_state.profile_pic:
    img = Image.open(io.BytesIO(st.session_state.profile_pic))
    st.markdown('<div class="profile-container">', unsafe_allow_html=True)
    st.image(img, width=120)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="profile-container"><div style="font-size: 80px; background: #eee; border-radius: 50%; padding: 10px;">👤</div></div>', unsafe_allow_html=True)

st.markdown(f'<div class="official-header"><h2>📝 WORK REPORT PRO</h2><h4>{st.session_state.report_name if st.session_state.report_name else "Employee"}</h4></div>', unsafe_allow_html=True)

# --- Entry Section ---
with st.expander("➕ Add New Work Entry", expanded=True):
    col1, col2 = st.columns(2)
    with col1: date_today = st.date_input("Date", datetime.now())
    with col2: quantity = st.number_input("Quantity", min_value=1, step=1, value=1)
    
    total_amount = float(st.session_state.fixed_rate * quantity)
    
    if st.button("SAVE ENTRY ✅", use_container_width=True):
        if st.session_state.fixed_rate > 0:
            # Serial Number logic (Starts from 1)
            new_sno = len(st.session_state.history) + 1
            entry = {
                "Sno": new_sno,
                "Date": date_today.strftime("%d-%m-%Y"),
                "Quantity": int(quantity),
                "Amount": total_amount,
                "Month": date_today.strftime("%B %Y")
            }
            st.session_state.history.append(entry)
            st.success(f"Entry No. {new_sno} Saved!")
            st.rerun()
        else:
            st.error("Pehle sidebar mein Rate set karein!")

# --- Work Record ---
if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    st.markdown("### 📊 Work Record")
    
    all_months = sorted(df["Month"].unique())
    selected_month = st.selectbox("Month Filter", all_months)
    filtered_df = df[df["Month"] == selected_month]
    
    if not filtered_df.empty:
        t_qty = filtered_df["Quantity"].sum()
        t_amt = filtered_df["Amount"].sum()
        
        # Dashboard
        st.markdown(f"""
            <div class="dashboard-container">
                <div class="dashboard-value">Total Qty: {t_qty}</div>
                <div class="dashboard-value">Total: ₹{t_amt:.2f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Table
        st.table(filtered_df[["Sno", "Date", "Quantity", "Amount"]])

        # WhatsApp Share
        report_text = f"*WORK REPORT PRO - {st.session_state.report_name}*\n📅 {selected_month}\n\n"
        for _, row in filtered_df.iterrows():
            report_text += f"• {row['Date']} | Qty: {row['Quantity']} | ₹{row['Amount']:.2f}\n"
        report_text += f"\n*Total Qty: {t_qty}*\n*Total Amount: ₹{t_amt:.2f}*"
        st.link_button("Share on WhatsApp ✅", f"https://wa.me/?text={urllib.parse.quote(report_text)}", use_container_width=True)

    # --- EDIT & DELETE SECTION ---
    st.divider()
    with st.expander("🛠️ Edit or Delete Entries"):
        record_sno = st.selectbox("Sno Chunein:", options=filtered_df["Sno"].tolist())
        
        # Index dhundna edit karne ke liye
        idx = next(i for i, item in enumerate(st.session_state.history) if item['Sno'] == record_sno)
        
        new_q = st.number_input("New Quantity:", value=int(st.session_state.history[idx]['Quantity']), min_value=1)
        
        col_e, col_d = st.columns(2)
        if col_e.button("Update Entry"):
            st.session_state.history[idx]['Quantity'] = new_q
            st.session_state.history[idx]['Amount'] = new_q * st.session_state.fixed_rate
            st.success("Entry Updated!")
            st.rerun()
            
        if col_d.button("Delete Entry 🗑️"):
            st.session_state.history.pop(idx)
            # Sno Reset logic (1 se dobara line mein)
            for i, item in enumerate(st.session_state.history):
                item['Sno'] = i + 1
            st.warning("Entry Deleted and Snos Re-ordered!")
            st.rerun()

    # Permanent Download Button
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Excel Backup", data=csv, file_name=f"work_report_{datetime.now().strftime('%d_%m')}.csv", mime='text/csv', use_container_width=True)
else:
    st.info("Abhi koi entry nahi hai. Nayi entry karke shuru karein!")
    
