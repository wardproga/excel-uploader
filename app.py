import streamlit as st
import os

# إعداد الصفحة
st.set_page_config(page_title="رفع فواتير Excel", layout="centered")

# CSS لتجاوب الهاتف وتحسين المظهر
st.markdown("""
    <style>
        @media screen and (max-width: 768px) {
            .block-container {
                padding: 1rem !important;
            }
        }
        .uploaded-file-box {
            background-color: #f0f8ff;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 5px;
            border: 1px solid #ccc;
        }
    </style>
""", unsafe_allow_html=True)

# العنوان
st.title("📄 رفع فواتير Excel")

# مربع رفع الملفات
uploaded_files = st.file_uploader(
    "اختر ملفات Excel",
    type=["xlsx", "xls"],
    accept_multiple_files=True
)

# عرض أسماء الملفات المرفوعة
if uploaded_files:
    st.markdown("### ✅ الملفات المرفوعة:")
    for file in uploaded_files:
        file_name = file.name
        file_ext = os.path.splitext(file_name)[1]
        st.markdown(f"""
            <div class="uploaded-file-box">
                📂 <strong>{file_name}</strong> <br>
                🧾 الامتداد: <code>{file_ext}</code>
            </div>
        """, unsafe_allow_html=True)
