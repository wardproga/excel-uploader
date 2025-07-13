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

st.title("📊 ملف أعمالي - تحليل البيانات")
st.markdown("مرحباً بك في تطبيق رفع وتحليل ملفات Excel")

# رفع ملف إكسل
uploaded_file = st.file_uploader("📁 الرجاء رفع ملف Excel", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        st.success("✅ تم رفع الملف بنجاح!")
        st.subheader("🧾 محتوى الملف:")
        st.dataframe(df)
        st.subheader("📊 إحصائيات سريعة:")
        st.write(df.describe())
    except Exception as e:
        st.error(f"❌ حدث خطأ أثناء قراءة الملف:\n{e}")

    # زر رفع الملف إلى Google Drive
    if st.button("☁️ رفع الملف إلى Google Drive"):
        try:
            # تحميل بيانات الاعتماد
            credentials_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
            credentials = service_account.Credentials.from_service_account_info(
                credentials_dict,
                scopes=["https://www.googleapis.com/auth/drive"]
            )

            # إنشاء خدمة Google Drive
            drive_service = build('drive', 'v3', credentials=credentials)

            # حفظ الملف مؤقتًا
            with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_file_path = tmp_file.name

            # إعداد بيانات الملف
            file_metadata = {
                'name': uploaded_file.name,
                'parents': ['1HgIm7YNXOLyv-idnd7eQKvVegdQsl8YT']  # معرف المجلد الذي زودتني به
            }
            media = MediaFileUpload(tmp_file_path, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

            # تنفيذ رفع الملف
            uploaded = drive_service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()

            st.success(f"✅ تم رفع الملف بنجاح إلى Google Drive! معرف الملف: {uploaded.get('id')}")
            os.remove(tmp_file_path)

        except Exception as e:
            st.error(f"❌ حدث خطأ أثناء رفع الملف:\n{e}")
else:
    st.info("⬆️ الرجاء رفع ملف Excel لعرض وتحليل البيانات.")
