"""
═══════════════════════════════════════════════════════════════════════════════
مشروع: مجلس البينة | Project: Majlis Al-Bina
الملف الأول: الواجهة الرئيسية | File: app_ui.py (Main UI)
═══════════════════════════════════════════════════════════════════════════════

المسؤولية: بناء الواجهة الكاملة بناءً على الكتالوج رقم 1
- السبورة المركزية
- شريط الأيقونات العلوي (الأعضاء 1A - 10A)
- الشريط الجانبي (الإعدادات والقواعس)
- مؤشرات الحالة (اللمبة الخضراء/الحمراء)
"""

import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import os

# ═══════════════════════════════════════════════════════════════════════════════
# 🎨 إعدادات الصفحة والتكوين الأساسي
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="مجلس البينة | Majlis Al-Bina",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS مخصص للواجهة
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<style>
    /* الخط والقاعدة الأساسية */
    * {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        direction: rtl;
    }
    
    /* تنسيق الجسم الرئيسي */
    .main {
        padding: 0;
    }
    
    /* شريط الأيقونات العلوي */
    .agent-bar {
        display: flex;
        flex-direction: row-reverse;
        gap: 8px;
        padding: 12px;
        background: linear-gradient(to bottom, #0f1419, #1a202c);
        border-bottom: 2px solid #2d3748;
        border-radius: 0;
        margin-bottom: 16px;
        overflow-x: auto;
    }
    
    /* أيقونة الوكيل */
    .agent-icon {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: linear-gradient(135deg, #2d3748, #4a5568);
        cursor: pointer;
        transition: all 0.3s ease;
        border: 2px solid transparent;
        position: relative;
    }
    
    .agent-icon:hover {
        transform: scale(1.1);
        border-color: #4299e1;
        box-shadow: 0 0 12px rgba(66, 153, 225, 0.4);
    }
    
    .agent-icon.active {
        background: linear-gradient(135deg, #4299e1, #3182ce);
        border-color: #2b6cb0;
        box-shadow: 0 0 16px rgba(66, 153, 225, 0.6);
    }
    
    /* مؤشر الحالة (اللمبة) */
    .status-light {
        position: absolute;
        top: 2px;
        right: 2px;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background-color: #cbd5e0;
        animation: pulse 2s infinite;
    }
    
    .status-light.green {
        background-color: #48bb78;
        box-shadow: 0 0 8px rgba(72, 187, 120, 0.8);
    }
    
    .status-light.red {
        background-color: #f56565;
        box-shadow: 0 0 8px rgba(245, 101, 101, 0.8);
    }
    
    .status-light.blinking {
        animation: blink 0.8s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }
    
    /* نص الأيقونة */
    .agent-icon-text {
        font-size: 11px;
        font-weight: bold;
        color: #e2e8f0;
        text-align: center;
    }
    
    /* السبورة الرئيسية */
    .board-container {
        background: #f7fafc;
        border-radius: 8px;
        padding: 20px;
        min-height: 400px;
        border: 1px solid #e2e8f0;
    }
    
    /* بلوك الوكيل */
    .agent-block {
        background: white;
        border-right: 4px solid #4299e1;
        border-radius: 6px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .agent-block:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    .agent-block-header {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 8px;
    }
    
    .agent-block-id {
        background: #4299e1;
        color: white;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 12px;
    }
    
    .agent-block-name {
        font-weight: bold;
        color: #2d3748;
        font-size: 14px;
    }
    
    .agent-block-content {
        color: #4a5568;
        font-size: 13px;
        line-height: 1.6;
        padding-right: 36px;
    }
    
    /* صندوق الإدخال */
    .input-section {
        margin-top: 16px;
        padding: 12px;
        background: #edf2f7;
        border-radius: 6px;
        border-left: 3px solid #4299e1;
    }
    
    /* الشريط الجانبي */
    .sidebar-section {
        background: #f7fafc;
        border-radius: 6px;
        padding: 12px;
        margin-bottom: 12px;
        border: 1px solid #e2e8f0;
    }
    
    .sidebar-section-title {
        font-weight: bold;
        color: #2d3748;
        margin-bottom: 8px;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* الأزرار */
    .btn-action {
        padding: 8px 12px;
        border-radius: 4px;
        border: none;
        cursor: pointer;
        font-weight: 500;
        transition: all 0.2s ease;
        font-size: 12px;
    }
    
    .btn-primary {
        background: #4299e1;
        color: white;
    }
    
    .btn-primary:hover {
        background: #3182ce;
    }
    
    .btn-danger {
        background: #f56565;
        color: white;
    }
    
    .btn-danger:hover {
        background: #e53e3e;
    }
    
    .btn-success {
        background: #48bb78;
        color: white;
    }
    
    .btn-success:hover {
        background: #38a169;
    }
    
    /* رسالة التنبيه */
    .alert-box {
        padding: 12px;
        border-radius: 4px;
        margin-bottom: 8px;
        font-size: 12px;
    }
    
    .alert-warning {
        background: #fffff5;
        border-left: 4px solid #f6ad55;
        color: #7c2d12;
    }
    
    .alert-info {
        background: #f0f9ff;
        border-left: 4px solid #4299e1;
        color: #1e40af;
    }
    
    .alert-success {
        background: #f0fdf4;
        border-left: 4px solid #48bb78;
        color: #15803d;
    }
    
    .alert-error {
        background: #fef2f2;
        border-left: 4px solid #f56565;
        color: #991b1b;
    }
    
    /* جدول القواعس */
    .rules-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 12px;
    }
    
    .rules-table th {
        background: #edf2f7;
        padding: 8px;
        text-align: right;
        border-bottom: 1px solid #cbd5e0;
        font-weight: bold;
        color: #2d3748;
    }
    
    .rules-table td {
        padding: 8px;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .rules-table tr:hover {
        background: #f7fafc;
    }
    
    /* عنوان الصفحة */
    .page-title {
        text-align: center;
        color: #2d3748;
        margin-bottom: 20px;
        font-size: 28px;
        font-weight: bold;
    }
    
    .page-subtitle {
        text-align: center;
        color: #718096;
        margin-bottom: 20px;
        font-size: 13px;
    }

</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 🔧 تهيئة Session State
# ═══════════════════════════════════════════════════════════════════════════════

def initialize_session():
    """تهيئة جميع متغيرات الجلسة"""
    
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ""
    
    if 'model_choice' not in st.session_state:
        st.session_state.model_choice = "Gemini"
    
    if 'temperature' not in st.session_state:
        st.session_state.temperature = 0.7
    
    if 'rules' not in st.session_state:
        st.session_state.rules = []
    
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    
    if 'active_agent' not in st.session_state:
        st.session_state.active_agent = None
    
    if 'connection_status' not in st.session_state:
        st.session_state.connection_status = {
            'api': False,
            'data_quran': False,
            'data_words': False
        }
    
    if 'board_output' not in st.session_state:
        st.session_state.board_output = []

initialize_session()

# ═══════════════════════════════════════════════════════════════════════════════
# 📊 تعريف الأعضاء العشرة (Agent Matrix)
# ═══════════════════════════════════════════════════════════════════════════════

AGENTS = {
    '1A': {'name': 'المستقبل', 'emoji': '📥', 'role': 'Receiver/Collector', 'color': '#4299e1'},
    '2A': {'name': 'المحلل', 'emoji': '🔍', 'role': 'Contextual Analyzer', 'color': '#38a169'},
    '3A': {'name': 'المقارن', 'emoji': '⚖️', 'role': 'Comparative Analyst', 'color': '#ed8936'},
    '4A': {'name': 'الراصد', 'emoji': '👁️', 'role': 'Observer', 'color': '#9f7aea'},
    '5A': {'name': 'الناقد', 'emoji': '❌', 'role': 'Logic Critic', 'color': '#f56565'},
    '6A': {'name': 'حارس القواعس', 'emoji': '⚔️', 'role': 'Rule Guardian', 'color': '#c53030'},
    '7A': {'name': 'المصنف', 'emoji': '📚', 'role': 'Classifier', 'color': '#2d3748'},
    '8A': {'name': 'الآمر', 'emoji': '👑', 'role': 'The Commander', 'color': '#1a202c'},
    '9A': {'name': 'الصيغ', 'emoji': '✍️', 'role': 'Final Formatter', 'color': '#805ad5'},
    '10A': {'name': 'المحرك', 'emoji': '⚙️', 'role': 'Orchestrator', 'color': '#0284c7'},
}

# ═══════════════════════════════════════════════════════════════════════════════
# 🌐 دوال الاتصال والفحص
# ═══════════════════════════════════════════════════════════════════════════════

def check_data_files():
    """فحص وجود ملفات البيانات"""
    data_path = Path("data")
    quran_file = data_path / "data_quran.xlsx"
    words_file = data_path / "data_words.xlsx"
    
    return {
        'data_quran': quran_file.exists(),
        'data_words': words_file.exists()
    }

def test_api_connection(api_key):
    """اختبار اتصال API (محاكاة مبدئية)"""
    # سيتم ربطه بـ main_controller لاحقاً
    if not api_key or len(api_key) < 10:
        return False
    return True

def update_connection_status():
    """تحديث حالة الاتصال"""
    data_files = check_data_files()
    
    st.session_state.connection_status['data_quran'] = data_files['data_quran']
    st.session_state.connection_status['data_words'] = data_files['data_words']
    
    if st.session_state.api_key:
        st.session_state.connection_status['api'] = test_api_connection(st.session_state.api_key)

# ═══════════════════════════════════════════════════════════════════════════════
# 🏠 الجزء الرئيسي: تخطيط الصفحة
# ═══════════════════════════════════════════════════════════════════════════════

# العنوان الرئيسي
st.markdown('<div class="page-title">📖 مجلس البينة</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Majlis Al-Bina - نظام تحليل النص القرآني الذكي | Quranic Text Analysis System</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# شريط الأيقونات العلوي (أعضاء 1A - 10A)
# ─────────────────────────────────────────────────────────────────────────────

st.markdown('<div class="agent-bar">', unsafe_allow_html=True)

cols = st.columns(10)
for idx, (agent_id, agent_info) in enumerate(sorted(AGENTS.items(), reverse=True)):
    with cols[9 - idx]:  # عكس الترتيب لتوافق RTL
        # تحديد حالة المؤشر
        api_status = "🟢" if st.session_state.connection_status['api'] else "🔴"
        data_status = "🟢" if (st.session_state.connection_status['data_quran'] and 
                              st.session_state.connection_status['data_words']) else "🔴"
        
        # اختيار المؤشر بناءً على نوع الوكيل
        if agent_id == '8A':
            indicator = "🟡"  # الآمر له مؤشر خاص
        else:
            indicator = api_status
        
        # عرض الأيقونة
        if st.button(
            f"{agent_info['emoji']}\n{agent_id}",
            key=f"agent_{agent_id}",
            use_container_width=True,
            help=f"{agent_info['role']}: {agent_info['name']}"
        ):
            st.session_state.active_agent = agent_id
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# تنبيه حول استقلالية الواجهة
# ─────────────────────────────────────────────────────────────────────────────

update_connection_status()  # تحديث حالة الاتصال قبل العرض

if not st.session_state.connection_status['api']:
    st.info(
        "ℹ️ **الواجهة تعمل بشكل مستقل عن API:** "
        "يمكنك استخدام محرك البحث وإدارة البيانات حتى بدون مفتاح API. "
        "أضف المفتاح لتفعيل التحليل بواسطة الذكاء الاصطناعي.",
        icon="ℹ️"
    )

# ─────────────────────────────────────────────────────────────────────────────
# المحتوى الرئيسي (السبورة + الشريط الجانبي)
# ─────────────────────────────────────────────────────────────────────────────

col_main, col_sidebar = st.columns([3, 1])

# ═════════════════════════════════════════════════════════════════════════════
# 🎯 العمود الرئيسي: السبورة
# ═════════════════════════════════════════════════════════════════════════════

with col_main:
    st.markdown("### 📊 السبورة (The Board)")
    
    board_container = st.container(border=True)
    
    with board_container:
        # عرض السجل الحالي
        if st.session_state.board_output:
            for message in st.session_state.board_output:
                agent_id = message.get('agent_id', 'System')
                agent_name = AGENTS.get(agent_id, {}).get('name', 'نظام')
                agent_emoji = AGENTS.get(agent_id, {}).get('emoji', '⚙️')
                
                st.markdown(f"""
                <div class="agent-block">
                    <div class="agent-block-header">
                        <div class="agent-block-id">{agent_id}</div>
                        <div class="agent-block-name">{agent_emoji} {agent_name}</div>
                    </div>
                    <div class="agent-block-content">{message.get('content', '')}</div>
                    <small style="color: #a0aec0;">{message.get('timestamp', '')}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("🌫️ السبورة فارغة الآن. أدخل استفسار وسيبدأ التحليل.", icon="ℹ️")
    
    # صندوق الإدخال
    st.markdown("### 📝 إدخال الاستفسار")
    
    input_col1, input_col2 = st.columns([4, 1])
    
    with input_col1:
        user_input = st.text_area(
            "أدخل سؤالك أو ملحوظتك:",
            placeholder="مثال: ابحث عن كلمة 'الحكمة' في القرآن وحلل سياقاتها",
            height=80,
            label_visibility="collapsed"
        )
    
    with input_col2:
        submit_btn = st.button(
            "📤 إرسال",
            use_container_width=True,
            type="primary"
        )
    
    if submit_btn and user_input:
        # إضافة الرسالة إلى السجل (مؤقتاً)
        st.session_state.board_output.append({
            'agent_id': 'USER',
            'content': user_input,
            'timestamp': datetime.now().strftime("%H:%M:%S")
        })
        st.session_state.conversation_history.append({
            'role': 'user',
            'content': user_input
        })
        st.rerun()
    
    # أزرار التحكم
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    with btn_col1:
        if st.button("🗑️ مسح السبورة", use_container_width=True):
            if st.checkbox("تأكيد المسح", key="confirm_clear"):
                st.session_state.board_output = []
                st.session_state.conversation_history = []
                st.success("✅ تم مسح السبورة")
                st.rerun()
    
    with btn_col2:
        if st.button("💾 حفظ الجلسة", use_container_width=True):
            session_data = {
                'timestamp': datetime.now().isoformat(),
                'rules': st.session_state.rules,
                'conversation': st.session_state.conversation_history,
                'board': st.session_state.board_output
            }
            with open('session_backup.json', 'w', encoding='utf-8') as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)
            st.success("✅ تم حفظ الجلسة في session_backup.json")
    
    with btn_col3:
        if st.button("🔄 تحديث الحالة", use_container_width=True):
            update_connection_status()
            st.rerun()

# ═════════════════════════════════════════════════════════════════════════════
# ⚙️ العمود الجانبي: الإعدادات والقواعس
# ═════════════════════════════════════════════════════════════════════════════

with col_sidebar:
    st.markdown("### ⚙️ الإعدادات")
    
    # ─────────────────────────────────────────────────────────────────────────
    # قسم اتصال API
    # ─────────────────────────────────────────────────────────────────────────
    
    with st.expander("🔑 مفتاح API", expanded=False):
        st.session_state.api_key = st.text_input(
            "أدخل مفتاح Gemini API:",
            value=st.session_state.api_key,
            type="password",
            label_visibility="collapsed"
        )
        
        # اختيار الموديل
        st.session_state.model_choice = st.radio(
            "اختر الموديل:",
            ["Gemini", "GPT (مستقبلاً)"],
            horizontal=True,
            label_visibility="collapsed"
        )
        
        # درجة الحرارة
        st.session_state.temperature = st.slider(
            "درجة الحرارة (Temperature):",
            0.0, 1.0, 0.7, 0.1,
            label_visibility="collapsed"
        )
        
        # زر الاتصال
        if st.button("🔗 اختبار الاتصال", use_container_width=True, type="primary"):
            update_connection_status()
            
            if st.session_state.connection_status['api']:
                st.success("✅ متصل برنامج بنجاح!")
            else:
                st.error("❌ فشل الاتصال. تحقق من المفتاح.")
    
    # ─────────────────────────────────────────────────────────────────────────
    # حالة الاتصال
    # ─────────────────────────────────────────────────────────────────────────
    
    with st.expander("🟢 حالة الاتصال", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**API:**")
            if st.session_state.connection_status['api']:
                st.success("🟢 متصل")
            else:
                st.error("🔴 غير متصل")
        
        with col2:
            st.markdown("**البيانات:**")
            if st.session_state.connection_status['data_quran'] and st.session_state.connection_status['data_words']:
                st.success("🟢 محملة")
            else:
                st.warning("🔴 ناقصة")
        
        st.markdown("""
        <div class="alert-info">
        <small>ملاحظة: الموقع يعمل حتى لو لم تكن البيانات محملة</small>
        </div>
        """, unsafe_allow_html=True)
    
    # ─────────────────────────────────────────────────────────────────────────
    # إدارة القواعس §
    # ─────────────────────────────────────────────────────────────────────────
    
    with st.expander("📋 القواعس §", expanded=False):
        st.markdown("#### إضافة قاعدة جديدة")
        
        new_rule_name = st.text_input(
            "اسم القاعدة:",
            placeholder="مثال: قاعدة تعريف الأسماء",
            label_visibility="collapsed"
        )
        
        new_rule_description = st.text_area(
            "شرح القاعدة:",
            placeholder="أدخل شرح القاعدة بالتفصيل...",
            height=60,
            label_visibility="collapsed"
        )
        
        if st.button("➕ إضافة القاعدة", use_container_width=True):
            if new_rule_name:
                st.session_state.rules.append({
                    'id': len(st.session_state.rules) + 1,
                    'name': new_rule_name,
                    'description': new_rule_description,
                    'enabled': True,
                    'created_at': datetime.now().isoformat()
                })
                st.success(f"✅ تمت إضافة القاعدة: {new_rule_name}")
                st.rerun()
            else:
                st.error("❌ يجب إدخال اسم للقاعدة")
        
        # عرض القواعس الموجودة
        if st.session_state.rules:
            st.markdown("#### القواعس المفعلة")
            
            for idx, rule in enumerate(st.session_state.rules):
                with st.container(border=True):
                    col1, col2 = st.columns([4, 1])
                    
                    with col1:
                        st.markdown(f"**§ {rule['name']}**")
                        st.caption(rule['description'])
                    
                    with col2:
                        if st.button("🗑️", key=f"delete_rule_{idx}", help="حذف"):
                            st.session_state.rules.pop(idx)
                            st.rerun()
        else:
            st.info("لا توجد قواعس مفعلة حالياً", icon="ℹ️")
    
    # ─────────────────────────────────────────────────────────────────────────
    # إدارة الجلسة
    # ─────────────────────────────────────────────────────────────────────────
    
    with st.expander("💾 إدارة الجلسة", expanded=False):
        if st.button("📥 استيراد جلسة سابقة", use_container_width=True):
            st.info("سيتم إضافة هذه الميزة لاحقاً", icon="ℹ️")
        
        if st.button("📤 تصدير الجلسة الحالية", use_container_width=True):
            session_data = {
                'timestamp': datetime.now().isoformat(),
                'rules': st.session_state.rules,
                'conversation': st.session_state.conversation_history,
                'board': st.session_state.board_output
            }
            st.json(session_data)

# ═════════════════════════════════════════════════════════════════════════════
# 🔧 تنبيه الملفات الناقصة
# ═════════════════════════════════════════════════════════════════════════════

update_connection_status()

if not (st.session_state.connection_status['data_quran'] and st.session_state.connection_status['data_words']):
    st.warning(
        """
        ⚠️ **ملفات البيانات ناقصة:**
        
        يجب وضع الملفات التالية في مجلد `data/` بجانب الملف الرئيسي:
        - `data_quran.xlsx`
        - `data_words.xlsx`
        
        النظام يعمل بدون هذه الملفات، لكن محرك البحث لن يكون فعالاً.
        """,
        icon="⚠️"
    )

# ═════════════════════════════════════════════════════════════════════════════
# 📌 التذييل والمعلومات
# ═════════════════════════════════════════════════════════════════════════════

st.divider()

col_footer1, col_footer2, col_footer3 = st.columns(3)

with col_footer1:
    st.caption("📖 **مجلس البينة** | Council of Evidence")

with col_footer2:
    st.caption(f"🕐 الجلسة الحالية: {len(st.session_state.board_output)} رسالة")

with col_footer3:
    st.caption("🔒 جميع البيانات محفوظة محلياً")
