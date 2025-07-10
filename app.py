import streamlit as st
import pandas as pd

st.set_page_config(page_title="رفع فواتير Excel", layout="centered")
st.title("📄 رفع فواتير Excel")

uploaded_files = st.file_uploader("اختر ملفات Excel", type=["xlsx", "xls"], accept_multiple_files=True)

if uploaded_files:
    st.subheader("📁 الملفات المرفوعة:")
    for file in uploaded_files:
        st.write(f"✅ {file.name}")
