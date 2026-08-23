import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="ESC 2024 CCS Initial Management Tool v14",
    page_icon="🫀",
    layout="wide"
)

# MENU ĐIỀU HƯỚNG
st.sidebar.page_link(
    "pe-cdss-web.py",
    label="🫁 Thuyên tắc phổi cấp"
)

st.sidebar.page_link(
    "pages/1_❤️_Hoi_chung_vanh_man.py",
    label="❤️ Hội chứng vành mạn"
)

# Custom CSS Styling to implement Strict Visual Hierarchy and Gorgeous Accordion Flow
st.markdown("""
<style>
    .reportview-container {
        background: #f8fafc;
    }
    
    /* =========================================================
       VISUAL HIERARCHY
       H0 (page title) > H1 (Bước 1-4) > H2 (đề mục cấp 2)
       > H3 (st.subheader) > H4 > body text.
       Chỉ thay đổi hiển thị, không thay đổi nội dung/logic.
       ========================================================= */

    /* H0 — Main page title: dominant, PE-like presentation */
    h1.main-title,
    div[data-testid="stMarkdownContainer"] h1.main-title,
    h1.main-title span,
    h1.main-title * {
        font-size: 2.45rem !important;
        color: #24458f !important;
        text-align: center !important;
        font-weight: 900 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.15px !important;
        line-height: 1.02 !important;
        margin: 0 0 1px 0 !important;
        padding: 0 !important;
        display: block !important;
        width: 100% !important;
        background: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        text-shadow: none !important;
        white-space: nowrap !important;
    }

    .main-subtitle,
    .main-subtitle * {
        text-align: center !important;
        color: #475569 !important;
        font-size: 1.02rem !important;
        font-weight: 600 !important;
        line-height: 1.06 !important;
        margin: 0 0 4px 0 !important;
        letter-spacing: 0 !important;
    }

    /* Header separator: visually separates the page identity from the clinical workflow */
    .header-divider {
        width: 100% !important;
        height: 1px !important;
        background: #d5dee8 !important;
        border: 0 !important;
        margin: 12px 0 20px 0 !important;
        padding: 0 !important;
    }

    /* Native markdown heading hierarchy below the 4 main Step headings */
    h1:not(.main-title) {
        font-size: 1.45rem !important;
        color: #153b5b !important;
        font-weight: 850 !important;
        line-height: 1.06 !important;
        margin-top: 5px !important;
        margin-bottom: 3px !important;
    }
    h2 {
        font-size: 1.25rem !important;
        color: #1a5276 !important;
        font-weight: 820 !important;
        line-height: 1.08 !important;
        margin-top: 5px !important;
        margin-bottom: 3px !important;
    }
    h3 {
        font-size: 1.12rem !important;
        color: #256b93 !important;
        font-weight: 800 !important;
        border-bottom: 2px solid #7ccfb0 !important;
        padding-bottom: 3px !important;
        line-height: 1.08 !important;
        margin-top: 5px !important;
        margin-bottom: 3px !important;
    }
    h4 {
        font-size: 1.03rem !important;
        color: #2c3e50 !important;
        font-weight: 720 !important;
        line-height: 1.10 !important;
        margin-top: 4px !important;
        margin-bottom: 2px !important;
    }

    /* Do not style every span globally: Streamlit places heading/button text in spans. */
    div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stMarkdownContainer"] li,
    label {
        font-size: 1.03rem !important;
    }

    /* Streamlit itself inserts vertical gaps between element blocks.
       Reduce that gap, not just CSS margins on the visible headings. */
    section.main div[data-testid="stVerticalBlock"] {
        gap: 0.35rem !important;
    }

    @media (max-width: 1200px) {
        h1.main-title,
        div[data-testid="stMarkdownContainer"] h1.main-title,
        h1.main-title span,
        h1.main-title * {
            font-size: 2.30rem !important;
            line-height: 1.02 !important;
        }
    }
    @media (max-width: 768px) {
        h1.main-title,
        div[data-testid="stMarkdownContainer"] h1.main-title,
        h1.main-title span,
        h1.main-title * {
            font-size: 1.95rem !important;
            line-height: 1.04 !important;
            white-space: normal !important;
        }
        .main-subtitle, .main-subtitle * {
            font-size: 0.94rem !important;
            margin-bottom: 3px !important;
        }
        h1:not(.main-title) { font-size: 1.30rem !important; }
        h2 { font-size: 1.16rem !important; }
        h3 { font-size: 0.98rem !important; }
        h4 { font-size: 0.98rem !important; }
    }

    /* Step-based Alert Box styles */
    .recommendation-box {
        background-color: #e8f4f8;
        border-left: 6px solid #1e3d59;
        padding: 15px;
        border-radius: 4px;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #fff5f5;
        border-left: 6px solid #ff4d4d;
        padding: 15px;
        border-radius: 4px;
        margin: 10px 0;
    }
    .success-box {
        background-color: #e8f8f5;
        border-left: 6px solid #2ecc71;
        padding: 15px;
        border-radius: 4px;
        margin: 10px 0;
    }
    .info-box {
        background-color: #f7f9fa;
        border: 1px solid #d3d3d3;
        padding: 12px;
        border-radius: 4px;
        margin: 10px 0;
    }
    .symptom-tag-inc {
        background-color: #fce4d6;
        color: #c55a11;
        padding: 2px 6px;
        border-radius: 3px;
        font-weight: bold;
        font-size: 0.95rem;
    }
    .symptom-tag-dec {
        background-color: #e2efda;
        color: #375623;
        padding: 2px 6px;
        border-radius: 3px;
        font-weight: bold;
        font-size: 0.95rem;
    }
    .class-badge-1 {
        background-color: #2e7d32;
        color: white;
        padding: 2px 6px;
        border-radius: 3px;
        font-weight: bold;
        font-size: 0.85rem;
    }
    .class-badge-2a {
        background-color: #e67e22;
        color: white;
        padding: 2px 6px;
        border-radius: 3px;
        font-weight: bold;
        font-size: 0.85rem;
    }
    .class-badge-2b {
        background-color: #f1c40f;
        color: black;
        padding: 2px 6px;
        border-radius: 3px;
        font-weight: bold;
        font-size: 0.85rem;
    }
    .class-badge-3 {
        background-color: #c0392b;
        color: white;
        padding: 2px 6px;
        border-radius: 3px;
        font-weight: bold;
        font-size: 0.85rem;
    }

    /* Accordion Main Step Buttons styling - styled on button and button p/span to beat default Streamlit styles */
    div.main-step-active button, div.main-step-active [data-testid="stBaseButton-secondary"] {
        background: linear-gradient(135deg, #1e3d59, #17b978) !important;
        border: 2px solid #17b978 !important;
        box-shadow: 0 4px 15px rgba(23, 185, 120, 0.4) !important;
        width: 100% !important;
        text-align: left !important;
        padding: 6px 12px !important;
        border-radius: 8px !important;
        margin-top: 1px !important;
        margin-bottom: 1px !important;
        display: block !important;
    }
    div.main-step-active button p, div.main-step-active [data-testid="stBaseButton-secondary"] p,
    div.main-step-active button span, div.main-step-active [data-testid="stBaseButton-secondary"] span {
        font-size: 1.42rem !important;
        font-weight: 900 !important;
        color: #ffffff !important;
        text-transform: uppercase !important;
        margin: 0 !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3) !important;
    }
    
    div.main-step-completed button, div.main-step-completed [data-testid="stBaseButton-secondary"] {
        background: linear-gradient(135deg, #e8f8f5, #d1f2eb) !important;
        border: 2px solid #2ecc71 !important;
        width: 100% !important;
        text-align: left !important;
        padding: 6px 12px !important;
        border-radius: 8px !important;
        margin-top: 1px !important;
        margin-bottom: 1px !important;
        opacity: 0.95 !important;
        display: block !important;
    }
    div.main-step-completed button p, div.main-step-completed [data-testid="stBaseButton-secondary"] p,
    div.main-step-completed button span, div.main-step-completed [data-testid="stBaseButton-secondary"] span {
        font-size: 1.42rem !important;
        font-weight: 800 !important;
        color: #117a65 !important;
        margin: 0 !important;
    }
    
    div.main-step-pending button, div.main-step-pending [data-testid="stBaseButton-secondary"] {
        background-color: #f1f2f6 !important;
        border: 1px dashed #bdc3c7 !important;
        width: 100% !important;
        text-align: left !important;
        padding: 6px 12px !important;
        border-radius: 8px !important;
        margin-top: 1px !important;
        margin-bottom: 1px !important;
        opacity: 0.7 !important;
        display: block !important;
    }
    div.main-step-pending button p, div.main-step-pending [data-testid="stBaseButton-secondary"] p,
    div.main-step-pending button span, div.main-step-pending [data-testid="stBaseButton-secondary"] span {
        font-size: 1.42rem !important;
        font-weight: 700 !important;
        color: #7f8c8d !important;
        margin: 0 !important;
    }

    /* Sub-section Accordion Buttons styling */
    div.sub-header-active button, div.sub-header-active [data-testid="stBaseButton-secondary"] {
        background-color: #ebf5fb !important;
        border-left: 8px solid #3498db !important;
        border-top: none !important;
        border-right: none !important;
        border-bottom: none !important;
        width: 100% !important;
        text-align: left !important;
        padding: 4px 8px !important;
        border-radius: 4px !important;
        margin-top: 1px !important;
        margin-bottom: 1px !important;
        display: block !important;
    }
    div.sub-header-active button p, div.sub-header-active [data-testid="stBaseButton-secondary"] p,
    div.sub-header-active button span, div.sub-header-active [data-testid="stBaseButton-secondary"] span {
        font-size: 1.10rem !important;
        font-weight: 800 !important;
        color: #1b4f72 !important;
        margin: 0 !important;
    }
    
    div.sub-header-inactive button, div.sub-header-inactive [data-testid="stBaseButton-secondary"] {
        background-color: #fcfcfc !important;
        border: 1px solid #d5dbdb !important;
        width: 100% !important;
        text-align: left !important;
        padding: 4px 8px !important;
        border-radius: 4px !important;
        margin-top: 0px !important;
        margin-bottom: 0px !important;
        opacity: 0.85 !important;
        display: block !important;
    }
    div.sub-header-inactive button p, div.sub-header-inactive [data-testid="stBaseButton-secondary"] p,
    div.sub-header-inactive button span, div.sub-header-inactive [data-testid="stBaseButton-secondary"] span {
        font-size: 1.03rem !important;
        font-weight: 600 !important;
        color: #5d6d7e !important;
        margin: 0 !important;
    }
    div.sub-header-inactive button:hover {
        border-color: #17b978 !important;
        color: #17b978 !important;
        opacity: 1.0 !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🫀 TIẾP CẬN BAN ĐẦU HỘI CHỨNG MẠCH VÀNH MẠN (CCS)</h1>", unsafe_allow_html=True)
st.markdown("<div class='main-subtitle'>Hệ thống Hỗ trợ Quyết định Lâm sàng (CDSS) tương tác đa tầng theo Hướng dẫn ESC 2024</div>", unsafe_allow_html=True)
st.markdown("<div class='header-divider'></div>", unsafe_allow_html=True)

# Session State Initialization
if 'step' not in st.session_state: st.session_state.step = 1
if 'step1_sub' not in st.session_state: st.session_state.step1_sub = 1
if 'step2_sub' not in st.session_state: st.session_state.step2_sub = 1
if 'step3_sub' not in st.session_state: st.session_state.step3_sub = 1
if 'step4_sub' not in st.session_state: st.session_state.step4_sub = 1

if 'acute_flag' not in st.session_state: st.session_state.acute_flag = False
if 'lipid_unit' not in st.session_state: st.session_state.lipid_unit = "mmol/L"

# Cross-step persistent variables
if 'hr_val' not in st.session_state: st.session_state.hr_val = 75
if 'sbp_val' not in st.session_state: st.session_state.sbp_val = 120
if 'ldlc_val_mmol' not in st.session_state: st.session_state.ldlc_val_mmol = 3.0
if 'tg_val_mmol' not in st.session_state: st.session_state.tg_val_mmol = 1.8
if 'egfr_val' not in st.session_state: st.session_state.egfr_val = 90
if 'ecg_abnormal' not in st.session_state: st.session_state.ecg_abnormal = False
if 'cxr_abnormal' not in st.session_state: st.session_state.cxr_abnormal = False
if 'pft_abnormal' not in st.session_state: st.session_state.pft_abnormal = False
if 'diabetes_flag' not in st.session_state: st.session_state.diabetes_flag = False
if 'dyslipidemia_flag' not in st.session_state: st.session_state.dyslipidemia_flag = False
if 'hypertension_flag' not in st.session_state: st.session_state.hypertension_flag = False
if 'hb_val' not in st.session_state: st.session_state.hb_val = 13.0
if 'thyroid_assessed' not in st.session_state: st.session_state.thyroid_assessed = False
if 'likelihood_category' not in st.session_state: st.session_state.likelihood_category = None

# Global ACS Emergency Banner
if st.session_state.acute_flag:
    st.markdown("""
    <div class='warning-box'>
        <h3 style='color: #ff4d4d; margin-top: 0;'>🔴 CẢNH BÁO KHẨN CẤP: NGHI NGỜ HỘI CHỨNG MẠCH VÀNH CẤP (ACS)!</h3>
        <p style='font-size: 1.1rem;'>Bệnh nhân có triệu chứng đau ngực không ổn định, biến đổi ECG cấp tính hoặc huyết động không ổn định. 
        <strong>Khuyến cáo chuyển ngay bệnh nhân đến Khoa Cấp cứu (Emergency Department)</strong> để làm Troponin nhạy cảm cao (hs-cTn) và xử trí khẩn cấp theo phác đồ ACS. Quy trình chẩn đoán mạch vành mạn bị tạm dừng.</p>
    </div>
    """, unsafe_allow_html=True)

# Helper function to switch steps safely
def set_step(step_num):
    st.session_state.step = step_num
    st.rerun()

# Helper function to render accordion step headers
def render_main_step_header(title, step_id):
    current_step = st.session_state.step
    is_active = (current_step == step_id)
    is_completed = (current_step > step_id)
    
    arrow = "▼" if is_active else "▶"
    prefix = "✅ " if is_completed else ""
    status_text = " [ĐANG THỰC HIỆN]" if is_active else ""
    
    wrapper_class = "main-step-active" if is_active else ("main-step-completed" if is_completed else "main-step-pending")

    # Robust key-based styling for the four primary headings (Bước 1-4).
    # All four keep the SAME heading size; state is communicated by colour, not hierarchy.
    if is_active:
        step_bg = "linear-gradient(135deg, #123a5a 0%, #176b78 52%, #17b978 100%)"
        step_border = "#17b978"
        step_text = "#ffffff"
        step_shadow = "0 8px 22px rgba(23, 107, 120, 0.30)"
    elif is_completed:
        step_bg = "linear-gradient(135deg, #e7f8f1 0%, #d2f1e5 100%)"
        step_border = "#2ecc71"
        step_text = "#0d684f"
        step_shadow = "0 5px 14px rgba(46, 204, 113, 0.16)"
    else:
        step_bg = "linear-gradient(135deg, #eef5fb 0%, #e7f1f8 100%)"
        step_border = "#79a9c7"
        step_text = "#183f5f"
        step_shadow = "0 4px 12px rgba(30, 61, 89, 0.10)"

    st.markdown(f"""
    <style>
    div[class*="st-key-main_step_btn_{step_id}"] button {{
        width: 100% !important;
        background: {step_bg} !important;
        border: 2px solid {step_border} !important;
        border-left-width: 7px !important;
        border-radius: 9px !important;
        padding: 6px 12px !important;
        margin: 0 !important;
        min-height: 42px !important;
        box-shadow: {step_shadow} !important;
        justify-content: flex-start !important;
        text-align: left !important;
    }}
    div[class*="st-key-main_step_btn_{step_id}"] button p,
    div[class*="st-key-main_step_btn_{step_id}"] button span {{
        font-size: 1.42rem !important;
        line-height: 1.04 !important;
        font-weight: 900 !important;
        color: {step_text} !important;
        letter-spacing: 0.25px !important;
        margin: 0 !important;
    }}
    @media (max-width: 1200px) {{
        div[class*="st-key-main_step_btn_{step_id}"] button p,
        div[class*="st-key-main_step_btn_{step_id}"] button span {{ font-size: 1.34rem !important; }}
    }}
    @media (max-width: 768px) {{
        div[class*="st-key-main_step_btn_{step_id}"] button {{ padding: 5px 9px !important; min-height: 38px !important; }}
        div[class*="st-key-main_step_btn_{step_id}"] button p,
        div[class*="st-key-main_step_btn_{step_id}"] button span {{ font-size: 1.18rem !important; }}
    }}
    </style>
    """, unsafe_allow_html=True)
    
    if st.button(f"{arrow} {prefix}{title}{status_text}", key=f"main_step_btn_{step_id}"):
        # Toggle accordion: click the open heading to close it; click another to open it.
        st.session_state.step = 0 if is_active else step_id
        st.rerun()
    
    return is_active

# Helper function to render sub-step accordion headers
def render_sub_header(title, sub_step_id, session_key):
    current_sub = st.session_state.get(session_key, 1)
    is_active = (current_sub == sub_step_id)
    arrow = "▼" if is_active else "▶"
    
    wrapper_class = "sub-header-active" if is_active else "sub-header-inactive"

    # Secondary accordion headings: visibly below Bước 1-4 in the hierarchy.
    sub_bg = "#eaf4fb" if is_active else "#fbfdff"
    sub_border = "#3498db" if is_active else "#c7d8e5"
    sub_text = "#174d70" if is_active else "#4d6475"
    sub_weight = 820 if is_active else 680
    sub_size = "1.10rem" if is_active else "1.02rem"

    widget_key = f"btn_{session_key}_{sub_step_id}"
    st.markdown(f"""
    <style>
    div[class*="st-key-{widget_key}"] button {{
        width: 100% !important;
        background: {sub_bg} !important;
        border: 1px solid {sub_border} !important;
        border-left: 6px solid {sub_border} !important;
        border-radius: 6px !important;
        padding: 4px 8px !important;
        margin: 4px 0 !important;
        justify-content: flex-start !important;
        text-align: left !important;
        box-shadow: {'0 3px 10px rgba(52, 152, 219, 0.10)' if is_active else 'none'} !important;
    }}
    div[class*="st-key-{widget_key}"] button p,
    div[class*="st-key-{widget_key}"] button span {{
        font-size: {sub_size} !important;
        line-height: 1.10 !important;
        font-weight: {sub_weight} !important;
        color: {sub_text} !important;
        margin: 0 !important;
    }}
    @media (max-width: 768px) {{
        div[class*="st-key-{widget_key}"] button p,
        div[class*="st-key-{widget_key}"] button span {{ font-size: 0.98rem !important; }}
    }}
    </style>
    """, unsafe_allow_html=True)
    
    if st.button(f"{arrow} {title}", key=widget_key):
        # Toggle accordion: active sub-heading can be collapsed; opening another closes the previous one.
        st.session_state[session_key] = 0 if is_active else sub_step_id
        st.rerun()
    
    return is_active


# ====================================================
# BƯỚC 1: ĐÁNH GIÁ BAN ĐẦU
# ====================================================
if render_main_step_header("BƯỚC 1: ĐÁNH GIÁ BAN ĐẦU", 1):
    
    # Sub-step 1.1: Triệu chứng cảnh báo
    if render_sub_header("Triệu chứng cảnh báo", 1, "step1_sub"):
        st.subheader("1. Đánh giá dấu hiệu nguy kịch loại trừ ACS")
        
        col1, col2 = st.columns(2)
        with col1:
            acute_symptoms = st.checkbox(
                "Đau thắt ngực mới xuất hiện, tăng dần tần suất hoặc cường độ (Crescendo angina)",
                value=st.session_state.get('acute_s_val', False),
                key='acute_s_val'
            )
            unstable_symptoms = st.checkbox(
                "Triệu chứng huyết động không ổn định (đau ngực khi nghỉ, suy tim cấp, rối loạn nhịp mới)",
                value=st.session_state.get('unstable_s_val', False),
                key='unstable_s_val'
            )
        with col2:
            resting_ecg_acute = st.checkbox(
                "ECG lúc nghỉ biến đổi động học cấp tính (ST chênh lên/chênh xuống, sóng T âm sâu đối xứng)",
                value=st.session_state.get('resting_ecg_acute_val', False),
                key='resting_ecg_acute_val'
            )
            
        # Immediately adjust global ACS flag
        if acute_symptoms or unstable_symptoms or resting_ecg_acute:
            if not st.session_state.acute_flag:
                st.session_state.acute_flag = True
                st.rerun()
        else:
            if st.session_state.acute_flag:
                st.session_state.acute_flag = False
                st.rerun()
                
        if not st.session_state.acute_flag:
            st.success("✅ Chưa phát hiện dấu hiệu nguy kịch. Triệu chứng cơ bản ổn định, cho phép tiếp tục quy trình đánh giá mạch vành mạn.")

    # Sub-step 1.2: Triệu chứng lâm sàng
    if render_sub_header("Triệu chứng lâm sàng", 2, "step1_sub"):
        st.subheader("2. Khảo sát đặc điểm cơn đau ngực hoặc khó thở")
        
        symptom_presentation = st.radio(
            "Lựa chọn biểu hiện lâm sàng chủ đạo của bệnh nhân:", 
            ["Đau/Khó chịu vùng ngực", "Khó thở khi gắng sức"]
        )
        
        symptom_analysis = {"type": symptom_presentation, "auto_winther_score": 0, "summary_text": ""}
        
        if symptom_presentation == "Đau/Khó chịu vùng ngực":
            st.write("**Đánh giá tính chất đau ngực:**")
            col_ang1, col_ang2 = st.columns(2)
            with col_ang1:
                st.markdown("<span class='symptom-tag-inc'>Tăng khả năng lâm sàng</span>", unsafe_allow_html=True)
                inc_q = st.checkbox("Tính chất: Đau bóp nghẹt, thắt, siết chặt hoặc đè nặng vùng trước tim")
                inc_l = st.checkbox("Vị trí: Sau xương ức, lan ra cánh tay trái, cổ, hàm, vai, kích thước nắm tay")
                inc_d = st.checkbox("Thời gian: Cơn đau kéo dài ngắn, thông thường khoảng 5-10 phút")
                inc_tr = st.checkbox("Yếu tố kích gợi: Xuất hiện rõ rệt khi gắng sức thể lực, xúc cảm lạnh hoặc sau ăn")
                inc_re = st.checkbox("Yếu tố giảm đau: Giảm trong 1-5 phút khi ngừng gắng sức hoặc đáp ứng nhanh với Nitrates")
            with col_ang2:
                st.markdown("<span class='symptom-tag-dec'>Giảm khả năng lâm sàng</span>", unsafe_allow_html=True)
                dec_q = st.checkbox("Tính chất: Đau rát bỏng, nhói nhọn như dao đâm, hoặc đau âm ỉ liên tục")
                dec_l = st.checkbox("Vị trí: Đau khu trú tại một điểm rất nhỏ hoặc lệch hoàn toàn sang ngực phải")
                dec_d = st.checkbox("Thời gian: Đau thoáng qua vài giây hoặc đau liên tục nhiều ngày")
                dec_tr = st.checkbox("Yếu tố kích gợi: Đau tăng khi hít sâu, ho, thay đổi tư thế hoặc ấn chẩn thành ngực")
                dec_re = st.checkbox("Yếu tố giảm: Giảm sau khi uống thuốc dạ dày, uống nước hoặc nghỉ ngơi rất chậm")
                
            # Winther score logic:
            winther_1 = int(inc_l)
            winther_2 = int(inc_tr)
            winther_3 = int(inc_re)
            symptom_analysis["auto_winther_score"] = winther_1 + winther_2 + winther_3
            
            inc_count = sum([inc_q, inc_l, inc_d, inc_tr, inc_re])
            dec_count = sum([dec_q, dec_l, dec_d, dec_tr, dec_re])
            if inc_count > dec_count:
                symptom_analysis["summary_text"] = "👉 Triệu chứng đau ngực có các đặc điểm làm tăng khả năng thiếu máu cơ tim do bệnh mạch vành. ESC 2024 ưu tiên mô tả chi tiết đặc điểm triệu chứng thay vì dùng nhãn “điển hình/không điển hình”."
            else:
                symptom_analysis["summary_text"] = "👉 Triệu chứng đau ngực có đặc tính gợi ý giảm khả năng do tim (Nghi ngờ đau ngực không do tim)."
                
        else: # Exertional dyspnoea
            st.write("**Đánh giá tính chất khó thở:**")
            col_dys1, col_dys2 = st.columns(2)
            with col_dys1:
                st.markdown("<span class='symptom-tag-inc'>Tăng khả năng lâm sàng</span>", unsafe_allow_html=True)
                inc_dys_q = st.checkbox("Tính chất: Cảm giác hụt hơi, không thở sâu được khi gắng sức")
                inc_dys_tr = st.checkbox("Yếu tố kích gợi: Chỉ xuất hiện rõ khi tăng cường hoạt động thể lực")
                inc_dys_re = st.checkbox("Yếu tố giảm: Triệu chứng hết nhanh chóng ngay sau khi dừng gắng sức")
            with col_dys2:
                st.markdown("<span class='symptom-tag-dec'>Giảm khả năng lâm sàng</span>", unsafe_allow_html=True)
                dec_dys_q = st.checkbox("Tính chất: Khó thở ra, thở khò khè, rít phế quản hoặc kèm ho đờm")
                dec_dys_tr = st.checkbox("Yếu tố kích gợi: Đột ngột xuất hiện lúc nghỉ ngơi, liên quan đến bụi/mùi")
                dec_dys_re = st.checkbox("Yếu tố giảm: Giảm rất chậm khi nghỉ, chỉ đỡ sau dùng giãn phế quản")
                
            symptom_analysis["auto_winther_score"] = 2  # Default to 2 in Winther model for Dyspnoea
            
            inc_dys_count = sum([inc_dys_q, inc_dys_tr, inc_dys_re])
            dec_dys_count = sum([dec_dys_q, dec_dys_tr, dec_dys_re])
            if inc_dys_count > dec_dys_count:
                symptom_analysis["summary_text"] = "👉 Triệu chứng khó thở gắng sức gợi ý tăng khả năng do thiếu máu cơ tim tương đương đau ngực."
            else:
                symptom_analysis["summary_text"] = "👉 Triệu chứng khó thở gợi ý căn nguyên ngoài tim (hô hấp, tâm lý...)."

        st.info(symptom_analysis["summary_text"])
        st.session_state.symptom_analysis = symptom_analysis

    # Sub-step 1.3: Cận lâm sàng ban đầu
    if render_sub_header("Cận lâm sàng ban đầu", 3, "step1_sub"):
        st.subheader("3. Nhập kết quả xét nghiệm và thăm dò cơ bản")
        
        test_col1, test_col2 = st.columns(2)
        with test_col1:
            st.write("**Xét nghiệm bắt buộc thường quy:**")
            done_ecg = st.checkbox("Điện tâm đồ 12 chuyển đạo lúc nghỉ", value=True)
            if done_ecg:
                ecg_res = st.radio(
                    "Kết quả ECG lúc nghỉ:",
                    ["Bình thường", "Bất thường (Sóng Q bệnh lý, ST-T thay đổi động học, LBBB...)"]
                )
                st.session_state.ecg_abnormal = (ecg_res != "Bình thường")
                
            done_biochem = st.checkbox("Xét nghiệm máu cơ bản theo ESC 2024")
            if done_biochem:
                st.session_state.lipid_unit = st.radio("Đơn vị đo lipid máu:", ["mmol/L", "mg/dL"], horizontal=True)
                bio_col1, bio_col2 = st.columns(2)
                with bio_col1:
                    if st.session_state.lipid_unit == "mmol/L":
                        ldlc = st.number_input("LDL-Cholesterol:", min_value=0.1, max_value=15.0, value=st.session_state.ldlc_val_mmol, step=0.1)
                        st.session_state.ldlc_val_mmol = ldlc
                        tg = st.number_input("Triglycerides:", min_value=0.1, max_value=30.0, value=st.session_state.tg_val_mmol, step=0.1)
                        st.session_state.tg_val_mmol = tg
                    else:
                        ldlc_mg = st.number_input("LDL-Cholesterol (mg/dL):", min_value=4.0, max_value=600.0, value=float(st.session_state.ldlc_val_mmol * 38.67), step=5.0)
                        st.session_state.ldlc_val_mmol = ldlc_mg / 38.67
                        tg_mg = st.number_input("Triglycerides (mg/dL):", min_value=10.0, max_value=2500.0, value=float(st.session_state.tg_val_mmol * 88.57), step=10.0)
                        st.session_state.tg_val_mmol = tg_mg / 88.57

                    st.session_state.lpa_val = st.number_input("Lipoprotein(a) - nmol/L (nhập 0 nếu chưa làm):", min_value=0, max_value=500, value=st.session_state.get('lpa_val', 0))
                    st.session_state.hb_val = st.number_input("Hemoglobin (g/dL):", min_value=3.0, max_value=25.0, value=float(st.session_state.hb_val), step=0.1)
                    st.caption("ESC 2024: công thức máu (bao gồm hemoglobin) là xét nghiệm cơ bản được khuyến cáo trong đánh giá ban đầu.")

                with bio_col2:
                    st.session_state.hba1c_val = st.number_input("HbA1c (%):", min_value=3.0, max_value=20.0, value=st.session_state.get('hba1c_val', 5.8), step=0.1)
                    st.session_state.egfr_val = st.number_input("Mức lọc cầu thận eGFR (mL/min/1.73m²):", min_value=5, max_value=150, value=st.session_state.egfr_val)

                    known_dm = st.checkbox(
                        "Bệnh nhân đã được chẩn đoán đái tháo đường trước đó",
                        value=st.session_state.diabetes_flag,
                        key="known_dm_ccs"
                    )
                    st.session_state.diabetes_flag = known_dm
                    st.session_state.thyroid_assessed = st.checkbox(
                        "Đã đánh giá chức năng tuyến giáp ít nhất một lần",
                        value=st.session_state.thyroid_assessed,
                        key="thyroid_assessed_ccs"
                    )

                    st.session_state.dyslipidemia_flag = (st.session_state.ldlc_val_mmol >= 3.0 or st.session_state.tg_val_mmol >= 1.7)

                    if st.session_state.hba1c_val >= 6.5 and not known_dm:
                        st.warning("⚠️ HbA1c đang ở ngưỡng gợi ý đái tháo đường (≥6,5%). Công cụ không tự động xác lập chẩn đoán; cần xác nhận chẩn đoán theo bối cảnh lâm sàng/tiêu chuẩn chẩn đoán phù hợp.")
                    if st.session_state.egfr_val < 60:
                        st.error(f"⚠️ eGFR giảm ({st.session_state.egfr_val} mL/min): Có suy giảm chức năng thận; cần đối chiếu tính mạn tính và nguyên nhân.")
                    if not st.session_state.thyroid_assessed:
                        st.info("ℹ️ ESC 2024 khuyến cáo đánh giá chức năng tuyến giáp ít nhất một lần ở người bệnh nghi ngờ CCS.")

        with test_col2:
            st.write("**Thăm dò chọn lọc bổ sung:**")
            done_cxr = st.checkbox("Chụp X-quang ngực thẳng (khi có chỉ định chọn lọc)")
            if done_cxr:
                st.caption("ESC 2024: cân nhắc X-quang ngực khi nghi suy tim, bệnh phổi cấp, bệnh động mạch chủ hoặc nguyên nhân tim/lồng ngực ngoài mạch vành.")
                cxr_status = st.radio("Kết quả X-quang ngực:", ["Chưa ghi nhận bất thường (Bình thường)", "Có bất thường"])
                if cxr_status == "Có bất thường":
                    cxr_res = st.multiselect("Bất thường ghi nhận:", ["Bóng tim to", "Sung huyết phổi", "Tràn dịch màng phổi", "Bất thường phổi/động mạch chủ/lồng ngực khác"])
                    st.session_state.cxr_abnormal = len(cxr_res) > 0
                else:
                    st.session_state.cxr_abnormal = False
                    st.success("✅ Chưa ghi nhận bất thường trên X-quang ngực.")

            done_ambulatory_ecg = st.checkbox("Theo dõi ECG lưu động (Holter/ambulatory ECG) khi có chỉ định")
            if done_ambulatory_ecg:
                ambulatory_reason = st.multiselect(
                    "Chỉ định phù hợp:",
                    ["Đau ngực kèm nghi rối loạn nhịp", "Nghi đau thắt ngực do co thắt mạch vành (VSA)"]
                )
                if "Đau ngực kèm nghi rối loạn nhịp" in ambulatory_reason:
                    st.info("ℹ️ ESC 2024: ambulatory ECG được khuyến cáo khi đau ngực kèm nghi rối loạn nhịp (Class I C).")
                if "Nghi đau thắt ngực do co thắt mạch vành (VSA)" in ambulatory_reason:
                    st.info("ℹ️ ESC 2024: ambulatory ST-segment monitoring nên được cân nhắc khi nghi VSA và có triệu chứng thường xuyên (Class IIa B).")

            done_pft = st.checkbox("Đo chức năng hô hấp (PFT)")
            if done_pft:
                pft_res = st.radio("Kết quả đo PFT:", ["Bình thường", "Rối loạn thông khí tắc nghẽn (COPD/Hen)", "Rối loạn thông khí hạn chế"])
                st.session_state.pft_abnormal = (pft_res != "Bình thường")
                if st.session_state.pft_abnormal:
                    st.warning(f"👉 Kết quả PFT bất thường ({pft_res}): Gợi ý nguyên nhân hô hấp đi kèm.")

        # Navigation Button to next step
        st.write("")
        if not st.session_state.acute_flag:
            if st.button("Xác nhận & Sang Bước 2 ➡️"):
                set_step(2)


# ====================================================
# BƯỚC 2: ĐÁNH GIÁ CHUYÊN SÂU
# ====================================================
if render_main_step_header("BƯỚC 2: ĐÁNH GIÁ CHUYÊN SÂU", 2):
    
    # Sub-step 2.1: Siêu âm tim
    if render_sub_header("Siêu âm tim", 1, "step2_sub"):
        st.subheader("1. Đánh giá siêu âm tim qua thành ngực lúc nghỉ")
        echo_col1, echo_col2 = st.columns(2)
        with echo_col1:
            lvef_val = st.slider("Phân suất tống máu thất trái (LVEF %):", min_value=10, max_value=80, value=st.session_state.get('lvef_val', 55))
            st.session_state.lvef_val = lvef_val
        with echo_col2:
            echo_findings = st.multiselect("Kết quả siêu âm tim lúc nghỉ:", [
                "Chưa ghi nhận bất thường (Bình thường lúc nghỉ)",
                "Rối loạn vận động vùng thất trái (Regional wall motion abnormality)",
                "Bệnh van tim thực tổn (Hẹp/hở van mức độ vừa - nặng)",
                "Phì đại cơ thất trái (LV Hypertrophy)",
                "Rối loạn chức năng tâm trương thất trái",
                "Rối loạn chức năng thất phải",
                "Tăng áp lực động mạch phổi ước tính"
            ])
        st.session_state.lvd_flag = (lvef_val <= 40 or "Rối loạn vận động vùng thất trái (Regional wall motion abnormality)" in echo_findings)
        
        if lvef_val <= 40:
            st.error("⚠️ Phân suất tống máu thất trái giảm nặng (LVEF ≤ 40%): Cần tối ưu điều trị suy tim và xem xét chỉ định mạch vành khẩn trương.")
        else:
            st.success("✅ Chức năng tâm thu thất trái trong giới hạn bảo tồn.")

    # Sub-step 2.2: Khả năng lâm sàng nền
    if render_sub_header("Khả năng lâm sàng nền", 2, "step2_sub"):
        st.subheader("2. Ước tính Khả năng lâm sàng nền theo Figure 4 (Winther Model)")
        
        calc_col1, calc_col2 = st.columns(2)
        with calc_col1:
            gender = st.radio("Giới tính sinh học:", ["Nữ", "Nam"])
            age_group = st.selectbox("Nhóm tuổi:", ["30-39", "40-49", "50-59", "60-69", "70-80"])
            
            # Auto link symptom type
            s_type_step1 = st.session_state.symptom_analysis.get("type", "Đau/Khó chịu vùng ngực") if "symptom_analysis" in st.session_state else "Đau/Khó chịu vùng ngực"
            s_type_idx = 0 if s_type_step1 == "Đau/Khó chịu vùng ngực" else 1
            symptom_type = st.radio("Triệu chứng lâm sàng chính:", ["Cơn đau thắt ngực (Chest Pain)", "Khó thở khi gắng sức (Exertional Dyspnoea)"], index=s_type_idx)
            
            if symptom_type == "Cơn đau thắt ngực (Chest Pain)":
                st.write("**Bảng tính điểm triệu chứng Đau ngực (Winther Score):**")
                w_l = st.checkbox("Đau sau xương ức hoặc trước tim", value=True)
                w_tr = st.checkbox("Khởi phát khi gắng sức hoặc xúc cảm", value=True)
                w_re = st.checkbox("Giảm khi nghỉ hoặc dùng Nitrates trong 5 phút", value=True)
                symptom_score = int(w_l) + int(w_tr) + int(w_re)
                st.markdown(f"👉 **Điểm triệu chứng Đau ngực (Winther Score):** `{symptom_score} / 3 điểm`")
            else:
                symptom_score = 2
                st.info("👉 **Triệu chứng khó thở:** Tự động quy đổi tương đương **2 điểm** theo Ma trận Figure 4 của ESC 2024.")
                
        with calc_col2:
            st.write("**Yếu tố nguy cơ tim mạch đi kèm (Yếu tố nguy cơ = 1 điểm):**")
            rf_family = st.checkbox("Tiền sử gia đình mắc mạch vành sớm (Nam < 55, Nữ < 65) [1 điểm]")
            rf_smoking = st.checkbox("Đang hút thuốc lá hoặc có tiền sử hút thuốc [1 điểm]")
            rf_dyslipidemia = st.checkbox("Rối loạn lipid máu [1 điểm]", value=st.session_state.dyslipidemia_flag)
            rf_hypertension = st.checkbox("Tăng huyết áp [1 điểm]", value=st.session_state.hypertension_flag)
            rf_diabetes = st.checkbox("Đái tháo đường [1 điểm]", value=st.session_state.diabetes_flag)
            
            rf_count = int(rf_family) + int(rf_smoking) + int(rf_dyslipidemia) + int(rf_hypertension) + int(rf_diabetes)
            rf_category = "0-1" if rf_count <= 1 else ("2-3" if rf_count <= 3 else "4-5")
            st.markdown(f"👉 **Tổng điểm yếu tố nguy cơ:** `{rf_count} / 5 điểm` (Phân hạng: **{rf_category}**)")

        # Ma trận RF-CL Matrix Lookup Table (Figure 4)
        rf_cl_matrix = {
            "Nữ": {
                "30-39": {"0-1": {"0-1": 0, "2-3": 1, "4-5": 2}, "2": {"0-1": 0, "2-3": 1, "4-5": 3}, "3": {"0-1": 2, "2-3": 5, "4-5": 10}},
                "40-49": {"0-1": {"0-1": 1, "2-3": 1, "4-5": 3}, "2": {"0-1": 1, "2-3": 2, "4-5": 5}, "3": {"0-1": 4, "2-3": 7, "4-5": 12}},
                "50-59": {"0-1": {"0-1": 1, "2-3": 2, "4-5": 5}, "2": {"0-1": 2, "2-3": 3, "4-5": 7}, "3": {"0-1": 6, "2-3": 10, "4-5": 15}},
                "60-69": {"0-1": {"0-1": 2, "2-3": 4, "4-5": 7}, "2": {"0-1": 3, "2-3": 6, "4-5": 11}, "3": {"0-1": 10, "2-3": 14, "4-5": 19}},
                "70-80": {"0-1": {"0-1": 4, "2-3": 7, "4-5": 11}, "2": {"0-1": 6, "2-3": 10, "4-5": 16}, "3": {"0-1": 16, "2-3": 19, "4-5": 23}}
            },
            "Nam": {
                "30-39": {"0-1": {"0-1": 1, "2-3": 2, "4-5": 5}, "2": {"0-1": 2, "2-3": 4, "4-5": 8}, "3": {"0-1": 9, "2-3": 14, "4-5": 22}},
                "40-49": {"0-1": {"0-1": 2, "2-3": 4, "4-5": 7}, "2": {"0-1": 3, "2-3": 6, "4-5": 12}, "3": {"0-1": 14, "2-3": 20, "4-5": 27}},
                "50-59": {"0-1": {"0-1": 4, "2-3": 7, "4-5": 12}, "2": {"0-1": 6, "2-3": 11, "4-5": 17}, "3": {"0-1": 21, "2-3": 27, "4-5": 33}},
                "60-69": {"0-1": {"0-1": 8, "2-3": 12, "4-5": 17}, "2": {"0-1": 12, "2-3": 17, "4-5": 25}, "3": {"0-1": 32, "2-3": 35, "4-5": 39}},
                "70-80": {"0-1": {"0-1": 15, "2-3": 19, "4-5": 24}, "2": {"0-1": 22, "2-3": 27, "4-5": 34}, "3": {"0-1": 44, "2-3": 44, "4-5": 45}}
            }
        }

        score_key = "0-1" if symptom_score <= 1 else str(symptom_score)
        base_likelihood = rf_cl_matrix[gender][age_group][score_key][rf_category]
        
        # Color categorizer
        def get_likelihood_color(val):
            if val <= 5: return "#28a745"
            elif val <= 15: return "#17a2b8"
            elif val <= 50: return "#ffc107"
            elif val <= 85: return "#fd7e14"
            else: return "#dc3545"

        base_color = get_likelihood_color(base_likelihood)
        
        st.markdown(f"""
        <div style='background-color: #f8f9fa; border-radius: 6px; padding: 15px; border-left: 6px solid {base_color}; margin: 15px 0;'>
            <h4 style='margin: 0; color: #333;'>Khả năng lâm sàng ban đầu (Base RF-CL):</h4>
            <p style='font-size: 1.60rem; margin: 10px 0 5px 0; font-weight: bold;'>Ước tính RF-CL mắc bệnh mạch vành tắc nghẽn: <span style='color: {base_color};'>{base_likelihood}%</span></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Visualize the Figure 4 Matrix Simulation Dynamic Spotlight
        st.markdown("#### 📊 Ma trận tra cứu khả năng lâm sàng (Mô phỏng Figure 4 - ESC 2024)")
        st.caption(f"*Ma trận tùy chỉnh cho đối tượng: **{gender}**. Ô được khoanh vùng màu xanh lá cây 🎯 thể hiện vị trí định vị thực tế của bệnh nhân.*")
        
        age_ranges = ["30-39", "40-49", "50-59", "60-69", "70-80"]
        symptom_scores_keys = ["0-1", "2", "3"]
        rf_classes = ["0-1", "2-3", "4-5"]
        
        # We will build a styled HTML Table
        html_table = """
        <table style='width: 100%; border-collapse: collapse; text-align: center; font-size: 0.9rem; font-family: Arial, sans-serif;'>
            <thead>
                <tr style='background-color: #1e3d59; color: white;'>
                    <th style='border: 1px solid #ddd; padding: 10px;' rowspan='2'>Nhóm tuổi</th>
                    <th style='border: 1px solid #ddd; padding: 10px;' rowspan='2'>Điểm lâm sàng</th>
                    <th style='border: 1px solid #ddd; padding: 10px;' colspan='3'>Số lượng Yếu tố nguy cơ (Risk Factors)</th>
                </tr>
                <tr style='background-color: #2c5e7a; color: white;'>
                    <th style='border: 1px solid #ddd; padding: 8px;'>0 - 1 yếu tố</th>
                    <th style='border: 1px solid #ddd; padding: 8px;'>2 - 3 yếu tố</th>
                    <th style='border: 1px solid #ddd; padding: 8px;'>4 - 5 yếu tố</th>
                </tr>
            </thead>
            <tbody>
        """
        
        for age in age_ranges:
            rowspan_text = " rowspan='3'"
            for s_idx, s_key in enumerate(symptom_scores_keys):
                html_table += "<tr>"
                if s_idx == 0:
                    html_table += f"<td{rowspan_text} style='border: 1px solid #ddd; font-weight: bold; background-color: #f7f9fa; padding: 10px;'>{age} tuổi</td>"
                
                # Format symptom label
                s_label = "0 - 1 điểm" if s_key == "0-1" else f"{s_key} điểm"
                html_table += f"<td style='border: 1px solid #ddd; background-color: #ffffff; padding: 6px; font-weight: 500;'>{s_label}</td>"
                
                for r_cat in rf_classes:
                    val = rf_cl_matrix[gender][age][s_key][r_cat]
                    
                    # Check if this cell is the patient's coordinate
                    is_patient_cell = (age == age_group and s_key == score_key and r_cat == rf_category)
                    
                    if is_patient_cell:
                        cell_style = "background-color: #17b978 !important; color: #ffffff !important; font-weight: 800; border: 3px solid #1e3d59; font-size: 1.05rem;"
                        cell_content = f"🎯 {val}%"
                    else:
                        c_col = get_likelihood_color(val)
                        cell_style = f"background-color: {c_col}25; color: #333333; border: 1px solid #ddd;"
                        cell_content = f"{val}%"
                        
                    html_table += f"<td style='{cell_style} padding: 8px;'>{cell_content}</td>"
                html_table += "</tr>"
                
        html_table += "</tbody></table>"
        st.markdown(html_table, unsafe_allow_html=True)
        st.session_state.base_likelihood = base_likelihood

    # Sub-step 2.3: Điều chỉnh khả năng lâm sàng
    if render_sub_header("Điều chỉnh khả năng lâm sàng", 3, "step2_sub"):
        st.subheader("3. Cá thể hóa và phân tầng lại nguy cơ (Figure 5)")
        
        adj_col1, adj_col2 = st.columns(2)
        with adj_col1:
            st.write("**Các dữ kiện lâm sàng dùng để điều chỉnh clinical likelihood:**")
            
            ecg_adj_default = st.session_state.ecg_abnormal
            lvd_adj_default = st.session_state.get('lvd_flag', False)
            
            adj_ecg = st.checkbox("ECG lúc nghỉ bất thường (Sóng Q bệnh lý hoặc ST-T biến đổi)", value=ecg_adj_default)
            adj_lvd = st.checkbox("Siêu âm tim có rối loạn vận động vùng hoặc giảm LVEF", value=lvd_adj_default)
            adj_pad = st.checkbox("Bệnh nhân có tiền sử bệnh động mạch ngoại biên (PAD)")
            adj_calc = st.checkbox("X-quang ngực hoặc CT phổi ghi nhận vôi hóa mạch vành")
            adj_ex_ecg = st.checkbox("Nghiệm pháp gắng sức ECG có bất thường")
            st.caption("ESC 2024: dữ kiện khám mạch ngoại biên, ECG, siêu âm tim và vôi hóa trên hình ảnh được dùng để điều chỉnh RF-CL (Class I C). Ở nhóm RF-CL thấp >5–15%, exercise ECG và phát hiện xơ vữa ngoài mạch vành có thể được cân nhắc để điều chỉnh (Class IIb C).")

            has_clinical_adjusters = (adj_ecg or adj_lvd or adj_pad or adj_calc or adj_ex_ecg)

        with adj_col2:
            st.write("**Phân tầng lại bằng Điểm vôi hóa mạch vành (CACS):**")
            cacs_available = st.radio("Đo vôi hóa mạch vành (CACS):", ["Chưa thực hiện", "Đã có kết quả"])
            cacs_val = -1

            if cacs_available == "Đã có kết quả":
                cacs_val = st.number_input("Nhập điểm vôi hóa mạch vành (Agatston):", min_value=0, max_value=5000, value=0, step=10)
                if cacs_val == 0:
                    st.success("✅ **CACS = 0:** Không ghi nhận vôi hóa mạch vành; CACS = 0 có giá trị dự báo âm rất cao đối với CAD tắc nghẽn, nhưng không được dùng riêng lẻ để tự gán một % RF-CL mới.")
                elif cacs_val < 100:
                    st.info("ℹ️ Có vôi hóa mạch vành mức thấp. CACS được dùng để hỗ trợ tái phân loại khả năng lâm sàng, không tự động cộng/trừ một số % cố định.")
                elif cacs_val < 400:
                    st.warning("⚠️ Có gánh nặng vôi hóa mạch vành đáng kể. Cần tích hợp với RF-CL và các dữ kiện lâm sàng; không tự động cộng +10% hoặc ép sang một nhóm nguy cơ cố định.")
                else:
                    st.warning("⚠️ Vôi hóa mạch vành nhiều có thể làm giảm chất lượng/độ chính xác của CCTA; khi phù hợp có thể ưu tiên hình ảnh chức năng. Không tự động suy diễn CACS thành một % khả năng lâm sàng.")

        # ESC 2024: RF-CL là nền; dữ kiện lâm sàng được dùng để điều chỉnh bằng clinical judgement.
        # Chỉ CACS-CL là mô hình đã được validation để tạo ra ước tính định lượng sau khi thêm CACS.
        base_lk = st.session_state.get('base_likelihood', 20)

        def get_class_label(val):
            if val <= 5: return "Rất thấp (Very Low)", "#28a745"
            elif val <= 15: return "Thấp (Low)", "#17a2b8"
            elif val <= 50: return "Trung bình (Moderate)", "#ffc107"
            elif val <= 85: return "Cao (High)", "#fd7e14"
            else: return "Rất cao (Very High)", "#dc3545"

        base_label, base_col = get_class_label(base_lk)

        if has_clinical_adjusters:
            st.warning("💡 **Clinical judgement:** ECG, siêu âm tim, bệnh động mạch ngoại biên, vôi hóa trên hình ảnh hoặc exercise ECG bất thường có thể làm thay đổi khả năng lâm sàng so với RF-CL nền. ESC 2024 không cung cấp công thức cộng % cố định cho các yếu tố này.")

        if cacs_available == "Đã có kết quả":
            if 5 < base_lk <= 15:
                st.info("ℹ️ **RF-CL thấp (>5–15%):** ESC 2024 khuyến cáo nên cân nhắc CACS để tái phân loại bằng mô hình **CACS-CL đã được validation** và nhận diện thêm người bệnh có khả năng rất thấp (≤5%) (Class IIa B).")
            else:
                st.info("ℹ️ CACS có thể hỗ trợ điều chỉnh clinical likelihood và lựa chọn thăm dò, nhưng công cụ này không tự suy diễn CACS thành một % mới khi không có kết quả CACS-CL đã được tính/đánh giá.")

        reclass_options = [
            "Giữ nguyên nhóm RF-CL nền",
            "Rất thấp (≤5%)",
            "Thấp (>5–15%)",
            "Trung bình (>15–50%)",
            "Cao (>50–85%)",
            "Rất cao (>85%)"
        ]
        reclass_choice = st.selectbox(
            "Nhóm clinical likelihood sau khi bác sĩ tích hợp dữ kiện bổ sung / kết quả CACS-CL (nếu có):",
            reclass_options,
            help="Không chọn nhóm mới chỉ dựa trên phép cộng/trừ CACS. Nếu chưa có cơ sở tái phân loại định lượng, giữ nguyên RF-CL nền."
        )

        if reclass_choice == "Giữ nguyên nhóm RF-CL nền":
            final_category = base_label
            final_display = f"{base_lk}%"
            final_col = base_col
        else:
            final_category = reclass_choice.replace("≤", "≤").replace("–", "–")
            final_display = "Không suy diễn % chính xác"
            category_colors = {
                "Rất thấp (≤5%)": "#28a745",
                "Thấp (>5–15%)": "#17a2b8",
                "Trung bình (>15–50%)": "#ffc107",
                "Cao (>50–85%)": "#fd7e14",
                "Rất cao (>85%)": "#dc3545"
            }
            final_col = category_colors[reclass_choice]

        st.markdown(f"""
        <div style='background-color: #f1f2f6; border-radius: 6px; padding: 15px; border-left: 6px solid {final_col}; margin: 15px 0;'>
            <h4 style='margin: 0; color: #333;'>Khả năng lâm sàng sau tích hợp dữ kiện:</h4>
            <p style='font-size: 1.35rem; margin: 10px 0 5px 0; font-weight: bold;'>RF-CL nền: <span style='color: {base_col};'>{base_lk}% — {base_label}</span></p>
            <p style='margin: 0;'>Phân loại sử dụng cho bước chọn thăm dò: <strong style='color: {final_col};'>{final_category}</strong> ({final_display})</p>
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        if st.button("Xác nhận & Sang Bước 3 ➡️"):
            st.session_state.likelihood_value = base_lk
            st.session_state.likelihood_category = final_category
            st.session_state.cacs_score_val = cacs_val if cacs_available == "Đã có kết quả" else -1
            set_step(3)


# ====================================================
# BƯỚC 3: XÁC ĐỊNH CHẨN ĐOÁN
# ====================================================
if render_main_step_header("BƯỚC 3: XÁC ĐỊNH CHẨN ĐOÁN", 3):
    
    # Sub-step 3.1: Khuyến cáo thăm dò
    if render_sub_header("Khuyến cáo thăm dò", 1, "step3_sub"):
        st.subheader("1. Khuyến cáo lựa chọn kỹ thuật chẩn đoán đầu tay")
        
        lik = st.session_state.get('likelihood_value', 20)
        lik_category = st.session_state.get('likelihood_category')
        cacs_score = st.session_state.get('cacs_score_val', -1)

        if not lik_category:
            if lik <= 5:
                lik_category = "Rất thấp (Very Low)"
            elif lik <= 15:
                lik_category = "Thấp (Low)"
            elif lik <= 50:
                lik_category = "Trung bình (Moderate)"
            elif lik <= 85:
                lik_category = "Cao (High)"
            else:
                lik_category = "Rất cao (Very High)"

        st.markdown(f"RF-CL nền: **{lik}%**. Nhóm clinical likelihood sử dụng cho lựa chọn thăm dò: **{lik_category}**")

        is_very_low = ("Rất thấp" in lik_category)
        is_low = ("Thấp" in lik_category and "Rất thấp" not in lik_category)
        is_moderate = ("Trung bình" in lik_category)
        is_high = ("Cao" in lik_category and "Rất cao" not in lik_category)
        is_very_high = ("Rất cao" in lik_category)

        if is_very_low:
            st.markdown("""
            <div class='success-box'>
                <strong>🟢 CÂN NHẮC HOÃN THĂM DÒ CHẨN ĐOÁN SÂU HƠN <span class='class-badge-2a'>Class IIa B</span></strong><br>
                - Ở người có clinical likelihood rất thấp (≤5%), nên cân nhắc trì hoãn thăm dò chẩn đoán thêm.<br>
                - Nếu triệu chứng vẫn dai dẳng sau khi đã loại trừ nguyên nhân ngoài tim, cần đánh giá lại thay vì coi kết quả này là loại trừ tuyệt đối mọi cơ chế thiếu máu cơ tim.
            </div>
            """, unsafe_allow_html=True)

        elif is_low:
            st.markdown("""
            <div class='recommendation-box'>
                <strong>🔵 CCTA LÀ PHƯƠNG THỨC ƯU TIÊN ĐỂ LOẠI TRỪ CAD TẮC NGHẼN <span class='class-badge-1'>Class I B</span></strong><br>
                - Với clinical likelihood thấp (>5–15%), CCTA là phương thức ưu tiên để loại trừ CAD tắc nghẽn.<br>
                - Nếu chưa thực hiện CACS-CL, CACS có thể được cân nhắc để tái phân loại thêm ở nhóm này.
            </div>
            """, unsafe_allow_html=True)

        elif is_moderate:
            if cacs_score >= 400:
                st.markdown("""
                <div class='warning-box' style='border-left-color: #fd7e14;'>
                    <strong>🟡 CCTA HOẶC HÌNH ẢNH CHỨC NĂNG — LỰA CHỌN THEO ĐẶC ĐIỂM NGƯỜI BỆNH <span class='class-badge-1'>Class I B</span></strong><br>
                    - Với clinical likelihood trung bình (>15–50%), CCTA hoặc hình ảnh chức năng đều là lựa chọn đầu tay phù hợp.<br>
                    - Bệnh nhân có vôi hóa mạch vành nhiều: hạn chế kỹ thuật của CCTA tăng lên, vì vậy hình ảnh chức năng có thể phù hợp hơn.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class='warning-box' style='border-left-color: #fd7e14;'>
                    <strong>🟡 CCTA HOẶC HÌNH ẢNH CHỨC NĂNG <span class='class-badge-1'>Class I B</span></strong><br>
                    - CCTA được ưu tiên khi mục tiêu chính là loại trừ CAD tắc nghẽn và nhận diện CAD không tắc nghẽn.<br>
                    - Hình ảnh chức năng (Stress Echo, Stress CMR, SPECT, PET) được ưu tiên khi cần liên hệ triệu chứng với thiếu máu cơ tim, đánh giá viability hoặc nghi bệnh vi mạch.
                </div>
                """, unsafe_allow_html=True)

        elif is_high:
            st.markdown("""
            <div class='warning-box' style='border-left-color: #fd7e14;'>
                <strong>🟠 ƯU TIÊN HÌNH ẢNH CHỨC NĂNG <span class='class-badge-1'>Class I B</span></strong><br>
                - Với clinical likelihood cao (>50–85%), hình ảnh chức năng thường được ưu tiên để đánh giá thiếu máu cơ tim và hỗ trợ quyết định tái thông.<br>
                - Lựa chọn kỹ thuật cụ thể vẫn phải dựa trên đặc điểm người bệnh, khả năng thực hiện và chuyên môn tại cơ sở.
            </div>
            """, unsafe_allow_html=True)

        elif is_very_high:
            st.markdown("""
            <div class='warning-box'>
                <strong>🔴 CÂN NHẮC/CHỈ ĐỊNH ICA KHI CLINICAL LIKELIHOOD RẤT CAO HOẶC CÓ DẤU HIỆU NGUY CƠ CAO</strong><br>
                - ESC 2024 khuyến cáo ICA để chẩn đoán CAD tắc nghẽn ở người có pre/post-test likelihood rất cao, triệu chứng nặng kháng GDMT, đau ngực ở mức gắng sức thấp và/hoặc nguy cơ biến cố cao.<br>
                - Nếu gặp tổn thương trung gian, cần đánh giá chức năng xâm lấn bằng FFR/iFR trước khi quyết định tái thông.
            </div>
            """, unsafe_allow_html=True)

    # Sub-step 3.2: Kết quả cận lâm sàng
    if render_sub_header("Kết quả cận lâm sàng", 2, "step3_sub"):
        st.subheader("2. Ghi nhận kết quả chẩn đoán hình ảnh thực tế")
        
        selected_test = st.radio(
            "Phương pháp chẩn đoán hình ảnh thực tế đã thực hiện:",
            ["Chờ kết quả / Chưa làm", "Chụp cắt lớp vi tính động mạch vành (CCTA)", "Thăm dò hình ảnh chức năng gắng sức", "Chụp động mạch vành xâm lấn (ICA)"]
        )
        st.session_state.selected_test_val = selected_test
        
        st.session_state.anoca_suspected = False
        st.session_state.high_risk_flag = False

        if selected_test == "Chụp cắt lớp vi tính động mạch vành (CCTA)":
            ccta_res = st.radio(
                "Kết quả mạch vành trên phim CCTA:",
                ["Không hẹp hoặc hẹp nhẹ (<50% Thân chung LMS, <50% các nhánh lớn)",
                 "Hẹp mức độ trung gian (cần đánh giá thêm ý nghĩa chức năng)",
                 "Hẹp nặng rõ rệt (ví dụ ≥50% Thân chung LMS hoặc ≥70% nhánh lớn khác)"]
            )

            if "Không hẹp" in ccta_res:
                st.session_state.coronary_status = "Non-obstructive"

            elif "trung gian" in ccta_res:
                st.warning("⚠️ **Tổn thương trung gian:** Mức độ hẹp giải phẫu không đồng nghĩa với ý nghĩa huyết động. Cần đánh giá thêm trước khi quyết định tái thông.")
                ccta_functional = st.radio(
                    "Đánh giá thêm tổn thương trung gian:",
                    ["Chưa đánh giá / Đang chờ",
                     "FFR-CT ≤ 0.80",
                     "FFR-CT > 0.80",
                     "Hình ảnh chức năng dương tính với thiếu máu cơ tim",
                     "Hình ảnh chức năng âm tính với thiếu máu cơ tim"]
                )

                if ccta_functional == "FFR-CT ≤ 0.80":
                    st.session_state.coronary_status = "Obstructive"
                    st.success("✅ Tổn thương trung gian trên CCTA có FFR-CT ≤0,80: có ý nghĩa chức năng.")
                elif ccta_functional == "FFR-CT > 0.80":
                    st.session_state.coronary_status = "Non-obstructive"
                    st.info("ℹ️ Tổn thương trung gian không cho thấy ý nghĩa huyết động theo FFR-CT.")
                elif ccta_functional == "Hình ảnh chức năng dương tính với thiếu máu cơ tim":
                    st.session_state.coronary_status = "Intermediate + Ischaemia"
                    st.warning("⚠️ Có thiếu máu cơ tim trên thăm dò chức năng, nhưng kết quả này không tự nó chứng minh CAD tắc nghẽn. Cần tích hợp giải phẫu và mức độ thiếu máu để quyết định bước tiếp theo.")
                elif ccta_functional == "Hình ảnh chức năng âm tính với thiếu máu cơ tim":
                    st.session_state.coronary_status = "Intermediate / no inducible ischaemia"
                    st.info("ℹ️ Tổn thương trung gian chưa cho thấy thiếu máu cơ tim cảm ứng; không tự động đồng nhất với mạch vành hoàn toàn bình thường.")
                else:
                    st.session_state.coronary_status = "Indeterminate"
                    st.info("ℹ️ Chưa đủ dữ liệu để phân loại tổn thương trung gian là có hay không có ý nghĩa chức năng.")

            else:
                st.session_state.coronary_status = "Obstructive"

        elif selected_test == "Thăm dò hình ảnh chức năng gắng sức":
            func_res = st.radio(
                "Kết quả thiếu máu cơ tim gắng sức:",
                ["Âm tính (không ghi nhận thiếu máu cơ tim cảm ứng đáng kể)",
                 "Dương tính (phát hiện thiếu máu cơ tim cảm ứng)"]
            )
            if "Dương tính" in func_res:
                st.session_state.coronary_status = "Ischaemia-positive / anatomy unconfirmed"
                st.warning("⚠️ Hình ảnh chức năng dương tính xác nhận thiếu máu cơ tim cảm ứng, **không tự động xác nhận CAD tắc nghẽn**. Nếu giải phẫu mạch vành chưa biết, cần lựa chọn CCTA hoặc ICA tùy mức độ thiếu máu, clinical likelihood và nguy cơ biến cố.")
            else:
                st.session_state.coronary_status = "No inducible ischaemia / anatomy unconfirmed"
                st.info("ℹ️ Hình ảnh chức năng âm tính không đồng nghĩa với việc đã chứng minh không có xơ vữa mạch vành; nếu triệu chứng vẫn dai dẳng, cần xem xét ANOCA/INOCA và các nguyên nhân khác theo bối cảnh.")

        elif selected_test == "Chụp động mạch vành xâm lấn (ICA)":
            ica_res = st.radio(
                "Kết quả giải phẫu mạch vành trên phim ICA:",
                ["Không hẹp hoặc hẹp nhẹ (<50% Thân chung LMS, <50% các nhánh chính)",
                 "Hẹp mức độ trung gian (thường khoảng 40–90% ngoài thân chung hoặc 40–70% thân chung)",
                 "Hẹp nặng rõ rệt"]
            )
            if "Không hẹp" in ica_res:
                st.session_state.coronary_status = "Non-obstructive"

            elif "trung gian" in ica_res:
                st.warning("⚠️ **Tổn thương trung gian:** ESC 2024 khuyến cáo đánh giá chức năng bằng FFR/iFR để hướng dẫn quyết định tái thông (FFR ≤0,80 hoặc iFR ≤0,89 được xem là có ý nghĩa).")
                ica_functional = st.radio(
                    "Kết quả đo FFR/iFR:",
                    ["Chưa đo FFR/iFR / Đang chờ",
                     "CÓ Ý NGHĨA SINH LÝ (FFR ≤ 0.80 hoặc iFR ≤ 0.89)",
                     "KHÔNG CÓ Ý NGHĨA SINH LÝ (FFR > 0.80 và iFR > 0.89)"]
                )
                if "CÓ Ý NGHĨA" in ica_functional:
                    st.session_state.coronary_status = "Obstructive"
                elif "KHÔNG CÓ Ý NGHĨA" in ica_functional:
                    st.session_state.coronary_status = "Non-obstructive"
                    st.info("ℹ️ Tổn thương trung gian không có ý nghĩa chức năng; nếu triệu chứng dai dẳng, bệnh nhân vẫn có thể thuộc phổ ANOCA/INOCA.")
                else:
                    st.session_state.coronary_status = "Indeterminate"

            else:
                st.session_state.coronary_status = "Obstructive"

        else:
            st.info("💡 Đang chờ kết quả thăm dò. Vui lòng cập nhật để thực hiện phân tầng điều trị.")
            st.session_state.coronary_status = "Untested"

        status_labels = {
            "Obstructive": "CAD tắc nghẽn / tổn thương thượng tâm mạc có ý nghĩa",
            "Non-obstructive": "Không có CAD tắc nghẽn hoặc không có tổn thương thượng tâm mạc giới hạn dòng",
            "Indeterminate": "Chưa xác định — cần đánh giá thêm",
            "Intermediate + Ischaemia": "Tổn thương trung gian + có thiếu máu cơ tim; chưa đồng nhất với CAD tắc nghẽn",
            "Intermediate / no inducible ischaemia": "Tổn thương trung gian, chưa ghi nhận thiếu máu cơ tim cảm ứng",
            "Ischaemia-positive / anatomy unconfirmed": "Có thiếu máu cơ tim cảm ứng — chưa biết giải phẫu mạch vành",
            "No inducible ischaemia / anatomy unconfirmed": "Không ghi nhận thiếu máu cơ tim cảm ứng — chưa biết giải phẫu mạch vành",
            "Untested": "Chưa có kết quả xác định"
        }
        st.write(f"👉 Trạng thái hiện tại: **{status_labels.get(st.session_state.coronary_status, st.session_state.coronary_status)}**")

    # Sub-step 3.3: Chẩn đoán ANOCA/INOCA
    if render_sub_header("Chẩn đoán ANOCA/INOCA", 3, "step3_sub"):
        if st.session_state.get('coronary_status', "Untested") == "Non-obstructive":
            st.subheader("3. Đánh giá đau ngực không hẹp tắc nghẽn (ANOCA/INOCA)")
            
            has_symptoms = st.radio(
                "Bệnh nhân vẫn có triệu chứng dai dẳng dù đã điều trị nội khoa, ảnh hưởng chất lượng cuộc sống và đã loại trừ nguyên nhân ngoài tim không?",
                ["Có — dai dẳng dù điều trị và ảnh hưởng chất lượng cuộc sống", "Không — triệu chứng nhẹ/ổn định hoặc chưa đáp ứng tiêu chí trên"]
            )

            if has_symptoms.startswith("Có"):
                st.session_state.anoca_suspected = True
                st.markdown("""
                <div class='warning-box' style='border-left-color: #f1c40f; background-color: #fefdf3;'>
                    <h4 style='color: #d4ac0d; margin-top: 0;'>🧩 NGHI NGỜ LÂM SÀNG: MẮC ANOCA / INOCA</h4>
                    <p>Giải phẫu mạch vành không có hẹp tắc nghẽn hoặc không có tổn thương thượng tâm mạc giới hạn dòng, trong khi triệu chứng vẫn dai dẳng dù điều trị và ảnh hưởng chất lượng cuộc sống. ESC 2024 khuyến cáo <strong>đo chức năng mạch vành xâm lấn (ICFT - Class I B)</strong> để xác định endotype có thể điều trị, có tính đến lựa chọn và ưu tiên của người bệnh.</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.write("**Nhập kết quả đo chức năng mạch vành xâm lấn (ICFT) bám sát tiêu chuẩn ESC 2024:**")
                col_i1, col_i2 = st.columns(2)
                with col_i1:
                    icft_cfr = st.selectbox("1. Lưu lượng dự trữ mạch vành (CFR):", ["Bình thường (CFR ≥ 2.5)", "Giảm (CFR < 2.5)"])
                    icft_imr = st.selectbox("2. Kháng trở vi tuần hoàn (IMR/HMR):", ["Bình thường (IMR < 25 VÀ HMR ≤ 2.5)", "Tăng (IMR ≥ 25 HOẶC HMR > 2.5)"])
                with col_i2:
                    icft_spasm = st.selectbox(
                        "3. Nghiệm pháp kích thích Acetylcholine (ACh):",
                        ["Âm tính", 
                         "Dương tính co thắt thượng tâm mạc (Hẹp kính mạch ≥ 90% kèm tái phát đau ngực và ST biến đổi)", 
                         "Dương tính co thắt vi tuần hoàn (ST biến đổi và tái phát đau ngực nhưng không co thắt nhánh mạch lớn)"]
                    )
                
                # Endotype Formulation
                st.session_state.anoca_endotype = "Chưa phân loại"
                has_cmd = (icft_cfr == "Giảm (CFR < 2.5)" or icft_imr == "Tăng (IMR ≥ 25 HOẶC HMR > 2.5)")
                epicardial_spasm = "thượng tâm mạc" in icft_spasm
                microvascular_spasm = "vi tuần hoàn" in icft_spasm

                if has_cmd and epicardial_spasm:
                    st.session_state.anoca_endotype = "Kiểu hình hỗn hợp (MVA + VSA)"
                elif has_cmd or microvascular_spasm:
                    st.session_state.anoca_endotype = "Đau thắt ngực vi mạch (MVA)"
                elif epicardial_spasm:
                    st.session_state.anoca_endotype = "Co thắt mạch vành thượng tâm mạc (VSA)"
                else:
                    st.session_state.anoca_endotype = "Không xác định endotype mạch vành bằng ICFT hiện tại"
                    
                st.success(f"🎯 **Kiểu hình ANOCA/INOCA xác định:** `{st.session_state.anoca_endotype}`. Phác đồ điều trị cá thể hóa tương ứng đã kích hoạt tại Bước 4.")
            else:
                st.session_state.anoca_suspected = False
                st.success("✅ Mạch vành không hẹp tắc nghẽn và lâm sàng ổn định, không có chỉ định thăm dò ANOCA chuyên sâu.")
        else:
            st.info("💡 Phần này chỉ hiển thị khi giải phẫu mạch vành được xác định là: **LOẠI TRỪ hẹp tắc nghẽn (Non-obstructive CAD)** ở tiểu mục 2.")

    # Sub-step 3.4: Phân tầng nguy cơ
    if render_sub_header("Phân tầng nguy cơ", 4, "step3_sub"):
        if st.session_state.get('coronary_status', "Untested") != "Untested":
            st.subheader("4. Phân tầng nguy cơ biến cố tim mạch tương lai (Event-Risk)")
            st.markdown("<p style='font-size: 0.95rem;'>Các tiêu chuẩn dưới đây là những dấu hiệu được ESC 2024 khuyến cáo sử dụng để nhận diện người bệnh nguy cơ biến cố cao (Class I B):</p>", unsafe_allow_html=True)

            risk_col1, risk_col2 = st.columns(2)
            with risk_col1:
                st.write("**Các tiêu chuẩn về cấu trúc giải phẫu (Anatomical):**")
                high_risk_anatomy = st.checkbox("CCTA: Thân chung trái (Left Main) hẹp ≥ 50%")
                high_risk_anatomy_2 = st.checkbox("CCTA: Bệnh 3 nhánh, mỗi nhánh hẹp ≥ 70%")
                high_risk_anatomy_3 = st.checkbox("CCTA: Bệnh 2 nhánh hẹp ≥ 70%, có bao gồm đoạn gần LAD")
                high_risk_anatomy_4 = st.checkbox("CCTA: Hẹp đoạn gần LAD ≥ 70% VÀ FFR-CT ≤ 0.80")
            with risk_col2:
                st.write("**Các tiêu chuẩn về chức năng thiếu máu (Functional):**")
                high_risk_func_1 = st.checkbox("Stress Echo: ≥ 3/16 phân vùng giảm động hoặc vô động do stress")
                high_risk_func_2 = st.checkbox("Stress CMR: ≥ 2/16 phân vùng có perfusion defect HOẶC ≥ 3 phân vùng rối loạn vận động do dobutamine")
                high_risk_func_3 = st.checkbox("Stress SPECT/PET: vùng thiếu máu cơ tim ≥ 10% khối cơ thất trái")
                high_risk_func_4 = st.checkbox("Exercise ECG: Duke Treadmill Score < -10")

            is_high_risk = (
                high_risk_anatomy or high_risk_anatomy_2 or high_risk_anatomy_3 or high_risk_anatomy_4 or
                high_risk_func_1 or high_risk_func_2 or high_risk_func_3 or high_risk_func_4
            )
            st.session_state.high_risk_flag = is_high_risk

            if is_high_risk:
                st.error("""
                **🚨 NGUY CƠ BIẾN CỐ CAO (HIGH EVENT-RISK):**
                - Có ít nhất một tiêu chuẩn nguy cơ cao theo ESC 2024.
                - **ICA kèm đánh giá áp lực nội mạch (FFR/iFR) khi phù hợp được khuyến cáo Class I A** nhằm làm rõ nguy cơ và xác định chiến lược điều trị.
                - Việc có tiêu chuẩn nguy cơ cao **không đồng nghĩa tự động với PCI/CABG để kéo dài sống còn**; chỉ định và phương thức tái thông còn phụ thuộc giải phẫu, ý nghĩa chức năng, LVEF, bệnh đồng mắc, nguy cơ thủ thuật và đáp ứng GDMT.
                """)
            else:
                st.info("💡 Chưa ghi nhận tiêu chuẩn high event-risk nào trong các mục đã chọn. Vẫn cần tích hợp tuổi, ECG, ngưỡng xuất hiện đau ngực, đái tháo đường, CKD, LVEF và toàn bộ dữ liệu lâm sàng để đánh giá nguy cơ.")
        else:
            st.info("💡 Chưa có kết quả thăm dò để phân tầng nguy cơ biến cố bằng các tiêu chuẩn hình ảnh/chức năng.")
        # Navigation to Step 4
        st.write("")
        if st.button("Xác nhận & Sang Bước 4 ➡️"):
            set_step(4)


# ====================================================
# BƯỚC 4: ĐIỀU TRỊ TỐI ƯU
# ====================================================
if render_main_step_header("BƯỚC 4: ĐIỀU TRỊ TỐI ƯU", 4):
    
    # Sub-step 4.1: Điều trị nội khoa
    if render_sub_header("Điều trị nội khoa", 1, "step4_sub"):
        st.subheader("1. Thiết lập phác đồ điều trị nội khoa tối ưu (GDMT)")
        
        tab_prognostic, tab_symptomatic = st.tabs(["🛡️ Thuốc bảo vệ & Cải thiện tiên lượng", "💊 Thuốc giảm đau thắt ngực (Figure 9)"])
        
        with tab_prognostic:
            st.write("**Thay đổi lối sống lành mạnh (Class I):**")
            st.markdown("""
            * **Cai thuốc lá tuyệt đối:** Hỗ trợ tư vấn cai thuốc, tránh phơi nhiễm khói thuốc lá thụ động (Class I A).
            * **Chế độ ăn Địa Trung Hải:** Hạn chế chất béo bão hòa < 10% năng lượng, tăng cường rau xanh, ngũ cốc nguyên hạt. Giới hạn rượu bia.
            * **Hoạt động thể lực:** Tập thể dục cường độ trung bình 150-300 phút hoặc cường độ mạnh 75-150 phút hàng tuần (Class I B).
            """)
            
            st.write("**Điều trị dự phòng biến cố — áp dụng theo đúng bối cảnh lâm sàng:**")
            st.markdown("""
            * **Kháng huyết khối dài hạn:**
                * CCS có **tiền sử MI hoặc PCI từ xa:** Aspirin 75–100 mg/ngày lâu dài — **Class I A**; Clopidogrel 75 mg/ngày là lựa chọn thay thế an toàn và hiệu quả cho aspirin — **Class I A**.
                * **Sau CABG:** Aspirin 75–100 mg/ngày lâu dài — **Class I A**.
                * Không có tiền sử MI/tái thông nhưng có **CAD tắc nghẽn đáng kể:** Aspirin 75–100 mg/ngày lâu dài — **Class I B**.
                * Lựa chọn và thời gian điều trị phải cân bằng nguy cơ thiếu máu cục bộ và nguy cơ chảy máu; không mặc định “aspirin hoặc clopidogrel Class I A” cho mọi CCS.
            * **Huyết áp:** Mục tiêu thực hành trong CCS là **SBP 120–129 mmHg nếu dung nạp**. Không tự gán mục tiêu DBP 70–79 mmHg như một khuyến cáo CCS Class I A từ guideline này.
            * **ACE-I/ARB:** Được khuyến cáo khi CCS kèm **tăng huyết áp, LVEF ≤40%, đái tháo đường hoặc CKD**, nếu không có chống chỉ định.
            """)
            if st.session_state.get('diabetes_flag', False):
                st.markdown("""
                * **T2DM đã được xác định + CCS:** SGLT2 inhibitor có bằng chứng lợi ích tim mạch và GLP-1 receptor agonist có bằng chứng lợi ích tim mạch đều **được khuyến cáo Class I A** để giảm biến cố tim mạch, độc lập với HbA1c nền/đích.
                """)
            else:
                st.caption("ℹ️ Không tự kích hoạt khuyến cáo SGLT2i/GLP-1 RA chỉ từ một giá trị HbA1c; cần xác định bệnh nhân thực sự có T2DM.")
                st.markdown("* **Không có T2DM nhưng thừa cân/béo phì (BMI ≥27 kg/m²):** Semaglutide **nên được cân nhắc (Class IIa B)** để giảm tử vong tim mạch, MI hoặc đột quỵ ở bệnh nhân CCS phù hợp.")
            
        with tab_symptomatic:
            # Pull clinical variables
            hr_val = st.session_state.get('hr_val', 75)
            sbp_val = st.session_state.get('sbp_val', 120)
            lvef_val = st.session_state.get('lvef_val', 55)
            egfr_val = st.session_state.get('egfr_val', 90)
            pft_abnormal = st.session_state.get('pft_abnormal', False)
            anoca_suspected = st.session_state.get('anoca_suspected', False)
            anoca_endotype = st.session_state.get('anoca_endotype', "Chưa phân loại")
            
            st.info("💊 **Cắt cơn đau thắt ngực:** Nitrate tác dụng ngắn được khuyến cáo để giảm đau ngực tức thời (**Class I B**), nếu không có chống chỉ định như dùng đồng thời PDE-5 inhibitor.")
            
            # Phenotype categorization
            if anoca_suspected and "VSA" in anoca_endotype:
                phenotype = "Co thắt mạch vành (ANOCA - VSA)"
                phenotype_desc = "Đau thắt ngực do co thắt động mạch thượng tâm mạc, không hẹp tắc nghẽn."
            elif anoca_suspected and "MVA" in anoca_endotype:
                phenotype = "Đau thắt ngực vi mạch (ANOCA - MVA)"
                phenotype_desc = "Rối loạn chức năng vi tuần hoàn mạch vành không có hẹp cơ học."
            elif lvef_val <= 40:
                phenotype = "Rối loạn chức năng thất trái / Suy tim giảm LVEF ≤ 40%"
                phenotype_desc = "Rối loạn chức năng tâm thu thất trái nặng kèm suy tim cơ năng."
            elif hr_val > 80:
                phenotype = "Tần số tim nhanh (HR > 80 nhịp/phút)"
                phenotype_desc = "Nhịp tim nền cao, ưu thế nhịp nhanh làm tăng công tim và thiếu máu."
            elif hr_val < 55:
                phenotype = "Tần số tim chậm (HR < 55 nhịp/phút)"
                phenotype_desc = "Nhịp tim nền thấp, chống chỉ định các thuốc làm giảm nhịp thêm."
            elif sbp_val < 95:
                phenotype = "Huyết áp thấp (SBP < 95 mmHg)"
                phenotype_desc = "Huyết áp cơ bản thấp, chống chỉ định các thuốc giãn mạch gây hạ áp mạnh."
            else:
                phenotype = "Kiểu hình chuẩn (Standard Profile)"
                phenotype_desc = "Nhịp tim, huyết áp và chức năng tim nằm trong giới hạn bình thường."
                
            # Mode selector
            if 'prescribing_mode_val' not in st.session_state:
                st.session_state.prescribing_mode_val = "💡 Khuyến nghị phác đồ (Tự động đề xuất theo Guideline)"
                
            mode_options = [
                "💡 Khuyến nghị phác đồ (Tự động đề xuất theo Guideline)",
                "🛠️ Tự phối hợp và tra cứu"
            ]
            default_mode_idx = mode_options.index(st.session_state.prescribing_mode_val) if st.session_state.prescribing_mode_val in mode_options else 0
            prescribing_mode = st.radio("Lựa chọn phương thức kê đơn chống đau ngực:", mode_options, index=default_mode_idx)
            st.session_state.prescribing_mode_val = prescribing_mode
            
            # 1. Advisor mode
            if prescribing_mode == "💡 Khuyến nghị phác đồ (Tự động đề xuất theo Guideline)":
                st.markdown(f"""
                <div class='info-box' style='background-color: #f7f9fa; border-left: 5px solid #17b978; margin-bottom: 20px;'>
                    <h5 style='margin-top: 0; color: #1e3d59; font-weight: bold;'>👤 KIỂU HÌNH LÂM SÀNG TỰ ĐỘNG:</h5>
                    <p style='margin: 0; font-size: 1.1rem;'>Kiểu hình phát hiện: <strong style='color: #17b978;'>{phenotype}</strong></p>
                    <p style='margin: 5px 0 0 0; color: #555; font-size: 0.9rem;'>{phenotype_desc} (Thông số: SBP {sbp_val} mmHg, HR {hr_val} bpm, LVEF {lvef_val}%, eGFR {egfr_val} mL/min)</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.subheader(f"📋 Đề xuất điều trị theo kiểu hình: {phenotype}")
                
                if phenotype == "Co thắt mạch vành (ANOCA - VSA)":
                    st.markdown("""
                    - **Bước 1 (Đầu tay):** <span class='class-badge-1'>Class I A</span> **Chẹn kênh Canxi (CCB)** được khuyến cáo để kiểm soát triệu chứng, phòng thiếu máu cơ tim và biến chứng có thể gây tử vong ở đau thắt ngực do co thắt.
                    - **Bước 2 (Phối hợp):** <span class='class-badge-2a'>Class IIa B</span> **Nitrates** nên được cân nhắc để phòng các cơn tái phát.
                    - **⚠️ Lưu ý:** Chẹn beta không phải điều trị đích cho co thắt mạch vành và có thể làm nặng co thắt ở một số bệnh nhân; tuy nhiên ESC 2024 không gán một khuyến cáo “Class III tuyệt đối” cho mọi trường hợp dùng chẹn beta đơn trị trong VSA.
                    """, unsafe_allow_html=True)
                    apply_target = ["Chẹn kênh Canxi DHP (DHP-CCB)"]
                elif phenotype == "Đau thắt ngực vi mạch (ANOCA - MVA)":
                    st.markdown("""
                    - **Điều trị theo endotype:** <span class='class-badge-2a'>Class IIa A</span> Ở ANOCA/INOCA có triệu chứng, nên cân nhắc điều trị dựa trên kết quả coronary functional testing để cải thiện triệu chứng và chất lượng cuộc sống.
                    - **MVA với giảm CFR/tăng IMR:** <span class='class-badge-2a'>Class IIa B</span> Nên cân nhắc thuốc chống đau ngực hướng đến giảm thiếu máu cơ tim do tăng nhu cầu. Trong phần thảo luận ESC 2024, **beta-blocker, CCB và ranolazine** là các lựa chọn thường được sử dụng; guideline không gán Class IIa B riêng cho từng thuốc này.
                    - **Rối loạn chức năng nội mô:** <span class='class-badge-2a'>Class IIa B</span> **ACE-I** nên được cân nhắc để kiểm soát triệu chứng.
                    - Điều trị yếu tố nguy cơ (lipid, huyết áp, hút thuốc, đái tháo đường) vẫn cần được tối ưu theo guideline.
                    """, unsafe_allow_html=True)
                    apply_target = ["Chẹn beta (Beta-blockers - BB)", "Chẹn kênh Canxi DHP (DHP-CCB)"]
                elif phenotype == "Rối loạn chức năng thất trái / Suy tim giảm LVEF ≤ 40%":
                    st.markdown("""
                    - **Điều trị nền:** Ưu tiên thuốc phù hợp với HFrEF và hồ sơ huyết động của người bệnh; khi dùng beta-blocker cho mục tiêu chống đau ngực, mục tiêu nhịp nghỉ thường khoảng 55–60 bpm nếu dung nạp.
                    - **Ivabradine:** <span class='class-badge-2a'>Class IIa B</span> Nên được cân nhắc như thuốc chống đau ngực bổ sung ở bệnh nhân có **rối loạn chức năng tâm thu thất trái (LVEF <40%)** và triệu chứng chưa kiểm soát, hoặc trong điều trị ban đầu ở bệnh nhân được lựa chọn phù hợp.
                    - **Trimetazidine:** <span class='class-badge-2b'>Class IIb B</span> Có thể được cân nhắc như thuốc bổ sung khi triệu chứng chưa kiểm soát với beta-blocker/CCB hoặc trong điều trị ban đầu ở bệnh nhân được lựa chọn phù hợp.
                    - **Non-DHP CCB (verapamil/diltiazem):** tránh ở HFrEF do tác dụng giảm co bóp; đây là vấn đề an toàn/đặc tính thuốc, không nên gắn nhãn Class III chung nếu guideline không nêu như một Recommendation Table tương ứng.
                    """, unsafe_allow_html=True)
                    apply_target = ["Chẹn beta (Beta-blockers - BB)"]
                elif phenotype == "Tần số tim nhanh (HR > 80 nhịp/phút)":
                    st.markdown("""
                    - **Bước 1 (Đầu tay):** <span class='class-badge-1'>Class I B</span> Khởi trị bằng **Chẹn beta (BB)** hoặc **Chẹn kênh canxi Non-DHP** để giảm nhịp tim lúc nghỉ về mốc 55-60 nhịp/phút.
                    - **Bước 2 (Phối hợp):** <span class='class-badge-2a'>Class IIa B</span> Phối hợp **Chẹn beta (BB) + Chẹn kênh canxi DHP (Amlodipine)** khi đau ngực chưa kiểm soát tốt.
                    - **Bước 3 (Phối hợp thêm):**
                        * Phối hợp thêm **Ranolazine** HOẶC **Nitrates tác dụng kéo dài** (<span class='class-badge-2a'>Class IIa B</span>).
                        * Phối hợp thêm **Trimetazidine MR** HOẶC **Nicorandil** (<span class='class-badge-2b'>Class IIb B</span>).
                        * **🚨 KHÔNG KHUYẾN CÁO (Class III B):** Không dùng Ivabradine add-on cho bệnh nhân CCS có LVEF >40% và không có suy tim lâm sàng.
                    """, unsafe_allow_html=True)
                    apply_target = ["Chẹn beta (Beta-blockers - BB)", "Chẹn kênh Canxi DHP (DHP-CCB)"]
                elif phenotype == "Tần số tim chậm (HR < 55 nhịp/phút)":
                    st.markdown("""
                    - **Bước 1 (Đầu tay):** <span class='class-badge-1'>Class I B</span> Khởi trị bằng **Chẹn kênh canxi DHP (DHP-CCB)** (như Amlodipine) do tác dụng giãn mạch chống đau thắt ngực độc lập với nhịp tim.
                    - **Bước 2 (Phối hợp):** 
                        * Phối hợp thêm **Ranolazine** HOẶC **Nitrates tác dụng kéo dài** (<span class='class-badge-2a'>Class IIa B</span>).
                        * Phối hợp thêm **Trimetazidine MR** HOẶC **Nicorandil** (<span class='class-badge-2b'>Class IIb B</span>).
                    - **⚠️ Cảnh báo thận trọng:** Chống chỉ định dùng thuốc làm giảm nhịp tim thêm (Chẹn Beta, Non-DHP CCB, Ivabradine).
                    """, unsafe_allow_html=True)
                    apply_target = ["Chẹn kênh Canxi DHP (DHP-CCB)"]
                elif phenotype == "Huyết áp thấp (SBP < 95 mmHg)":
                    st.markdown("""
                    - **Bước 1 (Đầu tay):** 
                        * **Chẹn beta (BB)** liều thấp chỉ khởi trị nếu nhịp nhanh VÀ kèm theo suy tim/LVEF ≤ 40% (<span class='class-badge-1'>Class I A</span>).
                        * Nếu LVEF > 40% không kèm suy tim, ưu tiên sử dụng các thuốc chống đau ngực không gây hạ áp như **Ranolazine** (<span class='class-badge-2a'>Class IIa B</span>) hoặc **Trimetazidine MR** (<span class='class-badge-2b'>Class IIb B</span>).
                    - **Bước 2 (Phối hợp):** Nếu nhịp xoang ≥ 70 bpm VÀ LVEF ≤ 40%: Có thể phối hợp thêm **Ivabradine** (<span class='class-badge-2a'>Class IIa B</span>).
                    - **🚨 KHÔNG KHUYẾN CÁO (Class III B):** Không dùng Ivabradine add-on cho bệnh nhân CCS có LVEF >40% và không có suy tim lâm sàng.
                    - **⚠️ Thận trọng rất cao:** Tránh dùng các thuốc giãn mạch hạ áp mạnh như CCB liều cao, LA Nitrates, Nicorandil.
                    """, unsafe_allow_html=True)
                    apply_target = ["Ranolazine"]
                else: # Standard Profile
                    st.markdown("""
                    - **Bước 1 (Đầu tay):** <span class='class-badge-1'>Class I B</span> Khởi trị bằng **Chẹn beta (BB)** hoặc **Chẹn kênh Canxi (CCB)** để kiểm soát đau ngực.
                    - **Bước 2 (Phối hợp):** <span class='class-badge-2a'>Class IIa B</span> Phối hợp **Chẹn beta (BB) + Chẹn kênh canxi DHP (DHP-CCB)** khi đơn trị liệu chưa kiểm soát tốt triệu chứng.
                    - **Bước 3 (Phối hợp thêm):**
                        * Phối hợp thêm **Ranolazine** HOẶC **Nitrates tác dụng kéo dài** (<span class='class-badge-2a'>Class IIa B</span>).
                        * Phối hợp thêm **Trimetazidine MR** HOẶC **Nicorandil** (<span class='class-badge-2b'>Class IIb B</span>).
                        * **🚨 KHÔNG KHUYẾN CÁO (Class III B):** Không dùng Ivabradine add-on cho bệnh nhân CCS có LVEF >40% và không có suy tim lâm sàng.
                    """, unsafe_allow_html=True)
                    apply_target = ["Chẹn beta (Beta-blockers - BB)", "Chẹn kênh Canxi DHP (DHP-CCB)"]
                    
                if st.button("👉 ÁP DỤNG PHÁC ĐỒ KHUYẾN NGHỊ NÀY", key="apply_advisor_btn"):
                    mapped_targets = []
                    for t in apply_target:
                        if "Beta-blockers" in t or "BB" in t: mapped_targets.append("Chẹn beta (Beta-blockers - BB)")
                        elif "DHP-CCB" in t: mapped_targets.append("Chẹn kênh Canxi DHP (DHP-CCB)")
                        elif "Ranolazine" in t: mapped_targets.append("Ranolazine")
                    st.session_state.selected_drugs_val = mapped_targets
                    st.session_state.prescribing_mode_val = "🛠️ Tự phối hợp và tra cứu"
                    st.success("✅ Đã áp dụng phác đồ! Hệ thống đã chuyển đổi sang hộp tự phối hợp.")
                    st.rerun()
                    
            # 2. Manual Mode (Tự phối hợp & Tra cứu)
            else:
                st.markdown("#### Lựa chọn thuốc Kê đơn & Tra cứu Chống chỉ định chi tiết")
                
                if 'selected_drugs_val' not in st.session_state:
                    st.session_state.selected_drugs_val = []
                    
                with st.container(border=True):
                    selected_drugs = st.multiselect(
                        "Chọn một hoặc nhiều nhóm thuốc chống đau thắt ngực để phối hợp và xem chống chỉ định động:",
                        options=[
                            "Chẹn beta (Beta-blockers - BB)",
                            "Chẹn kênh Canxi DHP (DHP-CCB)",
                            "Chẹn kênh Canxi Non-DHP (Non-DHP CCB)",
                            "Nitrates tác dụng kéo dài (Long-acting Nitrates)",
                            "Ivabradine",
                            "Ranolazine",
                            "Trimetazidine MR",
                            "Nicorandil"
                        ],
                        default=st.session_state.selected_drugs_val
                    )
                    st.session_state.selected_drugs_val = selected_drugs
                    
                    prescribe_bb = "Chẹn beta (Beta-blockers - BB)" in selected_drugs
                    prescribe_dhp_ccb = "Chẹn kênh Canxi DHP (DHP-CCB)" in selected_drugs
                    prescribe_non_dhp_ccb = "Chẹn kênh Canxi Non-DHP (Non-DHP CCB)" in selected_drugs
                    prescribe_la_nitrate = "Nitrates tác dụng kéo dài (Long-acting Nitrates)" in selected_drugs
                    prescribe_ivabradine = "Ivabradine" in selected_drugs
                    prescribe_ranolazine = "Ranolazine" in selected_drugs
                    prescribe_trimetazidine = "Trimetazidine MR" in selected_drugs
                    prescribe_nicorandil = "Nicorandil" in selected_drugs
                    
                    if selected_drugs:
                        st.markdown("##### 🔍 Chi tiết Chống chỉ định & Thận trọng của các thuốc đã chọn:")
                        
                        if prescribe_bb:
                            with st.expander("📖 Chống chỉ định & Thận trọng của Chẹn Beta (BB)", expanded=True):
                                st.markdown("""
                                - **❌ Không phù hợp/chống chỉ định theo hồ sơ an toàn thuốc:** Nhịp tim chậm rõ, block AV độ II–III khi chưa có máy tạo nhịp, hội chứng suy nút xoang hoặc suy tim mất bù cấp. Đây là cảnh báo an toàn thuốc, không phải một ESC Class III chung cho toàn bộ nhóm beta-blocker.
                                - **⚠️ Thận trọng quan trọng:** Hen phế quản nặng hoặc bệnh phổi tắc nghẽn mạn tính (COPD) có co thắt phế quản tiến triển (ưu tiên chọn chẹn beta siêu chọn lọc tim).
                                """)
                        if prescribe_dhp_ccb:
                            with st.expander("📖 Chống chỉ định & Thận trọng của Chẹn kênh Canxi DHP (DHP-CCB)", expanded=True):
                                st.markdown("""
                                - **❌ Chống chỉ định/thận trọng theo hồ sơ an toàn thuốc:** Hạ huyết áp nặng hoặc hẹp van động mạch chủ khít có triệu chứng. Không gắn nhãn ESC Class III nếu không có Recommendation Table tương ứng.
                                - **⚠️ Thận trọng quan trọng:** Nguy cơ gây phù ngoại biên vùng cổ chân ở liều cao (10mg).
                                """)
                        if prescribe_non_dhp_ccb:
                            with st.expander("📖 Chống chỉ định & Thận trọng của Chẹn kênh Canxi Non-DHP (Verapamil / Diltiazem)", expanded=True):
                                st.markdown("""
                                - **❌ Tránh/không phù hợp theo hồ sơ an toàn thuốc:** HFrEF/LVEF giảm rõ, nhịp chậm đáng kể, hội chứng suy nút xoang hoặc block AV độ II–III khi chưa có máy tạo nhịp.
                                - **⚠️ Phối hợp với beta-blocker:** không phải chống chỉ định ESC Class III tuyệt đối trong mọi tình huống; cần cá thể hóa và theo dõi chặt nhịp tim/dẫn truyền vì nguy cơ nhịp chậm và block AV.
                                - **❌ Phối hợp với Ivabradine:** ESC 2024 **không khuyến cáo (Class III B)**.
                                """)
                        if prescribe_la_nitrate:
                            with st.expander("📖 Chống chỉ định & Thận trọng của Long-acting Nitrates", expanded=True):
                                st.markdown("""
                                - **❌ ESC 2024 — không khuyến cáo (Class III B):**
                                    * Dùng nitrate đồng thời với **PDE-5 inhibitor**.
                                    * Dùng nitrate ở bệnh nhân **bệnh cơ tim phì đại (HCM)**.
                                - **⚠️ Khi dùng nitrate tác dụng kéo dài:** nên có khoảng không nitrate/ít nitrate để giảm hiện tượng dung nạp thuốc (**Class IIa B**).
                                """)
                        if prescribe_ivabradine:
                            with st.expander("📖 Chống chỉ định & Thận trọng của Ivabradine", expanded=True):
                                st.markdown("""
                                - **❌ ESC 2024 — không khuyến cáo (Class III B):**
                                    * Ivabradine add-on ở bệnh nhân **CCS, LVEF >40% và không có suy tim lâm sàng**.
                                    * Phối hợp Ivabradine với **Verapamil/Diltiazem (non-DHP CCB)** hoặc các chất ức chế CYP3A4 mạnh.
                                - **⚠️ Theo hồ sơ an toàn thuốc:** cần nhịp xoang và phải tránh ở nhịp chậm rõ hoặc rung/cuồng nhĩ không phù hợp với cơ chế tác dụng của thuốc.
                                """)
                        if prescribe_ranolazine:
                            with st.expander("📖 Chống chỉ định & Thận trọng của Ranolazine", expanded=True):
                                st.markdown("""
                                - **❌ CHỐNG CHỈ ĐỊNH THEO NHÃN THUỐC (Drug-label Contraindication):**
                                    * **Suy thận nặng với mức lọc cầu thận eGFR < 30 mL/min**.
                                    * Suy gan nặng hoặc trung bình.
                                    * Phối hợp với thuốc ức chế mạnh men gan CYP3A4 (Ketoconazole, Clarithromycin...).
                                """)
                        if prescribe_trimetazidine:
                            with st.expander("📖 Chống chỉ định & Thận trọng của Trimetazidine MR", expanded=True):
                                st.markdown("""
                                - **❌ CHỐNG CHỈ ĐỊNH THEO NHÃN THUỐC (Drug-label Contraindication):**
                                    * **Bệnh nhân mắc bệnh Parkinson**, có các triệu chứng Parkinson, run, hội chứng chân không yên, hoặc các rối loạn vận động ngoại tháp đi kèm.
                                    * **Suy thận nặng với mức lọc cầu thận eGFR < 30 mL/min** (độc tính tích lũy thuốc gây run tay).
                                """)
                        if prescribe_nicorandil:
                            with st.expander("📖 Chống chỉ định & Thận trọng của Nicorandil", expanded=True):
                                st.markdown("""
                                - **❌ Chống chỉ định theo hồ sơ an toàn thuốc:** Shock tim hoặc tụt huyết áp nặng.
                                - **⚠️ Thận trọng quan trọng:** **Nguy cơ gây loét nghiêm trọng:** Nicorandil có thể gây ra các vết loét niêm mạc dạ dày - tá tràng, loét da, loét giác mạc khó lành. Ngừng thuốc nếu xuất hiện loét nghiêm trọng theo thông tin an toàn thuốc; không gán Class I A của ESC cho cảnh báo này.
                                """)
                                
                        # INTERACTION AND COMPATIBILITY RESULTS
                        st.markdown("##### 🚨 Đánh giá Tương tác phối hợp & An toàn tự động:")
                        safety_alerts = []
                        success_alerts = []
                        
                        # Rule 1: Non-DHP + HFrEF (LVEF <= 40)
                        if prescribe_non_dhp_ccb and lvef_val <= 40:
                            safety_alerts.append(f"""
                            <div class='warning-box'>
                                <h5 style='color: #c0392b; margin: 0; font-weight: bold;'>❌ CHỐNG CHỈ ĐỊNH LÂM SÀNG (LVEF ≤ 40% - Drug-label Contraindication)</h5>
                                <strong>Non-DHP CCB ở bệnh nhân LVEF ≤ 40% ({lvef_val}%):</strong><br>
                                - Nhóm thuốc này có tính co bóp cơ tim âm tính mạnh, chống chỉ định tuyệt đối ở LVEF ≤ 40% do nguy cơ suy tim cấp tiến triển.
                            </div>
                            """)
                        # Rule 2: BB + Non-DHP CCB
                        if prescribe_bb and prescribe_non_dhp_ccb:
                            safety_alerts.append("""
                            <div class='warning-box' style='border-left-color: #fd7e14;'>
                                <h5 style='color: #fd7e14; margin: 0; font-weight: bold;'>⚠️ THẬN TRỌNG LÂM SÀNG CAO (Clinical Caution)</h5>
                                <strong>Phối hợp Chẹn beta (BB) + Non-DHP CCB (Verapamil/Diltiazem):</strong><br>
                                - Đây không phải là chống chỉ định tuyệt đối Class III của ESC, nhưng đòi hỏi **Thận trọng đặc biệt nghiêm ngặt** trên từng cá thể do nguy cơ cao gây nhịp chậm nặng, ngừng xoang, block nhĩ thất độ cao.<br>
                                - <strong>Giải pháp phối hợp thay thế tối ưu (Class IIa B):</strong> Nên phối hợp <strong>Chẹn beta + Chẹn kênh Canxi nhóm DHP (Amlodipine)</strong> là lựa chọn phối hợp chuẩn, an toàn hơn.
                            </div>
                            """)
                        # Rule 3: Ivabradine + Non-DHP CCB
                        if prescribe_ivabradine and prescribe_non_dhp_ccb:
                            safety_alerts.append("""
                            <div class='warning-box'>
                                <h5 style='color: #c0392b; margin: 0; font-weight: bold;'>❌ KHÔNG KHUYẾN CÁO PHỐI HỢP (Class III B)</h5>
                                <strong>Phối hợp Ivabradine + Non-DHP CCB:</strong><br>
                                - Làm tăng mạnh nồng độ Ivabradine trong máu qua ức chế CYP3A4, gây nhịp tim chậm nghiêm trọng đe dọa tính mạng.
                            </div>
                            """)
                        # Rule 4: Renal impairment + Trimetazidine/Ranolazine
                        if egfr_val < 30:
                            if prescribe_trimetazidine:
                                safety_alerts.append(f"""
                                <div class='warning-box'>
                                    <h5 style='color: #c0392b; margin: 0; font-weight: bold;'>❌ CHỐNG CHỈ ĐỊNH THEO NHÃN THUỐC (Drug-label Contraindication)</h5>
                                    <strong>Trimetazidine ở bệnh nhân eGFR < 30 mL/min ({egfr_val} mL/min):</strong><br>
                                    - Suy thận nặng làm giảm đào thải gây tích lũy độc tính thần kinh (gây run tay ngoại tháp).
                                </div>
                                """)
                            if prescribe_ranolazine:
                                safety_alerts.append(f"""
                                <div class='warning-box'>
                                    <h5 style='color: #c0392b; margin: 0; font-weight: bold;'>❌ CHỐNG CHỈ ĐỊNH THEO NHÃN THUỐC (Drug-label Contraindication)</h5>
                                    <strong>Ranolazine ở bệnh nhân eGFR < 30 mL/min ({egfr_val} mL/min):</strong><br>
                                    - Tích lũy thuốc và các chất chuyển hóa làm tăng mạnh nguy cơ kéo dài khoảng QT và khởi phát xoắn đỉnh nguy hiểm.
                                </div>
                                """)
                        # Rule 5: Bradycardia Warning (HR < 55)
                        if hr_val < 55 and (prescribe_bb or prescribe_non_dhp_ccb or prescribe_ivabradine):
                            safety_alerts.append(f"""
                            <div class='warning-box' style='border-left-color: #f1c40f;'>
                                <h5 style='color: #d4ac0d; margin: 0; font-weight: bold;'>⚠️ THẬN TRỌNG - BỆNH NHÂN ĐANG NHỊP CHẬM (HR = {hr_val} bpm)</h5>
                                - Dùng các thuốc giảm nhịp (Chẹn Beta, Non-DHP CCB, Ivabradine) có nguy cơ gây ngừng tim hoặc block AV độ cao.<br>
                                - **Gợi ý:** Nên ưu tiên chọn **Ranolazine** hoặc **Trimetazidine** (không ảnh hưởng lên tần số tim lúc nghỉ).
                            </div>
                            """)
                        # Rule 6: Hypotension Warning (SBP < 95)
                        if sbp_val < 95 and (prescribe_bb or prescribe_dhp_ccb or prescribe_non_dhp_ccb or prescribe_la_nitrate or prescribe_nicorandil):
                            safety_alerts.append(f"""
                            <div class='warning-box' style='border-left-color: #f1c40f;'>
                                <h5 style='color: #d4ac0d; margin: 0; font-weight: bold;'>⚠️ THẬN TRỌNG - BỆNH NHÂN ĐANG HUYẾT ÁP THẤP (SBP = {sbp_val} mmHg)</h5>
                                - Huyết áp tâm thu nền đang thấp. Các thuốc được chọn có hoạt tính giãn mạch mạnh gây tụt huyết áp sâu hơn.<br>
                                - **Gợi ý:** Nên ưu tiên chọn **Ranolazine**, **Trimetazidine** (không gây hạ áp) hoặc **Ivabradine** (chỉ giảm nhịp, không giảm huyết áp).
                            </div>
                            """)
                        # Rule 7: COPD/Asthma with Beta-blocker
                        if pft_abnormal and prescribe_bb:
                            safety_alerts.append("""
                            <div class='warning-box' style='border-left-color: #f1c40f;'>
                                <h5 style='color: #d4ac0d; margin: 0; font-weight: bold;'>⚠️ THẬN TRỌNG - BỆNH LÝ HÔ HẤP CO THẮT (COPD / Hen)</h5>
                                - Chẹn beta có nguy cơ co thắt phế quản. Nên chọn Chẹn beta siêu chọn lọc tim (như <strong>Bisoprolol</strong> hoặc <strong>Metoprolol Succinate</strong>) ở liều thấp và tăng liều chậm.
                            </div>
                            """)
                        # Rule 8: Vasospastic Angina with Beta-blocker monotherapy
                        if phenotype == "Co thắt mạch vành (ANOCA - VSA)" and prescribe_bb and not (prescribe_dhp_ccb or prescribe_non_dhp_ccb):
                            safety_alerts.append("""
                            <div class='warning-box' style='border-left-color: #fd7e14;'>
                                <h5 style='color: #fd7e14; margin: 0; font-weight: bold;'>⚠️ KHÔNG PHẢI ĐIỀU TRỊ ĐÍCH CHO VSA</h5>
                                <strong>Chẹn beta đơn trị ở bệnh nhân co thắt mạch (VSA):</strong><br>
                                - Có thể làm nặng co thắt ở một số bệnh nhân và không phải lựa chọn điều trị đích. ESC 2024 khuyến cáo CCB là điều trị hàng đầu cho VSA; không gán một Class III tuyệt đối cho mọi trường hợp chẹn beta đơn trị.
                            </div>
                            """)
                        # Rule 9: Standard Optimal combo (Class IIa B)
                        if prescribe_bb and prescribe_dhp_ccb and not prescribe_non_dhp_ccb:
                            success_alerts.append("""
                            <div class='success-box' style='background-color: #e8f8f5; border-left: 5px solid #2ecc71; padding: 10px; margin-bottom: 10px;'>
                                <span class='class-badge-2a'>Class IIa B</span> <strong>Phối hợp thuốc: Chẹn beta (BB) + Chẹn kênh Canxi DHP:</strong><br>
                                - Đây là phối hợp hữu ích hàng đầu khi Chẹn beta hoặc DHP-CCB đơn trị liệu không kiểm soát tốt triệu chứng đau thắt ngực (Class IIa B).
                            </div>
                            """)
                            
                        if safety_alerts:
                            for alert in safety_alerts: st.markdown(alert, unsafe_allow_html=True)
                        elif success_alerts:
                            for s_alert in success_alerts: st.markdown(s_alert, unsafe_allow_html=True)
                        else:
                            st.success("✅ **Đánh giá phối hợp:** Phối hợp thuốc an toàn, không phát hiện tương tác chống chỉ định hoặc cảnh báo đỏ nào.")
                    else:
                        st.info("💡 Vui lòng chọn một hoặc nhiều nhóm thuốc ở hộp trên để tự động phân tích an toàn kê đơn.")

        st.write("")
        # 3. Dynamic Titration and Dosage reference dictionary (Format without raw HTML tags like <br>)
        st.markdown("#### 3. Bảng tra cứu liều lượng chi tiết và chống chỉ định các thuốc thường gặp:")
        with st.expander("📖 Xem bảng tra cứu liều lượng chi tiết (8 nhóm thuốc)", expanded=False):
            st.markdown("""
            | Nhóm thuốc | Thuốc thường gặp (Tên biệt dược) | Liều khởi đầu khuyến cáo | Liều đích mục tiêu | Chống chỉ định chính & Cảnh báo |
            | :--- | :--- | :--- | :--- | :--- |
            | **1. Chẹn Beta (BB)** | Metoprolol Succinate (Betaloc Zok), Bisoprolol (Concor), Carvedilol (Dilatrend) | 25 - 50 mg q.d. / 2.5 - 5 mg q.d. / 6.25 mg b.i.d. | 100 - 200 mg q.d. / 10 - 20 mg q.d. / 25 - 50 mg b.i.d. | Suy nút xoang, block nhĩ thất độ II, III, nhịp chậm (HR < 50), suy tim mất bù. Thận trọng với Hen/COPD. Đích nhịp tim lúc nghỉ: 55-60 nhịp/phút. |
            | **2. DHP-CCB** | Amlodipine (Amlor), Felodipine (Plendil) | 5 mg q.d. | 10 mg q.d. | Huyết áp thấp nặng (SBP < 90), hẹp khít van động mạch chủ lơn, phù ngoại biên nặng. |
            | **3. Non-DHP CCB** | Verapamil (Isoptin), Diltiazem (Herbesser) | 120 - 240 mg/ngày / 120 - 180 mg/ngày | 360 - 480 mg/ngày / 360 mg/ngày | Tránh ở HFrEF/LVEF giảm rõ, nhịp chậm, block nhĩ thất, suy nút xoang. Phối hợp với Chẹn beta cần thận trọng và theo dõi dẫn truyền; phối hợp với Ivabradine không được khuyến cáo (Class III B). |
            | **4. LA Nitrates** | Isosorbide Mononitrate (Imdur), Isosorbide Dinitrate | 30 mg q.d. / 10 mg b.i.d. | 60 - 120 mg q.d. / 40 mg t.i.d. | Không khuyến cáo ở HCM hoặc dùng đồng thời PDE-5i (Class III B). Khi dùng kéo dài, nên có khoảng không/ít nitrate để giảm dung nạp thuốc (Class IIa B). |
            | **5. Ivabradine** | Ivabradine (Procoralan) | 5 mg b.i.d. (2.5mg nếu nhịp chậm) | 7.5 mg b.i.d. | Không khuyến cáo add-on khi CCS, LVEF >40% và không có HF (Class III B); không phối hợp với Non-DHP CCB/ức chế CYP3A4 mạnh (Class III B). Cần nhịp xoang để có tác dụng. |
            | **6. Ranolazine** | Ranolazine (Ranexa) | 375 mg b.i.d. | 500 - 1000 mg b.i.d. | Chống chỉ định ở eGFR < 30 mL/min, suy gan nặng, dùng chung chất ức chế CYP3A4 mạnh. Ưu điểm: Không ảnh hưởng nhịp tim và huyết áp. |
            | **7. Trimetazidine** | Trimetazidine MR (Vastarel MR) | 35 mg b.i.d. | 35 mg b.i.d. | Chống chỉ định ở bệnh Parkinson / rối loạn ngoại tháp, suy thận nặng (eGFR < 30 mL/min). |
            | **8. Nicorandil** | Nicorandil (Ikorel) | 10 mg b.i.d. | 20 - 30 mg b.i.d. | Shock tim, tụt huyết áp nặng. Nguy cơ gây loét đường tiêu hóa hoặc loét da nghiêm trọng (ngừng thuốc ngay nếu xuất hiện loét). |
            """)

    # Sub-step 4.2: Tối ưu hóa lipid máu
    if render_sub_header("Tối ưu hóa lipid máu", 2, "step4_sub"):
        st.subheader("2. Phân tích và điều chỉnh rối loạn lipid máu")
        
        ldlc_now = st.session_state.get('ldlc_val_mmol', 3.0)
        tg_now = st.session_state.get('tg_val_mmol', 1.8)
        lpa_now = st.session_state.get('lpa_val', 0)
        
        st.info(f"Dữ liệu xét nghiệm đã nhập: LDL-C = **{ldlc_now:.2f} mmol/L** ({ldlc_now*38.67:.1f} mg/dL) | Triglycerides = **{tg_now:.2f} mmol/L** ({tg_now*88.57:.1f} mg/dL)")
        
        st.markdown("""
        <div class='recommendation-box' style='padding: 10px; margin-bottom: 15px;'>
            <strong>PHÂN LOẠI NGUY CƠ TIM MẠCH:</strong> Bệnh nhân đã được xác định mắc hội chứng vành mạn (CCS) thuộc nhóm nguy cơ tim mạch rất cao (Very High Cardiovascular Risk). ESC/EAS Focused Update 2025 tiếp tục xếp CCS trong nhóm ASCVD đã xác định.
        </div>
        """, unsafe_allow_html=True)
        
        recurrent_event = st.checkbox("Bệnh nhân có biến cố xơ vữa thứ hai trong vòng 2 năm khi đang dùng liệu pháp statin dung nạp tối đa?", key="lipid_recurrent_chk_v8")
        
        # Determine targets
        if recurrent_event:
            target_ldlc_mmol = 1.0
            target_ldlc_mg = 40
            target_class_badge = "<span class='class-badge-2b'>Class IIb B</span>"
        else:
            target_ldlc_mmol = 1.4
            target_ldlc_mg = 55
            target_class_badge = "<span class='class-badge-1'>Class I A</span>"
            
        st.markdown(f"""
        #### 🎯 Mục tiêu LDL-C cần đạt:
        - **Nồng độ đích:** {target_class_badge} **< {target_ldlc_mmol} mmol/L** (< {target_ldlc_mg} mg/dL).
        - **Tỷ lệ giảm:** Giảm **≥ 50%** so với nồng độ LDL-C nền khi chưa bắt đầu điều trị.
        """, unsafe_allow_html=True)
        
        st.markdown("#### ⚙️ Lộ trình Phối hợp Thuốc Hạ Lipid (Stepwise Therapy Escalation)")
        current_therapy = st.selectbox(
            "Phác đồ hạ lipid hiện tại của bệnh nhân:",
            ["Chưa điều trị bằng thuốc hạ lipid máu",
             "Đang dùng Statin cường độ trung bình (Atorvastatin 10-20mg, Rosuvastatin 5-10mg)",
             "Đang dùng Statin cường độ cao (Atorvastatin 40-80mg, Rosuvastatin 20-40mg) ở liều tối đa dung nạp",
             "Đang dùng phối hợp Statin tối đa + Ezetimibe 10mg",
             "Đang dùng phối hợp 3 thuốc (Statin tối đa + Ezetimibe + PCSK9 monoclonal antibody)",
             "Bệnh nhân hoàn toàn Kém dung nạp với Statin (Statin Intolerance)"]
        )
        
        is_at_target = ldlc_now < target_ldlc_mmol
        if is_at_target:
            st.success(f"🎉 **Chúc mừng!** Bệnh nhân đã đạt mục tiêu LDL-C (< {target_ldlc_mmol} mmol/L). Khuyên dùng duy trì phác đồ và tái khám định kỳ 6-12 tháng.")
        else:
            st.error(f"❌ **Chưa đạt mục tiêu!** LDL-C hiện tại ({ldlc_now:.2f} mmol/L) cao hơn mục tiêu điều trị đích (< {target_ldlc_mmol} mmol/L).")
            
            st.markdown("##### 📌 Khuyến cáo hạ LDL-C theo ESC CCS 2024 + ESC/EAS Focused Update 2025:")
            if current_therapy == "Chưa điều trị bằng thuốc hạ lipid máu":
                st.markdown(f"""
                1. <span class='class-badge-1'>Class I A</span> Khởi trị ngay **Statin cường độ cao** (như Atorvastatin 40-80mg hoặc Rosuvastatin 20-40mg) đến liều tối đa mà bệnh nhân có thể dung nạp được.
                2. Đánh giá lại LDL-C sau **4 - 6 tuần**. Nếu chưa đạt mục tiêu, phối hợp thêm Ezetimibe 10mg.
                """, unsafe_allow_html=True)
            elif current_therapy == "Đang dùng Statin cường độ trung bình (Atorvastatin 10-20mg, Rosuvastatin 5-10mg)":
                st.markdown(f"""
                1. <span class='class-badge-1'>Class I A</span> Tối đa hóa liều Statin: **Tăng liều** lên Rosuvastatin 20-40mg hoặc Atorvastatin 40-80mg hàng ngày.
                2. Đánh giá lại sau 4-6 tuần. Nếu chưa đạt, tiếp tục phối hợp Ezetimibe 10mg.
                """, unsafe_allow_html=True)
            elif current_therapy == "Đang dùng Statin cường độ cao (Atorvastatin 40-80mg, Rosuvastatin 20-40mg) ở liều tối đa dung nạp":
                st.markdown(f"""
                1. <span class='class-badge-1'>Class I B</span> Phối hợp thêm **Ezetimibe 10mg** hàng ngày ngay lập tức.
                2. Kiểm tra lại sau 4-6 tuần để đánh giá tính dung nạp và mục tiêu đạt được.
                """, unsafe_allow_html=True)
            elif current_therapy == "Đang dùng phối hợp Statin tối đa + Ezetimibe 10mg":
                st.markdown(f"""
                1. <span class='class-badge-1'>Class I A</span> Nếu vẫn chưa đạt LDL-C đích, phối hợp thêm **PCSK9 monoclonal antibody có bằng chứng biến cố tim mạch** — **Alirocumab hoặc Evolocumab**.
                2. <span class='class-badge-2a'>Class IIa C</span> **Bempedoic acid** có thể được cân nhắc thêm vào statin dung nạp tối đa, có hoặc không kèm ezetimibe, ở bệnh nhân nguy cơ cao/rất cao chưa đạt đích.
                3. **Inclisiran:** có hiệu quả hạ LDL-C khoảng 50%, nhưng trong Focused Update 2025 các thử nghiệm kết cục tim mạch vẫn đang tiến hành; **không gắn cùng Class I A về giảm biến cố như alirocumab/evolocumab**.
                """, unsafe_allow_html=True)
            elif current_therapy == "Đang dùng phối hợp 3 thuốc (Statin tối đa + Ezetimibe + PCSK9 monoclonal antibody)":
                st.markdown("""
                1. Rà soát tuân thủ, liều tối đa dung nạp và các nguyên nhân thứ phát khiến LDL-C còn cao.
                2. <span class='class-badge-2a'>Class IIa C</span> Có thể cân nhắc thêm **Bempedoic acid** nếu vẫn chưa đạt mục tiêu và phù hợp lâm sàng.
                3. **Inclisiran** là một lựa chọn hạ LDL-C khác, nhưng không nên mô tả là tương đương PCSK9 monoclonal antibody về bằng chứng giảm biến cố tim mạch trong Focused Update 2025.
                """, unsafe_allow_html=True)
            else: # Statin Intolerance
                st.markdown(f"""
                1. <span class='class-badge-1'>Class I A</span> Ở bệnh nhân không thể dùng statin, nên sử dụng **liệu pháp non-statin có bằng chứng lợi ích tim mạch**, đơn trị hoặc phối hợp; lựa chọn dựa vào mức LDL-C cần giảm (Ezetimibe, PCSK9 monoclonal antibody, Bempedoic acid).
                2. <span class='class-badge-1'>Class I B</span> **Bempedoic acid** được khuyến cáo ở bệnh nhân không thể dùng statin để đạt mục tiêu LDL-C.
                3. Theo dõi đáp ứng LDL-C sau khởi trị/tăng cường điều trị, thông thường sau **4–6 tuần**.
                """, unsafe_allow_html=True)

        # Triglycerides Management
        st.markdown("#### 📈 Quản lý Triglyceride tăng cao")
        if 1.52 <= tg_now <= 5.63:
            st.warning(f"Triglyceride hiện tại: **{tg_now:.2f} mmol/L** ({tg_now*88.57:.0f} mg/dL).")
            st.markdown("""
            * <span class='class-badge-2a'>Class IIa B</span> Ở bệnh nhân **nguy cơ cao/rất cao** đang điều trị statin, **Icosapent Ethyl tinh khiết liều 2 g x 2 lần/ngày** nên được cân nhắc khi TG lúc đói 1,52–5,63 mmol/L (135–499 mg/dL) để giảm biến cố tim mạch.
            * Không đồng nhất khuyến cáo này với các chế phẩm **omega-3 EPA+DHA** nói chung; Focused Update 2025 nêu STRENGTH không chứng minh lợi ích biến cố với hỗn hợp EPA+DHA.
            """, unsafe_allow_html=True)
        elif tg_now > 5.63:
            st.warning(f"Triglyceride hiện tại **{tg_now:.2f} mmol/L** nằm ngoài khoảng 1,52–5,63 mmol/L của khuyến cáo Icosapent Ethyl để giảm biến cố tim mạch.")
            st.markdown("""
            * Không tự động ngoại suy khuyến cáo Icosapent Ethyl hoặc ghi chung “omega-3 liều cao” cho tình huống này.
            * Cần đánh giá nguyên nhân và xử trí tăng triglyceride nặng theo bối cảnh lâm sàng. Riêng **familial chylomicronaemia syndrome (FCS) đã xác định** với TG >8,5 mmol/L (>750 mg/dL), **Volanesorsen 300 mg/tuần nên được cân nhắc (Class IIa B)** theo Focused Update 2025.
            """, unsafe_allow_html=True)
        else:
            st.info(f"Triglyceride hiện tại: **{tg_now:.2f} mmol/L** — dưới ngưỡng 1,52 mmol/L của khuyến cáo Icosapent Ethyl trong Focused Update 2025.")

        # Lp(a) management — ESC/EAS Focused Update 2025
        if lpa_now >= 105:
            st.error(f"⚠️ **Lp(a) = {lpa_now} nmol/L:** đạt ngưỡng **risk-enhancing factor ≥105 nmol/L (≈50 mg/dL)** theo ESC/EAS 2025; nguy cơ tăng dần theo nồng độ Lp(a), vì vậy cần tối ưu kiểm soát các yếu tố nguy cơ tim mạch có thể thay đổi.")
        elif lpa_now >= 62:
            st.warning(f"ℹ️ **Lp(a) = {lpa_now} nmol/L:** chưa đạt ngưỡng risk-enhancing 105 nmol/L, nhưng dữ liệu trong Focused Update 2025 cho thấy nguy cơ tim mạch đã bắt đầu tăng nhẹ từ khoảng >62 nmol/L (≈30 mg/dL). Không nên gọi là “bình thường” tuyệt đối.")
        elif lpa_now > 0:
            st.info(f"Lp(a) = {lpa_now} nmol/L: chưa đạt ngưỡng risk-enhancing 105 nmol/L theo ESC/EAS 2025.")

    # Sub-step 4.3: Can thiệp mạch vành
    if render_sub_header("Can thiệp mạch vành", 3, "step4_sub"):
        if st.session_state.get('anoca_suspected', False):
            st.markdown(f"""
            <div class='warning-box' style='border-left-color: #c0392b; background-color: #fdf2f2;'>
                <h4 style='color: #c0392b; margin-top: 0;'>🚫 KHÔNG CÓ ĐÍCH TÁI THÔNG MẠCH THƯỢNG TÂM MẠC</h4>
                <p style='font-size: 1.05rem;'>Bệnh nhân thuộc phổ <strong>ANOCA/INOCA (Kiểu hình: {st.session_state.get('anoca_endotype', 'Chưa phân loại')})</strong> và không có tổn thương mạch vành thượng tâm mạc giới hạn dòng phù hợp để PCI/CABG.</p>
                <p style='margin-bottom: 0;'><strong>Hướng xử trí:</strong> tập trung vào điều trị nội khoa theo endotype, kiểm soát yếu tố nguy cơ và đánh giá lại triệu chứng. Không mô tả PCI/CABG là “chống chỉ định có hại” một cách tuyệt đối khi guideline không đưa ra kết luận như vậy.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.subheader("3. Chỉ định và lựa chọn Tái thông mạch vành (Revascularization)")

            is_high_risk = st.session_state.get('high_risk_flag', False)
            if is_high_risk:
                st.markdown("""
                <div class='warning-box' style='border-left-color: #fd7e14;'>
                    <h4 style='color: #fd7e14; margin-top: 0;'>🚨 HIGH EVENT-RISK → ICA + ĐÁNH GIÁ CHỨC NĂNG KHI PHÙ HỢP</h4>
                    <p>ESC 2024 khuyến cáo <strong>ICA, bổ sung FFR/iFR khi phù hợp (Class I A)</strong> ở người bệnh nguy cơ biến cố cao để làm rõ phân tầng nguy cơ và xác định chiến lược điều trị. <strong>High event-risk không tự động đồng nghĩa phải PCI/CABG để kéo dài sống còn.</strong></p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class='success-box' style='background-color: #e8f8f5; border-left-color: #2ecc71;'>
                    <h4 style='color: #2ecc71; margin-top: 0;'>✅ KHÔNG TỰ ĐỘNG CHỈ ĐỊNH TÁI THÔNG CHỈ DỰA TRÊN “HIGH-RISK FLAG”</h4>
                    <p>Quyết định tái thông phải dựa trên <strong>triệu chứng, ý nghĩa chức năng của tổn thương, giải phẫu mạch vành, LVEF, đái tháo đường, nguy cơ phẫu thuật, độ phức tạp giải phẫu và khả năng tái thông hoàn toàn</strong>.</p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("""
            #### Các tình huống tái thông mạch vành được ESC 2024 khuyến cáo
            * **Triệu chứng dai dẳng dù GDMT + CAD tắc nghẽn có ý nghĩa chức năng:** tái thông được khuyến cáo để **cải thiện triệu chứng — Class I A**. Guideline không yêu cầu phải thất bại với “ít nhất 2 nhóm thuốc” trước khi áp dụng khuyến cáo này.
            * **Multivessel CAD + LVEF ≤35% + đủ điều kiện phẫu thuật:** **CABG** được khuyến cáo hơn điều trị nội khoa đơn thuần để cải thiện sống còn dài hạn — **Class I B**.
            * **Left Main đáng kể, nguy cơ phẫu thuật thấp:** **CABG** được khuyến cáo hơn điều trị nội khoa đơn thuần để cải thiện sống còn — **Class I A**; nhìn chung CABG là phương thức ưu tiên hơn PCI — **Class I A**. Nếu giải phẫu ít phức tạp (SYNTAX ≤22) và PCI có thể tái thông tương đương, PCI là lựa chọn thay thế được khuyến cáo — **Class I A**.
            * **Multivessel CAD + đái tháo đường + đáp ứng GDMT chưa đủ:** **CABG** được khuyến cáo hơn điều trị nội khoa đơn thuần và hơn PCI để cải thiện triệu chứng và kết cục — **Class I A**.
            * **Bệnh 3 nhánh, LVEF bảo tồn, không đái tháo đường, đáp ứng GDMT chưa đủ:** **CABG** được khuyến cáo — **Class I A**; PCI cũng được khuyến cáo nếu giải phẫu phức tạp thấp–trung bình và có thể đạt mức tái thông tương tự CABG — **Class I A**.
            * **Bệnh 1–2 nhánh có đoạn gần LAD đáng kể, đáp ứng GDMT chưa đủ:** **CABG hoặc PCI** được khuyến cáo hơn điều trị nội khoa đơn thuần để cải thiện triệu chứng và kết cục — **Class I A**.
            """)

            st.markdown("""
            **Các lưu ý kỹ thuật quan trọng của ESC 2024:**
            * **Tổn thương trung gian:** đánh giá mức độ có ý nghĩa chức năng bằng **FFR/iFR** trước quyết định tái thông; ngưỡng có ý nghĩa thường **FFR ≤0,80 hoặc iFR ≤0,89** — **Class I A**.
            * **PCI tổn thương phức tạp:** hướng dẫn bằng **IVUS hoặc OCT** được khuyến cáo, đặc biệt ở thân chung, bifurcation thật và tổn thương dài — **Class I A**.
            * **Multivessel CAD:** nên tính **SYNTAX score** để đánh giá độ phức tạp giải phẫu — **Class I B**.
            * Khi cân nhắc CABG, **STS score** được khuyến cáo để ước tính bệnh suất trong viện và tử vong 30 ngày — **Class I B**.
            """)

        st.write("")
        if st.button("⬅️ Quay lại Bước 3"):
            set_step(3)

st.write("")
st.markdown("<p style='text-align: center; font-size: 0.8rem; color: #888;'>Phát triển dựa trên ESC 2024 về Hội chứng mạch vành mạn và ESC/EAS Focused Update 2025 về rối loạn lipid máu | Thiết kế tương tác từng bước cho nhà lâm sàng</p>", unsafe_allow_html=True)
