import streamlit as st
import pandas as pd

st.set_page_config(page_title="رفع فواتير Excel", layout="centered")
st.title("📄 رفع فواتير")
st.markdown("### 🗂️ اختر ملفات Excel")

uploaded_files = st.file_uploader(
    "رفع ملف أو أكثر",
    type=["xlsx", "xls"],
    accept_multiple_files=True
)

if uploaded_files:
    st.markdown("## ✅ الملفات المرفوعة:")

    for uploaded_file in uploaded_files:
        file_name = uploaded_file.name

        if st.button(f"📂 معاينة: {file_name}", key=file_name):
            try:
                # قراءة الملف مؤقتاً بدون رؤوس
                df_preview = pd.read_excel(uploaded_file, header=None)
                st.markdown("📄 **معاينة أول 20 صف من الملف:**")
                st.dataframe(df_preview.head(20))

                # تحديد الصف الذي يحتوي على رؤوس الأعمدة
                header_row = st.number_input(
                    f"🔢 اختر رقم الصف الذي يحتوي على رؤوس الأعمدة ({file_name})",
                    min_value=0, max_value=len(df_preview)-1, value=0, step=1,
                    key=f"header_row_{file_name}"
                )

                # زر عرض الجدول الحقيقي
                if st.button(f"📊 عرض جدول البيانات الحقيقي - {file_name}", key=f"show_{file_name}"):
                    uploaded_file.seek(0)  # إعادة المؤشر لبداية الملف
                    df = pd.read_excel(uploaded_file, header=header_row)
                    st.success(f"✅ جدول: {file_name}")
                    st.dataframe(df)

            except Exception as e:
                st.error(f"❌ حدث خطأ أثناء قراءة الملف:\n{e}")
