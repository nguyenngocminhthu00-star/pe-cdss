import streamlit as st

st.set_page_config(
    page_title="Hội chứng vành mạn",
    page_icon="❤️",
    layout="wide"
)

st.title("❤️ HỘI CHỨNG VÀNH MẠN")
st.write("Công cụ hỗ trợ tiếp cận Hội chứng vành mạn – ESC 2024")

import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="ESC 2024 CCS Initial Management Tool",
    page_icon="🫀",
    layout="wide"
)

# Custom Styling
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6;
    }
    .main-title {
        color: #1e3d59;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        text-align: center;
        padding: 10px;
        font-weight: bold;
    }
    .step-header {
        color: #17b978;
        font-weight: bold;
        font-size: 1.2rem;
        border-bottom: 2px solid #17b978;
        padding-bottom: 5px;
        margin-top: 15px;
        margin-bottom: 15px;
    }
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
    .info-box {
        background-color: #f7f9fa;
        border: 1px solid #d3d3d3;
        padding: 12px;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🫀 QUẢN LÝ BAN ĐẦU NGHI NGỜ HỘI CHỨNG MẠCH VÀNH MẠN (CCS)</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555;'>Ứng dụng lâm sàng tương tác từng bước (Stepwise Approach) theo Hướng dẫn ESC 2024</p>", unsafe_allow_html=True)
st.divider()

# Session State Initialization for Step Flow (Option A: Dynamic Expansion)
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'acute_flag' not in st.session_state:
    st.session_state.acute_flag = False

# Progress Bar
step_cols = st.columns(4)
steps_labels = ["1. Đánh giá ban đầu", "2. Đánh giá chuyên sâu & RF-CL", "3. Chẩn đoán xác định", "4. Điều trị nội & Can thiệp"]
for idx, col in enumerate(step_cols):
    step_num = idx + 1
    if st.session_state.step >= step_num:
        col.markdown(f"<div style='text-align: center; color: #17b978; font-weight: bold;'>🟢 {steps_labels[idx]}</div>", unsafe_allow_html=True)
    else:
        col.markdown(f"<div style='text-align: center; color: #888;'>⚪ {steps_labels[idx]}</div>", unsafe_allow_html=True)

st.divider()

# Helper function to transition steps
def set_step(step_num):
    st.session_state.step = step_num
    st.rerun()

# ----------------------------------------------------
# STEP 1: GENERAL CLINICAL EVALUATION
# ----------------------------------------------------
step1_expanded = (st.session_state.step == 1)
with st.expander("🩺 BƯỚC 1: ĐÁNH GIÁ LÂM SÀNG BAN ĐẦU (Initial Evaluation)", expanded=step1_expanded):
    st.markdown("<div class='step-header'>BƯỚC 1: Khám lâm sàng, loại trừ ACS và thực hiện thăm dò cơ bản</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("1. Triệu chứng lâm sàng cấp tính / Cảnh báo đỏ")
        acute_symptoms = st.checkbox("Đau ngực mới xuất hiện, tăng dần tần suất hoặc cường độ (Crescendo angina)")
        unstable_symptoms = st.checkbox("Triệu chứng không ổn định (đau ngực khi nghỉ, suy tim cấp, hoặc loạn nhịp tim mới xuất hiện)")
        resting_ecg_acute = st.checkbox("ECG lúc nghỉ có thay đổi cấp tính (ST chênh lên/chênh xuống, sóng T âm sâu đối xứng)")

    with col2:
        st.subheader("2. Khám lâm sàng cơ bản & Cận lâm sàng thường quy")
        bp_sys = st.number_input("Huyết áp tâm thu (mmHg)", min_value=70, max_value=250, value=120)
        heart_rate = st.number_input("Tần số tim (nhịp/phút)", min_value=30, max_value=200, value=75)
        comorbidities = st.multiselect("Bệnh đồng mắc kèm theo", [
            "Bệnh thận mạn (eGFR < 60 mL/min/1.73 m2)",
            "Bệnh động mạch ngoại biên (PAD)",
            "Đái tháo đường",
            "Bệnh phổi tắc nghẽn mạn tính (COPD)",
            "Rối loạn chức năng tuyến giáp"
        ])
    
    # Check for acute coronary syndrome (ACS) warning
    if acute_symptoms or unstable_symptoms or resting_ecg_acute:
        st.session_state.acute_flag = True
        st.markdown("""
        <div class='warning-box'>
            <h3 style='color: #ff4d4d; margin-top: 0;'>🔴 CẢNH BÁO: NGHI NGỜ HỘI CHỨNG MẠCH VÀNH CẤP (ACS)!</h3>
            <p>Bệnh nhân có triệu chứng hoặc điện tâm đồ gợi ý mạch vành cấp mất ổn định. <strong>Khuyến cáo chuyển ngay bệnh nhân đến Khoa Cấp cứu (Emergency Department)</strong> để làm Troponin nhạy cảm cao (hs-cTn) và xử trí theo phác đồ ACS 2023.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.session_state.acute_flag = False
        st.markdown("""
        <div class='recommendation-box'>
            <strong>Khuyến cáo cận lâm sàng cơ bản cho tất cả bệnh nhân nghi ngờ CCS (Class I):</strong><br>
            - Điện tâm đồ 12 chuyển đạo lúc nghỉ.<br>
            - Xét nghiệm máu: Công thức máu, Lipid máu (LDL-C), Đường huyết (HbA1c), Chức năng thận (eGFR), Chức năng tuyến giáp (ít nhất 1 lần).<br>
            - Siêu âm tim lúc nghỉ (thực hiện ở Bước 2).
        </div>
        """, unsafe_allow_html=True)

    # Next step button
    if st.session_state.acute_flag:
        st.button("Bị khóa do cảnh báo đỏ (ACS)", disabled=True)
    else:
        if st.button("Xác nhận & Sang Bước 2 ➡️"):
            set_step(2)

# ----------------------------------------------------
# STEP 2: FURTHER CARDIAC EVALUATION & RF-CL CALCULATOR
# ----------------------------------------------------
step2_expanded = (st.session_state.step == 2)
with st.expander("📊 BƯỚC 2: ĐÁNH GIÁ CHUYÊN SÂU & ƯỚC TÍNH KHẢ NĂNG LÂM SÀNG (RF-CL)", expanded=step2_expanded):
    if st.session_state.step < 2:
        st.warning("Vui lòng hoàn thành Bước 1 trước.")
    else:
        st.markdown("<div class='step-header'>BƯỚC 2: Khảo sát tim mạch sâu hơn & Tính toán Khả năng lâm sàng tắc nghẽn (RF-CL)</div>", unsafe_allow_html=True)
        
        # Section A: Resting Echocardiography
        st.subheader("1. Siêu âm tim qua thành ngực lúc nghỉ (Resting TTE) - Khuyến cáo Class I")
        echo_col1, echo_col2 = st.columns(2)
        with echo_col1:
            lvef = st.slider("Phân suất tống máu thất trái (LVEF %)", min_value=10, max_value=80, value=55)
        with echo_col2:
            echo_findings = st.multiselect("Phát hiện bất thường trên siêu âm tim", [
                "Rối loạn vận động vùng cơ tim thất trái (Regional wall motion abnormality)",
                "Bệnh van tim kèm theo (Hẹp/hở van mức độ vừa-nặng)",
                "Phì đại thất trái (LV Hypertrophy)",
                "Rối loạn chức năng tâm trương thất trái"
            ])
            
        if lvef <= 40:
            st.error("⚠️ Giảm chức năng tâm thu thất trái nặng (LVEF ≤ 40%). Cần điều trị suy tim theo khuyến cáo GDMT và xem xét chụp mạch vành sớm.")
        elif 41 <= lvef <= 49:
            st.warning("⚠️ Chức năng tâm thu thất trái giảm nhẹ (LVEF 41-49%).")

        st.divider()

        # Section B: RF-CL Calculator
        st.subheader("2. Bộ tính điểm Khả năng lâm sàng mạch vành tắc nghẽn (RF-CL Model - ESC 2024)")
        st.info("Mô hình RF-CL (Winther et al.) tích hợp: Tuổi, Giới tính, Đặc điểm triệu chứng và số lượng Yếu tố nguy cơ động mạch vành.")
        
        calc_col1, calc_col2 = st.columns(2)
        with calc_col1:
            gender = st.radio("Giới tính sinh học", ["Nữ (Women)", "Nam (Men)"])
            age_group = st.selectbox("Nhóm tuổi", ["30-39", "40-49", "50-59", "60-69", "70-80"])
            
            symptom_type = st.radio("Triệu chứng chính của bệnh nhân", ["Cơn đau thắt ngực (Chest Pain)", "Khó thở khi gắng sức (Exertional Dyspnoea)"])
            
            symptom_score = 0
            if symptom_type == "Cơn đau thắt ngực (Chest Pain)":
                st.markdown("<p style='font-size: 0.9rem; font-weight: bold;'>Đánh giá tính chất cơn đau thắt ngực (Mỗi tính chất đạt 1 điểm):</p>", unsafe_allow_html=True)
                c1 = st.checkbox("1. Đau thắt, đè ép vùng sau xương ức, cổ, hàm, vai hoặc cánh tay")
                c2 = st.checkbox("2. Khởi phát khi gắng sức thể lực hoặc căng thẳng tâm lý")
                c3 = st.checkbox("3. Giảm khi nghỉ ngơi hoặc dùng Nitrates dưới 5 phút")
                symptom_score = int(c1) + int(c2) + int(c3)
                st.write(f"👉 Điểm triệu chứng đau ngực: **{symptom_score}/3 điểm**")
            else:
                symptom_score = 2
                st.write("👉 Điểm triệu chứng khó thở khi gắng sức được tự động quy đổi thành **2 điểm** theo ESC 2024.")

        with calc_col2:
            st.markdown("<p style='font-size: 0.9rem; font-weight: bold;'>Các yếu tố nguy cơ tim mạch đi kèm (0-5):</p>", unsafe_allow_html=True)
            rf_family = st.checkbox("Tiền sử gia đình mắc bệnh mạch vành sớm (Nam <55, Nữ <65)")
            rf_smoking = st.checkbox("Đang hút thuốc lá hoặc có tiền sử hút thuốc")
            rf_dyslipidemia = st.checkbox("Rối loạn lipid máu")
            rf_hypertension = st.checkbox("Tăng huyết áp")
            rf_diabetes = st.checkbox("Đái tháo đường")
            
            rf_count = int(rf_family) + int(rf_smoking) + int(rf_dyslipidemia) + int(rf_hypertension) + int(rf_diabetes)
            
            if rf_count <= 1:
                rf_category = "0-1"
            elif rf_count <= 3:
                rf_category = "2-3"
            else:
                rf_category = "4-5"
                
            st.write(f"👉 Số lượng yếu tố nguy cơ mạch vành: **{rf_count}/5** (Nhóm nguy cơ: {rf_category})")

        # RF-CL Matrix Lookup
        # Structure: rf_cl_matrix[gender][age_group][symptom_score_str][rf_category]
        rf_cl_matrix = {
            "Nữ (Women)": {
                "30-39": {"0-1": {"0-1": 0, "2-3": 1, "4-5": 2}, "2": {"0-1": 0, "2-3": 1, "4-5": 3}, "3": {"0-1": 2, "2-3": 5, "4-5": 10}},
                "40-49": {"0-1": {"0-1": 1, "2-3": 1, "4-5": 3}, "2": {"0-1": 1, "2-3": 2, "4-5": 5}, "3": {"0-1": 4, "2-3": 7, "4-5": 12}},
                "50-59": {"0-1": {"0-1": 1, "2-3": 2, "4-5": 5}, "2": {"0-1": 2, "2-3": 3, "4-5": 7}, "3": {"0-1": 6, "2-3": 10, "4-5": 15}},
                "60-69": {"0-1": {"0-1": 2, "2-3": 4, "4-5": 7}, "2": {"0-1": 3, "2-3": 6, "4-5": 11}, "3": {"0-1": 10, "2-3": 14, "4-5": 19}},
                "70-80": {"0-1": {"0-1": 4, "2-3": 7, "4-5": 11}, "2": {"0-1": 6, "2-3": 10, "4-5": 16}, "3": {"0-1": 16, "2-3": 19, "4-5": 23}}
            },
            "Nam (Men)": {
                "30-39": {"0-1": {"0-1": 1, "2-3": 2, "4-5": 5}, "2": {"0-1": 2, "2-3": 4, "4-5": 8}, "3": {"0-1": 9, "2-3": 14, "4-5": 22}},
                "40-49": {"0-1": {"0-1": 2, "2-3": 4, "4-5": 7}, "2": {"0-1": 3, "2-3": 6, "4-5": 12}, "3": {"0-1": 14, "2-3": 20, "4-5": 27}},
                "50-59": {"0-1": {"0-1": 4, "2-3": 7, "4-5": 12}, "2": {"0-1": 6, "2-3": 11, "4-5": 17}, "3": {"0-1": 21, "2-3": 27, "4-5": 33}},
                "60-69": {"0-1": {"0-1": 8, "2-3": 12, "4-5": 17}, "2": {"0-1": 12, "2-3": 17, "4-5": 25}, "3": {"0-1": 32, "2-3": 35, "4-5": 39}},
                "70-80": {"0-1": {"0-1": 15, "2-3": 19, "4-5": 24}, "2": {"0-1": 22, "2-3": 27, "4-5": 34}, "3": {"0-1": 44, "2-3": 44, "4-5": 45}}
            }
        }

        # Convert score to lookup key string: "0-1" if score <= 1 else str(score)
        score_key = "0-1" if symptom_score <= 1 else str(symptom_score)
        
        # Calculate Base Likelihood
        base_likelihood = rf_cl_matrix[gender][age_group][score_key][rf_category]
        
        # Likelihood Classification
        def classify_likelihood(val):
            if val <= 5:
                return "Rất thấp (Very Low)", "#28a745"
            elif val <= 15:
                return "Thấp (Low)", "#17a2b8"
            elif val <= 50:
                return "Trung bình (Moderate)", "#ffc107"
            elif val <= 85:
                return "Cao (High)", "#fd7e14"
            else:
                return "Rất cao (Very High)", "#dc3545"

        likelihood_class, color_hex = classify_likelihood(base_likelihood)
        
        st.markdown(f"""
        <div style='background-color: #f1f2f6; border-radius: 6px; padding: 15px; border-left: 6px solid {color_hex}; margin: 15px 0;'>
            <h4 style='margin: 0; color: #333;'>Kết quả ước tính lâm sàng ban đầu (Base RF-CL):</h4>
            <p style='font-size: 1.5rem; margin: 10px 0 5px 0; font-weight: bold;'>Khả năng lâm sàng mắc CAD tắc nghẽn: <span style='color: {color_hex};'>{base_likelihood}%</span></p>
            <p style='margin: 0; font-size: 1.1rem;'>Nhóm phân loại: <strong style='color: {color_hex};'>{likelihood_class}</strong></p>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # Section C: Adjustments (Figure 5)
        st.subheader("3. Điều chỉnh và Phân tầng lại Khả năng lâm sàng (Adjust Clinical Likelihood)")
        st.markdown("<p style='font-size: 0.95rem; color: #555;'>Người sử dụng có thể cá thể hóa và phân tầng lại dựa trên các yếu tố lâm sàng bổ sung khác (Figure 5):</p>", unsafe_allow_html=True)
        
        adj_col1, adj_col2 = st.columns(2)
        with adj_col1:
            st.write("**Các yếu tố điều chỉnh tăng khả năng lâm sàng (Class I):**")
            adj_ecg = st.checkbox("Có sóng Q bệnh lý hoặc thay đổi ST-T bất thường trên điện tâm đồ lúc nghỉ")
            adj_lvd = st.checkbox("Có giảm chức năng hoặc rối loạn vận động vùng cơ tim thất trái")
            adj_pad = st.checkbox("Có bệnh động mạch ngoại biên (PAD)")
            adj_calc = st.checkbox("Phát hiện vôi hóa mạch vành trên phim chụp cắt lớp vi tính lồng ngực trước đó")
            adj_ex_ecg = st.checkbox("Nghiệm pháp gắng sức điện tâm đồ (Exercise ECG) dương tính/bất thường")
        
        with adj_col2:
            st.write("**Phân tầng lại bằng Điểm vôi hóa mạch vành (CACS - Class IIa):**")
            cacs_available = st.radio("Bệnh nhân có kết quả CACS không?", ["Chưa thực hiện", "Có kết quả"])
            cacs_val = 0
            if cacs_available == "Có kết quả":
                cacs_val = st.number_input("Nhập điểm CACS", min_value=0, max_value=5000, value=0)
                if cacs_val == 0:
                    st.success("🎉 CACS = 0: Khuyến cáo phân tầng lại về nhóm nguy cơ Rất Thấp (≤5%), có thể xem xét trì hoãn làm thêm các xét nghiệm chuyên sâu không xâm lấn.")
                elif cacs_val >= 400:
                    st.warning("⚠️ CACS ≥ 400: Khả năng lâm sàng tăng mạnh lên mức Cao - Rất Cao. Khuyến cáo làm thăm dò chức năng hoặc chụp động mạch vành sớm.")

        # Determine Adjusted Likelihood dynamically for testing path
        adjusted_likelihood = base_likelihood
        if adj_ecg or adj_lvd or adj_pad or adj_calc or adj_ex_ecg:
            adjusted_likelihood += 15  # Clinical judgment representation
            st.info("💡 Do có bất thường lâm sàng bổ sung, khả năng lâm sàng thực tế của bệnh nhân đã được điều chỉnh tăng lên.")
        
        if cacs_available == "Có kết quả" and cacs_val == 0:
            adjusted_likelihood = 5 # Adjusted to very low
        
        st.session_state.calculated_likelihood = adjusted_likelihood

        # Save to state and go next
        st.write("")
        col_prev, col_next = st.columns([1, 1])
        with col_prev:
            if st.button("⬅️ Quay lại Bước 1"):
                set_step(1)
        with col_next:
            if st.button("Xác nhận & Sang Bước 3 ➡️"):
                st.session_state.likelihood_value = adjusted_likelihood
                set_step(3)

# ----------------------------------------------------
# STEP 3: CONFIRMING DIAGNOSIS AND EVENT-RISK ESTIMATION
# ----------------------------------------------------
step3_expanded = (st.session_state.step == 3)
with st.expander("🔍 BƯỚC 3: XÁC ĐỊNH CHẨN ĐOÁN & PHÂN TẦNG NGUY CƠ BIẾN CỐ", expanded=step3_expanded):
    if st.session_state.step < 3:
        st.warning("Vui lòng hoàn thành Bước 2 trước.")
    else:
        st.markdown("<div class='step-header'>BƯỚC 3: Lựa chọn kỹ thuật chẩn đoán phù hợp nhất & Phân tầng nguy cơ biến cố tim mạch</div>", unsafe_allow_html=True)
        
        lik = st.session_state.get('likelihood_value', 20)
        st.markdown(f"Khả năng lâm sàng hiện tại của bệnh nhân: **{lik}%**")
        
        # Display Appropriate first line test according to Figure 6
        st.subheader("1. Khuyến cáo Lựa chọn Thăm dò Chẩn đoán Đầu tay (Figure 6 & 7)")
        
        if lik <= 5:
            st.success("""
            **KHUYẾN CÁO: HOÃN CÁC THĂM DÒ CHẨN ĐOÁN SÂU HƠN (Deferral of testing - Class IIa)**
            - Bệnh nhân có khả năng lâm sàng rất thấp (≤5%). Việc tầm soát thường quy không mang lại lợi ích lâm sàng rõ rệt.
            - Tìm kiếm các nguyên nhân đau ngực không do tim khác (cơ xương khớp, dạ dày - thực quản, phổi...).
            - Chỉ thực hiện nếu các triệu chứng hạn chế nặng hoặc tái phát không tìm được nguyên nhân khác.
            """)
        elif 5 < lik <= 15:
            st.info("""
            **KHUYẾN CÁO: CHỤP CẮT LỚP VI TÍNH ĐỘNG MẠCH VÀNH (CCTA) LÀ CHỈ ĐỊNH ĐẦU TAY (Class I)**
            - Phù hợp nhất để loại trừ bệnh động mạch vành tắc nghẽn ở những người có khả năng lâm sàng thấp.
            - Ngoài ra có thể xem xét chụp CACS trước để phân tầng lại nguy cơ (Class IIa).
            """)
        elif 15 < lik <= 50:
            st.warning("""
            **KHUYẾN CÁO: CHỌN CCTA (Class I A) HOẶC THĂM DÒ HÌNH ẢNH CHỨC NĂNG GẮNG SỨC (Class I B)**
            - Bệnh nhân ở nhóm trung bình có thể lựa chọn 1 trong 2 phương pháp chẩn đoán:
                - **CCTA (Anatomical):** Ưu tiên nếu muốn loại trừ hẹp, đánh giá mảng xơ vữa.
                - **Hình ảnh chức năng gắng sức (Functional - Stress Echo, Stress CMR, SPECT/PET):** Ưu tiên nếu nghi ngờ thiếu máu cơ tim mức độ ý nghĩa và muốn đánh giá chức năng sống còn cơ tim.
            - Ở nhóm này, việc phối hợp hoặc làm nghiệm pháp tiếp theo tuần tự (sequential testing) nếu kết quả thăm dò đầu tiên không rõ ràng là rất phổ biến (Figure 8).
            """)
        elif 50 < lik <= 85:
            st.error("""
            **KHUYẾN CÁO: ƯU TIÊN THĂM DÒ HÌNH ẢNH CHỨC NĂNG GẮNG SỨC (Class I B)**
            - Ở bệnh nhân có khả năng lâm sàng cao (>50%), CCTA có độ đặc hiệu giảm do dễ vôi hóa nặng dẫn đến phóng đại mức độ hẹp mạch vành.
            - Thực hiện: **Stress Echo, Stress CMR, PET hoặc stress SPECT** để chẩn đoán thiếu máu cơ tim mức độ vừa-nặng trực tiếp.
            """)
        else: # > 85%
            st.error("""
            **KHUYẾN CÁO: CHỤP ĐỘNG MẠCH VÀNH XÂM LẤN (ICA) TRỰC TIẾP (Class I C)**
            - Bệnh nhân có khả năng lâm sàng rất cao (>85%) hoặc triệu chứng đau thắt ngực nặng không đáp ứng tối thiểu với thuốc.
            - ICA nên được thực hiện trực tiếp để định hướng tái thông mạch máu cơ tim luôn (phối hợp đo FFR/iFR xâm lấn nếu cần thiết để đánh giá tổn thương hẹp ranh giới).
            """)

        st.divider()

        # Event risk stratification inputs (Table 14)
        st.subheader("2. Đánh giá Nguy cơ Biến cố Tim mạch tương lai (Event-Risk Stratification)")
        st.markdown("<p style='font-size: 0.95rem; color: #555;'>Xác định bệnh nhân có nguy cơ cao xảy ra các biến cố tim mạch bất lợi (MACE) - Khuyến cáo Class I B:</p>", unsafe_allow_html=True)
        
        risk_col1, risk_col2 = st.columns(2)
        with risk_col1:
            high_risk_anatomy = st.checkbox("CCTA/ICA: Tổn thương Thân chung Động mạch vành trái (Left Main) hẹp ≥ 50%")
            high_risk_anatomy_2 = st.checkbox("CCTA/ICA: Hẹp nặng ≥ 70% ở 3 nhánh mạch vành (Three-vessel disease)")
            high_risk_anatomy_3 = st.checkbox("CCTA/ICA: Hẹp đoạn gần động mạch liên thất trước (Proximal LAD) ≥ 70%")
        
        with risk_col2:
            high_risk_functional = st.checkbox("Stress Echo: ≥ 3/16 phân vùng cơ tim bị giảm động hoặc vô động do gắng sức")
            high_risk_functional_2 = st.checkbox("Stress CMR: ≥ 2/16 phân vùng thiếu máu cơ tim diện rộng")
            high_risk_functional_3 = st.checkbox("Stress SPECT/PET: Diện tích thiếu máu cơ tim ≥ 10% cơ thất trái")
            high_risk_functional_4 = st.checkbox("Exercise ECG: Điểm số gắng sức Duke (Duke Treadmill Score) < -10")

        is_high_risk = (high_risk_anatomy or high_risk_anatomy_2 or high_risk_anatomy_3 or 
                        high_risk_functional or high_risk_functional_2 or high_risk_functional_3 or high_risk_functional_4)

        if is_high_risk:
            st.error("""
            **🚨 BỆNH NHÂN THUỘC NHÓM NGUY CƠ BIẾN CỐ CAO (HIGH EVENT-RISK) - Khuyến cáo Class I B:**
            - Chụp mạch vành xâm lấn (ICA) - phối hợp đánh giá sinh lý mạch vành (FFR/iFR) - được khuyến cáo để xem xét chỉ định can thiệp tái thông mạch vành nhằm cải thiện triệu chứng và cải thiện tiên lượng sống còn.
            """)
        else:
            st.info("💡 Bệnh nhân chưa phát hiện các tiêu chuẩn nguy cơ biến cố cao diện rộng trên thăm dò hình ảnh. Ưu tiên điều trị thuốc tối ưu (GDMT).")

        st.write("")
        col_prev, col_next = st.columns([1, 1])
        with col_prev:
            if st.button("⬅️ Quay lại Bước 2"):
                set_step(2)
        with col_next:
            if st.button("Xác nhận & Sang Bước 4 ➡️"):
                st.session_state.high_risk_flag = is_high_risk
                set_step(4)

# ----------------------------------------------------
# STEP 4: OPTIMAL TREATMENT (GDMT & REVALCULARIZATION)
# ----------------------------------------------------
step4_expanded = (st.session_state.step == 4)
with st.expander("💊 BƯỚC 4: CHIẾN LƯỢC ĐIỀU TRỊ TỐI ƯU (GDMT & Revascularization)", expanded=step4_expanded):
    if st.session_state.step < 4:
        st.warning("Vui lòng hoàn thành Bước 3 trước.")
    else:
        st.markdown("<div class='step-header'>BƯỚC 4: Thiết lập chế độ điều trị nội khoa tối ưu (GDMT) & Cân nhắc Tái thông mạch vành</div>", unsafe_allow_html=True)
        
        # Split into tabs for medical management and revascularization
        tab_med, tab_revasc = st.tabs(["💊 Điều trị nội khoa tối ưu (GDMT)", "🩺 Chỉ định Can thiệp/Phẫu thuật"])
        
        with tab_med:
            st.subheader("1. Thay đổi lối sống và Kiểm soát các yếu tố nguy cơ (Class I)")
            st.markdown("""
            *   **Bỏ hoàn toàn thuốc lá:** Hỗ trợ tư vấn cai thuốc, tránh phơi nhiễm khói thuốc lá thụ động.
            *   **Chế độ ăn Địa Trung Hải (Mediterranean Diet):** Hạn chế chất béo bão hòa < 10% tổng năng lượng, tăng cường rau quả, ngũ cốc nguyên hạt. Hạn chế rượu bia (<100g/tuần).
            *   **Hoạt động thể lực:** Tập luyện thể dục cường độ trung bình 30-60 phút ít nhất 5 ngày/tuần. Giảm thời gian ngồi tĩnh tại.
            *   **Kiểm soát cân nặng:** Đưa cân nặng về mức BMI mục tiêu (18.5 - 24.9 kg/m2).
            """)
            
            st.subheader("2. Điều trị bằng thuốc bảo vệ mạch vành, cải thiện tiên lượng (Class I)")
            st.markdown("""
            *   **Kháng kết tập tiểu cầu (Antiplatelets):** 
                *   *Aspirin 75-100 mg/ngày* hoặc *Clopidogrel 75 mg/ngày* được khuyến cáo lâu dài ở bệnh nhân có bằng chứng xơ vữa tắc nghẽn mạch vành (Class I).
            *   **Liệu pháp Lipid:**
                *   Bắt đầu bằng *Statin liều cao* phối hợp hoặc không phối hợp với Ezetimibe.
                *   Mục tiêu LDL-C: **< 1.4 mmol/L (< 55 mg/dL)** và giảm ít nhất 50% so với giá trị nền.
            *   **Kiểm soát huyết áp:** Mục tiêu **120-129/70-79 mmHg** nếu dung nạp tốt (ưu tiên ức chế men chuyển ACEi/ARB).
            *   **Đái tháo đường đi kèm:** Ưu tiên sử dụng nhóm ức chế SGLT2 và/hoặc đồng vận thụ thể GLP-1 để bảo vệ tim mạch, giảm nguy cơ MACE.
            """)
            
            st.subheader("3. Điều trị thuốc giảm triệu chứng Đau thắt ngực (Antianginals)")
            st.markdown("""
            *   **Hàng đầu (First-line):** Sử dụng thuốc **Chẹn beta (Beta-blockers)** và/hoặc **Chẹn kênh Canxi (CCBs)** để kiểm soát nhịp tim và kiểm soát triệu chứng đau ngực (Class I).
            *   **Nitroglycerin xịt/ngậm dưới da:** Luôn kê đơn để cắt cơn đau ngực cấp tính kịp thời.
            """)
            
        with tab_revasc:
            st.subheader("Tiêu chuẩn Tái thông mạch vành theo Hướng dẫn ESC 2024")
            
            is_high_risk = st.session_state.get('high_risk_flag', False)
            if is_high_risk:
                st.markdown("""
                <div class='warning-box' style='border-left-color: #fd7e14;'>
                    <h4 style='color: #fd7e14; margin-top: 0;'>👉 BỆNH NHÂN CÓ CHỈ ĐỊNH TÁI THÔNG MẠCH VÀNH ĐỂ CẢI THIỆN TIÊN LƯỢNG (Class I A)</h4>
                    <p>Do bệnh nhân thuộc nhóm nguy cơ biến cố cao (Hẹp Thân chung, 3 nhánh hoặc đoạn gần LAD nguy cơ cao diện rộng), phẫu thuật làm cầu nối chủ-vành (CABG) hoặc can thiệp động mạch vành qua da (PCI) được chỉ định để kéo dài thời gian sống còn và ngăn ngừa Nhồi máu cơ tim tự phát.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class='info-box'>
                    <strong>Xem xét Tái thông mạch vành để cải thiện triệu chứng (Class I A):</strong><br>
                    Ở những bệnh nhân không thuộc nhóm nguy cơ biến cố cao, chỉ định tái thông mạch vành được đặt ra khi:
                    Triệu chứng đau thắt ngực dai dẳng, ảnh hưởng chất lượng cuộc sống mặc dù đã tối ưu hóa điều trị nội khoa tối đa (GDMT) với ít nhất 2 nhóm thuốc kháng đau thắt ngực.
                </div>
                """, unsafe_allow_html=True)

            st.markdown("""
            **Các lưu ý kỹ thuật quan trọng của ESC 2024:**
            *   **Hẹp ranh giới (Intermediate stenosis):** Luôn đánh giá chức năng bằng **FFR (fractional flow reserve)** hoặc **iFR (instantaneous wave-free ratio)** trước khi quyết định can thiệp (Class I).
            *   **Can thiệp phức tạp:** Sử dụng các phương tiện chẩn đoán hình ảnh trong lòng mạch như **IVUS (intravascular ultrasound)** hoặc **OCT** được khuyến cáo để hướng dẫn kỹ thuật can thiệp tối ưu (Class I).
            *   **Thảo luận nhóm tim mạch (Heart Team):** Khuyên dùng ở những ca tổn thương mạch vành đa nhánh, tổn thương thân chung phức tạp hoặc có đái tháo đường kèm theo để lựa chọn giữa PCI hay CABG (Class I).
            """)

        st.write("")
        if st.button("⬅️ Quay lại Bước 3"):
            set_step(3)

st.write("")
st.markdown("<p style='text-align: center; font-size: 0.8rem; color: #888;'>Phát triển dựa trên Hướng dẫn của Hội Tim mạch Châu Âu (ESC) 2024 về quản lý Hội chứng mạch vành mạn</p>", unsafe_allow_html=True)

