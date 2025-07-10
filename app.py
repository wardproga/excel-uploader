import streamlit as st

# إعداد الصفحة
st.set_page_config(page_title="رفع فواتير Excel", layout="centered")

# العنوان
st.title("📄 رفع فواتير Excel")

# مربع رفع الملفات فقط
uploaded_files = st.file_uploader(
    "اختر ملفات Excel",
    type=["xlsx", "xls"],
    accept_multiple_files=True
)

# لا عرض لأي شيء أسفل مربع الرفع (تم حذف كل المخرجات الإضافية)
