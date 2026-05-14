import pandas as pd
import streamlit as st
import os

class QuranSearchEngine:
    def __init__(self):
        # المسارات المادية للملفات داخل المستودع
        self.words_path = "data/data_words.xlsx"
        self.quran_path = "data/data_quran.xlsx"

    def load_data(self):
        """تحميل المادة الخام من ملفات الإكسيل"""
        try:
            if os.path.exists(self.words_path) and os.path.exists(self.quran_path):
                df_words = pd.read_excel(self.words_path)
                df_quran = pd.read_excel(self.quran_path)
                return df_words, df_quran
            else:
                st.error("❌ خطأ: لم يتم العثور على المجلد data أو الملفات بداخله.")
                return None, None
        except Exception as e:
            st.error(f"❌ فشل في تحميل البيانات: {e}")
            return None, None

    def search_word_identity(self, df_words, word):
        """وظيفة العضو A1: البحث عن تعريف اللفظ في جدول الألفاظ"""
        # نستخدم الكلمة كمعيار للبحث في عمود 'word'
        result = df_words[df_words['word'] == word]
        return result if not result.empty else None

    def search_quran_contexts(self, df_quran, word):
        """وظيفة العضو A2: رصد جميع سياقات اللفظ في النص القرآني"""
        # البحث في عمود 'text' عن أي آية تحتوي على الكلمة
        # na=False لتجنب الأخطاء في حالة وجود خلايا فارغة
        results = df_quran[df_quran['text'].str.contains(word, na=False)]
        return results if not results.empty else None

    def get_verse_by_order(self, df_quran, absolute_order):
        """جلب آية محددة بناءً على الترتيب المطلق (للربط المادي)"""
        result = df_quran[df_quran['absolute_order'] == absolute_order]
        return result

# --- مثال لكيفية استخدام كود البحث في الواجهة ---
# engine = QuranSearchEngine()
# df_w, df_q = engine.load_data()
# word_data = engine.search_word_identity(df_w, "كتب")
# contexts = engine.search_quran_contexts(df_q, "كتب")
