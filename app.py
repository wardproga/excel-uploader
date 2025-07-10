import streamlit as st
import pandas as pd

# إعداد الصفحة
st.set_page_config(page_title="رفع فواتير Excel", layout="centered")

# تخصيص CSS للتجاوب مع الهواتف
st.markdown("""
    <style>
        @media screen and (max-width: 768px) {
            .block-container {
                padding: 1rem !important;
            }
        }
        .css-1y4p8pa {
            border: 2px dashed #4a90e2;
            padding: 20px;
            border-radius: 10px;
            background-color: #f7fafd;
        }
        @media screen and (max-width: 480px) {
            h1, .stTitle {
                font-size: 1.5rem;
            }
            .stFileUploader {
                font-size: 0.9rem;
            }
        }
    </style>
""", unsafe_allow_html=True)

# العنوان
st.title("📄 رفع فواتير Excel")

# رفع ملفات
uploaded_files = st.file_uploader("اختر ملفات Excel", type=["xlsx", "xls"], accept_multiple_files=True)

if uploaded_files:
    st.subheader("📁 الملفات المرفوعة:")
    for file in uploaded_files:
        st.write(f"✅ {file.name}")
