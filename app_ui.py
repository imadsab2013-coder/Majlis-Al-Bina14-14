import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# --- البروتوكول المادي للربط بين المستودعات ---
# الربط مع المخزن الرئيسي 13-05
ORIGIN_USER = "imadsab2013-coder"
ORIGIN_REPO = "Majlis-Al-Bina13-05"
BRANCH = "main"

# روابط المادة الخام
URL_QURAN = f"https://raw.githubusercontent.com/{ORIGIN_USER}/{ORIGIN_REPO}/{BRANCH}/data/data_quran.xlsx"
URL_WORDS = f"https://raw.githubusercontent.com/{ORIGIN_USER}/{ORIGIN_REPO}/{BRANCH}/data/data_words.xlsx"

def load_data_from_origin(url):
    """وظيفة العضو A1: سحب المادة الخام من المخزن الرئيسي"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return pd.read_excel(BytesIO(response.content))
    except Exception as e:
        st.error(f"⚠️ فشل الاتصال بالمخزن 13-05: {e}")
        return None

# --- إعدادات واجهة مجلس البينة ---
st.set_page_config(page_title="مختبر البينة 14-14", layout="wide")

st.title("🧪 مختبر التطوير (14-14)")
st.caption(f"متصل حالياً بالمخزن الرئيسي: {ORIGIN_REPO}")

# المزامنة
if st.sidebar.button("🔄 مزامنة مع المخزن 13-05"):
    with st.spinner("جاري جلب البيانات..."):
        df_q = load_data_from_origin(URL_QURAN)
        df_w = load_data_from_origin(URL_WORDS)
        if df_q is not None and df_w is not None:
            st.session_state['data_quran'] = df_q
            st.session_state['data_words'] = df_w
            st.sidebar.success("🟢 البيانات محملة وجاهزة")

# --- منطقة الاختبار (السبورة) ---
word_to_search = st.text_input("أدخل اللفظ للاختبار:")

if word_to_search:
    if 'data_words' in st.session_state:
        # منطق العضو A1 في البحث
        data_w = st.session_state['data_words']
        result = data_w[data_w['word'] == word_to_search]
        
        if not result.empty:
            st.success(f"تم العثور على اللفظ: {word_to_search}")
            st.write(result)
            
            # هنا نربط مع العضو A2 لجلب الآيات
            if 'data_quran' in st.session_state:
                st.subheader("📖 السياقات المادية (من ملف القرآن)")
                # عرض عينة من ملف القرآن (سنطور منطق الربط لاحقاً)
                st.dataframe(st.session_state['data_quran'].head(10))
        else:
            st.error("اللفظ غير موجود في قاعدة بيانات 13-05")
    else:
        st.warning("يرجى الضغط على زر المزامنة أولاً.")

