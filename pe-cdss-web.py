import streamlit as st
import math

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Hỗ trợ Quyết định Lâm sàng PE - AHA/ACC 2026",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS cho giao diện y tế hiện đại, chuyên nghiệp, loại bỏ tối đa nhiễu
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        color: #1E3A8A;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2px;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
        text-align: center;
        margin-bottom: 25px;
    }
    .section-card {
        background-color: #F8FAFC;
        padding: 20px;
        border-radius: 8px;
        border-left: 5px solid #1E3A8A;
        margin-bottom: 15px;
    }
    .result-card {
        background-color: #EFF6FF;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #BFDBFE;
        margin-top: 15px;
    }
    .u-card {
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    .urgency-high {
        background-color: #FEF2F2;
        border-left: 5px solid #DC2626;
        color: #991B1B;
    }
    .urgency-medium {
        background-color: #FFFBEB;
        border-left: 5px solid #D97706;
        color: #92400E;
    }
    .urgency-low {
        background-color: #F0FDF4;
        border-left: 5px solid #16A34A;
        color: #166534;
    }
    .badge {
        background-color: #E2E8F0;
        color: #1E293B;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .summary-box {
        background-color: #F1F5F9;
        border: 1px solid #CBD5E1;
        padding: 12px;
        border-radius: 6px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-header'>🩺 CDSS THUYÊN TẮC PHỔI CẤP (AHA/ACC 2026)</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Hệ thống Hỗ trợ Quyết định Lâm sàng Từng bước (Step-by-Step Bedside Wizard v13)</div>", unsafe_allow_html=True)

# ==============================================================================
# KHỞI TẠO STATE MACHINE (SESSION STATE) CHO LUỒNG TỪNG BƯỚC ĐỘC LẬP
# ==============================================================================
if 'step' not in st.session_state:
    st.session_state.step = 1  # 1: Chẩn đoán, 2: Phân loại lâm sàng, 3: Điều trị

# State lưu trữ kết quả của các bước trước đó để không bị mất khi render lại
if 'is_pregnant' not in st.session_state:
    st.session_state.is_pregnant = False
if 'diag_result' not in st.session_state:
    st.session_state.diag_result = None  # "excluded" hoặc "ctpa_indicated"
if 'final_category' not in st.session_state:
    st.session_state.final_category = None  # Phân nhóm cuối cùng (A, B1, B2, C1, C2, C3, D1, D2, E1, E2)
if 'resp_modifier' not in st.session_state:
    st.session_state.resp_modifier = False

# Các biến điều khiển luồng rẽ nhánh trong Giai đoạn 2 (Huyết động ổn định)
if 'g2_stable_flow' not in st.session_state:
    st.session_state.g2_stable_flow = "cpes"  # "cpes" -> "organ_damage" -> "prognosis" -> "rv_biomarkers" / "hk_position"

# ==============================================================================
# THANH TIẾN TRÌNH QUY TRÌNH TỪNG BƯỚC CHUYÊN NGHIỆP
# ==============================================================================
step_cols = st.columns(3)
with step_cols[0]:
    if st.button("⚡ BƯỚC 1: CHẨN ĐOÁN & LOẠI TRỪ", use_container_width=True, type="primary" if st.session_state.step == 1 else "secondary"):
        st.session_state.step = 1
        st.rerun()
with step_cols[1]:
    if st.button("📊 BƯỚC 2: PHÂN LOẠI LÂM SÀNG AHA 2026", use_container_width=True, type="primary" if st.session_state.step == 2 else "secondary"):
        st.session_state.step = 2
        st.rerun()
with step_cols[2]:
    if st.button("💊 BƯỚC 3: CÁ THỂ HÓA ĐIỀU TRỊ & TÍNH LIỀU", use_container_width=True, type="primary" if st.session_state.step == 3 else "secondary"):
        st.session_state.step = 3
        st.rerun()

st.markdown("---")

# ==============================================================================
# BƯỚC 1: TIẾP CẬN CHẨN ĐOÁN BAN ĐẦU & LOẠI TRỪ PE
# ==============================================================================
if st.session_state.step == 1:
    st.subheader("⚡ GIAI ĐOẠN 1: CHẨN ĐOÁN & LOẠI TRỪ PE (D-dimer độc lập vs YEARS)")
    
    col1_1, col1_2 = st.columns([1, 1], gap="large")
    
    with col1_1:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.write("##### 📋 1. Đánh giá Xác suất lâm sàng tiền nghiệm (CPTP)")
        
        is_suspected = st.checkbox("Bệnh nhân có triệu chứng/dấu hiệu nghi ngờ PE cấp tính (khó thở, đau ngực, ho ra máu, ngất...)?", value=True)
        is_pregnant = st.checkbox("Bệnh nhân hiện tại đang mang thai?", value=st.session_state.is_pregnant)
        st.session_state.is_pregnant = is_pregnant
        
        cptp_category = "LOW"
        cptp_score = 0.0
        
        if is_suspected:
            score_type = st.radio("Chọn Thang điểm Đánh giá Xác suất tiền nghiệm:", ["Thang điểm Wells (Ưu tiên)", "Thang điểm Geneva Rút gọn"])
            
            if score_type == "Thang điểm Wells (Ưu tiên)":
                st.info("Tính điểm Wells:")
                w1 = st.checkbox("Lâm sàng có triệu chứng/dấu hiệu của DVT (sưng chân, đau dọc tĩnh mạch) (+3.0)")
                w2 = st.checkbox("PE là chẩn đoán khả thi nhất hoặc có khả năng xảy ra cao nhất (+3.0)")
                w3 = st.checkbox("Tần số tim > 100 chu kỳ/phút (+1.5)")
                w4 = st.checkbox("Bất động >= 3 ngày liên tục hoặc mới phẫu thuật trong vòng 4 tuần trước (+1.5)")
                w5 = st.checkbox("Tiền sử cá nhân đã từng bị DVT hoặc PE trước đây (+1.5)")
                w6 = st.checkbox("Bệnh nhân có ho ra máu (+1.0)")
                w7 = st.checkbox("Bệnh nhân có ung thư đang tiến triển (đang điều trị, điều trị giảm nhẹ, hoặc phát hiện trong 6 tháng) (+1.0)")
                
                cptp_score = (3.0 if w1 else 0.0) + (3.0 if w2 else 0.0) + (1.5 if w3 else 0.0) + (1.5 if w4 else 0.0) + (1.5 if w5 else 0.0) + (1.0 if w6 else 0.0) + (1.0 if w7 else 0.0)
                st.metric(label="Tổng điểm Wells", value=f"{cptp_score} điểm")
                
                if cptp_score < 2.0:
                    cptp_category = "LOW"
                elif cptp_score <= 6.0:
                    cptp_category = "INTERMEDIATE"
                else:
                    cptp_category = "HIGH"
                    
            else:
                st.info("Tính điểm Geneva Rút gọn (Simplified Revised Geneva):")
                g1 = st.checkbox("Tuổi > 65 tuổi (+1)")
                g2 = st.checkbox("Tiền sử cá nhân bị DVT hoặc PE (+1)")
                g3 = st.checkbox("Phẫu thuật (gây mê toàn thân) hoặc gãy xương chi dưới trong vòng 1 tháng qua (+1)")
                g4 = st.checkbox("Ung thư đang hoạt động/tiến triển (+1)")
                g5 = st.checkbox("Đau chân một bên (+1)")
                g6 = st.checkbox("Ho ra máu (+1)")
                g_hr = st.selectbox("Tần số tim bệnh nhân:", ["< 75 ck/phút (0 điểm)", "75 - 94 ck/phút (+1 điểm)", ">= 95 ck/phút (+1 điểm)"])
                g8 = st.checkbox("Đau khi ấn dọc hệ tĩnh mạch sâu ở chân kèm sưng chân một bên (+1)")
                
                hr_score = 0
                if "75 - 94" in g_hr: hr_score = 1
                elif ">= 95" in g_hr: hr_score = 1
                
                cptp_score = (1 if g1 else 0) + (1 if g2 else 0) + (1 if g3 else 0) + (1 if g4 else 0) + (1 if g5 else 0) + (1 if g6 else 0) + hr_score + (1 if g8 else 0)
                st.metric(label="Tổng điểm Geneva rút gọn", value=f"{cptp_score} điểm")
                
                if cptp_score <= 1:
                    cptp_category = "LOW"
                elif cptp_score <= 4:
                    cptp_category = "INTERMEDIATE"
                else:
                    cptp_category = "HIGH"
            
            # Hiển thị CPTP
            if cptp_category == "LOW":
                st.success("Xác suất lâm sàng tiền nghiệm: THẤP (<15% - Wells < 2 / Geneva ≤ 1)")
            elif cptp_category == "INTERMEDIATE":
                st.warning("Xác suất lâm sàng tiền nghiệm: TRUNG BÌNH (15% - 50% - Wells 2-6 / Geneva 2-4)")
            else:
                st.error("Xác suất lâm sàng tiền nghiệm: CAO (>50% - Wells > 6 / Geneva ≥ 5)")
        else:
            st.success("Không nghi ngờ PE cấp trên lâm sàng. Tìm nguyên nhân khác.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col1_2:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.write("##### 🔍 2. Thuật toán Loại trừ & Chỉ định Hình ảnh học")
        
        if is_suspected:
            any_perc_positive = False
            if cptp_category == "LOW":
                st.write("**Áp dụng Tiêu chuẩn loại trừ PE (PERC) tại giường:**")
                st.caption("Chỉ áp dụng khi xác suất lâm sàng tiền nghiệm (gestalt) <15% (hoặc Wells < 2). Nếu thỏa mãn tất cả 8 tiêu chí bên dưới (PERC âm tính), loại trừ PE hoàn toàn mà không cần xét nghiệm.")
                
                p1 = st.checkbox("Tuổi >= 50")
                p2 = st.checkbox("Tần số tim >= 100 chu kỳ/phút")
                p3 = st.checkbox("SpO2 < 95% ở khí trời")
                p4 = st.checkbox("Sưng đau chân một bên")
                p5 = st.checkbox("Ho ra máu")
                p6 = st.checkbox("Chấn thương hoặc phẫu thuật gần đây (đòi hỏi nhập viện trong 4 tuần trước)")
                p7 = st.checkbox("Tiền sử cá nhân bị DVT hoặc PE")
                p8 = st.checkbox("Sử dụng Hormone đường uống (Estrogen/thuốc tránh thai/liệu pháp hormone)")
                
                any_perc_positive = p1 or p2 or p3 or p4 or p5 or p6 or p7 or p8
                
                if not any_perc_positive:
                    st.markdown("<div class='u-card urgency-low'><strong>>>> KẾT QUẢ PERC: ÂM TÍNH (LOẠI TRỪ PE HOÀN TOÀN)</strong><br>Bệnh nhân thỏa mãn toàn bộ 8 tiêu chí loại trừ. LOẠI TRỪ PE TẠI GIƯỜNG BỆNH! Không cần làm D-dimer, không cần chụp CTPA.</div>", unsafe_allow_html=True)
                    st.session_state.diag_result = "excluded"
                    
                    if st.button("📊 Chuyển sang Bước 2: Phân loại & Điều trị (Bỏ qua loại trừ)", type="secondary", use_container_width=True):
                        st.session_state.step = 2
                        st.rerun()
                else:
                    st.markdown("<div class='u-card urgency-medium'><strong>>>> KẾT QUẢ PERC: DƯƠNG TÍNH</strong><br>Không thể loại trừ PE bằng PERC. Bắt buộc phải thực hiện xét nghiệm D-dimer theo một trong hai chiến lược độc lập bên dưới.</div>", unsafe_allow_html=True)
            
            # Cho phép chọn chiến lược D-dimer độc lập nếu CPTP <50% (Low/Intermediate)
            if cptp_category in ["LOW", "INTERMEDIATE"] and (cptp_category == "INTERMEDIATE" or any_perc_positive):
                st.write("**Lựa chọn Chiến lược D-dimer để loại trừ hoặc chỉ định chụp hình ảnh:**")
                st.warning("⚠️ CHÚ Ý: Chọn duy nhất 1 trong 2 chiến lược độc lập bên dưới. Tuyệt đối không trộn lẫn (không áp dụng hiệu chỉnh tuổi vào YEARS).")
                
                strategy = st.radio("Chọn chiến lược D-dimer:", [
                    "Chiến lược A: D-dimer theo độ tuổi (Age-Adjusted D-dimer)",
                    "Chiến lược B: Thuật toán YEARS (Pregnancy-adapted nếu có thai)"
                ])
                
                if strategy == "Chiến lược A: D-dimer theo độ tuổi (Age-Adjusted D-dimer)":
                    st.info("Chiến lược A: Age-Adjusted D-dimer (Class 2a, LOE B-R)")
                    age_years = st.number_input("Nhập tuổi bệnh nhân:", min_value=18, max_value=120, value=55, key="age_strategy_a")
                    
                    if age_years > 50:
                        cutoff_a = age_years * 10
                        st.write(f"Bệnh nhân > 50 tuổi. Ngưỡng cắt D-dimer hiệu chỉnh theo tuổi: **< {cutoff_a} ng/mL** (FEU).")
                    else:
                        cutoff_a = 500
                        st.write(f"Bệnh nhân ≤ 50 tuổi. Ngưỡng cắt D-dimer chuẩn: **< 500 ng/mL**.")
                        
                    d_dimer_val_a = st.number_input("Nhập nồng độ D-dimer thực tế đo được (ng/mL):", min_value=0, value=0, key="d_dimer_strategy_a")
                    
                    if d_dimer_val_a > 0:
                        if d_dimer_val_a < cutoff_a:
                            st.markdown(f"<div class='u-card urgency-low'><strong>>>> KẾT LUẬN: D-dimer ({d_dimer_val_a}) < Ngưỡng cắt ({cutoff_a})</strong><br>LOẠI TRỪ THUYÊN TẮC PHỔI (PE) THÀNH CÔNG! An toàn để KHÔNG chụp CTPA.</div>", unsafe_allow_html=True)
                            st.session_state.diag_result = "excluded"
                            if st.button("📊 Vẫn chuyển sang Phân loại & Điều trị (Giả định)", type="secondary", use_container_width=True):
                                st.session_state.step = 2
                                st.rerun()
                        else:
                            st.markdown(f"<div class='u-card urgency-high'><strong>>>> KẾT LUẬN: D-dimer ({d_dimer_val_a}) >= Ngưỡng cắt ({cutoff_a})</strong><br>VƯỢT NGƯỠNG AN TOÀN. CHỈ ĐỊNH CHỤP CTPA ĐỂ XÁC ĐỊNH CHẨN ĐOÁN!</div>", unsafe_allow_html=True)
                            st.session_state.diag_result = "ctpa_indicated"
                            if st.button("📊 Có kết quả CTPA? Chuyển sang Bước 2: Phân loại & Điều trị", type="primary", use_container_width=True):
                                st.session_state.step = 2
                                st.rerun()
                
                else: # YEARS
                    if is_pregnant:
                        st.info("Chiến lược B: Thuật toán YEARS thích ứng thai kỳ (Pregnancy-Adapted YEARS) (Class 2b, LOE B-R)")
                    else:
                        st.info("Chiến lược B: Thuật toán YEARS tiêu chuẩn (Class 2a, LOE B-R)")
                        
                    st.write("Đánh giá 3 tiêu chí YEARS:")
                    y1 = st.checkbox("1. Có dấu hiệu lâm sàng của DVT (sưng đau chân)?", key="years_y1")
                    y2 = st.checkbox("2. Có ho ra máu?", key="years_y2")
                    y3 = st.checkbox("3. PE là chẩn đoán khả thi nhất trên lâm sàng?", key="years_y3")
                    
                    years_count = (1 if y1 else 0) + (1 if y2 else 0) + (1 if y3 else 0)
                    st.write(f"Số tiêu chí YEARS thỏa mãn: **{years_count}/3**")
                    
                    years_cutoff = 1000 if years_count == 0 else 500
                    st.write(f"Ngưỡng cắt D-dimer theo YEARS (cố định): **{years_cutoff} ng/mL**")
                    
                    d_dimer_val_b = st.number_input("Nhập nồng độ D-dimer thực tế đo được (ng/mL):", min_value=0, value=0, key="d_dimer_strategy_b")
                    
                    if d_dimer_val_b > 0:
                        if d_dimer_val_b < years_cutoff:
                            st.markdown(f"<div class='u-card urgency-low'><strong>>>> KẾT LUẬN: D-dimer ({d_dimer_val_b}) < Ngưỡng YEARS ({years_cutoff})</strong><br>LOẠI TRỪ THUYÊN TẮC PHỔI (PE) THÀNH CÔNG! An toàn để không cần chụp CTPA.</div>", unsafe_allow_html=True)
                            st.session_state.diag_result = "excluded"
                            if is_pregnant and y1:
                                st.warning("👉 *Lưu ý thai kỳ:* Nếu thai phụ có triệu chứng chi dưới và siêu âm Doppler tĩnh mạch (CUS) dương tính, có thể điều trị kháng đông ngay mà không cần chụp CTPA.")
                            if st.button("📊 Vẫn chuyển sang Phân loại & Điều trị (Giả định)", type="secondary", use_container_width=True):
                                st.session_state.step = 2
                                st.rerun()
                        else:
                            st.markdown(f"<div class='u-card urgency-high'><strong>>>> KẾT LUẬN: D-dimer ({d_dimer_val_b}) >= Ngưỡng YEARS ({years_cutoff})</strong><br>VƯỢT NGƯỠNG AN TOÀN. CHỈ ĐỊNH CHỤP CTPA ĐỂ XÁC ĐỊNH CHẨN ĐOÁN!</div>", unsafe_allow_html=True)
                            st.session_state.diag_result = "ctpa_indicated"
                            if st.button("📊 Có kết quả CTPA? Chuyển sang Bước 2: Phân loại & Điều trị", type="primary", use_container_width=True):
                                st.session_state.step = 2
                                st.rerun()
            
            elif cptp_category == "HIGH":
                st.markdown("<div class='u-card urgency-high'><strong>>>> KẾT LUẬN: XÁC SUẤT LÂM SÀNG CỰC KỲ CAO (>50%)</strong><br><strong>HÀNH ĐỘNG NGAY:</strong> Chỉ định chụp CT động mạch phổi (CTPA) khẩn cấp lập tức! KHÔNG ĐƯỢC làm D-dimer để tránh âm tính giả nguy hiểm tính mạng.</div>", unsafe_allow_html=True)
                st.session_state.diag_result = "ctpa_indicated"
                if st.button("📊 Chuyển sang Bước 2: Phân loại & Điều trị sau khi có CTPA", type="primary", use_container_width=True):
                    st.session_state.step = 2
                    st.rerun()
        else:
            st.info("Vui lòng chọn dấu hiệu nghi ngờ để thực hiện thuật toán loại trừ.")
        st.markdown("</div>", unsafe_allow_html=True)

    # Nút chuyển tiếp nhanh ở cuối trang
    col_nav = st.columns([4, 1])
    with col_nav[1]:
        if st.button("Tiếp tục sang GĐ 2 ➡️", use_container_width=True):
            st.session_state.step = 2
            st.rerun()

# ==============================================================================
# BƯỚC 2: PHÂN LOẠI LÂM SÀNG CẤP TÍNH AHA/ACC 2026 (LUỒNG QUYẾT ĐỊNH TUẦN TỰ)
# ==============================================================================
elif st.session_state.step == 2:
    st.subheader("📊 GIAI ĐOẠN 2: PHÂN LOẠI LÂM SÀNG CẤP TÍNH AHA/ACC 2026")
    
    col2_1, col2_2 = st.columns([1, 1], gap="large")
    
    with col2_1:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.write("##### 🧬 Đánh giá Huyết động học & Tim phổi cấp cứu")
        
        # 1. Trạng thái huyết động chính
        primary_hemo = st.selectbox("1. Hãy chọn trạng thái Huyết động chính của bệnh nhân:", [
            "Huyết động ổn định (Huyết áp bình thường)",
            "Thuyên tắc phổi phát hiện tình cờ, hoàn toàn không có triệu chứng nghi ngờ (Category A - Subclinical PE)",
            "Tụt huyết áp thoáng qua (<15 phút, tự hồi phục nhanh hoặc đáp ứng nhanh sau bù dịch, không giảm tưới máu cơ quan)",
            "Tụt huyết áp kéo dài / Sốc tim thực sự (Huyết áp tâm thu <90 mmHg hoặc giảm >40 mmHg kéo dài >=15 phút, hoặc cần thuốc vận mạch để duy trì HA)",
            "Ngừng tuần hoàn hoặc Sốc tim kháng trị (Cần hồi sức tim phổi CPR tích cực hoặc vận mạch liều tối đa)"
        ])
        
        # Xử lý các nhánh huyết động không ổn định
        if primary_hemo == "Ngừng tuần hoàn hoặc Sốc tim kháng trị (Cần hồi sức tim phổi CPR tích cực hoặc vận mạch liều tối đa)":
            st.session_state.final_category = "E2"
            st.markdown("<div class='u-card urgency-high'><strong>>>> CHẨN ĐOÁN LÂM SÀNG: NHÓM E2 (Suy tim phổi hoàn toàn - Sụp đổ tuần hoàn)</strong><br>Kích hoạt ngay lập tức đội phản ứng nhanh PERT và hồi sức tim phổi CPR nâng cao.</div>", unsafe_allow_html=True)
            
            # Sàng lọc suy hô hấp (Modifier R) cho nhóm E
            st.write("---")
            st.write("##### 📢 Đánh giá Modifier R cho nhóm E")
            r_e = st.checkbox("Đang cần thông khí áp lực dương không xâm lấn (NIV/BiPAP) HOẶC đang phải thông khí xâm lấn (đặt nội khí quản thở máy)?")
            st.session_state.resp_modifier = r_e
            
            if st.button("Xác nhận & Đi tới Bước 3: Điều trị", type="primary", key="btn_confirm_e2", use_container_width=True):
                st.session_state.step = 3
                st.rerun()
            
        elif primary_hemo == "Tụt huyết áp kéo dài / Sốc tim thực sự (Huyết áp tâm thu <90 mmHg hoặc giảm >40 mmHg kéo dài >=15 phút, hoặc cần thuốc vận mạch để duy trì HA)":
            st.session_state.final_category = "E1"
            st.markdown("<div class='u-card urgency-high'><strong>>>> CHẨN ĐOÁN LÂM SÀNG: NHÓM E1 (Suy tim phổi hoàn toàn - Sốc tim thực sự)</strong><br>Cần theo dõi sát tại ICU/CCU và chuẩn bị phương án tiêu sợi huyết hoặc can thiệp cơ học MT.</div>", unsafe_allow_html=True)
            
            # Sàng lọc suy hô hấp (Modifier R) cho nhóm E
            st.write("---")
            st.write("##### 📢 Đánh giá Modifier R cho nhóm E")
            r_e = st.checkbox("Đang cần thông khí áp lực dương không xâm lấn (NIV/BiPAP) HOẶC đang phải thông khí xâm lấn (đặt nội khí quản thở máy)?")
            st.session_state.resp_modifier = r_e
            
            if st.button("Xác nhận & Đi tới Bước 3: Điều trị", type="primary", key="btn_confirm_e1", use_container_width=True):
                st.session_state.step = 3
                st.rerun()

        elif primary_hemo == "Thuyên tắc phổi phát hiện tình cờ, hoàn toàn không có triệu chứng nghi ngờ (Category A - Subclinical PE)":
            st.session_state.final_category = "A"
            st.markdown("<div class='u-card urgency-low'><strong>>>> CHẨN ĐOÁN LÂM SÀNG: NHÓM A (Dưới lâm sàng - Subclinical PE)</strong><br>Thuyên tắc phổi phát hiện tình cờ trên phim chụp CTPA vì bệnh lý khác, hoàn toàn không có triệu chứng nghi ngờ PE. Đủ điều kiện xem xét điều trị ngoại trú an toàn bằng DOACs đường uống (Class 1).</div>", unsafe_allow_html=True)
            st.session_state.resp_modifier = False
            
            if st.button("Xác nhận & Đi tới Bước 3: Điều trị", type="primary", key="btn_confirm_a", use_container_width=True):
                st.session_state.step = 3
                st.rerun()

        elif primary_hemo == "Tụt huyết áp thoáng qua (<15 phút, tự hồi phục nhanh hoặc đáp ứng nhanh sau bù dịch, không giảm tưới máu cơ quan)":
            # Chờ đánh giá giảm tưới máu để phân biệt D1 và D2
            st.info("👉 Bạn đã chọn Tụt huyết áp thoáng qua. Hệ thống cần rà soát xem bệnh nhân có biểu hiện giảm tưới máu mô hay không để phân loại chính xác giữa D1 và D2.")
            st.session_state.g2_stable_flow = "organ_damage"
            
        else: # Huyết động ổn định
            st.success("Huyết áp bình thường. Hệ thống chuyển sang luồng đánh giá tuần tự để loại trừ Sốc ẩn (D2) trước khi tính thang điểm tiên lượng.")
            # Đảm bảo luồng đi đúng tuần tự từ CPES -> Organ Damage -> Prognosis
            # Nếu trước đó đang bị kẹt ở trạng thái khác thì reset về cpes
            if st.session_state.g2_stable_flow not in ["cpes", "organ_damage", "prognosis", "rv_biomarkers", "hk_position"]:
                st.session_state.g2_stable_flow = "cpes"

        st.markdown("</div>", unsafe_allow_html=True)
        
        # ==============================================================================
        # LUỒNG TUẦN TỰ CHO HUYẾT ÁP BÌNH THƯỜNG / TỤT HA THOÁNG QUA
        # ==============================================================================
        if primary_hemo in ["Huyết động ổn định (Huyết áp bình thường)", "Tụt huyết áp thoáng qua (<15 phút, tự hồi phục nhanh hoặc đáp ứng nhanh sau bù dịch, không giảm tưới máu cơ quan)"]:
            
            # --------------------------------------------------------------------------
            # BƯỚC 2.1: ĐÁNH GIÁ THANG ĐIỂM CPES (Chỉ hiện khi huyết áp ổn định)
            # --------------------------------------------------------------------------
            if st.session_state.g2_stable_flow == "cpes" and primary_hemo == "Huyết động ổn định (Huyết áp bình thường)":
                st.markdown("<div class='section-card'>", unsafe_allow_html=True)
                st.write("##### 📊 BƯỚC 2.1: Đánh giá Thang điểm CPES (Composite Pulmonary Embolism Shock)")
                st.caption("Thang điểm CPES (0-6 điểm) giúp sàng lọc sớm nguy cơ tiến triển thành Sốc ẩn ở bệnh nhân có huyết áp ổn định.")
                
                c1 = st.checkbox("1. Tăng men tim Troponin tim (+1)")
                c2 = st.checkbox("2. Tăng peptide lợi niệu BNP hoặc NT-proBNP (+1)")
                c3 = st.checkbox("3. Giảm chức năng RV mức độ trung bình hoặc nặng trên siêu âm (+1)")
                c4 = st.checkbox("4. Có gánh nặng huyết khối trung tâm (Saddle PE) trên CTPA (+1)")
                c5 = st.checkbox("5. Có huyết khối tĩnh mạch sâu (DVT) đoạn gần kèm theo (+1)")
                c6 = st.checkbox("6. Tần số tim >= 100 chu kỳ/phút (+1)")
                
                cpes_score = sum([c1, c2, c3, c4, c5, c6])
                st.metric("Tổng điểm CPES", f"{cpes_score}/6 điểm")
                
                if cpes_score == 6:
                    st.markdown("<div class='u-card urgency-high'><strong>>>> ĐẠT ĐIỂM TỐI ĐA CPES 6/6!</strong><br>Bệnh nhân đạt điểm CPES 6/6 -> Tự động phân nhóm vào <strong>Nhóm D2 (Sốc ẩn - Nguy cơ rất cao)</strong> theo AHA/ACC 2026. Bạn không cần đánh giá thêm các thang điểm tiên lượng khác.</div>", unsafe_allow_html=True)
                    st.session_state.final_category = "D2"
                    
                    # Sàng lọc suy hô hấp (Modifier R) cho nhóm D
                    st.write("---")
                    st.write("##### 📢 Đánh giá Modifier R cho nhóm D")
                    r_d = st.checkbox("Đang cần thở oxy dòng cao HFNC (>6 L/phút) HOẶC đang phải sử dụng mặt nạ không thở lại (NRB)?")
                    st.session_state.resp_modifier = r_d
                    
                    if st.button("Xác nhận & Đi tới Bước 3: Điều trị", type="primary", use_container_width=True):
                        st.session_state.step = 3
                        st.rerun()
                else:
                    st.info("CPES < 6. Bấm nút dưới đây để tiếp tục sàng lọc các dấu hiệu tổn thương cơ quan / giảm tưới máu.")
                    if st.button("Xác nhận CPES & Đánh giá tổn thương cơ quan ➡️", type="primary", use_container_width=True):
                        st.session_state.g2_stable_flow = "organ_damage"
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

            # --------------------------------------------------------------------------
            # BƯỚC 2.2: ĐÁNH GIÁ TỔN THƯƠNG CƠ QUAN / GIẢM TƯỚI MÁU (SỐC ẨN)
            # --------------------------------------------------------------------------
            elif st.session_state.g2_stable_flow == "organ_damage":
                st.markdown("<div class='section-card'>", unsafe_allow_html=True)
                st.write("##### 🩸 BƯỚC 2.2: Đánh giá Tổn thương cơ quan & Giảm tưới máu mô (Sốc ẩn)")
                st.caption("Rà soát các bằng chứng giảm tưới máu hệ thống đơn độc ngay cả khi huyết áp đang bình thường.")
                
                opt_lactate = st.checkbox("Nồng độ Lactate huyết thanh > 2.0 mmol/L")
                opt_aki = st.checkbox("Suy thận cấp (AKI) (Creatinine tăng >= 0.3 mg/dL hoặc gấp 1.5 lần nền trong 24h)")
                opt_oliguria = st.checkbox("Thiểu niệu tiến triển (Lượng nước tiểu < 0.5 mL/kg/giờ kéo dài >= 2 giờ)")
                opt_mental = st.checkbox("Thay đổi trạng thái tâm thần cấp tính (lờ đờ, u ám, vật vã do thiếu máu não)")
                opt_ci_map = st.checkbox("Huyết áp trung bình MAP < 60 mmHg HOẶC Chỉ số tim (Cardiac Index) <= 2.2 L/min/m²")
                
                has_hypoperfusion = opt_lactate or opt_aki or opt_oliguria or opt_mental or opt_ci_map
                
                if has_hypoperfusion:
                    # Bất kỳ dấu hiệu giảm tưới máu nào xuất hiện -> D2 (Sốc ẩn)
                    st.session_state.final_category = "D2"
                    st.markdown("<div class='u-card urgency-high'><strong>>>> CHẨN ĐOÁN LÂM SÀNG: NHÓM D2 (Sốc ẩn - Incipient Cardiopulmonary Failure)</strong><br>Có bằng chứng giảm tưới máu mô/tổn thương cơ quan đích mặc dù huyết áp được bù trừ. Chuyển sang hồi sức tích cực và theo dõi sát.</div>", unsafe_allow_html=True)
                    
                    # Sàng lọc suy hô hấp (Modifier R) cho nhóm D
                    st.write("---")
                    st.write("##### 📢 Đánh giá Modifier R cho nhóm D")
                    r_d = st.checkbox("Đang cần thở oxy dòng cao HFNC (>6 L/phút) HOẶC đang phải sử dụng mặt nạ không thở lại (NRB)?")
                    st.session_state.resp_modifier = r_d
                    
                    if st.button("Xác nhận & Đi tới Bước 3: Điều trị", type="primary", use_container_width=True):
                        st.session_state.step = 3
                        st.rerun()
                else:
                    if primary_hemo == "Tụt huyết áp thoáng qua (<15 phút, tự hồi phục nhanh hoặc đáp ứng nhanh sau bù dịch, không giảm tưới máu cơ quan)":
                        # Tụt HA thoáng qua và KHÔNG có giảm tưới máu -> D1
                        st.session_state.final_category = "D1"
                        st.markdown("<div class='u-card urgency-medium'><strong>>>> CHẨN ĐOÁN LÂM SÀNG: NHÓM D1 (Tụt huyết áp thoáng qua)</strong><br>Huyết động bắt đầu có biểu hiện mất bù thoáng qua nhưng chưa có tổn thương tạng/giảm tưới máu mô thực sự.</div>", unsafe_allow_html=True)
                        
                        # Sàng lọc suy hô hấp (Modifier R) cho nhóm D
                        st.write("---")
                        st.write("##### 📢 Đánh giá Modifier R cho nhóm D")
                        r_d = st.checkbox("Đang cần thở oxy dòng cao HFNC (>6 L/phút) HOẶC đang phải sử dụng mặt nạ không thở lại (NRB)?")
                        st.session_state.resp_modifier = r_d
                        
                        if st.button("Xác nhận & Đi tới Bước 3: Điều trị", type="primary", use_container_width=True):
                            st.session_state.step = 3
                            st.rerun()
                    else:
                        st.info("Không phát hiện dấu hiệu giảm tưới máu mô. Bệnh nhân an toàn với Sốc ẩn. Bấm nút dưới đây để chuyển sang đánh giá các thang điểm tiên lượng lâm sàng.")
                        if st.button("Xác nhận Không có giảm tưới máu & Đánh giá Tiên lượng ➡️", type="primary", use_container_width=True):
                            st.session_state.g2_stable_flow = "prognosis"
                            st.rerun()
                
                # Nút quay lại bước trước để tránh bế tắc
                if st.button("⬅️ Quay lại đánh giá CPES", type="secondary"):
                    st.session_state.g2_stable_flow = "cpes"
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

            # --------------------------------------------------------------------------
            # BƯỚC 2.3: ĐÁNH GIÁ THANG ĐIỂM TIÊN LƯỢNG LÂM SÀNG (LỰA CHỌN 1 TRONG 4 THANG)
            # --------------------------------------------------------------------------
            elif st.session_state.g2_stable_flow == "prognosis":
                st.markdown("<div class='section-card'>", unsafe_allow_html=True)
                st.write("##### 📋 BƯỚC 2.3: Đánh giá Thang điểm Tiên lượng Lâm sàng")
                st.caption("Do không có giảm tưới máu/sốc ẩn, bệnh nhân sẽ được phân loại vào Nhóm B (Nguy cơ thấp) hoặc Nhóm C (Nguy cơ trung bình). Hãy lựa chọn 1 thang điểm duy nhất để đánh giá:")
                
                score_method = st.selectbox("Chọn thang điểm tiên lượng lâm sàng:", [
                    "sPESI (Simplified PESI) - Rút gọn, nhanh chóng",
                    "PESI Đầy đủ (11 tiêu chí)",
                    "Tiêu chí Hestia (11 mục loại trừ chuẩn)",
                    "Thang điểm Bova (Dành cho bệnh nhân huyết động ổn)"
                ])
                
                is_clinical_high = False
                
                if "sPESI" in score_method:
                    st.info("Tính điểm sPESI (Mỗi tiêu chí dương tính tính 1 điểm):")
                    sp1 = st.checkbox("Tuổi > 80")
                    sp2 = st.checkbox("Tiền sử ung thư đang tiến triển")
                    sp3 = st.checkbox("Tiền sử bệnh tim phổi mạn tính (suy tim mạn/COPD/bệnh phổi kẽ...)")
                    sp4 = st.checkbox("Tần số tim >= 110 chu kỳ/phút")
                    sp5 = st.checkbox("Huyết áp tâm thu < 100 mmHg")
                    sp6 = st.checkbox("SpO2 < 90% (hoặc cần oxy hỗ trợ)")
                    
                    spesi_score = sum([sp1, sp2, sp3, sp4, sp5, sp6])
                    st.metric("Tổng điểm sPESI", f"{spesi_score} điểm")
                    is_clinical_high = spesi_score >= 1
                    
                elif "PESI Đầy đủ" in score_method:
                    st.info("Tính điểm PESI Đầy đủ (11 tiêu chí chuẩn):")
                    pesi_age = st.number_input("Nhập tuổi bệnh nhân:", min_value=18, max_value=120, value=60, key="pesi_age_raw")
                    pesi_gender = st.radio("Giới tính sinh học:", ["Nam (+10)", "Nữ (0)"])
                    pesi_cancer = st.checkbox("Ung thư tiến triển (+30)")
                    pesi_hf = st.checkbox("Tiền sử suy tim mạn tính (+10)")
                    pesi_lung = st.checkbox("Bệnh phổi mạn tính (+10)")
                    pesi_hr = st.checkbox("Tần số tim >= 110 ck/phút (+20)")
                    pesi_sbp = st.checkbox("Huyết áp tâm thu < 100 mmHg (+30)")
                    pesi_rr = st.checkbox("Tần số thở >= 30 lần/phút (+20)")
                    pesi_temp = st.checkbox("Nhiệt độ cơ thể < 36 độ C (+20)")
                    pesi_mental = st.checkbox("Thay đổi trạng thái tâm thần (lẫn lộn, u ám, ngủ gà) (+60)")
                    pesi_spo2 = st.checkbox("SpO2 < 90% (+20)")
                    
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
                    h1 = st.checkbox("1. Huyết động không ổn định (cần vận mạch, bù dịch truyền, đặt ống, CPR)?")
                    h2 = st.checkbox("2. Cần dùng tiêu sợi huyết hoặc phẫu thuật lấy huyết khối?")
                    h3 = st.checkbox("3. Nguy cơ chảy máu cao hoặc đang chảy máu hoạt động?")
                    h4 = st.checkbox("4. Cần thở oxy hỗ trợ liên tục >24h để duy trì SpO2 >90%?")
                    h5 = st.checkbox("5. PE khởi phát khi đang dùng kháng đông liều đầy đủ?")
                    h6 = st.checkbox("6. Đau ngực dữ dội cần dùng thuốc giảm đau opioid đường truyền tĩnh mạch >24h?")
                    h7 = st.checkbox("7. Có lý do y khoa hoặc xã hội cần nhập viện kéo dài >24h (ví dụ: nhiễm trùng đồng mắc)?")
                    h8 = st.checkbox("8. Độ thanh thải Creatinine CrCl < 30 mL/phút?")
                    h9 = st.checkbox("9. Có suy gan nặng?")
                    h10 = st.checkbox("10. Bệnh nhân đang mang thai?")
                    h11 = st.checkbox("11. Tiền sử giảm tiểu cầu do Heparin (HIT)?")
                    
                    hestia_positive = any([h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11])
                    if hestia_positive:
                        st.error("Hestia dương tính (Có ít nhất 1 câu trả lời 'Có'): Bệnh nhân không thể điều trị ngoại trú -> Xếp vào nguy cơ trung bình (Nhóm C).")
                        is_clinical_high = True
                    else:
                        st.success("Tất cả câu trả lời là 'Không'. Hestia âm tính: Đủ điều kiện xem xét điều trị ngoại trú an toàn (Nhóm B).")
                        is_clinical_high = False
                        
                else: # Bova
                    st.info("Tính điểm Bova (Dành cho bệnh nhân huyết động ổn định - Table 6):")
                    b1 = st.checkbox("1. Tần số tim >= 110 chu kỳ/phút (+1)")
                    b2 = st.checkbox("2. Huyết áp tâm thu 90 - 100 mmHg (+2)")
                    b3 = st.checkbox("3. Có tăng men tim Troponin (+2)")
                    b4 = st.checkbox("4. Có rối loạn chức năng thất phải trên siêu âm hoặc CTPA (+2)")
                    
                    bova_score = (1 if b1 else 0) + (2 if b2 else 0) + (2 if b3 else 0) + (2 if b4 else 0)
                    st.metric("Tổng điểm Bova", f"{bova_score} điểm")
                    is_clinical_high = bova_score > 4 # Bova Stage III (>4đ) là nguy cơ trung bình-cao (C)

                st.write("---")
                if is_clinical_high:
                    st.markdown("<div class='u-card urgency-medium'><strong>KẾT QUẢ ĐÁNH GIÁ: LÂM SÀNG NGUY CƠ CAO (Category C)</strong><br>Thang điểm tiên lượng lâm sàng chỉ ra nguy cơ cao. Bệnh nhân được xếp vào Nhóm C. Hãy bấm nút dưới đây để đánh giá Thất phải (RV) và Biomarkers để phân nhóm sâu hơn (C1, C2, C3).</div>", unsafe_allow_html=True)
                    if st.button("Đánh giá Thất phải (RV) & Biomarkers ➡️", type="primary", use_container_width=True):
                        st.session_state.g2_stable_flow = "rv_biomarkers"
                        st.rerun()
                else:
                    st.markdown("<div class='u-card urgency-low'><strong>KẾT QUẢ ĐÁNH GIÁ: LÂM SÀNG NGUY CƠ THẤP (Category B)</strong><br>Thang điểm tiên lượng lâm sàng chỉ ra nguy cơ thấp. Bệnh nhân được xếp vào Nhóm B. Hãy bấm nút dưới đây để đánh giá vị trí huyết khối để phân loại B1 hay B2.</div>", unsafe_allow_html=True)
                    if st.button("Đánh giá vị trí huyết khối ➡️", type="primary", use_container_width=True):
                        st.session_state.g2_stable_flow = "hk_position"
                        st.rerun()
                        
                if st.button("⬅️ Quay lại đánh giá Tổn thương cơ quan", type="secondary"):
                    st.session_state.g2_stable_flow = "organ_damage"
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

            # --------------------------------------------------------------------------
            # BƯỚC 2.4: ĐÁNH GIÁ RV & BIOMARKERS (CHỈ CHO NHÓM C)
            # --------------------------------------------------------------------------
            elif st.session_state.g2_stable_flow == "rv_biomarkers":
                st.markdown("<div class='section-card'>", unsafe_allow_html=True)
                st.write("##### 🧬 BƯỚC 2.4: Đánh giá Thất phải (RV) & Biomarkers (Nhóm C)")
                st.caption("Xác định mức độ tổn thương tim phải để chia nhóm C thành C1, C2, C3.")
                
                st.write("**1. Đánh giá chi tiết Rối loạn chức năng Thất phải (RV) (Siêu âm/CT):**")
                rv_ct = st.checkbox("Tỷ lệ đường kính RV/LV >= 1.0 trên CTPA hoặc siêu âm 4 buồng")
                rv_echo_1 = st.checkbox("TAPSE < 17 mm (co bóp dọc vòng van 3 lá)")
                rv_echo_2 = st.checkbox("Dấu hiệu McConnell (giảm động thành tự do RV, bảo tồn vùng mỏm)")
                rv_echo_3 = st.checkbox("Vận tốc sóng S' TDI van 3 lá < 9.5 cm/s")
                rv_echo_4 = st.checkbox("Vận tốc hở 3 lá TR >= 2.9 m/s (gợi ý tăng áp phổi cấp)")
                rv_echo_5 = st.checkbox("Tĩnh mạch chủ dưới IVC giãn (>21mm) và xẹp < 50% khi hít vào")
                rv_echo_6 = st.checkbox("Vách liên thất dẹt nghịch thường trong thì tâm thu/tâm trương")
                
                has_rv_dysfunction = rv_ct or rv_echo_1 or rv_echo_2 or rv_echo_3 or rv_echo_4 or rv_echo_5 or rv_echo_6
                
                if has_rv_dysfunction:
                    st.error("Xác nhận: Có rối loạn chức năng/Quá tải thất phải (RV Dysfunction)")
                else:
                    st.success("Xác nhận: Thất phải (RV) hoạt động bình thường")
                
                st.write("---")
                st.write("**2. Đánh giá dấu ấn sinh học cơ tim (Biomarkers):**")
                has_elevated_biomarkers = st.checkbox("Có tăng men tim Troponin (I/T) HOẶC tăng peptide lợi niệu (BNP/NT-proBNP)?")
                
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
                r_c = st.checkbox("SpO2 < 90% ở khí trời, HOẶC nhịp thở (RR) >= 30 lần/phút, HOẶC đang cần bổ sung oxy hỗ trợ thông thường (qua gọng kính/mặt nạ)?")
                st.session_state.resp_modifier = r_c
                
                if st.button("Xác nhận Phân nhóm & Chuyển sang Bước 3: Điều trị", type="primary", use_container_width=True):
                    st.session_state.step = 3
                    st.rerun()
                    
                if st.button("⬅️ Quay lại chọn Thang điểm tiên lượng", type="secondary"):
                    st.session_state.g2_stable_flow = "prognosis"
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

            # --------------------------------------------------------------------------
            # BƯỚC 2.5: ĐÁNH GIÁ VỊ TRÍ HUYẾT KHỐI (CHỈ CHO NHÓM B)
            # --------------------------------------------------------------------------
            elif st.session_state.g2_stable_flow == "hk_position":
                st.markdown("<div class='section-card'>", unsafe_allow_html=True)
                st.write("##### 🔍 BƯỚC 2.5: Đánh giá vị trí huyết khối cho nhóm B")
                st.caption("Xác định xem bệnh nhân bị thuyên tắc ở phân thùy trở lên hay chỉ dưới phân thùy.")
                
                is_subsegmental = st.checkbox("Huyết khối chỉ khu trú ở nhánh dưới phân thùy (Subsegmental PE)?")
                if is_subsegmental:
                    st.session_state.final_category = "B1"
                else:
                    st.session_state.final_category = "B2"
                
                st.write("---")
                st.success(f"Xác lập phân nhóm: **Nhóm {st.session_state.final_category}**")
                st.session_state.resp_modifier = False # Nhóm B mặc định không có suy hô hấp nặng
                
                if st.button("Xác nhận Phân nhóm & Chuyển sang Bước 3: Điều trị", type="primary", use_container_width=True):
                    st.session_state.step = 3
                    st.rerun()
                    
                if st.button("⬅️ Quay lại chọn Thang điểm tiên lượng", type="secondary"):
                    st.session_state.g2_stable_flow = "prognosis"
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

    with col2_2:
        st.subheader("📋 Tóm tắt Phân loại hiện tại")
        
        # Tạo bảng tóm tắt nhanh trạng thái lâm sàng đang tích chọn
        if primary_hemo != "Huyết động ổn định (Huyết áp bình thường)":
            st.info(f"Trạng thái Huyết động chính: **{primary_hemo}**")
        else:
            st.success("Huyết động: **Ổn định (Huyết áp bình thường)**")
            
        st.write(f"Luồng phân loại đang ở: **Bước {st.session_state.g2_stable_flow.upper()}**")
        
        # Hiển thị tiến trình tóm tắt giúp bác sĩ không bị lạc hướng
        st.markdown("""
        **Quy trình Phân loại Tuần tự chuẩn của Hướng dẫn AHA/ACC 2026:**
        1. **Huyết động:** Nếu Ngừng tuần hoàn / Sốc thực sự -> Xếp thẳng **Nhóm E (E1/E2)**.
        2. **CPES (Với người huyết áp ổn định):** Nếu đạt **6/6** điểm -> Xếp thẳng **Nhóm D2 (Sốc ẩn)**.
        3. **Tổn thương tạng (Với người CPES < 6 hoặc tụt HA thoáng qua):** Nếu có bất kỳ tiêu chí nào (Lactate > 2, AKI, thiểu niệu,...) -> Xếp thẳng **Nhóm D2 (Sốc ẩn)**. Nếu tụt HA thoáng qua đơn thuần -> **Nhóm D1**.
        4. **Thang điểm tiên lượng (Với người HA ổn định, không giảm tưới máu):** Chấm 1 trong 4 thang điểm (sPESI, PESI, Hestia, Bova). 
            * Nếu thấp -> Xếp vào **Nhóm B** (Tiếp tục chia B1/B2 dựa trên vị trí huyết khối).
            * Nếu cao -> Xếp vào **Nhóm C** (Tiếp tục chia C1/C2/C3 dựa trên Thất phải và Men tim).
        """)
        
        if st.session_state.final_category:
            r_suffix = "R" if st.session_state.resp_modifier else ""
            st.markdown(f"<div class='result-card'><h3>KẾT QUẢ ĐÁNH GIÁ TẠM THỜI:<br><span style='color:#DC2626;'>NHÓM {st.session_state.final_category}{r_suffix}</span></h3></div>", unsafe_allow_html=True)

# ==============================================================================
# BƯỚC 3: CÁ THỂ HÓA ĐIỀU TRỊ & TÍNH LIỀU ĐIỀU TRỊ CỤ THỂ
# ==============================================================================
elif st.session_state.step == 3:
    st.subheader("💊 GIAI ĐOẠN 3: CÁ THỂ HÓA ĐIỀU TRỊ & TÍNH LIỀU KHÁNG ĐÔNG")
    
    if not st.session_state.final_category:
        st.error("🚨 Bạn chưa hoàn thành Giai đoạn 2: Phân loại Lâm sàng. Vui lòng bấm vào nút 'BƯỚC 2' ở trên để tiến hành phân tầng nguy cơ cho bệnh nhân trước.")
    else:
        col3_1, col3_2 = st.columns([1, 1], gap="large")
        
        with col3_1:
            st.markdown("<div class='section-card'>", unsafe_allow_html=True)
            st.write("##### 🧬 1. Thông số Sinh học & Tình huống đặc biệt")
            
            col_w, col_h, col_cr = st.columns(3)
            with col_w:
                weight = st.number_input("Cân nặng (kg):", min_value=30, max_value=250, value=70)
            with col_h:
                height = st.number_input("Chiều cao (cm):", min_value=100, max_value=250, value=165)
            with col_cr:
                scr = st.number_input("Creatinine huyết thanh (mg/dL):", min_value=0.2, max_value=15.0, value=1.0)
                
            age_calc = st.number_input("Tuổi bệnh nhân (để tính CrCl):", min_value=18, max_value=120, value=60, key="age_calc")
            gender_calc = st.radio("Giới tính sinh học:", ["Nam", "Nữ"], horizontal=True)
            
            # Tính toán chỉ số sinh học
            bmi = weight / ((height/100)**2)
            gender_mul = 0.85 if gender_calc == "Nữ" else 1.0
            crcl = ((140 - age_calc) * weight * gender_mul) / (72 * scr)
            
            st.write(f"Chỉ số BMI: **{bmi:.1f} kg/m²** | Độ thanh thải Creatinine (CrCl): **{crcl:.1f} mL/phút**")
            
            st.write("---")
            st.write("**💼 Tình huống lâm sàng đặc biệt:**")
            has_aps = st.checkbox("Bệnh nhân mắc Hội chứng kháng Phospholipid (APS) xác định?", key="has_aps")
            is_pregnant_t2 = st.checkbox("Bệnh nhân đang mang thai hoặc cho con bú?", value=st.session_state.is_pregnant, key="is_pregnant_t2")
            st.session_state.is_pregnant = is_pregnant_t2
            has_cancer = st.checkbox("Bệnh nhân mắc ung thư đang hoạt động / tiến triển (Cancer-associated thrombosis)?", key="has_cancer")
            has_drug_interactions = st.checkbox("Đang sử dụng thuốc tương tác mạnh (như Ketoconazole, Itraconazole, Ritonavir, Rifampicin, Phenytoin, Carbamazepine)?", key="has_drug_interactions")
            
            # Tự động đánh giá tiêu chí giảm liều Apixaban
            apix_criteria_count = sum([age_calc >= 80, weight <= 60, scr >= 1.5])
            apix_maint_dose = "2.5mg uống x 2 lần/ngày" if apix_criteria_count >= 2 else "5mg uống x 2 lần/ngày"
            apix_dose_note = " (Đã tự động giảm liều xuống 2.5mg x 2 do thỏa mãn >=2 tiêu chí: Tuổi >=80, Cân nặng <=60kg, Creatinine >=1.5 mg/dL)" if apix_criteria_count >= 2 else " (Liều duy trì chuẩn)"
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Bảng kiểm chống chỉ định tiêu sợi huyết (cho nhóm D, E)
            if st.session_state.final_category in ["D1", "D2", "E1", "E2"]:
                st.markdown("<div class='section-card'>", unsafe_allow_html=True)
                st.write("##### ⚡ Rà soát Chống chỉ định Tiêu sợi huyết Hệ thống")
                with st.expander("Bấm vào để rà soát chi tiết"):
                    st.markdown("**Chống chỉ định tuyệt đối (Absolute Contraindications):**")
                    abs1 = st.checkbox("Tiền sử xuất huyết não hoặc đột quỵ không rõ nguyên nhân bất kỳ thời điểm nào")
                    abs2 = st.checkbox("Đột quỵ nhồi máu não trong vòng 6 tháng qua")
                    abs3 = st.checkbox("U hệ thần kinh trung ương hoặc dị dạng động tĩnh mạch não")
                    abs4 = st.checkbox("Chấn thương lớn, phẫu thuật lớn hoặc chấn thương đầu nặng trong vòng 3 tuần qua")
                    abs5 = st.checkbox("Xuất huyết nội tạng đang tiến triển hoặc xuất huyết tiêu hóa trong vòng 1 tháng qua")
                    abs6 = st.checkbox("Phình tách động mạch chủ ngực/bụng hoặc nghi ngờ")
                    
                    st.markdown("**Chống chỉ định tương đối (Relative Contraindications):**")
                    rel1 = st.checkbox("Cơn thiếu máu não cục bộ thoáng qua (TIA) trong vòng 6 tháng qua")
                    rel2 = st.checkbox("Đang dùng kháng đông đường uống")
                    rel3 = st.checkbox("Mang thai hoặc trong vòng 1 tuần sau sinh")
                    rel4 = st.checkbox("Chọc dò mạch máu ở vị trí không ép được")
                    rel5 = st.checkbox("Hồi sức tim phổi (CPR) kéo dài hoặc chấn thương lớn do hồi sức")
                    rel6 = st.checkbox("Tăng huyết áp nặng không kiểm soát (HA tâm thu > 180 mmHg hoặc tâm trương > 110 mmHg)")
                    rel7 = st.checkbox("Bệnh gan nặng tiến triển hoặc viêm màng ngoài tim cấp")
                    
                    has_absolute = abs1 or abs2 or abs3 or abs4 or abs5 or abs6
                    has_relative = rel1 or rel2 or rel3 or rel4 or rel5 or rel6 or rel7
                    
                    if has_absolute:
                        st.error("🚨 CẢNH BÁO: Bệnh nhân có chống chỉ định TUYỆT ĐỐI với tiêu sợi huyết hệ thống! Bắt buộc cân nhắc phương pháp Lấy huyết khối cơ học (MT) hoặc Phẫu thuật lấy huyết khối.")
                    elif has_relative:
                        st.warning("⚠️ CẢNH BÁO: Bệnh nhân có chống chỉ định tương đối. Cần cân nhắc kỹ lợi ích/nguy cơ, ưu tiên can thiệp qua catheter (CDL) hoặc lấy huyết khối cơ học MT nếu có sẵn.")
                    else:
                        st.success("Không phát hiện chống chỉ định tiêu sợi huyết hệ thống.")
                st.markdown("</div>", unsafe_allow_html=True)

        with col3_2:
            r_suffix = "R" if st.session_state.resp_modifier else ""
            final_group = f"{st.session_state.final_category}{r_suffix}"
            
            st.markdown(f"<div class='result-card'><h3>PHÂN NHÓM HIỆN TẠI: <span style='color:#DC2626;'>NHÓM {final_group}</span></h3></div>", unsafe_allow_html=True)
            
            # --------------------------------------------------------------------------
            # PHÁC ĐỒ ĐIỀU TRỊ CHUẨN CHO NHÓM A, B (KHÁNG ĐÔNG ĐƯỜNG UỐNG ƯU TIÊN)
            # --------------------------------------------------------------------------
            if st.session_state.final_category in ["A", "B1", "B2"]:
                st.info("📍 **Nơi điều trị (Triage):** Điều trị ngoại trú an toàn (nếu đạt tiêu chí Hestia=0/sPESI=0) hoặc nhập viện ngắn ngày khoa thường.")
                
                if st.session_state.final_category == "B1":
                    st.warning("👉 **Nhánh dưới phân thùy (B1):** Hướng dẫn AHA/ACC 2026 cho phép cân nhắc theo dõi lâm sàng và siêu âm tĩnh mạch sâu chi dưới định kỳ mà **chưa cần dùng kháng đông ngay** nếu bệnh nhân có nguy cơ chảy máu cao, không kèm theo triệu chứng lâm sàng và KHÔNG CÓ DVT tĩnh mạch sâu (Class 2b). Nếu có DVT đi kèm, bắt buộc dùng kháng đông tiêu chuẩn.")
                
                # Check tình huống bắt buộc VKA hoặc LMWH
                if is_pregnant_t2:
                    st.error("🚨 **CHỈ ĐỊNH BẮT BUỘC CHO THAI KỲ (CHỐNG CHỈ ĐỊNH DOACs):**")
                    st.write("- Chống chỉ định hoàn toàn DOACs và VKA trong thời kỳ mang thai.")
                    st.write(f"- **Kháng đông ưu tiên bắt buộc:** **LMWH (Enoxaparin) liều chuẩn theo cân nặng: {weight * 1.0:.1f} mg tiêm dưới da mỗi 12 giờ** (1 mg/kg mỗi 12h). Cần duy trì suốt thai kỳ và tối thiểu 6 tuần sau sinh.")
                elif has_aps:
                    st.error("🚨 **CHỈ ĐỊNH BẮT BUỘC CHO APS (CHỐNG CHỈ ĐỊNH DOACs):**")
                    st.write("- Chống chỉ định DOACs do nguy cơ tắc mạch tái phát cực kỳ cao.")
                    st.write("- **Kháng đông bắt buộc:** Khởi đầu bằng kháng đông tiêm (LMWH/UFH) sau đó gối sang **Kháng vitamin K (VKA - Warfarin)** để duy trì lâu dài với đích **INR 2.0 - 3.0** (Class 1).")
                elif has_drug_interactions:
                    st.warning("⚠️ **CHỈ ĐỊNH THAY THẾ DO TƯƠNG TÁC THUỐC MẠNH:** Chống chỉ định DOACs. Khuyên dùng **VKA chỉnh liều sát theo INR** hoặc **LMWH (Enoxaparin)**.")
                else:
                    st.success("💊 **ƯU TIÊN HÀNG ĐẦU: DOACs đường uống (Class 1, LOE B-R)**")
                    st.caption("👉 *Chú thích ưu tiên:* DOACs đường uống (Apixaban hoặc Rivaroxaban) được ưu tiên tuyệt đối cho bệnh nhân nguy cơ thấp nhờ tính tiện dụng, an toàn cao, không cần nằm viện hay xét nghiệm theo dõi thường quy.")
                    
                    if has_cancer:
                        st.info("🎗️ *Bệnh nhân ung thư:* Hướng dẫn AHA/ACC 2026 ưu tiên dùng DOACs hoặc LMWH hơn là Kháng vitamin K (VKA) (Class 1).")
                        
                    st.write(f"- **Apixaban:** Khởi đầu **10mg uống x 2 lần/ngày trong 7 ngày đầu**, sau đó duy trì **{apix_maint_dose}**{apix_dose_note}.")
                    if crcl >= 30 and crcl < 50:
                        st.write(f"- **Rivaroxaban:** Khởi đầu **15mg uống x 2 lần/ngày trong 21 ngày đầu**, sau đó duy trì **15mg uống hằng ngày** (Đã giảm liều từ 20mg hằng ngày xuống 15mg hằng ngày do CrCl 30-49 mL/phút để tránh chảy máu).")
                    elif crcl < 30:
                        st.error(f"- **Rivaroxaban / Apixaban:** Không khuyến cáo sử dụng thường quy khi CrCl < 30 mL/phút. Khuyên dùng **VKA** hoặc **LMWH**.")
                    else:
                        st.write(f"- **Rivaroxaban:** Khởi đầu **15mg uống x 2 lần/ngày trong 21 ngày đầu**, sau đó duy trì **20mg uống hằng ngày**.")
            
            # --------------------------------------------------------------------------
            # PHÁC ĐỒ ĐIỀU TRỊ CHUẨN CHO NHÓM C (LMWH ƯU TIÊN, UFH THAY THẾ)
            # --------------------------------------------------------------------------
            elif st.session_state.final_category in ["C1", "C2", "C3"]:
                if st.session_state.final_category == "C3":
                    st.markdown("<div class='u-card urgency-medium'><strong>📍 Nơi điều trị: NHẬP ICU HOẶC ĐƠN VỊ ĐỆM (Intermediate/Step-down)</strong><br>Theo dõi sát huyết động liên tục trong 24-72 giờ đầu tại ICU/Step-down (Class 2a) do đây là nhóm có nguy cơ sụp đổ tuần hoàn cao nhất trong nhóm C.</div>\", unsafe_allow_html=True)", unsafe_allow_html=True)
                else:
                    st.info("📍 **Nơi điều trị (Triage):** Nhập viện điều trị nội trú tại Khoa Thường (Nội tim mạch/Nội chung).")
                
                st.write("💊 **Phác đồ Kháng đông Khởi đầu cá thể hóa:**")
                
                # Check tình huống bắt buộc VKA hoặc LMWH
                if has_aps:
                    st.error("🚨 **CHỈ ĐỊNH BẮT BUỘC CHO APS (CHỐNG CHỈ ĐỊNH DOACs):** Khởi đầu kháng đông tiêm LMWH/UFH gối sang **Kháng vitamin K (VKA)** lâu dài với đích **INR 2.0 - 3.0** (Class 1).")
                
                # 🌟 ƯU TIÊN: LMWH (Enoxaparin)
                st.write("🌟 **ƯU TIÊN: Heparin trọng lượng phân tử thấp (LMWH - Enoxaparin) (Class 1, LOE B-R)**")
                st.caption("👉 *Chú thích ưu tiên:* LMWH là kháng đông tiêm được ưu tiên lựa chọn hàng đầu cho bệnh nhân huyết động ổn định nhờ tính an toàn cao, sinh khả dụng tốt, ít gây xuất huyết nặng hơn UFH và không đòi hỏi xét nghiệm đông máu thường quy.")
                
                if crcl >= 30:
                    enox_standard = weight * 1.0
                    st.write(f"- **Liều LMWH chuẩn theo cân nặng thực tế:** **{enox_standard:.1f} mg tiêm dưới da mỗi 12 giờ** (1 mg/kg mỗi 12h).")
                    if bmi >= 40 or weight > 150:
                        enox_reduced = weight * 0.8
                        st.warning(f"⚠️ *Lưu ý béo phì độ III (BMI = {bmi:.1f} | Nặng {weight}kg):* Có thể cân nhắc giảm liều xuống **{enox_reduced:.1f} mg mỗi 12 giờ** (0.8 mg/kg mỗi 12h) để tránh tích lũy liều và giảm chảy máu (Class 2b, LOE B-NR). Quyết định tùy thuộc vào lâm sàng tại giường.")
                elif 15 <= crcl < 30:
                    enox_renal = weight * 1.0
                    st.write(f"- **Liều LMWH chỉnh liều suy thận nặng (CrCl 15-29 mL/phút):** Giảm tần suất xuống **{enox_renal:.1f} mg tiêm dưới da mỗi 24 giờ** (1 mg/kg mỗi 24h). Khuyến cáo định lượng đỉnh Anti-Xa (3-5h sau liều thứ 3).")
                else:
                    st.error("- **LMWH (Enoxaparin):** CHỐNG CHỈ ĐỊNH hoàn toàn do CrCl < 15 mL/phút. Bắt buộc chuyển sang dùng UFH truyền tĩnh mạch dưới đây.")
                
                # 👉 THAY THẾ: UFH
                st.write("👉 **LỰA CHỌN THAY THẾ: Heparin không phân đoạn (UFH) truyền tĩnh mạch (Class 1, LOE B-R)**")
                st.caption("👉 *Chú thích thay thế:* UFH là lựa chọn thay thế hợp lý, đặc biệt ở bệnh nhân nhóm C3 có nguy cơ sụp đổ tuần hoàn cao hoặc bệnh nhân suy thận nặng CrCl < 15 mL/phút chống chỉ định với LMWH.")
                
                ufh_bolus = min(80 * weight, 10000)
                ufh_maint = min(18 * weight, 1600)
                st.write(f"- **Liều nạp Bolus tĩnh mạch ban đầu:** **{ufh_bolus:.0f} UI** (Áp trần tối đa 10,000 UI để tránh quá liều ban đầu ở bệnh nhân béo phì).")
                st.write(f"- **Liều truyền tĩnh mạch duy trì ban đầu:** **{ufh_maint:.0f} UI/giờ** (Áp trần tối đa 1600 UI/giờ để đảm bảo an toàn trước khi có xét nghiệm đông máu lần đầu), sau đó điều chỉnh tốc độ truyền dựa theo APTT hoặc Anti-Xa.")
            
            # --------------------------------------------------------------------------
            # PHÁC ĐỒ ĐIỀU TRỊ CHUẨN CHO NHÓM D, E (UFH ƯU TIÊN TUYỆT ĐỐI, LMWH THAY THẾ)
            # --------------------------------------------------------------------------
            else:
                st.markdown("<div class='u-card urgency-high'><strong>📍 Nơi điều trị: KHOA HỒI SỨC TÍCH CỰC (ICU/CCU) tối khẩn cấp</strong><br>Kích hoạt ngay đội phản ứng nhanh PERT để phối hợp đa chuyên khoa đưa ra quyết định tái tưới máu sớm.</div>", unsafe_allow_html=True)
                
                st.write("💊 **Phác đồ Kháng đông Khởi đầu cá thể hóa:**")
                
                # 🌟 ƯU TIÊN: UFH
                st.write("🌟 **ƯU TIÊN: Heparin không phân đoạn (UFH) truyền tĩnh mạch (Class 1, LOE C-LD)**")
                st.caption("👉 *Chú thích ưu tiên:* UFH được ưu tiên tuyệt đối cho bệnh nhân huyết động không ổn định hoặc chuẩn bị can thiệp tái tưới máu khẩn cấp nhờ thời gian bán thải ngắn, dễ dàng theo dõi đông máu và có khả năng đảo ngược tác dụng nhanh chóng bằng Protamine khi xảy ra biến chứng chảy máu.")
                
                ufh_bolus = min(80 * weight, 10000)
                ufh_maint = min(18 * weight, 1600)
                st.write(f"- **Liều nạp Bolus tĩnh mạch ban đầu:** **{ufh_bolus:.0f} UI** (Áp trần tối đa 10,000 UI để đảm bảo an toàn ở bệnh nhân béo phì).")
                st.write(f"- **Liều truyền tĩnh mạch duy trì ban đầu:** **{ufh_maint:.0f} UI/giờ** (Áp trần tối đa 1600 UI/giờ để tránh quá liều ban đầu trước khi có xét nghiệm đông máu lần đầu), điều chỉnh duy trì sát sao theo APTT hoặc Anti-Xa.")
                
                # 👉 THAY THẾ: LMWH
                st.write("👉 **LỰA CHỌN THAY THẾ: Heparin trọng lượng phân tử thấp (LMWH - Enoxaparin) (Class 2a)**")
                st.caption("👉 *Chú thích thay thế:* LMWH thường không được ưu tiên trong pha cấp cứu sụp đổ huyết động do khó đảo ngược tác dụng hoàn toàn. Chỉ cân nhắc sử dụng khi huyết động đã ổn định hoàn toàn và không còn kế hoạch can thiệp tái tưới máu xâm lấn.")
                
                if crcl >= 30:
                    enox_standard = weight * 1.0
                    st.write(f"- **Liều chuẩn theo cân nặng thực tế:** **{enox_standard:.1f} mg tiêm dưới da mỗi 12 giờ** (1 mg/kg mỗi 12h).")
                    if bmi >= 40 or weight > 150:
                        enox_reduced = weight * 0.8
                        st.warning(f"⚠️ *Lưu ý béo phì độ III (BMI = {bmi:.1f} | Nặng {weight}kg):* Cân nhắc giảm liều xuống **{enox_reduced:.1f} mg mỗi 12 giờ** (0.8 mg/kg mỗi 12h) (Class 2b).")
                elif 15 <= crcl < 30:
                    enox_renal = weight * 1.0
                    st.write(f"- **Liều chỉnh liều suy thận nặng (CrCl 15-29 mL/phút):** Giảm tần suất xuống **{enox_renal:.1f} mg tiêm dưới da mỗi 24 giờ** (1 mg/kg mỗi 24h).")
                else:
                    st.error("- **LMWH (Enoxaparin):** CHỐNG CHỈ ĐỊNH do CrCl < 15 mL/phút.")
                
                # Liệu pháp can thiệp nâng cao cho nhóm D, E
                st.write("---")
                st.write("##### ⚡ Can thiệp Tái tưới máu Nâng cao (AHA/ACC 2026):")
                
                if st.session_state.final_category in ["E1", "E2"]:
                    st.success("👉 **Khuyến cáo Tiêu sợi huyết Hệ thống (Class 2a, LOE C-LD):** Tiêu sợi huyết hệ thống kết hợp kháng đông là hợp lý đối với bệnh nhân Nhóm E (Sốc tim/Ngừng tuần hoàn) nếu nguy cơ chảy máu chấp nhận được.")
                elif st.session_state.final_category in ["D1", "D2"]:
                    st.warning("👉 **Khuyến cáo Tiêu sợi huyết Hệ thống (Class 2b, LOE C-LD):** Tiêu sợi huyết hệ thống có thể được cân nhắc để tránh diễn tiến xấu thêm ở bệnh nhân Nhóm D (Sắp sụp đổ/Sốc ẩn).")
                
                # Chọn thuốc tiêu sợi huyết và tính liều
                selected_lytic = st.selectbox("Chọn thuốc tiêu sợi huyết lâm sàng muốn dùng:", [
                    "Alteplase (rt-PA) - Phổ biến nhất",
                    "Tenecteplase (TNK-tPA) - Thử nghiệm lâm sàng/Off-label"
                ])
                
                if "Alteplase" in selected_lytic:
                    st.info("💊 **Phác đồ Tiêu sợi huyết Hệ thống chuẩn (Alteplase - rt-PA):**")
                    st.write("- **Phác đồ liều chuẩn:** **100 mg truyền tĩnh mạch liên tục trong 2 giờ** (Phác đồ chuẩn duy nhất được FDA phê duyệt).")
                    if weight < 65:
                        st.write(f"- **Phác đồ liều thấp (Half-dose) khuyên dùng cho người nhẹ cân (<65kg):** Truyền **{weight * 0.5:.1f} mg** (tối đa 50 mg) truyền tĩnh mạch trong 2 giờ (Class 2b).")
                    else:
                        st.write("- **Phác đồ liều thấp (Half-dose):** Truyền **50 mg** truyền tĩnh mạch trong 2 giờ (Class 2b) để giảm nguy cơ chảy máu.")
                    st.write("- **Phác đồ liều siêu thấp (cho tắc ĐMP trung tâm nguy cơ cao):** **25 mg truyền tĩnh mạch chậm trong 6 giờ**.")
                else:
                    st.warning("⚠️ **Lưu ý về Tenecteplase (TNK-tPA):** Thuốc này **chưa được FDA phê duyệt** cho chỉ định PE (chỉ mang tính chất nghiên cứu/off-label).")
                    tnk_dose = 30
                    if weight < 60: tnk_dose = 30
                    elif 60 <= weight < 70: tnk_dose = 35
                    elif 70 <= weight < 80: tnk_dose = 40
                    elif 80 <= weight < 90: tnk_dose = 45
                    else: tnk_dose = 50
                    st.write(f"- **Liều TNK-tPA đề xuất theo cân nặng ({weight}kg):** Tiêm tĩnh mạch nhanh (Bolus) **{tnk_dose} mg** một lần duy nhất.")
                
                st.write("---")
                st.write("**Khuyến cáo can thiệp cơ học bằng dụng cụ (Mechanical Thrombectomy - MT) (AHA 2026):**")
                st.info("💡 Lấy huyết khối bằng dụng cụ cơ học (MT) là lựa chọn can thiệp nâng cao cực kỳ quan trọng (Class 2a cho nhóm E1, Class 2b cho nhóm D) đặc biệt khi bệnh nhân có chống chỉ định tuyệt đối hoặc thất bại với tiêu sợi huyết hệ thống.")

            # Hiển thị Respiratory Modifier nếu có R
            if st.session_state.resp_modifier:
                st.error("📢 **Cảnh báo Modifier R (Hô hấp):** Bệnh nhân có suy hô hấp nặng đi kèm. Hạn chế tối đa việc đặt nội khí quản máy thở áp lực dương lớn trừ khi bắt buộc để tránh làm sụp đổ tuần hoàn tim phải đang suy cấp. Ưu tiên sử dụng hỗ trợ oxy dòng cao (HFNC) hoặc thở máy không xâm lấn.")

        # Nút chuyển về GĐ 1 ở cuối trang
        st.markdown("---")
        if st.button("⬅️ Quay lại Bước 2 để hiệu chỉnh phân loại", type="secondary"):
            st.session_state.step = 2
            st.rerun()
