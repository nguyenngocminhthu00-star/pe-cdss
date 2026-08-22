import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="ESC 2024 CCS Initial Management & Lipid Optimizer Tool",
    page_icon="🫀",
    layout="wide"
)

# Custom Styling for cardiology clinical aesthetics
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6;
    }
    .main-title {
        color: #1e3d59;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        text-align: center;
        padding: 5px;
        font-weight: bold;
    }
    .step-header {
        color: #17b978;
        font-weight: bold;
        font-size: 1.25rem;
        border-bottom: 2px solid #17b978;
        padding-bottom: 5px;
        margin-top: 10px;
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
    .success-box {
        background-color: #f3fbf7;
        border-left: 6px solid #28a745;
        padding: 15px;
        border-radius: 4px;
        margin: 10px 0;
    }
    .info-box {
        background-color: #f7f9fa;
        border: 1px solid #d3d3d3;
        padding: 12px;
        border-radius: 4px;
        margin: 8px 0;
    }
    .symptom-tag-inc {
        background-color: #ffe8e8;
        color: #c92a2a;
        padding: 3px 8px;
        border-radius: 3px;
        font-weight: bold;
        font-size: 0.85rem;
        border: 1px solid #ffc9c9;
        display: inline-block;
        margin-bottom: 5px;
    }
    .symptom-tag-dec {
        background-color: #e6fcf5;
        color: #087f5b;
        padding: 3px 8px;
        border-radius: 3px;
        font-weight: bold;
        font-size: 0.85rem;
        border: 1px solid #c3fae8;
        display: inline-block;
        margin-bottom: 5px;
    }
    .class-badge-1 {
        background-color: #2b8a3e;
        color: white;
        padding: 2px 6px;
        border-radius: 3px;
        font-weight: bold;
        font-size: 0.8rem;
    }
    .class-badge-2a {
        background-color: #e67e22;
        color: white;
        padding: 2px 6px;
        border-radius: 3px;
        font-weight: bold;
        font-size: 0.8rem;
    }
    .class-badge-2b {
        background-color: #f1c40f;
        color: black;
        padding: 2px 6px;
        border-radius: 3px;
        font-weight: bold;
        font-size: 0.8rem;
    }
    .class-badge-3 {
        background-color: #c0392b;
        color: white;
        padding: 2px 6px;
        border-radius: 3px;
        font-weight: bold;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🫀 QUẢN LÝ BAN ĐẦU NGHI NGỜ HỘI CHỨNG MẠCH VÀNH MẠN (CCS)</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555; font-size: 1.05rem;'>Công cụ lâm sàng tương tác từng bước (Stepwise Approach) tích hợp Module Lipid Chuyên sâu & ANOCA/INOCA theo Hướng dẫn ESC 2024</p>", unsafe_allow_html=True)
st.divider()

# Session State Initialization for Step Flow (Option A: Dynamic Expansion)
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'acute_flag' not in st.session_state:
    st.session_state.acute_flag = False
if 'lipid_unit' not in st.session_state:
    st.session_state.lipid_unit = "mmol/L"

# Persistent states for cross-step dynamic linking
if 'ldlc_val_mmol' not in st.session_state:
    st.session_state.ldlc_val_mmol = 3.0
if 'tg_val_mmol' not in st.session_state:
    st.session_state.tg_val_mmol = 1.8
if 'egfr_val' not in st.session_state:
    st.session_state.egfr_val = 90
if 'ecg_abnormal' not in st.session_state:
    st.session_state.ecg_abnormal = False
if 'cxr_abnormal' not in st.session_state:
    st.session_state.cxr_abnormal = False
if 'pft_abnormal' not in st.session_state:
    st.session_state.pft_abnormal = False
if 'diabetes_flag' not in st.session_state:
    st.session_state.diabetes_flag = False
if 'dyslipidemia_flag' not in st.session_state:
    st.session_state.dyslipidemia_flag = False
if 'hypertension_flag' not in st.session_state:
    st.session_state.hypertension_flag = False

# Progress Bar
step_cols = st.columns(4)
steps_labels = [
    "1. Đánh giá lâm sàng & CLS",
    "2. Đánh giá chuyên sâu & RF-CL",
    "3. Chẩn đoán & ANOCA/INOCA",
    "4. Điều trị nội khoa & Can thiệp"
]
for idx, col in enumerate(step_cols):
    step_num = idx + 1
    if st.session_state.step >= step_num:
        col.markdown(f"<div style='text-align: center; color: #17b978; font-weight: bold;'>🟢 {steps_labels[idx]}</div>", unsafe_allow_html=True)
    else:
        col.markdown(f"<div style='text-align: center; color: #888;'>⚪ {steps_labels[idx]}</div>", unsafe_allow_html=True)

st.divider()

# Global Warning Check for ACS (Red Flags) - Displayed at the very top of the app if triggered
if st.session_state.acute_flag:
    st.markdown("""
    <div class='warning-box'>
        <h3 style='color: #ff4d4d; margin-top: 0;'>🔴 CẢNH BÁO KHẨN CẤP: NGHI NGỜ HỘI CHỨNG MẠCH VÀNH CẤP (ACS)!</h3>
        <p style='font-size: 1.1rem;'>Bệnh nhân có triệu chứng đau ngực không ổn định, biến đổi ECG cấp tính hoặc huyết động không ổn định. 
        <strong>Khuyến cáo chuyển ngay bệnh nhân đến Khoa Cấp cứu (Emergency Department)</strong> để làm Troponin nhạy cảm cao (hs-cTn) và xử trí khẩn cấp theo phác đồ ACS. Không tiến hành quy trình chẩn đoán mạch vành mạn.</p>
    </div>
    """, unsafe_allow_html=True)

# Helper function to transition steps
def set_step(step_num):
    st.session_state.step = step_num
    st.rerun()

# ----------------------------------------------------
# STEP 1: CLINICAL EVALUATION, SYMPTOMS (FIG 3) & CLS RESULTS
# ----------------------------------------------------
step1_expanded = (st.session_state.step == 1)
with st.expander("🩺 BƯỚC 1: ĐÁNH GIÁ LÂM SÀNG BAN ĐẦU & CẬN LÂM SÀNG CƠ BẢN", expanded=step1_expanded):
    st.markdown("<div class='step-header'>BƯỚC 1: Khai thác bệnh sử triệu chứng (Figure 3), Loại trừ ACS và thực hiện thăm dò cơ bản</div>", unsafe_allow_html=True)
    
    # 1. Red Flags to rule out ACS
    st.subheader("⚠️ 1. Triệu chứng lâm sàng cấp tính / Cảnh báo đỏ (Loại trừ ACS)")
    red_col1, red_col2 = st.columns(2)
    with red_col1:
        acute_symptoms = st.checkbox(
            "Đau thắt ngực mới xuất hiện, tăng dần tần suất hoặc cường độ (Crescendo angina)", 
            value=st.session_state.get('acute_s_val', False),
            key='acute_s_val'
        )
        unstable_symptoms = st.checkbox(
            "Triệu chứng huyết động không ổn định (đau ngực khi nghỉ, suy tim cấp, hoặc loạn nhịp mới xuất hiện)",
            value=st.session_state.get('unstable_s_val', False),
            key='unstable_s_val'
        )
    with red_col2:
        resting_ecg_acute = st.checkbox(
            "ECG lúc nghỉ có biến đổi động học cấp tính (ST chênh lên/chênh xuống, sóng T âm sâu đối xứng)",
            value=st.session_state.get('resting_ecg_acute_val', False),
            key='resting_ecg_acute_val'
        )

    # Update global acute flag immediately based on checkboxes
    if acute_symptoms or unstable_symptoms or resting_ecg_acute:
        if not st.session_state.acute_flag:
            st.session_state.acute_flag = True
            st.rerun()
    else:
        if st.session_state.acute_flag:
            st.session_state.acute_flag = False
            st.rerun()

    st.divider()

    # 2. Symptoms Characteristics based on Figure 3 (Main CCS symptoms)
    st.subheader("📋 2. Khảo sát Chi tiết Đặc điểm Triệu chứng Lâm sàng (Figure 3 - ESC 2024)")
    st.markdown("<p style='font-size: 0.95rem; color: #555;'>Phân tích chi tiết đặc tính cơn đau ngực hoặc khó thở giúp định hướng lâm sàng:</p>", unsafe_allow_html=True)
    
    symptom_presentation = st.radio("Lựa chọn triệu chứng chủ đạo của bệnh nhân:", 
                                    ["Đau/Khó chịu vùng ngực (Chest discomfort)", "Khó thở khi gắng sức (Exertional dyspnoea)"])
    
    symptom_analysis = {"type": symptom_presentation, "score_modifier": 0, "summary_text": "", "auto_winther_score": 0}
    
    if symptom_presentation == "Đau/Khó chịu vùng ngực (Chest discomfort)":
        st.write("**Đánh giá các đặc tính cơn đau thắt ngực:**")
        col_ang1, col_ang2 = st.columns(2)
        
        with col_ang1:
            st.markdown("<span class='symptom-tag-inc'>Gợi ý tăng khả năng lâm sàng (Increasing Likelihood)</span>", unsafe_allow_html=True)
            inc_q = st.checkbox("Tính chất: Đau bóp nghẹt, thắt, siết chặt hoặc đè nặng (Strangling, Constricting, Pressure, Heaviness)")
            inc_l = st.checkbox("Vị trí: Sau xương ức, lan ra cánh tay trái, cổ, hàm, vai hoặc vùng liên bả vai (Kích thước nắm tay - Fist-size)")
            inc_d = st.checkbox("Thời gian: Cơn đau ngắn, kéo dài khoảng 5–10 phút")
            inc_tr = st.checkbox("Yếu tố kích gợi: Xuất hiện khi gắng sức thể lực, cảm xúc mạnh; nặng hơn khi trời lạnh hoặc sau ăn")
            inc_re = st.checkbox("Yếu tố giảm đau: Giảm trong vòng 1-5 phút sau khi ngừng gắng sức hoặc đáp ứng nhanh với Nitroglycerin")
        
        with col_ang2:
            st.markdown("<span class='symptom-tag-dec'>Gợi ý giảm khả năng lâm sàng (Decreasing Likelihood)</span>", unsafe_allow_html=True)
            dec_q = st.checkbox("Tính chất: Đau rát bỏng, nhói nhọn như dao đâm, xé rách, hoặc đau âm ỉ kéo dài (Sharp, Tearing, Pleuritic)")
            dec_l = st.checkbox("Vị trí: Đau khu trú tại một điểm rất nhỏ hoặc lệch hoàn toàn sang ngực phải")
            dec_d = st.checkbox("Thời gian: Đau rất thoáng qua vài giây hoặc đau liên tục nhiều giờ/nhiều ngày")
            dec_tr = st.checkbox("Yếu tố kích gợi: Đau xuất hiện khi nghỉ ngơi, khi hít sâu, khi ho hoặc khi ấn chẩn vào thành ngực")
            dec_re = st.checkbox("Yếu tố giảm đau: Giảm sau khi dùng thuốc kháng toan dạ dày (antacids) hoặc uống sữa")
            
        # Winther criteria mapping (0-3 points)
        # 1. Retro/precordial location
        # 2. Provoked by exertion/stress
        # 3. Relieved by rest/nitrates within 5 min
        winther_1 = int(inc_l)
        winther_2 = int(inc_tr)
        winther_3 = int(inc_re)
        symptom_analysis["auto_winther_score"] = winther_1 + winther_2 + winther_3
        
        inc_count = sum([inc_q, inc_l, inc_d, inc_tr, inc_re])
        dec_count = sum([dec_q, dec_l, dec_d, dec_tr, dec_re])
        
        if inc_count > dec_count:
            symptom_analysis["summary_text"] = "👉 Triệu chứng đau ngực có nhiều đặc tính **GỢI Ý TĂNG** khả năng mắc CCS (đau thắt ngực điển hình hoặc không điển hình)."
        elif dec_count > inc_count:
            symptom_analysis["summary_text"] = "👉 Triệu chứng đau ngực có nhiều đặc tính **GỢI Ý GIẢM** khả năng mắc CCS (nghi ngờ đau ngực không do tim)."
        else:
            symptom_analysis["summary_text"] = "👉 Triệu chứng đau ngực có đặc điểm đan xen trung tính, cần đánh giá cẩn thận."
            
    else: # Exertional dyspnoea
        st.write("**Đánh giá đặc tính khó thở:**")
        col_dys1, col_dys2 = st.columns(2)
        with col_dys1:
            st.markdown("<span class='symptom-tag-inc'>Gợi ý tăng khả năng lâm sàng (Increasing Likelihood)</span>", unsafe_allow_html=True)
            inc_dys_q = st.checkbox("Tính chất: Cảm giác hụt hơi, không thở sâu được (Difficulty catching breath)")
            inc_dys_tr = st.checkbox("Yếu tố kích gợi: Chỉ xuất hiện khi gắng sức thể lực")
            inc_dys_re = st.checkbox("Yếu tố giảm: Hết nhanh chóng ngay sau khi ngừng gắng sức")
        with col_dys2:
            st.markdown("<span class='symptom-tag-dec'>Gợi ý giảm khả năng lâm sàng (Decreasing Likelihood)</span>", unsafe_allow_html=True)
            dec_dys_q = st.checkbox("Tính chất: Khó thở ra, thở có tiếng rít/khò khè, ho có đờm")
            dec_dys_tr = st.checkbox("Yếu tố kích gợi: Xuất hiện cả khi nghỉ ngơi hoặc liên quan đến tư thế")
            dec_dys_re = st.checkbox("Yếu tố giảm: Giảm chậm khi nghỉ ngơi hoặc chỉ đỡ sau khi xịt thuốc giãn phế quản")
            
        symptom_analysis["auto_winther_score"] = 2  # Dyspnoea is default 2 points in RF-CL model
        
        inc_dys_count = sum([inc_dys_q, inc_dys_tr, inc_dys_re])
        dec_dys_count = sum([dec_dys_q, dec_dys_tr, dec_dys_re])
        
        if inc_dys_count > dec_dys_count:
            symptom_analysis["summary_text"] = "👉 Triệu chứng khó thở có đặc tính **GỢI Ý TĂNG** khả năng do thiếu máu cơ tim (tương đương đau ngực)."
        else:
            symptom_analysis["summary_text"] = "👉 Triệu chứng khó thở **GỢI Ý GIẢM** khả năng do tim, hướng tới nguyên nhân hô hấp (COPD, hen...)."

    st.info(symptom_analysis["summary_text"])
    st.session_state.symptom_analysis = symptom_analysis

    st.divider()

    # 3. Basic & Selected Patient Testing with input fields for results
    st.subheader("🧪 3. Thăm dò Cận lâm sàng Ban đầu (Basic & Selected Testing) & Nhập Kết quả")
    st.markdown("<p style='font-size: 0.95rem; color: #555;'>Tích chọn các thăm dò đã thực hiện và điền kết quả để hệ thống liên kết dữ liệu tự động sang các bước sau:</p>", unsafe_allow_html=True)
    
    test_col1, test_col2 = st.columns(2)
    with test_col1:
        st.markdown("**1. Xét nghiệm thường quy bắt buộc (Cho mọi bệnh nhân - Class I):**")
        
        # Resting ECG
        done_ecg = st.checkbox("Điện tâm đồ 12 chuyển đạo lúc nghỉ (Resting ECG)", value=True)
        if done_ecg:
            ecg_res = st.radio("Kết quả ECG lúc nghỉ:", 
                               ["Bình thường (Normal)", 
                                "Bất thường (Sóng Q bệnh lý, ST-T thay đổi động học, LBBB...)"])
            st.session_state.ecg_abnormal = (ecg_res != "Bình thường (Normal)")
            if st.session_state.ecg_abnormal:
                st.markdown("<span class='class-badge-1'>Class I</span> *Có sóng Q bệnh lý hoặc ST-T bất thường sẽ tự động cộng điểm điều chỉnh khả năng lâm sàng ở Bước 2.*", unsafe_allow_html=True)
        
        # Biochemistry
        done_biochem = st.checkbox("Xét nghiệm Hóa sinh máu cơ bản (Biochemistry)")
        if done_biochem:
            st.info("Nhập các chỉ số hóa sinh máu của bệnh nhân:")
            
            # Unit selector
            st.session_state.lipid_unit = st.radio("Đơn vị đo Lipid máu:", ["mmol/L", "mg/dL"], horizontal=True)
            
            bio_col1, bio_col2 = st.columns(2)
            with bio_col1:
                # LDL-C Input
                if st.session_state.lipid_unit == "mmol/L":
                    ldlc = st.number_input("LDL-Cholesterol", min_value=0.1, max_value=15.0, value=st.session_state.ldlc_val_mmol, step=0.1)
                    st.session_state.ldlc_val_mmol = ldlc
                else:
                    ldlc_mg = st.number_input("LDL-Cholesterol (mg/dL)", min_value=4.0, max_value=600.0, value=float(st.session_state.ldlc_val_mmol * 38.67), step=5.0)
                    st.session_state.ldlc_val_mmol = ldlc_mg / 38.67
                
                # Triglyceride Input
                if st.session_state.lipid_unit == "mmol/L":
                    tg = st.number_input("Triglycerides", min_value=0.1, max_value=30.0, value=st.session_state.tg_val_mmol, step=0.1)
                    st.session_state.tg_val_mmol = tg
                else:
                    tg_mg = st.number_input("Triglycerides (mg/dL)", min_value=10.0, max_value=2500.0, value=float(st.session_state.tg_val_mmol * 88.57), step=10.0)
                    st.session_state.tg_val_mmol = tg_mg / 88.57

                st.session_state.lpa_val = st.number_input("Lipoprotein(a) - nmol/L (nếu có, nhập 0 nếu chưa làm)", min_value=0, max_value=500, value=0)
            
            with bio_col2:
                st.session_state.hba1c_val = st.number_input("HbA1c (%)", min_value=3.0, max_value=20.0, value=5.8, step=0.1)
                st.session_state.egfr_val = st.number_input("Mức lọc cầu thận eGFR (mL/min/1.73m²)", min_value=5, max_value=150, value=st.session_state.egfr_val)
                
                # Auto-detect risk flags from lab values
                st.session_state.diabetes_flag = (st.session_state.hba1c_val >= 6.5)
                st.session_state.dyslipidemia_flag = (st.session_state.ldlc_val_mmol >= 3.0 or st.session_state.tg_val_mmol >= 1.7)
                
                # Feedback notifications
                if st.session_state.diabetes_flag:
                    st.warning("⚠️ Phát hiện HbA1c ≥ 6.5%: Tự động kích hoạt Đái tháo đường ở yếu tố nguy cơ (Bước 2).")
                if st.session_state.egfr_val < 60:
                    st.error(f"⚠️ eGFR giảm ({st.session_state.egfr_val}): Bệnh nhân có suy thận mạn kèm theo.")

    with test_col2:
        st.markdown("**2. Thăm dò bổ sung cho các đối tượng chọn lọc (Selected Patients):**")
        
        # Chest X-ray
        done_cxr = st.checkbox("Chụp X-quang ngực thẳng (Chest X-ray)")
        if done_cxr:
            cxr_res = st.multiselect("Bất thường trên Chest X-ray (Class IIa C):", 
                                     ["Bóng tim to (Cardiomegaly)", 
                                      "Sung huyết phổi (Pulmonary congestion)", 
                                      "Tràn dịch màng phổi (Pleural effusion)"])
            st.session_state.cxr_abnormal = len(cxr_res) > 0
            if st.session_state.cxr_abnormal:
                st.warning("⚠️ Phát hiện bất thường trên X-quang ngực: Gợi ý suy tim hoặc bệnh lý phổi đi kèm.")
                
        # PFT
        done_pft = st.checkbox("Đo chức năng hô hấp (Pulmonary Function Test - PFT)")
        if done_pft:
            pft_res = st.radio("Kết quả PFT (Class I C cho bệnh nhân Khó thở):",
                               ["Bình thường (Normal)", 
                                "Rối loạn thông khí tắc nghẽn (Obstructive - COPD/Hen)", 
                                "Rối loạn thông khí hạn chế (Restrictive)"])
            st.session_state.pft_abnormal = (pft_res != "Bình thường (Normal)")
            if st.session_state.pft_abnormal:
                st.info(f"👉 Kết quả PFT: {pft_res}. Cần lưu ý tối ưu hóa thuốc hô hấp đồng hành.")

    # Proceed Button
    st.write("")
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
            echo_findings = st.multiselect("Phát hiện bất thường trên siêu âm tim lúc nghỉ:", [
                "Rối loạn vận động vùng cơ tim thất trái (Regional wall motion abnormality)",
                "Bệnh van tim kèm theo (Hẹp/hở van mức độ vừa-nặng)",
                "Phì đại thất trái (LV Hypertrophy)",
                "Rối loạn chức năng tâm trương thất trái"
            ])
            
        lvd_flag = (lvef <= 40 or "Rối loạn vận động vùng cơ tim thất trái (Regional wall motion abnormality)" in echo_findings)
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
            
            # Map symptom score dynamically from Step 1 if available
            symptom_type_step1 = st.session_state.symptom_analysis["type"] if "symptom_analysis" in st.session_state else "Đau/Khó chịu vùng ngực (Chest discomfort)"
            
            s_type_index = 0 if symptom_type_step1 == "Đau/Khó chịu vùng ngực (Chest discomfort)" else 1
            symptom_type = st.radio("Kiểu triệu chứng chính để tính RF-CL:", 
                                    ["Cơn đau thắt ngực (Chest Pain)", "Khó thở khi gắng sức (Exertional Dyspnoea)"],
                                    index=s_type_index)
            
            if symptom_type == "Cơn đau thắt ngực (Chest Pain)":
                default_score = st.session_state.symptom_analysis["auto_winther_score"] if "symptom_analysis" in st.session_state else 1
                symptom_score = st.slider("Điểm triệu chứng Đau ngực (Winther score 0-3):", min_value=0, max_value=3, value=default_score)
                st.caption("*Lưu ý: 1 điểm cho mỗi đặc tính: Đau sau xương ức | Khởi phát khi gắng sức/stress | Giảm khi nghỉ/dùng Nitrates trong 5p.*")
            else:
                symptom_score = 2
                st.write("👉 Triệu chứng khó thở được mặc định quy đổi thành **2 điểm** trong mô hình RF-CL.")

        with calc_col2:
            st.markdown("**Các yếu tố nguy cơ tim mạch đi kèm (0-5):**")
            
            # Auto-link risk factors from Step 1 biochem
            default_diabetes = st.session_state.diabetes_flag
            default_dyslip = st.session_state.dyslipidemia_flag
            
            rf_family = st.checkbox("Tiền sử gia đình mắc bệnh mạch vành sớm (Nam <55, Nữ <65)")
            rf_smoking = st.checkbox("Đang hút thuốc lá hoặc có tiền sử hút thuốc")
            rf_dyslipidemia = st.checkbox("Rối loạn lipid máu", value=default_dyslip)
            rf_hypertension = st.checkbox("Tăng huyết áp", value=st.session_state.hypertension_flag)
            rf_diabetes = st.checkbox("Đái tháo đường", value=default_diabetes)
            
            rf_count = int(rf_family) + int(rf_smoking) + int(rf_dyslipidemia) + int(rf_hypertension) + int(rf_diabetes)
            
            if rf_count <= 1:
                rf_category = "0-1"
            elif rf_count <= 3:
                rf_category = "2-3"
            else:
                rf_category = "4-5"
                
            st.write(f"👉 Số lượng yếu tố nguy cơ mạch vành: **{rf_count}/5** (Nhóm nguy cơ: {rf_category})")

        # RF-CL Matrix Lookup Table (Figure 4)
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

        # Lookup key string formulation
        score_key = "0-1" if symptom_score <= 1 else str(symptom_score)
        base_likelihood = rf_cl_matrix[gender][age_group][score_key][rf_category]
        
        # Color helper
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
            <p style='font-size: 1.6rem; margin: 10px 0 5px 0; font-weight: bold;'>Khả năng lâm sàng mắc bệnh mạch vành tắc nghẽn: <span style='color: {base_color};'>{base_likelihood}%</span></p>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # Section C: Adjustments (Figure 5) - Smart linked
        st.subheader("3. Điều chỉnh và Phân tầng lại Khả năng lâm sàng (Adjust Clinical Likelihood)")
        st.markdown("<p style='font-size: 0.95rem; color: #555;'>Cá thể hóa và phân tầng lại nguy cơ dựa trên các thông số cận lâm sàng chi tiết khác (Figure 5):</p>", unsafe_allow_html=True)
        
        adj_col1, adj_col2 = st.columns(2)
        with adj_col1:
            st.write("**Yếu tố lâm sàng và điện sinh lý (Class I):**")
            
            # Auto-checked from Step 1 results
            ecg_adj_default = st.session_state.ecg_abnormal
            lvd_adj_default = lvd_flag
            pad_adj_default = ("Bệnh động mạch ngoại biên (PAD)" in st.session_state.get('comorbidities_val', []))
            
            adj_ecg = st.checkbox("ECG lúc nghỉ: Sóng Q bệnh lý hoặc thay đổi ST-T bất thường", value=ecg_adj_default)
            adj_lvd = st.checkbox("Siêu âm tim: Giảm chức năng co bóp hoặc rối loạn vận động vùng LV", value=lvd_adj_default)
            adj_pad = st.checkbox("Có tiền sử bệnh động mạch ngoại biên (PAD)", value=pad_adj_default)
            adj_calc = st.checkbox("X-quang ngực/CT phổi: Phát hiện vôi hóa mạch vành từ trước")
            adj_ex_ecg = st.checkbox("Exercise ECG: Nghiệm pháp gắng sức điện tâm đồ dương tính/bất thường")
        
        with adj_col2:
            st.write("**Phân tầng lại bằng Điểm vôi hóa mạch vành (CACS - Class IIa):**")
            cacs_available = st.radio("Bệnh nhân đã có kết quả CACS chưa?", ["Chưa thực hiện", "Đã có kết quả"])
            
            cacs_feedback = ""
            cacs_modifier = 0
            cacs_override_flag = False
            
            if cacs_available == "Đã có kết quả":
                cacs_val = st.number_input("Nhập điểm vôi hóa mạch vành (CACS Agatston score):", min_value=0, max_value=5000, value=0, step=10)
                
                if cacs_val == 0:
                    cacs_override_flag = True
                    cacs_feedback = """
                    <div class='success-box' style='padding: 10px; margin-top: 5px;'>
                        <span class='class-badge-2a'>Class IIa</span> <strong>CACS = 0:</strong> Khả năng mạch vành tắc nghẽn cực kỳ thấp.<br>
                        👉 <strong>Hành động:</strong> Phân tầng lại lâm sàng về nhóm <strong>Rất Thấp (≤5%)</strong>. Cân nhắc trì hoãn các thăm dò gắng sức không xâm lấn nếu không đau ngực quá điển hình.
                    </div>
                    """
                elif 1 <= cacs_val < 10:
                    cacs_modifier = -5
                    cacs_feedback = "<div class='info-box' style='padding:10px;'>CACS 1-9: Vôi hóa mạch vành mức tối thiểu. Ít làm thay đổi khả năng lâm sàng nền.</div>"
                elif 10 <= cacs_val < 100:
                    cacs_modifier = 0
                    cacs_feedback = "<div class='info-box' style='padding:10px;'>CACS 10-99: Vôi hóa nhẹ. Chụp CCTA là thăm dò chẩn đoán ưu tiên hàng đầu.</div>"
                elif 100 <= cacs_val < 400:
                    cacs_modifier = 10
                    cacs_feedback = "<div class='info-box' style='padding:10px;'>CACS 100-399: Vôi hóa mức độ vừa. Khả năng lâm sàng tăng nhẹ (+10%). CCTA vẫn phù hợp.</div>"
                elif 400 <= cacs_val < 1000:
                    cacs_override_flag = True
                    cacs_override_val = max(base_likelihood, 65) # Elevate to High
                    cacs_feedback = """
                    <div class='warning-box' style='padding: 10px; margin-top: 5px; border-left-color: #fd7e14;'>
                        <span class='class-badge-2a'>Class IIa</span> <strong>CACS 400-999 (Vôi hóa nặng):</strong><br>
                        - Khả năng lâm sàng tăng lên mức **Cao (High)**.<br>
                        - Do vôi hóa nhiều gây xảo ảnh (calcium blooming), CCTA sẽ giảm độ đặc hiệu rõ rệt. Khuyến cáo **ưu tiên lựa chọn Thăm dò chức năng gắng sức** (Stress Echo/CMR/SPECT/PET) hơn là CCTA.
                    </div>
                    """
                else: # >= 1000
                    cacs_override_flag = True
                    cacs_override_val = 90 # Elevate to Very High
                    cacs_feedback = """
                    <div class='warning-box' style='padding: 10px; margin-top: 5px; border-left-color: #dc3545;'>
                        <span class='class-badge-2a'>Class IIa</span> <strong>CACS ≥ 1000 (Vôi hóa cực nặng):</strong><br>
                        - Khả năng lâm sàng mạch vành tắc nghẽn là **Rất Cao (>85%)**.<br>
                        - Chống chỉ định tương đối chụp CCTA chẩn đoán do xảo ảnh vôi hóa quá nặng. Khuyến cáo **ưu tiên Thăm dò hình ảnh chức năng gắng sức** hoặc cân nhắc chuyển chụp mạch vành xâm lấn (ICA) trực tiếp.
                    </div>
                    """
                st.markdown(cacs_feedback, unsafe_allow_html=True)

        # Dynamic re-calculation of Adjusted Likelihood
        adjusted_likelihood = base_likelihood
        
        # Base clinical adjustment modifiers
        if adj_ecg or adj_lvd or adj_pad or adj_calc or adj_ex_ecg:
            adjusted_likelihood += 15
            st.info("💡 Điểm khả năng lâm sàng đã được điều chỉnh tăng do phát hiện bất thường lâm sàng/ECG/siêu âm tim.")
        
        # Apply CACS modifications
        if cacs_available == "Đã có kết quả":
            if cacs_override_flag:
                if cacs_val == 0:
                    adjusted_likelihood = 5 # Forced to very low
                elif cacs_val >= 1000:
                    adjusted_likelihood = 90
                else: # 400-999
                    adjusted_likelihood = 65
            else:
                adjusted_likelihood += cacs_modifier
        
        # Cap limits between 0 and 95
        adjusted_likelihood = max(0, min(95, adjusted_likelihood))
        
        def get_class_label(val):
            if val <= 5: return "Rất thấp (Very Low)", "#28a745"
            elif val <= 15: return "Thấp (Low)", "#17a2b8"
            elif val <= 50: return "Trung bình (Moderate)", "#ffc107"
            elif val <= 85: return "Cao (High)", "#fd7e14"
            else: return "Rất cao (Very High)", "#dc3545"

        adj_class_label, adj_color = get_class_label(adjusted_likelihood)
        
        st.markdown(f"""
        <div style='background-color: #f1f2f6; border-radius: 6px; padding: 15px; border-left: 6px solid {adj_color}; margin: 15px 0;'>
            <h4 style='margin: 0; color: #333;'>KẾT QUẢ SAU ĐIỀU CHỈNH LÂM SÀNG (Adjusted Clinical Likelihood):</h4>
            <p style='font-size: 1.6rem; margin: 10px 0 5px 0; font-weight: bold;'>Khả năng lâm sàng thực tế: <span style='color: {adj_color};'>{adjusted_likelihood}%</span></p>
            <p style='margin: 0; font-size: 1.1rem;'>Nhóm phân tầng: <strong style='color: {adj_color};'>{adj_class_label}</strong></p>
        </div>
        """, unsafe_allow_html=True)

        # Step navigation
        st.write("")
        col_prev, col_next = st.columns(2)
        with col_prev:
            if st.button("⬅️ Quay lại Bước 1"):
                set_step(1)
        with col_next:
            if st.button("Xác nhận & Sang Bước 3 ➡️"):
                st.session_state.likelihood_value = adjusted_likelihood
                st.session_state.cacs_score_val = cacs_val if cacs_available == "Đã có kết quả" else -1
                set_step(3)

# ----------------------------------------------------
# STEP 3: DIAGNOSIS SELECTION, RISK STRATIFICATION & ANOCA/INOCA FLOW
# ----------------------------------------------------
step3_expanded = (st.session_state.step == 3)
with st.expander("🔍 BƯỚC 3: XÁC ĐỊNH CHẨN ĐOÁN, PHÂN TẦNG NGUY CƠ BIẾN CỐ & ANOCA/INOCA", expanded=step3_expanded):
    if st.session_state.step < 3:
        st.warning("Vui lòng hoàn thành Bước 2 trước.")
    else:
        st.markdown("<div class='step-header'>BƯỚC 3: Lựa chọn kỹ thuật chẩn đoán phù hợp, Phân tầng nguy cơ & Quản lý ANOCA/INOCA</div>", unsafe_allow_html=True)
        
        lik = st.session_state.get('likelihood_value', 20)
        cacs_score = st.session_state.get('cacs_score_val', -1)
        st.markdown(f"Khả năng lâm sàng hiện tại sau điều chỉnh: **{lik}%**")
        
        # 1. First-line Diagnostic Test Selection
        st.subheader("1. Khuyến cáo Lựa chọn Thăm dò Chẩn đoán Đầu tay")
        
        if lik <= 5:
            st.success("""
            **🟢 KHUYẾN CÁO: HOÃN CÁC THĂM DÒ CHẨN ĐOÁN SÂU HƠN (Deferral of testing) <span class='class-badge-2a'>Class IIa</span>**
            - Bệnh nhân có khả năng lâm sàng rất thấp (≤5%). Việc tầm soát mạch vành thường quy không mang lại lợi ích.
            - Tập trung tìm kiếm các nguyên nhân đau ngực ngoài tim khác (như dạ dày - thực quản, cơ xương khớp, thần kinh liên sườn).
            """)
        elif 5 < lik <= 15:
            st.info("""
            **🔵 KHUYẾN CÁO: CHỤP CẮT LỚP VI TÍNH ĐỘNG MẠCH VÀNH (CCTA) LÀ CHỈ ĐỊNH ĐẦU TAY <span class='class-badge-1'>Class I</span>**
            - Phù hợp nhất để chẩn đoán xác định và loại trừ bệnh động mạch vành tắc nghẽn ở những người có khả năng lâm sàng thấp.
            - CCTA có độ nhạy rất cao, giúp loại trừ hẹp lòng mạch và đánh giá gánh nặng xơ vữa mạch vành (atherosclerotic plaque).
            """)
        elif 15 < lik <= 50:
            if cacs_score >= 400:
                st.warning("""
                **🟡 KHUYẾN CÁO: THĂM DÒ HÌNH ẢNH CHỨC NĂNG GẮNG SỨC LÀ ƯU TIÊN <span class='class-badge-2a'>Class IIa</span>**
                - Mặc dù khả năng lâm sàng ở mức trung bình (15-50%) phù hợp với cả CCTA và Hình ảnh chức năng, nhưng do bệnh nhân có **CACS ≥ 400 (Vôi hóa nặng)**, độ đặc hiệu của CCTA sẽ giảm mạnh do xảo ảnh.
                - Khuyên dùng: **Stress Echo, Stress CMR, PET hoặc stress SPECT** để đánh giá trực tiếp tình trạng thiếu máu cơ tim.
                """)
            else:
                st.warning("""
                **🟡 KHUYẾN CÁO: CHỌN CCTA (Class I A) HOẶC THĂM DÒ HÌNH ẢNH CHỨC NĂNG GẮNG SỨC (Class I B)**
                - Bệnh nhân ở nhóm trung bình (15-50%) có thể lựa chọn một trong hai chiến lược:
                    - **CCTA (Cắt lớp vi tính):** Ưu tiên nếu muốn loại trừ hẹp, bệnh nhân trẻ tuổi, vôi hóa ít, cần xem cấu trúc mảng xơ vữa.
                    - **Hình ảnh chức năng gắng sức (Stress Echo, Stress CMR, SPECT/PET):** Ưu tiên nếu nghi ngờ thiếu máu cơ tim diện rộng có ý nghĩa sinh lý, hoặc đã có tiền sử mạch vành.
                """)
        elif 50 < lik <= 85:
            st.error("""
            **🟠 KHUYẾN CÁO: ƯU TIÊN THĂM DÒ HÌNH ẢNH CHỨC NĂNG GẮNG SỨC <span class='class-badge-1'>Class I</span>**
            - Bệnh nhân có khả năng lâm sàng cao (>50%), nguy cơ vôi hóa mạch vành lớn. CCTA giảm giá trị chẩn đoán xác định do xảo ảnh.
            - Chỉ định: **Stress Echo, Stress CMR, SPECT hoặc PET** để chẩn đoán thiếu máu cơ tim và đánh giá diện tích vùng thiếu máu.
            """)
        else: # > 85%
            st.error("""
            **🔴 KHUYẾN CÁO: CHỤP ĐỘNG MẠCH VÀNH XÂM LẤN (ICA) TRỰC TIẾP <span class='class-badge-1'>Class I</span>**
            - Bệnh nhân có khả năng lâm sàng rất cao (>85%), triệu chứng đau ngực nặng nề khó kiểm soát bằng thuốc, hoặc suy tim rõ.
            - ICA nên được thực hiện trực tiếp để chẩn đoán và chuẩn bị kế hoạch tái thông mạch vành đồng thời (kèm đo FFR/iFR nếu có hẹp ranh giới).
            """)

        st.divider()

        # 2. Event-Risk Stratification
        st.subheader("2. Đánh giá Nguy cơ Biến cố Tim mạch Tương lai (Event-Risk Stratification)")
        st.markdown("<p style='font-size: 0.95rem; color: #555;'>Xác định xem bệnh nhân có thuộc nhóm nguy cơ cao xảy ra biến cố tim mạch bất lợi (MACE) - Khuyến cáo <span class='class-badge-1'>Class I B</span>:</p>", unsafe_allow_html=True)
        
        risk_col1, risk_col2 = st.columns(2)
        with risk_col1:
            st.markdown("**Các tiêu chuẩn về cấu trúc giải phẫu (Anatomical):**")
            high_risk_anatomy = st.checkbox("CCTA/ICA: Tổn thương Thân chung Động mạch vành trái (Left Main) hẹp ≥ 50%")
            high_risk_anatomy_2 = st.checkbox("CCTA/ICA: Hẹp nặng ≥ 70% ở cả 3 nhánh mạch vành (Three-vessel disease)")
            high_risk_anatomy_3 = st.checkbox("CCTA/ICA: Hẹp đoạn gần động mạch liên thất trước (Proximal LAD) ≥ 70%")
        
        with risk_col2:
            st.markdown("**Các tiêu chuẩn về chức năng thiếu máu (Functional):**")
            high_risk_functional = st.checkbox("Stress Echo: ≥ 3/16 phân vùng cơ tim bị giảm động hoặc vô động do gắng sức")
            high_risk_functional_2 = st.checkbox("Stress CMR: ≥ 2/16 phân vùng thiếu máu cơ tim diện rộng")
            high_risk_functional_3 = st.checkbox("Stress SPECT/PET: Diện tích thiếu máu cơ tim ≥ 10% cơ thất trái")
            high_risk_functional_4 = st.checkbox("Exercise ECG: Điểm số gắng sức Duke (Duke Treadmill Score) < -10")

        is_high_risk = (high_risk_anatomy or high_risk_anatomy_2 or high_risk_anatomy_3 or 
                        high_risk_functional or high_risk_functional_2 or high_risk_functional_3 or high_risk_functional_4)

        if is_high_risk:
            st.error("""
            **🚨 BỆNH NHÂN THUỘC NHÓM NGUY CƠ BIẾN CỐ CAO (HIGH EVENT-RISK) - Khuyến cáo Class I B:**
            - Khuyến cáo thực hiện chụp mạch vành xâm lấn (ICA) - phối hợp đo FFR/iFR nếu cần - để lập kế hoạch tái thông mạch vành sớm nhằm cải thiện triệu chứng và tiên lượng sống còn.
            """)
        else:
            st.info("💡 Bệnh nhân chưa phát hiện các tiêu chuẩn nguy cơ biến cố cao diện rộng trên thăm dò hình ảnh. Ưu tiên điều trị thuốc tối ưu (GDMT).")

        st.divider()

        # 3. ANOCA/INOCA Diagnostic Section (New!)
        st.subheader("🧩 3. Định hướng Quản lý ANOCA/INOCA (Khi không có Hẹp Mạch Vành Tắc Nghẽn)")
        st.markdown("<p style='font-size: 0.95rem; color: #555;'>Áp dụng khi kết quả thăm dò hình ảnh chẩn đoán loại trừ bệnh động mạch vành tắc nghẽn (Obstructive CAD), nhưng triệu chứng vẫn dai dẳng:</p>", unsafe_allow_html=True)
        
        has_obstructive_cad = st.radio("Kết quả chẩn đoán hình ảnh (CCTA hoặc ICA):", 
                                       ["Chưa có kết quả / Có hẹp động mạch vành tắc nghẽn (≥50% Thân chung, hoặc ≥70% nhánh lớn)",
                                        "LOẠI TRỪ hẹp động mạch vành tắc nghẽn (Không hẹp hoặc hẹp nhẹ-vừa <50% thân chung, <70% các nhánh chính)"])
        
        st.session_state.anoca_suspected = False
        if has_obstructive_cad == "LOẠI TRỪ hẹp động mạch vành tắc nghẽn (Không hẹp hoặc hẹp nhẹ-vừa <50% thân chung, <70% các nhánh chính)":
            st.session_state.anoca_suspected = True
            st.markdown("""
            <div class='warning-box' style='border-left-color: #f1c40f; background-color: #fefdf3;'>
                <h4 style='color: #d4ac0d; margin-top: 0;'>🧩 NGHI NGỜ CAO MẮC ANOCA / INOCA (Cơn đau thắt ngực/Thiếu máu cơ tim không do tắc nghẽn)</h4>
                <p>Bệnh nhân vẫn có triệu chứng đau ngực/khó thở dai dẳng nhưng giải phẫu mạch vành bình thường hoặc chỉ hẹp nhẹ. Hướng dẫn ESC 2024 khuyến nghị:</p>
                <ul>
                    <li><strong>Đo chức năng mạch vành xâm lấn (Invasive Coronary Function Testing - ICFT):</strong> Khuyến cáo thực hiện để xác định cơ chế bệnh sinh (Class I B cho bệnh nhân có triệu chứng hạn chế dai dẳng).</li>
                    <li><strong>Phép thử chức năng vi tuần hoàn (Coronary Microvascular Function):</strong> Đo CFR (Coronary Flow Reserve) và IMR/HMR (Microcirculatory Resistance).</li>
                    <li><strong>Nghiệm pháp kích thích co thắt mạch (Acetylcholine Spasm Provocation):</strong> Xác định co thắt mạch vành thượng tâm mạc hoặc vi tuần hoàn.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Interactive endotype identification
            st.write("**Xác định kiểu hình (Endotypes) của ANOCA/INOCA dựa trên thăm dò chức năng mạch vành:**")
            endo_col1, endo_col2 = st.columns(2)
            with endo_col1:
                icft_cfr = st.selectbox("1. Lưu lượng dự trữ mạch vành (CFR):", ["Bình thường (CFR ≥ 2.0)", "Giảm (CFR < 2.0)"])
                icft_imr = st.selectbox("2. Chỉ số kháng vi tuần hoàn (IMR/HMR):", ["Bình thường (IMR < 25 / HMR < 1.9)", "Tăng (IMR ≥ 25 / HMR ≥ 1.9)"])
            with endo_col2:
                icft_spasm = st.selectbox("3. Nghiệm pháp kích thích Acetylcholine (ACh):", 
                                          ["Âm tính", 
                                           "Dương tính co thắt thượng tâm mạc (Hẹp đường kính mạch vành ≥ 90% kèm tái phát đau ngực và ST thay đổi)", 
                                           "Dương tính co thắt vi mạch (ST thay đổi và tái phát đau ngực nhưng không co thắt mạch lớn)"])
            
            # Formulating Endotype Conclusion
            st.session_state.anoca_endotype = "Chưa phân loại"
            if icft_cfr == "Giảm (CFR < 2.0)" or icft_imr == "Tăng (IMR ≥ 25 / HMR ≥ 1.9)":
                if icft_spasm == "Âm tính":
                    st.session_state.anoca_endotype = "Đau thắt ngực vi mạch (Microvascular Angina - MVA)"
                else:
                    st.session_state.anoca_endotype = "Kiểu hình hỗn hợp (Mixed MVA + Vasospastic)"
            elif icft_spasm != "Âm tính":
                st.session_state.anoca_endotype = "Co thắt mạch vành (Vasospastic Angina - VSA)"
            else:
                st.session_state.anoca_endotype = "Đau ngực không do tim (Non-cardiac Chest Pain)"
                
            st.success(f"🎯 **Kiểu hình ANOCA/INOCA xác định:** `{st.session_state.anoca_endotype}`. *Phác đồ điều trị cá thể hóa tương ứng đã được kích hoạt tại Bước 4.*")

        # Step navigation
        st.write("")
        col_prev, col_next = st.columns(2)
        with col_prev:
            if st.button("⬅️ Quay lại Bước 2"):
                set_step(2)
        with col_next:
            if st.button("Xác nhận & Sang Bước 4 ➡️"):
                st.session_state.high_risk_flag = is_high_risk
                set_step(4)

# ----------------------------------------------------
# STEP 4: OPTIMAL TREATMENT (GDMT, LIPID OPTIMIZER & REVAS)
# ----------------------------------------------------
step4_expanded = (st.session_state.step == 4)
with st.expander("💊 BƯỚC 4: CHIẾN LƯỢC ĐIỀU TRỊ TỐI ƯU (GDMT & Revascularization)", expanded=step4_expanded):
    if st.session_state.step < 4:
        st.warning("Vui lòng hoàn thành Bước 3 trước.")
    else:
        st.markdown("<div class='step-header'>BƯỚC 4: Thiết lập chế độ điều trị nội khoa tối ưu (GDMT) & Cân nhắc Tái thông mạch vành</div>", unsafe_allow_html=True)
        
        # Split into three tabs: GDMT general, Lipid Optimizer, and Revasc/ANOCA
        tab_med, tab_lipid, tab_revasc = st.tabs([
            "💊 Điều trị nội khoa tối ưu (GDMT)", 
            "🩸 TỐI ƯU HÓA LIPID MÁU CHUYÊN SÂU", 
            "🩺 Chỉ định Can thiệp / ANOCA-INOCA"
        ])
        
        with tab_med:
            st.subheader("1. Thay đổi lối sống và Kiểm soát các yếu tố nguy cơ (Class I)")
            st.markdown("""
            *   **Bỏ hoàn toàn thuốc lá:** Hỗ trợ tư vấn cai thuốc, tránh phơi nhiễm khói thuốc lá thụ động (Class I A).
            *   **Chế độ ăn Địa Trung Hải (Mediterranean Diet):** Hạn chế chất béo bão hòa < 10% tổng năng lượng, tăng cường rau quả, ngũ cốc nguyên hạt. Hạn chế rượu bia (<100g/tuần).
            *   **Hoạt động thể lực:** Tập luyện thể dục cường độ trung bình 30-60 phút ít nhất 5 ngày/tuần. Giảm thời gian ngồi tĩnh tại.
            *   **Kiểm soát cân nặng:** Đưa cân nặng về mức BMI mục tiêu (18.5 - 24.9 kg/m2).
            """)
            
            st.subheader("2. Thuốc bảo vệ mạch vành và Cải thiện tiên lượng (Class I)")
            st.markdown("""
            *   **Kháng kết tập tiểu cầu (Antiplatelets):** 
                *   *Aspirin 75-100 mg/ngày* hoặc *Clopidogrel 75 mg/ngày* được khuyến cáo lâu dài ở bệnh nhân có bệnh mạch vành tắc nghẽn (Class I A).
            *   **Kiểm soát huyết áp:** Mục tiêu **120-129 / 70-79 mmHg** nếu dung nạp tốt (Class I A, ưu tiên ACEi hoặc ARB).
            *   **Bệnh nhân Đái tháo đường đi kèm:** Bắt buộc sử dụng thuốc **ức chế SGLT2 (SGLT2i)** và/hoặc **đồng vận thụ thể GLP-1 (GLP-1 RA)** để giảm nguy cơ tử vong do tim mạch và nhồi máu cơ tim (Class I A).
            """)
            
            st.subheader("3. Thuốc giảm triệu chứng đau thắt ngực (Antianginal - Anti-ischemic)")
            st.markdown("""
            *   **Lựa chọn đầu tay (First-line):** Thuốc **Chẹn beta (Beta-blockers)** và/hoặc **Chẹn kênh Canxi (CCBs)** để kiểm soát tần số tim và giảm đau ngực (Class I A).
            *   **Cắt cơn đau ngực cấp:** Luôn luôn kê đơn Nitroglycerin dạng xịt hoặc ngậm dưới lưỡi cho bệnh nhân mang theo người (Class I B).
            """)
            
        with tab_lipid:
            st.subheader("🩸 PHÂN TÍCH VÀ ĐIỀU CHỈNH LIPID MÁU THEO TIÊU CHUẨN ESC 2024")
            
            # Pull LDL-C from Step 1 or show manual input
            ldlc_now = st.session_state.get('ldlc_val_mmol', 3.0)
            tg_now = st.session_state.get('tg_val_mmol', 1.8)
            lpa_now = st.session_state.get('lpa_val', 0)
            
            unit_active = st.session_state.get('lipid_unit', "mmol/L")
            
            st.info(f"Dữ liệu nhập từ Bước 1: LDL-C = **{ldlc_now:.2f} mmol/L** ({ldlc_now*38.67:.1f} mg/dL) | Triglycerides = **{tg_now:.2f} mmol/L** ({tg_now*88.57:.1f} mg/dL)")
            
            # Cardiovascular Risk Classification
            st.markdown("""
            <div class='recommendation-box' style='padding: 10px; margin-bottom: 15px;'>
                <strong>PHÂN LOẠI NGUY CƠ TIM MẠCH:</strong> Bệnh nhân đã xác định xơ vữa mạch vành (CCS) mặc định thuộc nhóm <strong>Nguy cơ Tim mạch Rực kỳ Cao (Very High CV Risk)</strong>.
            </div>
            """, unsafe_allow_html=True)
            
            # Check for recurrent ASCVD events within 2 years
            recurrent_event = st.checkbox("Bệnh nhân có biến cố xơ vữa tái phát (nhồi máu cơ tim, đột quỵ...) trong vòng 2 năm qua khi đang dùng Statin liều tối đa?")
            
            # Determine Target
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
            
            # Interactive Lipid Treatment Escalation Flow
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
            
            # Diagnostic & Therapy algorithm based on LDL-C target gap
            is_at_target = ldlc_now < target_ldlc_mmol
            
            if is_at_target:
                st.success(f"🎉 **Chúc mừng!** Bệnh nhân đã đạt mục tiêu LDL-C (< {target_ldlc_mmol} mmol/L). Khuyên dùng duy trì phác đồ hiện tại và xét nghiệm kiểm tra định kỳ mỗi 6-12 tháng.")
            else:
                st.error(f"❌ **Chưa đạt mục tiêu!** LDL-C hiện tại ({ldlc_now:.2f} mmol/L) cao hơn mục tiêu (< {target_ldlc_mmol} mmol/L).")
                
                # Stepwise recommendation logic
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
                    1. <span class='class-badge-1'>Class I B</span> Phối hợp thêm **Ezetimibe 10mg** hàng ngày ngay lập tức. (Phối hợp Statin tối đa + Ezetimibe giúp giảm thêm khoảng 15-20% LDL-C).
                    2. Kiểm tra lại sau 4-6 tuần để đánh giá tính dung nạp và mục tiêu đạt được.
                    """, unsafe_allow_html=True)
                    
                elif current_therapy == "Đang dùng phối hợp Statin tối đa + Ezetimibe 10mg":
                    st.markdown(f"""
                    1. <span class='class-badge-1'>Class I A</span> Phối hợp thêm thuốc **ức chế PCSK9 (PCSK9 inhibitor)** (như Alirocumab, Evolocumab hoặc Inclisiran).
                    2. <span class='class-badge-2a'>Class IIa C</span> Hoặc cân nhắc phối hợp thêm **Bempedoic acid** 180mg hàng ngày.
                    """, unsafe_allow_html=True)
                    
                elif current_therapy == "Đang dùng phối hợp 3 thuốc (Statin tối đa + Ezetimibe + Ức chế PCSK9)":
                    st.markdown(f"""
                    1. Bệnh nhân đã tối đa hóa các phác đồ hạ lipid chuẩn mà vẫn chưa đạt mục tiêu. Cân nhắc phối hợp thêm **Bempedoic acid** hoặc **chuyển đổi/tăng cường hoạt lực** của nhóm ức chế PCSK9.
                    2. Rà soát nghiêm ngặt sự tuân thủ điều trị của bệnh nhân.
                    """)
                    
                else: # Statin Intolerance
                    st.markdown(f"""
                    1. <span class='class-badge-1'>Class I B</span> Kê đơn **Ezetimibe 10mg** hàng ngày làm điều trị đầu tay.
                    2. <span class='class-badge-1'>Class I B</span> Phối hợp thêm **Bempedoic acid** nếu Ezetimibe đơn trị liệu không đạt mục tiêu.
                    3. <span class='class-badge-2a'>Class IIa C</span> Cân nhắc phối hợp thêm thuốc **ức chế PCSK9** nếu chưa kiểm soát được LDL-C.
                    """, unsafe_allow_html=True)

            # Triglycerides (TG) Management Section
            st.markdown("#### 📈 Quản lý Triglyceride tăng cao")
            if tg_now >= 1.7:
                st.warning(f"Chỉ số Triglyceride hiện tại: **{tg_now:.2f} mmol/L** (tăng nhẹ đến vừa).")
                if 1.52 <= tg_now <= 5.63:
                    st.markdown(f"""
                    *   <span class='class-badge-2a'>Class IIa B</span> Khuyến cáo cân nhắc bổ sung **Icosapent Ethyl (2 x 2g/ngày)** phối hợp cùng Statin để giảm thiểu nguy cơ biến cố tim mạch tồn dư.
                    *   *Lưu ý:* Fibrates (như Fenofibrate) không được ưu tiên hàng đầu để giảm nguy cơ tim mạch ở bệnh nhân CCS trừ khi TG tăng quá cao.
                    """, unsafe_allow_html=True)
                elif tg_now > 5.63:
                    st.markdown(f"""
                    *   ⚠️ **CẢNH BÁO NGUY CƠ VIÊM TỤY CẤP:** Hạn chế mỡ tuyệt đối, kiểm soát đường huyết chặt chẽ.
                    *   Sử dụng **Fenofibrate** phối hợp hoặc **Omega-3 liều cao** để giảm TG khẩn cấp.
                    """)
            else:
                st.success(f"Triglyceride bình thường: {tg_now:.2f} mmol/L (< 1.7 mmol/L).")

            # Lipoprotein(a) risk stratification
            if lpa_now > 50:
                st.error(f"⚠️ **Lp(a) tăng cao: {lpa_now} nmol/L** (> 50 mg/dL hoặc > 105 nmol/L). Đây là yếu tố nguy cơ độc lập do di truyền làm tăng mạnh gánh nặng xơ vữa mạch vành tồn dư, đòi hỏi kiểm soát LDL-C nghiêm ngặt hơn.")
            elif lpa_now > 0:
                st.info(f"Lp(a) trong giới hạn bình thường: {lpa_now} nmol/L.")

        with tab_revasc:
            st.subheader("1. Tiêu chuẩn chỉ định Tái thông mạch vành (Revascularization)")
            
            is_high_risk = st.session_state.get('high_risk_flag', False)
            if is_high_risk:
                st.markdown("""
                <div class='warning-box' style='border-left-color: #fd7e14;'>
                    <h4 style='color: #fd7e14; margin-top: 0;'>👉 CHỈ ĐỊNH TÁI THÔNG MẠCH VÀNH ĐỂ CẢI THIỆN TIÊN LƯỢNG (Class I A)</h4>
                    <p>Do bệnh nhân thuộc nhóm nguy cơ biến cố cao (Hẹp Thân chung trái, 3 nhánh mạch vành, hoặc đoạn gần LAD), can thiệp mạch vành qua da (PCI) hoặc phẫu thuật làm cầu nối chủ-vành (CABG) được chỉ định để kéo dài thời gian sống còn và ngăn ngừa Nhồi máu cơ tim tự phát.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class='info-box'>
                    <strong>Xem xét Tái thông mạch vành để cải thiện triệu chứng (Class I A):</strong><br>
                    Ở những bệnh nhân không thuộc nhóm nguy cơ biến cố cao, chỉ định tái thông mạch vành được đặt ra khi:
                    Triệu chứng đau thắt ngực hoặc khó thở vẫn dai dẳng, ảnh hưởng nặng đến chất lượng cuộc sống mặc dù đã điều trị nội khoa tối ưu (GDMT) với tối thiểu 2 nhóm thuốc kháng đau thắt ngực.
                </div>
                """, unsafe_allow_html=True)

            # 2. ANOCA / INOCA Pharmacological Management (New!)
            if st.session_state.get('anoca_suspected', False):
                st.subheader("2. Điều trị nội khoa cá thể hóa cho ANOCA / INOCA (Figure 15)")
                st.info(f"Phác đồ điều trị được cá thể hóa dựa trên Kiểu hình (Endotype) xác định: **{st.session_state.get('anoca_endotype', 'Chưa phân loại')}**")
                
                endotype_active = st.session_state.get('anoca_endotype', 'Chưa phân loại')
                
                if "Microvascular" in endotype_active or "MVA" in endotype_active:
                    st.markdown("""
                    *   **Thuốc chống đau ngực:** 
                        *   <span class='class-badge-2a'>Class IIa B</span> **Chẹn beta (Beta-blockers)** là lựa chọn đầu tay (như Nebivolol, Bisoprolol).
                        *   <span class='class-badge-2a'>Class IIa B</span> Phối hợp **Chẹn kênh canxi dihydropyridine (DHP-CCBs)** (như Amlodipine) nếu chẹn beta chưa kiểm soát được triệu chứng.
                        *   <span class='class-badge-2b'>Class IIb B</span> Nicorandil hoặc Ranolazine nếu triệu chứng kháng trị.
                    *   **Thuốc bảo vệ mạch vành:** Khuyến cáo sử dụng **ACEi/ARB** và **Statin** để cải thiện chức năng nội mạc vi tuần hoàn (Class IIa B).
                    """, unsafe_allow_html=True)
                elif "Vasospastic" in endotype_active or "VSA" in endotype_active:
                    st.markdown("""
                    *   **Thuốc điều trị đầu tay:** 
                        *   <span class='class-badge-1'>Class I B</span> **Chẹn kênh canxi (CCBs)** liều cao (như Diltiazem, Amlodipine) là nền tảng điều trị quan trọng nhất để ngăn ngừa co thắt mạch.
                        *   <span class='class-badge-2a'>Class IIa B</span> Phối hợp thêm **Nitrates tác dụng kéo dài** nếu CCB đơn trị chưa đủ kiểm soát.
                    *   **🚨 CẢNH BÁO ĐỎ (Class III):** **TRÁNH DÙNG THUỐC CHẸN BETA ĐƠN TRỊ LIỆU** ở bệnh nhân co thắt mạch vành, vì có thể gây hoạt hóa thụ thể alpha-adrenergic dẫn đến co thắt mạch vành trầm trọng hơn.
                    """, unsafe_allow_html=True)
                elif "Mixed" in endotype_active:
                    st.markdown("""
                    *   **Phối hợp điều trị:** 
                        *   Sử dụng **Chẹn kênh canxi (CCBs)** làm chủ đạo do kiểm soát được cả co thắt thượng tâm mạc và cải thiện vi tuần hoàn.
                        *   Có thể cân nhắc phối hợp chẹn beta cẩn thận nếu ưu thế thành phần đau thắt ngực vi mạch rõ rệt.
                    """)
                else:
                    st.markdown("*Chưa xác định kiểu hình ANOCA cụ thể. Vui lòng hoàn thành đánh giá chức năng mạch vành xâm lấn (ICFT) ở Bước 3.*")

        st.write("")
        if st.button("⬅️ Quay lại Bước 3"):
            set_step(3)

st.write("")
st.markdown("<p style='text-align: center; font-size: 0.8rem; color: #888;'>Phát triển chuyên sâu dựa trên Hướng dẫn của Hội Tim mạch Châu Âu (ESC) 2024 về quản lý Hội chứng mạch vành mạn | Thiết kế tương tác từng bước cho nhà lâm sàng</p>", unsafe_allow_html=True)
