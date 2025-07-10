import streamlit as st
import pandas as pd
import os
import tempfile

# إعداد الصفحة
st.set_page_config(page_title="رفع وتعديل ملفات Excel", layout="centered")
st.title("📄 رفع وتعديل ملفات Excel")
st.markdown("### 🗂️ اختر ملفات Excel")

# دالة لحفظ الملف المعدل مؤقتًا
def save_temp_excel(df, original_filename):
    temp_filename = f"temp_{original_filename}"
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, temp_filename)

    with pd.ExcelWriter(temp_path, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, header=False)

    return temp_path

# واجهة رفع الملفات
uploaded_files = st.file_uploader(
    "ارفع ملف أو أكثر من نوع Excel",
    type=["xlsx", "xls"],
    accept_multiple_files=True
)

if uploaded_files:
    st.markdown("## ✅ الملفات المرفوعة:")

    for uploaded_file in uploaded_files:
        file_name = uploaded_file.name

        with st.expander(f"📂 {file_name} : اضغط للعرض والتعديل"):
            try:
                uploaded_file.seek(0)
                excel_file = pd.ExcelFile(uploaded_file)
                sheet_name = excel_file.sheet_names[0]
                df = pd.read_excel(excel_file, sheet_name=sheet_name, header=None, dtype=str)

                st.markdown(f"### 🧾 تعديل محتوى الملف: {file_name}")
                
                # عرض وتعديل مباشر
                edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")

                # حفظ مؤقت تلقائيًا
                temp_path = save_temp_excel(edited_df, file_name)
                st.success(f"✅ تم حفظ الملف المعدل مؤقتًا في المسار التالي:")
                st.code(temp_path)

            except Exception as e:
                st.error(f"❌ خطأ أثناء قراءة الملف {file_name}: {e}")
