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

    /* H0 — Main page title: clean PE-like presentation, no surrounding frame */
    h1.main-title {
        font-size: 2.30rem !important;
        color: #24458f !important;
        text-align: center !important;
        font-weight: 900 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.35px !important;
        line-height: 1.05 !important;
        margin: 6px 0 2px 0 !important;
        padding: 0 !important;
        display: block !important;
        width: 100% !important;
        background: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        text-shadow: none !important;
    }

    .main-subtitle {
        text-align: center !important;
        color: #475569 !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        line-height: 1.15 !important;
        margin-top: 0 !important;
        margin-bottom: 16px !important;
        letter-spacing: 0 !important;
    }

    /* Native markdown heading hierarchy below the 4 main Step headings */
    h1:not(.main-title) {
        font-size: 1.60rem !important;
        color: #153b5b !important;
        font-weight: 850 !important;
        line-height: 1.10 !important;
        margin-top: 10px !important;
        margin-bottom: 7px !important;
    }
    h2 {
        font-size: 1.35rem !important;
        color: #1a5276 !important;
        font-weight: 820 !important;
        line-height: 1.12 !important;
        margin-top: 9px !important;
        margin-bottom: 6px !important;
    }
    h3 {
        font-size: 1.15rem !important;
        color: #256b93 !important;
        font-weight: 800 !important;
        border-bottom: 2px solid #7ccfb0 !important;
        padding-bottom: 4px !important;
        line-height: 1.12 !important;
        margin-top: 10px !important;
        margin-bottom: 6px !important;
    }
    h4 {
        font-size: 1.08rem !important;
        color: #2c3e50 !important;
        font-weight: 720 !important;
        line-height: 1.15 !important;
        margin-top: 8px !important;
        margin-bottom: 5px !important;
    }
    p, span, label, li {
        font-size: 1.03rem !important;
    }

    /* Responsive scaling keeps the hierarchy intact on smaller screens */
    @media (max-width: 1200px) {
        h1.main-title { font-size: 2.10rem !important; line-height: 1.05 !important; }
        .main-subtitle { font-size: 1.00rem !important; }
    }
    @media (max-width: 768px) {
        h1.main-title { font-size: 1.75rem !important; line-height: 1.07 !important; }
        .main-subtitle { font-size: 0.95rem !important; margin-bottom: 12px !important; }
        h1:not(.main-title) { font-size: 1.40rem !important; }
        h2 { font-size: 1.25rem !important; }
        h3 { font-size: 1.10rem !important; }
        h4 { font-size: 1.02rem !important; }
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
        padding: 9px 15px !important;
        border-radius: 8px !important;
        margin-top: 6px !important;
        margin-bottom: 6px !important;
        display: block !important;
    }
    div.main-step-active button p, div.main-step-active [data-testid="stBaseButton-secondary"] p,
    div.main-step-active button span, div.main-step-active [data-testid="stBaseButton-secondary"] span {
        font-size: 1.60rem !important;
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
        padding: 8px 14px !important;
        border-radius: 8px !important;
        margin-top: 5px !important;
        margin-bottom: 5px !important;
        opacity: 0.95 !important;
        display: block !important;
    }
    div.main-step-completed button p, div.main-step-completed [data-testid="stBaseButton-secondary"] p,
    div.main-step-completed button span, div.main-step-completed [data-testid="stBaseButton-secondary"] span {
        font-size: 1.60rem !important;
        font-weight: 800 !important;
        color: #117a65 !important;
        margin: 0 !important;
    }
    
    div.main-step-pending button, div.main-step-pending [data-testid="stBaseButton-secondary"] {
        background-color: #f1f2f6 !important;
        border: 1px dashed #bdc3c7 !important;
        width: 100% !important;
        text-align: left !important;
        padding: 8px 14px !important;
        border-radius: 8px !important;
        margin-top: 5px !important;
        margin-bottom: 5px !important;
        opacity: 0.7 !important;
        display: block !important;
    }
    div.main-step-pending button p, div.main-step-pending [data-testid="stBaseButton-secondary"] p,
    div.main-step-pending button span, div.main-step-pending [data-testid="stBaseButton-secondary"] span {
        font-size: 1.60rem !important;
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
        padding: 7px 11px !important;
        border-radius: 4px !important;
        margin-top: 5px !important;
        margin-bottom: 5px !important;
        display: block !important;
    }
    div.sub-header-active button p, div.sub-header-active [data-testid="stBaseButton-secondary"] p,
    div.sub-header-active button span, div.sub-header-active [data-testid="stBaseButton-secondary"] span {
        font-size: 1.20rem !important;
        font-weight: 800 !important;
        color: #1b4f72 !important;
        margin: 0 !important;
    }
    
    div.sub-header-inactive button, div.sub-header-inactive [data-testid="stBaseButton-secondary"] {
        background-color: #fcfcfc !important;
        border: 1px solid #d5dbdb !important;
        width: 100% !important;
        text-align: left !important;
        padding: 6px 10px !important;
        border-radius: 4px !important;
        margin-top: 4px !important;
        margin-bottom: 4px !important;
        opacity: 0.85 !important;
        display: block !important;
    }
    div.sub-header-inactive button p, div.sub-header-inactive [data-testid="stBaseButton-secondary"] p,
    div.sub-header-inactive button span, div.sub-header-inactive [data-testid="stBaseButton-secondary"] span {
        font-size: 1.15rem !important;
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

st.markdown("<h1 class='main-title'>🫀 QUẢN LÝ BAN ĐẦU NGHI NGỜ HỘI CHỨNG MẠCH VÀNH MẠN (CCS)</h1>", unsafe_allow_html=True)
st.markdown("<div class='main-subtitle'>Hệ thống Hỗ trợ Quyết định Lâm sàng (CDSS) tương tác đa tầng theo Hướng dẫn ESC 2024</div>", unsafe_allow_html=True)

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
        padding: 9px 15px !important;
        margin: 6px 0 !important;
        min-height: 50px !important;
        box-shadow: {step_shadow} !important;
        justify-content: flex-start !important;
        text-align: left !important;
    }}
    div[class*="st-key-main_step_btn_{step_id}"] button p,
    div[class*="st-key-main_step_btn_{step_id}"] button span {{
        font-size: 1.60rem !important;
        line-height: 1.10 !important;
        font-weight: 900 !important;
        color: {step_text} !important;
        letter-spacing: 0.25px !important;
        margin: 0 !important;
    }}
    @media (max-width: 1200px) {{
        div[class*="st-key-main_step_btn_{step_id}"] button p,
        div[class*="st-key-main_step_btn_{step_id}"] button span {{ font-size: 1.50rem !important; }}
    }}
    @media (max-width: 768px) {{
        div[class*="st-key-main_step_btn_{step_id}"] button {{ padding: 8px 11px !important; min-height: 44px !important; }}
        div[class*="st-key-main_step_btn_{step_id}"] button p,
        div[class*="st-key-main_step_btn_{step_id}"] button span {{ font-size: 1.28rem !important; }}
    }}
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f"<div class='{wrapper_class}'>", unsafe_allow_html=True)
    if st.button(f"{arrow} {prefix}{title}{status_text}", key=f"main_step_btn_{step_id}"):
        st.session_state.step = step_id
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
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
    sub_size = "1.20rem" if is_active else "1.12rem"

    widget_key = f"btn_{session_key}_{sub_step_id}"
    st.markdown(f"""
    <style>
    div[class*="st-key-{widget_key}"] button {{
        width: 100% !important;
        background: {sub_bg} !important;
        border: 1px solid {sub_border} !important;
        border-left: 6px solid {sub_border} !important;
        border-radius: 6px !important;
        padding: 6px 10px !important;
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
        div[class*="st-key-{widget_key}"] button span {{ font-size: 1.05rem !important; }}
    }}
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f"<div class='{wrapper_class}'>", unsafe_allow_html=True)
    if st.button(f"{arrow} {title}", key=widget_key):
        st.session_state[session_key] = sub_step_id
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
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
                symptom_analysis["summary_text"] = "👉 Triệu chứng đau ngực có đặc tính gợi ý tăng khả năng mắc bệnh mạch vành (Đau thắt ngực điển hình/Không điển hình)."
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
                
            done_biochem = st.checkbox("Hóa sinh máu cơ bản")
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
                with bio_col2:
                    st.session_state.hba1c_val = st.number_input("HbA1c (%):", min_value=3.0, max_value=20.0, value=st.session_state.get('hba1c_val', 5.8), step=0.1)
                    st.session_state.egfr_val = st.number_input("Mức lọc cầu thận eGFR (mL/min/1.73m²):", min_value=5, max_value=150, value=st.session_state.egfr_val)
                    
                    st.session_state.diabetes_flag = (st.session_state.hba1c_val >= 6.5)
                    st.session_state.dyslipidemia_flag = (st.session_state.ldlc_val_mmol >= 3.0 or st.session_state.tg_val_mmol >= 1.7)
                    
                    if st.session_state.diabetes_flag:
                        st.warning("⚠️ Phát hiện HbA1c ≥ 6.5%: Tự động kích hoạt tiền sử đái tháo đường ở Bước 2.")
                    if st.session_state.egfr_val < 60:
                        st.error(f"⚠️ eGFR giảm ({st.session_state.egfr_val} mL/min): Bệnh nhân có suy giảm chức năng thận mạn tính.")
        with test_col2:
            st.write("**Thăm dò chọn lọc bổ sung:**")
            done_cxr = st.checkbox("Chụp X-quang ngực thẳng")
            if done_cxr:
                cxr_status = st.radio("Kết quả X-quang ngực:", ["Chưa ghi nhận bất thường (Bình thường)", "Có bất thường"])
                if cxr_status == "Có bất thường":
                    cxr_res = st.multiselect("Bất thường ghi nhận:", ["Bóng tim to", "Sung huyết phổi", "Tràn dịch màng phổi"])
                    st.session_state.cxr_abnormal = len(cxr_res) > 0
                else:
                    st.session_state.cxr_abnormal = False
                    st.success("✅ Kết quả X-quang ngực hoàn toàn bình thường.")
                    
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
elif render_main_step_header("BƯỚC 2: ĐÁNH GIÁ CHUYÊN SÂU", 2):
    
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
                "Rối loạn chức năng tâm trương thất trái"
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
            st.write("**Các yếu tố lâm sàng làm thay đổi khả năng mắc bệnh (Class I):**")
            
            ecg_adj_default = st.session_state.ecg_abnormal
            lvd_adj_default = st.session_state.get('lvd_flag', False)
            
            adj_ecg = st.checkbox("ECG lúc nghỉ bất thường (Sóng Q bệnh lý hoặc ST-T biến đổi)", value=ecg_adj_default)
            adj_lvd = st.checkbox("Siêu âm tim có rối loạn vận động vùng hoặc giảm LVEF", value=lvd_adj_default)
            adj_pad = st.checkbox("Bệnh nhân có tiền sử bệnh động mạch ngoại biên (PAD)")
            adj_calc = st.checkbox("X-quang ngực hoặc CT phổi ghi nhận vôi hóa mạch vành")
            adj_ex_ecg = st.checkbox("Nghiệm pháp gắng sức ECG dương tính")
            
            has_clinical_adjusters = (adj_ecg or adj_lvd or adj_pad or adj_calc or adj_ex_ecg)
            
        with adj_col2:
            st.write("**Phân tầng lại bằng Điểm vôi hóa mạch vành (CACS - Class IIa):**")
            cacs_available = st.radio("Đo vôi hóa mạch vành (CACS):", ["Chưa thực hiện", "Đã có kết quả"])
            
            cacs_val = -1
            cacs_override_flag = False
            cacs_modifier = 0
            
            if cacs_available == "Đã có kết quả":
                cacs_val = st.number_input("Nhập điểm vôi hóa mạch vành (Agatston):", min_value=0, max_value=5000, value=0, step=10)
                if cacs_val == 0:
                    cacs_override_flag = True
                    st.success("✅ **CACS = 0 (Class IIa):** Khả năng hẹp tắc nghẽn vô cùng thấp. Phân tầng lại lâm sàng về nhóm **Rất thấp (≤5%)**.")
                elif 1 <= cacs_val < 10:
                    cacs_modifier = -5
                    st.info("CACS 1-9: Vôi hóa mạch vành tối thiểu. Không làm thay đổi đáng kể nguy cơ nền.")
                elif 10 <= cacs_val < 100:
                    cacs_modifier = 0
                    st.info("CACS 10-99: Vôi hóa mạch vành nhẹ. CCTA là lựa chọn chẩn đoán đầu tay.")
                elif 100 <= cacs_val < 400:
                    cacs_modifier = 10
                    st.warning("CACS 100-399: Vôi hóa vừa. Tăng nhẹ khả năng lâm sàng nền (+10%).")
                elif 400 <= cacs_val < 1000:
                    cacs_override_flag = True
                    st.warning("⚠️ **CACS 400-999 (Vôi hóa nặng - Class IIa):** Khả năng lâm sàng chuyển sang nhóm **Cao (High)**. Khuyên dùng **Thăm dò gắng sức chức năng** do CCTA dễ bị xảo ảnh.")
                else: # >= 1000
                    cacs_override_flag = True
                    st.error("🚨 **CACS ≥ 1000 (Vôi hóa cực nặng - Class IIa):** Khả năng lâm sàng chuyển sang nhóm **Rất cao (>85%)**. Khuyên chọn **Thăm dò gắng sức chức năng** hoặc cân nhắc chụp mạch vành xâm lấn (ICA).")

        # Clinical Judgment Correction (Correction bám sát Guideline: Không tự ý cộng dồn % toán học bừa bãi)
        base_lk = st.session_state.get('base_likelihood', 20)
        adjusted_likelihood = base_lk
        
        # Display judgment-based warning
        if has_clinical_adjusters:
            st.warning("💡 **Khuyến nghị Lâm sàng (Clinical Judgment):** Bệnh nhân có yếu tố bất thường (ECG, Siêu âm tim hoặc PAD). **Khả năng lâm sàng mắc mạch vành thực tế có thể CAO HƠN** tỷ lệ phần trăm RF-CL nền.")
            
        if cacs_available == "Đã có kết quả":
            if cacs_override_flag:
                if cacs_val == 0: adjusted_likelihood = 5
                elif cacs_val >= 1000: adjusted_likelihood = 90
                else: adjusted_likelihood = 65
            else:
                adjusted_likelihood += cacs_modifier
                
        adjusted_likelihood = max(0, min(95, adjusted_likelihood))
        
        def get_class_label(val):
            if val <= 5: return "Rất thấp (Very Low)", "#28a745"
            elif val <= 15: return "Thấp (Low)", "#17a2b8"
            elif val <= 50: return "Trung bình (Moderate)", "#ffc107"
            elif val <= 85: return "Cao (High)", "#fd7e14"
            else: return "Rất cao (Very High)", "#dc3545"

        adj_label, adj_col = get_class_label(adjusted_likelihood)
        
        st.markdown(f"""
        <div style='background-color: #f1f2f6; border-radius: 6px; padding: 15px; border-left: 6px solid {adj_col}; margin: 15px 0;'>
            <h4 style='margin: 0; color: #333;'>Khả năng lâm sàng sau phân tầng lại:</h4>
            <p style='font-size: 1.60rem; margin: 10px 0 5px 0; font-weight: bold;'>Khả năng lâm sàng mạch vành: <span style='color: {adj_col};'>{adjusted_likelihood}%</span></p>
            <p style='margin: 0;'>Nhóm phân loại: <strong style='color: {adj_col};'>{adj_label}</strong></p>
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        if st.button("Xác nhận & Sang Bước 3 ➡️"):
            st.session_state.likelihood_value = adjusted_likelihood
            st.session_state.cacs_score_val = cacs_val if cacs_available == "Đã có kết quả" else -1
            set_step(3)


# ====================================================
# BƯỚC 3: XÁC ĐỊNH CHẨN ĐOÁN
# ====================================================
elif render_main_step_header("BƯỚC 3: XÁC ĐỊNH CHẨN ĐOÁN", 3):
    
    # Sub-step 3.1: Khuyến cáo thăm dò
    if render_sub_header("Khuyến cáo thăm dò", 1, "step3_sub"):
        st.subheader("1. Khuyến cáo lựa chọn kỹ thuật chẩn đoán đầu tay")
        
        lik = st.session_state.get('likelihood_value', 20)
        cacs_score = st.session_state.get('cacs_score_val', -1)
        st.markdown(f"Khả năng lâm sàng thực tế của bệnh nhân: **{lik}%**")
        
        if lik <= 5:
            st.markdown("""
            <div class='success-box'>
                <strong>🟢 HOÃN CÁC THĂM DÒ CHẨN ĐOÁN SÂU HƠN <span class='class-badge-2a'>Class IIa</span></strong><br>
                - Bệnh nhân thuộc nhóm khả năng lâm sàng rất thấp (≤5%). Tầm soát thường quy không đem lại lợi ích thực tế.<br>
                - Nên tập trung tìm kiếm các nguyên nhân gây đau ngực ngoài tim khác.
            </div>
            """, unsafe_allow_html=True)
        elif 5 < lik <= 15:
            st.markdown("""
            <div class='recommendation-box'>
                <strong>🔵 CHỤP CẮT LỚP VI TÍNH ĐỘNG MẠCH VÀNH (CCTA) <span class='class-badge-1'>Class I</span></strong><br>
                - Chỉ định ưu tiên hàng đầu để chẩn đoán xác định và loại trừ hẹp động mạch vành cơ học ở nhóm khả năng lâm sàng thấp.<br>
                - Giúp đánh giá chi tiết gánh nặng và cấu trúc mảng xơ vữa.
            </div>
            """, unsafe_allow_html=True)
        elif 15 < lik <= 50:
            if cacs_score >= 400:
                st.markdown("""
                <div class='warning-box' style='border-left-color: #fd7e14;'>
                    <strong>🟡 THĂM DÒ HÌNH ẢNH CHỨC NĂNG GẮNG SỨC LÀ ƯU TIÊN <span class='class-badge-2a'>Class IIa</span></strong><br>
                    - Do vôi hóa mạch vành rất nặng (CACS ≥ 400), độ chính xác của chụp cắt lớp CCTA bị suy giảm mạnh do xảo ảnh vôi hóa.<br>
                    - Khuyên dùng: <strong>Stress Echo, Stress CMR, PET hoặc stress SPECT</strong> để đánh giá trực tiếp thiếu máu cơ tim sinh lý.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class='warning-box' style='border-left-color: #fd7e14;'>
                    <strong>🟡 CHỌN CCTA (Class I A) HOẶC THĂM DÒ HÌNH ẢNH CHỨC NĂNG GẮNG SỨC (Class I B)</strong><br>
                    - Bệnh nhân thuộc nhóm trung bình (15-50%) có thể lựa chọn linh hoạt một trong hai thăm dò đầu tay:<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;* <strong>CCTA (Cắt lớp vi tính):</strong> Ưu tiên để loại trừ hẹp, bệnh nhân trẻ, ít vôi hóa.<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;* <strong>Hình ảnh chức năng gắng sức (Stress Echo, Stress CMR, SPECT, PET):</strong> Ưu tiên nếu nghi ngờ thiếu máu cơ tim diện rộng hoặc có tiền sử nhồi máu cơ tim cũ.
                </div>
                """, unsafe_allow_html=True)
        elif 50 < lik <= 85:
            st.markdown("""
            <div class='warning-box' style='border-left-color: #fd7e14;'>
                <strong>🟠 ƯU TIÊN THĂM DÒ HÌNH ẢNH CHỨC NĂNG GẮNG SỨC <span class='class-badge-1'>Class I</span></strong><br>
                - Bệnh nhân khả năng lâm sàng cao (>50%). Khuyên chỉ định các thăm dò chức năng không xâm lấn để đánh giá trực tiếp diện tích vùng thiếu máu cơ tim.<br>
                - Chỉ định: <strong>Stress Echo, Stress CMR, SPECT hoặc PET</strong>.
            </div>
            """, unsafe_allow_html=True)
        else: # > 85%
            st.markdown("""
            <div class='warning-box'>
                <strong>🔴 CHỤP ĐỘNG MẠCH VÀNH XÂM LẤN (ICA) TRỰC TIẾP <span class='class-badge-1'>Class I</span></strong><br>
                - Nhóm khả năng lâm sàng rất cao (>85%), đau thắt ngực nặng kháng trị bằng thuốc, hoặc có biểu hiện suy tim cơ năng rõ rệt.<br>
                - Tiến hành ICA trực tiếp để lập phác đồ và lên kế hoạch can thiệp tái thông mạch vành đồng thời (kèm đo FFR/iFR nếu có hẹp trung gian).
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
                 "Hẹp mức độ trung bình (50-90% các nhánh chính - Tổn thương trung gian)",
                 "Hẹp nặng rõ rệt (Obstructive CAD: ≥50% Thân chung LMS, hoặc ≥70% nhánh lớn khác, hoặc FFR-CT ≤ 0.80)"]
            )
            if "Không hẹp" in ccta_res:
                st.session_state.coronary_status = "Non-obstructive"
            elif "trung bình" in ccta_res:
                st.warning("⚠️ **Tổn thương trung gian (Intermediate Stenosis):** Có sự không tương hợp phổ biến giữa mức độ hẹp giải phẫu và ý nghĩa huyết động thực tế (haemodynamic significance).")
                ccta_functional = st.radio(
                    "Đánh giá ý nghĩa huyết động của tổn thương trung gian này:",
                    ["Chưa đánh giá ý nghĩa sinh lý / Đang chờ",
                     "CÓ Ý NGHĨA SINH LÝ (Đã làm FFR-CT ≤ 0.80 hoặc Stress imaging dương tính)",
                     "KHÔNG CÓ Ý NGHĨA SINH LÝ (FFR-CT > 0.80 hoặc Stress imaging âm tính)"]
                )
                if "CÓ Ý NGHĨA" in ccta_functional:
                    st.session_state.coronary_status = "Obstructive"
                else:
                    st.session_state.coronary_status = "Non-obstructive"
            else:
                st.session_state.coronary_status = "Obstructive"
                
        elif selected_test == "Thăm dò hình ảnh chức năng gắng sức":
            func_res = st.radio(
                "Kết quả thiếu máu cơ tim gắng sức:",
                ["Âm tính (Không có thiếu máu cơ tim hoặc thiếu máu không đáng kể)",
                 "Dương tính (Phát hiện vùng thiếu máu cơ tim thực thể)"]
            )
            if "Dương tính" in func_res:
                st.session_state.coronary_status = "Obstructive"
            else:
                st.session_state.coronary_status = "Non-obstructive"
                
        elif selected_test == "Chụp động mạch vành xâm lấn (ICA)":
            ica_res = st.radio(
                "Kết quả giải phẫu mạch vành trên phim ICA:",
                ["Không hẹp hoặc hẹp nhẹ (<50% Thân chung LMS, <50% các nhánh chính)",
                 "Hẹp mức độ trung bình (Tổn thương ranh giới 50-90%)",
                 "Hẹp nặng rõ rệt (Obstructive CAD: ≥50% Thân chung LMS, hoặc ≥70% nhánh lớn khác, hoặc FFR ≤ 0.80 / iFR ≤ 0.89)"]
            )
            if "Không hẹp" in ica_res:
                st.session_state.coronary_status = "Non-obstructive"
            elif "trung bình" in ica_res:
                st.warning("⚠️ **Tổn thương ranh giới (Borderline Stenosis):** Yêu cầu đánh giá chức năng bằng FFR/iFR để chẩn đoán ý nghĩa sinh lý (Class I).")
                ica_functional = st.radio(
                    "Kết quả đo FFR/iFR trong buồng tim:",
                    ["Chưa đo FFR/iFR / Đang chờ",
                     "CÓ Ý NGHĨA SINH LÝ (FFR ≤ 0.80 hoặc iFR ≤ 0.89)",
                     "KHÔNG CÓ Ý NGHĨA SINH LÝ (FFR > 0.80 hoặc iFR > 0.89)"]
                )
                if "CÓ Ý NGHĨA" in ica_functional:
                    st.session_state.coronary_status = "Obstructive"
                else:
                    st.session_state.coronary_status = "Non-obstructive"
            else:
                st.session_state.coronary_status = "Obstructive"
        else:
            st.info("💡 Đang chờ kết quả xét nghiệm. Vui lòng cập nhật để thực hiện phân tầng điều trị.")
            st.session_state.coronary_status = "Untested"
            
        st.write(f"👉 Trạng thái mạch vành hiện tại: **{st.session_state.coronary_status}**")

    # Sub-step 3.3: Chẩn đoán ANOCA/INOCA
    if render_sub_header("Chẩn đoán ANOCA/INOCA", 3, "step3_sub"):
        if st.session_state.get('coronary_status', "Untested") == "Non-obstructive":
            st.subheader("3. Đánh giá đau ngực không hẹp tắc nghẽn (ANOCA/INOCA)")
            
            has_symptoms = st.radio(
                "Bệnh nhân có triệu chứng đau ngực hoặc khó thở dai dẳng ảnh hưởng chất lượng cuộc sống (đã loại trừ nguyên nhân ngoài tim) không?",
                ["Có triệu chứng dai dẳng", "Không còn triệu chứng / Triệu chứng nhẹ đã ổn định"]
            )
            
            if has_symptoms == "Có triệu chứng dai dẳng":
                st.session_state.anoca_suspected = True
                st.markdown("""
                <div class='warning-box' style='border-left-color: #f1c40f; background-color: #fefdf3;'>
                    <h4 style='color: #d4ac0d; margin-top: 0;'>🧩 NGHI NGỜ LÂM SÀNG: MẮC ANOCA / INOCA</h4>
                    <p>Giải phẫu mạch vành không có hẹp tắc nghẽn cơ học nhưng triệu chứng đau thắt ngực vẫn dai dẳng. Hướng dẫn ESC 2024 khuyến cáo thực hiện <strong>Đo chức năng mạch vành xâm lấn (ICFT - Class I B)</strong> để xác định kiểu hình.</p>
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
                if icft_cfr == "Giảm (CFR < 2.5)" or icft_imr == "Tăng (IMR ≥ 25 HOẶC HMR > 2.5)":
                    if icft_spasm == "Âm tính":
                        st.session_state.anoca_endotype = "Đau thắt ngực vi mạch (MVA)"
                    else:
                        st.session_state.anoca_endotype = "Kiểu hình hỗn hợp (Mixed MVA + VSA)"
                elif icft_spasm != "Âm tính":
                    st.session_state.anoca_endotype = "Co thắt mạch vành (VSA)"
                else:
                    st.session_state.anoca_endotype = "Đau ngực ngoài tim"
                    
                st.success(f"🎯 **Kiểu hình ANOCA/INOCA xác định:** `{st.session_state.anoca_endotype}`. Phác đồ điều trị cá thể hóa tương ứng đã kích hoạt tại Bước 4.")
            else:
                st.session_state.anoca_suspected = False
                st.success("✅ Mạch vành không hẹp tắc nghẽn và lâm sàng ổn định, không có chỉ định thăm dò ANOCA chuyên sâu.")
        else:
            st.info("💡 Phần này chỉ hiển thị khi giải phẫu mạch vành được xác định là: **LOẠI TRỪ hẹp tắc nghẽn (Non-obstructive CAD)** ở tiểu mục 2.")

    # Sub-step 3.4: Phân tầng nguy cơ
    if render_sub_header("Phân tầng nguy cơ", 4, "step3_sub"):
        if st.session_state.get('coronary_status', "Untested") == "Obstructive":
            st.subheader("4. Phân tầng nguy cơ biến cố tim mạch tương lai (Event-Risk)")
            st.markdown("<p style='font-size: 0.95rem;'>Xác định các tiêu chuẩn nguy cơ biến cố rất cao diện rộng (Class I B):</p>", unsafe_allow_html=True)
            
            risk_col1, risk_col2 = st.columns(2)
            with risk_col1:
                st.write("**Các tiêu chuẩn về cấu trúc giải phẫu (Anatomical):**")
                high_risk_anatomy = st.checkbox("CCTA/ICA: Tổn thương Thân chung Động mạch vành trái (Left Main) hẹp ≥ 50%")
                high_risk_anatomy_2 = st.checkbox("CCTA/ICA: Hẹp nặng ≥ 70% ở cả 3 nhánh mạch vành (Three-vessel disease)")
                high_risk_anatomy_3 = st.checkbox("CCTA/ICA: Hẹp đoạn gần động mạch liên thất trước (Proximal LAD) ≥ 70%")
            with risk_col2:
                st.write("**Các tiêu chuẩn về chức năng thiếu máu (Functional):**")
                high_risk_func_1 = st.checkbox("Stress Echo: ≥ 3/16 phân vùng cơ tim bị giảm động hoặc vô động do gắng sức")
                high_risk_func_2 = st.checkbox("Stress CMR: ≥ 2/16 phân vùng cơ tim thiếu máu diện rộng")
                high_risk_func_3 = st.checkbox("Stress SPECT/PET: Vùng thiếu máu cơ tim cơ năng ≥ 10% thất trái")
                high_risk_func_4 = st.checkbox("Exercise ECG: Điểm số gắng sức Duke (Duke Treadmill Score) < -10")
                
            is_high_risk = (high_risk_anatomy or high_risk_anatomy_2 or high_risk_anatomy_3 or 
                            high_risk_func_1 or high_risk_func_2 or high_risk_func_3 or high_risk_func_4)
            st.session_state.high_risk_flag = is_high_risk
            
            if is_high_risk:
                st.error("""
                **🚨 BỆNH NHÂN THUỘC NHÓM NGUY CƠ BIẾN CỐ CAO (HIGH EVENT-RISK) - Khuyến cáo Class I B:**
                - Có bằng chứng hẹp cấu trúc nguy cơ cao hoặc vùng cơ tim thiếu máu diện rộng.
                - Chỉ định chụp mạch vành xâm lấn (ICA) kết hợp đo FFR/iFR để lên phương án tái thông sớm cải thiện tiên lượng sống còn.
                """)
            else:
                st.info("💡 Hẹp mạch vành tắc nghẽn mức độ nhẹ-vừa (Nguy cơ biến cố thấp). Ưu tiên điều trị nội khoa tối ưu (GDMT) hàng đầu.")
        else:
            st.info("💡 Phần này chỉ hiển thị khi kết quả thăm dò xác định bệnh nhân **CÓ hẹp động mạch vành tắc nghẽn (Obstructive CAD)** ở tiểu mục 2.")

        # Navigation to Step 4
        st.write("")
        if st.button("Xác nhận & Sang Bước 4 ➡️"):
            set_step(4)


# ====================================================
# BƯỚC 4: ĐIỀU TRỊ TỐI ƯU
# ====================================================
elif render_main_step_header("BƯỚC 4: ĐIỀU TRỊ TỐI ƯU", 4):
    
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
            
            st.write("**Thuốc bảo vệ tim mạch cải thiện sống còn (Class I):**")
            st.markdown("""
            * **Kháng kết tập tiểu cầu:** *Aspirin 75-100 mg/ngày* hoặc *Clopidogrel 75 mg/ngày* được chỉ định lâu dài ở bệnh nhân có mạch vành tắc nghẽn (Class I A).
            * **Kiểm soát huyết áp:** Mục tiêu huyết áp đích là **120-129 / 70-79 mmHg** nếu dung nạp tốt (Class I A, ưu tiên ACEi hoặc ARB).
            * **Đồng mắc đái tháo đường:** Bắt buộc sử dụng thuốc **ức chế SGLT2 (SGLT2i)** và/hoặc **đồng vận thụ thể GLP-1 (GLP-1 RA)** (Class I A).
            """)
            
        with tab_symptomatic:
            # Pull clinical variables
            hr_val = st.session_state.get('hr_val', 75)
            sbp_val = st.session_state.get('sbp_val', 120)
            lvef_val = st.session_state.get('lvef_val', 55)
            egfr_val = st.session_state.get('egfr_val', 90)
            pft_abnormal = st.session_state.get('pft_abnormal', False)
            anoca_suspected = st.session_state.get('anoca_suspected', False)
            anoca_endotype = st.session_state.get('anoca_endotype', "Chưa phân loại")
            
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
                    - **Bước 1 (Đầu tay):** <span class='class-badge-1'>Class I B</span> Sử dụng **Chẹn kênh Canxi (CCBs) liều cao** (như Amlodipine 10mg hoặc Diltiazem 120-240mg) để giãn động mạch co thắt.
                    - **Bước 2 (Phối hợp):** <span class='class-badge-2a'>Class IIa B</span> Phối hợp thêm **Nitrates tác dụng kéo dài** nếu triệu chứng co thắt chưa kiểm soát tốt.
                    - **🚨 CẢNH BÁO ĐỎ (Class III):** Tránh dùng thuốc Chẹn beta đơn trị vì gây hoạt hóa thụ thể alpha-adrenergic làm tăng co thắt mạch ác tính.
                    """, unsafe_allow_html=True)
                    apply_target = ["Chẹn kênh Canxi DHP (DHP-CCB)"]
                elif phenotype == "Đau thắt ngực vi mạch (ANOCA - MVA)":
                    st.markdown("""
                    - **Bước 1 (Đầu tay):** <span class='class-badge-2a'>Class IIa B</span> **Chẹn beta (BB)** (như Bisoprolol) làm giảm công tim và phục hồi cung lượng vi mạch.
                    - **Bước 2 (Phối hợp):** <span class='class-badge-2a'>Class IIa B</span> Phối hợp thêm **Chẹn kênh canxi DHP (DHP-CCB)** (như Amlodipine) nếu chẹn beta đơn trị chưa đỡ.
                    - **Bước 3 (Kháng trị):** <span class='class-badge-2b'>Class IIb B</span> Cân nhắc dùng thêm Nicorandil hoặc Ranolazine.
                    - **Bảo vệ nội mạc:** <span class='class-badge-2a'>Class IIa B</span> Sử dụng ACEi/ARB kết hợp Statin để cải thiện chức năng nội mạc vi tuần hoàn.
                    """, unsafe_allow_html=True)
                    apply_target = ["Chẹn beta (Beta-blockers - BB)", "Chẹn kênh Canxi DHP (DHP-CCB)"]
                elif phenotype == "Rối loạn chức năng thất trái / Suy tim giảm LVEF ≤ 40%":
                    st.markdown("""
                    - **Bước 1 (Đầu tay):** <span class='class-badge-1'>Class I A</span> **Chẹn beta (BB)** (như Bisoprolol, Metoprolol Succinate hoặc Carvedilol) liều thấp tăng dần để cải thiện sống còn.
                    - **Bước 2 (Phối hợp):** <span class='class-badge-2a'>Class IIa B</span> Phối hợp thêm **Ivabradine** (nếu nhịp xoang ≥ 70 bpm) HOẶC **Trimetazidine MR** (Class IIa B) để bổ sung năng lượng cơ tim.
                    - **🚨 CHỐNG CHỈ ĐỊNH (Class III):** Cấm sử dụng các thuốc chẹn canxi Non-DHP (Verapamil, Diltiazem) vì nguy cơ ức chế tim nặng làm bùng phát suy tim cấp.
                    """, unsafe_allow_html=True)
                    apply_target = ["Chẹn beta (Beta-blockers - BB)"]
                elif phenotype == "Tần số tim nhanh (HR > 80 nhịp/phút)":
                    st.markdown("""
                    - **Bước 1 (Đầu tay):** <span class='class-badge-1'>Class I B</span> Khởi trị bằng **Chẹn beta (BB)** hoặc **Chẹn kênh canxi Non-DHP** để giảm nhịp tim lúc nghỉ về mốc 55-60 nhịp/phút.
                    - **Bước 2 (Phối hợp):** <span class='class-badge-2a'>Class IIa B</span> Phối hợp **Chẹn beta (BB) + Chẹn kênh canxi DHP (Amlodipine)** khi đau ngực chưa kiểm soát tốt.
                    - **Bước 3 (Phối hợp thêm):**
                        * Phối hợp thêm **Ranolazine** HOẶC **Nitrates tác dụng kéo dài** (<span class='class-badge-2a'>Class IIa B</span>).
                        * Phối hợp thêm **Trimetazidine MR** HOẶC **Nicorandil** (<span class='class-badge-2b'>Class IIb B</span>).
                        * **🚨 CHỐNG CHỈ ĐỊNH (Class III B):** Tuyệt đối không dùng Ivabradine cho bệnh nhân LVEF > 40% không có suy tim.
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
                    - **🚨 CHỐNG CHỈ ĐỊNH (Class III B):** Tuyệt đối không dùng Ivabradine cho bệnh nhân LVEF > 40% không có suy tim.
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
                        * **🚨 CHỐNG CHỈ ĐỊNH (Class III B):** Tuyệt đối không dùng Ivabradine cho bệnh nhân LVEF > 40% không có suy tim.
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
                                - **❌ CHỐNG CHỈ ĐỊNH TUYỆT ĐỐI (Class III):** Nhịp tim chậm lúc nghỉ (< 50 nhịp/phút), Block AV độ II hoặc III (trừ khi đã đặt máy tạo nhịp), Hội chứng suy nút xoang, Suy tim mất bù cấp.
                                - **⚠️ Thận trọng quan trọng:** Hen phế quản nặng hoặc bệnh phổi tắc nghẽn mạn tính (COPD) có co thắt phế quản tiến triển (ưu tiên chọn chẹn beta siêu chọn lọc tim).
                                """)
                        if prescribe_dhp_ccb:
                            with st.expander("📖 Chống chỉ định & Thận trọng của Chẹn kênh Canxi DHP (DHP-CCB)", expanded=True):
                                st.markdown("""
                                - **❌ CHỐNG CHỈ ĐỊNH TUYỆT ĐỐI (Class III):** Huyết áp thấp nặng (Huyết áp tâm thu < 90 mmHg), Hẹp khít van động mạch chủ có triệu chứng nặng.
                                - **⚠️ Thận trọng quan trọng:** Nguy cơ gây phù ngoại biên vùng cổ chân ở liều cao (10mg).
                                """)
                        if prescribe_non_dhp_ccb:
                            with st.expander("📖 Chống chỉ định & Thận trọng của Chẹn kênh Canxi Non-DHP (Verapamil / Diltiazem)", expanded=True):
                                st.markdown("""
                                - **❌ CHỐNG CHỈ ĐỊNH TUYỆT ĐỐI (Class III - Figure 9 Đỏ / Drug-label):**
                                    * **Suy tim phân suất tống máu giảm LVEF ≤ 40% (HFrEF)** do tác dụng ức chế co bóp cơ tim lực (negative inotropic effect).
                                    * Phối hợp đồng thời với **Chẹn Beta (BB)** hoặc **Ivabradine** (nguy cơ nhịp chậm cực độ, ngừng xoang, block AV nặng).
                                    * Nhịp tim chậm lúc nghỉ (< 50 nhịp/phút).
                                    * Hội chứng suy nút xoang hoặc Block AV độ II-III.
                                """)
                        if prescribe_la_nitrate:
                            with st.expander("📖 Chống chỉ định & Thận trọng của Long-acting Nitrates", expanded=True):
                                st.markdown("""
                                - **❌ CHỐNG CHỈ ĐỊNH TUYỆT ĐỐI (Class III - Figure 9 Đỏ):**
                                    * **Sử dụng chung với thuốc ức chế PDE-5 (Sildenafil, Tadalafil...)** trong vòng 24 - 48 giờ trước (tương tác gây giãn mạch ác tính, tụt huyết áp đe dọa tính mạng).
                                    * Bệnh cơ tim phì đại tắc nghẽn (HCM) - do làm tăng độ chênh áp đường ra thất trái (LVOT obstruction).
                                - **⚠️ Thận trọng quan trọng:** Bắt buộc phải có khoảng trống không thuốc (Nitrate-free interval) từ 10-14 tiếng mỗi ngày để ngăn ngừa hiện tượng lờn thuốc.
                                """)
                        if prescribe_ivabradine:
                            with st.expander("📖 Chống chỉ định & Thận trọng của Ivabradine", expanded=True):
                                st.markdown("""
                                - **❌ CHỐNG CHỈ ĐỊNH TUYỆT ĐỐI (Class III - Figure 9 Đỏ):**
                                    * Bệnh nhân nhịp xoang lúc nghỉ < 50 nhịp/phút.
                                    * Phối hợp đồng thời với thuốc **Chẹn kênh Canxi Non-DHP (Verapamil / Diltiazem)**.
                                    * Bệnh nhân **LVEF > 40% mà KHÔNG có biểu hiện suy tim** lâm sàng (Class III B - Thử nghiệm SIGNIFY).
                                    * Bệnh nhân **Rung nhĩ (Atrial Fibrillation)** hoặc cuồng nhĩ.
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
                                - **❌ CHỐNG CHỈ ĐỊNH TUYỆT ĐỐI (Class III):** Shock tim, tụt huyết áp nặng.
                                - **⚠️ Thận trọng quan trọng:** **Nguy cơ gây loét nghiêm trọng:** Nicorandil có thể gây ra các vết loét niêm mạc dạ dày - tá tràng, loét da, loét giác mạc khó lành. Ngừng thuốc ngay lập tức nếu phát hiện các vết loét này (Class I A).
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
                                <h5 style='color: #c0392b; margin: 0; font-weight: bold;'>❌ CHỐNG CHỈ ĐỊNH PHỐI HỢP (Class III)</h5>
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
                            <div class='warning-box'>
                                <h5 style='color: #c0392b; margin: 0; font-weight: bold;'>❌ CHỐNG CHỈ ĐỊNH ĐƠN TRỊ LIỆU (Class III)</h5>
                                <strong>Chẹn beta đơn trị ở bệnh nhân Co thắt mạch (VSA):</strong><br>
                                - Chống chỉ định tuyệt đối Chẹn beta đơn trị do có thể làm co thắt mạch dữ dội hơn qua thụ thể alpha-adrenergic không đối kháng.
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
            | **3. Non-DHP CCB** | Verapamil (Isoptin), Diltiazem (Herbesser) | 120 - 240 mg/ngày / 120 - 180 mg/ngày | 360 - 480 mg/ngày / 360 mg/ngày | Chống chỉ định ở HFrEF (LVEF ≤ 40%), nhịp chậm, block nhĩ thất, suy nút xoang. Tuyệt đối không phối hợp cùng Chẹn beta hoặc Ivabradine (Class III). |
            | **4. LA Nitrates** | Isosorbide Mononitrate (Imdur), Isosorbide Dinitrate | 30 mg q.d. / 10 mg b.i.d. | 60 - 120 mg q.d. / 40 mg t.i.d. | Chống chỉ định ở bệnh cơ tim phì đại tắc nghẽn (HCM) và dùng chung PDE-5i (Sildenafil...) (Class III). Bắt buộc có khoảng nghỉ nitrate-free 10-14h hàng ngày để tránh lờn thuốc. |
            | **5. Ivabradine** | Ivabradine (Procoralan) | 5 mg b.i.d. (2.5mg nếu nhịp chậm) | 7.5 mg b.i.d. | Nhịp xoang < 50, rung nhĩ/cuồng nhĩ, nhồi máu cơ tim cấp. CCĐ ở LVEF > 40% không suy tim (Class III). Không dùng chung với Non-DHP CCB (Class III). |
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
            <strong>PHÂN LOẠI NGUY CƠ TIM MẠCH:</strong> Bệnh nhân đã được xác định mắc hội chứng vành mạn (CCS) được xem là thuộc nhóm nguy cơ tim mạch rất cao (Very High Cardiovascular Risk) theo ESC 2024.
        </div>
        """, unsafe_allow_html=True)
        
        recurrent_event = st.checkbox("Bệnh nhân có biến cố xơ vữa tái phát (nhồi máu cơ tim, đột quỵ...) trong vòng 2 năm qua khi đang dùng Statin liều tối đa?", key="lipid_recurrent_chk_v8")
        
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
             "Đang dùng phối hợp 3 thuốc (Statin tối đa + Ezetimibe + Ức chế PCSK9)",
             "Bệnh nhân hoàn toàn Kém dung nạp với Statin (Statin Intolerance)"]
        )
        
        is_at_target = ldlc_now < target_ldlc_mmol
        if is_at_target:
            st.success(f"🎉 **Chúc mừng!** Bệnh nhân đã đạt mục tiêu LDL-C (< {target_ldlc_mmol} mmol/L). Khuyên dùng duy trì phác đồ và tái khám định kỳ 6-12 tháng.")
        else:
            st.error(f"❌ **Chưa đạt mục tiêu!** LDL-C hiện tại ({ldlc_now:.2f} mmol/L) cao hơn mục tiêu điều trị đích (< {target_ldlc_mmol} mmol/L).")
            
            st.markdown("##### 📌 Khuyến cáo can thiệp tiếp theo từ ESC 2024:")
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
                1. <span class='class-badge-1'>Class I A</span> Phối hợp thêm thuốc **ức chế PCSK9 (PCSK9 inhibitor)** (như Alirocumab, Evolocumab hoặc Inclisiran).
                2. <span class='class-badge-2a'>Class IIa C</span> Hoặc cân nhắc phối hợp thêm **Bempedoic acid** 180mg hàng ngày.
                """, unsafe_allow_html=True)
            elif current_therapy == "Đang dùng phối hợp 3 thuốc (Statin tối đa + Ezetimibe + Ức chế PCSK9)":
                st.markdown("""
                1. Bệnh nhân đã tối đa hóa các phác đồ hạ lipid chuẩn mà vẫn chưa đạt mục tiêu. Cân nhắc phối hợp thêm **Bempedoic acid** hoặc **chuyển đổi/tăng cường hoạt lực** của nhóm ức chế PCSK9.
                2. Rà soát nghiêm ngặt sự tuân thủ điều trị của bệnh nhân.
                """)
            else: # Statin Intolerance
                st.markdown(f"""
                1. <span class='class-badge-1'>Class I B</span> Kê đơn **Ezetimibe 10mg** hàng ngày làm điều trị đầu tay.
                2. <span class='class-badge-1'>Class I B</span> Phối hợp thêm **Bempedoic acid** nếu Ezetimibe đơn trị liệu không đạt mục tiêu.
                3. <span class='class-badge-2a'>Class IIa C</span> Cân nhắc phối hợp thêm thuốc **ức chế PCSK9** nếu chưa kiểm soát được LDL-C.
                """, unsafe_allow_html=True)

        # Triglycerides Management
        st.markdown("#### 📈 Quản lý Triglyceride tăng cao")
        if tg_now >= 1.7:
            st.warning(f"Chỉ số Triglyceride hiện tại: **{tg_now:.2f} mmol/L** (tăng nhẹ đến vừa).")
            if 1.52 <= tg_now <= 5.63:
                st.markdown(f"""
                * <span class='class-badge-2a'>Class IIa B</span> Khuyến cáo cân nhắc bổ sung **Icosapent Ethyl (2 x 2g/ngày)** phối hợp cùng Statin để giảm thiểu nguy cơ biến cố tim mạch tồn dư.
                """, unsafe_allow_html=True)
            elif tg_now > 5.63:
                st.markdown("""
                * ⚠️ **CẢNH BÁO NGUY CƠ VIÊM TỤY CẤP:** Hạn chế mỡ tuyệt đối, kiểm soát đường huyết chặt chẽ.
                * Sử dụng **Fenofibrate** phối hợp hoặc **Omega-3 liều cao** để giảm TG khẩn cấp.
                """)
        else:
            st.success(f"Triglyceride bình thường: {tg_now:.2f} mmol/L (< 1.7 mmol/L).")

        # Lp(a) management (Correct threshold: nmol/L should use 105 instead of 50)
        if lpa_now > 105:
            st.error(f"⚠️ **Lp(a) tăng cao: {lpa_now} nmol/L** (> 105 nmol/L hoặc > 50 mg/dL). Đây là yếu tố nguy cơ độc lập do di truyền làm tăng mạnh gánh nặng xơ vữa mạch vành tồn dư, đòi hỏi kiểm soát LDL-C nghiêm ngặt hơn.")
        elif lpa_now > 0:
            st.info(f"Lp(a) trong giới hạn bình thường: {lpa_now} nmol/L.")

    # Sub-step 4.3: Can thiệp mạch vành
    if render_sub_header("Can thiệp mạch vành", 3, "step4_sub"):
        if st.session_state.get('anoca_suspected', False):
            st.markdown(f"""
            <div class='warning-box' style='border-left-color: #c0392b; background-color: #fdf2f2;'>
                <h4 style='color: #c0392b; margin-top: 0;'>🚫 KHÔNG CÓ CHỈ ĐỊNH CAN THIỆP / TÁI THÔNG MẠCH VÀNH (PCI / CABG)</h4>
                <p style='font-size: 1.05rem;'>Bệnh nhân đã được chẩn đoán mắc <strong>ANOCA/INOCA (Kiểu hình: {st.session_state.get('anoca_endotype', 'Chưa phân loại')})</strong>. 
                Không có tổn thương hẹp động mạch vành tắc nghẽn giải phẫu tầng thượng tâm mạc.</p>
                <p style='margin-bottom: 0;'><strong>Khuyến cáo:</strong> Chống chỉ định tái thông mạch cơ học do không đem lại lợi ích lâm sàng và có hại cho người bệnh. 
                <strong>Hãy tập trung hoàn toàn vào phác đồ điều trị nội khoa cá thể hóa cho ANOCA/INOCA tại Tab 'Điều trị nội khoa' (Phần 1).</strong></p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.subheader("3. Tiêu chuẩn chỉ định Tái thông mạch vành (Revascularization)")
            
            is_high_risk = st.session_state.get('high_risk_flag', False)
            if is_high_risk:
                st.markdown("""
                <div class='warning-box' style='border-left-color: #fd7e14;'>
                    <h4 style='color: #fd7e14; margin-top: 0;'>👉 CHỈ ĐỊNH TÁI THÔNG MẠCH VÀNH ĐỂ CẢI THIỆN TIÊN LƯỢNG (PROGNOSIS - Class I)</h4>
                    <p>Do bệnh nhân thuộc nhóm nguy cơ biến cố cao. Chỉ định tái thông để cải thiện tiên lượng sống còn phụ thuộc vào giải phẫu hẹp có ý nghĩa sinh lý và trị số LVEF bám sát ESC 2024:</p>
                    <ul>
                        <li><strong>Thân chung trái (Left Main) functionally significant VÀ LVEF > 35%:</strong> <span class='class-badge-1'>Class I A</span> (Ưu tiên CABG nếu giải phẫu phức tạp).</li>
                        <li><strong>Bệnh 3 nhánh functionally significant VÀ LVEF > 35%:</strong> <span class='class-badge-1'>Class I A</span>.</li>
                        <li><strong>Bệnh 1-2 nhánh có hẹp đoạn gần LAD functionally significant:</strong> <span class='class-badge-1'>Class I B</span>.</li>
                        <li><strong>Bệnh nhân có LVEF ≤ 35%:</strong> <span class='class-badge-1'>Class I B</span> Cần hội chẩn chuyên sâu **Heart Team** để lựa chọn chiến lược PCI hay CABG tối ưu.</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class='success-box' style='background-color: #e8f8f5; border-left-color: #2ecc71;'>
                    <h4 style='color: #2ecc71; margin-top: 0;'>🔴 ƯU TIÊN ĐIỀU TRỊ NỘI KHOA TỐI ƯU (GDMT) LÀ LỰA CHỌN ĐẦU TAY (Class I)</h4>
                    <p>Bệnh nhân hẹp mạch vành tắc nghẽn mức độ nhẹ-vừa (Nguy cơ biến cố thấp-trung bình):</p>
                    <ul>
                        <li><strong>🚫 CHƯA CÓ CHỈ ĐỊNH CAN THIỆP MẠCH VÀNH BAN ĐẦU:</strong> Không tự ý can thiệp mạch vành (PCI/CABG) sớm ở nhóm này vì không mang lại lợi ích cải thiện tiên lượng tử vong hay kéo dài sự sống so với điều trị thuốc tối ưu.</li>
                        <li><strong>⚠️ Chỉ định can thiệp trì hoãn (Class I A):</strong> Chỉ xem xét can thiệp mạch vành nhằm <strong>cải thiện triệu chứng</strong> nếu triệu chứng đau ngực hoặc khó thở vẫn dai dẳng, ảnh hưởng nặng đến sinh hoạt hoạt động hàng ngày, mặc dù đã điều trị nội khoa tối đa (GDMT) với <strong>ít nhất 2 nhóm thuốc</strong> chống đau thắt ngực.</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown("""
            **Các lưu ý kỹ thuật quan trọng của ESC 2024:**
            * **Hẹp ranh giới (Intermediate stenosis):** Luôn đánh giá chức năng bằng **FFR** hoặc **iFR** trước khi quyết định can thiệp (Class I).
            * **Can thiệp phức tạp:** Sử dụng các phương tiện chẩn đoán hình ảnh trong lòng mạch như **IVUS** hoặc **OCT** để hướng dẫn kỹ thuật can thiệp tối ưu (Class I).
            """)

        st.write("")
        if st.button("⬅️ Quay lại Bước 3"):
            set_step(3)

st.write("")
st.markdown("<p style='text-align: center; font-size: 0.8rem; color: #888;'>Phát triển chuyên sâu dựa trên Hướng dẫn của Hội Tim mạch Châu Âu (ESC) 2024 về quản lý Hội chứng mạch vành mạn | Thiết kế tương tác từng bước cho nhà lâm sàng</p>", unsafe_allow_html=True)
