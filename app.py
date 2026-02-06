import streamlit as st
import pandas as pd
import numpy as np
import pickle
import re
import string
import os
import requests
import tensorflow as tf  
from datetime import datetime
import hashlib

# ---------------------------------------------------------
# 1. إعدادات الصفحة
# ---------------------------------------------------------
st.set_page_config(page_title="تحليل آراء الطلاب", layout="wide", page_icon="🎓")

# ---------------------------------------------------------
# 1.1 تصميم الواجهة (CSS)
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif !important;
        direction: rtl;
    }

    /* ───── خلفية عامة ───── */
    .stApp {
        background: linear-gradient(160deg, #f8fafc 0%, #eef2ff 40%, #f0fdf4 100%);
    }

    /* ───── Header (المستخدم) ───── */
    .app-header {
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 50%, #0369a1 100%);
        border-radius: 24px;
        padding: 44px 40px;
        color: white;
        margin-bottom: 28px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(14, 165, 233, 0.20);
    }
    .app-header::before {
        content: '';
        position: absolute;
        width: 240px; height: 240px;
        background: rgba(255,255,255,0.07);
        border-radius: 50%;
        top: -80px; left: -60px;
    }
    .app-header::after {
        content: '';
        position: absolute;
        width: 160px; height: 160px;
        background: rgba(255,255,255,0.05);
        border-radius: 50%;
        bottom: -50px; right: 40px;
    }
    .app-header h1 {
        font-size: 30px; font-weight: 800;
        margin: 0 0 8px 0;
        position: relative; z-index: 1;
        letter-spacing: -0.3px;
    }
    .app-header p {
        font-size: 15px; opacity: 0.92;
        margin: 0; font-weight: 300;
        position: relative; z-index: 1;
        line-height: 1.7;
    }
    .header-badge {
        display: inline-block;
        background: rgba(255,255,255,0.18);
        backdrop-filter: blur(6px);
        padding: 5px 16px;
        border-radius: 20px;
        font-size: 12px; font-weight: 500;
        margin-bottom: 14px;
        position: relative; z-index: 1;
        border: 1px solid rgba(255,255,255,0.12);
    }

    /* ───── بطاقات المزايا ───── */
    .info-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 22px 18px;
        text-align: center;
        transition: all 0.25s ease;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .info-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 28px rgba(14, 165, 233, 0.10);
        border-color: #bae6fd;
    }
    .info-card .ic-icon { font-size: 30px; margin-bottom: 10px; }
    .info-card .ic-label {
        font-size: 13px; color: #94a3b8; font-weight: 400;
        margin-bottom: 4px;
    }
    .info-card .ic-value {
        font-size: 17px; font-weight: 700; color: #1e293b;
    }

    /* ───── منطقة الشات ───── */
    .chat-label {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 20px 24px;
        margin-bottom: 18px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .chat-label .cl-title {
        font-size: 17px; font-weight: 700; color: #1e293b;
        margin: 0 0 4px 0;
    }
    .chat-label .cl-sub {
        font-size: 13px; color: #94a3b8; margin: 0;
    }

    /* ───── بطاقة النتيجة ───── */
    .result-box {
        border-radius: 16px;
        padding: 20px 24px;
        margin-top: 12px;
        display: flex; align-items: center; gap: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .result-positive {
        background: linear-gradient(135deg, #f0fdf4, #dcfce7);
        border: 1px solid #86efac;
    }
    .result-negative {
        background: linear-gradient(135deg, #fef2f2, #fee2e2);
        border: 1px solid #fca5a5;
    }
    .result-neutral {
        background: linear-gradient(135deg, #fffbeb, #fef3c7);
        border: 1px solid #fcd34d;
    }
    .result-box .rb-emoji { font-size: 38px; }
    .result-box .rb-text {
        font-size: 18px; font-weight: 700; color: #1e293b;
    }
    .result-box .rb-conf {
        font-size: 13px; color: #64748b; font-weight: 400;
    }

    /* ───── بطاقة تسجيل الدخول ───── */
    .login-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 24px;
        padding: 48px 40px;
        max-width: 420px;
        margin: 60px auto;
        box-shadow: 0 8px 32px rgba(0,0,0,0.06);
        text-align: center;
    }
    .login-card h2 {
        font-size: 24px; font-weight: 700; color: #1e293b;
        margin: 0 0 6px 0;
    }
    .login-card p {
        font-size: 14px; color: #94a3b8;
        margin: 0 0 24px 0;
    }
    .login-icon { font-size: 52px; margin-bottom: 16px; }

    /* ───── هيدر الأدمن ───── */
    .admin-header {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border-radius: 24px;
        padding: 36px 40px;
        color: white;
        margin-bottom: 28px;
        box-shadow: 0 10px 40px rgba(30, 41, 59, 0.18);
    }
    .admin-header h1 {
        font-size: 26px; font-weight: 800;
        margin: 0 0 6px 0;
    }
    .admin-header p {
        font-size: 14px; opacity: 0.7;
        margin: 0; font-weight: 300;
    }

    /* ───── بطاقات الإحصائيات (أدمن) ───── */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 24px 20px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        transition: all 0.2s ease;
    }
    .metric-card:hover {
        box-shadow: 0 6px 20px rgba(0,0,0,0.06);
    }
    .metric-card .mc-num {
        font-size: 34px; font-weight: 800;
    }
    .metric-card .mc-label {
        font-size: 13px; color: #94a3b8; margin-top: 6px;
    }
    .mc-blue   { color: #0ea5e9; }
    .mc-green  { color: #10b981; }
    .mc-red    { color: #f43f5e; }
    .mc-amber  { color: #f59e0b; }

    /* ───── الأزرار ───── */
    .stButton>button {
        background: linear-gradient(135deg, #0ea5e9, #0284c7) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px;
        padding: 10px 22px;
        font-weight: 600;
        font-family: 'Tajawal', sans-serif !important;
        transition: all 0.2s ease;
        box-shadow: 0 2px 8px rgba(14, 165, 233, 0.20);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #0284c7, #0369a1) !important;
        color: white !important;
        box-shadow: 0 4px 16px rgba(14, 165, 233, 0.30);
        transform: translateY(-1px);
    }

    .stDownloadButton>button {
        background: #ffffff !important;
        color: #0ea5e9 !important;
        border: 2px solid #0ea5e9 !important;
        border-radius: 12px;
        font-weight: 600;
        font-family: 'Tajawal', sans-serif !important;
        transition: all 0.2s ease;
    }
    .stDownloadButton>button:hover {
        background: #f0f9ff !important;
        color: #0284c7 !important;
        border-color: #0284c7 !important;
    }

    .stProgress>div>div>div>div {
        background: linear-gradient(90deg, #0ea5e9, #06b6d4);
        border-radius: 8px;
    }

    /* ───── السايدبار ───── */
    section[data-testid="stSidebar"] {
        background: #f8fafc;
        border-left: 1px solid #e2e8f0;
    }
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #1e293b;
    }

    /* ───── عناصر الإدخال ───── */
    div[data-testid="stChatMessage"] {
        border-radius: 16px !important;
        border: 1px solid #e2e8f0;
    }
    .stTextInput>div>div>input,
    .stTextArea textarea {
        border-radius: 12px !important;
        border: 1.5px solid #e2e8f0 !important;
        background: #fff !important;
        transition: all 0.2s ease;
    }
    .stTextInput>div>div>input:focus,
    .stTextArea textarea:focus {
        border-color: #0ea5e9 !important;
        box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.12) !important;
    }
    .stSelectbox>div>div {
        border-radius: 12px !important;
    }

    /* ───── الفواصل ───── */
    hr {
        border: none;
        height: 1px;
        background: #e2e8f0;
        margin: 24px 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# إعدادات الإدارة
# ---------------------------------------------------------
FILE_NAME = "collected_responses.xlsx"

# إعدادات تيليجرام (مخفية)
TELEGRAM_BOT_TOKEN = "8289972631:AAH8g7CIrYRqcYDBMp-gOBSn9DMGE-qiQxc"
TELEGRAM_CHAT_ID = "1566742277"  # ضع الآيدي الخاص بك هنا

ADMIN_CREDENTIALS = {
    "hisham": "a20a2b7bb0842d5cf8a0c06c626421fd51ec103925c1819a51271f2779afa730",  # password: '2005'
}

# تهيئة session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'page' not in st.session_state:
    st.session_state.page = "main"

# ---------------------------------------------------------
# 2. دوال المساعدة
# ---------------------------------------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username, password):
    if username in ADMIN_CREDENTIALS:
        return ADMIN_CREDENTIALS[username] == hash_password(password)
    return False

def send_file_to_telegram(bot_token, chat_id, file_path):
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
        with open(file_path, 'rb') as f:
            files = {'document': f}
            data = {'chat_id': chat_id, 'caption': '📊 هذا ملف الردود الجديد.'}
            response = requests.post(url, files=files, data=data)
            
        if response.status_code == 200:
            return True, "تم الإرسال بنجاح! 🚀"
        else:
            return False, f"فشل الإرسال. كود الخطأ: {response.status_code}"
    except Exception as e:
        return False, f"حدث خطأ تقني: {e}"

# ---------------------------------------------------------
# 3. تحميل المودل والتوكينايزر
# ---------------------------------------------------------
@st.cache_resource
def load_ai_assets():
    try:
        # --- التعديل هنا: استخدام tf.keras ---
        model = tf.keras.models.load_model('best_model.keras')
        
        with open('tokenizer.pickle', 'rb') as handle:
            tokenizer = pickle.load(handle)
        return model, tokenizer
    except Exception as e:
        st.error(f"حدث خطأ أثناء تحميل الملفات: {e}")
        return None, None

model, tokenizer = load_ai_assets()

# ---------------------------------------------------------
# 4. دوال التنظيف
# ---------------------------------------------------------
def clean_arabic_text(text):
    text = str(text)
    text = re.sub(r'[\u0617-\u061A\u064B-\u0652]', "", text)
    text = re.sub("[أإآ]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ة", "ه", text)
    text = re.sub(r'\d+', '', text)
    translator = str.maketrans('', '', string.punctuation + '،؛؟')
    text = text.translate(translator)
    return " ".join(text.split())

# ---------------------------------------------------------
# 5. صفحة تسجيل الدخول للإدارة
# ---------------------------------------------------------
def admin_login():
    st.markdown(
        """
        <div class="login-card">
            <div class="login-icon">🔐</div>
            <h2>لوحة الإدارة</h2>
            <p>سجّل دخولك للوصول إلى نتائج التحليل</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    with st.form("login_form"):
        col1, col2, col3 = st.columns([1, 1.5, 1])
        with col2:
            username = st.text_input("اسم المستخدم")
            password = st.text_input("كلمة المرور", type="password")
            login_button = st.form_submit_button("تسجيل الدخول", use_container_width=True)
    
    if login_button:
        if authenticate_user(username, password):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.page = "admin"
            st.rerun()
        else:
            st.error("اسم المستخدم أو كلمة المرور غير صحيحة")
    
    st.markdown("")
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        if st.button("العودة للصفحة الرئيسية", use_container_width=True):
            st.session_state.page = "main"
            st.rerun()

# ---------------------------------------------------------
# 6. صفحة الإدارة
# ---------------------------------------------------------
def admin_dashboard():
    st.markdown(
        f"""
        <div class="admin-header">
            <h1>لوحة تحكم الإدارة</h1>
            <p>مرحبا {st.session_state.username} — إليك ملخص نتائج تحليل المشاعر</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("تسجيل خروج", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.session_state.page = "main"
            st.rerun()
    
    # عرض الإحصائيات العامة
    if os.path.exists(FILE_NAME):
        df = pd.read_excel(FILE_NAME)
        
        positive_count = len(df[df['AI_Prediction'] == 'راضي 😃'])
        negative_count = len(df[df['AI_Prediction'] == 'غير راضي 😞'])
        neutral_count = len(df[df['AI_Prediction'] == 'محايد 😐'])
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f'<div class="metric-card"><div class="mc-num mc-blue">{len(df)}</div><div class="mc-label">إجمالي الردود</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card"><div class="mc-num mc-green">{positive_count}</div><div class="mc-label">ردود إيجابية</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="metric-card"><div class="mc-num mc-red">{negative_count}</div><div class="mc-label">ردود سلبية</div></div>', unsafe_allow_html=True)
        with col4:
            st.markdown(f'<div class="metric-card"><div class="mc-num mc-amber">{neutral_count}</div><div class="mc-label">ردود محايدة</div></div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # فلترة البيانات
        st.subheader("🔍 فلترة النتائج")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            date_filter_enabled = st.checkbox("تفعيل فلتر التاريخ")
            if date_filter_enabled:
                default_date = datetime.now().date()
                if not df.empty:
                    default_date = pd.to_datetime(df['Timestamp']).dt.date.min()
                date_filter = st.date_input("من تاريخ:", value=default_date)
            else:
                date_filter = None
        with col2:
            sentiment_filter = st.selectbox(
                "نوع المشاعر:",
                ["الكل", "راضي 😃", "محايد 😐", "غير راضي 😞"]
            )
        with col3:
            min_confidence = st.slider("الحد الأدنى للثقة:", 0.0, 100.0, 0.0)
        
        # تطبيق الفلاتر
        filtered_df = df.copy()
        
        if date_filter_enabled and date_filter:
            filtered_df['Date'] = pd.to_datetime(filtered_df['Timestamp']).dt.date
            filtered_df = filtered_df[filtered_df['Date'] >= date_filter]
        
        if sentiment_filter != "الكل":
            filtered_df = filtered_df[filtered_df['AI_Prediction'] == sentiment_filter]
        
        # فلتر الثقة
        filtered_df['Confidence_Numeric'] = pd.to_numeric(
            filtered_df['Confidence'].str.replace('%', ''),
            errors='coerce'
        ).fillna(0.0)
        filtered_df = filtered_df[filtered_df['Confidence_Numeric'] >= min_confidence]
        
        st.markdown("---")
        
        # عرض البيانات المفلترة
        st.subheader(f"📋 النتائج ({len(filtered_df)} من {len(df)})")
        
        if len(filtered_df) > 0:
            # رسم بياني للمشاعر
            sentiment_counts = filtered_df['AI_Prediction'].value_counts()
            
            col1, col2 = st.columns([2, 1])
            with col1:
                st.bar_chart(sentiment_counts)
            
            with col2:
                st.write("**توزيع المشاعر:**")
                for sentiment, count in sentiment_counts.items():
                    percentage = (count / len(filtered_df)) * 100
                    st.write(f"{sentiment}: {count} ({percentage:.1f}%)")
            
            # جدول البيانات
            st.markdown("---")
            st.subheader("📊 تفاصيل الردود")
            
            # إعادة ترتيب الأعمدة لعرض أفضل
            available_cols = filtered_df.columns.tolist()
            desired_cols = ['Timestamp', 'Student_Name', 'الجنس', 'المرحلة الدراسية', 'القسم العلمي',
                            'التقييم العام', 'تجربة التعليم الإلكتروني', 'التفضيل والراحة النفسية',
                            'الذكاء الاصطناعي والمستقبل', 'AI_Prediction', 'Confidence']
            # fallback للأعمدة القديمة
            show_cols = [c for c in desired_cols if c in available_cols]
            if not show_cols:
                show_cols = [c for c in ['Timestamp', 'Student_Name', 'Review', 'AI_Prediction', 'Confidence'] if c in available_cols]
            display_df = filtered_df[show_cols].copy()
            if 'Timestamp' in display_df.columns:
                display_df['Timestamp'] = pd.to_datetime(display_df['Timestamp']).dt.strftime('%Y-%m-%d %H:%M')
            
            st.dataframe(
                display_df,
                use_container_width=True,
                height=400
            )
            
            # تحميل البيانات المفلترة
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("📥 تحميل البيانات المفلترة", use_container_width=True):
                    csv_data = display_df.to_csv(index=False, encoding='utf-8-sig')
                    st.download_button(
                        label="💾 تحميل ملف CSV",
                        data=csv_data,
                        file_name=f"filtered_responses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
        else:
            st.warning("لا توجد بيانات تطابق الفلاتر المحددة.")
    else:
        st.info("لا توجد بيانات محفوظة بعد.")
    
    st.markdown("---")
    if st.button("🏠 العودة للصفحة الرئيسية", use_container_width=True):
        st.session_state.page = "main"
        st.rerun()

# ---------------------------------------------------------
# 7. واجهة المستخدم الرئيسية
# ---------------------------------------------------------
def main_interface():
    # ───── Header ─────
    st.markdown(
        """
        <div class="app-header">
            <div class="header-badge">🎓 تحليل مشاعر بالذكاء الاصطناعي</div>
            <h1>استبيان تحليل مشاعر الطلاب</h1>
            <p>أجب على الأسئلة التالية وسنحلل مشاعرك تلقائيا بعد الانتهاء</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ───── Feature pills ─────
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="info-card"><div class="ic-icon">⚡</div><div class="ic-label">سرعة التحليل</div><div class="ic-value">أقل من 3 ثوانٍ</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="info-card"><div class="ic-icon">🔒</div><div class="ic-label">الخصوصية</div><div class="ic-value">الاسم اختياري</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="info-card"><div class="ic-icon">🎯</div><div class="ic-label">الدقة</div><div class="ic-value">نسبة ثقة مئوية</div></div>', unsafe_allow_html=True)

    st.markdown("")

    # ───── قائمة الأسئلة من ملف الاكسل ─────
    SURVEY_QUESTIONS = [
        {
            "key": "q_university",
            "text": "ما اسم جامعتك؟",
            "type": "text",
            "column": "الجامعة"
        },
        {
            "key": "q_college",
            "text": "ما اسم كليتك؟",
            "type": "text",
            "column": "الكلية"
        },
        {
            "key": "q_gender",
            "text": "ما هو جنسك؟",
            "type": "text",
            "column": "الجنس"
        },
        {
            "key": "q_stage",
            "text": "ما هي مرحلتك الدراسية؟",
            "type": "text",
            "column": "المرحلة الدراسية"
        },
        {
            "key": "q_dept",
            "text": "ما هو قسمك العلمي؟",
            "type": "text",
            "column": "القسم العلمي"
        },
        {
            "key": "q_experience",
            "text": "حدثنا عن تجربتك مع التعليم الإلكتروني، ما هي أكثر الأشياء التي أعجبتك وأكثر المشاكل التي واجهتها؟",
            "type": "text",
            "column": "تجربة التعليم الإلكتروني"
        },
        {
            "key": "q_preference",
            "text": "هل تفضل التعليم الحضوري أم الإلكتروني؟ وهل شعرت بفرق في مستوى التوتر أو الراحة النفسية بينهما؟",
            "type": "text",
            "column": "التفضيل والراحة النفسية"
        },
        {
            "key": "q_ai",
            "text": "رأيك، هل ساعدك استخدام الذكاء الاصطناعي والتقنيات الحديثة في الفهم؟ وهل تنصح باستمرار التعليم الإلكتروني مستقبلاً؟",
            "type": "text",
            "column": "الذكاء الاصطناعي والمستقبل"
        },
    ]

    # ───── تهيئة session state ─────
    if "student_name" not in st.session_state:
        st.session_state.student_name = ""
    if "survey_step" not in st.session_state:
        st.session_state.survey_step = 0
    if "survey_answers" not in st.session_state:
        st.session_state.survey_answers = {}
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    if "survey_done" not in st.session_state:
        st.session_state.survey_done = False

    # ───── Chat label ─────
    st.markdown(
        """
        <div class="chat-label">
            <div class="cl-title">الاستبيان</div>
            <div class="cl-sub">أجب على الأسئلة بالترتيب — سيتم التحليل بعد آخر سؤال</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.session_state.student_name = st.text_input(
        "الاسم (اختياري)",
        value=st.session_state.student_name,
        placeholder="مثال: أحمد"
    )

    current_step = st.session_state.survey_step
    total_questions = len(SURVEY_QUESTIONS)

    # شريط التقدم
    if not st.session_state.survey_done:
        progress_pct = current_step / total_questions
        st.progress(progress_pct, text=f"السؤال {current_step} من {total_questions}")

    # عرض الرسائل السابقة
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # ───── عرض السؤال الحالي ─────
    if not st.session_state.survey_done and current_step < total_questions:
        q = SURVEY_QUESTIONS[current_step]

        # عرض السؤال كرسالة مساعد (إذا لم يُعرض بعد)
        question_msg = f"**سؤال {current_step + 1}/{total_questions}:** {q['text']}"
        already_shown = any(
            m["content"] == question_msg and m["role"] == "assistant"
            for m in st.session_state.chat_messages
        )
        if not already_shown:
            st.session_state.chat_messages.append({"role": "assistant", "content": question_msg})
            st.rerun()

        # سؤال نصي
        user_input = st.chat_input("اكتب إجابتك هنا...")
        if user_input:
                st.session_state.survey_answers[q["key"]] = user_input
                st.session_state.chat_messages.append({"role": "user", "content": user_input})
                st.session_state.survey_step += 1

                # إذا كان آخر سؤال → حلل
                if st.session_state.survey_step >= total_questions:
                    st.session_state.survey_done = True

                st.rerun()

    # ───── التحليل بعد اكتمال الأسئلة ─────
    if st.session_state.survey_done and model is not None and tokenizer is not None:
        answers = st.session_state.survey_answers

        # تحليل كل إجابة نصية جوهرية على حدة ثم أخذ المعدل
        analysis_keys = ["q_experience", "q_preference", "q_ai"]
        all_predictions = []

        for akey in analysis_keys:
            if akey in answers and answers[akey].strip():
                cleaned = clean_arabic_text(answers[akey])
                seq = tokenizer.texts_to_sequences([cleaned])
                padded = tf.keras.preprocessing.sequence.pad_sequences(seq, maxlen=100)
                pred = model.predict(padded, verbose=0)
                all_predictions.append(pred[0])

        if all_predictions:
            avg_prediction = np.mean(all_predictions, axis=0)
        else:
            avg_prediction = np.array([0.33, 0.34, 0.33])

        class_idx = np.argmax(avg_prediction)

        labels = {0: 'غير راضي 😞', 1: 'محايد 😐', 2: 'راضي 😃'}
        result_text = labels[class_idx]
        confidence = np.max(avg_prediction) * 100

        # Result banner
        if class_idx == 2:
            css_class = "result-positive"
        elif class_idx == 0:
            css_class = "result-negative"
        else:
            css_class = "result-neutral"

        emoji_map = {0: '😞', 1: '😐', 2: '😃'}
        label_map = {0: 'غير راضي', 1: 'محايد', 2: 'راضي'}

        result_msg = f"نتيجة التحليل: {result_text} — الثقة: {confidence:.1f}%"
        already_result = any(m["content"] == result_msg for m in st.session_state.chat_messages)
        if not already_result:
            st.session_state.chat_messages.append({"role": "assistant", "content": result_msg})

        with st.chat_message("assistant"):
            st.markdown(
                f"""
                <div class="result-box {css_class}">
                    <div class="rb-emoji">{emoji_map[class_idx]}</div>
                    <div>
                        <div class="rb-text">{label_map[class_idx]}</div>
                        <div class="rb-conf">نسبة الثقة: {confidence:.1f}%</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        st.progress(int(confidence))

        # الحفظ (مرة واحدة فقط)
        if "saved" not in st.session_state:
            result_data = {
                'Timestamp': pd.Timestamp.now(),
                'Student_Name': st.session_state.student_name,
                'الجامعة': answers.get("q_university", ""),
                'الكلية': answers.get("q_college", ""),
                'الجنس': answers.get("q_gender", ""),
                'المرحلة الدراسية': answers.get("q_stage", ""),
                'القسم العلمي': answers.get("q_dept", ""),
                'تجربة التعليم الإلكتروني': answers.get("q_experience", ""),
                'التفضيل والراحة النفسية': answers.get("q_preference", ""),
                'الذكاء الاصطناعي والمستقبل': answers.get("q_ai", ""),
                'AI_Prediction': result_text,
                'Confidence': f"{confidence:.2f}%"
            }

            df_new = pd.DataFrame([result_data])

            if not os.path.exists(FILE_NAME):
                df_new.to_excel(FILE_NAME, index=False, engine='openpyxl')
            else:
                existing_df = pd.read_excel(FILE_NAME)
                combined_df = pd.concat([existing_df, df_new], ignore_index=True)
                combined_df.to_excel(FILE_NAME, index=False, engine='openpyxl')

            # إرسال تلقائي صامت للتيليجرام
            try:
                send_file_to_telegram(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, FILE_NAME)
            except Exception:
                pass

            st.session_state.saved = True
            st.toast("تم الحفظ بنجاح", icon="✅")

        # زر إعادة الاستبيان
        st.markdown("")
        if st.button("🔄 إعادة الاستبيان", use_container_width=True):
            for key in ["survey_step", "survey_answers", "chat_messages", "survey_done", "saved"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

# ---------------------------------------------------------
# 8. التحكم في الصفحات
# ---------------------------------------------------------
# معالجة التنقل بين الصفحات
if st.session_state.page == "login":
    admin_login()
elif st.session_state.page == "admin" and st.session_state.authenticated:
    admin_dashboard()
else:
    st.session_state.page = "main"
    main_interface()
    
    with st.sidebar:
        st.markdown("### الإعدادات")
        st.markdown("")

        if st.button("لوحة الإدارة", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()