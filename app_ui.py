import streamlit as st
from data_engine import DataEngine

# إعدادات الواجهة
st.set_page_config(page_title="مختبر البينة 14", layout="wide")
engine = DataEngine()

st.title("🏛️ مجلس البينة - منصة التطوير 14")

# المزامنة
if st.sidebar.button("🔄 تحديث المادة الخام"):
    df_q, df_w = engine.get_data()
    if df_q is not None:
        st.session_state['data'] = (df_q, df_w)
        st.sidebar.success("🟢 تم تحميل البيانات")

# البحث
word = st.text_input("أدخل اللفظ المادي للبحث:")

if word and 'data' in st.session_state:
    df_q, df_w = st.session_state['data']
    res_w, res_q = engine.search_logic(df_q, df_w, word)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📦 بيانات اللفظ (A1)")
        st.write(res_w)
    with col2:
        st.subheader("📖 السياقات المرصودة (A2)")
        st.dataframe(res_q[['absolute_order', 'text']])
else:
    st.info("قم بتفعيل اتصال الداتا من القائمة الجانبية.")
