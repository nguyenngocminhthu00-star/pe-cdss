import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="ESC 2024 CCS Initial Management Tool v2",
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
        font-size: 1.25rem;
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
    .anoca-box {
        background-color: #f3e9f9;
        border-left: 6px solid #8e44ad;
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
    .symptom-tag-inc {
        background-color: #ffe6e6;
        color: #b30000;
        padding: 3px 8px;
        border-radius: 3px;
        font-weight: bold;
        font-size: 0.85rem;
    }
    .symptom-tag-dec {
        background-color: #e6f7ff;
        color: #0066cc;
        padding: 3px 8px;
        border-radius: 3px;
        font-weight: bold;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🫀 QUẢN LÝ BAN ĐẦU NGHI NGỜ HỘI CHỨNG MẠCH VÀNH MẠN (CCS)</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555; font-size: 1.1rem;'>Công cụ lâm sàng tương tác từng bước (Stepwise Approach) theo Hướng dẫn ESC 2024 - Phiên bản v2</p>", unsafe_allow_html=True)
st.divider()

# Session State Initialization for Step Flow (Option A: Dynamic Expansion)
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'acute_flag' not in st.session_state:
    st.session_state.acute_flag = False

# Progress Bar
step_cols = st.columns(4)
steps_labels = ["1. Đánh giá ban đầu", "2. Đánh giá chuyên sâu & RF-CL", "3. Chẩn đoán xác định", "4. Điều trị & ANOCA/INOCA"]
for idx, col in enumerate(step_cols):
    step_num = idx + 1
    if st.session_state.step >= step_num:
        col.markdown(f"<div style='text-align: center; color: #17b978; font-weight: bold; font-size: 1.1rem;'>🟢 {steps_labels[idx]}</div>", unsafe_allow_html=True)
    else:
        col.markdown(f"<div style='text-align: center; color: #888; font-size: 1.1rem;'>⚪ {steps_labels[idx]}</div>", unsafe_allow_html=True)

st.divider()

# Helper function to transition steps
def set_step(step_num):
    st.session_state.step = step_num
    st.rerun()

# ----------------------------------------------------
# STEP 1: GENERAL CLINICAL EVALUATION (Figure 3 & Basic Tests)
# ----------------------------------------------------
step1_expanded = (st.session_state.step == 1)
with st.expander("🩺 BƯỚC 1: ĐÁNH GIÁ LÂM SÀNG BAN ĐẦU (Initial Evaluation)", expanded=step1_expanded):
    st.markdown("<div class='step-header'>BƯỚC 1: Khai thác bệnh sử triệu chứng (Figure 3), Loại trừ ACS và thực hiện thăm dò cơ bản</div>", unsafe_allow_html=True)
    
    # 1. Red Flags to rule out ACS
    st.subheader("⚠️ 1. Triệu chứng lâm sàng cấp tính / Cảnh báo đỏ (Loại trừ ACS)")
    red_col1, red_col2 = st.columns(2)
    with red_col1:
        acute_symptoms = st.checkbox("Đau thắt ngực mới xuất hiện, tăng dần tần suất hoặc cường độ (Crescendo angina)")
        unstable_symptoms = st.checkbox("Triệu chứng huyết động không ổn định (đau ngực khi nghỉ, suy tim cấp, hoặc rối loạn nhịp mới xuất hiện)")
    with red_col2:
        resting_ecg_acute = st.checkbox("ECG lúc nghỉ có biến đổi động học cấp tính (ST chênh lên/chênh xuống, sóng T âm sâu đối xứng)")

    st.divider()

    # 2. Symptoms Characteristics based on Figure 3 (Main CCS symptoms)
    st.subheader("📋 2. Khảo sát Đặc điểm Triệu chứng Lâm sàng (Figure 3 - ESC 2024)")
    st.markdown("<p style='font-size: 0.95rem; color: #555;'>Phân tích đặc điểm triệu chứng giúp bác sĩ định hướng lâm sàng trước khi tính thang điểm RF-CL:</p>", unsafe_allow_html=True)
    
    symptom_presentation = st.radio("Lựa chọn triệu chứng chính của bệnh nhân:", 
                                    ["Đau/Khó chịu vùng ngực (Chest discomfort)", "Khó thở khi gắng sức (Exertional dyspnoea)"])
    
    symptom_analysis = {"type": symptom_presentation, "score_modifier": 0, "summary_text": ""}
    
    if symptom_presentation == "Đau/Khó chịu vùng ngực (Chest discomfort)":
        st.write("**Đánh giá các đặc tính cơn đau thắt ngực:**")
        col_ang1, col_ang2 = st.columns(2)
        
        with col_ang1:
            st.markdown("<span class='symptom-tag-inc'>Tăng khả năng lâm sàng (Increasing Likelihood)</span>", unsafe_allow_html=True)
            inc_q = st.checkbox("Tính chất: Đau bóp nghẹt, thắt, siết chặt hoặc đè nặng (Strangling, Constricting, Squeezing, Pressure, Heaviness)")
            inc_l = st.checkbox("Vị trí: Sau xương ức, lan ra cánh tay trái, cổ, hàm, vai hoặc vùng liên bả vai; kích thước khoảng một nắm tay (Fist-size)")
            inc_d = st.checkbox("Thời gian: Ngắn, kéo dài khoảng 5–10 phút")
            inc_tr = st.checkbox("Yếu tố kích gợi: Xuất hiện khi gắng sức, xúc cảm; nặng hơn khi trời lạnh, gió mạnh hoặc sau bữa ăn thịnh soạn")
            inc_re = st.checkbox("Yếu tố giảm đau: Giảm trong vòng 1-5 phút sau khi ngừng gắng sức hoặc đáp ứng nhanh với Nitroglycerin ngậm/xịt dưới lưỡi")
        
        with col_ang2:
            st.markdown("<span class='symptom-tag-dec'>Giảm khả năng lâm sàng (Decreasing Likelihood)</span>", unsafe_allow_html=True)
            dec_q = st.checkbox("Tính chất: Đau rát bỏng, nhói nhọn như dao đâm, xé rách, hoặc đau âm ỉ kéo dài (Burning, Sharp, Tearing, Pleuritic, Aching)")
            dec_l = st.checkbox("Vị trí: Đau lệch phải hoàn toàn, đau di chuyển không cố định, hoặc khu trú tại một điểm rất nhỏ")
            dec_d = st.checkbox("Thời gian: Đau rất thoáng qua vài giây hoặc đau liên tục nhiều giờ/nhiều ngày")
            dec_tr = st.checkbox("Yếu tố kích gợi: Đau khi nghỉ ngơi, khi hít sâu, khi ho hoặc khi ấn chẩn vào thành ngực/xương ức")
            dec_re = st.checkbox("Yếu tố giảm đau: Giảm sau khi dùng thuốc kháng toan dạ dày (antacids) hoặc uống sữa")
            
        # Calculation of symptoms score (Winther criteria in Step 2 needs symptom_score 0-3)
        # Based on typical definition: 
        # - Constricting retrosternal discomfort (1 point)
        # - Provoked by exertion or emotion (1 point)
        # - Relieved by rest or nitrates within 5 min (1 point)
        calc_symptom_score = 0
        if inc_q or inc_l: calc_symptom_score += 1
        if inc_tr: calc_symptom_score += 1
        if inc_re: calc_symptom_score += 1
        
        symptom_analysis["symptom_score"] = calc_symptom_score
        
        # Summary analysis helper
        inc_count = sum([inc_q, inc_l, inc_d, inc_tr, inc_re])
        dec_count = sum([dec_q, dec_l, dec_d, dec_tr, dec_re])
        
        if inc_count > dec_count:
            symptom_analysis["summary_text"] = "👉 Triệu chứng đau ngực có nhiều đặc điểm **GỢI Ý TĂNG** khả năng mắc CCS (đau thắt ngực điển hình hoặc không điển hình)."
        elif dec_count > inc_count:
            symptom_analysis["summary_text"] = "👉 Triệu chứng đau ngực có nhiều đặc điểm **GỢI Ý GIẢM** khả năng mắc CCS (nghi ngờ đau ngực không do tim)."
        else:
            symptom_analysis["summary_text"] = "👉 Triệu chứng đau ngực có đặc điểm đan xen trung tính, cần đánh giá cẩn thận."
            
    else: # Exertional dyspnoea
        st.write("**Đánh giá đặc tính khó thở:**")
        col_dys1, col_row2 = st.columns(2)
        with col_dys1:
            st.markdown("<span class='symptom-tag-inc'>Tăng khả năng lâm sàng (Increasing Likelihood)</span>", unsafe_allow_html=True)
            inc_dys_q = st.checkbox("Tính chất: Cảm giác hụt hơi, không thở sâu được (Difficulty catching breath)")
            inc_dys_tr = st.checkbox("Yếu tố kích gợi: Chỉ xuất hiện khi gắng sức thể lực")
            inc_dys_re = st.checkbox("Yếu tố giảm: Hết nhanh chóng ngay sau khi ngừng gắng sức")
        with col_row2:
            st.markdown("<span class='symptom-tag-dec'>Giảm khả năng lâm sàng (Decreasing Likelihood)</span>", unsafe_allow_html=True)
            dec_dys_q = st.checkbox("Tính chất: Khó thở ra, thở có tiếng rít/khò khè (Difficulty to exhale, with wheezing)")
            dec_dys_tr = st.checkbox("Yếu tố kích gợi: Xuất hiện cả khi nghỉ ngơi hoặc liên quan đến ho")
            dec_dys_re = st.checkbox("Yếu tố giảm: Giảm chậm khi nghỉ ngơi hoặc chỉ đỡ sau khi xịt thuốc giãn phế quản")
            
        symptom_analysis["symptom_score"] = 2  # Dyspnoea score is fixed to 2 in RF-CL matrix
        
        inc_dys_count = sum([inc_dys_q, inc_dys_tr, inc_dys_re])
        dec_dys_count = sum([dec_dys_q, dec_dys_tr, dec_dys_re])
        
        if inc_dys_count > dec_dys_count:
            symptom_analysis["summary_text"] = "👉 Triệu chứng khó thở có đặc tính **GỢI Ý TĂNG** khả năng do thiếu máu cơ tim (tương đương đau ngực)."
        else:
            symptom_analysis["summary_text"] = "👉 Triệu chứng khó thở **GỢI Ý GIẢM** khả năng do tim, hướng tới nguyên nhân hô hấp (COPD, hen...)."

    # Display analysis
    st.info(symptom_analysis["summary_text"])
    st.session_state.symptom_analysis = symptom_analysis

    st.divider()

    # 3. Basic & Selected Patient Testing
    st.subheader("🧪 3. Thăm dò Cận lâm sàng Ban đầu (Basic & Selected Testing - Class I)")
    st.markdown("<p style='font-size: 0.95rem; color: #555;'>Tích chọn các thăm dò đã thực hiện hoặc cần chỉ định để quản lý ban đầu:</p>", unsafe_allow_html=True)
    
    test_col1, test_col2 = st.columns(2)
    with test_col1:
        st.write("**Xét nghiệm thường quy bắt buộc (Cho mọi bệnh nhân - Class I):**")
        done_ecg = st.checkbox("Điện tâm đồ 12 chuyển đạo lúc nghỉ (Resting ECG)", value=True)
        done_biochem = st.checkbox("Xét nghiệm Hóa sinh máu cơ bản (Biochemistry)")
        
        if done_biochem:
            st.markdown("""
            <div class='recommendation-box' style='font-size: 0.9rem; padding: 10px;'>
                <strong>Bộ xét nghiệm hóa sinh khuyến cáo (ESC 2024):</strong><br>
                - <strong>Troponin tim (hs-cTn):</strong> Chỉ định khi nghi ngờ ACS ổn định hay mất bù.<br>
                - <strong>Bilan lipid máu:</strong> Cholesterol toàn phần, HDL-C, Triglycerid và đặc biệt là <strong>LDL-C</strong> làm cơ sở điều trị.<br>
                - <strong>Đánh giá đường huyết:</strong> HbA1c và Đường huyết đói.<br>
                - <strong>Chức năng thận:</strong> Creatinine huyết thanh và ước tính mức lọc cầu thận <strong>eGFR</strong>.<br>
                - <strong>Chức năng tuyến giáp (TSH, FT4):</strong> Khuyến cáo làm ít nhất 1 lần (Class I B).<br>
                - <strong>Khác:</strong> Tổng phân tích tế bào máu (loại trừ thiếu máu), hs-CRP/Fibrinogen (cân nhắc phân tầng nguy cơ - IIa B).
            </div>
            """, unsafe_allow_html=True)
            
    with test_col2:
        st.write("**Thăm dò bổ sung cho các đối tượng chọn lọc (Selected Patients):**")
        done_cxr = st.checkbox("Chụp X-quang ngực thẳng (Chest X-ray)")
        done_pft = st.checkbox("Đo chức năng hô hấp (Pulmonary Function Test - PFT)")
        
        if done_cxr:
            st.markdown("""
            <div class='info-box' style='font-size: 0.9rem;'>
                <strong>Chỉ định Chest X-ray (Class IIa C):</strong><br>
                Cân nhắc cho bệnh nhân có biểu hiện lâm sàng nghi ngờ suy tim kèm theo, nghi ngờ bệnh phổi cấp tính, phình tách ngực, hoặc đau ngực chưa rõ nguyên nhân khác.
            </div>
            """, unsafe_allow_html=True)
            
        if done_pft:
            st.markdown("""
            <div class='info-box' style='font-size: 0.9rem;'>
                <strong>Chỉ định PFT (Class I C):</strong><br>
                Khuyến cáo thực hiện ở những bệnh nhân có triệu chứng chủ đạo là Khó thở (Dyspnoea) nhằm phát hiện và đánh giá mức độ của bệnh lý hô hấp đi kèm (COPD, Hen phế quản).
            </div>
            """, unsafe_allow_html=True)

    # Check for acute coronary syndrome (ACS) warning
    if acute_symptoms or unstable_symptoms or resting_ecg_acute:
        st.session_state.acute_flag = True
        st.markdown("""
        <div class='warning-box'>
            <h3 style='color: #ff4d4d; margin-top: 0;'>🔴 CẢNH BÁO: NGHI NGỜ HỘI CHỨNG MẠCH VÀNH CẤP (ACS)!</h3>
            <p>Bệnh nhân có triệu chứng hoặc điện tâm đồ gợi ý mạch vành cấp mất ổn định. <strong>Khuyến cáo chuyển ngay bệnh nhân đến Khoa Cấp cứu (Emergency Department)</strong> để làm Troponin nhạy cảm cao (hs-cTn) và xử trí khẩn cấp theo phác đồ ACS.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.session_state.acute_flag = False

    # Next step button
    st.write("")
    if st.session_state.acute_flag:
        st.button("Bị khóa do cảnh báo đỏ (ACS)", disabled=True)
    else:
        if st.button("Xác nhận & Sang Bước 2 ➡️"):
            set_step(2)


# ----------------------------------------------------
# STEP 2: FURTHER CARDIAC EVALUATION & RF-CL CALCULATOR (CACS Bug Fixed)
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
            st.error("⚠️ Giảm chức năng tâm thu thất trái nặng (LVEF ≤ 40%). Cần điều trị suy tim theo khuyến cáo GDMT và xem xét chụp mạch vành sớm để xác định căn nguyên.")
        elif 41 <= lvef <= 49:
            st.warning("⚠️ Chức năng tâm thu thất trái giảm nhẹ (LVEF 41-49%).")

        st.divider()

        # Section B: RF-CL Calculator
        st.subheader("2. Bộ tính điểm Khả năng lâm sàng mạch vành tắc nghẽn (RF-CL Model - ESC 2024)")
        st.info("Mô hình RF-CL (Winther et al.) tích hợp: Tuổi, Giới tính, Đặc điểm triệu chứng và số lượng Yếu tố nguy cơ động mạch vành.")
        
        calc_col1, calc_col2 = st.columns(2)
        
        # Retrieve symptom score from Step 1 state
        s_analysis = st.session_state.get("symptom_analysis", {"type": "Đau/Khó chịu vùng ngực (Chest discomfort)", "symptom_score": 1})
        
        with calc_col1:
            gender = st.radio("Giới tính sinh học", ["Nữ (Women)", "Nam (Men)"])
            age_group = st.selectbox("Nhóm tuổi", ["30-39", ["40-49"], "50-59", "60-69", "70-80"], index=2)
            # Normalize age_group if nested by mistake
            if isinstance(age_group, list):
                age_group = age_group[0]
            
            st.write(f"Triệu chứng chính đã ghi nhận ở Bước 1: **{s_analysis['type']}**")
            symptom_score = s_analysis['symptom_score']
            st.write(f"👉 Điểm số triệu chứng (Symptom Score) quy đổi: **{symptom_score}/3 điểm**")

        with calc_col2:
            st.markdown("<p style='font-size: 0.9rem; font-weight: bold;'>Các yếu tố nguy cơ tim mạch đi kèm (0-5):</p>", unsafe_allow_html=True)
            rf_family = st.checkbox("Tiền sử gia đình mắc bệnh mạch vành sớm (Nam <55 tuổi, Nữ <65 tuổi)")
            rf_smoking = st.checkbox("Đang hút thuốc lá hoặc có tiền sử hút thuốc nhiều")
            rf_dyslipidemia = st.checkbox("Rối loạn lipid máu (hoặc đang dùng thuốc hạ lipid)")
            rf_hypertension = st.checkbox("Tăng huyết áp (hoặc đang dùng thuốc hạ áp)")
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
            adj_lvd = st.checkbox("Có giảm chức năng hoặc rối loạn vận động vùng cơ tim thất trái trên siêu âm tim")
            adj_pad = st.checkbox("Có bệnh động mạch ngoại biên (PAD) đã xác định")
            adj_calc = st.checkbox("Phát hiện xơ vữa/vôi hóa mạch vành trên phim chụp cắt lớp vi tính lồng ngực trước đó")
            adj_ex_ecg = st.checkbox("Nghiệm pháp gắng sức điện tâm đồ (Exercise ECG) dương tính/bất thường")
        
        with adj_col2:
            st.write("**Phân tầng lại bằng Điểm vôi hóa mạch vành (CACS - Class IIa):**")
            cacs_available = st.radio("Bệnh nhân có kết quả CACS không?", ["Chưa thực hiện", "Có kết quả"])
            
            cacs_val = -1
            adjusted_likelihood = base_likelihood
            
            if cacs_available == "Có kết quả":
                cacs_val = st.number_input("Nhập điểm CACS (Agatston score):", min_value=0, max_value=5000, value=100)
                
                # Full evaluation of all CACS levels based on Figure 5
                if cacs_val == 0:
                    adjusted_likelihood = 5 # Set to very low limit
                    st.success("🎉 **CACS = 0:** Khuyến cáo phân tầng lại về nhóm nguy cơ **Rất Thấp (≤5%)**. Có thể xem xét trì hoãn làm thêm các xét nghiệm chẩn đoán hình ảnh chuyên sâu không xâm lấn (Class IIa).")
                elif 1 <= cacs_val <= 9:
                    adjusted_likelihood = max(5.0, base_likelihood * 0.8)
                    st.info("ℹ️ **CACS 1 - 9:** Vôi hóa tối thiểu. Khả năng lâm sàng thường giữ nguyên hoặc giảm nhẹ. Nguy cơ biến cố lâu dài rất thấp.")
                elif 10 <= cacs_val <= 99:
                    adjusted_likelihood = base_likelihood
                    st.info("ℹ️ **CACS 10 - 99:** Vôi hóa mức độ nhẹ. Khả năng lâm sàng ít thay đổi hoặc tăng nhẹ. Thăm dò chẩn đoán không xâm lấn (ưu tiên CCTA) là phù hợp.")
                elif 100 <= cacs_val <= 399:
                    adjusted_likelihood = min(85.0, max(base_likelihood, base_likelihood + 10))
                    st.warning("⚠️ **CACS 100 - 399:** Vôi hóa mức độ trung bình. Tăng nhẹ khả năng lâm sàng thực tế của bệnh nhân (+10%). Cân nhắc chỉ định CCTA hoặc hình ảnh chức năng gắng sức.")
                elif 400 <= cacs_val <= 999:
                    adjusted_likelihood = min(95.0, max(base_likelihood, base_likelihood + 25))
                    st.warning("⚠️ **CACS 400 - 999:** Vôi hóa mức độ nặng. Khả năng lâm sàng tăng mạnh (+25%). Độ đặc hiệu của CCTA giảm đáng kể do xảo ảnh blooming; khuyến cáo ưu tiên làm các thăm dò hình ảnh chức năng gắng sức (Class IIa).")
                elif cacs_val >= 1000:
                    adjusted_likelihood = min(99.0, max(base_likelihood, base_likelihood + 40))
                    st.error("🚨 **CACS ≥ 1000:** Vôi hóa mạch vành cực kỳ nghiêm trọng. Khả năng lâm sàng rất cao. Khuyến cáo bỏ qua CCTA do xảo ảnh nặng, ưu tiên chỉ định Thăm dò hình ảnh chức năng gắng sức hoặc Chụp mạch vành xâm lấn (ICA) trực tiếp.")

        # Determine Adjusted Likelihood dynamically for clinical signs
        if adj_ecg or adj_lvd or adj_pad or adj_calc or adj_ex_ecg:
            if cacs_available == "Chưa thực hiện":
                adjusted_likelihood = min(95.0, base_likelihood + 15)  # Represent clinical reclassification upwards
                st.info("💡 Do có bất thường lâm sàng bổ sung, khả năng lâm sàng thực tế của bệnh nhân đã được điều chỉnh tăng lên (+15%).")
            elif cacs_val > 0:
                adjusted_likelihood = min(95.0, adjusted_likelihood + 10)
                st.info("💡 Do phối hợp cả bất thường lâm sàng và CACS tăng, khả năng lâm sàng được điều chỉnh tăng thêm.")

        st.session_state.calculated_likelihood = adjusted_likelihood

        # Display Final Adjusted Likelihood
        adj_class, adj_color = classify_likelihood(adjusted_likelihood)
        st.markdown(f"""
        <div style='background-color: #fcfcfc; border: 1px solid #d3d3d3; border-radius: 6px; padding: 15px; border-left: 6px solid {adj_color}; margin: 15px 0;'>
            <h5 style='margin: 0; color: #555;'>Khả năng lâm sàng sau điều chỉnh (Adjusted Likelihood):</h5>
            <p style='font-size: 1.6rem; margin: 5px 0; font-weight: bold; color: {adj_color};'>{adjusted_likelihood:.1f}% ({adj_class})</p>
        </div>
        """, unsafe_allow_html=True)

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
# STEP 3: CONFIRMING DIAGNOSIS AND EVENT-RISK ESTIMATION (ANOCA/INOCA Integrated)
# ----------------------------------------------------
step3_expanded = (st.session_state.step == 3)
with st.expander("🔍 BƯỚC 3: XÁC ĐỊNH CHẨN ĐOÁN & PHÂN TẦNG NGUY CƠ BIẾN CỐ", expanded=step3_expanded):
    if st.session_state.step < 3:
        st.warning("Vui lòng hoàn thành Bước 2 trước.")
    else:
        st.markdown("<div class='step-header'>BƯỚC 3: Lựa chọn kỹ thuật chẩn đoán phù hợp nhất & Phân tầng nguy cơ biến cố tim mạch</div>", unsafe_allow_html=True)
        
        lik = st.session_state.get('likelihood_value', 20)
        st.markdown(f"Khả năng lâm sàng hiện tại của bệnh nhân (đã điều chỉnh): **{lik:.1f}%**")
        
        # Display Appropriate first line test according to Figure 6 & 7
        st.subheader("1. Khuyến cáo Lựa chọn Thăm dò Chẩn đoán Đầu tay (Figure 6 & 7)")
        
        if lik <= 5:
            st.success("""
            **KHUYẾN CÁO: HOÃN CÁC THĂM DÒ CHẨN ĐOÁN MẠCH VÀNH CHUYÊN SÂU (Deferral of testing - Class IIa)**
            - Bệnh nhân có khả năng lâm sàng rất thấp (≤5%). Việc làm thêm cận lâm sàng thường quy không mang lại ích lợi thực tế và có nguy cơ dương tính giả.
            - Tìm kiếm tích cực các nguyên nhân ngoài tim khác (như cơ xương khớp, dạ dày - thực quản, phổi, tâm lý...).
            - Chỉ thực hiện nếu các triệu chứng hạn chế nặng hoặc tái phát nhiều lần mà không tìm thấy nguyên nhân nào khác.
            """)
        elif 5 < lik <= 15:
            st.info("""
            **KHUYẾN CÁO: CHỤP CẮT LỚP VI TÍNH ĐỘNG MẠCH VÀNH (CCTA) LÀ CHỈ ĐỊNH ĐẦU TAY (Class I)**
            - Phù hợp nhất để loại trừ bệnh động mạch vành tắc nghẽn ở những người có khả năng lâm sàng thấp.
            - Có giá trị tiên lượng âm tính rất cao (NPV >98%).
            - Nếu chưa thực hiện, có thể xem xét chụp CACS trước để phân tầng lại nguy cơ (Class IIa).
            """)
        elif 15 < lik <= 50:
            st.warning("""
            **KHUYẾN CÁO: CHỌN CCTA (Class I A) HOẶC THĂM DÒ HÌNH ẢNH CHỨC NĂNG GẮNG SỨC (Class I B)**
            - Bệnh nhân ở nhóm trung bình có thể lựa chọn 1 trong 2 chiến lược chẩn đoán đầu tay:
                - **CCTA (Chiến lược giải phẫu):** Ưu tiên nếu bệnh nhân trẻ tuổi, nhịp tim đều chậm, không vôi hóa nhiều, muốn loại trừ hẹp và đánh giá gánh nặng mảng xơ vữa.
                - **Hình ảnh chức năng gắng sức (Stress Echo, Stress CMR, SPECT/PET):** Ưu tiên nếu nghi ngờ thiếu máu cơ tim mức độ có ý nghĩa lâm sàng, bệnh nhân lớn tuổi hoặc vôi hóa mạch vành nặng.
            - Ở nhóm này, việc phối hợp tuần tự (Sequential testing) giữa giải phẫu và chức năng rất phổ biến nếu kết quả thăm dò đầu tiên không rõ ràng (Figure 8).
            """)
        elif 50 < lik <= 85:
            st.error("""
            **KHUYẾN CÁO: ƯU TIÊN THĂM DÒ HÌNH ẢNH CHỨC NĂNG GẮNG SỨC (Class I B)**
            - Ở bệnh nhân có khả năng lâm sàng cao (>50%), CCTA có độ đặc hiệu giảm nhiều do dễ vôi hóa nặng (calcium blooming) dẫn đến phóng đại mức độ hẹp mạch vành thực tế.
            - Thực hiện: **Stress Echo, Stress CMR, PET hoặc stress SPECT** để chẩn đoán thiếu máu cơ tim và đánh giá diện rộng vùng thiếu máu trực tiếp.
            """)
        else: # > 85%
            st.error("""
            **KHUYẾN CÁO: CHỤP ĐỘNG MẠCH VÀNH XÂM LẤN (ICA) TRỰC TIẾP (Class I C)**
            - Bệnh nhân có khả năng lâm sàng rất cao (>85%), triệu chứng đau thắt ngực nặng không đáp ứng tối thiểu với thuốc, hoặc có dấu hiệu nguy cơ cao trên lâm sàng.
            - ICA nên được thực hiện trực tiếp để định hướng tái thông mạch máu cơ tim luôn (phối hợp đo FFR/iFR xâm lấn tại phòng thông tim nếu cần thiết để đánh giá tổn thương hẹp ranh giới).
            """)

        st.divider()

        # Event risk stratification inputs (Table 14)
        st.subheader("2. Đánh giá Nguy cơ Biến cố Tim mạch tương lai (Event-Risk Stratification - Class I B)")
        st.markdown("<p style='font-size: 0.95rem; color: #555;'>Xác định các tiêu chuẩn nguy cơ cao xảy ra biến cố tim mạch bất lợi (MACE) dựa trên kết quả thăm dò lâm sàng:</p>", unsafe_allow_html=True)
        
        risk_col1, risk_col2 = st.columns(2)
        with risk_col1:
            st.write("**Tiêu chuẩn giải phẫu (trên CCTA hoặc ICA):**")
            high_risk_anatomy = st.checkbox("Hẹp Thân chung Động mạch vành trái (Left Main) ≥ 50%")
            high_risk_anatomy_2 = st.checkbox("Hẹp nặng ≥ 70% ở cả 3 nhánh mạch vành chính (Three-vessel disease)")
            high_risk_anatomy_3 = st.checkbox("Hẹp đoạn gần động mạch liên thất trước (Proximal LAD) ≥ 70%")
        
        with risk_col2:
            st.write("**Tiêu chuẩn chức năng (Thiếu máu diện rộng):**")
            high_risk_functional = st.checkbox("Stress Echo: ≥ 3 trong số 16 phân vùng cơ tim bị giảm động/vô động do gắng sức")
            high_risk_functional_2 = st.checkbox("Stress CMR: ≥ 2 trong số 16 phân vùng thiếu máu cơ tim diện rộng")
            high_risk_functional_3 = st.checkbox("Stress SPECT/PET: Diện tích thiếu máu cơ tim ≥ 10% cơ thất trái (LV)")
            high_risk_functional_4 = st.checkbox("Exercise ECG: Điểm số gắng sức Duke (Duke Treadmill Score) < -11")

        is_high_risk = (high_risk_anatomy or high_risk_anatomy_2 or high_risk_anatomy_3 or 
                        high_risk_functional or high_risk_functional_2 or high_risk_functional_3 or high_risk_functional_4)

        if is_high_risk:
            st.error("""
            **🚨 BỆNH NHÂN THUỘC NHÓM NGUY CƠ BIẾN CỐ CAO (HIGH EVENT-RISK) - Khuyến cáo Class I B:**
            - Chụp mạch vành xâm lấn (ICA) - phối hợp đánh giá sinh lý mạch vành (FFR/iFR) - được khuyến cáo để xem xét chỉ định can thiệp tái thông mạch vành nhằm cải thiện triệu chứng và tiên lượng sống còn lâu dài.
            """)
        else:
            st.info("💡 Bệnh nhân chưa phát hiện các tiêu chuẩn nguy cơ biến cố cao diện rộng trên thăm dò hình ảnh. Ưu tiên điều trị nội khoa tối ưu (GDMT).")

        st.divider()

        # Integration of ANOCA/INOCA path
        st.subheader("💡 3. Xem xét bệnh lý Đau ngực/Thiếu máu cơ tim không do tắc nghẽn (ANOCA / INOCA)")
        st.markdown("""
        Trong thực hành, có tới **40-60%** bệnh nhân đau thắt ngực nghi ngờ CCS khi làm CCTA hoặc ICA không phát hiện hẹp mạch vành tắc nghẽn (Obstructive CAD).
        """)
        
        no_obstructive_cad = st.checkbox("Bệnh nhân Đã được loại trừ mạch vành tắc nghẽn (CCTA hoặc ICA không hẹp ≥50% hoặc FFR >0.8), nhưng vẫn đau ngực dai dẳng")
        
        if no_obstructive_cad:
            st.markdown("""
            <div class='anoca-box'>
                <h4 style='color: #8e44ad; margin-top: 0;'>🧪 TIẾP CẬN CHẨN ĐOÁN ANOCA / INOCA (Khuyến cáo Class I B):</h4>
                <p>Khi mạch vành tắc nghẽn đã được loại trừ mà triệu chứng vẫn tiếp diễn gây suy giảm chất lượng cuộc sống (QoL), khuyến cáo thực hiện <strong>Đo chức năng mạch vành xâm lấn (Invasive Coronary Functional Testing - ICFT)</strong> để xác định kiểu hình (Endotypes) nhằm cá thể hóa điều trị:</p>
                <ul>
                    <li><strong>Đo dự trữ lưu lượng vi tuần hoàn (Adenosine-dependent):</strong> Đánh giá CFR và IMR (hoặc HMR):
                        <ul>
                            <li>Nếu <strong>CFR < 2.0</strong> (hoặc < 2.5) và/hoặc <strong>IMR ≥ 25</strong> (HMR ≥ 2.5) -> Xác định mắc <strong>Rối loạn chức năng vi tuần hoàn mạch vành (CMD)</strong>.</li>
                        </ul>
                    </li>
                    <li><strong>Nghiệm pháp kích thích co thắt (Acetylcholine provocation test):</strong> Truyền tĩnh mạch Ach liều tăng dần (Class I C nếu nghi ngờ VSA):
                        <ul>
                            <li>Nếu có đau ngực, biến đổi ECG và hẹp lòng mạch thượng mạc ≥90% -> Xác định mắc <strong>Co thắt động mạch vành thượng mạc (Epicardial Vasospasm)</strong>.</li>
                            <li>Nếu có đau ngực, biến đổi ECG nhưng hẹp lòng mạch <90% -> Xác định mắc <strong>Co thắt vi tuần hoàn mạch vành (Microvascular Vasospasm)</strong>.</li>
                        </ul>
                    </li>
                    <li><strong>Thăm dò không xâm lấn (Class IIb B):</strong> Transthoracic Doppler của động mạch LAD, stress CMR, hoặc PET có thể được cân nhắc để đánh giá myocardial flow reserve (CFR).</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            st.session_state.anoca_flag = True
        else:
            st.session_state.anoca_flag = False

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
# STEP 4: OPTIMAL TREATMENT (GDMT & ANOCA/INOCA MANAGEMENT)
# ----------------------------------------------------
step4_expanded = (st.session_state.step == 4)
with st.expander("💊 BƯỚC 4: CHIẾN LƯỢC ĐIỀU TRỊ TỐI ƯU (GDMT & Revascularization)", expanded=step4_expanded):
    if st.session_state.step < 4:
        st.warning("Vui lòng hoàn thành Bước 3 trước.")
    else:
        st.markdown("<div class='step-header'>BƯỚC 4: Thiết lập chế độ điều trị nội khoa tối ưu (GDMT) & Hướng dẫn xử trí theo kiểu hình bệnh</div>", unsafe_allow_html=True)
        
        # Check flags from step 3
        is_anoca = st.session_state.get('anoca_flag', False)
        
        # Tabs depending on patient type
        if is_anoca:
            tab_anoca_med, tab_general_med = st.tabs(["🩺 Cá thể hóa điều trị ANOCA / INOCA", "💊 Thuốc bảo vệ chung (CVD Prevention)"])
            
            with tab_anoca_med:
                st.subheader("Cá thể hóa điều trị nội khoa ANOCA/INOCA theo Kiểu hình (Endotypes - Figure 15)")
                st.markdown("""
                Điều trị ANOCA/INOCA cần dựa vào kết quả đo chức năng mạch vành (ICFT) để nhắm đúng cơ chế bệnh sinh:
                """)
                
                endotype_selection = st.selectbox("Chọn kiểu hình (Endotype) xác định được:", [
                    "Cơn đau thắt ngực vi mạch đơn thuần (Microvascular Angina - MVA)",
                    "Đau thắt ngực do co thắt mạch (Vasospastic Angina - VSA) thượng mạc hoặc vi mạch",
                    "Kiểu hình hỗn hợp (Mixed MVA + VSA)",
                    "Rối loạn chức năng nội mạc đơn thuần (Endothelial Dysfunction)"
                ])
                
                if endotype_selection == "Cơn đau thắt ngực vi mạch đơn thuần (Microvascular Angina - MVA)":
                    st.markdown("""
                    <div class='anoca-box' style='border-left-color: #2980b9; background-color: #ebf5fb;'>
                        <h4 style='color: #2980b9; margin-top: 0;'>👉 Phác đồ điều trị cho MVA:</h4>
                        <ul>
                            <li><strong>Chẹn beta (Beta-blockers):</strong> Là lựa chọn hàng đầu để kiểm soát triệu chứng đau ngực và giảm nhịp tim (Class IIa).</li>
                            <li><strong>Chẹn kênh Canxi (CCBs):</strong> Ưu tiên nhóm Dihydropyridine (như Amlodipine) phối hợp nếu chẹn beta đơn trị liệu chưa kiểm soát tốt triệu chứng.</li>
                            <li><strong>Thuốc chống đau ngực khác:</strong> Ranolazine hoặc Trimetazidine có thể cân nhắc phối hợp làm thuốc hàng thứ hai.</li>
                            <li><strong>Thuốc bảo vệ mạch:</strong> Xem xét chỉ định <strong>Ức chế men chuyển (ACEi) / ARB</strong> và <strong>Statin</strong> để cải thiện chức năng nội mạc và xơ vữa mạch máu (Class IIa).</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                elif endotype_selection == "Đau thắt ngực do co thắt mạch (Vasospastic Angina - VSA) thượng mạc hoặc vi mạch":
                    st.markdown("""
                    <div class='anoca-box' style='border-left-color: #d35400; background-color: #fef5e7;'>
                        <h4 style='color: #d35400; margin-top: 0;'>👉 Phác đồ điều trị cho VSA (Co thắt mạch):</h4>
                        <ul>
                            <li><strong>Chẹn kênh Canxi (CCBs) là Thuốc đầu tay bắt buộc (Class I):</strong> Giúp kiểm soát triệu chứng, ngăn ngừa thiếu máu và biến cố loạn nhịp nguy hiểm. Sử dụng Dihydropyridine (Amlodipine) hoặc Non-dihydropyridine (Diltiazem).</li>
                            <li><strong>Liều cao CCBs:</strong> Trường hợp co thắt nặng, có thể cần tăng liều cao (ví dụ: Diltiazem lên tới 360-480 mg/ngày) hoặc phối hợp 2 nhóm CCB với nhau (Diltiazem + Amlodipine).</li>
                            <li><strong>Nitrates tác dụng kéo dài:</strong> Chỉ định thêm nếu CCB đơn trị liệu không đáp ứng hoàn toàn. Luôn có Nitroglycerin ngậm dưới lưỡi để cắt cơn co thắt cấp.</li>
                            <li><strong>Nicorandil:</strong> Thêm vào điều trị phối hợp nếu đau ngực kháng trị.</li>
                            <li><strong>🔴 CẢNH BÁO TRÁNH DÙNG:</strong> <strong>Tránh sử dụng thuốc Chẹn beta đơn thuần</strong> ở bệnh nhân co thắt mạch cô độc vì thuốc có thể làm co thắt mạch nặng thêm thông qua kích thích thụ thể alpha-adrenergic không đối kháng.</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                elif endotype_selection == "Kiểu hình hỗn hợp (Mixed MVA + VSA)":
                    st.markdown("""
                    <div class='anoca-box'>
                        <h4 style='color: #8e44ad; margin-top: 0;'>👉 Phác đồ phối hợp điều trị:</h4>
                        <ul>
                            <li>Sự chồng lấp các kiểu hình là rất thường gặp (chiếm 20-30%).</li>
                            <li>Khuyến cáo ưu tiên sử dụng thuốc <strong>Chẹn kênh canxi (CCBs)</strong> nhóm dihydropyridine phối hợp với thuốc <strong>Chẹn beta</strong> liều thấp (nếu dung nạp tốt và kiểm soát được co thắt).</li>
                            <li>Bắt buộc sử dụng <strong>ACEi/ARB và Statin</strong> để bảo vệ nội mạc mạch máu.</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                else: # Endothelial dysfunction
                    st.markdown("""
                    <div class='anoca-box' style='border-left-color: #27ae60; background-color: #eaf2f8;'>
                        <h4 style='color: #27ae60; margin-top: 0;'>👉 Phác đồ cải thiện chức năng nội mạc:</h4>
                        <ul>
                            <li>Thay đổi lối sống, kiểm soát cân nặng chặt chẽ là tối quan trọng.</li>
                            <li><strong>Statin liều cao và Thuốc ức chế men chuyển (ACEi):</strong> Có bằng chứng rõ ràng giúp phục hồi và cải thiện đáng kể chức năng nội mạc mạch vành.</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                    
            with tab_general_med:
                st.subheader("Liệu pháp phòng ngừa biến cố mạch vành chung (Class I)")
                st.markdown("""
                Dù là ANOCA/INOCA, việc phòng ngừa xơ vữa tiến triển vẫn cực kỳ quan trọng:
                - **Statin:** Điều trị Statin cường độ cao nhằm kiểm soát các mảng xơ vữa vi mạch và thượng mạc kèm theo.
                - **Kiểm soát huyết áp:** Mục tiêu huyết áp tối ưu là **120-129 / 70-79 mmHg** nếu bệnh nhân dung nạp tốt (ưu tiên thuốc nhóm ACEi/ARB).
                - **Kiểm soát các yếu tố lối sống:** Bỏ hoàn toàn thuốc lá, chế độ ăn Địa Trung Hải, rèn luyện thể lực phù hợp.
                """)
                
        else: # Standard Obstructive CAD treatment
            tab_med, tab_revasc = st.tabs(["💊 Điều trị nội khoa tối ưu (GDMT)", "🩺 Chỉ định Tái thông mạch (Revascularization)"])
            
            with tab_med:
                st.subheader("1. Thay đổi lối sống và Kiểm soát các yếu tố nguy cơ (Class I)")
                st.markdown("""
                *   **Bỏ hoàn toàn thuốc lá:** Hỗ trợ tư vấn cai thuốc chủ động, tránh phơi nhiễm khói thuốc lá thụ động.
                *   **Chế độ ăn Địa Trung Hải (Mediterranean Diet):** Hạn chế chất béo bão hòa < 10% tổng năng lượng, tăng cường rau quả, ngũ cốc nguyên hạt. Hạn chế tối đa rượu bia (<100g cồn/tuần).
                *   **Hoạt động thể lực:** Tập luyện thể dục cường độ trung bình ít nhất 150-300 phút mỗi tuần hoặc 30-60 phút x 5 ngày/tuần. Giảm thiểu thời gian ngồi tĩnh tại.
                *   **Kiểm soát cân nặng:** Đưa cân nặng về mức BMI mục tiêu (18.5 - 24.9 kg/m2 cho người châu Á).
                """)
                
                st.subheader("2. Điều trị bằng thuốc bảo vệ mạch vành, cải thiện tiên lượng (Class I)")
                st.markdown("""
                *   **Kháng kết tập tiểu cầu (Antiplatelets):** 
                    *   *Aspirin 75-100 mg/ngày* hoặc *Clopidogrel 75 mg/ngày* (nếu dị ứng Aspirin) được khuyến cáo dùng lâu dài ở bệnh nhân có bằng chứng hẹp tắc nghẽn mạch vành (Class I).
                *   **Liệu pháp Lipid máu:**
                    *   Bắt đầu ngay bằng *Statin liều cao* phối hợp hoặc không phối hợp với Ezetimibe.
                    *   Mục tiêu LDL-C nghiêm ngặt: **< 1.4 mmol/L (< 55 mg/dL)** và giảm ít nhất 50% so với giá trị nền (Class I).
                *   **Kiểm soát huyết áp:** Mục tiêu **120-129/70-79 mmHg** nếu dung nạp tốt (ưu tiên thuốc ức chế men chuyển ACEi hoặc ARB).
                *   **Đái tháo đường đi kèm:** Bắt buộc ưu tiên sử dụng nhóm **ức chế SGLT2 (SGLT2i)** và/hoặc đồng vận thụ thể **GLP-1 (GLP-1 RA)** để bảo vệ tim mạch, thận và giảm nguy cơ MACE bất kể mức HbA1c nền (Class I).
                """)
                
                st.subheader("3. Điều trị thuốc giảm triệu chứng Đau thắt ngực (Antianginals)")
                st.markdown("""
                *   **Hàng đầu (First-line - Class I):** Sử dụng thuốc **Chẹn beta (Beta-blockers)** và/hoặc **Chẹn kênh Canxi (CCBs)** để kiểm soát nhịp tim mục tiêu và kiểm soát triệu chứng đau ngực gắng sức.
                *   **Nitroglycerin xịt/ngậm dưới da:** Luôn luôn kê đơn để cắt cơn đau thắt ngực cấp tính kịp thời khi cần thiết.
                """)
                
            with tab_revasc:
                st.subheader("Tiêu chuẩn Tái thông mạch vành theo Hướng dẫn ESC 2024")
                
                is_high_risk = st.session_state.get('high_risk_flag', False)
                if is_high_risk:
                    st.markdown("""
                    <div class='warning-box' style='border-left-color: #fd7e14;'>
                        <h4 style='color: #fd7e14; margin-top: 0;'>👉 BỆNH NHÂN CÓ CHỈ ĐỊNH TÁI THÔNG MẠCH VÀNH ĐỂ CẢI THIỆN TIÊN LƯỢNG (Class I A)</h4>
                        <p>Do bệnh nhân thuộc nhóm nguy cơ biến cố tim mạch cao (Hẹp Thân chung LM, hẹp 3 nhánh mạch vành chính hoặc hẹp đoạn gần LAD nguy cơ cao trên thăm dò diện rộng), phẫu thuật làm cầu nối chủ-vành (CABG) hoặc can thiệp động mạch vành qua da (PCI) được chỉ định để kéo dài thời gian sống còn và ngăn ngừa Nhồi máu cơ tim tự phát.</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class='info-box'>
                        <strong>Xem xét Tái thông mạch vành để cải thiện triệu chứng lâm sàng (Class I A):</strong><br>
                        Ở những bệnh nhân không thuộc nhóm nguy cơ biến cố cao, chỉ định tái thông mạch vành được đặt ra khi:<br>
                        Các triệu chứng đau thắt ngực vẫn tiếp diễn dai dẳng, ảnh hưởng nghiêm trọng chất lượng cuộc sống mặc dù đã được tối ưu hóa điều trị nội khoa tối đa (GDMT) với ít nhất 2 nhóm thuốc kháng đau thắt ngực khác nhau.
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("""
                **Các lưu ý kỹ thuật quan trọng của ESC 2024:**
                *   **Hẹp ranh giới (Intermediate stenosis):** Luôn luôn đánh giá chức năng bằng **FFR (fractional flow reserve)** hoặc **iFR (instantaneous wave-free ratio)** trước khi quyết định can thiệp (Class I).
                *   **Can thiệp phức tạp:** Sử dụng các phương tiện chẩn đoán hình ảnh trong lòng mạch như **IVUS (intravascular ultrasound)** hoặc **OCT** được khuyến cáo để hướng dẫn kỹ thuật can thiệp tối ưu hóa lòng mạch (Class I).
                *   **Thảo luận nhóm tim mạch (Heart Team):** Khuyên dùng ở những ca tổn thương mạch vành đa nhánh, tổn thương thân chung phức tạp hoặc có đái tháo đường kèm theo để lựa chọn giữa PCI hay CABG (Class I).
                """)

        st.write("")
        if st.button("⬅️ Quay lại Bước 3"):
            set_step(3)

st.write("")
st.markdown("<p style='text-align: center; font-size: 0.8rem; color: #888;'>Phát triển dựa trên Hướng dẫn của Hội Tim mạch Châu Âu (ESC) 2024 về quản lý Hội chứng mạch vành mạn</p>", unsafe_allow_html=True)
