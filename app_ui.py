import streamlit as st
import pandas as pd
import os

# --- إعدادات الواجهة ---
st.set_page_config(page_title="مجلس البينة - التحليل المادي", layout="wide")

# --- محرك البحث المادي (لوكال) ---
def load_data():
    # المسارات المادية الصحيحة حسب GitHub ديالك
    path_quran = "data/data_quran.xlsx"
    path_words = "data/data_words.xlsx"
    
    if os.path.exists(path_quran) and os.path.exists(path_words):
        try:
            df_q = pd.read_excel(path_quran)
            df_w = pd.read_excel(path_words)
            return df_q, df_w
        except Exception as e:
            st.error(f"خطأ في قراءة الجداول: {e}")
            return None, None
    else:
        st.error("⚠️ الملفات غير موجودة في مجلد data. تأكد من المسارات في GitHub.")
        return None, None

# --- الجانب الجمالي والتحكم ---
with st.sidebar:
    st.title("⚙️ تحكم المختبر")
    if st.button("🔄 تفعيل اتصال الداتا"):
        df_q, df_w = load_data()
        if df_q is not None:
            st.session_state['df_quran'] = df_q
            st.session_state['df_words'] = df_w
            st.success("🟢 الداتا متصلة الآن")

# --- السبورة المركزية ---
st.title("🏛️ مجلس البينة - التحليل المادي")

word_input = st.text_input("أدخل اللفظ المراد رصده:", placeholder="مثال: كتب")

if word_input:
    if 'df_words' in st.session_state:
        df_w = st.session_state['df_words']
        df_q = st.session_state['df_quran']
        
        # البحث في جدول الألفاظ (A1)
        res_a1 = df_w[df_w['word'] == word_input]
        
        if not res_a1.empty:
            st.subheader("📦 بيانات اللفظ (A1)")
            st.dataframe(res_a1)
            
            # البحث في نص القرآن (A2)
            st.subheader("📖 السياقات المادية (A2)")
            res_a2 = df_q[df_q['text'].str.contains(word_input, na=False)]
            st.table(res_a2[['absolute_order', 'surah', 'ayah', 'text']].head(20))
        else:
            st.warning("اللفظ غير موجود في سجلات الداتا.")
    else:
        st.info("💡 اضغط على 'تفعيل اتصال الداتا' في القائمة الجانبية أولاً.")
