import streamlit as st
import pandas as pd

# إعداد الصفحة
st.set_page_config(page_title="عرض ملفات Excel", layout="centered")

st.title("📄 رفع فواتير Excel")

uploaded_files = st.file_uploader(
    "اختر ملفات Excel",
    type=["xlsx", "xls"],
    accept_multiple_files=True
)

# تخزين في session_state
if 'uploaded_data' not in st.session_state:
    st.session_state.uploaded_data = {}

# عرض الأزرار لأسماء الملفات
if uploaded_files:
    for file in uploaded_files:
        file_name = file.name

        # إنشاء زر باسم الملف
        if st.button(f"📂 {file_name}"):
            try:
                # قراءة الملف
                df = pd.read_excel(file)
                st.session_state.uploaded_data[file_name] = df

                # فتح نافذة منبثقة لعرض البيانات
                with st.modal(f"📄 محتويات الملف: {file_name}"):
                    st.dataframe(df, use_container_width=True)
                    st.caption("اضغط خارج النافذة للإغلاق.")
            except Exception as e:
                st.error(f"❌ فشل في قراءة الملف {file_name}: {e}")
