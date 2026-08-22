import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="ESC 2024 CCS Initial Management Tool v6",
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

# Custom Styling with Class badges and distinct alerts
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
    }
    .symptom-tag-inc {
        background-color: #fce4d6;
        color: #c55a11;
        padding: 3px 8px;
        border-radius: 3px;
        font-weight: bold;
        font-size: 0.85rem;
    }
    .symptom-tag-dec {
        background-color: #e2efda;
        color: #375623;
        padding: 3px 8px;
        border-radius: 3px;
        font-weight: bold;
        font-size: 0.85rem;
    }
    .class-badge-1 {
        background-color: #2e7d32;
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
st.markdown("<p style='text-align: center; color: #555; font-size: 1.05rem;'>Công cụ lâm sàng tương tác từng bước (Stepwise Approach) tích hợp Bộ Cố vấn kê đơn theo Figure 9 & Quy trình ANOCA/INOCA theo Hướng dẫn ESC 2024</p>", unsafe_allow_html=True)
st.divider()

# Session State Initialization for Step Flow (Option A: Dynamic Expansion)
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'acute_flag' not in st.session_state:
    st.session_state.acute_flag = False
if 'lipid_unit' not in st.session_state:
    st.session_state.lipid_unit = "mmol/L"

# Persistent states for cross-step dynamic linking
if 'hr_val' not in st.session_state:
    st.session_state.hr_val = 75
if 'sbp_val' not in st.session_state:
    st.session_state.sbp_val = 120
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
        
        # Clinical parameters added for Step 4 drug safety (Figure 9)
        st.session_state.sbp_val = st.number_input("Huyết áp tâm thu (mmHg) lúc nghỉ:", min_value=70, max_value=230, value=st.session_state.sbp_val)
        st.session_state.hr_val = st.number_input("Tần số tim (nhịp/phút) lúc nghỉ:", min_value=30, max_value=180, value=st.session_state.hr_val)
        
        # Chest X-ray
        done_cxr = st.checkbox("Chụp X-quang ngực thẳng (Chest X-ray)")
        if done_cxr:
            cxr_status = st.radio("Kết quả Chest X-ray (Class IIa C):", 
                                  ["Chưa ghi nhận bất thường (Bình thường)", "Có bất thường"],
                                  key="cxr_status_radio")
            if cxr_status == "Có bất thường":
                cxr_res = st.multiselect("Bất thường trên Chest X-ray:", 
                                         ["Bóng tim to (Cardiomegaly)", 
                                          "Sung huyết phổi (Pulmonary congestion)", 
                                          "Tràn dịch màng phổi (Pleural effusion)"])
                st.session_state.cxr_abnormal = len(cxr_res) > 0
                if st.session_state.cxr_abnormal:
                    st.warning("⚠️ Phát hiện bất thường trên X-quang ngực: Gợi ý suy tim hoặc bệnh lý phổi đi kèm.")
            else:
                st.session_state.cxr_abnormal = False
                st.success("✅ Kết quả X-quang ngực bình thường / Chưa ghi nhận bất thường.")
                
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
            st.session_state.lvef_val = lvef
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
            pad_adj_default = False
            
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

        # Determine Adjusted Likelihood dynamically for testing path (Sửa theo yêu cầu: Giữ nguyên RF-CL % nền, không cộng dồn +15%)
        adjusted_likelihood = base_likelihood
        cacs_reclassified = False
        reclassified_label = ""
        reclassified_color = ""
        reclassified_likelihood_val = base_likelihood

        def get_class_label(val):
            if val <= 5: return "Rất thấp (Very Low)", "#28a745"
            elif val <= 15: return "Thấp (Low)", "#17a2b8"
            elif val <= 50: return "Trung bình (Moderate)", "#ffc107"
            elif val <= 85: return "Cao (High)", "#fd7e14"
            else: return "Rất cao (Very High)", "#dc3545"

        # CACS reclassification concept (ESC 2024 / clinical judgment)
        if cacs_available == "Đã có kết quả":
            if cacs_val == 0:
                cacs_reclassified = True
                reclassified_label = "Rất thấp (Very Low) (đã hạ bậc nhờ CACS = 0)"
                reclassified_color = "#28a745"
                reclassified_likelihood_val = 5
            elif cacs_val >= 1000:
                cacs_reclassified = True
                reclassified_label = "Rất cao (Very High) (đã tăng bậc do CACS ≥ 1000)"
                reclassified_color = "#dc3545"
                reclassified_likelihood_val = 90
            elif cacs_val >= 400:
                cacs_reclassified = True
                reclassified_label = "Cao (High) (đã tăng bậc do CACS 400-999)"
                reclassified_color = "#fd7e14"
                reclassified_likelihood_val = 65

        # Display results based on clinical judgment
        st.markdown("### 🔍 Đánh giá Lâm sàng & Điều chỉnh Khả năng Lâm sàng (Clinical Judgment)")
        
        has_other_abnormalities = (adj_ecg or adj_lvd or adj_pad or adj_calc or adj_ex_ecg)
        
        if has_other_abnormalities:
            st.warning("⚠️ **Định hướng lâm sàng:** Do có bất thường lâm sàng bổ sung (ECG, Siêu âm tim, PAD, hoặc vôi hóa mạch vành trên phim chụp khác), **khả năng lâm sàng thực tế của bệnh nhân có thể cao hơn khả năng lâm sàng nền (RF-CL)**. Việc quyết định thăm dò tiếp theo nên dựa trên đánh giá cá thể hóa này của nhà lâm sàng.")
        
        if cacs_available == "Đã có kết quả":
            if cacs_val == 0:
                st.info("💡 **Hạ bậc nguy cơ nhờ CACS = 0:** Khả năng lâm sàng thực tế của bệnh nhân được phân tầng lại về nhóm **Rất thấp (Very Low) (Class IIa)**.")
            elif cacs_val >= 400:
                st.warning("💡 **Tăng bậc nguy cơ do CACS cao:** Khả năng lâm sàng thực tế được phân tầng lại lên mức **Cao đến Rất cao (Class IIa)**.")

        # Determine display values
        if cacs_reclassified:
            display_label = reclassified_label
            display_color = reclassified_color
            display_val_str = f"~ {reclassified_likelihood_val}% (Phân tầng lại dựa trên CACS)"
            adjusted_likelihood = reclassified_likelihood_val
        else:
            base_label, base_col_hex = get_class_label(base_likelihood)
            display_label = base_label
            display_color = base_col_hex
            if has_other_abnormalities:
                display_val_str = f"{base_likelihood}% (Cảnh báo: khả năng lâm sàng thực tế có thể cao hơn mức nền này)"
            else:
                display_val_str = f"{base_likelihood}%"
            adjusted_likelihood = base_likelihood

        st.markdown(f"""
        <div style='background-color: #f1f2f6; border-radius: 6px; padding: 15px; border-left: 6px solid {display_color}; margin: 15px 0;'>
            <h4 style='margin: 0; color: #333;'>KẾT QUẢ ĐÁNH GIÁ KHẢ NĂNG LÂM SÀNG:</h4>
            <p style='font-size: 1.6rem; margin: 10px 0 5px 0; font-weight: bold;'>Khả năng lâm sàng nền (RF-CL): <span style='color: {display_color};'>{display_val_str}</span></p>
            <p style='margin: 0; font-size: 1.1rem;'>Nhóm phân tầng: <strong style='color: {display_color};'>{display_label}</strong></p>
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
                **🟡 KHUYẾN CÁO: CHỌN CCTA (Class I A) HOẶC THĂM DÒ HÌNH ẢNH CHỨC NĂNG GỨNG SỨC (Class I B)**
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

        # 2. Results of Diagnostic Tests
        st.subheader("2. Lựa chọn Phương pháp Thăm dò đã Thực hiện & Nhập Kết quả")
        st.markdown("<p style='font-size: 0.95rem; color: #555;'>Để tiếp tục phân tầng nguy cơ và quyết định hướng điều trị tiếp theo, vui lòng lựa chọn phương pháp thăm dò đã được chỉ định thực hiện trên thực tế cho bệnh nhân:</p>", unsafe_allow_html=True)
        
        # Initialize selected_test in session state
        if 'selected_test_val' not in st.session_state:
            st.session_state.selected_test_val = "Chờ làm xét nghiệm / Chưa thực hiện"
            
        test_options = [
            "Chờ làm xét nghiệm / Chưa thực hiện",
            "Chụp cắt lớp vi tính động mạch vành (CCTA)",
            "Thăm dò hình ảnh chức năng gắng sức (Stress Echo, Stress CMR, PET/SPECT...)",
            "Chụp động mạch vành xâm lấn (ICA)"
        ]
        
        default_test_idx = test_options.index(st.session_state.selected_test_val) if st.session_state.selected_test_val in test_options else 0
        
        selected_test = st.radio(
            "Phương pháp thăm dò cận lâm sàng đã thực hiện thực tế:",
            test_options,
            index=default_test_idx
        )
        st.session_state.selected_test_val = selected_test
        
        # Initialize variables to prevent undefined errors
        is_high_risk = False
        st.session_state.anoca_suspected = False
        
        if selected_test == "Chờ làm xét nghiệm / Chưa thực hiện":
            st.info("💡 Đang chờ kết quả cận lâm sàng. Vui lòng lựa chọn phương pháp thăm dò thực tế ở trên và nhập kết quả để tiếp tục phân tầng nguy cơ và thiết lập phác đồ.")
            
        elif selected_test == "Chụp cắt lớp vi tính động mạch vành (CCTA)":
            ccta_res = st.radio(
                "Kết quả giải phẫu mạch vành trên phim CCTA:",
                [
                    "LOẠI TRỪ hẹp động mạch vành tắc nghẽn (Không hẹp hoặc chỉ hẹp nhẹ-vừa <50% thân chung LMS, <70% các nhánh chính)",
                    "CÓ hẹp động mạch vành tắc nghẽn (Obstructive CAD: ≥50% thân chung LMS, hoặc ≥70% ít nhất một nhánh mạch vành lớn)"
                ]
            )
            
            if "LOẠI TRỪ" in ccta_res:
                st.session_state.anoca_suspected = False
                has_persistent_symptoms = st.radio(
                    "Bệnh nhân có triệu chứng đau ngực hoặc khó thở dai dẳng, ảnh hưởng chất lượng cuộc sống (sau khi đã loại trừ nguyên nhân ngoài tim) không?",
                    ["Có triệu chứng dai dẳng (Persistent symptoms of ischemia)", "Không còn triệu chứng / Triệu chứng nhẹ đã ổn định"]
                )
                if has_persistent_symptoms == "Có triệu chứng dai dẳng (Persistent symptoms of ischemia)":
                    st.session_state.anoca_suspected = True
                    # Render ANOCA/INOCA diagnosis flow
                    st.markdown("""
                    <div class='warning-box' style='border-left-color: #f1c40f; background-color: #fefdf3;'>
                        <h4 style='color: #d4ac0d; margin-top: 0;'>🧩 NGHI NGỜ CAO MẮC ANOCA / INOCA (Thiếu máu cơ tim không do tắc nghẽn)</h4>
                        <p>CCTA loại trừ hẹp tắc nghẽn nhưng bệnh nhân vẫn đau ngực/khó thở dai dẳng. Hướng dẫn ESC 2024 khuyến nghị:</p>
                        <ul>
                            <li><strong>Đo chức năng mạch vành xâm lấn (Invasive Coronary Function Testing - ICFT):</strong> Khuyến cáo thực hiện để xác định cơ chế bệnh sinh (Class I B cho bệnh nhân có triệu chứng hạn chế dai dẳng).</li>
                            <li><strong>Các chỉ số cần đo:</strong> CFR (Coronary Flow Reserve) và IMR/HMR (Kháng vi tuần hoàn) và Nghiệm pháp co thắt Acetylcholine (ACh).</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.write("**Xác định kiểu hình (Endotypes) của ANOCA/INOCA dựa trên kết quả thăm dò chức năng mạch vành:**")
                    endo_col1, endo_col2 = st.columns(2)
                    with endo_col1:
                        icft_cfr = st.selectbox("1. Lưu lượng dự trữ mạch vành (CFR):", ["Bình thường (CFR ≥ 2.5)", "Giảm (CFR < 2.5)"])
                        icft_imr = st.selectbox("2. Chỉ số kháng vi tuần hoàn (IMR/HMR):", ["Bình thường (IMR < 25 VÀ HMR ≤ 2.5)", "Tăng (IMR ≥ 25 HOẶC HMR > 2.5)"])
                    with endo_col2:
                        icft_spasm = st.selectbox("3. Nghiệm pháp kích thích Acetylcholine (ACh):", 
                                                  ["Âm tính", 
                                                   "Dương tính co thắt thượng tâm mạc (Hẹp đường kính mạch vành ≥ 90% kèm tái phát đau ngực và ST thay đổi)", 
                                                   "Dương tính co thắt vi mạch (ST thay đổi và tái phát đau ngực nhưng không co thắt mạch lớn)"])
                    
                    st.session_state.anoca_endotype = "Chưa phân loại"
                    if icft_cfr == "Giảm (CFR < 2.5)" or icft_imr == "Tăng (IMR ≥ 25 HOẶC HMR > 2.5)":
                        if icft_spasm == "Âm tính":
                            st.session_state.anoca_endotype = "Đau thắt ngực vi mạch (Microvascular Angina - MVA)"
                        else:
                            st.session_state.anoca_endotype = "Kiểu hình hỗn hợp (Mixed MVA + Vasospastic)"
                    elif icft_spasm != "Âm tính":
                        st.session_state.anoca_endotype = "Co thắt mạch vành (Vasospastic Angina - VSA)"
                    else:
                        st.session_state.anoca_endotype = "Đau ngực không do tim (Non-cardiac Chest Pain)"
                        
                    st.success(f"🎯 **Kiểu hình ANOCA/INOCA xác định:** `{st.session_state.anoca_endotype}`. *Phác đồ điều trị cá thể hóa tương ứng đã được kích hoạt tại Bước 4.*")
                else:
                    st.session_state.anoca_suspected = False
                    st.success("✅ Kết quả: Động mạch vành không hẹp tắc nghẽn và bệnh nhân ổn định không triệu chứng. Khuyên dùng tối ưu lối sống, kiểm soát yếu tố nguy cơ chung.")
            
            else: # Obstructive CAD
                st.session_state.anoca_suspected = False
                st.subheader("⚡ Phân tầng Nguy cơ Biến cố Tim mạch (Cho Bệnh nhân Hẹp Mạch Vành Tắc Nghẽn)")
                st.markdown("<p style='font-size: 0.95rem; color: #555;'>Xác định các tiêu chuẩn giải phẫu hoặc chức năng nguy cơ cao xảy ra biến cố (MACE) - Khuyến cáo <span class='class-badge-1'>Class I B</span>:</p>", unsafe_allow_html=True)
                
                risk_col1, risk_col2 = st.columns(2)
                with risk_col1:
                    st.markdown("**Các tiêu chuẩn về cấu trúc giải phẫu (Anatomical):**")
                    high_risk_anatomy = st.checkbox("CCTA: Tổn thương Thân chung Động mạch vành trái (Left Main) hẹp ≥ 50%")
                    high_risk_anatomy_2 = st.checkbox("CCTA: Hẹp nặng ≥ 70% ở cả 3 nhánh mạch vành (Three-vessel disease)")
                    high_risk_anatomy_3 = st.checkbox("CCTA: Hẹp đoạn gần động mạch liên thất trước (Proximal LAD) ≥ 70%")
                with risk_col2:
                    st.markdown("**Các tiêu chuẩn chức năng gắng sức (nếu làm phối hợp):**")
                    high_risk_func_1 = st.checkbox("Stress Echo: ≥ 3/16 phân vùng cơ tim giảm động/vô động do gắng sức")
                    high_risk_func_2 = st.checkbox("Stress CMR: ≥ 2/16 phân vùng thiếu máu cơ tim diện rộng")
                    high_risk_func_3 = st.checkbox("SPECT/PET: Diện tích thiếu máu cơ tim ≥ 10% cơ thất trái")
                    high_risk_func_4 = st.checkbox("Exercise ECG: Điểm số Duke (Duke Treadmill Score) < -10")
                
                is_high_risk = (high_risk_anatomy or high_risk_anatomy_2 or high_risk_anatomy_3 or 
                                high_risk_func_1 or high_risk_func_2 or high_risk_func_3 or high_risk_func_4)
                
                if is_high_risk:
                    st.error("""
                    **🚨 BỆNH NHÂN THUỘC NHÓM NGUY CƠ BIẾN CỐ CAO (HIGH EVENT-RISK) - Khuyến cáo Class I B:**
                    - Khuyến cáo chụp mạch vành xâm lấn (ICA) để lập kế hoạch tái thông mạch vành (can thiệp hoặc mổ cầu nối) nhằm cải thiện triệu chứng và tiên lượng sống còn.
                    """)
                else:
                    st.info("💡 Bệnh nhân có hẹp tắc nghẽn nhưng chưa đủ tiêu chí nguy cơ biến cố cao diện rộng. Ưu tiên điều trị nội khoa tối ưu (GDMT). Xem xét tái thông để giảm triệu chứng nếu đau ngực vẫn dai dẳng.")

        elif selected_test == "Thăm dò hình ảnh chức năng gắng sức (Stress Echo, Stress CMR, PET/SPECT...)":
            func_res = st.radio(
                "Kết quả thiếu máu cơ tim gắng sức:",
                [
                    "ÂM TÍNH (Không có thiếu máu cơ tim có ý nghĩa lâm sàng)",
                    "DƯƠNG TÍNH (Phát hiện thiếu máu cơ tim có ý nghĩa sinh lý)"
                ]
            )
            
            if "DƯƠNG TÍNH" in func_res:
                st.session_state.anoca_suspected = False
                st.subheader("⚡ Phân tầng Nguy cơ Biến cố Tim mạch dựa trên diện tích thiếu máu")
                st.markdown("<p style='font-size: 0.95rem; color: #555;'>Đánh giá mức độ rộng của vùng thiếu máu cơ tim để phân tầng nguy cơ biến cố cao:</p>", unsafe_allow_html=True)
                
                func_risk_col1, func_risk_col2 = st.columns(2)
                with func_risk_col1:
                    high_func_1 = st.checkbox("Stress Echo: ≥ 3/16 phân vùng cơ tim giảm động/vô động do gắng sức")
                    high_func_2 = st.checkbox("Stress CMR: ≥ 2/16 phân vùng thiếu máu cơ tim diện rộng")
                with func_risk_col2:
                    high_func_3 = st.checkbox("Stress SPECT/PET: Diện tích thiếu máu cơ tim ≥ 10% cơ thất trái")
                    high_func_4 = st.checkbox("Exercise ECG: Điểm số Duke (Duke Treadmill Score) < -10")
                
                is_high_risk = (high_func_1 or high_func_2 or high_func_3 or high_func_4)
                
                if is_high_risk:
                    st.error("""
                    **🚨 BỆNH NHÂN THUỘC NHÓM NGUY CƠ BIẾN CỐ CAO (HIGH EVENT-RISK) - Khuyến cáo Class I B:**
                    - Vùng thiếu máu cơ tim diện rộng, nguy cơ xảy ra biến cố tim mạch bất lợi (MACE) trong tương lai cao.
                    - Khuyến cáo chụp mạch vành xâm lấn (ICA) sớm để xem xét chỉ định can thiệp/phẫu thuật mạch vành.
                    """)
                else:
                    st.info("💡 Thiếu máu cơ tim mức độ nhẹ-vừa (nguy cơ thấp-trung bình). Ưu tiên điều trị nội khoa tối ưu (GDMT). Xem xét can thiệp mạch vành chỉ khi triệu chứng vẫn dai dẳng dù đã tối ưu hóa thuốc.")
            
            else: # Âm tính
                st.session_state.anoca_suspected = False
                has_persistent_symptoms = st.radio(
                    "Bệnh nhân có triệu chứng đau ngực hoặc khó thở dai dẳng, ảnh hưởng chất lượng cuộc sống (sau khi đã loại trừ nguyên nhân ngoài tim) không?",
                    ["Có triệu chứng dai dẳng (Persistent symptoms of ischemia)", "Không còn triệu chứng / Triệu chứng nhẹ đã ổn định"]
                )
                if has_persistent_symptoms == "Có triệu chứng dai dẳng (Persistent symptoms of ischemia)":
                    st.session_state.anoca_suspected = True
                    st.markdown("""
                    <div class='warning-box' style='border-left-color: #f1c40f; background-color: #fefdf3;'>
                        <h4 style='color: #d4ac0d; margin-top: 0;'>🧩 NGHI NGỜ MẮC ANOCA / INOCA</h4>
                        <p>Nghiệm pháp gắng sức không phát hiện thiếu máu cơ tim thượng tâm mạc rộng, nhưng bệnh nhân vẫn có triệu chứng đau ngực dai dẳng. Cần xem xét:</p>
                        <ul>
                            <li>Định hướng thực hiện <strong>Chụp cắt lớp vi tính mạch vành (CCTA)</strong> để loại trừ hẹp cấu trúc hoặc đo chức năng vi mạch.</li>
                            <li>Nếu CCTA âm tính, tiến hành <strong>đo chức năng mạch vành xâm lấn (ICFT)</strong> khi triệu chứng ảnh hưởng nặng chất lượng cuộc sống.</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.write("**Xác định kiểu hình (Endotypes) của ANOCA/INOCA (nếu đã làm ICFT):**")
                    endo_col1, endo_col2 = st.columns(2)
                    with endo_col1:
                        icft_cfr = st.selectbox("1. Lưu lượng dự trữ mạch vành (CFR):", ["Bình thường (CFR ≥ 2.5)", "Giảm (CFR < 2.5)"])
                        icft_imr = st.selectbox("2. Chỉ số kháng vi tuần hoàn (IMR/HMR):", ["Bình thường (IMR < 25 VÀ HMR ≤ 2.5)", "Tăng (IMR ≥ 25 HOẶC HMR > 2.5)"])
                    with endo_col2:
                        icft_spasm = st.selectbox("3. Nghiệm pháp kích thích Acetylcholine (ACh):", 
                                                  ["Âm tính", 
                                                   "Dương tính co thắt thượng tâm mạc (Hẹp đường kính mạch vành ≥ 90% kèm tái phát đau ngực và ST thay đổi)", 
                                                   "Dương tính co thắt vi mạch (ST thay đổi và tái phát đau ngực nhưng không co thắt mạch lớn)"])
                    
                    st.session_state.anoca_endotype = "Chưa phân loại"
                    if icft_cfr == "Giảm (CFR < 2.5)" or icft_imr == "Tăng (IMR ≥ 25 HOẶC HMR > 2.5)":
                        if icft_spasm == "Âm tính":
                            st.session_state.anoca_endotype = "Đau thắt ngực vi mạch (Microvascular Angina - MVA)"
                        else:
                            st.session_state.anoca_endotype = "Kiểu hình hỗn hợp (Mixed MVA + Vasospastic)"
                    elif icft_spasm != "Âm tính":
                        st.session_state.anoca_endotype = "Co thắt mạch vành (Vasospastic Angina - VSA)"
                    else:
                        st.session_state.anoca_endotype = "Đau ngực không do tim (Non-cardiac Chest Pain)"
                        
                    st.success(f"🎯 **Kiểu hình ANOCA/INOCA xác định:** `{st.session_state.anoca_endotype}`. *Phác đồ điều trị cá thể hóa tương ứng đã được kích hoạt tại Bước 4.*")
                else:
                    st.session_state.anoca_suspected = False
                    st.success("✅ Kết quả: Thăm dò gắng sức âm tính và bệnh nhân không triệu chứng. Khuyên dùng duy trì lối sống lành mạnh.")

        elif selected_test == "Chụp động mạch vành xâm lấn (ICA)":
            ica_res = st.radio(
                "Kết quả giải phẫu mạch vành trên phim chụp ICA xâm lấn:",
                [
                    "LOẠI TRỪ hẹp động mạch vành tắc nghẽn (Mạch vành hoàn toàn bình thường hoặc chỉ hẹp nhẹ <50% thân chung LMS, <50% các nhánh chính)",
                    "HẸP ĐỘNG MẠCH VÀNH TRUNG GIAN (Intermediate stenosis: Hẹp 50-90% các nhánh chính)",
                    "CÓ hẹp động mạch vành tắc nghẽn RÕ RỆT (Obstructive CAD: ≥50% thân chung LMS, hoặc ≥70% ít nhất một nhánh mạch vành lớn, hoặc FFR ≤ 0.80 / iFR ≤ 0.89)"
                ]
            )
            
            is_obstructive_flow = False
            is_non_obstructive_flow = False
            
            if ica_res == "HẸP ĐỘNG MẠCH VÀNH TRUNG GIAN (Intermediate stenosis: Hẹp 50-90% các nhánh chính)":
                st.warning("""
                **⚠️ KHUYẾN CÁO QUAN TRỌNG (ESC 2024): Sự không tương hợp giữa giải phẫu và ý nghĩa huyết động**
                - Hướng dẫn đặc biệt nhấn mạnh tổn thương hẹp trung gian trên giải phẫu không đồng nghĩa với việc gây ra thiếu máu cơ tim thực sự (haemodynamic significance).
                - **Khuyến cáo:** Bắt buộc phải đánh giá ý nghĩa chức năng/sinh lý của tổn thương (functional significance) bằng các biện pháp đo sinh lý trực tiếp: **FFR** hoặc **iFR** xâm lấn (Class I A) trước khi quyết định can thiệp.
                """)
                intermediate_functional_status = st.radio(
                    "Tình trạng đánh giá ý nghĩa sinh lý (Functional significance) của tổn thương trung gian này:",
                    [
                        "Chưa làm thăm dò chức năng (Cần làm thêm để đánh giá)",
                        "ĐÃ CHỨNG MINH CÓ Ý NGHĨA SINH LÝ (FFR ≤ 0.80 hoặc iFR ≤ 0.89)",
                        "ĐÃ CHỨNG MINH KHÔNG CÓ Ý NGHĨA SINH LÝ (FFR > 0.80 hoặc iFR > 0.89)"
                    ],
                    key="ica_intermediate_status"
                )
                if intermediate_functional_status == "Chưa làm thăm dò chức năng (Cần làm thêm để đánh giá)":
                    st.info("💡 Vui lòng thực hiện đo FFR hoặc iFR trực tiếp trong buồng tim để xác định xem hẹp trung gian này có thực sự gây ảnh hưởng huyết động không.")
                    st.session_state.anoca_suspected = False
                    is_high_risk = False
                elif "CÓ Ý NGHĨA SINH LÝ" in intermediate_functional_status:
                    is_obstructive_flow = True
                else:
                    is_non_obstructive_flow = True
            elif "LOẠI TRỪ" in ica_res:
                is_non_obstructive_flow = True
            else:
                is_obstructive_flow = True
                
            if is_non_obstructive_flow:
                st.session_state.anoca_suspected = False
                has_persistent_symptoms = st.radio(
                    "Bệnh nhân có triệu chứng đau ngực hoặc khó thở dai dẳng, ảnh hưởng chất lượng cuộc sống (sau khi đã loại trừ nguyên nhân ngoài tim) không?",
                    ["Có triệu chứng dai dẳng (Persistent symptoms of ischemia)", "Không còn triệu chứng / Triệu chứng nhẹ đã ổn định"]
                )
                if has_persistent_symptoms == "Có triệu chứng dai dẳng (Persistent symptoms of ischemia)":
                    st.session_state.anoca_suspected = True
                    st.markdown("""
                    <div class='warning-box' style='border-left-color: #f1c40f; background-color: #fefdf3;'>
                        <h4 style='color: #d4ac0d; margin-top: 0;'>🧩 NGHI NGỜ CAO MẮC ANOCA / INOCA</h4>
                        <p>Chụp ICA loại trừ hẹp tắc nghẽn nhưng bệnh nhân vẫn đau ngực dai dẳng. Hướng dẫn ESC 2024 khuyến nghị thực hiện <strong>Đo chức năng mạch vành xâm lấn (ICFT - Class I B)</strong> ngay trong buồng tim để chẩn đoán kiểu hình:</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.write("**Xác định kiểu hình (Endotypes) của ANOCA/INOCA dựa trên ICFT thực hiện trực tiếp:**")
                    endo_col1, endo_col2 = st.columns(2)
                    with endo_col1:
                        icft_cfr = st.selectbox("1. Lưu lượng dự trữ mạch vành (CFR):", ["Bình thường (CFR ≥ 2.5)", "Giảm (CFR < 2.5)"])
                        icft_imr = st.selectbox("2. Chỉ số kháng vi tuần hoàn (IMR/HMR):", ["Bình thường (IMR < 25 VÀ HMR ≤ 2.5)", "Tăng (IMR ≥ 25 HOẶC HMR > 2.5)"])
                    with endo_col2:
                        icft_spasm = st.selectbox("3. Nghiệm pháp kích thích Acetylcholine (ACh):", 
                                                  ["Âm tính", 
                                                   "Dương tính co thắt thượng tâm mạc (Hẹp đường kính mạch vành ≥ 90% kèm tái phát đau ngực và ST thay đổi)", 
                                                   "Dương tính co thắt vi mạch (ST thay đổi và tái phát đau ngực nhưng không co thắt mạch lớn)"])
                    
                    st.session_state.anoca_endotype = "Chưa phân loại"
                    if icft_cfr == "Giảm (CFR < 2.5)" or icft_imr == "Tăng (IMR ≥ 25 HOẶC HMR > 2.5)":
                        if icft_spasm == "Âm tính":
                            st.session_state.anoca_endotype = "Đau thắt ngực vi mạch (Microvascular Angina - MVA)"
                        else:
                            st.session_state.anoca_endotype = "Kiểu hình hỗn hợp (Mixed MVA + Vasospastic)"
                    elif icft_spasm != "Âm tính":
                        st.session_state.anoca_endotype = "Co thắt mạch vành (Vasospastic Angina - VSA)"
                    else:
                        st.session_state.anoca_endotype = "Đau ngực không do tim (Non-cardiac Chest Pain)"
                        
                    st.success(f"🎯 **Kiểu hình ANOCA/INOCA xác định:** `{st.session_state.anoca_endotype}`. *Phác đồ điều trị cá thể hóa tương ứng đã được kích hoạt tại Bước 4.*")
                else:
                    st.session_state.anoca_suspected = False
                    st.success("✅ Kết quả: Chụp ICA hoàn toàn bình thường và bệnh nhân ổn định. Không cần điều trị chuyên biệt mạch vành.")
                    
            elif is_obstructive_flow: # Obstructive CAD
                st.session_state.anoca_suspected = False
                st.subheader("⚡ Phân tầng Nguy cơ Biến cố Tim mạch (Cho Bệnh nhân Hẹp Mạch Vành Tắc Nghẽn)")
                st.markdown("<p style='font-size: 0.95rem; color: #555;'>Xác định các tiêu chuẩn giải phẫu hoặc chức năng nguy cơ cao xảy ra biến cố (MACE) - Khuyến cáo <span class='class-badge-1'>Class I B</span>:</p>", unsafe_allow_html=True)
                
                risk_col1, risk_col2 = st.columns(2)
                with risk_col1:
                    st.markdown("**Các tiêu chuẩn về cấu trúc giải phẫu (Anatomical):**")
                    high_risk_anatomy = st.checkbox("ICA: Tổn thương Thân chung Động mạch vành trái (Left Main) hẹp ≥ 50%")
                    high_risk_anatomy_2 = st.checkbox("ICA: Hẹp nặng ≥ 70% ở cả 3 nhánh mạch vành (Three-vessel disease)")
                    high_risk_anatomy_3 = st.checkbox("ICA: Hẹp đoạn gần động mạch liên thất trước (Proximal LAD) ≥ 70%")
                with risk_col2:
                    st.markdown("**Các tiêu chuẩn chức năng gắng sức kèm theo (nếu có):**")
                    high_risk_func_1 = st.checkbox("Stress Echo: ≥ 3/16 phân vùng cơ tim giảm động/vô động do gắng sức", key="ica_f1")
                    high_risk_func_2 = st.checkbox("Stress CMR: ≥ 2/16 phân vùng thiếu máu cơ tim diện rộng", key="ica_f2")
                    high_risk_func_3 = st.checkbox("SPECT/PET: Diện tích thiếu máu cơ tim ≥ 10% cơ thất trái", key="ica_f3")
                    high_risk_func_4 = st.checkbox("Exercise ECG: Điểm số Duke (Duke Treadmill Score) < -10", key="ica_f4")
                
                is_high_risk = (high_risk_anatomy or high_risk_anatomy_2 or high_risk_anatomy_3 or 
                                high_risk_func_1 or high_risk_func_2 or high_risk_func_3 or high_risk_func_4)
                
                if is_high_risk:
                    st.error("""
                    **🚨 BỆNH NHÂN THUỘC NHÓM NGUY CƠ BIẾN CỐ CAO (HIGH EVENT-RISK) - Khuyến cáo Class I B:**
                    - Có bằng chứng tổn thương hẹp cấu trúc nguy cơ cao trên giải phẫu. Khuyến cáo chụp mạch vành xâm lấn (ICA) kết hợp đánh giá chức năng/sinh lý mạch vành (FFR/iFR) để lập kế hoạch chiến lược tái thông mạch vành sớm.
                    """)
                else:
                    st.info("💡 Bệnh nhân có hẹp tắc nghẽn mạch vành nhưng không thuộc nhóm nguy cơ biến cố cao diện rộng. Ưu tiên điều trị nội khoa tối ưu (GDMT). Xem xét can thiệp mạch vành chỉ khi triệu chứng đau ngực vẫn dai dẳng dù đã điều trị tối ưu thuốc.")

        # Step navigation
        st.write("")
        col_prev, col_next = st.columns(2)
        with col_prev:
            if st.button("⬅️ Quay lại Bước 2", key="step3_prev_btn"):
                set_step(2)
        with col_next:
            if st.button("Xác nhận & Sang Bước 4 ➡️", key="step3_next_btn"):
                st.session_state.high_risk_flag = is_high_risk
                set_step(4)


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
            sub_tab_med_prognostic, sub_tab_med_symptomatic = st.tabs([
                "🛡️ 1. Điều trị Cải thiện Tiên lượng",
                "💊 2. Tối ưu hóa Thuốc Chống Đau Thắt Ngực (Figure 9)"
            ])
            
            with sub_tab_med_prognostic:
                st.subheader("1. Thay đổi lối sống và Kiểm soát các yếu tố nguy cơ (Class I)")
                st.markdown("""
                *   **Bỏ hoàn toàn thuốc lá:** Hỗ trợ tư vấn cai thuốc, tránh phơi nhiễm khói thuốc lá thụ động (Class I A).
                *   **Chế độ ăn Địa Trung Hải (Mediterranean Diet):** Hạn chế chất béo bão hòa < 10% tổng năng lượng, tăng cường rau quả, ngũ cốc nguyên hạt. Hạn chế rượu bia (<100g/tuần).
                *   **Hoạt động thể lực:** Tập luyện thể dục cường độ trung bình 150-300 phút hoặc cường độ mạnh 75-150 phút mỗi tuần (Class I B). Giảm thời gian ngồi tĩnh tại (Class I B).
                *   **Kiểm soát cân nặng:** Đưa cân nặng về mức BMI mục tiêu (18.5 - 24.9 kg/m2).
                """)
                
                st.subheader("2. Thuốc bảo vệ mạch vành và Cải thiện tiên lượng (Class I)")
                st.markdown("""
                *   **Kháng kết tập tiểu cầu (Antiplatelets):** 
                    *   *Aspirin 75-100 mg/ngày* hoặc *Clopidogrel 75 mg/ngày* được khuyến cáo lâu dài ở bệnh nhân có bệnh mạch vành tắc nghẽn (Class I A).
                *   **Kiểm soát huyết áp:** Mục tiêu **120-129 / 70-79 mmHg** nếu dung nạp tốt (Class I A, ưu tiên ACEi hoặc ARB).
                *   **Bệnh nhân Đái tháo đường đi kèm:** Bắt buộc sử dụng thuốc **ức chế SGLT2 (SGLT2i)** (như Dapagliflozin 10mg q.d., Empagliflozin 10mg q.d.) và/hoặc **đồng vận thụ thể GLP-1 (GLP-1 RA)** để giảm nguy cơ tử vong do tim mạch và nhồi máu cơ tim (Class I A).
                """)
                
            with sub_tab_med_symptomatic:
                st.subheader("💊 Kê đơn & Phối hợp Thuốc chống Thiếu máu theo Figure 9 (ESC 2024)")
                
                # Pull clinical stats
                hr_val = st.session_state.get('hr_val', 75)
                sbp_val = st.session_state.get('sbp_val', 120)
                lvef_val = st.session_state.get('lvef_val', 55)
                egfr_val = st.session_state.get('egfr_val', 90)
                pft_abnormal = st.session_state.get('pft_abnormal', False)
                anoca_suspected = st.session_state.get('anoca_suspected', False)
                anoca_endotype = st.session_state.get('anoca_endotype', "Chưa phân loại")
                
                # Phenotype Classification Logic
                if anoca_suspected and "Vasospastic" in anoca_endotype:
                    phenotype = "Co thắt mạch vành (ANOCA - VSA)"
                    phenotype_desc = "Bệnh nhân co thắt động mạch vành không có hẹp tắc nghẽn."
                elif anoca_suspected and ("Microvascular" in anoca_endotype or "MVA" in anoca_endotype):
                    phenotype = "Đau thắt ngực vi mạch (ANOCA - MVA)"
                    phenotype_desc = "Rối loạn chức năng vi tuần hoàn vành không có hẹp tắc nghẽn."
                elif lvef_val <= 40:
                    phenotype = "Rối loạn chức năng thất trái / Suy tim HFrEF (LVEF ≤ 40%)"
                    phenotype_desc = "Rối loạn chức năng co bóp tâm thu cơ tim rõ rệt."
                elif hr_val > 80:
                    phenotype = "Tần số tim nhanh (HR > 80 nhịp/phút)"
                    phenotype_desc = "Huyết động ưu thế nhịp nhanh, cần giảm nhịp tim để kéo dài thời gian tâm trương."
                elif hr_val < 55:
                    phenotype = "Tần số tim chậm (HR < 55 nhịp/phút)"
                    phenotype_desc = "Tần số tim cơ bản thấp, chống chỉ định các thuốc làm chậm nhịp tim thêm."
                elif sbp_val < 95:
                    phenotype = "Huyết áp thấp (SBP < 95 mmHg)"
                    phenotype_desc = "Huyết áp cơ bản thấp, chống chỉ định các thuốc gây tụt huyết áp mạnh."
                else:
                    phenotype = "Kiểu hình chuẩn (Standard Profile)"
                    phenotype_desc = "Nhịp tim, huyết áp và chức năng thất trái trong giới hạn bình thường."

                # State initialization to avoid widget key assignment issues
                if 'prescribing_mode_val' not in st.session_state:
                    st.session_state.prescribing_mode_val = "💡 Khuyến nghị phác đồ (Tự động đề xuất theo Guideline)"

                mode_options = [
                    "💡 Khuyến nghị phác đồ (Tự động đề xuất theo Guideline)", 
                    "🛠️ Tự phối hợp và tra cứu"
                ]
                
                default_mode_idx = mode_options.index(st.session_state.prescribing_mode_val) if st.session_state.prescribing_mode_val in mode_options else 0
                
                prescribing_mode = st.radio(
                    "Chọn phương thức hỗ trợ quyết định điều trị:",
                    mode_options,
                    index=default_mode_idx
                )
                st.session_state.prescribing_mode_val = prescribing_mode
                
                # 1. Advisor Mode (Khuyến nghị phác đồ)
                if prescribing_mode == "💡 Khuyến nghị phác đồ (Tự động đề xuất theo Guideline)":
                    st.markdown(f"""
                    <div class='info-box' style='background-color: #f7f9fa; border-left: 5px solid #17b978; margin-bottom: 20px;'>
                        <h5 style='margin-top: 0; color: #1e3d59; font-weight: bold;'>👤 KIỂU HÌNH LÂM SÀNG TỰ ĐỘNG:</h5>
                        <p style='margin: 0; font-size: 1.1rem;'>Kiểu hình phát hiện: <strong style='color: #17b978;'>{phenotype}</strong></p>
                        <p style='margin: 5px 0 0 0; color: #555; font-size: 0.9rem;'>{phenotype_desc} (Thông số: SBP {sbp_val} mmHg, HR {hr_val} bpm, LVEF {lvef_val}%, eGFR {egfr_val} mL/min)</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.subheader(f"📋 Khuyến nghị điều trị cá thể hóa cho Kiểu hình: {phenotype}")
                    
                    if phenotype == "Co thắt mạch vành (ANOCA - VSA)":
                        st.markdown("""
                        - **Bước 1 (Đầu tay):** <span class='class-badge-1'>Class I B</span> Sử dụng **Chẹn kênh Canxi (CCBs)** liều cao (như Amlodipine 10mg hoặc Diltiazem 120-240mg) để giãn động mạch thượng tâm mạc co thắt.
                        - **Bước 2 (Phối hợp):** <span class='class-badge-2a'>Class IIa B</span> Thêm **Nitrates tác dụng kéo dài** (như Isosorbide Mononitrate 30-60mg q.d.) nếu triệu chứng chưa được kiểm soát hoàn toàn.
                        - **🚨 CẢNH BÁO ĐỎ (Class III):** **TRÁNH DÙNG THUỐC CHẸN BETA ĐƠN TRỊ LIỆU** vì gây co thắt vành nặng thêm do kích thích alpha-adrenergic không đối kháng.
                        """, unsafe_allow_html=True)
                        apply_target = ["Chẹn kênh Canxi DHP (DHP-CCB)"]
                        
                    elif phenotype == "Đau thắt ngực vi mạch (ANOCA - MVA)":
                        st.markdown("""
                        - **Bước 1 (Đầu tay):** <span class='class-badge-2a'>Class IIa B</span> **Chẹn beta (BB)** (như Bisoprolol hoặc Nebivolol) để giảm công tim.
                        - **Bước 2 (Phối hợp):** <span class='class-badge-2a'>Class IIa B</span> Phối hợp thêm **Chẹn kênh canxi DHP (DHP-CCB)** (như Amlodipine) nếu chẹn beta đơn trị chưa đỡ.
                        - **Bước 3 (Kháng trị):** <span class='class-badge-2b'>Class IIb B</span> Cân nhắc dùng thêm Nicorandil hoặc Ranolazine.
                        - **Bảo vệ mạch:** <span class='class-badge-2a'>Class IIa B</span> Sử dụng **ACEi/ARB** và **Statin** để phục hồi chức năng nội mạc vi tuần hoàn.
                        """, unsafe_allow_html=True)
                        apply_target = ["Chẹn beta (Beta-blockers - BB)", "Chẹn kênh Canxi DHP (DHP-CCB)"]
                        
                    elif phenotype == "Rối loạn chức năng thất trái / Suy tim HFrEF (LVEF ≤ 40%)":
                        st.markdown("""
                        - **Bước 1 (Đầu tay):** <span class='class-badge-1'>Class I A</span> **Chẹn beta (BB)** (như Bisoprolol, Metoprolol Succinate, Carvedilol) liều thấp, tăng liều dần để cải thiện tiên lượng tử vong.
                        - **Bước 2 (Phối hợp):** <span class='class-badge-2a'>Class IIa B</span> Phối hợp thêm **Ivabradine** (nếu bệnh nhân nhịp xoang ≥ 70 bpm) HOẶC **Trimetazidine MR** (Class IIa B) để bổ sung năng lượng cơ tim.
                        - **Hỗ trợ triệu chứng:** <span class='class-badge-2a'>Class IIa B</span> Thêm Nitrates kéo dài hoặc DHP-CCB (như Amlodipine) để kiểm soát triệu chứng đau ngực thêm.
                        - **🚨 CẤM DÙNG (Class III):** **Non-DHP CCB (Verapamil / Diltiazem)** bị chống chỉ định tuyệt đối do tác dụng ức chế cơ tim làm nặng thêm suy tim.
                        """, unsafe_allow_html=True)
                        apply_target = ["Chẹn beta (Beta-blockers - BB)"]
                        
                    elif phenotype == "Tần số tim nhanh (HR > 80 nhịp/phút)":
                        st.markdown("""
                        - **Bước 1 (Đầu tay):** <span class='class-badge-1'>Class I B</span> Khởi trị bằng **Chẹn beta (BB)** hoặc **Chẹn kênh canxi Non-DHP** (Verapamil/Diltiazem) để đưa nhịp tim đích về mốc 55-60 nhịp/phút.
                        - **Bước 2 (Phối hợp):** <span class='class-badge-2a'>Class IIa B</span> Phối hợp **Chẹn beta (BB) + Chẹn kênh canxi DHP** (DHP-CCB) khi đơn trị liệu chưa kiểm soát tốt triệu chứng.
                        - **Bước 3 (Phối hợp thêm):** 
                            * Phối hợp thêm **Ranolazine** HOẶC **Nitrates tác dụng kéo dài** (<span class='class-badge-2a'>Class IIa B</span>).
                            * Phối hợp thêm **Trimetazidine MR** HOẶC **Nicorandil** (<span class='class-badge-2b'>Class IIb B</span>).
                            * Chỉ cân nhắc phối hợp thêm **Ivabradine** (<span class='class-badge-2a'>Class IIa B</span>) nếu bệnh nhân có nhịp xoang ≥ 70 bpm VÀ kèm theo **suy tim/LVEF ≤ 40%**. 
                            * **🚨 CHỐNG CHỈ ĐỊNH (Class III B):** Tuyệt đối không dùng Ivabradine cho bệnh nhân LVEF > 40% không có suy tim lâm sàng.
                        """, unsafe_allow_html=True)
                        apply_target = ["Chẹn beta (Beta-blockers - BB)", "Chẹn kênh Canxi DHP (DHP-CCB)"]
                        
                    elif phenotype == "Tần số tim chậm (HR < 55 nhịp/phút)":
                        st.markdown("""
                        - **Bước 1 (Đầu tay):** <span class='class-badge-1'>Class I B</span> Khởi trị bằng **Chẹn kênh canxi DHP (DHP-CCB)** (như Amlodipine, Felodipine) do tác dụng giãn mạch chống đau thắt ngực mà không làm giảm nhịp tim thêm.
                        - **Bước 2 (Phối hợp):** 
                            * Phối hợp thêm **Ranolazine** HOẶC **Nitrates tác dụng kéo dài** (<span class='class-badge-2a'>Class IIa B</span>).
                            * Phối hợp thêm **Trimetazidine MR** HOẶC **Nicorandil** (<span class='class-badge-2b'>Class IIb B</span>).
                        - **⚠️ Thận trọng rất cao:** Chống chỉ định dùng thuốc làm giảm nhịp tim thêm (Chẹn Beta, Non-DHP CCB, Ivabradine).
                        """, unsafe_allow_html=True)
                        apply_target = ["Chẹn kênh Canxi DHP (DHP-CCB)"]
                        
                    elif phenotype == "Huyết áp thấp (SBP < 95 mmHg)":
                        st.markdown("""
                        - **Bước 1 (Đầu tay):** 
                            * **Chẹn beta (BB)** liều thấp chỉ khởi trị nếu nhịp nhanh VÀ kèm theo suy tim/LVEF ≤ 40% (<span class='class-badge-1'>Class I A</span>).
                            * Nếu LVEF > 40% không kèm suy tim, ưu tiên sử dụng các thuốc chống đau ngực không gây hạ áp như **Ranolazine** (<span class='class-badge-2a'>Class IIa B</span>) hoặc **Trimetazidine MR** (<span class='class-badge-2b'>Class IIb B</span>) làm lựa chọn đầu tay.
                        - **Bước 2 (Phối hợp):**
                            * Nếu nhịp xoang ≥ 70 bpm VÀ LVEF ≤ 40%: Có thể phối hợp thêm **Ivabradine** (<span class='class-badge-2a'>Class IIa B</span>).
                            * **🚨 CHỐNG CHỈ ĐỊNH (Class III B):** Tuyệt đối không dùng Ivabradine cho bệnh nhân LVEF > 40% không có suy tim lâm sàng.
                        - **⚠️ Thận trọng rất cao:** Tránh sử dụng các thuốc giãn mạch mạnh làm tụt huyết áp sâu thêm như CCBs, Long-acting Nitrates, Nicorandil ở liều cao.
                        """, unsafe_allow_html=True)
                        apply_target = ["Ranolazine"]
                        
                    else: # Standard Profile
                        st.markdown("""
                        - **Bước 1 (Đầu tay):** <span class='class-badge-1'>Class I B</span> Khởi trị bằng **Chẹn beta (BB)** và/hoặc **Chẹn kênh Canxi (CCBs)** để kiểm soát triệu chứng đau thắt ngực.
                        - **Bước 2 (Phối hợp):** <span class='class-badge-2a'>Class IIa B</span> Phối hợp **Chẹn beta (BB) + Chẹn kênh canxi DHP (DHP-CCB)** khi đơn trị liệu chưa kiểm soát tốt triệu chứng.
                        - **Bước 3 (Phối hợp thêm):**
                            * Phối hợp thêm **Ranolazine** HOẶC **Nitrates tác dụng kéo dài** (<span class='class-badge-2a'>Class IIa B</span>).
                            * Phối hợp thêm **Trimetazidine MR** HOẶC **Nicorandil** (<span class='class-badge-2b'>Class IIb B</span>).
                            * **🚨 CHỐNG CHỈ ĐỊNH (Class III B):** Tuyệt đối không dùng Ivabradine cho bệnh nhân LVEF > 40% không có suy tim lâm sàng.
                        """, unsafe_allow_html=True)
                        apply_target = ["Chẹn beta (Beta-blockers - BB)", "Chẹn kênh Canxi DHP (DHP-CCB)"]
                        
                    # Auto Prescribe Button WITHOUT direct key assignment
                    if st.button("👉 ÁP DỤNG PHÁC ĐỒ KHUYẾN NGHỊ NÀY", key="auto_prescribe_run_btn"):
                        mapping = {
                            "Chẹn beta (Beta-blockers - BB)": "Chẹn beta (Beta-blockers - BB)",
                            "Chẹn kênh Canxi DHP (DHP-CCB)": "Chẹn kênh Canxi DHP (DHP-CCB)",
                            "Chẹn kênh Canxi Non-DHP (Non-DHP CCB)": "Chẹn kênh Canxi Non-DHP (Non-DHP CCB)",
                            "Long-acting Nitrates": "Nitrates tác dụng kéo dài (Long-acting Nitrates)",
                            "Ivabradine": "Ivabradine",
                            "Ranolazine": "Ranolazine",
                            "Trimetazidine MR": "Trimetazidine MR",
                            "Nicorandil": "Nicorandil"
                        }
                        # map properly from short keys to full keys
                        mapped_targets = []
                        for t in apply_target:
                            if "Beta-blockers" in t or "BB" in t: mapped_targets.append("Chẹn beta (Beta-blockers - BB)")
                            elif "DHP-CCB" in t: mapped_targets.append("Chẹn kênh Canxi DHP (DHP-CCB)")
                        st.session_state.selected_drugs_val = mapped_targets
                        st.session_state.prescribing_mode_val = "🛠️ Tự phối hợp và tra cứu"
                        st.success("✅ Đã áp dụng phác đồ! Hệ thống đã tự động chuyển sang chế độ Tự phối hợp với các thuốc tương ứng.")
                        st.rerun()

                # 2. Manual Mode (Tự phối hợp và tra cứu)
                else: 
                    st.markdown("#### Lựa chọn thuốc Kê đơn & Tra cứu Chống chỉ định chi tiết")
                    
                    if 'selected_drugs_val' not in st.session_state:
                        st.session_state.selected_drugs_val = []
                        
                    with st.container(border=True):
                        selected_drugs = st.multiselect(
                            "Chọn một hoặc nhiều nhóm thuốc chống đau thắt ngực để phối hợp và xem chống chỉ định chi tiết dưới dạng hộp:",
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
                        
                        # Display Contraindications Dynamically inside the container for SELECTED drugs only
                        if selected_drugs:
                            st.markdown("##### 🔍 Chi tiết Chống chỉ định & Thận trọng của các thuốc đã chọn:")
                            
                            if prescribe_bb:
                                with st.expander("📖 Chống chỉ định & Thận trọng của Chẹn Beta (BB)", expanded=True):
                                    st.markdown("""
                                    - **❌ CHỐNG CHỈ ĐỊNH TUYỆT ĐỐI (Class III):**
                                        * Nhịp tim chậm lúc nghỉ (< 50 nhịp/phút).
                                        * Block nhĩ thất (AV Block) độ II hoặc III (trừ khi đã đặt máy tạo nhịp).
                                        * Hội chứng suy nút xoang (Sick sinus syndrome).
                                        * Suy tim mất bù cấp (Decompensated acute heart failure).
                                    - **⚠️ Thận trọng quan trọng:**
                                        * Hen phế quản nặng hoặc bệnh phổi tắc nghẽn mạn tính (COPD) có co thắt phế quản tiến triển (ưu tiên chọn chẹn beta siêu chọn lọc tim).
                                    """)
                                    
                            if prescribe_dhp_ccb:
                                with st.expander("📖 Chống chỉ định & Thận trọng của Chẹn kênh Canxi DHP (DHP-CCB)", expanded=True):
                                    st.markdown("""
                                    - **❌ CHỐNG CHỈ ĐỊNH TUYỆT ĐỐI (Class III):**
                                        * Huyết áp thấp nặng (Huyết áp tâm thu < 90 mmHg).
                                        * Hẹp khít van động mạch chủ có triệu chứng (Severe symptomatic aortic stenosis).
                                    - **⚠️ Thận trọng quan trọng:**
                                        * Nguy cơ gây phù ngoại biên vùng cổ chân ở liều cao (10mg).
                                    """)
                                    
                            if prescribe_non_dhp_ccb:
                                with st.expander("📖 Chống chỉ định & Thận trọng của Chẹn kênh Canxi Non-DHP (Verapamil / Diltiazem)", expanded=True):
                                    st.markdown("""
                                    - **❌ CHỐNG CHỈ ĐỊNH TUYỆT ĐỐI (Class III - Figure 9 Đỏ):**
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
                                    - **⚠️ Thận trọng quan trọng:**
                                        * Bắt buộc phải có khoảng trống không thuốc (Nitrate-free interval) từ 10-14 tiếng mỗi ngày để ngăn ngừa hiện tượng lờn thuốc.
                                    """)
                                    
                            if prescribe_ivabradine:
                                with st.expander("📖 Chống chỉ định & Thận trọng của Ivabradine", expanded=True):
                                    st.markdown("""
                                    - **❌ CHỐNG CHỈ ĐỊNH TUYỆT ĐỐI (Class III - Figure 9 Đỏ):**
                                        * Bệnh nhân nhịp xoang lúc nghỉ < 50 nhịp/phút.
                                        * Phối hợp đồng thời với thuốc **Chẹn kênh Canxi Non-DHP (Verapamil / Diltiazem)**.
                                        * Bệnh nhân **LVEF > 40% mà KHÔNG có biểu hiện suy tim** lâm sàng.
                                        * Bệnh nhân **Rung nhĩ (Atrial Fibrillation)** hoặc cuồng nhĩ.
                                    """)
                                    
                            if prescribe_ranolazine:
                                with st.expander("📖 Chống chỉ định & Thận trọng của Ranolazine", expanded=True):
                                    st.markdown("""
                                    - **❌ CHỐNG CHỈ ĐỊNH TUYỆT ĐỐI (Class III - Figure 9 Đỏ):**
                                        * **Suy thận nặng với mức lọc cầu thận eGFR < 30 mL/min**.
                                        * Suy gan nặng hoặc trung bình.
                                        * Phối hợp với thuốc ức chế mạnh men gan CYP3A4 (Ketoconazole, Clarithromycin...).
                                    """)
                                    
                            if prescribe_trimetazidine:
                                with st.expander("📖 Chống chỉ định & Thận trọng của Trimetazidine MR", expanded=True):
                                    st.markdown("""
                                    - **❌ CHỐNG CHỈ ĐỊNH TUYỆT ĐỐI (Class III - Figure 9 Đỏ):**
                                        * **Bệnh nhân mắc bệnh Parkinson**, có các triệu chứng Parkinson, run, hội chứng chân không yên, hoặc các rối loạn vận động ngoại tháp đi kèm.
                                        * **Suy thận nặng với mức lọc cầu thận eGFR < 30 mL/min** (độc tính tích lũy thuốc gây run tay).
                                    """)
                                    
                            if prescribe_nicorandil:
                                with st.expander("📖 Chống chỉ định & Thận trọng của Nicorandil", expanded=True):
                                    st.markdown("""
                                    - **❌ CHỐNG CHỈ ĐỊNH TUYỆT ĐỐI (Class III):**
                                        * Shock tim, tụt huyết áp nặng.
                                    - **⚠️ Thận trọng quan trọng:**
                                        * **Nguy cơ gây loét nghiêm trọng:** Nicorandil có thể gây ra các vết loét niêm mạc dạ dày - tá tràng, loét da, loét giác mạc khó lành. Ngừng thuốc ngay lập tức nếu phát hiện các vết loét này (Class I A).
                                    """)
                            
                            # INTERACTION AND COMPATIBILITY RESULTS DISPLAYED DYNAMICALLY WITHIN THE CONTAINER
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
                                    - **Khuyến cáo:** Chỉ nên sử dụng khi có chỉ định chuyên biệt và cần theo dõi nhịp tim/ECG liên tục.<br>
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
                                
                            # Rule 9: Standard Optimal combo (Class I)
                            if prescribe_bb and prescribe_dhp_ccb and not prescribe_non_dhp_ccb:
                                success_alerts.append("""
                                <div class='success-box' style='background-color: #e8f8f5; border-left: 5px solid #2ecc71; padding: 10px; margin-bottom: 10px;'>
                                    <span class='class-badge-2a'>Class IIa B</span> <strong>Phối hợp thuốc: Chẹn beta (BB) + Chẹn kênh Canxi DHP:</strong><br>
                                    - Đây là phối hợp hữu ích hàng đầu khi Chẹn beta hoặc DHP-CCB đơn trị liệu không kiểm soát tốt triệu chứng đau thắt ngực (Class IIa B).
                                </div>
                                """)
                                
                            # Rendering Alerts
                            if safety_alerts:
                                for alert in safety_alerts:
                                    st.markdown(alert, unsafe_allow_html=True)
                            elif success_alerts:
                                for s_alert in success_alerts:
                                    st.markdown(s_alert, unsafe_allow_html=True)
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
                <strong>PHÂN LOẠI NGUY CƠ TIM MẠCH:</strong> Bệnh nhân đã xác định xơ vữa mạch vành (CCS) mặc định thuộc nhóm <strong>Nguy cơ Tim mạch Cực kỳ Cao (Very High CV Risk)</strong>.
            </div>
            """, unsafe_allow_html=True)
            
            # Check for recurrent ASCVD events within 2 years
            recurrent_event = st.checkbox("Bệnh nhân có biến cố xơ vữa tái phát (nhồi máu cơ tim, đột quỵ...) trong vòng 2 năm qua khi đang dùng Statin liều tối đa?", key="lipid_recurrent_chk_v8")
            
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
            if lpa_now > 105:
                st.error(f"⚠️ **Lp(a) tăng cao: {lpa_now} nmol/L** (> 105 nmol/L hoặc > 50 mg/dL). Đây là yếu tố nguy cơ độc lập do di truyền làm tăng mạnh gánh nặng xơ vữa mạch vành tồn dư, đòi hỏi kiểm soát LDL-C nghiêm ngặt hơn.")
            elif lpa_now > 0:
                st.info(f"Lp(a) trong giới hạn bình thường: {lpa_now} nmol/L.")

        with tab_revasc:
            # 1. Revascularization vs ANOCA check
            if st.session_state.get('anoca_suspected', False):
                st.markdown(f"""
                <div class='warning-box' style='border-left-color: #c0392b; background-color: #fdf2f2;'>
                    <h4 style='color: #c0392b; margin-top: 0;'>🚫 KHÔNG CÓ CHỈ ĐỊNH CAN THIỆP / TÁI THÔNG MẠCH VÀNH (PCI / CABG)</h4>
                    <p style='font-size: 1.05rem;'>Bệnh nhân đã được chẩn đoán mắc <strong>ANOCA/INOCA (Kiểu hình: {st.session_state.get('anoca_endotype', 'Chưa phân loại')})</strong>. 
                    Không có tổn thương hẹp động mạch vành tắc nghẽn giải phẫu tầng thượng tâm mạc.</p>
                    <p style='margin-bottom: 0;'><strong>Khuyến cáo:</strong> Chống chỉ định tái thông mạch cơ học do không đem lại lợi ích lâm sàng và có hại cho người bệnh. 
                    <strong>Hãy tập trung hoàn toàn vào phác đồ điều trị nội khoa cá thể hóa cho ANOCA/INOCA tại Tab 'Điều trị nội khoa' (Phần 2).</strong></p>
                </div>
                """, unsafe_allow_html=True)
                
                # Render ANOCA pharmacotherapy details in Revasc/ANOCA tab
                st.subheader("💊 Phác đồ điều trị nội khoa cá thể hóa cho ANOCA / INOCA (Figure 15)")
                st.info(f"Phác đồ điều trị dựa trên Kiểu hình (Endotype): **{st.session_state.get('anoca_endotype', 'Chưa phân loại')}**")
                
                endotype_active = st.session_state.get('anoca_endotype', 'Chưa phân loại')
                if "Microvascular" in endotype_active or "MVA" in endotype_active:
                    st.markdown("""
                    *   **Thuốc chống đau ngực (Antianginal):** 
                        *   <span class='class-badge-2a'>Class IIa B</span> **Chẹn beta (Beta-blockers)** là điều trị đầu tay (ưu tiên nhóm chọn lọc tim như Nebivolol, Bisoprolol).
                        *   <span class='class-badge-2a'>Class IIa B</span> Phối hợp **Chẹn kênh canxi dihydropyridine (DHP-CCBs)** (như Amlodipine) nếu chẹn beta đơn trị chưa kiểm soát tốt triệu chứng.
                        *   <span class='class-badge-2b'>Class IIb B</span> Nitrates tác dụng kéo dài, Nicorandil hoặc Ranolazine nếu triệu chứng kháng trị.
                    *   **Thuốc bảo vệ mạch vành:** Khuyến cáo sử dụng **ACEi/ARB** và **Statin** để phục hồi chức năng nội mạc vi tuần hoàn (Class IIa B).
                    """, unsafe_allow_html=True)
                elif "Vasospastic" in endotype_active or "VSA" in endotype_active:
                    st.markdown("""
                    *   **Thuốc chống đau ngực (Antianginal):** 
                        *   <span class='class-badge-1'>Class I B</span> **Chẹn kênh canxi (CCBs)** liều cao (như Diltiazem, Amlodipine) là nền tảng điều trị quan trọng nhất để giãn động mạch co thắt.
                        *   <span class='class-badge-2a'>Class IIa B</span> Phối hợp thêm **Nitrates tác dụng kéo dài** nếu CCB đơn trị chưa đủ kiểm soát.
                    *   **🚨 CẢNH BÁO ĐỎ (Class III):** **TRÁNH DÙNG THUỐC CHẸN BETA ĐƠN TRỊ LIỆU** ở bệnh nhân co thắt mạch, vì gây co thắt trầm trọng hơn do kích thích alpha-adrenergic không đối kháng.
                    """, unsafe_allow_html=True)
                elif "Mixed" in endotype_active:
                    st.markdown("""
                    *   **Phối hợp điều trị:** 
                        *   Sử dụng **Chẹn kênh canxi (CCBs)** làm chủ đạo do kiểm soát được cả thành phần co thắt thượng tâm mạc và cải thiện vi tuần hoàn.
                        *   Có thể cân nhắc phối hợp chẹn beta cẩn thận nếu ưu thế thành phần đau thắt ngực vi mạch rõ rệt.
                    """)
                else:
                    st.markdown("*Chưa xác định kiểu hình ANOCA cụ thể hoặc không có chỉ định ANOCA. Vui lòng hoàn thành đánh giá ở Bước 3.*")
            else:
                st.subheader("1. Tiêu chuẩn chỉ định Tái thông mạch vành (Revascularization)")
                is_high_risk = st.session_state.get('high_risk_flag', False)
                if is_high_risk:
                    st.markdown("""
                    <div class='warning-box' style='border-left-color: #fd7e14;'>
                        <h4 style='color: #fd7e14; margin-top: 0;'>👉 CHỈ ĐỊNH TÁI THÔNG MẠCH VÀNH ĐỂ CẢI THIỆN TIÊN LƯỢNG (Class I A)</h4>
                        <p>Do bệnh nhân thuộc nhóm nguy cơ biến cố cao (Hẹp Thân chung trái LMS ≥50%, hẹp 3 nhánh mạch vành, hoặc hẹp đoạn gần LAD ≥70% hoặc diện tích thiếu máu rộng), can thiệp mạch vành qua da (PCI) hoặc phẫu thuật làm cầu nối chủ-vành (CABG) được chỉ định để kéo dài thời gian sống còn và ngăn ngừa biến cố tim mạch bất lợi.</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class='info-box'>
                        <strong>Xem xét Tái thông mạch vành để cải thiện triệu chứng (Class I A):</strong><br>
                        Ở những bệnh nhân không thuộc nhóm nguy cơ biến cố cao, chỉ định tái thông mạch vành được đặt ra khi:<br>
                        Triệu chứng đau thắt ngực hoặc khó thở vẫn dai dẳng, ảnh hưởng nặng đến chất lượng cuộc sống mặc dù đã điều trị nội khoa tối ưu (GDMT) với tối thiểu 2 nhóm thuốc kháng đau thắt ngực.
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("""
                **Các lưu ý kỹ thuật quan trọng của ESC 2024 (Mạch vành tắc nghẽn):**
                *   **Hẹp ranh giới (Intermediate stenosis):** Luôn đánh giá chức năng bằng **FFR** hoặc **iFR** trước khi quyết định can thiệp (Class I).
                *   **Can thiệp phức tạp:** Sử dụng các phương tiện chẩn đoán hình ảnh trong lòng mạch như **IVUS** hoặc **OCT** được khuyến cáo để hướng dẫn kỹ thuật can thiệp tối ưu (Class I).
                *   **Thảo luận nhóm tim mạch (Heart Team):** Khuyên dùng ở những ca tổn thương mạch vành đa nhánh, tổn thương thân chung phức tạp hoặc có đái tháo đường kèm theo để lựa chọn giữa PCI hay CABG (Class I).
                """)

        st.write("")
        if st.button("⬅️ Quay lại Bước 3", key="step4_prev_btn_v8"):
            set_step(3)

st.write("")
st.markdown("<p style='text-align: center; font-size: 0.8rem; color: #888;'>Phát triển chuyên sâu dựa trên Hướng dẫn của Hội Tim mạch Châu Âu (ESC) 2024 về quản lý Hội chứng mạch vành mạn | Thiết kế tương tác từng bước cho nhà lâm sàng</p>", unsafe_allow_html=True)
