import streamlit as st
import math

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Hỗ trợ Quyết định Lâm sàng PE - AHA/ACC 2026 (Bản chuẩn)",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="auto"
)

# MENU ĐIỀU HƯỚNG — đồng bộ với công cụ CCS
st.sidebar.page_link(
    "pe-cdss-web.py",
    label="🫁 Thuyên tắc phổi cấp"
)
st.sidebar.page_link(
    "pages/1_❤️_Hoi_chung_vanh_man.py",
    label="❤️ Hội chứng vành mạn"
)

# Giao diện đồng bộ CCS: phân cấp trực quan + accordion + responsive mobile
st.markdown(r"""
<style>
    .stApp { background: #f8fafc; }
    .block-container {
        /* Chừa khoảng trống cho thanh công cụ cố định của Streamlit/Safari. */
        padding-top: 4.75rem !important;
        padding-bottom: 2.0rem !important;
        max-width: 1480px;
    }

    h1.main-title,
    div[data-testid="stMarkdownContainer"] h1.main-title,
    h1.main-title span,
    h1.main-title * {
        color: #123a5a !important;
        font-size: 2.65rem !important;
        line-height: 1.02 !important;
        font-weight: 950 !important;
        letter-spacing: -0.7px !important;
        margin: 0 !important;
        padding: 0 !important;
        white-space: nowrap !important;
    }
    .main-subtitle, .main-subtitle * {
        color: #526979 !important;
        font-size: 1.02rem !important;
        line-height: 1.25 !important;
        font-weight: 540 !important;
        margin-top: 4px !important;
        margin-bottom: 0 !important;
    }
    .header-divider {
        height: 3px;
        border-radius: 99px;
        background: linear-gradient(90deg, #123a5a 0%, #176b78 55%, #17b978 100%);
        margin: 11px 0 16px 0;
    }

    h1:not(.main-title) { font-size: 1.45rem !important; color:#153b5b !important; font-weight:850 !important; }
    h2 { font-size: 1.25rem !important; color:#1a5276 !important; font-weight:820 !important; }
    h3 { font-size: 1.12rem !important; color:#256b93 !important; font-weight:800 !important; border-bottom:2px solid #7ccfb0 !important; padding-bottom:3px !important; }
    h4 { font-size: 1.03rem !important; color:#2c3e50 !important; font-weight:720 !important; }
    div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stMarkdownContainer"] li,
    label { font-size: 1.01rem !important; }
    section.main div[data-testid="stVerticalBlock"] { gap: 0.38rem !important; }

    .section-card {
        background-color: #F8FAFC;
        padding: 16px;
        border-radius: 8px;
        border-left: 5px solid #1E3A8A;
        margin-bottom: 10px;
    }
    .result-card {
        background-color: #EFF6FF;
        padding: 16px;
        border-radius: 8px;
        border: 1px solid #BFDBFE;
        margin-top: 8px;
    }
    .u-card { padding: 13px; border-radius: 8px; margin-bottom: 8px; }
    .urgency-high { background-color:#FEF2F2; border-left:5px solid #DC2626; color:#991B1B; }
    .urgency-medium { background-color:#FFFBEB; border-left:5px solid #D97706; color:#92400E; }
    .urgency-low { background-color:#F0FDF4; border-left:5px solid #16A34A; color:#166534; }
    .badge { background-color:#E2E8F0; color:#1E293B; padding:4px 8px; border-radius:4px; font-size:.85rem; font-weight:600; }

    /* Bảng rộng: giữ dễ đọc trên desktop và cuộn ngang trên mobile */
    .table-style {
        width: 100%;
        border-collapse: collapse;
        margin: 12px 0;
        display: block;
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
    }
    .table-style tbody { display: table; width: 100%; min-width: 760px; }
    .table-style th, .table-style td { border:1px solid #CBD5E1; padding:8px 12px; text-align:left; }
    .table-style th { background-color:#F1F5F9; font-weight:600; }

    /* Native expander được dùng như heading cấp 2 để nội dung vẫn được thực thi khi thu gọn. */
    details[data-testid="stExpander"] {
        border: 1px solid #c7d8e5 !important;
        border-left: 6px solid #3498db !important;
        border-radius: 7px !important;
        background: #fbfdff !important;
        margin: 4px 0 7px 0 !important;
        overflow: hidden !important;
    }
    details[data-testid="stExpander"] > summary {
        background: #eef7fc !important;
        min-height: 42px !important;
        padding: 4px 9px !important;
    }
    details[data-testid="stExpander"] > summary:hover { background:#e6f4fb !important; }
    details[data-testid="stExpander"] > summary p,
    details[data-testid="stExpander"] > summary span {
        color:#174d70 !important;
        font-size:1.08rem !important;
        font-weight:820 !important;
        line-height:1.12 !important;
    }
    details[data-testid="stExpander"] > div { padding-top: 6px !important; }

    /* Touch targets */
    div[data-testid="stButton"] button { min-height: 40px; }


    /* Bảng kiểm chống chỉ định tiêu sợi huyết: nút dạng card có thể mở/thu gọn.
       Dùng button thay vì nested st.expander để tránh expander lồng expander. */
    div.st-key-thrombolysis_ci_toggle button {
        width: 100% !important;
        min-height: 50px !important;
        justify-content: flex-start !important;
        text-align: left !important;
        white-space: normal !important;
        background: #FFFBEB !important;
        color: #92400E !important;
        border: 1px solid #F3D18A !important;
        border-left: 5px solid #D97706 !important;
        border-radius: 8px !important;
        font-weight: 800 !important;
        box-shadow: none !important;
        padding: 10px 13px !important;
    }
    div.st-key-thrombolysis_ci_toggle button:hover {
        background: #FFF7D6 !important;
        border-color: #D97706 !important;
        color: #78350F !important;
    }
    div.st-key-thrombolysis_ci_toggle button p {
        font-size: 1.02rem !important;
        font-weight: 800 !important;
        margin: 0 !important;
    }

    /* Trạng thái huyết động là quyết định rẽ nhánh chính của Bước 2: làm nổi bật như một decision box. */
    div.st-key-w_primary_hemo {
        background: linear-gradient(135deg, #eef8ff 0%, #ecfbf5 100%) !important;
        border: 1px solid #8bc9c2 !important;
        border-left: 6px solid #176b78 !important;
        border-radius: 9px !important;
        padding: 10px 12px 12px 12px !important;
        margin: 3px 0 12px 0 !important;
        box-shadow: 0 4px 12px rgba(23,107,120,.10) !important;
    }
    div.st-key-w_primary_hemo [data-baseweb="select"] > div {
        background: #ffffff !important;
        border: 2px solid #176b78 !important;
        min-height: 48px !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 7px rgba(18,58,90,.08) !important;
    }
    div.st-key-w_primary_hemo [data-baseweb="select"] span,
    div.st-key-w_primary_hemo [data-baseweb="select"] div {
        font-weight: 720 !important;
        color: #163f5c !important;
    }

    @media (max-width: 1200px) {
        h1.main-title, div[data-testid="stMarkdownContainer"] h1.main-title,
        h1.main-title span, h1.main-title * { font-size:2.25rem !important; }
    }
    @media (max-width: 768px) {
        /* Trên mobile vẫn chừa đủ khoảng trống để header không bị thanh app che. */
        .block-container { padding: 3.85rem .72rem 1.5rem .72rem !important; }
        h1.main-title, div[data-testid="stMarkdownContainer"] h1.main-title,
        h1.main-title span, h1.main-title * {
            font-size:1.78rem !important;
            line-height:1.05 !important;
            white-space:normal !important;
            letter-spacing:-0.25px !important;
        }
        .main-subtitle, .main-subtitle * { font-size:.91rem !important; line-height:1.22 !important; }
        .header-divider { margin:8px 0 12px 0 !important; }
        h1:not(.main-title) { font-size:1.26rem !important; }
        h2 { font-size:1.13rem !important; }
        h3 { font-size:1.00rem !important; }
        h4 { font-size:.98rem !important; }
        div[data-testid="stMarkdownContainer"] p,
        div[data-testid="stMarkdownContainer"] li,
        label { font-size:.96rem !important; }
        .section-card, .result-card, .u-card { padding:11px !important; }
        details[data-testid="stExpander"] > summary { min-height:46px !important; padding:6px 8px !important; }
        details[data-testid="stExpander"] > summary p,
        details[data-testid="stExpander"] > summary span { font-size:.98rem !important; }
        div[data-testid="stButton"] button { min-height:46px !important; width:100% !important; }
        /* Mọi micro-column tự xếp dọc trên điện thoại; desktop không bị ảnh hưởng. */
        div[data-testid="stHorizontalBlock"] { flex-wrap:wrap !important; gap:.35rem !important; }
        div[data-testid="stColumn"], div[data-testid="column"] { flex:1 1 100% !important; min-width:100% !important; width:100% !important; }
        input, textarea, select { font-size:16px !important; }
        .table-style { max-width:100%; }
        .table-style tbody { min-width:720px; }
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🫁 TIẾP CẬN BAN ĐẦU THUYÊN TẮC PHỔI CẤP (PE)</h1>", unsafe_allow_html=True)
st.markdown("<div class='main-subtitle'>Hệ thống Hỗ trợ Quyết định Lâm sàng (CDSS) tương tác đa tầng theo Hướng dẫn AHA/ACC 2026</div>", unsafe_allow_html=True)
st.markdown("<div class='header-divider'></div>", unsafe_allow_html=True)
# Khởi tạo kho lưu trữ toàn cục cho các lựa chọn nếu chưa có
if 'saved_inputs' not in st.session_state:
    st.session_state.saved_inputs = {}

# Định nghĩa các hàm tiện ích hỗ trợ lưu trữ trạng thái khi đổi tab
def persistent_checkbox(label, key, default=False, help_text=None):
    if key not in st.session_state.saved_inputs:
        st.session_state.saved_inputs[key] = default
    val = st.checkbox(label, value=st.session_state.saved_inputs[key], key=f"w_{key}", help=help_text)
    st.session_state.saved_inputs[key] = val
    return val

def persistent_selectbox(label, options, key, default_idx=0, help_text=None, label_visibility="visible"):
    if key not in st.session_state.saved_inputs:
        st.session_state.saved_inputs[key] = options[default_idx]
    stored_val = st.session_state.saved_inputs[key]
    if stored_val not in options:
        stored_val = options[default_idx]
    idx = options.index(stored_val)
    val = st.selectbox(label, options, index=idx, key=f"w_{key}", help=help_text, label_visibility=label_visibility)
    st.session_state.saved_inputs[key] = val
    return val

def persistent_radio(label, options, key, default_idx=0, horizontal=False):
    if key not in st.session_state.saved_inputs:
        st.session_state.saved_inputs[key] = options[default_idx]
    stored_val = st.session_state.saved_inputs[key]
    if stored_val not in options:
        stored_val = options[default_idx]
    idx = options.index(stored_val)
    val = st.radio(label, options, index=idx, key=f"w_{key}", horizontal=horizontal)
    st.session_state.saved_inputs[key] = val
    return val

def persistent_number_input(label, min_value, max_value, default_val, key, step=1):
    if key not in st.session_state.saved_inputs:
        st.session_state.saved_inputs[key] = default_val
    val = st.number_input(label, min_value=min_value, max_value=max_value, value=st.session_state.saved_inputs[key], key=f"w_{key}", step=step)
    st.session_state.saved_inputs[key] = val
    return val

# Quản lý State bằng Session State
if 'step' not in st.session_state:
    st.session_state.step = 1  # 1: Chẩn đoán, 2: Phân loại lâm sàng, 3: Điều trị

if 'is_pregnant' not in st.session_state:
    st.session_state.is_pregnant = False

if 'final_category' not in st.session_state:
    st.session_state.final_category = None

if 'resp_modifier' not in st.session_state:
    st.session_state.resp_modifier = False

if 'g2_stable_flow' not in st.session_state:
    st.session_state.g2_stable_flow = "organ_damage"  # Tuần tự mới: organ_damage -> cpes -> prognosis

if 'step1_sub' not in st.session_state:
    st.session_state.step1_sub = 1
if 'step2_focus' not in st.session_state:
    st.session_state.step2_focus = "hemo"
if 'step3_open' not in st.session_state:
    st.session_state.step3_open = 1

# Helper render main step giống CCS; chỉ thay đổi UI/interaction, không đổi logic lâm sàng.
def render_main_step_header(title, step_id):
    current_step = st.session_state.step
    is_active = (current_step == step_id)
    is_completed = (current_step > step_id)
    arrow = "▼" if is_active else "▶"
    prefix = "✅ " if is_completed else ""
    status_text = " [ĐANG THỰC HIỆN]" if is_active else ""

    if is_active:
        bg = "linear-gradient(135deg, #123a5a 0%, #176b78 52%, #17b978 100%)"
        border = "#17b978"; text = "#ffffff"; shadow = "0 8px 22px rgba(23,107,120,.30)"
    elif is_completed:
        bg = "linear-gradient(135deg, #e7f8f1 0%, #d2f1e5 100%)"
        border = "#2ecc71"; text = "#0d684f"; shadow = "0 5px 14px rgba(46,204,113,.16)"
    else:
        bg = "linear-gradient(135deg, #eef5fb 0%, #e7f1f8 100%)"
        border = "#79a9c7"; text = "#183f5f"; shadow = "0 4px 12px rgba(30,61,89,.10)"

    key = f"main_step_btn_{step_id}"
    st.markdown(f"""
    <style>
    div[class*="st-key-{key}"] button {{
        width:100% !important; background:{bg} !important; border:2px solid {border} !important;
        border-left-width:7px !important; border-radius:9px !important; padding:6px 12px !important;
        margin:1px 0 !important; min-height:42px !important; box-shadow:{shadow} !important;
        justify-content:flex-start !important; text-align:left !important;
    }}
    div[class*="st-key-{key}"] button p, div[class*="st-key-{key}"] button span {{
        font-size:1.38rem !important; line-height:1.05 !important; font-weight:900 !important;
        color:{text} !important; margin:0 !important;
    }}
    @media (max-width:768px) {{
      div[class*="st-key-{key}"] button {{ padding:7px 9px !important; min-height:48px !important; }}
      div[class*="st-key-{key}"] button p, div[class*="st-key-{key}"] button span {{ font-size:1.08rem !important; }}
    }}
    </style>
    """, unsafe_allow_html=True)
    if st.button(f"{arrow} {prefix}{title}{status_text}", key=key):
        st.session_state.step = 0 if is_active else step_id
        st.rerun()
    return is_active

# Nút điều hướng nhỏ giữa các heading cấp 2.
def goto_step1_sub(n):
    st.session_state.step1_sub = n
    st.rerun()

def goto_step3_sub(n):
    st.session_state.step3_open = n
    st.rerun()

# Accordion cấp 2 dùng chung cho Bước 1 và Bước 3.
# Cùng ngôn ngữ thị giác với các heading động ở Bước 2; chỉ render nội dung của heading đang mở.
def render_flow_sub_header(title, focus_id, state_key, key_prefix):
    current_focus = st.session_state.get(state_key, focus_id)
    is_active = (current_focus == focus_id)
    arrow = "▼" if is_active else "▶"

    sub_bg = "#eaf4fb" if is_active else "#fbfdff"
    sub_border = "#3498db" if is_active else "#c7d8e5"
    sub_text = "#174d70" if is_active else "#4d6475"
    sub_weight = 820 if is_active else 680
    safe_id = str(focus_id).replace("_", "-")
    widget_key = f"{key_prefix}_{safe_id}"

    st.markdown(f"""
    <style>
    div[class*="st-key-{widget_key}"] button {{
        width:100% !important;
        background:{sub_bg} !important;
        border:1px solid {sub_border} !important;
        border-left:6px solid {sub_border} !important;
        border-radius:7px !important;
        padding:5px 10px !important;
        margin:4px 0 !important;
        justify-content:flex-start !important;
        text-align:left !important;
        min-height:42px !important;
        box-shadow:{'0 3px 10px rgba(52,152,219,.10)' if is_active else 'none'} !important;
    }}
    div[class*="st-key-{widget_key}"] button p,
    div[class*="st-key-{widget_key}"] button span {{
        font-size:{'1.08rem' if is_active else '1.01rem'} !important;
        line-height:1.12 !important;
        font-weight:{sub_weight} !important;
        color:{sub_text} !important;
        margin:0 !important;
        white-space:normal !important;
    }}
    @media (max-width:768px) {{
        div[class*="st-key-{widget_key}"] button {{ min-height:46px !important; padding:7px 9px !important; }}
        div[class*="st-key-{widget_key}"] button p,
        div[class*="st-key-{widget_key}"] button span {{ font-size:.98rem !important; }}
    }}
    </style>
    """, unsafe_allow_html=True)

    if st.button(f"{arrow} {title}", key=widget_key):
        st.session_state[state_key] = 0 if is_active else focus_id
        st.rerun()
    return is_active

# Accordion cấp 2 riêng cho Bước 2.
# Khác với st.expander native, nội dung chỉ render ở heading đang active,
# nên khi chuyển quyết định cũ sẽ THU GỌN thật sự và heading kế tiếp tự mở.
def render_step2_sub_header(title, focus_id):
    current_focus = st.session_state.get("step2_focus", "hemo")
    is_active = (current_focus == focus_id)
    arrow = "▼" if is_active else "▶"

    sub_bg = "#eaf4fb" if is_active else "#fbfdff"
    sub_border = "#3498db" if is_active else "#c7d8e5"
    sub_text = "#174d70" if is_active else "#4d6475"
    sub_weight = 820 if is_active else 680
    safe_id = str(focus_id).replace("_", "-")
    widget_key = f"step2_sub_{safe_id}"

    st.markdown(f"""
    <style>
    div[class*="st-key-{widget_key}"] button {{
        width:100% !important;
        background:{sub_bg} !important;
        border:1px solid {sub_border} !important;
        border-left:6px solid {sub_border} !important;
        border-radius:7px !important;
        padding:5px 10px !important;
        margin:4px 0 !important;
        justify-content:flex-start !important;
        text-align:left !important;
        min-height:42px !important;
        box-shadow:{'0 3px 10px rgba(52,152,219,.10)' if is_active else 'none'} !important;
    }}
    div[class*="st-key-{widget_key}"] button p,
    div[class*="st-key-{widget_key}"] button span {{
        font-size:{'1.08rem' if is_active else '1.01rem'} !important;
        line-height:1.12 !important;
        font-weight:{sub_weight} !important;
        color:{sub_text} !important;
        margin:0 !important;
        white-space:normal !important;
    }}
    @media (max-width:768px) {{
        div[class*="st-key-{widget_key}"] button {{ min-height:46px !important; padding:7px 9px !important; }}
        div[class*="st-key-{widget_key}"] button p,
        div[class*="st-key-{widget_key}"] button span {{ font-size:.98rem !important; }}
    }}
    </style>
    """, unsafe_allow_html=True)

    if st.button(f"{arrow} {title}", key=widget_key):
        st.session_state.step2_focus = "none" if is_active else focus_id
        # Nếu bác sĩ chủ động quay lại một heading của nhánh huyết động ổn định,
        # đồng bộ luôn clinical flow để các heading phía sau không còn được xem là đã đi qua.
        if not is_active and focus_id in {"organ_damage", "cpes", "prognosis", "rv_biomarkers", "hk_position"}:
            st.session_state.g2_stable_flow = focus_id
        st.rerun()
    return is_active

# ==============================================================================
# BƯỚC 1: CHẨN ĐOÁN & LOẠI TRỪ PE
# ==============================================================================
if render_main_step_header("⚡ BƯỚC 1: CHẨN ĐOÁN & LOẠI TRỪ", 1):
    # Khôi phục các biến cần dùng giữa 1.1 và 1.2 từ persistent state để accordion có thể render từng phần độc lập.
    _s1 = st.session_state.saved_inputs
    is_anticoagulated = _s1.get("is_anticoagulated", False)
    is_suspected = _s1.get("is_suspected", True)
    st.session_state.is_pregnant = _s1.get("is_pregnant", st.session_state.is_pregnant)
    _score_type_saved = _s1.get("score_type", "Thang điểm Wells (Khuyên dùng)")
    if "Wells" in _score_type_saved:
        cptp_score = (3.0 if _s1.get("w1", False) else 0.0) + (3.0 if _s1.get("w2", False) else 0.0) + (1.5 if _s1.get("w3", False) else 0.0) + (1.5 if _s1.get("w4", False) else 0.0) + (1.5 if _s1.get("w5", False) else 0.0) + (1.0 if _s1.get("w6", False) else 0.0) + (1.0 if _s1.get("w7", False) else 0.0)
        if cptp_score < 2.0:
            cptp_category = "LOW"
        elif cptp_score <= 6.0:
            cptp_category = "INTERMEDIATE"
        else:
            cptp_category = "HIGH"
    else:
        cptp_score = sum(1.0 for _k in ["g1", "g2", "g3", "g4", "g5", "g6", "g8"] if _s1.get(_k, False)) + (1.0 if _s1.get("g7", False) else 0.0)
        if cptp_score <= 1.0:
            cptp_category = "LOW"
        elif cptp_score <= 4.0:
            cptp_category = "INTERMEDIATE"
        else:
            cptp_category = "HIGH"

    if render_flow_sub_header("1.1 📋 Đánh giá Sơ bộ & Xác suất lâm sàng tiền nghiệm (CPTP)", 1, "step1_sub", "step1_sub"):
        
        # Câu hỏi sàng lọc chống chỉ định loại trừ không hình ảnh học
        is_anticoagulated = persistent_checkbox("Bệnh nhân ĐANG sử dụng thuốc kháng đông liều đầy đủ (therapeutic anticoagulation)?", key="is_anticoagulated")
        
        if is_anticoagulated:
            st.markdown("""
            <div class='u-card urgency-medium'>
                <strong>⚠️ CẢNH BÁO LÂM SÀNG:</strong> Bệnh nhân đang dùng kháng đông liều đầy đủ không phù hợp để áp dụng các chiến lược loại trừ dựa trên D-dimer (như PERC hay YEARS) vì D-dimer bị ảnh hưởng mạnh bởi thuốc kháng đông. Hãy tiến hành đánh giá lâm sàng trực tiếp hoặc chỉ định hình ảnh học nếu nghi ngờ tắc mạch tái phát/tiến triển.
            </div>
            """, unsafe_allow_html=True)
            
        is_suspected = persistent_checkbox("Bệnh nhân có triệu chứng/dấu hiệu nghi ngờ PE cấp tính (khó thở, đau ngực, ho ra máu, ngất...)?", key="is_suspected", default=True)
        is_pregnant_input = persistent_checkbox("Bệnh nhân hiện tại đang mang thai?", key="is_pregnant")
        st.session_state.is_pregnant = is_pregnant_input
        
        cptp_category = "LOW"
        cptp_score = 0.0
        
        if is_suspected:
            # ==================================================================
            # NHÁNH TIẾP CẬN THAI KỲ (PREGNANCY-ADAPTED YEARS)
            # ==================================================================
            if st.session_state.is_pregnant:
                st.markdown("<div class='section-card'>", unsafe_allow_html=True)
                st.write("🤰 **Tiếp cận thích ứng Thai kỳ (Pregnancy-adapted YEARS):**")
                has_dvt_sym = persistent_checkbox("Bệnh nhân mang thai có triệu chứng sưng đau một bên chân gợi ý DVT?", key="has_dvt_sym")
                
                is_preg_cus_positive = False
                if has_dvt_sym:
                    st.markdown("""
                    <div class='u-card urgency-high'>
                        <strong>🚨 CHỈ ĐỊNH SIÊU ÂM DOPPLER TĨNH MẠCH CHI DƯỚI (CUS) TRƯỚC TIÊN:</strong><br>
                        Theo Guideline, thai phụ có triệu chứng DVT chi dưới phải thực hiện siêu âm CUS trước tiên để tránh tia xạ tối đa (Class 1, LOE C-LD).
                    </div>
                    """, unsafe_allow_html=True)
                    
                    cus_result = persistent_radio("Kết quả siêu âm CUS chi dưới:", [
                        "Chưa thực hiện / Kết quả Âm tính",
                        "DƯƠNG TÍNH (Xác nhận có DVT chi dưới)"
                    ], key="cus_result")
                    
                    if "DƯƠNG TÍNH" in cus_result:
                        is_preg_cus_positive = True
                        st.markdown("""
                        <div class='u-card urgency-low'>
                            <strong>>>> KẾT LUẬN CHẨN ĐOÁN: XÁC LẬP VTE/PE LÂM SÀNG (KHỞI TRỊ KHÁNG ĐÔNG NGAY)</strong><br>
                            Có bằng chứng DVT chân trên siêu âm -> Khuyến cáo điều trị kháng đông bằng LMWH ngay lập tức (Class 1, LOE C-LD) mà không nhất thiết phải chụp CTPA hay làm D-dimer để tránh phơi nhiễm phóng xạ (VTE/PE presumed).
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Vẫn hiển thị Wells/Geneva để bác sĩ tham khảo CPTP ban đầu (như yêu cầu)
                # Chỉ hiển thị khi CUS không dương tính để giao diện tinh gọn
                if not is_preg_cus_positive:
                    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
                    st.write("📋 **Xác suất lâm sàng tiền nghiệm tham khảo (CPTP cho thai kỳ):**")
                    score_type = persistent_radio("Chọn Thang điểm Đánh giá:", ["Thang điểm Wells (Khuyên dùng)", "Thang điểm Geneva Rút gọn"], key="score_type")
                    
                    if score_type == "Thang điểm Wells (Khuyên dùng)":
                        st.info("Tính điểm Wells:")
                        w1 = persistent_checkbox("Lâm sàng có triệu chứng/dấu hiệu của DVT (+3.0)", key="w1")
                        w2 = persistent_checkbox("PE là chẩn đoán khả thi nhất hoặc có khả năng xảy ra cao nhất (+3.0)", key="w2")
                        w3 = persistent_checkbox("Tần số tim > 100 chu kỳ/phút (+1.5)", key="w3")
                        w4 = persistent_checkbox("Bất động >= 3 ngày liên tục hoặc mới phẫu thuật trong vòng 4 tuần trước (+1.5)", key="w4")
                        w5 = persistent_checkbox("Tiền sử cá nhân đã từng bị DVT hoặc PE trước đây (+1.5)", key="w5")
                        w6 = persistent_checkbox("Bệnh nhân có ho ra máu (+1.0)", key="w6")
                        w7 = persistent_checkbox("Bệnh nhân có ung thư đang tiến triển (+1.0)", key="w7")
                        
                        cptp_score = (3.0 if w1 else 0.0) + (3.0 if w2 else 0.0) + (1.5 if w3 else 0.0) + (1.5 if w4 else 0.0) + (1.5 if w5 else 0.0) + (1.0 if w6 else 0.0) + (1.0 if w7 else 0.0)
                        st.metric(label="Tổng điểm Wells", value=f"{cptp_score} điểm")
                        
                        if cptp_score < 2.0: cptp_category = "LOW"
                        elif cptp_score <= 6.0: cptp_category = "INTERMEDIATE"
                        else: cptp_category = "HIGH"
                    else:
                        st.info("Tính điểm Geneva Rút gọn:")
                        g1 = persistent_checkbox("Tuổi > 65 tuổi (+1)", key="g1")
                        g2 = persistent_checkbox("Tiền sử cá nhân bị DVT hoặc PE (+1)", key="g2")
                        g3 = persistent_checkbox("Phẫu thuật hoặc gãy xương chi dưới trong vòng 1 tháng qua (+1)", key="g3")
                        g4 = persistent_checkbox("Ung thư đang hoạt động/tiến triển (+1)", key="g4")
                        g5 = persistent_checkbox("Đau một bên chi dưới (+1)", key="g5")
                        g6 = persistent_checkbox("Ho ra máu (+1)", key="g6")
                        g7 = persistent_checkbox("Tần số tim 75 - 94 chu kỳ/phút (+1) HOẶC >= 95 chu kỳ/phút (+1)", key="g7")
                        g8 = persistent_checkbox("Đau khi sờ nắn tĩnh mạch sâu một bên chi dưới và phù một bên chân (+1)", key="g8")
                        
                        cptp_score = sum([g1, g2, g3, g4, g5, g6, g8])
                        if g7: cptp_score += 1.0
                        st.metric(label="Tổng điểm Geneva Rút gọn", value=f"{cptp_score} điểm")
                        
                        if cptp_score <= 1.0: cptp_category = "LOW"
                        elif cptp_score <= 4.0: cptp_category = "INTERMEDIATE"
                        else: cptp_category = "HIGH"
                    st.markdown("</div>", unsafe_allow_html=True)
            
            # ==================================================================
            # BỆNH NHÂN KHÔNG MANG THAI - DÙNG WELLS / GENEVA TIÊU CHUẨN
            # ==================================================================
            else:
                st.markdown("<div class='section-card'>", unsafe_allow_html=True)
                score_type = persistent_radio("Chọn Thang điểm Đánh giá Xác suất lâm sàng tiền nghiệm:", ["Thang điểm Wells (Khuyên dùng)", "Thang điểm Geneva Rút gọn"], key="score_type")
                
                if score_type == "Thang điểm Wells (Khuyên dùng)":
                    st.info("Tính điểm Wells:")
                    w1 = persistent_checkbox("Lâm sàng có triệu chứng/dấu hiệu của DVT (sưng chân, đau dọc tĩnh mạch) (+3.0)", key="w1")
                    w2 = persistent_checkbox("PE là chẩn đoán khả thi nhất hoặc có khả năng xảy ra cao nhất (+3.0)", key="w2")
                    w3 = persistent_checkbox("Tần số tim > 100 chu kỳ/phút (+1.5)", key="w3")
                    w4 = persistent_checkbox("Bất động >= 3 ngày liên tục hoặc mới phẫu thuật trong vòng 4 tuần trước (+1.5)", key="w4")
                    w5 = persistent_checkbox("Tiền sử cá nhân đã từng bị DVT hoặc PE trước đây (+1.5)", key="w5")
                    w6 = persistent_checkbox("Bệnh nhân có ho ra máu (+1.0)", key="w6")
                    w7 = persistent_checkbox("Bệnh nhân có ung thư đang tiến triển (đang điều trị, điều trị giảm nhẹ, hoặc phát hiện trong 6 tháng) (+1.0)", key="w7")
                    
                    cptp_score = (3.0 if w1 else 0.0) + (3.0 if w2 else 0.0) + (1.5 if w3 else 0.0) + (1.5 if w4 else 0.0) + (1.5 if w5 else 0.0) + (1.0 if w6 else 0.0) + (1.0 if w7 else 0.0)
                    st.metric(label="Tổng điểm Wells", value=f"{cptp_score} điểm")
                    
                    if cptp_score < 2.0: cptp_category = "LOW"
                    elif cptp_score <= 6.0: cptp_category = "INTERMEDIATE"
                    else: cptp_category = "HIGH"
                    
                else:
                    st.info("Tính điểm Geneva Rút gọn (Simplified Revised Geneva):")
                    g1 = persistent_checkbox("Tuổi > 65 tuổi (+1)", key="g1")
                    g2 = persistent_checkbox("Tiền sử cá nhân bị DVT hoặc PE (+1)", key="g2")
                    g3 = persistent_checkbox("Phẫu thuật hoặc gãy xương chi dưới trong vòng 1 tháng qua (+1)", key="g3")
                    g4 = persistent_checkbox("Ung thư đang hoạt động/tiến triển (+1)", key="g4")
                    g5 = persistent_checkbox("Đau một bên chi dưới (+1)", key="g5")
                    g6 = persistent_checkbox("Ho ra máu (+1)", key="g6")
                    g7 = persistent_checkbox("Tần số tim 75 - 94 chu kỳ/phút (+1) HOẶC >= 95 chu kỳ/phút (+1)", key="g7")
                    g8 = persistent_checkbox("Đau khi sờ nắn tĩnh mạch sâu một bên chi dưới và phù một bên chân (+1)", key="g8")
                    
                    cptp_score = sum([g1, g2, g3, g4, g5, g6, g8])
                    if g7: cptp_score += 1.0
                    st.metric(label="Tổng điểm Geneva Rút gọn", value=f"{cptp_score} điểm")
                    
                    if cptp_score <= 1.0: cptp_category = "LOW"
                    elif cptp_score <= 4.0: cptp_category = "INTERMEDIATE"
                    else: cptp_category = "HIGH"
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.success("Bệnh nhân không có triệu chứng nghi ngờ. Khám phát hiện tình cờ -> Thích hợp để quản lý ngoại trú (Category A)")
        if st.button("Tiếp tục → Thuật toán loại trừ không hình ảnh học", type="primary", use_container_width=True, key="step1_to_sub2"):
            st.session_state.step1_sub = 2
            st.rerun()
    if render_flow_sub_header("1.2 ⚡ Thuật toán Loại trừ Không hình ảnh học", 2, "step1_sub", "step1_sub"):
        
        if is_suspected:
            if is_anticoagulated:
                st.markdown("""
                <div class='u-card urgency-high'>
                    <strong>>>> KẾT LUẬN: CHỈ ĐỊNH CHỤP HÌNH ẢNH HỌC PHỔI LẬP TỨC!</strong><br>
                    Bệnh nhân đang sử dụng thuốc kháng đông liều đầy đủ (therapeutic anticoagulation). Không áp dụng các chiến lược dựa trên D-dimer (như PERC hay YEARS) vì D-dimer bị ảnh hưởng mạnh bởi thuốc kháng đông và có nguy cơ âm tính giả rất lớn.<br><br>
                    <strong>Hành động đề xuất:</strong> Chỉ định chụp CT động mạch phổi (CTPA) ngay lập tức hoặc Xạ hình phổi (V/Q SPECT) nếu có chống chỉ định để chẩn đoán xác định/loại trừ PE tái phát.
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<div class='section-card'>", unsafe_allow_html=True)
                st.write("🌿 **Nhánh chẩn đoán thay thế (Nếu chống chỉ định CTPA):**")
                st.caption("Nếu bệnh nhân có chống chỉ định tuyệt đối với CTPA (suy thận nặng CrCl < 30, dị ứng cản quang, có thai):")
                st.info("👉 **Khuyến cáo (Class 2a):** Thực hiện **Xạ hình thông khí - tưới máu phổi (V/Q Scan)**. Trong đó, **V/Q SPECT được khuyến cáo ưu tiên hơn V/Q phẳng thông thường (planar V/Q)** nhờ độ nhạy và độ đặc hiệu cao hơn đáng kể.")
                st.markdown("</div>", unsafe_allow_html=True)
                
            elif st.session_state.is_pregnant:
                # NHÁNH LOẠI TRỪ DÀNH RIÊNG CHO MANG THAI (PREGNANCY-ADAPTED YEARS) - HOÀN TOÀN TÁCH BIỆT!
                is_preg_cus_positive_val = st.session_state.saved_inputs.get('has_dvt_sym') and "DƯƠNG TÍNH" in st.session_state.saved_inputs.get('cus_result', '')
                
                if is_preg_cus_positive_val:
                    st.markdown("""
                    <div class='u-card urgency-low'>
                        <strong>✔️ CHẨN ĐOÁN ĐÃ XÁC LẬP BẰNG CUS DƯƠNG TÍNH</strong><br>
                        Siêu âm Doppler chân phát hiện thấy huyết khối. Thai phụ đã có bằng chứng VTE lâm sàng. 
                        Không có chỉ định thực hiện thêm xét nghiệm loại trừ D-dimer hay chẩn đoán hình ảnh phổi CTPA để tránh tia xạ tối đa (Class 1, LOE C-LD).
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
                    st.write("##### 🤰 Thuật toán YEARS thích ứng thai kỳ (Pregnancy-Adapted YEARS) (Class 2b, LOE B-NR)")
                    st.caption("Áp dụng riêng cho phụ nữ mang thai nghi ngờ PE để tối ưu hóa việc loại trừ và giảm thiểu chỉ định chụp CTPA nhiễm xạ.")
                    
                    has_dvt_sym_val = st.session_state.saved_inputs.get('has_dvt_sym', False)
                    st.write("**Đánh giá 3 tiêu chí YEARS:**")
                    st.write(f"- 1. Có dấu hiệu lâm sàng của DVT: **" + ("Có (Được tích chọn ở cột trái)" if has_dvt_sym_val else "Không") + "**")
                    y2 = persistent_checkbox("2. Có ho ra máu?", key="years_y2")
                    y3 = persistent_checkbox("3. PE là chẩn đoán khả thi nhất trên lâm sàng?", key="years_y3")
                    
                    years_count = (1 if has_dvt_sym_val else 0) + (1 if y2 else 0) + (1 if y3 else 0)
                    st.write(f"Số tiêu chí YEARS thỏa mãn: **{years_count}/3**")
                    
                    years_cutoff = 1000 if years_count == 0 else 500
                    st.write(f"Ngưỡng cắt D-dimer theo YEARS (cố định cho thai kỳ): **{years_cutoff} ng/mL**")
                    
                    d_dimer_val_preg = persistent_number_input("Nhập nồng độ D-dimer thực tế đo được (ng/mL):", 0, 50000, 0, key="d_dimer_val_preg")
                    
                    if d_dimer_val_preg > 0:
                        if d_dimer_val_preg < years_cutoff:
                            st.markdown(f"""
                            <div class='u-card' style='background-color: #F0FDF4; border-left: 5px solid #16A34A; color: #166534;'>
                                <strong>>>> KẾT LUẬN: D-dimer ({d_dimer_val_preg}) < Ngưỡng YEARS ({years_cutoff})</strong><br>
                                LOẠI TRỪ THUYÊN TẮC PHỔI (PE) THÀNH CÔNG! An toàn để không chụp CTPA cho thai phụ.
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div class='u-card' style='background-color: #FEF2F2; border-left: 5px solid #DC2626; color: #991B1B;'>
                                <strong>>>> KẾT LUẬN: D-dimer ({d_dimer_val_preg}) >= Ngưỡng YEARS ({years_cutoff})</strong><br>
                                CHỈ ĐỊNH HÌNH ẢNH HỌC PHỔI KHẨN CẤP! Khuyến cáo thực hiện <strong>CTPA liều thấp (low-dose CTPA)</strong> (Class 2a, LOE B-NR) hoặc <strong>Xạ hình phổi V/Q SPECT</strong> (Class 2a, LOE B-R).
                            </div>
                            """, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Phần hướng dẫn thay thế CTPA nếu có chống chỉ định
                    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
                    st.write("🌿 **Nhánh chẩn đoán thay thế (Nếu chống chỉ định CTPA):**")
                    st.caption("Nếu thai phụ mong muốn giảm thiểu tia xạ vú tối đa hoặc có chống chỉ định khác:")
                    st.info("👉 **Khuyến cáo (Class 2a):** Thực hiện **Xạ hình thông khí - tưới máu phổi (V/Q Scan)**. Trong đó, **V/Q SPECT được khuyến cáo ưu tiên hơn V/Q phẳng thông thường (planar V/Q)**.")
                    st.markdown("</div>", unsafe_allow_html=True)
                    
            else:
                # BỆNH NHÂN KHÔNG MANG THAI - DÙNG QUY TRÌNH LOẠI TRỪ TIÊU CHUẨN (PERC -> D-DIMER)
                st.write(f"Xác suất tiền nghiệm lâm sàng (CPTP): **{cptp_category}** (Điểm: {cptp_score})")
                
                # Sàng lọc bằng PERC nếu lâm sàng nguy cơ thấp
                if cptp_category == "LOW":
                    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
                    st.write("##### 🩺 Sàng lọc bằng Tiêu chí Loại trừ PERC (PE Rule-Out Criteria)")
                    st.caption("Nếu bệnh nhân thỏa mãn toàn bộ 8 tiêu chí bên dưới (tất cả là Không), có thể loại trừ PE hoàn toàn tại giường mà không cần làm D-dimer.")
                    
                    p1 = persistent_checkbox("1. Tuổi >= 50?", key="p1")
                    p2 = persistent_checkbox("2. Tần số tim >= 100 chu kỳ/phút?", key="p2")
                    p3 = persistent_checkbox("3. SpO2 ở khí trời < 95%?", key="p3")
                    p4 = persistent_checkbox("4. Sưng phù một bên chân?", key="p4")
                    p5 = persistent_checkbox("5. Ho ra máu?", key="p5")
                    p6 = persistent_checkbox("6. Chấn thương hoặc phẫu thuật lớn cần gây mê trong 4 tuần qua?", key="p6")
                    p7 = persistent_checkbox("7. Tiền sử bị DVT hoặc PE?", key="p7")
                    p8 = persistent_checkbox("8. Đang sử dụng estrogen (bao gồm tất cả các đường dùng: đường uống, miếng dán da, v.v.)?", key="p8")
                    
                    any_perc_positive = any([p1, p2, p3, p4, p5, p6, p7, p8])
                    
                    if not any_perc_positive:
                        st.markdown("""
                        <div class='u-card' style='background-color: #F0FDF4; border-left: 5px solid #16A34A; color: #166534;'>
                            <strong>>>> KẾT QUẢ PERC: ÂM TÍNH (LOẠI TRỪ PE HOÀN TOÀN)</strong><br>
                            Bệnh nhân thỏa mãn toàn bộ 8 tiêu chí loại trừ. LOẠI TRỪ PE TẠI GIƯỜNG BỆNH! Không cần làm D-dimer, không cần chụp CTPA.
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button("Xác nhận & Hoàn thành ca lâm sàng", type="primary"):
                            st.success("Ca lâm sàng đã được loại trừ an toàn.")
                        st.markdown("</div>", unsafe_allow_html=True)
                        st.stop()
                    else:
                        st.markdown("""
                        <div class='u-card urgency-medium'>
                            <strong>>>> KẾT QUẢ PERC: DƯƠNG TÍNH</strong><br>
                            Không thể loại trừ bằng PERC. Bắt buộc phải thực hiện xét nghiệm D-dimer theo một trong hai chiến lược bên dưới.
                        </div>
                        """, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                # Đánh giá D-dimer
                if cptp_category in ["LOW", "INTERMEDIATE"]:
                    if cptp_category == "LOW" and not any_perc_positive:
                        pass
                    else:
                        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
                        st.write("##### 🧪 Định lượng và Loại trừ bằng D-dimer")
                        
                        strategy = persistent_selectbox("Chọn chiến lược diễn giải D-dimer:", [
                            "Chiến lược A: Age-Adjusted D-dimer (Hiệu chỉnh theo tuổi)",
                            "Chiến lược B: Thuật toán YEARS thích ứng (YEARS Algorithm)"
                        ], key="strategy")
                        
                        if "Age-Adjusted" in strategy:
                            st.info("Chiến lược A: Age-Adjusted D-dimer (Class 2a, LOE B-R)")
                            age = persistent_number_input("Nhập tuổi bệnh nhân để tính ngưỡng cắt:", 18, 120, 60, key="age_dd")
                            cutoff_a = 500 if age <= 50 else age * 10
                            st.write(f"Ngưỡng cắt D-dimer đề xuất: **{cutoff_a} ng/mL**")
                            
                            d_dimer_val_a = persistent_number_input("Nhập nồng độ D-dimer thực tế đo được (ng/mL):", 0, 50000, 0, key="d_dimer_strategy_a")
                            
                            if d_dimer_val_a > 0:
                                if d_dimer_val_a < cutoff_a:
                                    st.markdown(f"""
                                    <div class='u-card' style='background-color: #F0FDF4; border-left: 5px solid #16A34A; color: #166534;'>
                                        <strong>>>> KẾT LUẬN: D-dimer ({d_dimer_val_a}) < Ngưỡng cắt ({cutoff_a})</strong><br>
                                        LOẠI TRỪ THUYÊN TẮC PHỔI (PE) THÀNH CÔNG! An toàn để KHÔNG chụp CTPA.
                                    </div>
                                    """, unsafe_allow_html=True)
                                else:
                                    st.markdown(f"""
                                    <div class='u-card' style='background-color: #FEF2F2; border-left: 5px solid #DC2626; color: #991B1B;'>
                                        <strong>>>> KẾT LUẬN: D-dimer ({d_dimer_val_a}) >= Ngưỡng cắt ({cutoff_a})</strong><br>
                                        CHỈ ĐỊNH HÌNH ẢNH HỌC (CTPA) ĐỂ XÁC ĐỊNH CHẨN ĐOÁN!
                                    </div>
                                    """, unsafe_allow_html=True)
                        
                        else: # YEARS
                            st.info("Chiến lược B: Thuật toán YEARS tiêu chuẩn (Class 2a, LOE B-R)")
                            st.write("Đánh giá 3 tiêu chí YEARS:")
                            y1 = persistent_checkbox("1. Có dấu hiệu lâm sàng của DVT (sưng đau chân)?", key="years_y1")
                            y2 = persistent_checkbox("2. Có ho ra máu?", key="years_y2")
                            y3 = persistent_checkbox("3. PE là chẩn đoán khả thi nhất trên lâm sàng?", key="years_y3")
                            
                            years_count = (1 if y1 else 0) + (1 if y2 else 0) + (1 if y3 else 0)
                            st.write(f"Số tiêu chí YEARS thỏa mãn: **{years_count}/3**")
                            
                            years_cutoff = 1000 if years_count == 0 else 500
                            st.write(f"Ngưỡng cắt D-dimer theo YEARS (cố định): **{years_cutoff} ng/mL**")
                            
                            d_dimer_val_b = persistent_number_input("Nhập nồng độ D-dimer thực tế đo được (ng/mL):", 0, 50000, 0, key="d_dimer_strategy_b")
                            
                            if d_dimer_val_b > 0:
                                if d_dimer_val_b < years_cutoff:
                                    st.markdown(f"""
                                    <div class='u-card' style='background-color: #F0FDF4; border-left: 5px solid #16A34A; color: #166534;'>
                                        <strong>>>> KẾT LUẬN: D-dimer ({d_dimer_val_b}) < Ngưỡng YEARS ({years_cutoff})</strong><br>
                                        LOẠI TRỪ THUYÊN TẮC PHỔI (PE) THÀNH CÔNG! An toàn để không chụp CTPA.
                                    </div>
                                    """, unsafe_allow_html=True)
                                else:
                                    st.markdown(f"""
                                    <div class='u-card' style='background-color: #FEF2F2; border-left: 5px solid #DC2626; color: #991B1B;'>
                                        <strong>>>> KẾT LUẬN: D-dimer ({d_dimer_val_b}) >= Ngưỡng YEARS ({years_cutoff})</strong><br>
                                        CHỈ ĐỊNH HÌNH ẢNH HỌC (CTPA) ĐỂ XÁC ĐỊNH CHẨN ĐOÁN!
                                    </div>
                                    """, unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                elif cptp_category == "HIGH":
                    st.markdown("""
                    <div class='u-card' style='background-color: #FEF2F2; border-left: 5px solid #DC2626; color: #991B1B;'>
                        <strong>>>> KẾT LUẬN: CHỈ ĐỊNH CHỤP HÌNH ẢNH HỌC PHỔI KHẨN CẤP LẬP TỨC!</strong><br>
                        Bệnh nhân có xác suất lâm sàng rất cao (Wells > 6 hoặc Geneva > 4). Tiến hành chụp CT động mạch phổi (CTPA) ngay mà không làm D-dimer.
                    </div>
                    """, unsafe_allow_html=True)
                    
                # Phần hướng dẫn thay thế CTPA nếu có chống chỉ định
                st.markdown("<div class='section-card'>", unsafe_allow_html=True)
                st.write("🌿 **Nhánh chẩn đoán thay thế (Nếu chống chỉ định CTPA):**")
                st.caption("Nếu bệnh nhân có chống chỉ định tuyệt đối với CTPA (suy thận nặng CrCl < 30, dị ứng thuốc cản quang có iod, v.v.):")
                st.info("👉 **Khuyến cáo (Class 2a):** Thực hiện **Xạ hình thông khí - tưới máu phổi (V/Q Scan)**. Trong đó, **V/Q SPECT được khuyến cáo ưu tiên hơn V/Q phẳng thông thường (planar V/Q)**.")
                st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("---")
    col_nav = st.columns([4, 1])
    with col_nav[1]:
        if st.button("Tiếp tục sang GĐ 2 ➡️", use_container_width=True, type="primary"):
            st.session_state.step = 2
            st.session_state.step2_focus = "hemo"
            st.rerun()

# ==============================================================================
# BƯỚC 2: PHÂN LOẠI LÂM SÀNG CẤP TÍNH AHA/ACC 2026 (RẼ NHÁNH TUẦN TỰ)
# ==============================================================================
if render_main_step_header("📊 BƯỚC 2: PHÂN LOẠI LÂM SÀNG AHA 2026", 2):

    hemo_options = [
        "Huyết động ổn định (Huyết áp bình thường)",
        "Tụt huyết áp thoáng qua (<15 phút, tự hồi phục nhanh hoặc đáp ứng nhanh sau bù dịch)",
        "Tụt huyết áp kéo dài / Sốc tim thực sự (Huyết áp tâm thu <90 mmHg hoặc giảm >40 mmHg kéo dài >=15 phút, hoặc cần thuốc vận mạch để duy trì HA)",
        "Sốc tim kháng trị hoặc Ngừng tuần hoàn (SCAI Stage D/E, hoặc cardiac arrest không đạt ROSC sau 30 phút hồi sức)",
        "Thuyên tắc phổi phát hiện tình cờ, hoàn toàn không có triệu chứng (Category A - Subclinical PE)"
    ]
    primary_hemo = st.session_state.saved_inputs.get("primary_hemo", hemo_options[0])
    if primary_hemo not in hemo_options:
        primary_hemo = hemo_options[0]

    if render_step2_sub_header("🧬 Đánh giá Huyết động học & Tim phổi cấp cứu", "hemo"):
        # Heading phía trên đã mô tả nhiệm vụ; dropdown được làm nổi bật và không lặp lại câu "Hãy chọn...".
        primary_hemo = persistent_selectbox(
            "Trạng thái huyết động chính", hemo_options, key="primary_hemo", label_visibility="collapsed"
        )
        
        # RESET FLOW STATE IF HEMODYNAMIC TYPE CHANGED TO PREVENT C-GROUP SLIPPAGE
        if 'last_primary_hemo' not in st.session_state:
            st.session_state.last_primary_hemo = primary_hemo
            
        if primary_hemo != st.session_state.last_primary_hemo:
            st.session_state.last_primary_hemo = primary_hemo
            st.session_state.g2_stable_flow = "organ_damage"
            st.session_state.final_category = None
            st.session_state.resp_modifier = False
            st.session_state.step2_focus = "hemo"
            st.rerun()
        if "Sốc tim kháng trị" in primary_hemo:
            st.session_state.final_category = "E2"
            st.markdown("""
            <div class='u-card urgency-high'>
                <strong>>>> CHẨN ĐOÁN LÂM SÀNG: NHÓM E2 (Suy tim phổi hoàn toàn - Sốc kháng trị / Ngừng tuần hoàn)</strong><br>
                <em>Định nghĩa:</em> Sốc tim kháng trị (SCAI Stage D hoặc E) hoặc ngừng tuần hoàn (cardiac arrest) không đạt ROSC sau 30 phút hồi sức tích cực. Đòi hỏi hồi sức nâng cao khẩn cấp.
            </div>
            """, unsafe_allow_html=True)
        elif "Tụt huyết áp kéo dài" in primary_hemo:
            st.session_state.final_category = "E1"
            st.markdown("""
            <div class='u-card urgency-high'>
                <strong>>>> CHẨN ĐOÁN LÂM SÀNG: NHÓM E1 (Suy tim phổi hoàn toàn - Sốc tim thực sự)</strong><br>
                <em>Định nghĩa:</em> Sốc tim hoặc tụt huyết áp kéo dài (HA tâm thu <90 mmHg hoặc giảm >40 mmHg kéo dài >=15 phút, hoặc cần dùng vận mạch). Cần điều trị tích cực tại ICU.
            </div>
            """, unsafe_allow_html=True)
        elif "phát hiện tình cờ" in primary_hemo:
            st.session_state.final_category = "A"
            st.markdown("""
            <div class='u-card urgency-low'>
                <strong>>>> CHẨN ĐOÁN LÂM SÀNG: NHÓM A (Thuyên tắc phổi dưới lâm sàng - Subclinical PE)</strong><br>
                Bệnh nhân hoàn toàn không có triệu chứng nghi ngờ và được phát hiện tình cờ trên CTPA khi thực hiện vì mục đích khác.
            </div>
            """, unsafe_allow_html=True)
            st.session_state.resp_modifier = False
        if st.button("Xác nhận trạng thái huyết động → Tiếp tục", type="primary", use_container_width=True, key="confirm_primary_hemo"):
            if "Sốc tim kháng trị" in primary_hemo or "Tụt huyết áp kéo dài" in primary_hemo or "phát hiện tình cờ" in primary_hemo:
                st.session_state.step2_focus = "branch"
            else:
                st.session_state.step2_focus = "organ_damage"
                st.session_state.g2_stable_flow = "organ_damage"
            st.rerun()
    if "Sốc tim kháng trị" in primary_hemo:
        if render_step2_sub_header("📢 Đánh giá Modifier R cho nhóm E", "branch"):
            st.write("##### 📢 Đánh giá Modifier R cho nhóm E")
            r_e = persistent_checkbox("Đang cần thông khí áp lực dương không xâm lấn (NIV/BiPAP) HOẶC đang phải thông khí xâm lấn (đặt nội khí quản thở máy)?", key="r_e")
            st.session_state.resp_modifier = r_e
            
            if st.button("Xác nhận & Đi tới Bước 3: Điều trị ➡️", type="primary", use_container_width=True, key="to_step3_e2"):
                st.session_state.step = 3
                st.rerun()
    elif "Tụt huyết áp kéo dài" in primary_hemo:
        if render_step2_sub_header("📢 Đánh giá Modifier R cho nhóm E", "branch"):
            st.write("##### 📢 Đánh giá Modifier R cho nhóm E")
            r_e = persistent_checkbox("Đang cần thông khí áp lực dương không xâm lấn (NIV/BiPAP) HOẶC đang phải thông khí xâm lấn (đặt nội khí quản thở máy)?", key="r_e")
            st.session_state.resp_modifier = r_e
            
            if st.button("Xác nhận & Đi tới Bước 3: Điều trị ➡️", type="primary", use_container_width=True, key="to_step3_e1"):
                st.session_state.step = 3
                st.rerun()
    elif "phát hiện tình cờ" in primary_hemo:
        if render_step2_sub_header("📋 Đánh giá Tiêu chuẩn An toàn Điều trị Ngoại trú cho Nhóm A", "branch"):
            st.markdown("<div class='section-card'>", unsafe_allow_html=True)
            st.write("##### 📋 Đánh giá Tiêu chuẩn An toàn Điều trị Ngoại trú cho Nhóm A")
            st.caption("Khuyến cáo AHA/ACC 2026 cho phép quản lý ngoại trú (Class 2a, LOE B-R) cho một số bệnh nhân được lựa chọn thuộc Nhóm A khi thỏa mãn đầy đủ các tiêu chuẩn y khoa và xã hội dưới đây:")
            
            st.write("**1. Sàng lọc Y khoa (sPESI hoặc Hestia):**")
            a_score_method = persistent_selectbox("Chọn thang điểm sàng lọc y khoa cho Nhóm A:", [
                "Đánh giá bằng sPESI (Simplified PESI) - Đòi hỏi sPESI = 0",
                "Đánh giá bằng Tiêu chí Hestia (11 mục loại trừ) - Đòi hỏi Hestia = 0"
            ], key="a_score_method")
            
            is_a_medical_safe = False
            
            if "sPESI" in a_score_method:
                st.info("Tính sPESI cho Nhóm A (Mỗi tiêu chí dương tính tính 1 điểm):")
                as1 = persistent_checkbox("Tuổi > 80", key="as1")
                as2 = persistent_checkbox("Tiền sử ung thư đang tiến triển", key="as2")
                as3 = persistent_checkbox("Tiền sử bệnh tim phổi mạn tính (suy tim/COPD...)", key="as3")
                as4 = persistent_checkbox("Tần số tim >= 110 chu kỳ/phút", key="as4")
                as5 = persistent_checkbox("Huyết áp tâm thu < 100 mmHg", key="as5")
                as6 = persistent_checkbox("SpO2 < 90% (hoặc cần oxy hỗ trợ)", key="as6")
                
                aspesi_score = sum([as1, as2, as3, as4, as5, as6])
                st.metric("Tổng điểm sPESI cho Nhóm A", f"{aspesi_score} điểm")
                is_a_medical_safe = (aspesi_score == 0)
                if is_a_medical_safe:
                    st.success("✔️ sPESI = 0 điểm (Nguy cơ thấp). Đủ tiêu chuẩn y khoa!")
                else:
                    st.error("❌ sPESI >= 1 điểm (Nguy cơ cao). Không khuyến cáo điều trị ngoại trú.")
            else:
                st.info("Sàng lọc tiêu chí Hestia cho Nhóm A (Đòi hỏi tất cả câu hỏi là 'Không'):")
                ah1 = persistent_checkbox("1. Huyết động không ổn định (cần vận mạch, bù dịch truyền, đặt ống, CPR)?", key="ah1")
                ah2 = persistent_checkbox("2. Cần dùng tiêu sợi huyết hoặc phẫu thuật lấy huyết khối?", key="ah2")
                ah3 = persistent_checkbox("3. Nguy cơ chảy máu cao hoặc đang chảy máu hoạt động?", key="ah3")
                ah4 = persistent_checkbox("4. Cần thở oxy hỗ trợ liên tục >24h để duy trì SpO2 >90%?", key="ah4")
                ah5 = persistent_checkbox("5. PE khởi phát khi đang dùng kháng đông liều đầy đủ?", key="ah5")
                ah6 = persistent_checkbox("6. Đau ngực dữ dội cần dùng thuốc giảm đau opioid đường truyền tĩnh mạch >24h?", key="ah6")
                ah7 = persistent_checkbox("7. Có lý do y khoa hoặc xã hội cần nhập viện kéo dài >24h?", key="ah7")
                ah8 = persistent_checkbox("8. Độ thanh thải Creatinine CrCl < 30 mL/phút?", key="ah8")
                ah9 = persistent_checkbox("9. Có suy gan nặng?", key="ah9")
                ah10 = persistent_checkbox("10. Bệnh nhân đang mang thai?", key="ah10")
                ah11 = persistent_checkbox("11. Tiền sử giảm tiểu cầu do Heparin (HIT)?", key="ah11")
                
                ahestia_positive = any([ah1, ah2, ah3, ah4, ah5, ah6, ah7, ah8, ah9, ah10, ah11])
                is_a_medical_safe = not ahestia_positive
                if is_a_medical_safe:
                    st.success("✔️ Tất cả câu hỏi Hestia là 'Không'. Đủ tiêu chuẩn y khoa!")
                else:
                    st.error("❌ Hestia dương tính. Bệnh nhân cần nhập viện ngắn ngày.")
                    
            st.write("---")
            st.write("**2. Tiêu chuẩn Xã hội & Điều kiện Theo dõi (Bắt buộc):**")
            asoc1 = persistent_checkbox("Bệnh nhân có điều kiện gia đình, xã hội ổn định, có người hỗ trợ?", key="asoc1")
            asoc2 = persistent_checkbox("Tiếp cận thuốc kháng đông ngay lập tức và thuận tiện?", key="asoc2")
            asoc3 = persistent_checkbox("Có kế hoạch theo dõi y khoa và hẹn tái khám chuyên khoa nhanh chóng, tin cậy (trong vòng 24-72 giờ)?", key="asoc3")
            
            is_a_social_safe = asoc1 and asoc2 and asoc3
            
            if is_a_medical_safe and is_a_social_safe:
                st.markdown("<div class='u-card' style='background-color: #F0FDF4; border-left: 5px solid #16A34A; color: #166534;'><strong>✔️ ĐỦ TIÊU CHUẨN ĐIỀU TRỊ NGOẠI TRÚ (Class 2a, LOE B-R)</strong><br>Bệnh nhân thỏa mãn đầy đủ điều kiện y khoa và xã hội để quản lý ngoại trú an toàn.</div>", unsafe_allow_html=True)
                if st.button("Xác nhận & Đi tới Bước 3: Điều trị ➡️", type="primary", use_container_width=True, key="to_step3_organ"):
                    st.session_state.step = 3
                    st.rerun()
            else:
                st.markdown("<div class='u-card urgency-high'><strong>❌ CHƯA ĐỦ ĐIỀU KIỆN ĐIỀU TRỊ NGOẠI TRÚ</strong><br>Khuyến cáo điều trị nội trú ngắn ngày tại khoa Thường do chưa thỏa mãn đủ các điều kiện y khoa hoặc xã hội.</div>", unsafe_allow_html=True)
                if st.button("Vẫn xác nhận & Đi tới Bước 3 để tính liều điều trị nội trú ➡️", type="secondary", use_container_width=True):
                    st.session_state.step = 3
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
    if primary_hemo in ["Huyết động ổn định (Huyết áp bình thường)", "Tụt huyết áp thoáng qua (<15 phút, tự hồi phục nhanh hoặc đáp ứng nhanh sau bù dịch)"]:
        if primary_hemo == "Tụt huyết áp thoáng qua (<15 phút, tự hồi phục nhanh hoặc đáp ứng nhanh sau bù dịch)":
            st.session_state.g2_stable_flow = "organ_damage"
        _flow = st.session_state.g2_stable_flow
        _flow_rank = {"organ_damage": 1, "cpes": 2, "prognosis": 3, "rv_biomarkers": 4, "hk_position": 4}.get(_flow, 1)
        if render_step2_sub_header("2.1 📋 Đánh giá Tổn thương cơ quan đích & Giảm tưới máu mô", "organ_damage"):
            st.caption("Hãy rà soát kỹ các dấu hiệu giảm tưới máu hoặc suy chức năng cơ quan đích dưới đây:")
            
            opt_lactate = persistent_checkbox("Nồng độ Lactate huyết thanh > 2.0 mmol/L", key="opt_lactate")
            opt_aki = persistent_checkbox("Suy thận cấp (AKI) (Creatinine tăng >= 0.3 mg/dL hoặc gấp >= 1.5 lần nền trong 24h)", key="opt_aki")
            opt_oliguria = persistent_checkbox("Thiểu niệu tiến triển (Lượng nước tiểu < 0.5 mL/kg/giờ kéo dài >= 2 giờ)", key="opt_oliguria")
            opt_mental = persistent_checkbox("Thay đổi trạng thái tâm thần cấp tính (lờ đờ, u ám, ngủ gà, vật vã do thiếu máu não)", key="opt_mental")
            opt_ci_map = persistent_checkbox("Huyết áp trung bình MAP < 60 mmHg HOẶC Chỉ số tim (Cardiac Index) <= 2.2 L/min/m²", key="opt_ci_map")
            
            has_hypoperfusion = opt_lactate or opt_aki or opt_oliguria or opt_mental or opt_ci_map
            
            if has_hypoperfusion:
                st.session_state.final_category = "D2"
                st.markdown("""
                <div class='u-card urgency-high'>
                    <strong>>>> CHẨN ĐOÁN LÂM SÀNG: NHÓM D2 (Sốc ẩn - Incipient Cardiopulmonary Failure)</strong><br>
                    Phát hiện thấy bằng chứng giảm tưới máu mô/tổn thương cơ quan đích mặc dù huyết áp vẫn đang được cơ thể bù trừ. Bệnh nhân có nguy cơ sụp đổ tuần hoàn cao!
                </div>
                """, unsafe_allow_html=True)
                
                # Đánh giá Respiratory Modifier cho nhóm D
                st.write("---")
                st.write("##### 📢 Đánh giá Modifier R cho nhóm D")
                r_d = persistent_checkbox("Cần hỗ trợ oxy lưu lượng >6 L/phút qua gọng mũi thường HOẶC mặt nạ không thở lại (NRB)?", key="r_d")
                st.session_state.resp_modifier = r_d
                
                if st.button("Xác nhận & Đi tới Bước 3: Điều trị ➡️", type="primary", use_container_width=True, key="to_step3_organ_d1"):
                    st.session_state.step = 3
                    st.rerun()
            else:
                st.success("Không phát hiện dấu hiệu giảm tưới máu cơ quan đích nào.")
                
                if primary_hemo == "Tụt huyết áp thoáng qua (<15 phút, tự hồi phục nhanh hoặc đáp ứng nhanh sau bù dịch)":
                    # Tụt HA thoáng qua + Không giảm tưới máu -> D1
                    st.session_state.final_category = "D1"
                    st.markdown("""
                    <div class='u-card urgency-medium'>
                        <strong>>>> CHẨN ĐOÁN LÂM SÀNG: NHÓM D1 (Tụt huyết áp thoáng qua)</strong><br>
                        Huyết động có biểu hiện mất bù thoáng qua nhưng chưa tiến triển thành tổn thương cơ quan đích.
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Đánh giá Respiratory Modifier cho nhóm D
                    st.write("---")
                    st.write("##### 📢 Đánh giá Modifier R cho nhóm D")
                    r_d = persistent_checkbox("Cần hỗ trợ oxy lưu lượng >6 L/phút qua gọng mũi thường HOẶC mặt nạ không thở lại (NRB)?", key="r_d")
                    st.session_state.resp_modifier = r_d
                    
                    if st.button("Xác nhận & Đi tới Bước 3: Điều trị ➡️", type="primary", use_container_width=True, key="to_step3_cpes"):
                        st.session_state.step = 3
                        st.rerun()
                else:
                    # Huyết áp bình thường + Không giảm tưới máu -> Đánh giá CPES
                    st.info("Huyết áp bình thường và không có giảm tưới máu. Hãy bấm nút dưới đây để chuyển sang đánh giá thang điểm CPES.")
                    if st.button("Xác nhận Không giảm tưới máu -> Tiếp tục đánh giá CPES ➡️", type="primary", use_container_width=True):
                        st.session_state.g2_stable_flow = "cpes"
                        st.session_state.step2_focus = "cpes"
                        st.rerun()
        if primary_hemo == "Huyết động ổn định (Huyết áp bình thường)" and _flow_rank >= 2:
            if render_step2_sub_header("2.2 📊 Đánh giá Thang điểm CPES (Composite Pulmonary Embolism Shock)", "cpes"):
                st.caption("CPES (0-6 điểm) giúp sàng lọc sớm nguy cơ tiến triển thành Sốc ẩn ở bệnh nhân có huyết áp ổn định và không có tổn thương cơ quan trước đó.")
                
                c1 = persistent_checkbox("1. Tăng men tim Troponin tim (+1)", key="c1")
                c2 = persistent_checkbox("2. Tăng peptide lợi niệu BNP hoặc NT-proBNP (+1)", key="c2")
                c3 = persistent_checkbox("3. Giảm chức năng RV mức độ trung bình hoặc nặng trên siêu âm (+1)", key="c3")
                c4 = persistent_checkbox("4. Có gánh nặng huyết khối trung tâm (Saddle PE) trên CTPA (+1)", key="c4")
                c5 = persistent_checkbox("5. Có huyết khối tĩnh mạch sâu (DVT) đoạn gần kèm theo (+1)", key="c5")
                c6 = persistent_checkbox("6. Tần số tim >= 100 chu kỳ/phút (+1)", key="c6")
                
                cpes_score = sum([c1, c2, c3, c4, c5, c6])
                st.metric("Tổng điểm CPES", f"{cpes_score}/6 điểm")
                
                if cpes_score == 6:
                    st.markdown("""
                    <div class='u-card urgency-high'>
                        <strong>>>> ĐẠT ĐIỂM CPES TỐI ĐA 6/6!</strong><br>
                        Bệnh nhân đạt CPES 6/6 -> Tự động quy đổi phân loại vào <strong>Nhóm D2 (Sốc ẩn - Nguy cơ rất cao)</strong> theo AHA/ACC 2026.
                    </div>
                    """, unsafe_allow_html=True)
                    st.session_state.final_category = "D2"
                    
                    # Đánh giá Respiratory Modifier cho nhóm D
                    st.write("---")
                    st.write("##### 📢 Đánh giá Modifier R cho nhóm D")
                    r_d = persistent_checkbox("Cần hỗ trợ oxy lưu lượng >6 L/phút qua gọng mũi thường HOẶC mặt nạ không thở lại (NRB)?", key="r_d")
                    st.session_state.resp_modifier = r_d
                    
                    if st.button("Xác nhận & Đi tới Bước 3: Điều trị ➡️", type="primary", use_container_width=True):
                        st.session_state.step = 3
                        st.rerun()
                else:
                    st.info(f"Điểm CPES = {cpes_score}/6 (< 6/6). Hãy tiếp tục chuyển sang đánh giá các thang điểm tiên lượng lâm sàng để phân loại nhóm B hay C.")
                    if st.button("Xác nhận CPES < 6 -> Đánh giá Thang điểm Tiên lượng Lâm sàng ➡️", type="primary", use_container_width=True):
                        st.session_state.g2_stable_flow = "prognosis"
                        st.session_state.step2_focus = "prognosis"
                        st.rerun()
                        
                if st.button("⬅️ Quay lại đánh giá Tổn thương cơ quan", type="secondary"):
                    st.session_state.g2_stable_flow = "organ_damage"
                    st.session_state.step2_focus = "organ_damage"
                    st.rerun()
        if primary_hemo == "Huyết động ổn định (Huyết áp bình thường)" and _flow_rank >= 3:
            if render_step2_sub_header("2.3 📋 Đánh giá Thang điểm Tiên lượng Lâm sàng", "prognosis"):
                st.write("##### 📋 BƯỚC 2.3: Đánh giá Thang điểm Tiên lượng Lâm sàng")
                st.caption("Do không có giảm tưới máu/sốc ẩn, bệnh nhân sẽ được phân loại vào Nhóm B (Nguy cơ thấp) hoặc Nhóm C (Nguy cơ trung bình). Hãy lựa chọn 1 thang điểm duy nhất để đánh giá:")
                
                score_method = persistent_selectbox("Chọn thang điểm tiên lượng lâm sàng:", [
                    "sPESI (Simplified PESI) - Rút gọn, nhanh chóng",
                    "PESI Đầy đủ (11 tiêu chí)",
                    "Tiêu chí Hestia (11 mục loại trừ chuẩn)",
                    "Thang điểm Bova (Dành cho bệnh nhân huyết động ổn)"
                ], key="score_method")
                
                is_clinical_high = False
                
                if "sPESI" in score_method:
                    st.info("Tính điểm sPESI (Mỗi tiêu chí dương tính tính 1 điểm):")
                    sp1 = persistent_checkbox("Tuổi > 80", key="sp1")
                    sp2 = persistent_checkbox("Tiền sử ung thư đang tiến triển", key="sp2")
                    sp3 = persistent_checkbox("Tiền sử bệnh tim phổi mạn tính (suy tim mạn/COPD/bệnh phổi kẽ...)", key="sp3")
                    sp4 = persistent_checkbox("Tần số tim >= 110 chu kỳ/phút", key="sp4")
                    sp5 = persistent_checkbox("Huyết áp tâm thu < 100 mmHg", key="sp5")
                    sp6 = persistent_checkbox("SpO2 < 90% (hoặc cần oxy hỗ trợ)", key="sp6")
                    
                    spesi_score = sum([sp1, sp2, sp3, sp4, sp5, sp6])
                    st.metric("Tổng điểm sPESI", f"{spesi_score} điểm")
                    is_clinical_high = spesi_score >= 1
                    
                elif "PESI Đầy đủ" in score_method:
                    st.info("Tính điểm PESI Đầy đủ (11 tiêu chí chuẩn):")
                    pesi_age = persistent_number_input("Nhập tuổi bệnh nhân:", 18, 120, 60, key="pesi_age_raw")
                    pesi_gender = persistent_radio("Giới tính sinh học:", ["Nam (+10)", "Nữ (0)"], key="pesi_gender")
                    pesi_cancer = persistent_checkbox("Ung thư tiến triển (+30)", key="pesi_cancer")
                    pesi_hf = persistent_checkbox("Tiền sử suy tim mạn tính (+10)", key="pesi_hf")
                    pesi_lung = persistent_checkbox("Bệnh phổi mạn tính (+10)", key="pesi_lung")
                    pesi_hr = persistent_checkbox("Tần số tim >= 110 ck/phút (+20)", key="pesi_hr")
                    pesi_sbp = persistent_checkbox("Huyết áp tâm thu < 100 mmHg (+30)", key="pesi_sbp")
                    pesi_rr = persistent_checkbox("Tần số thở >= 30 lần/phút (+20)", key="pesi_rr")
                    pesi_temp = persistent_checkbox("Nhiệt độ cơ thể < 36 độ C (+20)", key="pesi_temp")
                    pesi_mental = persistent_checkbox("Thay đổi trạng thái tâm thần (lẫn lộn, u ám, ngủ gà) (+60)", key="pesi_mental")
                    pesi_spo2 = persistent_checkbox("SpO2 < 90% (+20)", key="pesi_spo2")
                    
                    pesi_score = pesi_age
                    if pesi_gender == "Nam (+10)": pesi_score += 10
                    if pesi_cancer: pesi_score += 30
                    if pesi_hf: pesi_score += 10
                    if pesi_lung: pesi_score += 10
                    if pesi_hr: pesi_score += 20
                    if pesi_sbp: pesi_score += 30
                    if pesi_rr: pesi_score += 20
                    if pesi_temp: pesi_score += 20
                    if pesi_mental: pesi_score += 60
                    if pesi_spo2: pesi_score += 20
                    
                    st.metric("Tổng điểm PESI", f"{pesi_score} điểm")
                    
                    pesi_class = "I"
                    if pesi_score <= 65: pesi_class = "I"
                    elif pesi_score <= 85: pesi_class = "II"
                    elif pesi_score <= 105: pesi_class = "III"
                    elif pesi_score <= 125: pesi_class = "IV"
                    else: pesi_class = "V"
                    
                    st.write(f"Phân loại PESI: **Class {pesi_class}**")
                    is_clinical_high = pesi_score > 85 # Class III trở lên là nguy cơ cao lâm sàng (C)
                    
                elif "Hestia" in score_method:
                    st.info("Sàng lọc tiêu chí Hestia (11 mục loại trừ chuẩn - Table 6):")
                    h1 = persistent_checkbox("1. Huyết động không ổn định (cần vận mạch, bù dịch truyền, đặt ống, CPR)?", key="h1")
                    h2 = persistent_checkbox("2. Cần dùng tiêu sợi huyết hoặc phẫu thuật lấy huyết khối?", key="h2")
                    h3 = persistent_checkbox("3. Nguy cơ chảy máu cao hoặc đang chảy máu hoạt động?", key="h3")
                    h4 = persistent_checkbox("4. Cần thở oxy hỗ trợ liên tục >24h để duy trì SpO2 >90%?", key="h4")
                    h5 = persistent_checkbox("5. PE khởi phát khi đang dùng kháng đông liều đầy đủ?", key="h5")
                    h6 = persistent_checkbox("6. Đau ngực dữ dội cần dùng thuốc giảm đau opioid đường truyền tĩnh mạch >24h?", key="h6")
                    h7 = persistent_checkbox("7. Có lý do y khoa hoặc xã hội cần nhập viện kéo dài >24h (ví dụ: nhiễm trùng đồng mắc)?", key="h7")
                    h8 = persistent_checkbox("8. Độ thanh thải Creatinine CrCl < 30 mL/phút?", key="h8")
                    h9 = persistent_checkbox("9. Có suy gan nặng?", key="h9")
                    h10 = persistent_checkbox("10. Bệnh nhân đang mang thai?", key="h10")
                    h11 = persistent_checkbox("11. Tiền sử giảm tiểu cầu do Heparin (HIT)?", key="h11")
                    
                    hestia_positive = any([h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11])
                    if hestia_positive:
                        st.error("Hestia dương tính (Có ít nhất 1 câu trả lời 'Có'): Bệnh nhân không thể điều trị ngoại trú -> Xếp vào nguy cơ trung bình (Nhóm C).")
                        is_clinical_high = True
                    else:
                        st.success("Tất cả câu trả lời là 'Không'. Hestia âm tính: Đủ điều kiện xem xét điều trị ngoại trú an toàn (Nhóm B).")
                        is_clinical_high = False
                        
                else: # Bova
                    st.info("Tính điểm Bova (Dành cho bệnh nhân huyết động ổn định - Table 6):")
                    b1 = persistent_checkbox("1. Tần số tim >= 110 chu kỳ/phút (+1)", key="b1")
                    b2 = persistent_checkbox("2. Huyết áp tâm thu 90 - 100 mmHg (+2)", key="b2")
                    b3 = persistent_checkbox("3. Có tăng men tim Troponin (+2)", key="b3")
                    b4 = persistent_checkbox("4. Có rối loạn chức năng thất phải trên siêu âm hoặc CTPA (+2)", key="b4")
                    
                    bova_score = (1 if b1 else 0) + (2 if b2 else 0) + (2 if b3 else 0) + (2 if b4 else 0)
                    st.metric("Tổng điểm Bova", f"{bova_score} điểm")
                    is_clinical_high = bova_score > 4 # Bova Stage III (>4đ) là nguy cơ trung bình-cao (C)

                st.write("---")
                if is_clinical_high:
                    st.markdown("<div class='u-card urgency-medium'><strong>KẾT QUẢ ĐÁNH GIÁ: LÂM SÀNG NGUY CƠ CAO (Category C)</strong><br>Thang điểm tiên lượng lâm sàng chỉ ra nguy cơ cao. Bệnh nhân được xếp vào Nhóm C. Hãy bấm nút dưới đây để đánh giá Thất phải (RV) và Biomarkers để phân nhóm sâu hơn (C1, C2, C3).</div>", unsafe_allow_html=True)
                    if st.button("Đánh giá Thất phải (RV) & Biomarkers ➡️", type="primary", use_container_width=True):
                        st.session_state.g2_stable_flow = "rv_biomarkers"
                        st.session_state.step2_focus = "rv_biomarkers"
                        st.rerun()
                else:
                    st.markdown("<div class='u-card urgency-low'><strong>KẾT QUẢ ĐÁNH GIÁ: LÂM SÀNG NGUY CƠ THẤP (Category B)</strong><br>Thang điểm tiên lượng lâm sàng chỉ ra nguy cơ thấp. Bệnh nhân được xếp vào Nhóm B. Hãy bấm nút dưới đây để đánh giá vị trí huyết khối để phân loại B1 hay B2.</div>", unsafe_allow_html=True)
                    if st.button("Đánh giá vị trí huyết khối ➡️", type="primary", use_container_width=True):
                        st.session_state.g2_stable_flow = "hk_position"
                        st.session_state.step2_focus = "hk_position"
                        st.rerun()
                        
                if st.button("⬅️ Quay lại đánh giá CPES", type="secondary"):
                    st.session_state.g2_stable_flow = "cpes"
                    st.session_state.step2_focus = "cpes"
                    st.rerun()
        if primary_hemo == "Huyết động ổn định (Huyết áp bình thường)" and _flow == "rv_biomarkers":
            if render_step2_sub_header("2.4 🧬 Đánh giá Thất phải (RV) & Biomarkers — Nhóm C", "rv_biomarkers"):
                st.caption("Xác định mức độ tổn thương tim phải để chia nhóm C thành C1, C2, C3.")
                
                st.write("**1. Đánh giá chi tiết Rối loạn chức năng Thất phải (RV) (Siêu âm/CT):**")
                rv_ct = persistent_checkbox("Tỷ lệ đường kính RV/LV >= 1.0 trên CTPA hoặc siêu âm 4 buồng", key="rv_ct")
                rv_echo_1 = persistent_checkbox("TAPSE < 17 mm (co bóp dọc vòng van 3 lá)", key="rv_echo_1")
                rv_echo_2 = persistent_checkbox("Dấu hiệu McConnell (giảm động thành tự do RV, bảo tồn vùng mỏm)", key="rv_echo_2")
                rv_echo_3 = persistent_checkbox("Vận tốc sóng S' TDI van 3 lá < 9.5 cm/s", key="rv_echo_3")
                rv_echo_4 = persistent_checkbox("Vận tốc hở 3 lá TR >= 2.9 m/s (gợi ý tăng áp phổi cấp)", key="rv_echo_4")
                rv_echo_5 = persistent_checkbox("Tĩnh mạch chủ dưới IVC giãn (>21mm) và xẹp < 50% khi hít vào", key="rv_echo_5")
                rv_echo_6 = persistent_checkbox("Vách liên thất dẹt nghịch thường trong thì tâm thu/tâm trương", key="rv_echo_6")
                
                has_rv_dysfunction = rv_ct or rv_echo_1 or rv_echo_2 or rv_echo_3 or rv_echo_4 or rv_echo_5 or rv_echo_6
                
                if has_rv_dysfunction:
                    st.error("Xác nhận: Có rối loạn chức năng/Quá tải thất phải (RV Dysfunction)")
                else:
                    st.success("Xác nhận: Thất phải (RV) hoạt động bình thường")
                
                st.write("---")
                st.write("**2. Đánh giá dấu ấn sinh học cơ tim (Biomarkers):**")
                has_elevated_biomarkers = persistent_checkbox("Có tăng men tim Troponin (I/T) HOẶC tăng peptide lợi niệu (BNP/NT-proBNP)?", key="has_elevated_biomarkers")
                
                if has_rv_dysfunction and has_elevated_biomarkers:
                    st.session_state.final_category = "C3"
                elif has_rv_dysfunction or has_elevated_biomarkers:
                    st.session_state.final_category = "C2"
                else:
                    st.session_state.final_category = "C1"
                    
                st.write("---")
                st.success(f"Xác lập phân nhóm: **Nhóm {st.session_state.final_category}**")
                
                # Đánh giá Respiratory Modifier cho nhóm C
                st.write("##### 📢 Đánh giá Modifier R cho nhóm C")
                r_c = persistent_checkbox("SpO2 < 90% ở khí trời, HOẶC nhịp thở (RR) >= 30 lần/phút, HOẶC đang cần bổ sung oxy hỗ trợ thông thường (qua gọng kính/mặt nạ)?", key="r_c")
                st.session_state.resp_modifier = r_c
                
                if st.button("Xác nhận Phân nhóm & Chuyển sang Bước 3: Điều trị ➡️", type="primary", use_container_width=True, key="to_step3_rv"):
                    st.session_state.step = 3
                    st.rerun()
                    
                if st.button("⬅️ Quay lại chọn Thang điểm tiên lượng", type="secondary"):
                    st.session_state.g2_stable_flow = "prognosis"
                    st.session_state.step2_focus = "prognosis"
                    st.rerun()
        if primary_hemo == "Huyết động ổn định (Huyết áp bình thường)" and _flow == "hk_position":
            if render_step2_sub_header("2.5 🔍 Đánh giá vị trí huyết khối — Nhóm B", "hk_position"):
                st.caption("Xác định vị trí giải phẫu của huyết khối để chia nhóm B thành B1 (Dưới phân thùy) hoặc B2 (Phân thùy trở lên).")
                
                is_subsegmental = persistent_checkbox("Huyết khối chỉ khu trú ở nhánh dưới phân thùy (Subsegmental PE) trên CTPA?", key="is_subsegmental")
                
                if is_subsegmental:
                    st.session_state.final_category = "B1"
                else:
                    st.session_state.final_category = "B2"
                
                st.write("---")
                st.success(f"Xác lập phân nhóm: **Nhóm {st.session_state.final_category}**")
                
                # BỔ SUNG RESPIRATORY MODIFIER CHO NHÓM B
                st.write("##### 📢 Đánh giá Modifier R cho nhóm B")
                r_b = persistent_checkbox("SpO2 < 90% ở khí trời, HOẶC nhịp thở (RR) >= 30 lần/phút, HOẶC đang cần bổ sung oxy hỗ trợ thông thường (qua gọng kính/mặt nạ)?", key="r_b")
                st.session_state.resp_modifier = r_b
                
                if st.button("Xác nhận Phân nhóm & Chuyển sang Bước 3: Điều trị ➡️", type="primary", use_container_width=True, key="to_step3_hk"):
                    st.session_state.step = 3
                    st.rerun()
                    
                if st.button("⬅️ Quay lại chọn Thang điểm tiên lượng", type="secondary"):
                    st.session_state.g2_stable_flow = "prognosis"
                    st.session_state.step2_focus = "prognosis"
                    st.rerun()
    with st.expander("ℹ️ Xem Sơ đồ Tóm tắt Phân tầng AHA/ACC 2026", expanded=False):
        st.subheader("📋 Sơ đồ Tóm tắt Phân tầng AHA/ACC 2026")
        st.markdown("""
        *   **Nhóm E (Nguy kịch):** Ngừng tuần hoàn / Sốc tim thực sự.
        *   **Nhóm D (Chớm suy):** Sốc ẩn (D2) hoặc Tụt huyết áp thoáng qua (D1).
        *   **Nhóm C (Nguy cơ trung bình):** Thang điểm sPESI/PESI/Hestia cao.
            *   *C3:* Có cả rối loạn chức năng RV và tăng men tim.
            *   *C2:* Có rối loạn chức năng RV HOẶC tăng men tim.
            *   *C1:* Không có rối loạn chức năng RV và men tim bình thường.
        *   **Nhóm B (Nguy cơ thấp):** Thang điểm tiên lượng lâm sàng thấp.
            *   *B2:* Huyết khối từ nhánh phân thùy trở lên.
            *   *B1:* Huyết khối khu trú ở nhánh dưới phân thùy.
        *   **Nhóm A:** Thuyên tắc phổi phát hiện tình cờ, không triệu chứng.
        """)

# ==============================================================================
# BƯỚC 3: CÁ THỂ HÓA ĐIỀU TRỊ & TÍNH LIỀU
# ==============================================================================
if render_main_step_header("💊 BƯỚC 3: CÁ THỂ HÓA ĐIỀU TRỊ & TÍNH LIỀU", 3):
    st.session_state.is_pregnant = st.session_state.saved_inputs.get('is_pregnant', False)
    # Khôi phục các biến đầu vào để các heading điều trị có thể render độc lập mà không mất dữ liệu.
    _s3 = st.session_state.saved_inputs
    weight = _s3.get("weight", 70)
    height = _s3.get("height", 165)
    scr = _s3.get("scr", 1.0)
    age_calc = _s3.get("age_calc", 60)
    gender_calc = _s3.get("gender_calc", "Nam")
    bmi = weight / ((height / 100) ** 2)
    gender_mul = 0.85 if gender_calc == "Nữ" else 1.0
    crcl = ((140 - age_calc) * weight * gender_mul) / (72 * scr)
    has_aps = _s3.get("has_aps", False)
    is_breastfeeding_t2 = _s3.get("is_breastfeeding_t2", False)
    has_cancer = _s3.get("has_cancer", False)
    has_drug_interactions = _s3.get("has_drug_interactions", False)

    if render_flow_sub_header("3.1 🧬 Nhập thông số sinh học & Tình huống đặc biệt", 1, "step3_open", "step3_sub"):
        
        # Nhập thông số cân nặng chiều cao chức năng thận bằng persistent widget để không bao giờ bị reset!
        col_w, col_h, col_cr = st.columns(3)
        with col_w:
            weight = persistent_number_input("Cân nặng (kg):", 30, 250, 70, key="weight")
        with col_h:
            height = persistent_number_input("Chiều cao (cm):", 100, 250, 165, key="height")
        with col_cr:
            scr = persistent_number_input("Creatinine huyết thanh (mg/dL):", 0.2, 15.0, 1.0, key="scr", step=0.1)
            
        age_calc = persistent_number_input("Tuổi bệnh nhân (để tính CrCl):", 18, 120, 60, key="age_calc")
        gender_calc = persistent_radio("Giới tính sinh học:", ["Nam", "Nữ"], key="gender_calc", horizontal=True)
        
        # Tính toán chỉ số sinh học
        bmi = weight / ((height/100)**2)
        gender_mul = 0.85 if gender_calc == "Nữ" else 1.0
        crcl = ((140 - age_calc) * weight * gender_mul) / (72 * scr)
        
        st.write(f"Chỉ số BMI: **{bmi:.1f} kg/m²** | Độ thanh thải Creatinine (CrCl): **{crcl:.1f} mL/phút**")
        
        # TÌNH HUỐNG LÂM SÀNG ĐẶC BIỆT (TÁCH BIỆT BÉ BÚ & MANG THAI)
        st.markdown("""
        <div style='background-color: #FFFBEB; border-left: 5px solid #D97706; padding: 15px; border-radius: 8px; margin-top: 20px; margin-bottom: 15px;'>
            <span style='color: #B45309; font-weight: 700; font-size: 1.1rem;'>💼 CÁC TÌNH HUỐNG LÂM SÀNG ĐẶC BIỆT</span><br>
            <span style='color: #92400E; font-size: 0.9rem;'>Tích chọn nếu bệnh nhân có bối cảnh đặc biệt dưới đây để tự động thay đổi hoàn toàn phác đồ khởi trị và kế hoạch chuyển đổi duy trì dài hạn:</span>
        </div>
        """, unsafe_allow_html=True)
        has_aps = persistent_checkbox("Bệnh nhân mắc Hội chứng kháng Phospholipid (APS) xác định?", key="has_aps")
        
        # Đồng bộ hóa hộp checkbox mang thai trong Bước 3 với Giai đoạn 1 và state đệm
        is_pregnant_t2 = persistent_checkbox("Bệnh nhân hiện tại đang MANG THAI?", key="is_pregnant") 
        st.session_state.is_pregnant = is_pregnant_t2
        
        is_breastfeeding_t2 = persistent_checkbox("Bệnh nhân hiện tại đang CHO CON BÚ?", key="is_breastfeeding_t2") 
        has_cancer = persistent_checkbox("Bệnh nhân mắc ung thư đang hoạt động / tiến triển (Cancer-associated thrombosis)?", key="has_cancer")
        has_drug_interactions = persistent_checkbox("Đang sử dụng thuốc tương tác mạnh (như Ketoconazole, Itraconazole, Ritonavir, Rifampicin, Phenytoin, Carbamazepine)?", key="has_drug_interactions")
        
        st.markdown("</div>", unsafe_allow_html=True)
        if st.button("Tiếp tục → Phân nhóm & phân luồng điều trị", type="primary", use_container_width=True, key="step3_to_2"):
            st.session_state.step3_open = 2
            st.rerun()
    if render_flow_sub_header("3.2 📍 Phân nhóm lâm sàng & Phân luồng điều trị (Triage/PERT)", 2, "step3_open", "step3_sub"):
        r_suffix = "R" if st.session_state.resp_modifier else ""
        final_group = f"{st.session_state.final_category}{r_suffix}" if st.session_state.final_category else "Chưa xác định"
        
        st.markdown(f"<div class='result-card'><h3>PHÂN NHÓM LÂM SÀNG: <span style='color:#DC2626;'>NHÓM {final_group}</span></h3></div>", unsafe_allow_html=True)
        
        # --------------------------------------------------------------------------
        # PHÁC ĐỒ TRIAGE & KHUYẾN CÁO PERT (Sửa COR/LOE theo chuẩn Hướng dẫn)
        # --------------------------------------------------------------------------
        
        if st.session_state.final_category in ["A", "B1", "B2"]:
            st.markdown("""
            <div class='u-card' style='background-color: #F0FDF4; border-left: 5px solid #16A34A; color: #166534; margin-bottom: 15px;'>
                <strong>Khuyến cáo Quản lý Ngoại trú (Class 2a, LOE B-R):</strong><br>
                Có thể cân nhắc điều trị ngoại trú hoặc xuất viện sớm cho các bệnh nhân thuộc <strong>Nhóm A</strong> hoặc một số bệnh nhân <strong>Nhóm B</strong> nếu thỏa mãn đầy đủ các điều kiện y khoa - xã hội sau:<br>
                1. Điểm sPESI = 0 hoặc Hestia âm tính (đã rà soát ở Giai đoạn 2).<br>
                2. Bệnh nhân có điều kiện gia đình, xã hội ổn định, có người hỗ trợ.<br>
                3. Tiếp cận thuốc kháng đông ngay lập tức và thuận tiện.<br>
                4. Có kế hoạch theo dõi y khoa và hẹn tái khám chuyên khoa nhanh chóng, tin cậy (trong vòng 24-72 giờ đầu).
            </div>
""", unsafe_allow_html=True)
            
        elif st.session_state.final_category in ["C1", "C2", "C3"]:
            pert_text = "📞 **Khuyến cáo kích hoạt PERT (Pulmonary Embolism Response Team) (Class 1, LOE B-NR):** Khuyến cáo mạnh mẽ hội chẩn đa chuyên khoa PERT để tối ưu hóa quyết định điều trị và đẩy nhanh tiến trình điều trị kháng đông tại viện."
            if st.session_state.final_category == "C3":
                st.markdown(f"""
                <div class='u-card urgency-medium'>
                    <strong>📍 Nơi điều trị: ICU HOẶC ĐƠN VỊ ĐỆM (Intermediate/Step-down)</strong><br>
                    Theo dõi sát huyết động liên tục trong 24-72 giờ đầu (Class 2a) do có nguy cơ tiến triển thành sốc ẩn rất cao.<br>
                    {pert_text}
                </div>
""", unsafe_allow_html=True)
            else:
                st.info(f"📍 **Nơi điều trị:** Nhập viện điều trị nội trú tại Khoa Thường (Nội tim mạch/Nội chung).\n\n{pert_text}")
                
        elif st.session_state.final_category in ["D1", "D2", "E1", "E2"]:
            st.markdown(f"""
            <div class='u-card urgency-high'>
                <strong>📍 Nơi điều trị: KHOA HỒI SỨC TÍCH CỰC (ICU/CCU) tối khẩn cấp</strong><br>
                Theo dõi huyết động liên tục.<br>
                📞 **BẮT BUỘC KÍCH HOẠT NGAY ĐỘI PHẢN ỨNG NHANH PERT (Class 1, LOE B-NR):** Phối hợp đa chuyên khoa khẩn cấp để đưa ra quyết định tái tưới máu can thiệp nâng cao.
            </div>
""", unsafe_allow_html=True)

        st.write("---")
        if st.button("Tiếp tục → Kháng đông & tính liều", type="primary", use_container_width=True, key="step3_to_3"):
            st.session_state.step3_open = 3
            st.rerun()
    if render_flow_sub_header("3.3 💊 Kháng đông & tính liều cá thể hóa", 3, "step3_open", "step3_sub"):
        # --------------------------------------------------------------------------
        # PHÁC ĐỒ ĐIỀU TRỊ CHUYÊN BIỆT CHO THAI KỲ / CHO CON BÚ TRƯỚC (KHÔNG HIỆN DOACs)
        # --------------------------------------------------------------------------
        if st.session_state.is_pregnant:
            st.error("🤰 **PHÁC ĐỒ KHÁNG ĐÔNG BẮT BUỘC TRONG THAI KỲ (CHỐNG CHỈ ĐỊNH TUYỆT ĐỐI DOACs / VKA - Class 3: Harm, LOE C-LD)**")
            st.caption("Kháng đông uống DOACs (Apixaban, Rivaroxaban...) và VKA (Warfarin) chống chỉ định tuyệt đối trong suốt thai kỳ do nguy cơ sảy thai, dị tật bẩm sinh và quái thai.")
            
            st.write("🌟 **1. KHỞI TRỊ BAN ĐẦU VÀ DUY TRÌ TRONG THAI KỲ:**")
            st.write("Kháng đông tiêm **LMWH (Enoxaparin) được khuyến cáo lựa chọn hàng đầu (Class 1, LOE C-LD)** do tính an toàn cao cho thai nhi (không đi qua bánh nhau).")
            
            if crcl >= 30:
                enox_dose = weight * 1.0
                st.write(f"- **Liều Enoxaparin tiêu chuẩn:** **{enox_dose:.1f} mg tiêm dưới da mỗi 12 giờ** (1.0 mg/kg mỗi 12 giờ).")
                st.caption("⚠️ *Lưu ý:* Không cần theo dõi nồng độ anti-Xa thường quy ở thai phụ có cân nặng bình thường (Class 3: No Benefit, LOE A). Cân nhắc đo nồng độ đỉnh anti-Xa (3-5 giờ sau liều thứ 3) ở thai phụ béo phì độ III hoặc cực kỳ nhẹ cân (Class 2a, LOE C-LD).")
            elif 15 <= crcl < 30:
                enox_dose = weight * 1.0
                st.write(f"- **Liều Enoxaparin hiệu chỉnh suy thận nặng (CrCl 15-29 mL/phút):** **{enox_dose:.1f} mg tiêm dưới da mỗi 24 giờ** (1.0 mg/kg mỗi 24 giờ). Cần theo dõi đỉnh anti-Xa.")
            else:
                st.error("- **Enoxaparin (LMWH):** Chống chỉ định tuyệt đối do CrCl < 15 mL/phút. Bắt buộc dùng **Heparin không phân đoạn (UFH)** truyền tĩnh mạch điều chỉnh theo aPTT.")
                ufh_bolus = min(80 * weight, 10000)
                ufh_maint = min(18 * weight, 1600)
                st.write(f"  - *Liều nạp Bolus UFH:* **{ufh_bolus:.0f} UI** bolus tĩnh mạch (chuẩn local nomogram).")
                st.write(f"  - *Tốc độ truyền duy trì ban đầu:* **{ufh_maint:.0f} UI/giờ** (áp trần 1,600 UI/h, chuẩn local nomogram).")

            st.write("🕒 **2. THỜI GIAN SỬ DỤNG KHÁNG ĐÔNG (DURATION):**")
            st.write("- Kháng đông tiêm LMWH phải được duy trì liên tục **suốt thai kỳ** (tạm ngưng 24 giờ trước khi chủ động khởi phát chuyển dạ hoặc mổ đẻ).")
            st.write("- **Bắt buộc kéo dài ít nhất 6 tuần sau sinh** (Class 1, LOE C-LD).")
            st.write("- **Tổng thời gian điều trị tối thiểu phải đạt 3 tháng** (bao gồm cả trước sinh và sau sinh) (Class 1, LOE C-LD).")
            
            st.write("🔄 **3. KẾ HOẠCH CHUYỂN ĐỔI (TRANSITION PHASE) SAU SINH:**")
            st.write("- **Nếu nuôi con bằng sữa mẹ:** Bệnh nhân có thể chuyển đổi từ kháng đông tiêm LMWH sang **Kháng vitamin K (Warfarin - VKA) (Class 1, LOE C-LD)** sau khi sinh vì Warfarin tương thích tốt và không bài tiết qua sữa mẹ đáng kể. Tuyệt đối không dùng DOACs.")
            st.write("  - *Cách thức gối liều (Overlap):* Bắt đầu uống Warfarin hằng ngày đồng thời **duy trì song song LMWH** trong **ít nhất 5 ngày VÀ cho đến khi INR đạt mục tiêu 2.0 - 3.0 trong 24 giờ liên tục** (2 lần đo liên tiếp cách nhau 24h đạt đích). Khi INR đạt đích, ngừng tiêm LMWH.")
            st.write("- **Nếu KHÔNG nuôi con bằng sữa mẹ:** Có thể chuyển sang dùng **DOACs đường uống** (Apixaban 5mg BID hoặc Rivaroxaban 20mg QD) sau sinh.")
            st.write("  - *Cách thức chuyển sang DOAC:* Bắt đầu uống liều DOAC đầu tiên ngay vào thời điểm liều LMWH tiếp theo chuẩn bị tiêm (không cần gối overlap).")

        elif is_breastfeeding_t2:
            st.warning("🍼 **PHÁC ĐỒ KHÁNG ĐÔNG CHO PHỤ NỮ ĐANG CHO CON BÚ (CHỐNG CHỈ ĐỊNH DOACs - Class 1, LOE C-LD)**")
            st.caption("Các DOACs có thể bài tiết qua sữa mẹ và thiếu dữ liệu an toàn ở trẻ sơ sinh, do đó chống chỉ định cho thời kỳ cho con bú.")
            
            st.write("🌟 **1. KHỞI TRỊ BAN ĐẦU VÀ KHÁNG ĐÔNG ƯU TIÊN:**")
            st.write("Kháng đông **LMWH (Enoxaparin), UFH, hoặc Kháng vitamin K (Warfarin)** được khuyến cáo lựa chọn hơn là các thuốc DOACs (**Class 1, LOE C-LD**).")
            
            if crcl >= 30:
                enox_dose = weight * 1.0
                st.write(f"- **Liều Enoxaparin đề xuất:** **{enox_dose:.1f} mg tiêm dưới da mỗi 12 giờ** (1.0 mg/kg mỗi 12 giờ).")
            else:
                st.write("- Chống chỉ định Enoxaparin do suy thận nặng. Ưu tiên gối Warfarin gối đầu bằng UFH truyền tĩnh mạch.")

            st.write("🕒 **2. THỜI GIAN SỬ DỤNG KHÁNG ĐÔNG (DURATION):**")
            st.write("- **Nếu PE do yếu tố nguy cơ tạm thời đảo ngược được lớn (phẫu thuật, chấn thương...):** Điều trị trong **3 tháng** đầy đủ (Class 1, LOE B-NR).")
            st.write("- **Nếu PE tự phát hoặc có nguy cơ dai dẳng (như ung thư, APS):** Duy trì lâu dài **vô hạn định** (Class 1, LOE A) và đánh giá định kỳ nguy cơ chảy máu.")

            st.write("🔄 **3. KẾ HOẠCH GỐI LIỀU VÀ CHUYỂN SANG WARFARIN (VKA) UỐNG DUY TRÌ:**")
            st.write("Warfarin (VKA) là kháng đông đường uống duy nhất được khuyến cáo cho phụ nữ cho con bú.")
            st.write("- *Quy trình chuyển đổi chuẩn:* Bắt đầu uống Warfarin hằng ngày đồng thời **duy trì song song kháng đông tiêm LMWH/UFH** trong **ít nhất 5 ngày VÀ cho đến khi INR đạt mục tiêu 2.0 - 3.0 trong 24 giờ liên tục (2 lần đo liên tiếp)**. Khi INR đạt đích y khoa, ngừng tiêm và duy trì Warfarin uống đơn trị liệu lâu dài.")

        # --------------------------------------------------------------------------
        # PHÁC ĐỒ ĐIỀU TRỊ CHO BỆNH NHÂN THÔNG THƯỜNG (KHÔNG CÓ THAI / CHO CON BÚ)
        # --------------------------------------------------------------------------
        else:
            # --------------------------------------------------------------------------
            # NHÓM A, B (KHÁNG ĐÔNG ĐƯỜNG UỐNG ƯU TIÊN - DOACs)
            # --------------------------------------------------------------------------
            if st.session_state.final_category in ["A", "B1", "B2"]:
                st.success("💊 **Kháng đông ưu tiên: DOACs đường uống (Class 1, LOE B-R)**")
                
                if st.session_state.final_category == "B1":
                    st.warning("👉 *Lưu ý Nhóm B1 (Dưới phân thùy):* Guideline cho phép theo dõi sát lâm sàng và siêu âm tĩnh mạch chi dưới định kỳ mà chưa cần dùng kháng đông ngay nếu bệnh nhân có nguy cơ chảy máu cao, không có triệu chứng lâm sàng và KHÔNG CÓ DVT chi dưới (Class 2b, LOE B-R). Nếu có DVT đi kèm, bắt buộc dùng kháng đông tiêu chuẩn.")
                
                if has_aps:
                    st.error("🩸 **HỘI CHỨNG KHÁNG PHOSPHOLIPID - APS (CHỐNG CHỈ ĐỊNH DOACs):**\nChống chỉ định dùng DOACs do tăng nguy cơ tắc mạch tái phát nghiêm trọng (Class 1, LOE A). Bắt buộc khởi đầu bằng kháng đông tiêm (LMWH/UFH) sau đó gối sang **Kháng Vitamin K (VKA - Warfarin)** duy trì lâu dài với đích **INR 2.0 - 3.0 (Class 1, LOE A)**.")
                elif has_drug_interactions:
                    st.warning("⚠️ **TƯƠNG TÁC THUỐC MẠNH (CHỐNG CHỈ ĐỊNH DOACs):**\nThuốc đồng vận làm biến đổi nồng độ DOACs nguy hiểm. Khuyến cáo dùng LMWH dài hạn hoặc chuyển sang VKA (theo dõi sát INR).")
                else:
                    if has_cancer:
                        st.info("🎗️ *Bệnh nhân Ung thư (CAT):* Khuyến cáo ưu tiên sử dụng DOACs (như Apixaban, Rivaroxaban) hơn là Kháng vitamin K (VKA) để dự phòng tái phát VTE (Class 1, LOE B-R). Các nghiên cứu cho thấy DOAC không kém hơn LMWH về mặt hiệu quả và an toàn, tuy nhiên việc lựa chọn giữa DOAC và LMWH cần cá thể hóa dựa trên loại ung thư (ví dụ: tránh dùng DOAC ở bệnh nhân ung thư biểu mô đường tiêu hóa hoặc tiết niệu chưa cắt bỏ do làm tăng nguy cơ chảy máu).")
                    
                    # CHUẨN HÓA LIỀU DOAC
                    st.write("**• Apixaban:**")
                    st.write(f"  - *Liều tấn công:* **10 mg uống x 2 lần/ngày** (10 mg BID) trong 7 ngày đầu.")
                    st.write("  - *Liều duy trì:* **5 mg uống x 2 lần/ngày** (5 mg BID).")
                    st.caption("⚠️ *Lưu ý y khoa:* Không áp dụng công thức giảm liều AF (giảm xuống 2.5 mg BID dựa trên tuổi, cân nặng, creatinine) trong điều trị PE cấp tính. Liều 2.5 mg BID chỉ dùng ở giai đoạn kéo dài (extended phase) sau 3-6 tháng điều trị ban đầu để phòng ngừa thứ phát (Class 1, LOE A).")
                    
                    # Chỉnh liều suy thận nặng dựa trên CrCl và eGFR tách biệt
                    if crcl < 30:
                        st.warning("🏥 **Lưu ý chức năng thận giảm nặng (eGFR hoặc CrCl < 30 mL/phút, hoặc suy thận giai đoạn cuối):**\nTheo Hướng dẫn AHA/ACC 2026, đối với bệnh nhân suy thận mạn nặng (CKD Stage 4 hoặc 5, eGFR < 30 mL/phút hoặc suy thận giai đoạn cuối lọc máu), việc lựa chọn giữa Apixaban và VKA là chưa rõ ràng (Class 2b, LOE B-NR) để phòng ngừa chảy máu nặng; các DOAC khác (như Rivaroxaban) nhìn chung cần tránh dùng.\n\n*Lưu ý y khoa:* Độ thanh thải Creatinine tính theo công thức Cockcroft-Gault (CrCl) là thông số chuẩn mực được FDA quy định để hiệu chỉnh liều lượng thuốc, trong khi eGFR được dùng để phân độ suy thận mạn.")
                    
                    st.write("**• Rivaroxaban:**")
                    st.write(f"  - *Liều tấn công:* **15 mg uống x 2 lần/ngày** (15 mg BID) cùng thức ăn trong 21 ngày đầu.")
                    st.write("  - *Liều duy trì:* **20 mg uống hằng ngày** (20 mg QD) cùng thức ăn.")
                    st.caption("⚠️ *Lưu ý y khoa:* Không giảm liều duy trì xuống 15 mg QD cho bệnh nhân suy thận CrCl 30-49 mL/phút trong điều trị PE cấp tính ở pha cấp cứu (luôn giữ liều tấn công 15mg BID x 21 ngày và duy trì 20mg QD).")

                    # THỜI GIAN SỬ DỤNG CHO NHÓM A, B THÔNG THƯỜNG
                    st.markdown("---")
                    st.write("🕒 **THỜI GIAN ĐIỀU TRỊ KHÁNG ĐÔNG DUY TRÌ (DURATION):**")
                    st.write("- **Nếu PE do yếu tố nguy cơ có thể đảo ngược lớn (như phẫu thuật lớn):** Ngừng điều trị kháng đông sau **3 tháng** điều trị đầy đủ (Class 1, LOE B-NR).")
                    st.write("- **Nếu PE tự phát hoặc có nguy cơ dai dẳng:** Tiếp tục điều trị kéo dài **vô hạn định (extended phase)** (Class 1, LOE A).")
                    st.write("  - *Hạ liều dự phòng thứ phát:* Sau 3-6 tháng điều trị ban đầu, khuyến cáo **giảm xuống liều dự phòng: Apixaban 2.5mg BID HOẶC Rivaroxaban 10mg QD** để giảm nguy cơ chảy máu nặng (Class 1, LOE A).")

            # --------------------------------------------------------------------------
            # NHÓM C1, C2, C3, D1, D2, E1 (KHÁNG ĐÔNG TIÊM KHỞI ĐẦU: LMWH > UFH)
            # --------------------------------------------------------------------------
            elif st.session_state.final_category in ["C1", "C2", "C3", "D1", "D2", "E1"]:
                st.success("💊 **Kháng đông tiêm khởi đầu (C1 - E1): LMWH được khuyến cáo hơn UFH (Class 1, LOE B-R)**")
                st.caption("LMWH được chứng minh làm giảm nguy cơ tái phát VTE và giảm nguy cơ chảy máu nặng, giảm biến chứng HIT tốt hơn UFH.")
                
                # Tính liều Enoxaparin (LMWH) - ƯU TIÊN HÀNG ĐẦU
                st.write("🌟 **LỰA CHỌN ƯU TIÊN: Heparin trọng lượng phân tử thấp (LMWH - Enoxaparin)**")
                
                if crcl >= 30:
                    enox_dose = weight * 1.0
                    st.write(f"- **Liều Enoxaparin tiêu chuẩn:** **{enox_dose:.1f} mg tiêm dưới da mỗi 12 giờ** (1.0 mg/kg Q12h).")
                    if bmi >= 40 or weight > 150:
                        st.warning(f"⚠️ *Lưu ý béo phì độ III (BMI = {bmi:.1f} hoặc cân nặng > 150 kg):* Hướng dẫn AHA/ACC 2026 cho thấy việc cân nhắc điều chỉnh giảm liều LMWH ở bệnh nhân béo phì độ III nhằm phòng ngừa nguy cơ chảy máu nặng là hợp lý (Class 2b, LOE B-NR). Tuy nhiên, liều tối ưu chưa được xác lập thống nhất và công thức giảm liều (như giảm xuống 0.8 mg/kg mỗi 12 giờ) chỉ là một phác đồ từ nghiên cứu thử nghiệm nhỏ; việc quyết định điều chỉnh liều cần cá thể hóa sát sao dựa trên bối cảnh lâm sàng thực tế.")
                    st.caption("⚠️ *Theo dõi Anti-Xa:* Không có chỉ định theo dõi nồng độ anti-Xa thường quy ở hầu hết bệnh nhân dùng LMWH theo cân nặng thực tế (Class 3: No Benefit, LOE A).")
                elif 15 <= crcl < 30:
                    enox_dose = weight * 1.0
                    st.write(f"- **Liều Enoxaparin hiệu chỉnh suy thận nặng (CrCl 15-29 mL/phút):** **{enox_dose:.1f} mg tiêm dưới da mỗi 24 giờ** (1.0 mg/kg Q24h).")
                    st.caption("⚠️ *Theo dõi Anti-Xa (Class 2a, LOE C-LD):* Ở bệnh nhân suy thận nặng (CrCl < 30 mL/phút) dùng LMWH, việc đo nồng độ đỉnh anti-Xa (3-5 giờ sau liều thứ 3 ở trạng thái ổn định) là hợp lý để hỗ trợ điều chỉnh liều.")
                else:
                    st.error("- **Enoxaparin (LMWH):** Chống chỉ định tuyệt đối do CrCl < 15 mL/phút.")

                # Tính liều UFH - THAY THẾ
                st.write("👉 **LỰA CHỌN THAY THẾ: Heparin không phân đoạn (UFH) truyền tĩnh mạch**")
                st.caption("Chỉ định thay thế khi bệnh nhân chống chỉ định with LMWH (CrCl < 15), hoặc khi bác sĩ dự kiến sẽ can thiệp tái tưới máu ngay lập tức và cần tính đảo ngược nhanh của UFH.")
                
                ufh_bolus = min(80 * weight, 10000)
                ufh_maint = min(18 * weight, 1600)  # SỬA LỖI: ÁP TRẦN 1600 UI/h
                st.write(f"- **Liều nạp Bolus tĩnh mạch ban đầu:** **{ufh_bolus:.0f} UI** (Áp trần tối đa 10,000 UI).")
                st.write(f"- **Tốc độ truyền tĩnh mạch duy trì ban đầu:** **{ufh_maint:.0f} UI/giờ** (Áp trần tối đa **1,600 UI/giờ** để phòng ngừa quá liều ban đầu trước khi có kết quả aPTT/Anti-Xa), chỉnh liều theo aPTT.")
                st.caption("👉 *Lưu ý y khoa:* Phác đồ bolus 80 UI/kg và truyền 18 UI/kg/h với các mức trần trên là phác đồ ngoài nước được chuẩn hóa (local/external VTE nomogram), không phải do hướng dẫn AHA 2026 trực tiếp quy định cụ thể.")

            # --------------------------------------------------------------------------
            # PHÁC ĐỒ KHÁNG ĐÔNG TIÊM CHO NHÓM E2 (YÊU CẦU: LINH HOẠT LMWH/UFH)
            # --------------------------------------------------------------------------
            elif st.session_state.final_category == "E2":
                st.success("💊 **Kháng đông tiêm khởi đầu ở Nhóm E2: Cần linh hoạt giữa UFH và LMWH**")
                st.caption("Trong tình huống ngừng tuần hoàn hoặc sốc tim kháng trị (E2), việc lựa chọn giữa UFH và LMWH cần được quyết định linh hoạt tùy theo bối cảnh cụ thể (khả năng đảo ngược tác dụng nhanh, chức năng thận và kế hoạch can thiệp hỗ trợ tuần hoàn ECMO/phẫu thuật).")
                
                tab_ufh, tab_lmwh = st.tabs(["🌟 Lựa chọn UFH (Dễ kiểm soát)", "🌟 Lựa chọn LMWH (Hạn chế HIT)"])
                
                with tab_ufh:
                    st.write("**Heparin không phân đoạn (UFH) truyền tĩnh mạch:**")
                    st.caption("Được ưa chuộng hơn trong pha cấp cứu cực kỳ nguy kịch cần can thiệp ngoại khoa khẩn cấp, ECMO hoặc khi chức năng thận chưa xác định được ngay.")
                    ufh_bolus = min(80 * weight, 10000)
                    ufh_maint = min(18 * weight, 1600)
                    st.write(f"- **Liều nạp Bolus tĩnh mạch ban đầu:** **{ufh_bolus:.0f} UI** (Áp trần tối đa 10,000 UI).")
                    st.write(f"- **Tốc độ truyền tĩnh mạch duy trì ban đầu:** **{ufh_maint:.0f} UI/giờ** (Áp trần tối đa **1,600 UI/giờ**), chỉnh liều sát theo aPTT.")
                    st.caption("👉 *Lưu ý y khoa:* Phác đồ trên dựa theo chuẩn local/external VTE nomogram, không do hướng dẫn AHA 2026 trực tiếp quy định.")
                    
                with tab_lmwh:
                    st.write("**Heparin trọng lượng phân tử thấp (LMWH - Enoxaparin):**")
                    st.caption("Có thể cân nhắc nhờ tính tiện dụng, không đòi hỏi theo dõi xét nghiệm đông máu liên tục và nguy cơ bị giảm tiểu cầu do Heparin (HIT) thấp hơn.")
                    if crcl >= 30:
                        enox_dose = weight * 1.0
                        st.write(f"- **Liều Enoxaparin tiêu chuẩn:** **{enox_dose:.1f} mg tiêm dưới da mỗi 12 giờ** (1.0 mg/kg Q12h).")
                    elif 15 <= crcl < 30:
                        enox_dose = weight * 1.0
                        st.write(f"- **Liều Enoxaparin hiệu chỉnh:** **{enox_dose:.1f} mg tiêm dưới da mỗi 24 giờ** (1.0 mg/kg Q24h).")
                        st.caption("⚠️ *Lưu ý:* Đo nồng độ đỉnh anti-Xa (3-5 giờ sau liều thứ 3) là hợp lý (Class 2a, LOE C-LD) để hướng dẫn chỉnh liều.")
                    else:
                        st.error("- Chống chỉ định Enoxaparin do CrCl < 15 mL/phút.")

            
        _has_advanced = st.session_state.final_category in ["C3", "D1", "D2", "E1", "E2"]
        _has_resp = bool(st.session_state.resp_modifier)
        _has_longterm = (not st.session_state.is_pregnant and not is_breastfeeding_t2 and st.session_state.final_category in ["C1", "C2", "C3", "D1", "D2", "E1", "E2"])
        _next3 = 4 if _has_advanced else (5 if _has_resp else (6 if _has_longterm else None))
        if _next3 and st.button("Tiếp tục → Nội dung điều trị tiếp theo", type="primary", use_container_width=True, key="step3_after_anticoag"):
            st.session_state.step3_open = _next3
            st.rerun()
    if st.session_state.final_category in ["C3", "D1", "D2", "E1", "E2"]:
        if render_flow_sub_header("3.4 ⚡ Liệu pháp Can thiệp tái tưới máu nâng cao", 4, "step3_open", "step3_sub"):
            # Rà soát chống chỉ định tiêu sợi huyết hệ thống — đặt trong mục tái tưới máu nâng cao
            st.markdown("---")
            if "thrombolysis_ci_open" not in st.session_state:
                st.session_state.thrombolysis_ci_open = False

            ci_arrow = "▼" if st.session_state.thrombolysis_ci_open else "▶"
            if st.button(
                f"{ci_arrow} 🩸 Bảng kiểm Chống chỉ định của Tiêu sợi huyết Hệ thống",
                key="thrombolysis_ci_toggle",
                use_container_width=True,
            ):
                st.session_state.thrombolysis_ci_open = not st.session_state.thrombolysis_ci_open
                st.rerun()

            if st.session_state.thrombolysis_ci_open:
                with st.container(border=True):
                    abs1 = persistent_checkbox("Tiền sử xuất huyết não hoặc đột quỵ không rõ nguyên nhân bất kỳ thời điểm nào", key="abs1")
                    abs2 = persistent_checkbox("Đột quỵ nhồi máu não trong vòng 6 tháng qua", key="abs2")
                    abs3 = persistent_checkbox("U hệ thần kinh trung ương hoặc dị dạng động tĩnh mạch não", key="abs3")
                    abs4 = persistent_checkbox("Chấn thương lớn, phẫu thuật lớn hoặc chấn thương đầu nặng trong vòng 3 tuần qua", key="abs4")
                    abs5 = persistent_checkbox("Xuất huyết nội tạng đang tiến triển hoặc xuất huyết tiêu hóa trong vòng 1 tháng qua", key="abs5")
                    abs6 = persistent_checkbox("Phình tách động mạch chủ ngực/bụng hoặc nghi ngờ", key="abs6")
                
                    st.markdown("**Chống chỉ định tương đối (Relative Contraindications):**")
                    rel1 = persistent_checkbox("Cơn thiếu máu não cục bộ thoáng qua (TIA) trong vòng 6 tháng qua", key="rel1")
                    rel2 = persistent_checkbox("Đang dùng kháng đông đường uống", key="rel2")
                    rel3 = persistent_checkbox("Mang thai hoặc trong vòng 1 tuần sau sinh", key="rel3")
                    rel4 = persistent_checkbox("Chọc dò mạch máu ở vị trí không ép được", key="rel4")
                    rel5 = persistent_checkbox("Hồi sức tim phổi (CPR) kéo dài hoặc chấn thương lớn do hồi sức", key="rel5")
                    rel6 = persistent_checkbox("Tăng huyết áp nặng không kiểm soát (HA tâm thu > 180 mmHg hoặc tâm trương > 110 mmHg)", key="rel6")
                    rel7 = persistent_checkbox("Bệnh gan nặng tiến triển hoặc viêm màng ngoài tim cấp", key="rel7")
                
                    has_absolute = abs1 or abs2 or abs3 or abs4 or abs5 or abs6
                    has_relative = rel1 or rel2 or rel3 or rel4 or rel5 or rel6 or rel7
                
                    if has_absolute:
                        st.error("🚨 CẢNH BÁO: Bệnh nhân có chống chỉ định TUYỆT ĐỐI với tiêu sợi huyết hệ thống! Bắt buộc cân nhắc phương pháp Lấy huyết khối cơ học (MT) hoặc Phẫu thuật lấy huyết khối.")
                    elif has_relative:
                        st.warning("⚠️ CẢNH BÁO: Bệnh nhân có chống chỉ định tương đối. Cần cân nhắc kỹ lợi ích/nguy cơ, ưu tiên can thiệp qua catheter (CDL) hoặc lấy huyết khối cơ học MT nếu có sẵn.")
                    else:
                        st.success("Không phát hiện chống chỉ định tiêu sợi huyết hệ thống.")

            
            # Đồng bộ phác đồ Alteplase chuẩn (Bỏ lỗi tự ý chia liều unapproved)
            st.info("💊 **Phác đồ Tiêu sợi huyết Hệ thống (Systemic Thrombolysis):**\n- **Các thuốc được FDA phê duyệt cho PE:** **rt-PA (Alteplase), Streptokinase, và Urokinase**. Trong đó, rt-PA (alteplase) là thuốc phổ biến nhất trong thực hành lâm sàng hiện đại.\n- **Phác đồ Alteplase chuẩn:** **100 mg truyền tĩnh mạch liên tục trong 2 giờ**.\n- *Cân nhắc liều thấp (Lower-dose):* Có thể cân nhắc truyền liều thấp (ví dụ: **50 mg rt-PA truyền trong 2 giờ** hoặc các phác đồ liều thấp khác) để giảm nguy cơ chảy máu (**Class 2b, LOE C-LD**), đặc biệt ở bệnh nhân có nguy cơ xuất huyết cao (Không áp dụng công thức chia liều cố định universally theo cân nặng).\n- *Lưu ý về Tenecteplase (TNK-tPA):* Đã được nghiên cứu lâm sàng nhưng **CHƯA ĐƯỢC FDA PHÊ DUYỆT** cho chỉ định thuyên tắc phổi (off-label) và không được xem là phác đồ tương đương quy chuẩn.")
            
            # COPY GẦN NHƯ NGUYÊN BẢN LOGIC TABLE 7 KHÔNG DIỄN GIẢI THÊM (SỬA LỖI TABLE 7)
            st.markdown("**Khuyến cáo can thiệp nâng cao theo quy chuẩn Table 7 (AHA/ACC 2026):**", unsafe_allow_html=True)
            
            if st.session_state.final_category == "C3":
                st.markdown("""
                <table class='table-style'>
                    <tr><th>Can thiệp điều trị nâng cao</th><th>Mức độ Khuyến cáo (COR & LOE)</th><th>Ý nghĩa lâm sàng theo AHA/ACC 2026</th></tr>
                    <tr><td><strong>Tiêu sợi huyết hệ thống (Systemic Lysis)</strong></td><td><span class='badge' style='background-color:#FFFBEB; color:#92400E;'>Class 2b, LOE C-LD</span></td><td>Hiệu quả lâm sàng chưa rõ ràng (uncertain/unclear).</td></tr>
                    <tr><td><strong>CDL (Tiêu sợi huyết qua Catheter)</strong></td><td><span class='badge' style='background-color:#FFFBEB; color:#92400E;'>Class 2b, LOE C-LD</span></td><td>Hiệu quả lâm sàng chưa rõ ràng (uncertain/unclear).</td></tr>
                    <tr><td><strong>MT (Lấy huyết khối cơ học qua da)</strong></td><td><span class='badge' style='background-color:#FFFBEB; color:#92400E;'>Class 2b, LOE C-LD</span></td><td>Hiệu quả lâm sàng chưa rõ ràng (uncertain/unclear).</td></tr>
                    <tr><td><strong>Phẫu thuật lấy huyết khối (Surgical Embolectomy)</strong></td><td><span class='badge' style='background-color:#FEF2F2; color:#991B1B;'>Class 3: No Benefit, LOE C-EO</span></td><td>Không khuyến cáo (Không có lợi ích so với chỉ dùng kháng đông đơn thuần).</td></tr>
                </table>
""", unsafe_allow_html=True)
                st.warning("👉 **Lưu ý lâm sàng:** Chỉ định tiêu sợi huyết hệ thống thường quy ngay từ đầu cho Nhóm C1-C2 là **Class 3: Harm (Class 3: Harm, LOE B-R)** do tăng nguy cơ xuất huyết nặng/xuất huyết não một cách không cần thiết.")
                
            elif st.session_state.final_category in ["D1", "D2"]:
                st.markdown("""
                <table class='table-style'>
                    <tr><th>Can thiệp điều trị nâng cao</th><th>Mức độ Khuyến cáo (COR & LOE)</th><th>Ý nghĩa lâm sàng theo AHA/ACC 2026</th></tr>
                    <tr><td><strong>Tiêu sợi huyết hệ thống (Systemic Lysis)</strong></td><td><span class='badge' style='background-color:#FFFBEB; color:#92400E;'>Class 2b, LOE C-LD</span></td><td>Có thể cân nhắc (nhằm ngăn ngừa diễn tiến lâm sàng xấu đi).</td></tr>
                    <tr><td><strong>CDL (Tiêu sợi huyết qua Catheter)</strong></td><td><span class='badge' style='background-color:#FFFBEB; color:#92400E;'>Class 2b, LOE B-NR</span></td><td>Có thể cân nhắc lựa chọn.</td></tr>
                    <tr><td><strong>MT (Lấy huyết khối cơ học qua da)</strong></td><td><span class='badge' style='background-color:#FFFBEB; color:#92400E;'>Class 2b, LOE B-NR</span></td><td>Có thể cân nhắc lựa chọn.</td></tr>
                    <tr><td><strong>Phẫu thuật lấy huyết khối (Surgical Embolectomy)</strong></td><td><span class='badge' style='background-color:#FFFBEB; color:#92400E;'>Class 2b, LOE C-LD</span></td><td>Hiệu quả lâm sàng chưa rõ ràng (uncertain/unclear).</td></tr>
                </table>
""", unsafe_allow_html=True)
                
            elif st.session_state.final_category == "E1":
                st.markdown("""
                <table class='table-style'>
                    <tr><th>Can thiệp điều trị nâng cao</th><th>Mức độ Khuyến cáo (COR & LOE)</th><th>Ý nghĩa lâm sàng theo AHA/ACC 2026</th></tr>
                    <tr><td><strong>Tiêu sợi huyết hệ thống (Systemic Lysis)</strong></td><td><span class='badge' style='background-color:#F0FDF4; color:#166534;'>Class 2a, LOE C-LD</span></td><td>Hợp lý để lựa chọn thay vì chỉ sử dụng kháng đông đơn thuần.</td></tr>
                    <tr><td><strong>CDL (Tiêu sợi huyết qua Catheter)</strong></td><td><span class='badge' style='background-color:#F0FDF4; color:#166534;'>Class 2a, LOE C-LD</span></td><td>Hợp lý để lựa chọn.</td></tr>
                    <tr><td><strong>MT (Lấy huyết khối cơ học qua da)</strong></td><td><span class='badge' style='background-color:#F0FDF4; color:#166534;'>Class 2a, LOE B-NR</span></td><td>Hợp lý để lựa chọn.</td></tr>
                    <tr><td><strong>Phẫu thuật lấy huyết khối (Surgical Embolectomy)</strong></td><td><span class='badge' style='background-color:#F0FDF4; color:#166534;'>Class 2a, LOE B-NR</span></td><td>Hợp lý để lựa chọn.</td></tr>
                </table>
""", unsafe_allow_html=True)
                
            elif st.session_state.final_category == "E2":
                st.markdown("""
                <table class='table-style'>
                    <tr><th>Can thiệp điều trị nâng cao</th><th>Mức độ Khuyến cáo (COR & LOE)</th><th>Ý nghĩa lâm sàng theo AHA/ACC 2026</th></tr>
                    <tr><td><strong>Tiêu sợi huyết hệ thống (Systemic Lysis)</strong></td><td><span class='badge' style='background-color:#F0FDF4; color:#166534;'>Class 2a, LOE C-LD</span></td><td>Hợp lý để lựa chọn thay vì chỉ sử dụng kháng đông đơn thuần.</td></tr>
                    <tr><td><strong>CDL (Tiêu sợi huyết qua Catheter)</strong></td><td><span class='badge' style='background-color:#94A3B8; color:#1E293B;'>N/A</span></td><td>Không phù hợp (Not applicable).</td></tr>
                    <tr><td><strong>MT (Lấy huyết khối cơ học qua da)</strong></td><td><span class='badge' style='background-color:#94A3B8; color:#1E293B;'>N/A</span></td><td>Không phù hợp (Not applicable).</td></tr>
                    <tr><td><strong>Phẫu thuật lấy huyết khối (Surgical Embolectomy)</strong></td><td><span class='badge' style='background-color:#FEF2F2; color:#991B1B;'>Class 3: No Benefit, LOE B-NR</span></td><td>Không khuyến cáo (Không có lợi ích) trừ khi được thực hiện song song với thiết bị hỗ trợ tuần hoàn cơ học (MCS/VA-ECMO).</td></tr>
                </table>
""", unsafe_allow_html=True)
                st.info("💡 **Hỗ trợ VA-ECMO trong Nhóm E2 (Sốc tim kháng trị / Ngừng tuần hoàn):** Khuyến cáo thiết lập VA-ECMO (**Class 2a, LOE B-NR**) để ổn định huyết động và hỗ trợ chức năng tim phổi hồi sức nâng cao (E-CPR).")
            _next4 = 5 if st.session_state.resp_modifier else (6 if (not st.session_state.is_pregnant and not is_breastfeeding_t2 and st.session_state.final_category in ["C1", "C2", "C3", "D1", "D2", "E1", "E2"]) else None)
            if _next4 and st.button("Tiếp tục → Nội dung điều trị tiếp theo", type="primary", use_container_width=True, key="step3_after_reperfusion"):
                st.session_state.step3_open = _next4
                st.rerun()
    if st.session_state.resp_modifier:
        if render_flow_sub_header("3.5 📢 Hỗ trợ hô hấp — Modifier R", 5, "step3_open", "step3_sub"):
            st.error("📢 **CẢNH BÁO SUY HÔ HẤP (Respiratory Modifier R):**\nBệnh nhân có suy hô hấp đi kèm. Theo Hướng dẫn AHA/ACC 2026, liệu pháp oxy dòng cao qua gọng mũi (HFNC) được khuyến cáo sử dụng ở bệnh nhân có suy hô hấp giảm oxy máu từ vừa đến nặng (Class 2a, LOE C-LD).\\n\\n*Lưu ý lâm sàng cực kỳ quan trọng:* Khuyến cáo không tự ý áp dụng thông khí áp lực dương (như NIV/CPAP hoặc thở máy xâm lấn) như một phương án ưu tiên thường quy, vì áp lực dương lồng ngực làm giảm tiền gánh và tăng hậu gánh thất phải cấp, dễ dẫn đến sụp đổ tuần hoàn tim phải cấp (NIV/thông khí áp lực dương chính là một marker lâm sàng của mức độ nguy kịch E-R).")
            if (not st.session_state.is_pregnant and not is_breastfeeding_t2 and st.session_state.final_category in ["C1", "C2", "C3", "D1", "D2", "E1", "E2"]) and st.button("Tiếp tục → Kế hoạch duy trì dài hạn", type="primary", use_container_width=True, key="step3_after_resp"):
                st.session_state.step3_open = 6
                st.rerun()
    if not st.session_state.is_pregnant and not is_breastfeeding_t2 and st.session_state.final_category in ["C1", "C2", "C3", "D1", "D2", "E1", "E2"]:
        if render_flow_sub_header("3.6 🔄 Kế hoạch Chuyển đổi Kháng đông & Duy trì dài hạn", 6, "step3_open", "step3_sub"):
            st.markdown("<div style='background-color: #F8FAFC; border-left: 5px solid #2563EB; padding: 20px; border-radius: 8px;'>", unsafe_allow_html=True)
            
            # Check các tình huống đặc biệt để hướng dẫn chuyển đổi
            if has_aps:
                st.error("🩸 **HỘI CHỨNG KHÁNG PHOSPHOLIPID (APS) (CHỐNG CHỈ ĐỊNH DOACs - Class 1, LOE A):**\n- **Thời gian tiêm gối:** Phải tiêm kháng đông đầy đủ (LMWH hoặc UFH) khởi đầu, đồng thời bắt đầu uống **Warfarin (VKA)** hằng ngày.\n- **Quy trình chuyển đổi:** Phải duy trì gối overlap cả tiêm và uống trong **ít nhất 5 ngày VÀ cho đến khi INR đạt mục tiêu 2.0 - 3.0 trong 24 giờ liên tục** (2 lần đo cách nhau 24h). Khi INR đạt đích y khoa, ngừng kháng đông tiêm.\n- **Thời gian duy trì:** Bắt buộc duy trì Warfarin lâu dài **vô hạn định** với đích INR 2.0 - 3.0 (Class 1, LOE A) để tránh huyết khối động mạch/tĩnh mạch tái phát cực kỳ nguy kịch.")
            elif has_cancer:
                st.info("🎗️ **UNG THƯ TIẾN TRIỂN (Cancer-Associated Thrombosis):**\n- **Kháng đông ưu tiên:** Khuyến cáo sử dụng **DOAC (Apixaban hoặc Rivaroxaban) ưu tiên hơn VKA (Class 1, LOE B-R)**. Việc chuyển đổi từ tiêm LMWH sang DOAC đường uống thực hiện ngay vào thời điểm liều LMWH tiếp theo chuẩn bị tiêm (không cần gối overlap).\n- **Thời gian điều trị:** Điều trị tối thiểu từ **3 đến 6 tháng** (Class 1, LOE A), và kéo dài **vô hạn định** miễn là ung thư còn hoạt động hoặc đang tiếp nhận hóa/xạ trị (Class 1, LOE A).")
            elif has_drug_interactions:
                st.warning("⚠️ **TƯƠNG TÁC THUỐC MẠNH:**\n- Do tương tác làm thay đổi nồng độ DOACs nguy hiểm, khuyến cáo **tránh dùng DOACs**. Duy trì kháng đông tiêm LMWH dài hạn hoặc gối sang Warfarin (VKA) với thời gian gối overlap ít nhất 5 ngày và INR đạt 2.0 - 3.0 mới ngắt tiêm. Duy trì từ 3 - 6 tháng hoặc kéo dài tùy yếu tố nguy cơ.")
            else:
                st.success("🏠 **DUY TRÌ THÔNG THƯỜNG (Standard Case - Không có bối cảnh đặc biệt):**\n- **Kháng đông ưu tiên:** Khuyến cáo chuyển đổi từ kháng đông tiêm sang **DOACs đường uống** (Apixaban hoặc Rivaroxaban) (Class 1, LOE B-R) sau khi bệnh nhân ổn định tại viện.\n- **Cách thức chuyển đổi:** Bắt đầu uống liều DOAC đầu tiên **ngay vào thời điểm liều LMWH tiếp theo chuẩn bị tiêm** (không cần gối overlap liều), hoặc uống ngay khi ngừng truyền UFH tĩnh mạch.\n- **Thời gian điều trị cụ thể (Duration):**\n  1. **Nếu PE do yếu tố nguy cơ có thể đảo ngược lớn (như phẫu thuật lớn):** Ngừng điều trị kháng đông sau **3 tháng** điều trị đầy đủ (Class 1, LOE B-NR) để cân bằng lợi ích - nguy cơ chảy máu.\n  2. **Nếu PE tự phát (không rõ nguyên nhân) hoặc có yếu tố nguy cơ dai dẳng:** Khuyến cáo tiếp tục điều trị kháng đông kéo dài **vô hạn định (extended phase)** (Class 1, LOE A) với việc đánh giá định kỳ nguy cơ chảy máu và lợi ích (Class 1, LOE B-NR). Khi chuyển sang giai đoạn kéo dài (sau 3-6 tháng), khuyến cáo **giảm xuống liều dự phòng thứ phát: Apixaban 2.5mg BID HOẶC Rivaroxaban 10mg hằng ngày** để giảm nguy cơ chảy máu nặng (Class 1, LOE A).")
            st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("---")
    if st.button("⬅️ Quay lại Giai đoạn Phân loại (Bước 2)"):
        st.session_state.step = 2
        st.rerun()
