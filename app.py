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

        with st.expander(f"📂 {file_name} :اضغط لعرض"):
            try:
                uploaded_file.seek(0)
                excel_file = pd.ExcelFile(uploaded_file)
                first_sheet = excel_file.sheet_names[0]
                df = pd.read_excel(excel_file, sheet_name=first_sheet, header=None, dtype=str)

                st.markdown(f"### 🧾 محتوى: {file_name}")

                # إضافة خيار للعرض الكامل
                preview = st.toggle("👁️ عرض كل الصفوف", key=file_name)

                if preview:
                    st.dataframe(df, use_container_width=True, height=len(df) * 35)
                else:
                    st.dataframe(df.head(10), use_container_width=True, height=400)

            except Exception as e:
                st.error(f"❌ فشل في قراءة الملف {file_name}: {e}")
