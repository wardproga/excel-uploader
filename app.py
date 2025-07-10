import streamlit as st
import pandas as pd

st.set_page_config(page_title="رفع فواتير Excel", layout="centered")
st.title("📄 رفع فواتير Excel")
st.markdown("### 🗂️ اختر ملفات Excel")

uploaded_files = st.file_uploader(
    "رفع ملف أو أكثر",
    type=["xlsx", "xls"],
    accept_multiple_files=True
)

if uploaded_files:
    st.markdown("## ✅ الملفات المرفوعة:")

    for uploaded_file in uploaded_files:
        file_name = uploaded_file.name

        with st.expander(f"📂 {file_name} - اضغط للعرض"):
            try:
                # إعادة المؤشر لبداية الملف
                uploaded_file.seek(0)

                # قراءة الملف كاملاً بدون تجاهل أي صف أو عمود
                df = pd.read_excel(uploaded_file, header=None)

                # عرض المحتوى كاملًا
                st.markdown(f"### 🧾 محتوى: {file_name}")
                st.dataframe(df)

            except Exception as e:
                st.error(f"❌ خطأ أثناء قراءة الملف: {e}")
