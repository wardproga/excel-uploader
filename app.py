تفضل يا معاذ، إليك الكود الكامل المحدث في ملف app.py، والذي يحتوي على:


---

✅ الميزات المضمنة:

رفع ملف Excel.

عرض البيانات داخل التطبيق.

تعديل الخلايا مباشرة داخل Streamlit.

زر لحفظ وتنزيل الملف بعد التعديل.

زر لرفع الملف (الأصلي أو المعدل) إلى Google Drive داخل مجلدك المشترك.



---

📄 app.py:

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
st.markdown("مرحباً بك في تطبيق رفع وتحليل وتعديل ملفات Excel")

# رفع ملف إكسل
uploaded_file = st.file_uploader("📁 الرجاء رفع ملف Excel", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        st.success("✅ تم رفع الملف بنجاح!")

        # تعديل البيانات
        st.subheader("📝 قم بتعديل البيانات:")
        edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")

        # عرض إحصائيات
        st.subheader("📊 إحصائيات سريعة:")
        st.write(edited_df.describe())

        # حفظ الملف المعدل وتنزيله
        if st.button("💾 تنزيل الملف بعد التعديل"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
                edited_df.to_excel(tmp.name, index=False)
                tmp_path = tmp.name

            with open(tmp_path, "rb") as f:
                st.download_button(
                    label="⬇️ تحميل الملف المعدل",
                    data=f,
                    file_name="بيانات_معدلة.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

        # زر لرفع الملف إلى Google Drive
        if st.button("☁️ رفع الملف المعدل إلى Google Drive"):
            try:
                # تحميل بيانات الاعتماد من secrets
                credentials_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
                credentials = service_account.Credentials.from_service_account_info(
                    credentials_dict,
                    scopes=["https://www.googleapis.com/auth/drive"]
                )

                # إنشاء خدمة Google Drive
                drive_service = build('drive', 'v3', credentials=credentials)

                # حفظ الملف المعدل مؤقتاً
                with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp_file:
                    edited_df.to_excel(tmp_file.name, index=False)
                    tmp_file_path = tmp_file.name

                # رفع الملف إلى المجلد المشترك
                file_metadata = {
                    'name': uploaded_file.name,
                    'parents': ['1HgIm7YNXOLyv-idnd7eQKvVegdQsl8YT'],  # معرف المجلد الذي زودتني به
                    'mimeType': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                }

                media = MediaFileUpload(tmp_file_path, mimetype=file_metadata['mimeType'])

                uploaded = drive_service.files().create(
                    body=file_metadata,
                    media_body=media,
                    fields='id'
                ).execute()

                st.success(f"🚀 تم رفع الملف إلى Google Drive بنجاح! معرف الملف: {uploaded.get('id')}")
                os.remove(tmp_file_path)

            except Exception as e:
                st.error(f"❌ خطأ أثناء الرفع إلى Google Drive:\n{e}")

    except Exception as e:
        st.error(f"❌ حدث خطأ أثناء قراءة الملف:\n{e}")
else:
    st.info("⬆️ الرجاء رفع ملف Excel لعرض وتعديل البيانات.")


---

✅ جاهز للنشر على GitHub وStreamlit Cloud مباشرة

هل تود أن أرفعه لك على GitHub أيضًا؟
أو نبدأ بإضافة ميزات جديدة مثل رسم بياني تلقائي أو البحث داخل الجدول؟

