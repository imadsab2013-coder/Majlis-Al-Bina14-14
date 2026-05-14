import streamlit as st
import pandas as pd
import os

# --- 1. محرك البيانات المدمج (Data Engine) ---
class DataEngine:
    @staticmethod
    def load_local_resources():
        """جلب المادة الخام من المجلد المحلي data/"""
        # المسارات المادية كما هي في GitHub الخاص بك
        path_quran = "data/data_quran.xlsx"
        path_words = "data/data_words.xlsx"
        
        try:
            # التحقق من وجود المجلد والملفات أولاً
            if os.path.exists(path_quran) and os.path.exists(path_words):
                df_quran = pd.read_excel(path_quran)
                df_words = pd.read_excel(path_words)
                return df_quran, df_words
            else:
                st.error("⚠️ خطأ مادي: المجلد 'data' أو الملفات غير موجودة في الجذر.")
                return None, None
        except Exception as e:
            st.error(f"❌ فشل في قراءة الإكسيل: {e}")
            return None, None

# --- 2. إعدادات واجهة مجلس البينة ---
st.set_page_config(page_title="مجلس البينة 14-14", layout="wide")

# تصميم السبورة
st.markdown("""
    <style>
    .stTable { background-color: #ffffff; }
    .main-header { color: #1e3a8a; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.title("⚙️ تحكم المختبر")
    # زر المزامنة يقرأ الآن من الملفات المحلية مباشرة
    if st.button("🔄 تفعيل اتصال الداتا"):
        df_q, df_w = DataEngine.load_local_resources()
        if df_q is not None:
            st.session_state['df_quran'] = df_q
            st.session_state['df_words'] = df_w
            st.success("🟢 اللمبة خضراء: تم الاتصال بمجلد data")

    st.write("---")
    st.subheader("👥 الأعضاء النشطين")
    a1_active = st.toggle("A1: المستقبل", value=True)
    a2_active = st.toggle("A2: المحلل السياقي", value=True)

# --- 3. السبورة المركزية (Main Board) ---
st.markdown('<h1 class="main-header">🏛️ مجلس البينة - التحليل المادي</h1>', unsafe_allow_html=True)

# خانة البحث
target_word = st.text_input("أدخل اللفظ المكتوب المراد رصده:", placeholder="مثال: كتب")

if target_word:
    if 'df_words' in st.session_state and 'df_quran' in st.session_state:
        df_words = st.session_state['df_words']
        df_quran = st.session_state['df_quran']
        
        # تنفيذ مهام العضو A1 (تحديد الهوية المادية للفظ)
        if a1_active:
            st.subheader("📦 بيانات اللفظ (العضو A1)")
            # البحث عن اللفظ في عمود 'word'
            word_result = df_words[df_words['word'] == target_word]
            
            if not word_result.empty:
                st.dataframe(word_result, use_container_width=True)
                
                # تنفيذ مهام العضو A2 (رصد السياقات النصية)
                if a2_active:
                    st.write("---")
                    st.subheader(f"📖 السياقات المادية للفظ '{target_word}' (العضو A2)")
                    # البحث في نص القرآن
                    # ملاحظة: تأكد أن اسم العمود في الإكسيل هو 'text'
                    context_results = df_quran[df_quran['text'].str.contains(target_word, na=False)]
                    
                    if not context_results.empty:
                        st.info(f"تم رصد {len(context_results)} مورد مادي.")
                        st.table(context_results[['absolute_order', 'surah', 'ayah', 'text']].head(20))
                    else:
                        st.warning("اللفظ موجود في الجداول ولكن لم يُرصد له نص مطابق في ملف القرآن.")
            else:
                st.error(f"اللفظ '{target_word}' غير مدرج في سجلات البيانات الحالية.")
    else:
        st.warning("⚠️ المجلس بانتظار المادة الخام. اضغط على 'تفعيل اتصال الداتا' من القائمة الجانبية.")

# تذييل تقني
if 'df_quran' in st.session_state:
    st.divider()
    st.caption(f"قاعدة البيانات النشطة: {len(st.session_state['df_quran'])} سطر مادي.")
