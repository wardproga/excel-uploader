import streamlit as st
import pandas as pd
import tempfile
import os
import json
import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

# إعداد الصفحة
st.set_page_config(page_title="رفع وتعديل ملفات Excel", layout="wide")
st.title("📂 تعديل ورفع ملفات Excel إلى Google Drive")

# إعداد Google Drive API
@st.cache_resource
def get_gdrive_service():
    credentials_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
    credentials = service_account.Credentials.from_service_account_info(credentials_dict)
    return build("drive", "v3", credentials=credentials)

drive_service = get_gdrive_service()

# رفع الملفات
uploaded_files = st.file_uploader("📤 ارفع ملفات Excel", type=["xlsx", "xls"], accept_multiple_files=True)

# حفظ الملف المعدل مؤقتًا
def save_temp_excel(df, original_filename):
    temp_filename = f"temp_{original_filename}"
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, temp_filename)

    with pd.ExcelWriter(temp_path, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, header=False)

    return temp_path

# رفع إلى Google Drive
def upload_to_drive(filepath, filename):
    file_metadata = {"name": filename}
    with open(filepath, "rb") as f:
        media = MediaIoBaseUpload(f, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        uploaded_file = drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    return uploaded_file.get("id")

# التعامل مع الملفات
if uploaded_files:
    for uploaded_file in uploaded_files:
        with st.expander(f"📄 {uploaded_file.name}"):
            try:
                df = pd.read_excel(uploaded_file, header=None)
                st.markdown("⬇️ يمكنك التعديل على الجدول أدناه")
                edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")

                # حفظ الملف مؤقتًا
                saved_path = save_temp_excel(edited_df, uploaded_file.name)

                # تحميل محلي
                with open(saved_path, "rb") as f:
                    st.download_button("⬇️ تحميل الملف المعدل", f, file_name=f"تعديل_{uploaded_file.name}")

                # رفع إلى Google Drive
                if st.button(f"📤 رفع {uploaded_file.name} إلى Google Drive"):
                    file_id = upload_to_drive(saved_path, f"تعديل_{uploaded_file.name}")
                    st.success(f"✅ تم رفع الملف إلى Google Drive بنجاح! [فتح الملف](https://drive.google.com/file/d/{file_id})")

            except Exception as e:
                st.error(f"❌ خطأ أثناء معالجة الملف: {e}")
