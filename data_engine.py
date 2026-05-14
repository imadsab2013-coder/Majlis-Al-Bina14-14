import pandas as pd
import os

class DataEngine:
    def __init__(self):
        self.quran_path = "data/data_quran.xlsx"
        self.words_path = "data/data_words.xlsx"

    def get_data(self):
        if os.path.exists(self.quran_path) and os.path.exists(self.words_path):
            df_q = pd.read_excel(self.quran_path)
            df_w = pd.read_excel(self.words_path)
            return df_q, df_w
        return None, None

    def search_logic(self, df_q, df_w, word):
        # وظيفة A1: تحديد اللفظ
        res_w = df_w[df_w['word'] == word]
        # وظيفة A2: حصر السياقات
        res_q = df_q[df_q['text'].str.contains(word, na=False)]
        return res_w, res_q
