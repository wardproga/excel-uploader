import streamlit as st
import pandas as pd
import json
import os
import tempfile
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# إعداد الصفحة
st.set_page_config(
    page_title="📊 ملف أعمالي - تحليل البيانات",
    page_icon="📈",
    layout="centered"
)

# عنوان التطبيق
st.title("📊 ملف أعمالي - تحليل البيانات")
st.markdown("مرحباً بك في تطبيق رفع وتحليل ملفات Excel")

# تحميل بيانات الاعتماد من secrets
credentials_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
credentials = service_account.Credentials.from_service_account_info(
    credentials_dict,
    scopes=["https://www.googleapis.com/auth/drive"]
)

# إنشاء خدمة Google Drive
drive_service = build('drive', 'v3', credentials=credentials)

# رفع ملف إكسل
uploaded_file = st.file_uploader("📁 الرجاء رفع ملف Excel", type=["xlsx", "xls"])

# إذا تم رفع الملف
if uploaded_file is not None:
    try:
        # قراءة البيانات
        df = pd.read_excel(uploaded_file)

        # عرض رسالة نجاح
        st.success("✅ تم رفع الملف بنجاح!")

        # عرض البيانات
        st.subheader("🧾 محتوى الملف:")
        st.dataframe(df)

        # عرض إحصائيات عامة
        st.subheader("📊 إحصائيات سريعة:")
        st.write(df.describe())

        # زر رفع إلى Google Drive
        if st.button("☁️ رفع الملف إلى Google Drive"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_file_path = tmp_file.name

            file_metadata = {
                'name': uploaded_file.name,
                'mimeType': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            }

            media = MediaFileUpload(tmp_file_path, mimetype=file_metadata['mimeType'])
            uploaded = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

            st.success("🚀 تم رفع الملف إلى Google Drive بنجاح! ✅")

    except Exception as e:
        st.error(f"❌ حدث خطأ أثناء قراءة الملف:\n{e}")
else:
    st.info("⬆️ الرجاء رفع ملف Excel لعرض وتحليل البيانات.")
