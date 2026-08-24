# -*- coding: utf-8 -*-
"""
CDSS Rối loạn lipid máu ở người lớn — ACC/AHA 2026
Nguồn lâm sàng chính:
Blumenthal RS, et al. 2026 ACC/AHA/... Guideline on the Management of Dyslipidemia.
Circulation. 2026;153:e1154-e1276. DOI: 10.1161/CIR.0000000000001423

Thiết kế:
- 3 bước: Thông tin ban đầu -> Đánh giá nguy cơ & phân nhóm -> Điều trị
- 6 nhóm quản lý chính của guideline:
  1) Dự phòng tiên phát LDL-C 70–189 mg/dL
  2) Tăng cholesterol máu nặng LDL-C >=190 mg/dL
  3) Đái tháo đường chưa có ASCVD
  4) Bệnh tim mạch do xơ vữa đã xác định
  5) Xơ vữa động mạch vành dưới lâm sàng
  6) Tăng triglycerid máu (chạy song song)
- PREVENT-ASCVD: Base / uACR / HbA1c.
  Công cụ gọi dịch vụ PREVENT chính thức của AHA tại thời điểm chạy.
  Nếu dịch vụ không phản hồi, công cụ KHÔNG tự suy diễn hoặc tự tạo điểm nguy cơ.

Lưu ý:
- File này KHÔNG tạo sidebar; sidebar do file điều hướng trung tâm quản lý.
- Phiên bản này chưa triển khai nhánh thai kỳ/cho con bú.
"""

import json
import urllib.request
import urllib.error

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
st.markdown(
    """
<style>
    .stApp {
        background: #f8fafc;
    }

    .block-container {
        max-width: 1480px;
        padding-top: 3.0rem;
        padding-bottom: 3rem;
    }

    .lipid-title {
        font-weight: 900;
        font-size: clamp(2.0rem, 3.2vw, 3.15rem);
        line-height: 1.08;
        color: #123a5a;
        letter-spacing: -0.025em;
        margin-bottom: .25rem;
    }

    .lipid-subtitle {
        color: #5b6b78;
        font-weight: 650;
        font-size: 1.05rem;
        margin-bottom: .9rem;
    }

    .accent-line {
        height: 4px;
        border-radius: 999px;
        background: linear-gradient(90deg, #123a5a 0%, #0f766e 55%, #10b981 100%);
        margin: .3rem 0 2.0rem 0;
    }

    .step-active {
        display: inline-block;
        background: linear-gradient(90deg, #0f5f79 0%, #10b981 100%);
        color: white;
        font-weight: 900;
        font-size: 1.35rem;
        padding: .72rem 1.15rem;
        border-radius: .72rem;
        box-shadow: 0 9px 22px rgba(15, 118, 110, .20);
        margin: .35rem 0 1.15rem 0;
    }

    .step-done {
        display: inline-block;
        background: #e7f3f8;
        color: #164e63;
        border: 2px solid #7db7d1;
        font-weight: 850;
        font-size: 1.18rem;
        padding: .58rem 1rem;
        border-radius: .68rem;
        margin: .35rem 0 .75rem 0;
    }

    .step-locked {
        display: inline-block;
        background: #f1f5f9;
        color: #64748b;
        border: 1px solid #cbd5e1;
        font-weight: 800;
        font-size: 1.12rem;
        padding: .55rem 1rem;
        border-radius: .68rem;
        margin: .35rem 0 .75rem 0;
    }

    .subhead {
        display: inline-block;
        background: #edf7fb;
        color: #164e63;
        border: 2px solid #4aa3d4;
        border-left-width: 7px;
        border-radius: .55rem;
        padding: .43rem .72rem;
        font-weight: 850;
        font-size: 1.05rem;
        margin: .5rem 0 .85rem 0;
    }

    .path-main {
        border: 1px solid #99d5c2;
        border-left: 7px solid #10b981;
        border-radius: .8rem;
        padding: .9rem 1rem;
        background: #ecfdf5;
        margin: .6rem 0 .8rem 0;
    }

    .path-main b {
        color: #065f46;
    }

    .path-extra {
        border: 1px solid #f6c76d;
        border-left: 7px solid #f59e0b;
        border-radius: .8rem;
        padding: .85rem 1rem;
        background: #fffbeb;
        margin: .55rem 0;
    }

    .target-card {
        border: 1px solid #a7c7e7;
        border-radius: .85rem;
        background: #eff6ff;
        padding: 1rem 1.1rem;
        margin: .6rem 0 1rem 0;
    }

    .treat-card {
        border: 1px solid #d7e1e8;
        border-radius: .85rem;
        background: white;
        padding: 1rem 1.1rem;
        margin: .55rem 0 .8rem 0;
        box-shadow: 0 3px 12px rgba(15, 23, 42, .04);
    }

    .small-note {
        color: #64748b;
        font-size: .92rem;
    }

    @media (max-width: 800px) {
        .block-container {
            padding-top: 2rem;
        }
        .step-active {
            font-size: 1.06rem;
            width: 100%;
        }
        .step-done, .step-locked {
            font-size: 1rem;
            width: 100%;
        }
    }
</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# HÀM TIỆN ÍCH
# =========================================================
def step_banner(number, title, state):
    if state == "active":
        css = "step-active"
        prefix = "▼"
        suffix = " [ĐANG THỰC HIỆN]"
    elif state == "done":
        css = "step-done"
        prefix = "▶"
        suffix = ""
    else:
        css = "step-locked"
        prefix = "▶"
        suffix = ""
    st.markdown(
        f'<div class="{css}">{prefix} BƯỚC {number}: {title}{suffix}</div>',
        unsafe_allow_html=True,
    )


def subhead(text):
    st.markdown(f'<div class="subhead">{text}</div>', unsafe_allow_html=True)


def is_severe_hyperchol(ldl_now, untreated_known, untreated_ldl):
    if ldl_now >= 190:
        return True
    if untreated_known and untreated_ldl is not None and untreated_ldl >= 190:
        return True
    return False


def classify_tg(tg, fasting_status):
    """
    Không suy diễn tăng TG nặng từ mẫu không nhịn đói.
    - Nhịn đói: >=150 là tăng; 500–999 nặng; >=1000 rất nặng.
    - Không nhịn đói: >=175 là tăng; nếu cao, yêu cầu xét nghiệm nhịn đói để phân tầng.
    """
    if fasting_status == "Nhịn đói":
        if tg >= 1000:
            return True, "≥1000 mg/dL"
        if tg >= 500:
            return True, "500–999 mg/dL"
        if tg >= 150:
            return True, "150–499 mg/dL"
        return False, "Không tăng"
    else:
        if tg >= 175:
            return True, "Tăng trên mẫu không nhịn đói"
        return False, "Không tăng"


def main_pathway(data):
    """Chọn trục điều trị chính; các phenotype khác vẫn được giữ lại."""
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


def call_aha_prevent(
    sex,
    age,
    total_chol,
    hdl,
    sbp,
    bmi,
    egfr,
    antihypertensive,
    lipid_lowering,
    diabetes,
    smoker,
    model,
    uacr=None,
    hba1c=None,
):
    """
    Gọi dịch vụ PREVENT của American Heart Association.
    Không có fallback tự tạo điểm nguy cơ: nếu API lỗi, trả lỗi.
    """
    payload = {
        "genderType": 1 if sex == "Nữ" else 2,
        "age": float(age),
        "totalCholesterol": float(total_chol),
        "hdlCholesterol": float(hdl),
        "sbp": float(sbp),
        "bmi": float(bmi),
        "egfr": float(egfr),
        "isAntihyperTensiveMedicUsed": bool(antihypertensive),
        "isLipidLoweringMedicUsed": bool(lipid_lowering),
        "isDiabetes": bool(diabetes),
        "isSmoker": bool(smoker),
        "uacr": float(uacr) if model == "uACR" and uacr is not None else None,
        "hbA1C": float(hba1c) if model == "HbA1c" and hba1c is not None else None,
        "zipCode": None,
    }

    url = "https://professional.heart.org/aha-service/PHDSearch/PreventCalculate"
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=12) as response:
            raw = response.read().decode("utf-8")
            result = json.loads(raw)
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Dịch vụ AHA phản hồi lỗi HTTP {e.code}.") from e
    except urllib.error.URLError as e:
        raise RuntimeError("Không kết nối được dịch vụ PREVENT của AHA.") from e
    except Exception as e:
        raise RuntimeError("Không đọc được kết quả PREVENT từ AHA.") from e

    if isinstance(result, dict) and result.get("success") is False:
        msg = result.get("message") or "AHA không trả về kết quả hợp lệ."
        raise RuntimeError(str(msg))

    def extract(items, wanted_type):
        if not isinstance(items, list):
            return None
        for item in items:
            if not isinstance(item, dict):
                continue
            item_type = str(item.get("Type", item.get("type", ""))).strip().lower()
            if item_type == wanted_type.lower():
                val = item.get("RiskPercentage", item.get("riskPercentage"))
                try:
                    return float(val)
                except (TypeError, ValueError):
                    return None
        return None

    ten = result.get("tenYearRiskEstimations", []) if isinstance(result, dict) else []
    thirty = result.get("thirtyYearRiskEstimations", []) if isinstance(result, dict) else []

    asc10 = extract(ten, "ASCVD")
    asc30 = extract(thirty, "ASCVD")

    if asc10 is None:
        raise RuntimeError("AHA đã phản hồi nhưng không có PREVENT-ASCVD 10 năm.")

    return {
        "ascvd_10": asc10,
        "ascvd_30": asc30,
        "model_name": result.get("modelName", model) if isinstance(result, dict) else model,
        "raw": result,
    }


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


def nonstatin_dose_expander():
    with st.expander("📋 Liều các thuốc hạ LDL-C thường dùng"):
        st.markdown(
            """
- **Ezetimibe:** 10 mg/ngày.
- **Bempedoic acid:** 180 mg/ngày.
- **Alirocumab:** 75–150 mg tiêm dưới da mỗi 2 tuần, hoặc 300 mg mỗi 4 tuần.
- **Evolocumab:** 140 mg tiêm dưới da mỗi 2 tuần.
- **Inclisiran:** 284 mg tiêm dưới da liều đầu, liều thứ hai sau 3 tháng, sau đó mỗi 6 tháng.

**Ghi chú:** lựa chọn thuốc bổ sung phụ thuộc mức LDL-C cần hạ, nguy cơ tuyệt đối, khả năng dung nạp, khả năng tiếp cận và ưu tiên của người bệnh.
"""
        )


def followup_box():
    st.info(
        "🔄 **Đánh giá lại lipid máu:** 4–12 tuần sau khi khởi trị hoặc tăng cường điều trị; "
        "sau đó mỗi 6–12 tháng, cá thể hóa theo nguy cơ, đáp ứng và độ ổn định."
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


# =========================================================
# TIÊU ĐỀ
# =========================================================
st.markdown(
    '<div class="lipid-title">🩸 TIẾP CẬN RỐI LOẠN LIPID MÁU</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="lipid-subtitle">Hệ thống Hỗ trợ Quyết định Lâm sàng theo ACC/AHA 2026</div>',
    unsafe_allow_html=True,
)
st.markdown('<div class="accent-line"></div>', unsafe_allow_html=True)

st.caption(
    "Phạm vi hiện tại: người lớn. Phiên bản này chưa triển khai xử trí thai kỳ/cho con bú. "
    "Công cụ hỗ trợ quyết định, không thay thế đánh giá lâm sàng."
)


# =========================================================
# BƯỚC 1 — THÔNG TIN BAN ĐẦU
# =========================================================
step_banner(
    1,
    "THÔNG TIN BAN ĐẦU",
    "active" if st.session_state.lipid_step == 1 else "done",
)

if st.session_state.lipid_step == 1:
    subhead("Thông tin cần thiết để phân nhóm")

    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Tuổi:", min_value=18, max_value=120, value=55, step=1)
    with col2:
        sex = st.radio("Giới:", ["Nam", "Nữ"], horizontal=True)

    col1, col2 = st.columns(2)
    with col1:
        ldl = st.number_input(
            "LDL-C hiện tại (mg/dL):",
            min_value=0.0,
            value=120.0,
            step=1.0,
        )
    with col2:
        tg = st.number_input(
            "Triglycerid hiện tại (mg/dL):",
            min_value=0.0,
            value=140.0,
            step=1.0,
        )

    fasting_status = st.radio(
        "Mẫu triglycerid:",
        ["Nhịn đói", "Không nhịn đói"],
        horizontal=True,
    )

    untreated_status = st.radio(
        "Có biết LDL-C trước khi bắt đầu điều trị hạ lipid không?",
        ["Không rõ", "Có"],
        horizontal=True,
    )
    untreated_known = untreated_status == "Có"
    untreated_ldl = None
    if untreated_known:
        untreated_ldl = st.number_input(
            "LDL-C trước điều trị / LDL-C cao nhất trước điều trị (mg/dL):",
            min_value=0.0,
            value=float(max(ldl, 120.0)),
            step=1.0,
        )

    st.markdown("**Tình trạng bệnh:**")
    col1, col2 = st.columns(2)
    with col1:
        ascvd = st.checkbox(
            "Có bệnh tim mạch do xơ vữa đã xác định",
            help="Ví dụ: ACS, tiền sử nhồi máu cơ tim, đau thắt ngực ổn định/không ổn định, tái thông động mạch, đột quỵ/TIA, bệnh động mạch ngoại biên.",
        )
    with col2:
        diabetes = st.checkbox("Có đái tháo đường")

    col1, col2 = st.columns(2)
    with col1:
        egfr = st.number_input(
            "eGFR (mL/phút/1,73 m²):",
            min_value=0.0,
            value=90.0,
            step=1.0,
        )
    with col2:
        lipid_lowering_now = st.checkbox("Đang dùng thuốc hạ lipid")

    subclinical_type = st.selectbox(
        "Bằng chứng xơ vữa động mạch vành dưới lâm sàng:",
        [
            "Chưa có",
            "Có điểm CAC",
            "Vôi hóa động mạch vành tình cờ trên CT không chuyên tim",
        ],
    )

    cac = None
    incidental_grade = None
    if subclinical_type == "Có điểm CAC":
        cac = st.number_input(
            "Điểm CAC (Agatston):",
            min_value=0.0,
            value=0.0,
            step=1.0,
        )
    elif subclinical_type == "Vôi hóa động mạch vành tình cờ trên CT không chuyên tim":
        incidental_grade = st.selectbox(
            "Mức độ được mô tả trên kết quả CT:",
            ["Nhẹ", "Trung bình", "Nặng", "Không ghi rõ"],
        )

    if egfr < 60:
        st.warning(
            "⚠️ eGFR <60 mL/phút/1,73 m²: có tình trạng thận làm thay đổi một số khuyến cáo điều trị; "
            "công cụ sẽ giữ thông tin này khi phân nhóm."
        )

    if st.button("XÁC NHẬN & ĐÁNH GIÁ NGUY CƠ ➡️", type="primary", use_container_width=True):
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
            "lipid_lowering_now": bool(lipid_lowering_now),
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
        st.rerun()

else:
    d = st.session_state.lipid_initial
    if d:
        st.caption(
            f"Tuổi {d['age']} • {d['sex']} • LDL-C {d['ldl']:.0f} mg/dL • "
            f"TG {d['tg']:.0f} mg/dL • eGFR {d['egfr']:.0f}"
        )
    if st.button("↩️ Sửa thông tin ban đầu", key="back_to_1"):
        st.session_state.lipid_step = 1
        st.rerun()


# =========================================================
# BƯỚC 2 — ĐÁNH GIÁ NGUY CƠ VÀ PHÂN NHÓM
# =========================================================
step_banner(
    2,
    "ĐÁNH GIÁ NGUY CƠ VÀ PHÂN NHÓM",
    "active" if st.session_state.lipid_step == 2 else (
        "done" if st.session_state.lipid_step >= 3 else "locked"
    ),
)

if st.session_state.lipid_step == 2:
    d = st.session_state.lipid_initial
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

    # -----------------------------------------------------
    # 2A. DỰ PHÒNG TIÊN PHÁT — CPR
    # -----------------------------------------------------
    if path == "Dự phòng tiên phát":
        subhead("Khung đánh giá CPR: Tính nguy cơ → Cá thể hóa → Tái phân loại")

        st.markdown("### 1. Tính nguy cơ bằng PREVENT-ASCVD")

        if not (30 <= d["age"] <= 79):
            st.error("PREVENT-ASCVD 10 năm không được áp dụng ngoài tuổi 30–79 trong nhánh này.")
        else:
            model = st.radio(
                "Mô hình PREVENT:",
                ["Base", "uACR", "HbA1c"],
                horizontal=True,
            )

            col1, col2 = st.columns(2)
            with col1:
                tc = st.number_input(
                    "Cholesterol toàn phần (mg/dL):",
                    min_value=0.0,
                    value=200.0,
                    step=1.0,
                )
                hdl = st.number_input(
                    "HDL-C (mg/dL):",
                    min_value=0.0,
                    value=50.0,
                    step=1.0,
                )
                sbp = st.number_input(
                    "Huyết áp tâm thu (mmHg):",
                    min_value=0.0,
                    value=120.0,
                    step=1.0,
                )
            with col2:
                bmi = st.number_input(
                    "BMI (kg/m²):",
                    min_value=0.0,
                    value=23.0,
                    step=0.1,
                )
                antihypertensive = st.checkbox("Đang dùng thuốc hạ huyết áp")
                smoker = st.checkbox("Đang hút thuốc")

            uacr = None
            hba1c = None
            if model == "uACR":
                uacr = st.number_input(
                    "uACR (mg/g):",
                    min_value=0.0,
                    value=10.0,
                    step=1.0,
                )
            elif model == "HbA1c":
                hba1c = st.number_input(
                    "HbA1c (%):",
                    min_value=0.0,
                    value=5.5,
                    step=0.1,
                )

            if st.button("🧮 TÍNH PREVENT-ASCVD", use_container_width=True):
                try:
                    result = call_aha_prevent(
                        sex=d["sex"],
                        age=d["age"],
                        total_chol=tc,
                        hdl=hdl,
                        sbp=sbp,
                        bmi=bmi,
                        egfr=d["egfr"],
                        antihypertensive=antihypertensive,
                        lipid_lowering=d["lipid_lowering_now"],
                        diabetes=d["diabetes"],
                        smoker=smoker,
                        model=model,
                        uacr=uacr,
                        hba1c=hba1c,
                    )
                    st.session_state.lipid_risk = result
                except RuntimeError as e:
                    st.session_state.lipid_risk = None
                    st.error(
                        f"Không tính được PREVENT-ASCVD: {e} "
                        "Công cụ không tự tạo điểm nguy cơ thay thế."
                    )

            risk_result = st.session_state.lipid_risk
            if risk_result:
                risk10 = risk_result["ascvd_10"]
                cat, icon = risk_category(risk10)
                c1, c2 = st.columns(2)
                with c1:
                    st.metric("PREVENT-ASCVD 10 năm", f"{risk10:.1f}%")
                with c2:
                    st.metric("Phân tầng", f"{icon} {cat}")
                if risk_result.get("ascvd_30") is not None and d["age"] <= 59:
                    st.caption(f"Nguy cơ ASCVD 30 năm: {risk_result['ascvd_30']:.1f}%")
                st.caption(f"Mô hình AHA trả về: {risk_result.get('model_name', model)}")
                step2["prevent_risk"] = float(risk10)
                step2["prevent_category"] = cat
                step2["prevent_model"] = model
            else:
                step2["prevent_risk"] = None

            st.info(
                "PREVENT được dùng để hỗ trợ quyết định ở người 30–79 tuổi chưa có ASCVD hoặc "
                "xơ vữa dưới lâm sàng, LDL-C 70–189 mg/dL. Điểm nguy cơ không thay thế thảo luận lợi ích–nguy cơ."
            )

        st.markdown("### 2. Cá thể hóa bằng các yếu tố làm tăng nguy cơ")
        enhancers = []

        fam = st.checkbox(
            "Tiền sử ASCVD sớm ở cha/mẹ hoặc anh/chị/em ruột "
            "(nam <55 tuổi; nữ <65 tuổi)"
        )
        ancestry = st.checkbox("Nguồn gốc có nguy cơ cao (ví dụ Nam Á, Philippines)")
        polygenic = st.checkbox("Nguy cơ đa gen cao (nếu đã được đo)")
        inflammatory = st.checkbox(
            "Bệnh viêm mạn (ví dụ lupus, viêm khớp dạng thấp, vảy nến nặng, viêm khớp viêm)"
        )
        lpa_high = st.checkbox("Lp(a) ≥125 nmol/L hoặc ≥50 mg/dL")
        hscrp_high = st.checkbox("hsCRP ≥2 mg/L trên hơn 1 lần đo, không có nguyên nhân giải thích")
        ckms = st.checkbox("Có hội chứng tim mạch–thận–chuyển hóa (CKM)")
        nonhdl_apob = st.checkbox("non-HDL-C 190–219 mg/dL hoặc ApoB ≥120 mg/dL")

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
                "hsCRP ≥2 mg/L trên 2 lần liên tiếp, không có nguyên nhân khác: guideline cho phép "
                "cân nhắc statin cường độ cao ở người nguy cơ cận biên."
            )

        st.markdown("### 3. Tái phân loại bằng CAC khi cần")
        if d["subclinical_type"] == "Chưa có":
            consider_cac = st.checkbox(
                "Quyết định điều trị vẫn chưa chắc chắn và muốn cân nhắc CAC để tái phân loại"
            )
            step2["consider_cac"] = consider_cac
            if consider_cac:
                st.info(
                    "CAC có thể hỗ trợ tái phân loại ở nam ≥40 tuổi hoặc nữ ≥45 tuổi khi quyết định "
                    "khởi trị thuốc hạ lipid còn chưa chắc chắn."
                )
        else:
            step2["consider_cac"] = False
            st.info("Bệnh nhân đã có dữ liệu xơ vữa mạch vành; không cần yêu cầu CAC như một bước tái phân loại mới.")

    # -----------------------------------------------------
    # 2B. TĂNG CHOLESTEROL MÁU NẶNG
    # -----------------------------------------------------
    elif path == "Tăng cholesterol máu nặng":
        subhead("Tăng cholesterol máu nặng")

        st.success(
            "LDL-C hiện tại hoặc LDL-C trước điều trị ≥190 mg/dL → không dùng PREVENT để quyết định có điều trị hay không."
        )

        hefh = st.checkbox("Đã xác nhận HeFH bằng lâm sàng hoặc di truyền")
        additional_risk = st.checkbox("Có thêm yếu tố nguy cơ ASCVD đã được xác định")
        secondary_causes_reviewed = st.checkbox("Đã đánh giá nguyên nhân thứ phát của tăng LDL-C")

        step2["hefh"] = hefh
        step2["additional_risk"] = additional_risk
        step2["secondary_causes_reviewed"] = secondary_causes_reviewed

        if not secondary_causes_reviewed and not d["ascvd"]:
            st.warning(
                "Cần đánh giá và xử trí nguyên nhân thứ phát của tăng LDL-C khi phù hợp."
            )

        if hefh:
            st.info(
                "HeFH là nhóm nguy cơ cao; không dùng công cụ nguy cơ chuẩn của dân số chung để 'hạ bậc' nguy cơ."
            )

    # -----------------------------------------------------
    # 2C. ĐÁI THÁO ĐƯỜNG
    # -----------------------------------------------------
    elif path == "Đái tháo đường chưa có bệnh tim mạch do xơ vữa":
        subhead("Đái tháo đường chưa có bệnh tim mạch do xơ vữa")

        dm_type = st.radio("Loại đái tháo đường:", ["Típ 2", "Típ 1"], horizontal=True)
        duration = st.number_input(
            "Thời gian mắc đái tháo đường (năm):",
            min_value=0.0,
            value=5.0,
            step=1.0,
        )
        albuminuria = st.checkbox("Albumin niệu ≥30 μg/mg creatinin")
        retinopathy = st.checkbox("Có bệnh võng mạc do đái tháo đường")
        neuropathy = st.checkbox("Có bệnh thần kinh do đái tháo đường")
        abi_low = st.checkbox("ABI <0,9")

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
            st.warning("Yếu tố làm tăng nguy cơ riêng của đái tháo đường: " + "; ".join(dm_enhancers))

    # -----------------------------------------------------
    # 2D. DỰ PHÒNG THỨ PHÁT
    # -----------------------------------------------------
    elif path == "Dự phòng thứ phát":
        subhead("Bệnh tim mạch do xơ vữa đã xác định — dự phòng thứ phát")

        st.markdown("**Biến cố ASCVD chính:**")
        major1 = st.checkbox("ACS trong 12 tháng qua")
        major2 = st.checkbox("Tiền sử nhồi máu cơ tim khác với ACS trong 12 tháng qua")
        major3 = st.checkbox("Tiền sử đột quỵ thiếu máu não")
        major4 = st.checkbox("Bệnh động mạch ngoại biên có triệu chứng")
        major_count = sum([major1, major2, major3, major4])

        st.markdown("**Đặc điểm nguy cơ cao:**")
        high_risk_features = []
        if d["age"] >= 65:
            high_risk_features.append("Tuổi ≥65")
            st.caption("✓ Tuổi ≥65")
        revasc = st.checkbox("Đã CABG hoặc PCI")
        smoker = st.checkbox("Đang hút thuốc")
        hf = st.checkbox("Tiền sử suy tim")
        hypertension = st.checkbox("Tăng huyết áp")
        ldl100_on_combo = st.checkbox(
            "LDL-C ≥100 mg/dL dù đã dùng statin tối đa dung nạp + ezetimibe"
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

        very_high = (major_count >= 2) or (major_count >= 1 and len(high_risk_features) >= 2)

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

    # -----------------------------------------------------
    # 2E. XƠ VỮA ĐMV DƯỚI LÂM SÀNG
    # -----------------------------------------------------
    elif path == "Xơ vữa động mạch vành dưới lâm sàng":
        subhead("Xơ vữa động mạch vành dưới lâm sàng")

        age_eligible = (d["sex"] == "Nam" and d["age"] >= 40) or (d["sex"] == "Nữ" and d["age"] >= 45)
        step2["subclinical_age_eligible"] = age_eligible

        if not age_eligible:
            st.warning(
                "Nhánh khuyến cáo CAC của guideline áp dụng cho nam ≥40 tuổi hoặc nữ ≥45 tuổi. "
                "Công cụ không tự ngoại suy mục tiêu điều trị cho tuổi thấp hơn."
            )

        if d["subclinical_type"] == "Có điểm CAC":
            cac = d["cac"] or 0
            percentile_known = False
            percentile = None
            if 1 <= cac <= 99:
                percentile_known = st.checkbox("Có biết bách phân vị CAC")
                if percentile_known:
                    percentile = st.number_input(
                        "Bách phân vị CAC (%):",
                        min_value=0.0,
                        max_value=100.0,
                        value=50.0,
                        step=1.0,
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

    # -----------------------------------------------------
    # Không đủ branch
    # -----------------------------------------------------
    else:
        st.warning(
            "Dữ liệu hiện tại chưa nằm trọn trong một nhánh tự động của phiên bản này. "
            "Không dùng PREVENT ngoài điều kiện guideline."
        )

    # -----------------------------------------------------
    # 2F. TĂNG TRIGLYCERID — CHẠY SONG SONG
    # -----------------------------------------------------
    if d["tg_active"]:
        st.divider()
        subhead("Nhóm đồng thời: Tăng triglycerid máu")

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
                "Tăng triglycerid còn kéo dài sau khi đánh giá nguyên nhân thứ phát và can thiệp lối sống"
            )
            step2["tg_persistent"] = persistent

            if d["tg"] >= 1000:
                fcs = st.checkbox("Đã xác nhận hội chứng chylomicron máu gia đình (FCS)")
                step2["fcs"] = fcs
                st.error(
                    "🚨 TG ≥1000 mg/dL: ưu tiên ban đầu là hạ triglycerid để giảm nguy cơ viêm tụy."
                )
            elif d["tg"] >= 500:
                st.warning(
                    "⚠️ TG 500–999 mg/dL: tăng nguy cơ viêm tụy; cần xử trí nguyên nhân thứ phát và chế độ ăn chuyên biệt."
                )
            else:
                st.info(
                    "TG 150–499 mg/dL: ưu tiên lối sống, nguyên nhân thứ phát và kiểm soát nguy cơ ASCVD."
                )

    st.session_state.lipid_step2 = step2

    if st.button("XÁC NHẬN PHÂN NHÓM & SANG ĐIỀU TRỊ ➡️", type="primary", use_container_width=True):
        # Với nhánh PREVENT, nếu chưa tính điểm thì không cho sang điều trị tự động.
        if path == "Dự phòng tiên phát" and st.session_state.lipid_risk is None:
            st.error("Cần tính PREVENT-ASCVD trước khi sang bước điều trị.")
        else:
            st.session_state.lipid_step2 = step2
            st.session_state.lipid_step = 3
            st.rerun()

elif st.session_state.lipid_step >= 3:
    d = st.session_state.lipid_initial
    st.caption(f"Nhóm điều trị chính: {d['main_path']}")
    if st.button("↩️ Sửa đánh giá nguy cơ / phân nhóm", key="back_to_2"):
        st.session_state.lipid_step = 2
        st.rerun()


# =========================================================
# BƯỚC 3 — ĐIỀU TRỊ
# =========================================================
step_banner(
    3,
    "ĐIỀU TRỊ",
    "active" if st.session_state.lipid_step == 3 else "locked",
)

if st.session_state.lipid_step == 3:
    d = st.session_state.lipid_initial
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

    # -----------------------------------------------------
    # DỰ PHÒNG TIÊN PHÁT
    # -----------------------------------------------------
    if path == "Dự phòng tiên phát":
        risk = st.session_state.lipid_risk["ascvd_10"]
        cat, icon = risk_category(risk)

        st.markdown(
            f"""
<div class="target-card">
<b>{icon} PREVENT-ASCVD 10 năm: {risk:.1f}% — {cat}</b>
</div>
""",
            unsafe_allow_html=True,
        )

        enhancers = s2.get("risk_enhancers", [])

        if risk < 3:
            st.markdown("### Khuyến cáo hiện tại")
            st.markdown(
                """
<div class="treat-card">
<b>Lối sống là nền tảng.</b><br>
PREVENT-ASCVD <3% không tự động kích hoạt chỉ định statin chỉ dựa trên điểm nguy cơ.
Các yếu tố làm tăng nguy cơ có thể được đưa vào thảo luận lợi ích–nguy cơ.
</div>
""",
                unsafe_allow_html=True,
            )
            if enhancers:
                st.warning("Có yếu tố làm tăng nguy cơ: " + "; ".join(enhancers))

        elif risk < 5:
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
            st.markdown("### Điều trị")
            preferred_statin_box("moderate")
            st.info(
                "Nguy cơ cận biên 3–<5%: quyết định dùng thuốc dựa trên thảo luận lợi ích–nguy cơ; "
                "các yếu tố làm tăng nguy cơ có thể củng cố quyết định khởi trị hoặc tăng cường điều trị."
            )
            if "hsCRP tăng" in enhancers:
                st.warning(
                    "hsCRP ≥2 mg/L trên 2 lần liên tiếp, không có nguyên nhân khác: statin cường độ cao có thể hữu ích."
                )

        elif risk < 10:
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
            st.markdown("### Điều trị")
            preferred_statin_box("moderate")
            st.info(
                "Nguy cơ trung gian 5–<10%: ít nhất statin cường độ trung bình là hợp lý; "
                "statin cường độ cao để giảm LDL-C ≥50% cũng là lựa chọn hợp lý."
            )

        else:
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
            st.markdown("### Điều trị")
            preferred_statin_box("high")
            st.markdown(
                """
<div class="treat-card">
Nếu chưa đạt LDL-C &lt;70 mg/dL và non-HDL-C &lt;100 mg/dL trên statin tối đa dung nạp:
<b>cân nhắc thêm ezetimibe 10 mg/ngày.</b>
</div>
""",
                unsafe_allow_html=True,
            )

    # -----------------------------------------------------
    # TĂNG CHOLESTEROL MÁU NẶNG
    # -----------------------------------------------------
    elif path == "Tăng cholesterol máu nặng":
        hefh = s2.get("hefh", False)
        additional = s2.get("additional_risk", False)

        if d["ascvd"]:
            target = "LDL-C <55 mg/dL • non-HDL-C <85 mg/dL"
        elif hefh or additional or d["subclinical_active"]:
            target = "LDL-C <70 mg/dL • non-HDL-C <100 mg/dL"
        else:
            target = "LDL-C <100 mg/dL • non-HDL-C <130 mg/dL"

        st.markdown(
            f"""
<div class="target-card">
<b>Mục tiêu điều trị:</b><br>{target}
</div>
""",
            unsafe_allow_html=True,
        )
        st.markdown("### Điều trị")
        preferred_statin_box("high")
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

    # -----------------------------------------------------
    # ĐÁI THÁO ĐƯỜNG
    # -----------------------------------------------------
    elif path == "Đái tháo đường chưa có bệnh tim mạch do xơ vữa":
        enh = s2.get("dm_enhancers", [])

        if 40 <= d["age"] <= 75:
            if len(enh) >= 2:
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
                preferred_statin_box("high")
                st.info(
                    "Ở người 40–75 tuổi có đái tháo đường và nhiều yếu tố nguy cơ ASCVD, "
                    "statin cường độ cao là hợp lý."
                )
            else:
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
                if enh:
                    st.info(
                        "Có yếu tố làm tăng nguy cơ riêng của đái tháo đường; "
                        "có thể cân nhắc tăng cường cường độ điều trị theo bối cảnh."
                    )
        else:
            st.warning(
                "Ngoài tuổi 40–75, phiên bản này không tự ngoại suy khuyến cáo statin nền; "
                "cần cá thể hóa theo nhóm tuổi và bối cảnh guideline."
            )

    # -----------------------------------------------------
    # DỰ PHÒNG THỨ PHÁT
    # -----------------------------------------------------
    elif path == "Dự phòng thứ phát":
        very_high = s2.get("very_high_risk", False)

        if very_high:
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
            preferred_statin_box("high")
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
            preferred_statin_box("high")
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

    # -----------------------------------------------------
    # XƠ VỮA ĐMV DƯỚI LÂM SÀNG
    # -----------------------------------------------------
    elif path == "Xơ vữa động mạch vành dưới lâm sàng":
        if not s2.get("subclinical_age_eligible", False):
            st.warning(
                "Không tự động đưa mục tiêu điều trị vì tuổi nằm ngoài nhóm CAC được guideline mô tả "
                "(nam ≥40 hoặc nữ ≥45)."
            )
        elif d["subclinical_type"] == "Có điểm CAC":
            group = s2.get("cac_group", "")

            if group == "CAC ≥1000":
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
                preferred_statin_box("high")

            elif group == "CAC 300–999":
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
                preferred_statin_box("high")
                st.info(
                    "Nếu cần, có thể tăng cường bằng ezetimibe, kháng thể đơn dòng PCSK9 hoặc bempedoic acid."
                )

            elif group in ["CAC 100–299", "CAC 1–99 nhưng ≥bách phân vị 75"]:
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
                st.markdown(
                    '<div class="treat-card"><b>Statin là điều trị đầu tay.</b></div>',
                    unsafe_allow_html=True,
                )

            elif group == "CAC 1–99":
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
                preferred_statin_box("moderate")

            elif group == "CAC = 0":
                st.info(
                    "CAC = 0 không chứng minh có xơ vữa mạch vành dưới lâm sàng. "
                    "Quyết định statin quay lại bối cảnh dự phòng tiên phát và các ngoại lệ không được 'hạ bậc' nguy cơ."
                )

        else:
            grade = s2.get("incidental_grade", d.get("incidental_grade"))
            if grade == "Nhẹ":
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
                preferred_statin_box("moderate")
            elif grade in ["Trung bình", "Nặng"]:
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
                preferred_statin_box("high")
            else:
                st.warning(
                    "CT không ghi rõ mức độ; công cụ không tự suy diễn mục tiêu điều trị."
                )

    else:
        st.warning(
            "Chưa có khuyến cáo điều trị tự động cho nhóm hiện tại trong phiên bản này."
        )

    # -----------------------------------------------------
    # CKD MODIFIER
    # -----------------------------------------------------
    if 40 <= d["age"] <= 75 and d["egfr"] < 60 and not d["ascvd"] and 70 <= d["ldl"] < 190:
        st.divider()
        st.warning(
            "🩺 **Tình trạng thận:** Ở người 40–75 tuổi có CKD giai đoạn 3 trở lên và LDL-C 70–189 mg/dL, "
            "guideline khuyến cáo statin cường độ trung bình hoặc statin cường độ trung bình + ezetimibe "
            "để giảm nguy cơ ASCVD."
        )

    # -----------------------------------------------------
    # HYPERTRIGLYCERID CHẠY SONG SONG
    # -----------------------------------------------------
    if d["tg_active"]:
        st.divider()
        st.markdown("## 🔶 Xử trí tăng triglycerid đồng thời")

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

    # -----------------------------------------------------
    # THÔNG TIN THUỐC / AN TOÀN / THEO DÕI
    # -----------------------------------------------------
    st.divider()
    nonstatin_dose_expander()

    with st.expander("⚠️ Thận trọng và tương tác cần nhớ"):
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

    followup_box()

    with st.expander("📚 Cơ sở hướng dẫn"):
        st.markdown(
            """
**2026 ACC/AHA/AACVPR/ABC/ACPM/ADA/AGS/APhA/ASPC/NLA/PCNA Guideline on the Management of Dyslipidemia**

Circulation. 2026;153:e1154–e1276.  
DOI: **10.1161/CIR.0000000000001423**

Công cụ hiện tập trung vào 6 nhóm quản lý chính của guideline và các quyết định cốt lõi đã được xây dựng trong phiên bản này.
"""
        )

    if st.button("🔄 BẮT ĐẦU LẠI", use_container_width=True):
        for key in ["lipid_step", "lipid_initial", "lipid_path", "lipid_risk", "lipid_step2"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
