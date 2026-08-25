# -*- coding: utf-8 -*-
"""
CDSS Rối loạn lipid máu ở người lớn — ACC/AHA 2026

Nguồn lâm sàng chính:
Blumenthal RS, et al. 2026 ACC/AHA/AACVPR/ABC/ACPM/ADA/AGS/APhA/ASPC/NLA/PCNA
Guideline on the Management of Dyslipidemia.
Circulation. 2026;153:e1154-e1276. DOI: 10.1161/CIR.0000000000001423

PREVENT-ASCVD:
Khan SS, et al. Development and Validation of the American Heart Association
PREVENT Equations. Circulation. 2024;149:430-449.
DOI: 10.1161/CIRCULATIONAHA.123.067626

Phiên bản v3:
- Toàn bộ heading dùng đúng hệ thống nút accordion của PE/CCS; không dùng st.expander mặc định.
- PREVENT-ASCVD Base 10 năm được tính OFFLINE bằng phương trình đã công bố;
  không gọi endpoint AHA nên không còn lỗi HTTP 403.
- Phần "Cá thể hóa bằng yếu tố làm tăng nguy cơ" chỉ xuất hiện khi
  PREVENT-ASCVD nằm trong khoảng 6% đến 15% theo yêu cầu thiết kế hiện tại.
- Bước điều trị hỏi phác đồ hạ lipid hiện tại và cường độ statin để điều chỉnh
  hành động khởi trị/tăng cường/thêm thuốc.
- File này KHÔNG tạo sidebar; sidebar do file điều hướng trung tâm quản lý.
- Phiên bản này chưa triển khai nhánh thai kỳ/cho con bú.
"""

import math
import streamlit as st


# =========================================================
# CẤU HÌNH TRANG
# =========================================================
st.set_page_config(
    page_title="Rối loạn lipid máu - ACC/AHA 2026",
    page_icon="🩸",
    layout="wide",
)


# =========================================================
# GIAO DIỆN
# =========================================================
st.markdown("""
<style>
    .stApp, .reportview-container { background: #f8fafc; }

    .block-container {
        max-width: 1480px;
        padding-top: 3.0rem;
        padding-bottom: 3rem;
    }

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

    .main-subtitle, .main-subtitle * {
        text-align: center !important;
        color: #475569 !important;
        font-size: 1.02rem !important;
        font-weight: 600 !important;
        line-height: 1.06 !important;
        margin: 0 0 4px 0 !important;
    }

    .header-divider {
        width: 100% !important;
        height: 1px !important;
        background: #d5dee8 !important;
        border: 0 !important;
        margin: 12px 0 20px 0 !important;
        padding: 0 !important;
    }

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

    div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stMarkdownContainer"] li,
    label { font-size: 1.03rem !important; }

    section.main div[data-testid="stVerticalBlock"] { gap: 0.35rem !important; }

    .path-main {
        background-color: #e8f4f8;
        border-left: 6px solid #1e3d59;
        padding: 15px;
        border-radius: 4px;
        margin: 10px 0;
    }
    .path-extra {
        background-color: #fff8e8;
        border-left: 6px solid #f39c12;
        padding: 15px;
        border-radius: 4px;
        margin: 10px 0;
    }
    .target-card {
        background-color: #e8f4f8;
        border-left: 6px solid #1e3d59;
        padding: 15px;
        border-radius: 4px;
        margin: 10px 0;
    }
    .treat-card {
        background-color: #f7f9fa;
        border: 1px solid #d3d3d3;
        padding: 12px;
        border-radius: 4px;
        margin: 10px 0;
    }

    @media (max-width: 1200px) {
        h1.main-title,
        div[data-testid="stMarkdownContainer"] h1.main-title,
        h1.main-title span,
        h1.main-title * { font-size: 2.30rem !important; }
    }
    @media (max-width: 768px) {
        .block-container { padding-top: 2rem; }
        h1.main-title,
        div[data-testid="stMarkdownContainer"] h1.main-title,
        h1.main-title span,
        h1.main-title * {
            font-size: 1.95rem !important;
            line-height: 1.04 !important;
            white-space: normal !important;
        }
        .main-subtitle, .main-subtitle * { font-size: 0.94rem !important; }
        h1:not(.main-title) { font-size: 1.30rem !important; }
        h2 { font-size: 1.16rem !important; }
        h3, h4 { font-size: 0.98rem !important; }
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# HÀM TIỆN ÍCH
# =========================================================

def render_main_step_header(title, step_id):
    current_step = st.session_state.lipid_step
    is_active = current_step == step_id
    is_completed = current_step > step_id
    is_open = st.session_state.get("lipid_open_main", current_step) == step_id

    arrow = "▼" if is_open else "▶"
    prefix = "✅ " if is_completed else ""
    status_text = " [ĐANG THỰC HIỆN]" if is_active else ""

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

    widget_key = f"lipid_main_step_btn_{step_id}"
    st.markdown(f"""
    <style>
    div[class*="st-key-{widget_key}"] button {{
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
    div[class*="st-key-{widget_key}"] button p,
    div[class*="st-key-{widget_key}"] button span {{
        font-size: 1.42rem !important;
        line-height: 1.04 !important;
        font-weight: 900 !important;
        color: {step_text} !important;
        letter-spacing: 0.25px !important;
        margin: 0 !important;
    }}
    @media (max-width: 768px) {{
        div[class*="st-key-{widget_key}"] button {{ padding: 5px 9px !important; min-height: 38px !important; }}
        div[class*="st-key-{widget_key}"] button p,
        div[class*="st-key-{widget_key}"] button span {{ font-size: 1.18rem !important; }}
    }}
    </style>
    """, unsafe_allow_html=True)

    if st.button(f"{arrow} {prefix}{title}{status_text}", key=widget_key):
        st.session_state.lipid_open_main = 0 if is_open else step_id
        st.rerun()

    return is_open


def render_sub_header(title, sub_step_id, session_key):
    current_sub = st.session_state.get(session_key, 1)
    is_active = current_sub == sub_step_id
    arrow = "▼" if is_active else "▶"

    sub_bg = "#eaf4fb" if is_active else "#fbfdff"
    sub_border = "#3498db" if is_active else "#c7d8e5"
    sub_text = "#174d70" if is_active else "#4d6475"
    sub_weight = 820 if is_active else 680
    sub_size = "1.10rem" if is_active else "1.02rem"

    widget_key = f"lipid_btn_{session_key}_{sub_step_id}"
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
    </style>
    """, unsafe_allow_html=True)

    if st.button(f"{arrow} {title}", key=widget_key):
        st.session_state[session_key] = 0 if is_active else sub_step_id
        st.rerun()

    return is_active


def is_severe_hyperchol(ldl_now, untreated_known, untreated_ldl):
    if ldl_now >= 190:
        return True
    if untreated_known and untreated_ldl is not None and untreated_ldl >= 190:
        return True
    return False


def classify_tg(tg, fasting_status):
    """
    Không suy diễn tăng TG nặng từ mẫu không nhịn đói.
    """
    if fasting_status == "Nhịn đói":
        if tg >= 1000:
            return True, "≥1000 mg/dL"
        if tg >= 500:
            return True, "500–999 mg/dL"
        if tg >= 150:
            return True, "150–499 mg/dL"
        return False, "Không tăng"
    if tg >= 175:
        return True, "Tăng trên mẫu không nhịn đói"
    return False, "Không tăng"


def main_pathway(data):
    if data["ascvd"]:
        return "Dự phòng thứ phát"
    if data["severe_hyperchol"]:
        return "Tăng cholesterol máu nặng"
    if data["diabetes"]:
        return "Đái tháo đường chưa có bệnh tim mạch do xơ vữa"
    if data["subclinical_active"]:
        return "Xơ vữa động mạch vành dưới lâm sàng"
    if 30 <= data["age"] <= 79 and 70 <= data["ldl"] < 190:
        return "Dự phòng tiên phát"
    return "Chưa đủ điều kiện để xếp vào một nhánh điều trị tự động của phiên bản này"


def risk_category(risk):
    if risk < 3:
        return "Nguy cơ thấp", "🟢"
    if risk < 5:
        return "Nguy cơ cận biên", "🟡"
    if risk < 10:
        return "Nguy cơ trung gian", "🟠"
    return "Nguy cơ cao", "🔴"


def validate_prevent_base_inputs(age, tc, hdl, sbp, egfr):
    errors = []
    if not 30 <= age <= 79:
        errors.append("Tuổi phải trong khoảng 30–79.")
    if not 130 <= tc <= 320:
        errors.append("Cholesterol toàn phần phải trong khoảng 130–320 mg/dL.")
    if not 20 <= hdl <= 100:
        errors.append("HDL-C phải trong khoảng 20–100 mg/dL.")
    if not 90 <= sbp <= 200:
        errors.append("Huyết áp tâm thu phải trong khoảng 90–200 mmHg.")
    if egfr <= 0:
        errors.append("eGFR phải >0 mL/phút/1,73 m².")
    return errors


def calculate_prevent_base_10y_ascvd(
    sex,
    age,
    total_chol,
    hdl,
    sbp,
    egfr,
    antihypertensive,
    statin,
    diabetes,
    smoker,
):
    """
    PREVENT-ASCVD Base 10 năm, logistic equation.

    Biến đổi:
    age=(age-55)/10
    non-HDL mmol/L=(TC-HDL)*0.02586; centered at 3.5
    HDL mmol/L centered/scaled at 1.3/0.3
    SBP piecewise: <110 and >=110
    eGFR piecewise: <60 and >=60
    """

    errors = validate_prevent_base_inputs(age, total_chol, hdl, sbp, egfr)
    if errors:
        raise ValueError(" ".join(errors))

    age_t = (float(age) - 55.0) / 10.0
    non_hdl_mmol = (float(total_chol) - float(hdl)) * 0.02586
    non_hdl_t = non_hdl_mmol - 3.5
    hdl_t = (float(hdl) * 0.02586 - 1.3) / 0.3

    sbp_lt110 = (min(float(sbp), 110.0) - 110.0) / 20.0
    sbp_gte110 = (max(float(sbp), 110.0) - 130.0) / 20.0

    egfr_lt60 = (min(float(egfr), 60.0) - 60.0) / -15.0
    egfr_gte60 = (max(float(egfr), 60.0) - 90.0) / -15.0

    dm = 1.0 if diabetes else 0.0
    smk = 1.0 if smoker else 0.0
    bptx = 1.0 if antihypertensive else 0.0
    stat = 1.0 if statin else 0.0

    if sex == "Nữ":
        c = {
            "const": -3.8199750,
            "age": 0.7198830,
            "nh": 0.1176967,
            "hdl": -0.1511850,
            "sbp_lo": -0.0835358,
            "sbp_hi": 0.3592852,
            "dm": 0.8348585,
            "smk": 0.4831078,
            "egfr_lo": 0.4864619,
            "egfr_hi": 0.0397779,
            "bptx": 0.2265309,
            "statin": -0.0592374,
            "bptx_sbp": -0.0395762,
            "statin_nh": 0.0844423,
            "age_nh": -0.0567839,
            "age_hdl": 0.0325692,
            "age_sbp": -0.1035985,
            "age_dm": -0.2417542,
            "age_smk": -0.0791142,
            "age_egfr": -0.1671492,
        }
    else:
        c = {
            "const": -3.5006550,
            "age": 0.7099847,
            "nh": 0.1658663,
            "hdl": -0.1144285,
            "sbp_lo": -0.2837212,
            "sbp_hi": 0.3239977,
            "dm": 0.7189597,
            "smk": 0.3956973,
            "egfr_lo": 0.3690075,
            "egfr_hi": 0.0203619,
            "bptx": 0.2036522,
            "statin": -0.0865581,
            "bptx_sbp": -0.0322916,
            "statin_nh": 0.1145630,
            "age_nh": -0.0300005,
            "age_hdl": 0.0232747,
            "age_sbp": -0.0927024,
            "age_dm": -0.2018525,
            "age_smk": -0.0970527,
            "age_egfr": -0.1217081,
        }

    lp = (
        c["const"]
        + c["age"] * age_t
        + c["nh"] * non_hdl_t
        + c["hdl"] * hdl_t
        + c["sbp_lo"] * sbp_lt110
        + c["sbp_hi"] * sbp_gte110
        + c["dm"] * dm
        + c["smk"] * smk
        + c["egfr_lo"] * egfr_lt60
        + c["egfr_hi"] * egfr_gte60
        + c["bptx"] * bptx
        + c["statin"] * stat
        + c["bptx_sbp"] * bptx * sbp_gte110
        + c["statin_nh"] * stat * non_hdl_t
        + c["age_nh"] * age_t * non_hdl_t
        + c["age_hdl"] * age_t * hdl_t
        + c["age_sbp"] * age_t * sbp_gte110
        + c["age_dm"] * age_t * dm
        + c["age_smk"] * age_t * smk
        + c["age_egfr"] * age_t * egfr_lt60
    )

    return 100.0 / (1.0 + math.exp(-lp))


def preferred_statin_box(intensity):
    if intensity == "high":
        st.markdown(
            """
<div class="treat-card">
<b>Statin cường độ cao — giảm LDL-C kỳ vọng ≥50%</b><br>
• Atorvastatin 40–80 mg/ngày<br>
• Rosuvastatin 20–40 mg/ngày
</div>
""",
            unsafe_allow_html=True,
        )
    elif intensity == "moderate":
        st.markdown(
            """
<div class="treat-card">
<b>Statin cường độ trung bình — giảm LDL-C kỳ vọng 30–49%</b><br>
• Atorvastatin 10–20 mg/ngày<br>
• Rosuvastatin 5–10 mg/ngày
</div>
""",
            unsafe_allow_html=True,
        )


STATIN_RANK = {
    "Không dùng statin": 0,
    "Statin cường độ thấp": 1,
    "Statin cường độ trung bình": 2,
    "Statin cường độ cao": 3,
}


def current_therapy_interpretation(
    treated,
    current_statin,
    current_nonstatin,
    required_intensity,
    current_ldl,
    target_ldl=None,
):
    """
    Chỉ diễn giải hành động từ dữ liệu người dùng đã nhập.
    Không tự quy cường độ cho "statin tối đa dung nạp" hoặc "không dung nạp".
    """
    if not treated:
        if required_intensity == "high":
            st.success("➡️ Hiện chưa điều trị: ưu tiên **khởi trị statin cường độ cao** nếu không có chống chỉ định.")
        elif required_intensity == "moderate":
            st.success("➡️ Hiện chưa điều trị: ưu tiên **khởi trị ít nhất statin cường độ trung bình** nếu không có chống chỉ định.")
        else:
            st.info("➡️ Hiện chưa điều trị: quyết định khởi trị dựa trên nhánh nguy cơ bên dưới.")
        return

    if current_statin == "Không dung nạp/không thể dùng statin":
        st.warning(
            "➡️ Người bệnh không dung nạp/không thể dùng statin: không áp dụng logic tăng cường cường độ statin; "
            "cần lựa chọn thuốc không statin theo nhóm nguy cơ và mục tiêu LDL-C."
        )
        return

    if current_statin == "Statin tối đa dung nạp nhưng không đạt cường độ khuyến cáo":
        if target_ldl is not None and current_ldl >= target_ldl:
            st.warning(
                "➡️ Đã dùng statin tối đa dung nạp nhưng LDL-C còn trên mục tiêu: "
                "chuyển trọng tâm sang **thêm/tối ưu thuốc không statin** theo nhánh điều trị."
            )
        else:
            st.info("➡️ Đang dùng statin tối đa dung nạp; không tự ép tăng cường độ vượt khả năng dung nạp.")
        return

    rank = STATIN_RANK.get(current_statin, 0)
    req_rank = 3 if required_intensity == "high" else (2 if required_intensity == "moderate" else None)

    if req_rank is not None and rank < req_rank:
        name = "cao" if required_intensity == "high" else "trung bình"
        st.warning(
            f"➡️ Cường độ statin hiện tại thấp hơn cường độ được ưu tiên trong nhánh này: "
            f"**cân nhắc tăng lên cường độ {name}** nếu dung nạp."
        )
    elif req_rank is not None and rank >= req_rank:
        if target_ldl is not None and current_ldl >= target_ldl:
            if current_nonstatin:
                st.warning(
                    "➡️ Đã đạt cường độ statin phù hợp nhưng LDL-C còn trên mục tiêu và đã có thuốc không statin: "
                    "cần đánh giá mức hạ LDL-C còn thiếu và tối ưu/bổ sung điều trị theo nhánh bên dưới."
                )
            else:
                st.warning(
                    "➡️ Đã đạt cường độ statin phù hợp nhưng LDL-C còn trên mục tiêu: "
                    "**cân nhắc thêm thuốc không statin** theo nhánh bên dưới."
                )
        elif target_ldl is not None and current_ldl < target_ldl:
            st.success("➡️ LDL-C hiện đã dưới mục tiêu đã xác định; tiếp tục đánh giá dung nạp, tuân thủ và theo dõi.")
        else:
            st.info("➡️ Cường độ statin hiện tại phù hợp với cường độ được ưu tiên trong nhánh này.")


def treatment_current_regimen(default_on_statin=False):
    default_treated = "Có điều trị" if default_on_statin else "Chưa điều trị"
    treated_choice = st.radio(
        "Người bệnh hiện đã được điều trị hạ lipid máu chưa?",
        ["Chưa điều trị", "Có điều trị"],
        index=1 if default_treated == "Có điều trị" else 0,
        horizontal=True,
        key="lipid_tx_current_status",
    )

    treated = treated_choice == "Có điều trị"
    current_statin = "Không dùng statin"
    current_nonstatin = []

    if treated:
        current_statin = st.selectbox(
            "Cường độ statin hiện tại:",
            [
                "Không dùng statin",
                "Statin cường độ thấp",
                "Statin cường độ trung bình",
                "Statin cường độ cao",
                "Statin tối đa dung nạp nhưng không đạt cường độ khuyến cáo",
                "Không dung nạp/không thể dùng statin",
            ],
            key="lipid_tx_current_statin",
        )
        current_nonstatin = st.multiselect(
            "Thuốc hạ LDL-C khác đang dùng:",
            [
                "Ezetimibe",
                "PCSK9 mAb",
                "Bempedoic acid",
                "Inclisiran",
            ],
            key="lipid_tx_current_nonstatin",
        )

    return treated, current_statin, current_nonstatin


def render_dose_table():
    st.markdown(
        """
- **Ezetimibe:** 10 mg/ngày.
- **Bempedoic acid:** 180 mg/ngày.
- **Alirocumab:** 75–150 mg tiêm dưới da mỗi 2 tuần, hoặc 300 mg mỗi 4 tuần.
- **Evolocumab:** 140 mg tiêm dưới da mỗi 2 tuần.
- **Inclisiran:** 284 mg tiêm dưới da liều đầu, liều thứ hai sau 3 tháng, sau đó mỗi 6 tháng.

**Ghi chú:** lựa chọn thuốc bổ sung phụ thuộc mức LDL-C cần hạ, nguy cơ tuyệt đối,
khả năng dung nạp, khả năng tiếp cận và ưu tiên của người bệnh.
"""
    )


# =========================================================
# KHỞI TẠO TRẠNG THÁI
# =========================================================
if "lipid_step" not in st.session_state:
    st.session_state.lipid_step = 1
if "lipid_initial" not in st.session_state:
    st.session_state.lipid_initial = None
if "lipid_path" not in st.session_state:
    st.session_state.lipid_path = None
if "lipid_risk" not in st.session_state:
    st.session_state.lipid_risk = None
if "lipid_step2" not in st.session_state:
    st.session_state.lipid_step2 = {}
if "lipid_open_main" not in st.session_state:
    st.session_state.lipid_open_main = st.session_state.lipid_step
if "lipid_step1_sub" not in st.session_state:
    st.session_state.lipid_step1_sub = 1
if "lipid_step2_sub" not in st.session_state:
    st.session_state.lipid_step2_sub = 1
if "lipid_step3_sub" not in st.session_state:
    st.session_state.lipid_step3_sub = 1


# =========================================================
# TIÊU ĐỀ
# =========================================================
st.markdown("<h1 class='main-title'>🩸 TIẾP CẬN RỐI LOẠN LIPID MÁU</h1>", unsafe_allow_html=True)
st.markdown("<div class='main-subtitle'>Hệ thống Hỗ trợ Quyết định Lâm sàng theo ACC/AHA 2026</div>", unsafe_allow_html=True)
st.markdown("<div class='header-divider'></div>", unsafe_allow_html=True)

st.caption(
    "Phạm vi hiện tại: người lớn. Phiên bản này chưa triển khai xử trí thai kỳ/cho con bú. "
    "Công cụ hỗ trợ quyết định, không thay thế đánh giá lâm sàng."
)


# =========================================================
# BƯỚC 1 — THÔNG TIN BAN ĐẦU
# =========================================================
step1_label = (
    "🟢 BƯỚC 1: THÔNG TIN BAN ĐẦU"
    if st.session_state.lipid_step == 1
    else "✅ BƯỚC 1: THÔNG TIN BAN ĐẦU"
)

if render_main_step_header("BƯỚC 1: THÔNG TIN BAN ĐẦU", 1):
    if st.session_state.lipid_step == 1:
        if render_sub_header("1.1 Thông tin cần thiết để phân nhóm", 1, "lipid_step1_sub"):
            col1, col2 = st.columns(2)
            with col1:
                age = st.number_input("Tuổi:", min_value=18, max_value=120, value=55, step=1, key="lip_age")
            with col2:
                sex = st.radio("Giới:", ["Nam", "Nữ"], horizontal=True, key="lip_sex")

            col1, col2 = st.columns(2)
            with col1:
                ldl = st.number_input(
                    "LDL-C hiện tại (mg/dL):",
                    min_value=0.0,
                    value=120.0,
                    step=1.0,
                    key="lip_ldl",
                )
            with col2:
                tg = st.number_input(
                    "Triglycerid hiện tại (mg/dL):",
                    min_value=0.0,
                    value=140.0,
                    step=1.0,
                    key="lip_tg",
                )

            fasting_status = st.radio(
                "Mẫu triglycerid:",
                ["Nhịn đói", "Không nhịn đói"],
                horizontal=True,
                key="lip_fasting",
            )

            untreated_status = st.radio(
                "Có biết LDL-C trước khi bắt đầu điều trị hạ lipid không?",
                ["Không rõ", "Có"],
                horizontal=True,
                key="lip_untreated_status",
            )
            untreated_known = untreated_status == "Có"
            untreated_ldl = None
            if untreated_known:
                untreated_ldl = st.number_input(
                    "LDL-C trước điều trị / LDL-C cao nhất trước điều trị (mg/dL):",
                    min_value=0.0,
                    value=float(max(ldl, 120.0)),
                    step=1.0,
                    key="lip_untreated_ldl",
                )

            st.markdown("**Tình trạng bệnh:**")
            col1, col2 = st.columns(2)
            with col1:
                ascvd = st.checkbox(
                    "Có bệnh tim mạch do xơ vữa đã xác định",
                    help="Ví dụ: ACS, tiền sử nhồi máu cơ tim, đau thắt ngực ổn định/không ổn định, tái thông động mạch, đột quỵ/TIA, bệnh động mạch ngoại biên.",
                    key="lip_ascvd",
                )
            with col2:
                diabetes = st.checkbox("Có đái tháo đường", key="lip_diabetes")

            col1, col2 = st.columns(2)
            with col1:
                egfr = st.number_input(
                    "eGFR (mL/phút/1,73 m²):",
                    min_value=0.0,
                    value=90.0,
                    step=1.0,
                    key="lip_egfr",
                )
            with col2:
                statin_now = st.checkbox(
                    "Đang dùng statin",
                    help="Biến này được dùng trong phương trình PREVENT-ASCVD. Chi tiết cường độ/thuốc khác sẽ nhập ở Bước 3.",
                    key="lip_statin_now",
                )

            subclinical_type = st.selectbox(
                "Bằng chứng xơ vữa động mạch vành dưới lâm sàng:",
                [
                    "Chưa có",
                    "Có điểm CAC",
                    "Vôi hóa động mạch vành tình cờ trên CT không chuyên tim",
                ],
                key="lip_subclinical_type",
            )

            cac = None
            incidental_grade = None
            if subclinical_type == "Có điểm CAC":
                cac = st.number_input(
                    "Điểm CAC (Agatston):",
                    min_value=0.0,
                    value=0.0,
                    step=1.0,
                    key="lip_cac",
                )
            elif subclinical_type == "Vôi hóa động mạch vành tình cờ trên CT không chuyên tim":
                incidental_grade = st.selectbox(
                    "Mức độ được mô tả trên kết quả CT:",
                    ["Nhẹ", "Trung bình", "Nặng", "Không ghi rõ"],
                    key="lip_incidental_grade",
                )

            if egfr < 60:
                st.warning(
                    "⚠️ eGFR <60 mL/phút/1,73 m²: có tình trạng thận làm thay đổi một số khuyến cáo điều trị; "
                    "công cụ sẽ giữ thông tin này khi phân nhóm."
                )

            if st.button(
                "XÁC NHẬN & ĐÁNH GIÁ NGUY CƠ ➡️",
                type="primary",
                use_container_width=True,
                key="lip_go_step2",
            ):
                severe = is_severe_hyperchol(ldl, untreated_known, untreated_ldl)
                tg_active, tg_level = classify_tg(tg, fasting_status)

                subclinical_active = False
                if subclinical_type == "Có điểm CAC" and cac is not None and cac > 0:
                    subclinical_active = True
                elif subclinical_type == "Vôi hóa động mạch vành tình cờ trên CT không chuyên tim":
                    subclinical_active = True

                data = {
                    "age": int(age),
                    "sex": sex,
                    "ldl": float(ldl),
                    "tg": float(tg),
                    "fasting_status": fasting_status,
                    "untreated_known": untreated_known,
                    "untreated_ldl": float(untreated_ldl) if untreated_ldl is not None else None,
                    "ascvd": bool(ascvd),
                    "diabetes": bool(diabetes),
                    "egfr": float(egfr),
                    "statin_now": bool(statin_now),
                    "subclinical_type": subclinical_type,
                    "cac": float(cac) if cac is not None else None,
                    "incidental_grade": incidental_grade,
                    "subclinical_active": subclinical_active,
                    "severe_hyperchol": severe,
                    "tg_active": tg_active,
                    "tg_level": tg_level,
                }
                data["main_path"] = main_pathway(data)

                st.session_state.lipid_initial = data
                st.session_state.lipid_path = data["main_path"]
                st.session_state.lipid_risk = None
                st.session_state.lipid_step2 = {}
                st.session_state.lipid_step = 2
                st.session_state.lipid_open_main = 2
                st.session_state.lipid_step2_sub = 1
                st.rerun()

    else:
        d = st.session_state.lipid_initial
        if d:
            # Tương thích với session của bản trước
            if "statin_now" not in d:
                d["statin_now"] = bool(d.get("lipid_lowering_now", False))
            st.info(
                f"Tuổi {d['age']} • {d['sex']} • LDL-C {d['ldl']:.0f} mg/dL • "
                f"TG {d['tg']:.0f} mg/dL • eGFR {d['egfr']:.0f}"
            )
        if st.button("↩️ Sửa thông tin ban đầu", key="lip_back_to_1"):
            st.session_state.lipid_step = 1
            st.session_state.lipid_open_main = 1
            st.rerun()


# =========================================================
# BƯỚC 2 — ĐÁNH GIÁ NGUY CƠ VÀ PHÂN NHÓM
# =========================================================
if st.session_state.lipid_step == 1:
    step2_label = "🔒 BƯỚC 2: ĐÁNH GIÁ NGUY CƠ VÀ PHÂN NHÓM"
elif st.session_state.lipid_step == 2:
    step2_label = "🟢 BƯỚC 2: ĐÁNH GIÁ NGUY CƠ VÀ PHÂN NHÓM"
else:
    step2_label = "✅ BƯỚC 2: ĐÁNH GIÁ NGUY CƠ VÀ PHÂN NHÓM"

if render_main_step_header("BƯỚC 2: ĐÁNH GIÁ NGUY CƠ VÀ PHÂN NHÓM", 2):
    if st.session_state.lipid_step == 1:
        st.info("Hoàn tất Bước 1 để mở phần đánh giá nguy cơ và phân nhóm.")

    elif st.session_state.lipid_step == 2:
        d = st.session_state.lipid_initial
        if "statin_now" not in d:
            d["statin_now"] = bool(d.get("lipid_lowering_now", False))
        path = d["main_path"]

        st.markdown(
            f"""
<div class="path-main">
<b>🎯 NHÓM ĐIỀU TRỊ CHÍNH:</b> {path}
</div>
""",
            unsafe_allow_html=True,
        )

        coexisting = []
        if d["ascvd"] and d["severe_hyperchol"]:
            coexisting.append("Tăng cholesterol máu nặng")
        if d["ascvd"] and d["diabetes"]:
            coexisting.append("Đái tháo đường")
        if d["ascvd"] and d["subclinical_active"]:
            coexisting.append("Xơ vữa động mạch vành dưới lâm sàng")
        if (not d["ascvd"]) and path != "Tăng cholesterol máu nặng" and d["severe_hyperchol"]:
            coexisting.append("Tăng cholesterol máu nặng")
        if path not in ["Đái tháo đường chưa có bệnh tim mạch do xơ vữa", "Dự phòng thứ phát"] and d["diabetes"]:
            coexisting.append("Đái tháo đường")
        if path != "Xơ vữa động mạch vành dưới lâm sàng" and d["subclinical_active"]:
            coexisting.append("Xơ vữa động mạch vành dưới lâm sàng")
        if d["tg_active"]:
            coexisting.append("Tăng triglycerid máu")

        if coexisting:
            st.markdown(
                '<div class="path-extra"><b>⚠️ TÌNH TRẠNG ĐỒNG THỜI CẦN LƯU Ý:</b><br>'
                + " • ".join(coexisting)
                + "</div>",
                unsafe_allow_html=True,
            )

        step2 = {}

        # -------------------------------------------------
        # DỰ PHÒNG TIÊN PHÁT
        # -------------------------------------------------
        if path == "Dự phòng tiên phát":
            if render_sub_header("2.1 Tính nguy cơ bằng PREVENT-ASCVD", 1, "lipid_step2_sub"):
                st.caption(
                    "PREVENT-ASCVD Base 10 năm được tính trực tiếp trong ứng dụng bằng phương trình đã công bố; "
                    "không gọi dịch vụ web AHA."
                )

                if not (30 <= d["age"] <= 79):
                    st.error("PREVENT-ASCVD 10 năm không được áp dụng ngoài tuổi 30–79 trong nhánh này.")
                else:
                    st.markdown("**Mô hình:** PREVENT-ASCVD Base")

                    col1, col2 = st.columns(2)
                    with col1:
                        tc = st.number_input(
                            "Cholesterol toàn phần (mg/dL):",
                            min_value=0.0,
                            value=200.0,
                            step=1.0,
                            key="prevent_tc",
                        )
                        hdl = st.number_input(
                            "HDL-C (mg/dL):",
                            min_value=0.0,
                            value=50.0,
                            step=1.0,
                            key="prevent_hdl",
                        )
                    with col2:
                        sbp = st.number_input(
                            "Huyết áp tâm thu (mmHg):",
                            min_value=0.0,
                            value=120.0,
                            step=1.0,
                            key="prevent_sbp",
                        )
                        antihypertensive = st.checkbox(
                            "Đang dùng thuốc hạ huyết áp",
                            key="prevent_bptx",
                        )
                        smoker = st.checkbox(
                            "Đang hút thuốc",
                            key="prevent_smoker",
                        )

                    st.caption(
                        f"PREVENT đang sử dụng: eGFR {d['egfr']:.0f} • "
                        f"Đái tháo đường: {'Có' if d['diabetes'] else 'Không'} • "
                        f"Đang dùng statin: {'Có' if d['statin_now'] else 'Không'}."
                    )

                    if st.button(
                        "🧮 TÍNH PREVENT-ASCVD",
                        use_container_width=True,
                        key="prevent_calc",
                    ):
                        try:
                            risk10 = calculate_prevent_base_10y_ascvd(
                                sex=d["sex"],
                                age=d["age"],
                                total_chol=tc,
                                hdl=hdl,
                                sbp=sbp,
                                egfr=d["egfr"],
                                antihypertensive=antihypertensive,
                                statin=d["statin_now"],
                                diabetes=d["diabetes"],
                                smoker=smoker,
                            )
                            st.session_state.lipid_risk = {
                                "ascvd_10": float(risk10),
                                "model_name": "PREVENT-ASCVD Base (offline)",
                            }
                        except ValueError as e:
                            st.session_state.lipid_risk = None
                            st.error(f"Không tính được PREVENT-ASCVD: {e}")

                    risk_result = st.session_state.lipid_risk
                    if risk_result:
                        risk10 = risk_result["ascvd_10"]
                        cat, icon = risk_category(risk10)
                        c1, c2 = st.columns(2)
                        with c1:
                            st.metric("PREVENT-ASCVD 10 năm", f"{risk10:.1f}%")
                        with c2:
                            st.metric("Phân tầng", f"{icon} {cat}")
                        st.caption("Mô hình: PREVENT-ASCVD Base — tính offline.")
                        step2["prevent_risk"] = float(risk10)
                        step2["prevent_category"] = cat
                        step2["prevent_model"] = "Base"
                    else:
                        step2["prevent_risk"] = None

                    st.info(
                        "PREVENT được dùng để hỗ trợ quyết định ở người 30–79 tuổi chưa có ASCVD hoặc "
                        "xơ vữa dưới lâm sàng, LDL-C 70–189 mg/dL."
                    )

            risk_result = st.session_state.lipid_risk
            risk10 = risk_result["ascvd_10"] if risk_result else None

            # Yêu cầu thiết kế của người dùng: chỉ hiện từ 6% đến 15%
            if risk10 is not None and 6.0 <= risk10 <= 15.0:
                if render_sub_header("2.2 Cá thể hóa bằng các yếu tố làm tăng nguy cơ", 2, "lipid_step2_sub"):
                    enhancers = []

                    fam = st.checkbox(
                        "Tiền sử ASCVD sớm ở cha/mẹ hoặc anh/chị/em ruột "
                        "(nam <55 tuổi; nữ <65 tuổi)",
                        key="re_fam",
                    )
                    ancestry = st.checkbox(
                        "Nguồn gốc có nguy cơ cao (ví dụ Nam Á, Philippines)",
                        key="re_ancestry",
                    )
                    polygenic = st.checkbox(
                        "Nguy cơ đa gen cao (nếu đã được đo)",
                        key="re_polygenic",
                    )
                    inflammatory = st.checkbox(
                        "Bệnh viêm mạn (ví dụ lupus, viêm khớp dạng thấp, vảy nến nặng, viêm khớp viêm)",
                        key="re_inflammatory",
                    )
                    lpa_high = st.checkbox(
                        "Lp(a) ≥125 nmol/L hoặc ≥50 mg/dL",
                        key="re_lpa",
                    )
                    hscrp_high = st.checkbox(
                        "hsCRP ≥2 mg/L trên hơn 1 lần đo, không có nguyên nhân giải thích",
                        key="re_hscrp",
                    )
                    ckms = st.checkbox(
                        "Có hội chứng tim mạch–thận–chuyển hóa (CKM)",
                        key="re_ckm",
                    )
                    nonhdl_apob = st.checkbox(
                        "non-HDL-C 190–219 mg/dL hoặc ApoB ≥120 mg/dL",
                        key="re_nh_apob",
                    )

                    if fam:
                        enhancers.append("Tiền sử gia đình ASCVD sớm")
                    if ancestry:
                        enhancers.append("Nguồn gốc nguy cơ cao")
                    if polygenic:
                        enhancers.append("Nguy cơ đa gen cao")
                    if inflammatory:
                        enhancers.append("Bệnh viêm mạn")
                    if lpa_high:
                        enhancers.append("Lp(a) tăng")
                    if hscrp_high:
                        enhancers.append("hsCRP tăng")
                    if ckms:
                        enhancers.append("Hội chứng CKM")
                    if nonhdl_apob:
                        enhancers.append("non-HDL-C/ApoB tăng")
                    if 160 <= d["ldl"] <= 189:
                        enhancers.append("LDL-C kéo dài 160–189 mg/dL")
                    if d["tg_active"]:
                        enhancers.append("Triglycerid tăng kéo dài nếu được xác nhận")

                    step2["risk_enhancers"] = enhancers

                    if enhancers:
                        st.warning("Có yếu tố làm tăng nguy cơ: " + "; ".join(enhancers))
                    else:
                        st.info("Chưa ghi nhận yếu tố làm tăng nguy cơ từ các mục đã nhập.")

                    if hscrp_high:
                        st.warning(
                            "hsCRP ≥2 mg/L trên 2 lần liên tiếp, không có nguyên nhân khác: "
                            "guideline cho phép cân nhắc statin cường độ cao ở người nguy cơ cận biên."
                        )
            else:
                step2["risk_enhancers"] = []

            if render_sub_header("2.3 Tái phân loại bằng CAC khi cần", 3, "lipid_step2_sub"):
                if d["subclinical_type"] == "Chưa có":
                    consider_cac = st.checkbox(
                        "Quyết định điều trị vẫn chưa chắc chắn và muốn cân nhắc CAC để tái phân loại",
                        key="re_consider_cac",
                    )
                    step2["consider_cac"] = consider_cac
                    if consider_cac:
                        st.info(
                            "CAC có thể hỗ trợ tái phân loại ở nam ≥40 tuổi hoặc nữ ≥45 tuổi "
                            "khi quyết định khởi trị thuốc hạ lipid còn chưa chắc chắn."
                        )
                else:
                    step2["consider_cac"] = False
                    st.info(
                        "Bệnh nhân đã có dữ liệu xơ vữa mạch vành; "
                        "không yêu cầu CAC như một bước tái phân loại mới."
                    )

        # -------------------------------------------------
        # TĂNG CHOLESTEROL MÁU NẶNG
        # -------------------------------------------------
        elif path == "Tăng cholesterol máu nặng":
            if render_sub_header("2.1 Tăng cholesterol máu nặng", 1, "lipid_step2_sub"):
                st.success(
                    "LDL-C hiện tại hoặc LDL-C trước điều trị ≥190 mg/dL → "
                    "không dùng PREVENT để quyết định có điều trị hay không."
                )

                hefh = st.checkbox(
                    "Đã xác nhận HeFH bằng lâm sàng hoặc di truyền",
                    key="sh_hefh",
                )
                additional_risk = st.checkbox(
                    "Có thêm yếu tố nguy cơ ASCVD đã được xác định",
                    key="sh_additional_risk",
                )
                secondary_causes_reviewed = st.checkbox(
                    "Đã đánh giá nguyên nhân thứ phát của tăng LDL-C",
                    key="sh_secondary",
                )

                step2["hefh"] = hefh
                step2["additional_risk"] = additional_risk
                step2["secondary_causes_reviewed"] = secondary_causes_reviewed

                if not secondary_causes_reviewed and not d["ascvd"]:
                    st.warning("Cần đánh giá và xử trí nguyên nhân thứ phát của tăng LDL-C khi phù hợp.")

                if hefh:
                    st.info(
                        "HeFH là nhóm nguy cơ cao; không dùng công cụ nguy cơ chuẩn của dân số chung để 'hạ bậc' nguy cơ."
                    )

        # -------------------------------------------------
        # ĐÁI THÁO ĐƯỜNG
        # -------------------------------------------------
        elif path == "Đái tháo đường chưa có bệnh tim mạch do xơ vữa":
            if render_sub_header("2.1 Đái tháo đường chưa có bệnh tim mạch do xơ vữa", 1, "lipid_step2_sub"):
                dm_type = st.radio(
                    "Loại đái tháo đường:",
                    ["Típ 2", "Típ 1"],
                    horizontal=True,
                    key="dm_type",
                )
                duration = st.number_input(
                    "Thời gian mắc đái tháo đường (năm):",
                    min_value=0.0,
                    value=5.0,
                    step=1.0,
                    key="dm_duration",
                )
                albuminuria = st.checkbox("Albumin niệu ≥30 μg/mg creatinin", key="dm_albumin")
                retinopathy = st.checkbox("Có bệnh võng mạc do đái tháo đường", key="dm_retina")
                neuropathy = st.checkbox("Có bệnh thần kinh do đái tháo đường", key="dm_neuro")
                abi_low = st.checkbox("ABI <0,9", key="dm_abi")

                dm_enhancers = []
                if (dm_type == "Típ 2" and duration >= 10) or (dm_type == "Típ 1" and duration >= 20):
                    dm_enhancers.append("Thời gian mắc đái tháo đường kéo dài")
                if albuminuria:
                    dm_enhancers.append("Albumin niệu")
                if d["egfr"] < 60:
                    dm_enhancers.append("eGFR <60")
                if retinopathy:
                    dm_enhancers.append("Bệnh võng mạc")
                if neuropathy:
                    dm_enhancers.append("Bệnh thần kinh")
                if abi_low:
                    dm_enhancers.append("ABI <0,9")

                step2["dm_type"] = dm_type
                step2["dm_duration"] = float(duration)
                step2["dm_enhancers"] = dm_enhancers

                if 40 <= d["age"] <= 75:
                    st.success(
                        "Ở người 40–75 tuổi có đái tháo đường, statin cường độ trung bình được chỉ định "
                        "bất kể nguy cơ ASCVD 10 năm ước tính."
                    )
                else:
                    st.info(
                        "Ngoài tuổi 40–75, quyết định điều trị cần dựa vào nhóm tuổi và bối cảnh lâm sàng; "
                        "phiên bản này không tự ngoại suy khuyến cáo 40–75 tuổi."
                    )

                if dm_enhancers:
                    st.warning(
                        "Yếu tố làm tăng nguy cơ riêng của đái tháo đường: "
                        + "; ".join(dm_enhancers)
                    )

        # -------------------------------------------------
        # DỰ PHÒNG THỨ PHÁT
        # -------------------------------------------------
        elif path == "Dự phòng thứ phát":
            if render_sub_header("2.1 Bệnh tim mạch do xơ vữa đã xác định — dự phòng thứ phát", 1, "lipid_step2_sub"):
                st.markdown("**Biến cố ASCVD chính:**")
                major1 = st.checkbox("ACS trong 12 tháng qua", key="sec_acs")
                major2 = st.checkbox(
                    "Tiền sử nhồi máu cơ tim khác với ACS trong 12 tháng qua",
                    key="sec_mi",
                )
                major3 = st.checkbox("Tiền sử đột quỵ thiếu máu não", key="sec_stroke")
                major4 = st.checkbox("Bệnh động mạch ngoại biên có triệu chứng", key="sec_pad")
                major_count = sum([major1, major2, major3, major4])

                st.markdown("**Đặc điểm nguy cơ cao:**")
                high_risk_features = []

                if d["age"] >= 65:
                    high_risk_features.append("Tuổi ≥65")
                    st.caption("✓ Tuổi ≥65")

                revasc = st.checkbox("Đã CABG hoặc PCI", key="sec_revasc")
                smoker = st.checkbox("Đang hút thuốc", key="sec_smoker")
                hf = st.checkbox("Tiền sử suy tim", key="sec_hf")
                hypertension = st.checkbox("Tăng huyết áp", key="sec_htn")
                ldl100_on_combo = st.checkbox(
                    "LDL-C ≥100 mg/dL dù đã dùng statin tối đa dung nạp + ezetimibe",
                    key="sec_ldl100",
                )

                if revasc:
                    high_risk_features.append("CABG/PCI")
                if smoker:
                    high_risk_features.append("Hút thuốc")
                if d["diabetes"]:
                    high_risk_features.append("Đái tháo đường")
                    st.caption("✓ Đái tháo đường")
                if hf:
                    high_risk_features.append("Suy tim")
                if hypertension:
                    high_risk_features.append("Tăng huyết áp")
                if ldl100_on_combo:
                    high_risk_features.append("LDL-C ≥100 dù statin tối đa + ezetimibe")

                very_high = (major_count >= 2) or (
                    major_count >= 1 and len(high_risk_features) >= 2
                )

                step2["major_ascvd_count"] = major_count
                step2["high_risk_features"] = high_risk_features
                step2["very_high_risk"] = very_high

                if very_high:
                    st.error("🔴 Phân tầng: ASCVD NGUY CƠ RẤT CAO")
                else:
                    st.info(
                        "Chưa đủ tiêu chuẩn ASCVD nguy cơ rất cao theo dữ liệu đã nhập. "
                        "Bệnh nhân vẫn thuộc dự phòng thứ phát."
                    )

        # -------------------------------------------------
        # XƠ VỮA ĐMV DƯỚI LÂM SÀNG
        # -------------------------------------------------
        elif path == "Xơ vữa động mạch vành dưới lâm sàng":
            if render_sub_header("2.1 Xơ vữa động mạch vành dưới lâm sàng", 1, "lipid_step2_sub"):
                age_eligible = (
                    (d["sex"] == "Nam" and d["age"] >= 40)
                    or (d["sex"] == "Nữ" and d["age"] >= 45)
                )
                step2["subclinical_age_eligible"] = age_eligible

                if not age_eligible:
                    st.warning(
                        "Nhánh khuyến cáo CAC của guideline áp dụng cho nam ≥40 tuổi hoặc nữ ≥45 tuổi. "
                        "Công cụ không tự ngoại suy mục tiêu điều trị cho tuổi thấp hơn."
                    )

                if d["subclinical_type"] == "Có điểm CAC":
                    cac = d["cac"] or 0
                    percentile = None

                    if 1 <= cac <= 99:
                        percentile_known = st.checkbox(
                            "Có biết bách phân vị CAC",
                            key="cac_pct_known",
                        )
                        if percentile_known:
                            percentile = st.number_input(
                                "Bách phân vị CAC (%):",
                                min_value=0.0,
                                max_value=100.0,
                                value=50.0,
                                step=1.0,
                                key="cac_pct",
                            )

                    step2["cac"] = cac
                    step2["cac_percentile"] = percentile

                    if cac >= 1000:
                        cac_group = "CAC ≥1000"
                    elif cac >= 300:
                        cac_group = "CAC 300–999"
                    elif cac >= 100:
                        cac_group = "CAC 100–299"
                    elif cac >= 1:
                        if percentile is not None and percentile >= 75:
                            cac_group = "CAC 1–99 nhưng ≥bách phân vị 75"
                        else:
                            cac_group = "CAC 1–99"
                    else:
                        cac_group = "CAC = 0"

                    step2["cac_group"] = cac_group
                    st.success(f"Phân nhóm CAC: **{cac_group}**")

                    if 1 <= cac <= 99 and percentile is None:
                        st.caption(
                            "Nếu CAC 1–99 nhưng bách phân vị ≥75, khuyến cáo điều trị mạnh hơn; "
                            "hãy bổ sung bách phân vị khi có."
                        )

                else:
                    grade = d["incidental_grade"]
                    step2["incidental_grade"] = grade
                    if grade == "Nhẹ":
                        st.success("Vôi hóa mạch vành tình cờ mức nhẹ")
                    elif grade in ["Trung bình", "Nặng"]:
                        st.warning(f"Vôi hóa mạch vành tình cờ mức {grade.lower()}")
                    else:
                        st.info("Kết quả CT chưa ghi rõ mức độ vôi hóa; không tự suy diễn mức độ.")

        else:
            if render_sub_header("2.1 Phân nhóm", 1, "lipid_step2_sub"):
                st.warning(
                    "Dữ liệu hiện tại chưa nằm trọn trong một nhánh tự động của phiên bản này. "
                    "Không dùng PREVENT ngoài điều kiện guideline."
                )

        # -------------------------------------------------
        # TĂNG TRIGLYCERID CHẠY SONG SONG
        # -------------------------------------------------
        if d["tg_active"]:
            if render_sub_header("2.X Tăng triglycerid máu đồng thời", 4, "lipid_step2_sub"):
                if d["fasting_status"] == "Không nhịn đói":
                    st.warning(
                        f"TG không nhịn đói {d['tg']:.0f} mg/dL: đã phát hiện tăng triglycerid. "
                        "Cần lipid máu nhịn đói để xác nhận và phân tầng điều trị tăng triglycerid, "
                        "đặc biệt trước khi xếp mức 500–999 hoặc ≥1000 mg/dL."
                    )
                    step2["tg_verified_fasting"] = False
                else:
                    st.success(f"TG nhịn đói: **{d['tg']:.0f} mg/dL — {d['tg_level']}**")
                    step2["tg_verified_fasting"] = True

                    persistent = st.checkbox(
                        "Tăng triglycerid còn kéo dài sau khi đánh giá nguyên nhân thứ phát và can thiệp lối sống",
                        key="tg_persistent",
                    )
                    step2["tg_persistent"] = persistent

                    if d["tg"] >= 1000:
                        fcs = st.checkbox(
                            "Đã xác nhận hội chứng chylomicron máu gia đình (FCS)",
                            key="tg_fcs",
                        )
                        step2["fcs"] = fcs
                        st.error(
                            "🚨 TG ≥1000 mg/dL: ưu tiên ban đầu là hạ triglycerid để giảm nguy cơ viêm tụy."
                        )
                    elif d["tg"] >= 500:
                        st.warning(
                            "⚠️ TG 500–999 mg/dL: tăng nguy cơ viêm tụy; "
                            "cần xử trí nguyên nhân thứ phát và chế độ ăn chuyên biệt."
                        )
                    else:
                        st.info(
                            "TG 150–499 mg/dL: ưu tiên lối sống, nguyên nhân thứ phát và kiểm soát nguy cơ ASCVD."
                        )

        st.session_state.lipid_step2 = step2

        if st.button(
            "XÁC NHẬN PHÂN NHÓM & SANG ĐIỀU TRỊ ➡️",
            type="primary",
            use_container_width=True,
            key="lip_go_step3",
        ):
            if path == "Dự phòng tiên phát" and st.session_state.lipid_risk is None:
                st.error("Cần tính PREVENT-ASCVD trước khi sang bước điều trị.")
            else:
                st.session_state.lipid_step2 = step2
                st.session_state.lipid_step = 3
                st.session_state.lipid_open_main = 3
                st.session_state.lipid_step3_sub = 1
                st.rerun()

    else:
        d = st.session_state.lipid_initial
        st.info(f"Nhóm điều trị chính: **{d['main_path']}**")
        if st.session_state.lipid_risk:
            st.caption(
                f"PREVENT-ASCVD 10 năm: {st.session_state.lipid_risk['ascvd_10']:.1f}%"
            )
        if st.button("↩️ Sửa đánh giá nguy cơ / phân nhóm", key="lip_back_to_2"):
            st.session_state.lipid_step = 2
            st.session_state.lipid_open_main = 2
            st.rerun()


# =========================================================
# BƯỚC 3 — ĐIỀU TRỊ
# =========================================================
step3_label = (
    "🟢 BƯỚC 3: ĐIỀU TRỊ"
    if st.session_state.lipid_step == 3
    else "🔒 BƯỚC 3: ĐIỀU TRỊ"
)

if render_main_step_header("BƯỚC 3: ĐIỀU TRỊ", 3):
    if st.session_state.lipid_step < 3:
        st.info("Hoàn tất Bước 2 để mở phần điều trị.")

    else:
        d = st.session_state.lipid_initial
        if "statin_now" not in d:
            d["statin_now"] = bool(d.get("lipid_lowering_now", False))
        s2 = st.session_state.lipid_step2
        path = d["main_path"]

        st.markdown(
            f"""
<div class="path-main">
<b>🎯 NHÓM ĐIỀU TRỊ CHÍNH:</b> {path}
</div>
""",
            unsafe_allow_html=True,
        )

        # -------------------------------------------------
        # 3.1 PHÁC ĐỒ HIỆN TẠI
        # -------------------------------------------------
        if render_sub_header("3.1 Điều trị hạ lipid hiện tại", 1, "lipid_step3_sub"):
            treated, current_statin, current_nonstatin = treatment_current_regimen(
                default_on_statin=d.get("statin_now", False)
            )

            if treated:
                current_parts = [current_statin]
                if current_nonstatin:
                    current_parts += current_nonstatin
                st.info("Phác đồ hiện tại: **" + " + ".join(current_parts) + "**")
            else:
                st.info("Phác đồ hiện tại: **Chưa điều trị hạ lipid máu.**")

        # -------------------------------------------------
        # 3.2 MỤC TIÊU + KHUYẾN CÁO
        # -------------------------------------------------
        if render_sub_header("3.2 Mục tiêu và khuyến cáo điều trị", 2, "lipid_step3_sub"):
            # DỰ PHÒNG TIÊN PHÁT
            if path == "Dự phòng tiên phát":
                risk = st.session_state.lipid_risk["ascvd_10"]
                cat, icon = risk_category(risk)
                enhancers = s2.get("risk_enhancers", [])

                st.markdown(
                    f"""
<div class="target-card">
<b>{icon} PREVENT-ASCVD 10 năm: {risk:.1f}% — {cat}</b>
</div>
""",
                    unsafe_allow_html=True,
                )

                if risk < 3:
                    current_therapy_interpretation(
                        treated,
                        current_statin,
                        current_nonstatin,
                        required_intensity=None,
                        current_ldl=d["ldl"],
                        target_ldl=None,
                    )
                    st.markdown(
                        """
<div class="treat-card">
<b>Lối sống là nền tảng.</b><br>
PREVENT-ASCVD &lt;3% không tự động kích hoạt chỉ định statin chỉ dựa trên điểm nguy cơ.
</div>
""",
                        unsafe_allow_html=True,
                    )

                elif risk < 5:
                    target_ldl = 100
                    st.markdown(
                        """
<div class="target-card">
<b>Mục tiêu nếu khởi trị statin:</b><br>
• LDL-C &lt;100 mg/dL<br>
• non-HDL-C &lt;130 mg/dL
</div>
""",
                        unsafe_allow_html=True,
                    )
                    current_therapy_interpretation(
                        treated,
                        current_statin,
                        current_nonstatin,
                        required_intensity="moderate",
                        current_ldl=d["ldl"],
                        target_ldl=target_ldl,
                    )
                    preferred_statin_box("moderate")
                    st.info(
                        "Nguy cơ cận biên 3–<5%: quyết định dùng thuốc dựa trên thảo luận lợi ích–nguy cơ."
                    )

                elif risk < 10:
                    target_ldl = 100
                    st.markdown(
                        """
<div class="target-card">
<b>Mục tiêu:</b><br>
• Giảm LDL-C ≥30%<br>
• LDL-C &lt;100 mg/dL<br>
• non-HDL-C &lt;130 mg/dL
</div>
""",
                        unsafe_allow_html=True,
                    )
                    current_therapy_interpretation(
                        treated,
                        current_statin,
                        current_nonstatin,
                        required_intensity="moderate",
                        current_ldl=d["ldl"],
                        target_ldl=target_ldl,
                    )
                    preferred_statin_box("moderate")
                    st.info(
                        "Nguy cơ trung gian 5–<10%: ít nhất statin cường độ trung bình là hợp lý; "
                        "statin cường độ cao để giảm LDL-C ≥50% cũng là lựa chọn hợp lý."
                    )

                else:
                    target_ldl = 70
                    st.markdown(
                        """
<div class="target-card">
<b>Mục tiêu:</b><br>
• Giảm LDL-C ≥50%<br>
• LDL-C &lt;70 mg/dL<br>
• non-HDL-C &lt;100 mg/dL
</div>
""",
                        unsafe_allow_html=True,
                    )
                    current_therapy_interpretation(
                        treated,
                        current_statin,
                        current_nonstatin,
                        required_intensity="high",
                        current_ldl=d["ldl"],
                        target_ldl=target_ldl,
                    )
                    preferred_statin_box("high")

                    if d["ldl"] >= target_ldl:
                        st.markdown(
                            """
<div class="treat-card">
Nếu chưa đạt LDL-C &lt;70 mg/dL và non-HDL-C &lt;100 mg/dL trên statin tối đa dung nạp:
<b>cân nhắc thêm ezetimibe 10 mg/ngày.</b>
</div>
""",
                            unsafe_allow_html=True,
                        )

                if enhancers:
                    st.warning("Yếu tố làm tăng nguy cơ đã ghi nhận: " + "; ".join(enhancers))

            # TĂNG CHOLESTEROL NẶNG
            elif path == "Tăng cholesterol máu nặng":
                hefh = s2.get("hefh", False)
                additional = s2.get("additional_risk", False)

                if d["ascvd"]:
                    target_ldl = 55
                    target_text = "LDL-C <55 mg/dL • non-HDL-C <85 mg/dL"
                elif hefh or additional or d["subclinical_active"]:
                    target_ldl = 70
                    target_text = "LDL-C <70 mg/dL • non-HDL-C <100 mg/dL"
                else:
                    target_ldl = 100
                    target_text = "LDL-C <100 mg/dL • non-HDL-C <130 mg/dL"

                st.markdown(
                    f"""
<div class="target-card">
<b>Mục tiêu điều trị:</b><br>{target_text}
</div>
""",
                    unsafe_allow_html=True,
                )

                current_therapy_interpretation(
                    treated,
                    current_statin,
                    current_nonstatin,
                    required_intensity="high",
                    current_ldl=d["ldl"],
                    target_ldl=target_ldl,
                )
                preferred_statin_box("high")

                if d["ldl"] >= target_ldl:
                    st.markdown(
                        """
<div class="treat-card">
<b>Nếu chưa đạt mục tiêu trên statin tối đa dung nạp:</b><br>
có thể cần thêm ezetimibe, kháng thể đơn dòng PCSK9 và/hoặc bempedoic acid,
tùy mức LDL-C cần hạ và bối cảnh nguy cơ.
</div>
""",
                        unsafe_allow_html=True,
                    )

                if d["ldl"] >= 100:
                    st.info(
                        "Ở tăng cholesterol máu nặng với LDL-C ≥100 mg/dL dù đã dùng statin tối đa dung nạp "
                        "có hoặc không kèm ezetimibe, inclisiran là lựa chọn hợp lý để hạ LDL-C."
                    )

                if hefh:
                    st.info("HeFH: cân nhắc đánh giá gia đình/cascade screening và chuyên gia lipid khi cần.")

            # ĐÁI THÁO ĐƯỜNG
            elif path == "Đái tháo đường chưa có bệnh tim mạch do xơ vữa":
                enh = s2.get("dm_enhancers", [])

                if 40 <= d["age"] <= 75:
                    if len(enh) >= 2:
                        target_ldl = 70
                        st.markdown(
                            """
<div class="target-card">
<b>Mục tiêu khi có nhiều yếu tố nguy cơ ASCVD:</b><br>
• Giảm LDL-C ≥50%<br>
• LDL-C &lt;70 mg/dL<br>
• non-HDL-C &lt;100 mg/dL
</div>
""",
                            unsafe_allow_html=True,
                        )
                        current_therapy_interpretation(
                            treated,
                            current_statin,
                            current_nonstatin,
                            required_intensity="high",
                            current_ldl=d["ldl"],
                            target_ldl=target_ldl,
                        )
                        preferred_statin_box("high")
                    else:
                        current_therapy_interpretation(
                            treated,
                            current_statin,
                            current_nonstatin,
                            required_intensity="moderate",
                            current_ldl=d["ldl"],
                            target_ldl=None,
                        )
                        st.markdown(
                            """
<div class="target-card">
<b>Điều trị nền:</b> statin cường độ trung bình được chỉ định ở tuổi 40–75,
bất kể nguy cơ ASCVD 10 năm ước tính.
</div>
""",
                            unsafe_allow_html=True,
                        )
                        preferred_statin_box("moderate")
                else:
                    st.warning(
                        "Ngoài tuổi 40–75, phiên bản này không tự ngoại suy khuyến cáo statin nền; "
                        "cần cá thể hóa theo nhóm tuổi và bối cảnh guideline."
                    )

            # DỰ PHÒNG THỨ PHÁT
            elif path == "Dự phòng thứ phát":
                very_high = s2.get("very_high_risk", False)

                if very_high:
                    target_ldl = 55
                    st.markdown(
                        """
<div class="target-card">
<b>ASCVD nguy cơ rất cao — mục tiêu:</b><br>
• Giảm LDL-C ≥50%<br>
• LDL-C &lt;55 mg/dL<br>
• non-HDL-C &lt;85 mg/dL
</div>
""",
                        unsafe_allow_html=True,
                    )
                    current_therapy_interpretation(
                        treated,
                        current_statin,
                        current_nonstatin,
                        required_intensity="high",
                        current_ldl=d["ldl"],
                        target_ldl=target_ldl,
                    )
                    preferred_statin_box("high")

                    if d["ldl"] >= target_ldl:
                        st.markdown(
                            """
<div class="treat-card">
<b>Nếu chưa đạt mục tiêu trên statin tối đa dung nạp:</b><br>
• Thêm ezetimibe và/hoặc kháng thể đơn dòng PCSK9.<br>
• Bempedoic acid có thể được thêm tùy mức LDL-C còn cần hạ.<br>
• Inclisiran có thể hợp lý khi không dung nạp/không tiếp cận evolocumab hoặc alirocumab,
hoặc ưu tiên lịch dùng thưa hơn.
</div>
""",
                            unsafe_allow_html=True,
                        )
                else:
                    target_ldl = 70
                    st.markdown(
                        """
<div class="target-card">
<b>ASCVD chưa xếp nguy cơ rất cao:</b><br>
• Statin cường độ cao, mục tiêu giảm LDL-C ≥50%<br>
• Mục tiêu ban đầu LDL-C &lt;70 mg/dL và non-HDL-C &lt;100 mg/dL
</div>
""",
                        unsafe_allow_html=True,
                    )
                    current_therapy_interpretation(
                        treated,
                        current_statin,
                        current_nonstatin,
                        required_intensity="high",
                        current_ldl=d["ldl"],
                        target_ldl=target_ldl,
                    )
                    preferred_statin_box("high")

                    if d["ldl"] >= target_ldl:
                        st.markdown(
                            """
<div class="treat-card">
Nếu chưa đạt LDL-C &lt;70 mg/dL / non-HDL-C &lt;100 mg/dL trên statin:
có thể thêm ezetimibe, kháng thể đơn dòng PCSK9 hoặc bempedoic acid.
Guideline cũng cho phép tăng cường hơn nữa đến LDL-C &lt;55 mg/dL / non-HDL-C &lt;85 mg/dL
ở người phù hợp sau đánh giá lợi ích–nguy cơ.
</div>
""",
                            unsafe_allow_html=True,
                        )

            # XƠ VỮA DƯỚI LÂM SÀNG
            elif path == "Xơ vữa động mạch vành dưới lâm sàng":
                if not s2.get("subclinical_age_eligible", False):
                    st.warning(
                        "Không tự động đưa mục tiêu điều trị vì tuổi nằm ngoài nhóm CAC được guideline mô tả "
                        "(nam ≥40 hoặc nữ ≥45)."
                    )

                elif d["subclinical_type"] == "Có điểm CAC":
                    group = s2.get("cac_group", "")

                    if group == "CAC ≥1000":
                        target_ldl = 55
                        st.markdown(
                            """
<div class="target-card">
<b>CAC ≥1000:</b><br>
• Giảm LDL-C ≥50%<br>
• LDL-C &lt;55 mg/dL<br>
• non-HDL-C &lt;85 mg/dL
</div>
""",
                            unsafe_allow_html=True,
                        )
                        current_therapy_interpretation(
                            treated,
                            current_statin,
                            current_nonstatin,
                            required_intensity="high",
                            current_ldl=d["ldl"],
                            target_ldl=target_ldl,
                        )
                        preferred_statin_box("high")

                    elif group == "CAC 300–999":
                        target_ldl = 70
                        st.markdown(
                            """
<div class="target-card">
<b>CAC 300–999:</b><br>
• Ít nhất giảm LDL-C ≥50%<br>
• Mục tiêu ban đầu LDL-C &lt;70 mg/dL, non-HDL-C &lt;100 mg/dL<br>
• Có thể tăng cường đến LDL-C &lt;55 mg/dL, non-HDL-C &lt;85 mg/dL
</div>
""",
                            unsafe_allow_html=True,
                        )
                        current_therapy_interpretation(
                            treated,
                            current_statin,
                            current_nonstatin,
                            required_intensity="high",
                            current_ldl=d["ldl"],
                            target_ldl=target_ldl,
                        )
                        preferred_statin_box("high")

                    elif group in ["CAC 100–299", "CAC 1–99 nhưng ≥bách phân vị 75"]:
                        target_ldl = 70
                        st.markdown(
                            """
<div class="target-card">
<b>Mục tiêu:</b><br>
• LDL-C &lt;70 mg/dL<br>
• non-HDL-C &lt;100 mg/dL
</div>
""",
                            unsafe_allow_html=True,
                        )
                        current_therapy_interpretation(
                            treated,
                            current_statin,
                            current_nonstatin,
                            required_intensity="moderate",
                            current_ldl=d["ldl"],
                            target_ldl=target_ldl,
                        )
                        st.markdown(
                            '<div class="treat-card"><b>Statin là điều trị đầu tay.</b></div>',
                            unsafe_allow_html=True,
                        )

                    elif group == "CAC 1–99":
                        target_ldl = 100
                        st.markdown(
                            """
<div class="target-card">
<b>CAC 1–99 và &lt;bách phân vị 75:</b><br>
• Giảm LDL-C 30–49%<br>
• LDL-C &lt;100 mg/dL<br>
• non-HDL-C &lt;130 mg/dL
</div>
""",
                            unsafe_allow_html=True,
                        )
                        current_therapy_interpretation(
                            treated,
                            current_statin,
                            current_nonstatin,
                            required_intensity="moderate",
                            current_ldl=d["ldl"],
                            target_ldl=target_ldl,
                        )
                        preferred_statin_box("moderate")

                    elif group == "CAC = 0":
                        st.info(
                            "CAC = 0 không chứng minh có xơ vữa mạch vành dưới lâm sàng. "
                            "Quyết định statin quay lại bối cảnh dự phòng tiên phát và các ngoại lệ không được 'hạ bậc' nguy cơ."
                        )

                else:
                    grade = s2.get("incidental_grade", d.get("incidental_grade"))
                    if grade == "Nhẹ":
                        target_ldl = 100
                        st.markdown(
                            """
<div class="target-card">
<b>Vôi hóa ĐMV tình cờ mức nhẹ:</b><br>
• Statin cường độ trung bình<br>
• Giảm LDL-C 30–49%<br>
• LDL-C &lt;100 mg/dL<br>
• non-HDL-C &lt;130 mg/dL
</div>
""",
                            unsafe_allow_html=True,
                        )
                        current_therapy_interpretation(
                            treated,
                            current_statin,
                            current_nonstatin,
                            required_intensity="moderate",
                            current_ldl=d["ldl"],
                            target_ldl=target_ldl,
                        )
                        preferred_statin_box("moderate")

                    elif grade in ["Trung bình", "Nặng"]:
                        target_ldl = 70
                        st.markdown(
                            """
<div class="target-card">
<b>Vôi hóa ĐMV tình cờ mức trung bình–nặng:</b><br>
• Statin cường độ cao<br>
• Giảm LDL-C ≥50%<br>
• LDL-C &lt;70 mg/dL<br>
• non-HDL-C &lt;100 mg/dL
</div>
""",
                            unsafe_allow_html=True,
                        )
                        current_therapy_interpretation(
                            treated,
                            current_statin,
                            current_nonstatin,
                            required_intensity="high",
                            current_ldl=d["ldl"],
                            target_ldl=target_ldl,
                        )
                        preferred_statin_box("high")
                    else:
                        st.warning("CT không ghi rõ mức độ; công cụ không tự suy diễn mục tiêu điều trị.")

            else:
                st.warning("Chưa có khuyến cáo điều trị tự động cho nhóm hiện tại trong phiên bản này.")

            # CKD modifier
            if (
                40 <= d["age"] <= 75
                and d["egfr"] < 60
                and not d["ascvd"]
                and 70 <= d["ldl"] < 190
            ):
                st.warning(
                    "🩺 Ở người 40–75 tuổi có CKD giai đoạn 3 trở lên và LDL-C 70–189 mg/dL, "
                    "guideline khuyến cáo statin cường độ trung bình hoặc statin cường độ trung bình + ezetimibe."
                )

        # -------------------------------------------------
        # 3.3 TG ĐỒNG THỜI
        # -------------------------------------------------
        if d["tg_active"]:
            if render_sub_header("3.3 Xử trí tăng triglycerid đồng thời", 3, "lipid_step3_sub"):
                if d["fasting_status"] == "Không nhịn đói":
                    st.warning(
                        "Cần xét nghiệm lipid máu **nhịn đói** trước khi phân tầng và đưa khuyến cáo điều trị "
                        "cho tăng triglycerid nặng."
                    )
                else:
                    tg = d["tg"]
                    persistent = s2.get("tg_persistent", False)

                    if tg < 500:
                        st.markdown(
                            """
<div class="treat-card">
<b>TG 150–499 mg/dL:</b><br>
• Lối sống và xử trí nguyên nhân thứ phát là nền tảng.<br>
• Nếu statin có chỉ định theo nguy cơ ASCVD, statin vẫn là điều trị nền.<br>
• Khi TG tăng, non-HDL-C hoặc ApoB được ưu tiên hơn LDL-C đơn độc để hỗ trợ quyết định lâm sàng.
</div>
""",
                            unsafe_allow_html=True,
                        )
                        if 40 <= d["age"] <= 75 and not d["ascvd"] and not d["diabetes"]:
                            st.info(
                                "Ở người 40–75 tuổi không ASCVD/đái tháo đường và TG tăng kéo dài 150–499 mg/dL, "
                                "PREVENT-ASCVD được dùng để hướng dẫn thảo luận lợi ích–nguy cơ của statin."
                            )

                    elif tg < 1000:
                        st.markdown(
                            """
<div class="target-card">
<b>TG 500–999 mg/dL — tăng nguy cơ viêm tụy</b>
</div>
""",
                            unsafe_allow_html=True,
                        )
                        st.markdown(
                            """
<div class="treat-card">
• Hạn chế đường thêm, carbohydrate tinh chế và chất béo bão hòa.<br>
• Không uống rượu.<br>
• Cá thể hóa tổng lượng chất béo trong khẩu phần.<br>
• Đánh giá và xử trí nguyên nhân thứ phát.
</div>
""",
                            unsafe_allow_html=True,
                        )
                        if persistent:
                            st.success(
                                "Nếu TG vẫn 500–999 mg/dL sau can thiệp chế độ ăn: "
                                "fibrate hoặc omega-3 kê đơn là lựa chọn hợp lý để hạ TG và giảm nguy cơ viêm tụy."
                            )

                    else:
                        st.markdown(
                            """
<div class="target-card">
<b>🚨 TG ≥1000 mg/dL — ưu tiên ban đầu: giảm TG để phòng viêm tụy</b>
</div>
""",
                            unsafe_allow_html=True,
                        )
                        st.markdown(
                            """
<div class="treat-card">
• Chế độ ăn rất ít chất béo và carbohydrate tinh chế.<br>
• Loại bỏ rượu và đường thêm.<br>
• Đánh giá nguyên nhân thứ phát và nguyên nhân di truyền.<br>
• Fibrate hoặc omega-3 kê đơn là lựa chọn hợp lý khi TG vẫn tăng nặng sau can thiệp chế độ ăn.
</div>
""",
                            unsafe_allow_html=True,
                        )
                        if s2.get("fcs", False):
                            st.success(
                                "Đã xác nhận FCS: olezarsen là thuốc được guideline khuyến cáo bổ sung vào chế độ ăn "
                                "để hạ TG và giảm nguy cơ viêm tụy."
                            )

                st.caption(
                    "Fibrate/niacin không được dùng thường quy như thuốc bổ sung vào statin chỉ nhằm giảm biến cố ASCVD; "
                    "mục tiêu của fibrate/omega-3 ở tăng TG nặng chủ yếu là hạ TG và giảm nguy cơ viêm tụy."
                )

        # -------------------------------------------------
        # 3.4 LIỀU THUỐC
        # -------------------------------------------------
        if render_sub_header("3.4 Liều các thuốc hạ LDL-C thường dùng", 4, "lipid_step3_sub"):
            render_dose_table()

        # -------------------------------------------------
        # 3.5 THẬN TRỌNG
        # -------------------------------------------------
        if render_sub_header("3.5 Thận trọng và tương tác cần nhớ", 5, "lipid_step3_sub"):
            st.markdown(
                """
- Trước khi khởi trị statin, cần rà soát tương tác thuốc.
- **Gemfibrozil:** tránh phối hợp với các statin được guideline liệt kê do nguy cơ tương tác/độc tính cơ.
- **Rosuvastatin ở CKD nặng (eGFR <30 mL/phút/1,73 m²):** nồng độ thuốc có thể tăng; có thể cần giới hạn liều, ví dụ ≤10 mg/ngày.
- **Chất gắn acid mật:** có thể làm tăng triglycerid; tránh khi TG ≥300 mg/dL.
- Không cần đo CK thường quy ở người dùng statin nếu không có triệu chứng cơ nặng.
- Không cần xét nghiệm chức năng gan thường quy ở người đang dùng statin nếu không có triệu chứng gợi ý độc gan nặng.
"""
            )

        # -------------------------------------------------
        # 3.6 THEO DÕI
        # -------------------------------------------------
        if render_sub_header("3.6 Theo dõi sau khởi trị hoặc tăng cường điều trị", 6, "lipid_step3_sub"):
            st.info(
                "🔄 Đánh giá lại lipid máu sau **4–12 tuần** kể từ khi khởi trị hoặc thay đổi liều/thuốc; "
                "sau đó theo dõi định kỳ, cá thể hóa theo nguy cơ, đáp ứng và độ ổn định."
            )

        if render_sub_header("Tài liệu nền", 7, "lipid_step3_sub"):
            st.markdown(
                """
**2026 ACC/AHA/AACVPR/ABC/ACPM/ADA/AGS/APhA/ASPC/NLA/PCNA Guideline on the Management of Dyslipidemia**  
Circulation. 2026;153:e1154–e1276. DOI: **10.1161/CIR.0000000000001423**

**PREVENT equations:** Khan SS, et al. Circulation. 2024;149:430–449.  
DOI: **10.1161/CIRCULATIONAHA.123.067626**
"""
            )

        if st.button("🔄 BẮT ĐẦU LẠI", use_container_width=True, key="lip_reset"):
            for key in [
                "lipid_step",
                "lipid_initial",
                "lipid_path",
                "lipid_risk",
                "lipid_step2",
                "lipid_tx_current_status",
                "lipid_tx_current_statin",
                "lipid_tx_current_nonstatin",
            ]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
