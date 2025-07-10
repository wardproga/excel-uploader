import streamlit as st
import pandas as pd

st.set_page_config(page_title="رفع فواتير Excel", layout="centered")

st.title("📄 رفع فواتير")
st.subheader("اختر ملفات Excel")

uploaded_files = st.file_uploader(
    "Drag and drop files here",
    type=["xlsx", "xls"],
    accept_multiple_files=True,
    label_visibility="collapsed"
)

if uploaded_files:
    st.markdown("## 📁 الملفات المرفوعة:")
    for file in uploaded_files:
        file_name = file.name
        file_extension = file_name.split('.')[-1]

        # عرض اسم الملف كزر
        if st.button(f"📂 {file_name}"):
            try:
                # قراءة الملف مع تخطي أول 16 صفًا
                df = pd.read_excel(file, header=16)
                st.success(f"✅ {file_name} : محتوى الملف")
                st.dataframe(df)
            except Exception as e:
                st.error(f"❌ {file_name} فشل في قراءة الملف:\n{e}")
