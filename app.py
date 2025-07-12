import streamlit as st
import pandas as pd
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import tempfile
import os

st.set_page_config(page_title="رفع ملفات Excel إلى Google Drive", layout="centered")

st.title("📁 رفع وتعديل ملفات Excel إلى Google Drive")

# تحميل بيانات الاعتماد من secrets
credentials_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
credentials = service_account.Credentials.from_service_account_info(
    credentials_dict,
    scopes=["https://www.googleapis.com/auth/drive"]
)

# إنشاء خدمة Google Drive
drive_service = build('drive', 'v3', credentials=credentials)

# رفع ملف Excel
uploaded_file = st.file_uploader("اختر ملف Excel لرفعه إلى Google Drive", type=["xlsx"])

if uploaded_file is not None:
    # عرض البيانات كمراجعة
    df = pd.read_excel(uploaded_file)
    st.write("📊 محتوى الملف:")
    st.dataframe(df)

    # رفع الملف إلى Google Drive
    if st.button("📤 رفع الملف"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_file_path = tmp_file.name

        file_metadata = {
            'name': uploaded_file.name,
            'mimeType': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        }
        media = MediaFileUpload(tmp_file_path, mimetype=file_metadata['mimeType'])

        uploaded = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, name'
        ).execute()

        st.success(f"✅ تم رفع الملف بنجاح! اسم الملف: {uploaded['name']}")
        os.remove(tmp_file_path)
