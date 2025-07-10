import streamlit as st
import pandas as pd
import os

# إعداد الصفحة
st.set_page_config(page_title="رفع فواتير Excel", layout="centered")

st.title("📄 رفع فواتير Excel")
st.markdown("### اختر ملفات Excel")

# رفع الملفات
uploaded_files = st.file_uploader(
    "Drag and drop files here",
    type=["xlsx", "xls"],
    accept_multiple_files=True,
    label_visibility="collapsed"
)

# تخزين الملفات المؤقتة
if uploaded_files:
    st.markdown("### 📁 الملفات المرفوعة:")
    for file in uploaded_files:
        # عرض اسم الملف كزر قابل للنقر
        if st.button(f"📂 {file.name}"):
            try:
                df = pd.read_excel(file)
                with st.expander(f"📊 محتوى الملف: {file.name}", expanded=True):
                    st.dataframe(df)
            except Exception as e:
                st.error(f"❌ فشل في قراءة الملف {file.name}:\n{str(e)}")
