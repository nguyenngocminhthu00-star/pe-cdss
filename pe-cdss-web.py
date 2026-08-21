import streamlit as st
import math

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Hỗ trợ Quyết định Lâm sàng PE - AHA/ACC 2026 (Bản chuẩn)",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS cho giao diện y tế hiện đại, chuyên nghiệp
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
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-header'>🩺 CDSS THUYÊN TẮC PHỔI CẤP (AHA/ACC 2026)</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Công cụ Hỗ trợ Quyết định Lâm sàng Tương tác tại Giường bệnh (Bản Chuẩn hóa Guideline v6)</div>", unsafe_allow_html=True)

# Quản lý Tab qua Session State để hỗ trợ chuyển tab động bằng nút bấm
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "GIAI ĐOẠN 1"

# Tạo nút chọn Tab ở đầu trang
tab_cols = st.columns(2)
with tab_cols[0]:
    if st.button("⚡ GIAI ĐOẠN 1: CHẨN ĐOÁN & LOẠI TRỪ PE", use_container_width=True, type="primary" if st.session_state.active_tab == "GIAI ĐOẠN 1" else "secondary"):
        st.session_state.active_tab = "GIAI ĐOẠN 1"
        st.rerun()
with tab_cols[1]:
    if st.button("📊 GIAI ĐOẠN 2 & 3: PHÂN LOẠI AHA 2026 & TÍNH LIỀU ĐIỀU TRỊ", use_container_width=True, type="primary" if st.session_state.active_tab == "GIAI ĐOẠN 2" else "secondary"):
        st.session_state.active_tab = "GIAI ĐOẠN 2"
        st.rerun()

st.markdown("---")

# ==============================================================================
# TAB 1: GIAI ĐOẠN 1 - CHẨN ĐOÁN (Phân luồng độc lập: Age-Adjusted D-dimer vs YEARS)
# ==============================================================================
if st.session_state.active_tab == "GIAI ĐOẠN 1":
    st.header("⚡ Tiếp cận Chẩn đoán ban đầu (Nghi ngờ PE)")
    
    col1_1, col1_2 = st.columns([1, 1], gap="large")
    
    with col1_1:
        st.subheader("📋 Thông tin Sơ bộ & Đánh giá Xác suất tiền nghiệm (CPTP)")
        
        is_suspected = st.checkbox("Bệnh nhân có triệu chứng/dấu hiệu nghi ngờ PE cấp tính (khó thở, đau ngực, ho ra máu, ngất...)?", value=True)
        is_pregnant = st.checkbox("Bệnh nhân hiện tại đang mang thai?")
        
        if is_suspected:
            score_type = st.radio("Chọn Thang điểm Đánh giá Xác suất tiền nghiệm:", ["Thang điểm Wells (Ưu tiên)", "Thang điểm Geneva Rút gọn"])
            
            cptp_category = "LOW"
            cptp_score = 0.0
            
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

    with col1_2:
        st.subheader("🔍 Thuật toán Loại trừ & Chỉ định Hình ảnh học")
        
        if is_suspected:
            any_perc_positive = False
            if cptp_category == "LOW":
                st.markdown("<div class='section-card'>", unsafe_allow_html=True)
                st.write("**1. Áp dụng Tiêu chuẩn loại trừ PE (PERC) tại giường:**")
                st.write("Chỉ áp dụng khi xác suất lâm sàng tiền nghiệm (gestalt) <15% (hoặc Wells < 2). Nếu thỏa mãn tất cả 8 tiêu chí bên dưới (PERC âm tính), loại trừ PE hoàn toàn mà không cần xét nghiệm.")
                
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
                    
                    # Nút nhảy tab động khi loại trừ thành công
                    if st.button("📊 Vẫn chuyển sang Phân loại & Điều trị (Đóng giả định)", type="secondary"):
                        st.session_state.active_tab = "GIAI ĐOẠN 2"
                        st.rerun()
                else:
                    st.markdown("<div class='u-card urgency-medium'><strong>>>> KẾT QUẢ PERC: DƯƠNG TÍNH</strong><br>Không thể loại trừ PE bằng PERC. Bắt buộc phải thực hiện xét nghiệm D-dimer theo một trong hai chiến lược độc lập bên dưới.</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Cho phép chọn chiến lược D-dimer độc lập nếu CPTP <50% (Low/Intermediate)
            if cptp_category in ["LOW", "INTERMEDIATE"] and (cptp_category == "INTERMEDIATE" or any_perc_positive):
                st.markdown("<div class='section-card'>", unsafe_allow_html=True)
                st.write("**2. Lựa chọn Chiến lược D-dimer để loại trừ hoặc chỉ định chụp hình ảnh:**")
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
                        st.write(f"Bệnh nhân > 50 tuổi. Ngưỡng cắt D-dimer hiệu chỉnh theo tuổi: **< {cutoff_a} ng/mL** (Fibrinogen Equivalent Units).")
                    else:
                        cutoff_a = 500
                        st.write(f"Bệnh nhân ≤ 50 tuổi. Ngưỡng cắt D-dimer chuẩn: **< 500 ng/mL**.")
                        
                    d_dimer_val_a = st.number_input("Nhập nồng độ D-dimer thực tế đo được (ng/mL):", min_value=0, value=0, key="d_dimer_strategy_a")
                    
                    if d_dimer_val_a > 0:
                        if d_dimer_val_a < cutoff_a:
                            st.markdown(f"<div class='u-card urgency-low'><strong>>>> KẾT LUẬN: D-dimer ({d_dimer_val_a}) < Ngưỡng cắt ({cutoff_a})</strong><br>LOẠI TRỪ THUYÊN TẮC PHỔI (PE) THÀNH CÔNG! An toàn để KHÔNG chụp CTPA.</div>", unsafe_allow_html=True)
                            if st.button("📊 Vẫn chuyển sang Phân loại & Điều trị (Giả định)", type="secondary"):
                                st.session_state.active_tab = "GIAI ĐOẠN 2"
                                st.rerun()
                        else:
                            st.markdown(f"<div class='u-card urgency-high'><strong>>>> KẾT LUẬN: D-dimer ({d_dimer_val_a}) >= Ngưỡng cắt ({cutoff_a})</strong><br>VƯỢT NGƯỠNG AN TOÀN. CHỈ ĐỊNH CHỤP CTPA ĐỂ XÁC ĐỊNH CHẨN ĐOÁN!</div>", unsafe_allow_html=True)
                            if st.button("📊 Có kết quả CTPA? Chuyển sang Phân loại & Điều trị", type="primary"):
                                st.session_state.active_tab = "GIAI ĐOẠN 2"
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
                    
                    # Ngưỡng cắt YEARS cố định hoàn toàn
                    years_cutoff = 1000 if years_count == 0 else 500
                    st.write(f"Ngưỡng cắt D-dimer theo YEARS (cố định): **{years_cutoff} ng/mL**")
                    
                    d_dimer_val_b = st.number_input("Nhập nồng độ D-dimer thực tế đo được (ng/mL):", min_value=0, value=0, key="d_dimer_strategy_b")
                    
                    if d_dimer_val_b > 0:
                        if d_dimer_val_b < years_cutoff:
                            st.markdown(f"<div class='u-card urgency-low'><strong>>>> KẾT LUẬN: D-dimer ({d_dimer_val_b}) < Ngưỡng YEARS ({years_cutoff})</strong><br>LOẠI TRỪ THUYÊN TẮC PHỔI (PE) THÀNH CÔNG! An toàn để không cần chụp CTPA.</div>", unsafe_allow_html=True)
                            if is_pregnant and y1:
                                st.warning("👉 *Lưu ý thai kỳ:* Nếu thai phụ có triệu chứng chi dưới và siêu âm Doppler tĩnh mạch (CUS) dương tính, có thể điều trị kháng đông ngay mà không cần chụp CTPA.")
                            if st.button("📊 Vẫn chuyển sang Phân loại & Điều trị (Giả định)", type="secondary"):
                                st.session_state.active_tab = "GIAI ĐOẠN 2"
                                st.rerun()
                        else:
                            st.markdown(f"<div class='u-card urgency-high'><strong>>>> KẾT LUẬN: D-dimer ({d_dimer_val_b}) >= Ngưỡng YEARS ({years_cutoff})</strong><br>VƯỢT NGƯỠNG AN TOÀN. CHỈ ĐỊNH CHỤP CTPA ĐỂ XÁC ĐỊNH CHẨN ĐOÁN!</div>", unsafe_allow_html=True)
                            if st.button("📊 Có kết quả CTPA? Chuyển sang Phân loại & Điều trị", type="primary"):
                                st.session_state.active_tab = "GIAI ĐOẠN 2"
                                st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
                
            elif cptp_category == "HIGH": # HIGH
                st.markdown("<div class='u-card urgency-high'><strong>>>> KẾT LUẬN: XÁC SUẤT LÂM SÀNG CỰC KỲ CAO (>50%)</strong><br><strong>HÀNH ĐỘNG NGAY:</strong> Chỉ định chụp CT động mạch phổi (CTPA) khẩn cấp lập tức! KHÔNG ĐƯỢC làm D-dimer để tránh âm tính giả nguy hiểm tính mạng.</div>", unsafe_allow_html=True)
                if st.button("📊 Chuyển sang Giai đoạn Phân loại & Điều trị sau khi có CTPA", type="primary"):
                    st.session_state.active_tab = "GIAI ĐOẠN 2"
                    st.rerun()

    # Nút chuyển tiếp nhanh ở cuối trang
    st.markdown("---")
    col_nav = st.columns([4, 1])
    with col_nav[1]:
        if st.button("Tiếp tục sang GĐ 2 ➡️", use_container_width=True):
            st.session_state.active_tab = "GIAI ĐOẠN 2"
            st.rerun()

# ==============================================================================
# TAB 2: GIAI ĐOẠN 2 & 3 - PHÂN NHÓM & TÍNH LIỀU ĐIỀU TRỊ
# ==============================================================================
elif st.session_state.active_tab == "GIAI ĐOẠN 2":
    st.header("📊 Phân loại Lâm sàng Cấp tính AHA/ACC 2026 & Tính liều Điều trị")
    
    col2_1, col2_2 = st.columns([1, 1], gap="large")
    
    with col2_1:
        st.subheader("🧬 1. Nhập thông số để Phân loại Nguy cơ (Nhóm A - E)")
        
        # Đánh giá tim phổi huyết động cấp cứu
        st.write("**Tình trạng Huyết động & Tim phổi cấp cứu:**")
        
        e_class = st.selectbox("Huyết động và trạng thái suy tim phổi:", [
            "Huyết động ổn định (Huyết áp bình thường)",
            "Tụt huyết áp thoáng qua (<15 phút, tự hồi phục hoặc đáp ứng nhanh với bù dịch, không giảm tưới máu cơ quan)",
            "Sốc ẩn (HA bình thường nhưng GIẢM TƯỚI MÁU CƠ QUAN / SHOCK SCORE tăng: Lactate >2, AKI, thiểu niệu, thay đổi tri giác, hoặc CPES = 6/6)",
            "Sốc tim thực sự hoặc tụt huyết áp kéo dài (HA tâm thu <90 hoặc giảm >40 mmHg kéo dài >=15 phút, cần thuốc vận mạch)",
            "Ngừng tuần hoàn hoặc Sốc tim kháng trị (phải hồi sức tim phổi CPR hoặc dùng vận mạch liều tối đa)"
        ])
        
        category = "A"
        
        if "Ngừng tuần hoàn" in e_class:
            category = "E2"
        elif "Sốc tim thực sự" in e_class:
            category = "E1"
        elif "Sốc ẩn" in e_class:
            category = "D2"
        elif "Tụt huyết áp thoáng qua" in e_class:
            category = "D1"
        else:
            # Nhóm ổn định huyết động -> Chọn thang điểm
            is_asymptomatic = st.checkbox("Bệnh nhân hoàn toàn KHÔNG triệu chứng và PE được phát hiện tình cờ trên CTPA vì bệnh lý khác?")
            if is_asymptomatic:
                category = "A"
            else:
                score_method = st.selectbox("Chọn thang điểm tiên lượng lâm sàng để phân loại B/C:", [
                    "sPESI (Simplified PESI) - Rút gọn, nhanh chóng",
                    "PESI Đầy đủ (11 tiêu chí)",
                    "Tiêu chí Hestia (11 mục loại trừ chuẩn)",
                    "Thang điểm Bova (Dành cho bệnh nhân huyết động ổn)",
                    "Thang điểm CPES (Dự báo nguy cơ sốc)"
                ])
                
                is_clinical_high = False
                
                if "sPESI" in score_method:
                    st.info("Tính điểm sPESI (Mỗi tiêu chí dương tính tính 1 điểm):")
                    sp1 = st.checkbox("Tuổi > 80")
                    sp2 = st.checkbox("Tiền sử ung thư đang tiến triển")
                    sp3 = st.checkbox("Tiền sử bệnh tim phổi mạn tính")
                    sp4 = st.checkbox("Tần số tim >= 110 chu kỳ/phút")
                    sp5 = st.checkbox("Huyết áp tâm thu < 100 mmHg")
                    sp6 = st.checkbox("SpO2 < 90% (hoặc cần oxy hỗ trợ)")
                    
                    spesi_score = sum([sp1, sp2, sp3, sp4, sp5, sp6])
                    st.metric("Tổng điểm sPESI", f"{spesi_score} điểm")
                    is_clinical_high = spesi_score >= 1
                    
                elif "PESI Đầy đủ" in score_method:
                    st.info("Tính điểm PESI Đầy đủ (11 tiêu chí chuẩn):")
                    pesi_age = st.number_input("Nhập tuổi bệnh nhân:", min_value=18, max_value=120, value=60, key="pesi_age_raw")
                    pesi_gender = st.radio("Giới tính:", ["Nam (+10)", "Nữ (0)"])
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
                    if pesi_mental: pesi_score += 60 # Đúng +60 chuẩn Guideline!
                    if pesi_spo2: pesi_score += 20
                    
                    st.metric("Tổng điểm PESI", f"{pesi_score} điểm")
                    
                    pesi_class = "I"
                    if pesi_score <= 65: pesi_class = "I"
                    elif pesi_score <= 85: pesi_class = "II"
                    elif pesi_score <= 105: pesi_class = "III"
                    elif pesi_score <= 125: pesi_class = "IV"
                    else: pesi_class = "V"
                    
                    st.write(f"Phân loại PESI: **Class {pesi_class}**")
                    is_clinical_high = pesi_score > 85 # Class III trở lên là nguy cơ cao lâm sàng
                    
                elif "Hestia" in score_method:
                    st.info("Sàng lọc tiêu chí Hestia (11 mục loại trừ chuẩn - Table 6):")
                    h1 = st.checkbox("1. Huyết động không ổn định?")
                    h2 = st.checkbox("2. Cần dùng tiêu sợi huyết hoặc phẫu thuật lấy huyết khối?")
                    h3 = st.checkbox("3. Nguy cơ chảy máu cao hoặc đang chảy máu hoạt động?")
                    h4 = st.checkbox("4. Cần thở oxy hỗ trợ liên tục >24h để duy trì SpO2 >90%?")
                    h5 = st.checkbox("5. PE khởi phát khi đang dùng kháng đông liều đầy đủ?")
                    h6 = st.checkbox("6. Đau ngực dữ dội cần dùng thuốc giảm đau opioid đường truyền tĩnh mạch >24h?")
                    h7 = st.checkbox("7. Có lý do y khoa hoặc xã hội cần nhập viện kéo dài >24h (ví dụ: nhiễm trùng đồng mắc)?")
                    h8 = st.checkbox("8. Độ thanh thải Creatinine CrCl < 30 mL/phút?")
                    h9 = st.checkbox("9. Có suy gan nặng?")
                    h10 = st.checkbox("10. Bệnh nhân có thai?")
                    h11 = st.checkbox("11. Tiền sử giảm tiểu cầu do Heparin (HIT)?")
                    
                    hestia_positive = any([h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11])
                    if hestia_positive:
                        st.error("Bệnh nhân có ít nhất 1 câu trả lời 'Có'. Hestia dương tính: Bắt buộc nhập viện (Nguy cơ cao để quản lý ngoại trú).")
                        is_clinical_high = True
                    else:
                        st.success("Tất cả câu trả lời là 'Không'. Hestia âm tính: Có thể xem xét điều trị ngoại trú an toàn.")
                        is_clinical_high = False
                        
                elif "Bova" in score_method:
                    st.info("Tính điểm Bova (Dành cho bệnh nhân huyết động ổn định - Table 6):")
                    b1 = st.checkbox("1. Tần số tim >= 110 chu kỳ/phút (+1)")
                    b2 = st.checkbox("2. Huyết áp tâm thu 90 - 100 mmHg (+2)")
                    b3 = st.checkbox("3. Có tăng men tim Troponin (+2)")
                    b4 = st.checkbox("4. Có rối loạn chức năng thất phải trên siêu âm hoặc CTPA (+2)")
                    
                    bova_score = (1 if b1 else 0) + (2 if b2 else 0) + (2 if b3 else 0) + (2 if b4 else 0)
                    st.metric("Tổng điểm Bova", f"{bova_score} điểm")
                    is_clinical_high = bova_score > 4 # Bova Stage III (>4đ) là nguy cơ trung bình-cao (C)
                    
                else: # CPES
                    st.info("Tính điểm CPES (Sàng lọc nguy cơ tiến triển sốc ở người HA bình thường - Table 6):")
                    c1 = st.checkbox("1. Tăng Troponin tim (+1)")
                    c2 = st.checkbox("2. Tăng peptide lợi niệu BNP hoặc NT-proBNP (+1)")
                    c3 = st.checkbox("3. Giảm chức năng RV mức độ trung bình hoặc nặng trên siêu âm (+1)")
                    c4 = st.checkbox("4. Có gánh nặng huyết khối trung tâm (Saddle PE) trên CTPA (+1)")
                    c5 = st.checkbox("5. Có huyết khối tĩnh mạch sâu (DVT) đoạn gần kèm theo (+1)")
                    c6 = st.checkbox("6. Tần số tim >= 100 chu kỳ/phút (+1)")
                    
                    cpes_score = sum([c1, c2, c3, c4, c5, c6])
                    st.metric("Tổng điểm CPES", f"{cpes_score} điểm")
                    is_clinical_high = cpes_score >= 3 # Điểm cao cho thấy xu hướng tăng nguy cơ
                    
                # Tiến hành phân nhóm C vs B sau khi xác định điểm lâm sàng
                if is_clinical_high:
                    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
                    st.write("**Đánh giá Thất phải (RV) & Biomarkers cho nhóm C:**")
                    
                    st.write("**Đánh giá chi tiết Rối loạn chức năng Thất phải (RV) (Siêu âm/CT):**")
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
                        
                    has_elevated_biomarkers = st.checkbox("Có tăng men tim Troponin (I/T) HOẶC tăng peptide lợi niệu (BNP/NT-proBNP)?")
                    
                    if has_rv_dysfunction and has_elevated_biomarkers:
                        category = "C3"
                    elif has_rv_dysfunction or has_elevated_biomarkers:
                        category = "C2"
                    else:
                        category = "C1"
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    # Nhóm B (Xếp loại thuần túy theo giải phẫu!)
                    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
                    st.write("**Đánh giá vị trí huyết khối cho nhóm B:**")
                    is_subsegmental = st.checkbox("Huyết khối chỉ khu trú ở nhánh dưới phân thùy (Subsegmental PE)?")
                    if is_subsegmental:
                        category = "B1" # Nhánh dưới phân thùy
                    else:
                        category = "B2" # Nhánh phân thùy trở lên
                    st.markdown("</div>", unsafe_allow_html=True)

        # Đánh giá Respiratory Modifier (R) động theo từng nhóm cụ thể
        st.write("**Đánh giá Suy hô hấp đi kèm (Respiratory Modifier R):**")
        resp_modifier = False
        
        if category in ["C1", "C2", "C3"]:
            st.info("Tiêu chí R cho Nhóm C: Suy hô hấp thông thường")
            r_c = st.checkbox("SpO2 < 90% ở khí trời, HOẶC nhịp thở (RR) >= 30 lần/phút, HOẶC đang cần bổ sung oxy hỗ trợ thông thường (qua gọng kính/mặt nạ)?")
            resp_modifier = r_c
        elif category in ["D1", "D2"]:
            st.info("Tiêu chí R cho Nhóm D: Suy hô hấp tiến triển")
            r_d = st.checkbox("Đang cần thở oxy dòng cao HFNC (>6 L/phút) HOẶC đang phải sử dụng mặt nạ không thở lại (NRB)?")
            resp_modifier = r_d
        elif category in ["E1", "E2"]:
            st.info("Tiêu chí R cho Nhóm E: Suy hô hấp nguy kịch")
            r_e = st.checkbox("Đang cần thông khí áp lực dương không xâm lấn (NIV/BiPAP) HOẶC đang phải thông khí xâm lấn (đặt nội khí quản thở máy)?")
            resp_modifier = r_e

        # Hiển thị kết quả phân nhóm lớn
        r_str = "R" if resp_modifier else ""
        final_group = f"{category}{r_str}"
        st.markdown(f"<div class='result-card'><h3>KẾT QUẢ PHÂN NHÓM: <span style='color:#DC2626;'>NHÓM {final_group}</span></h3></div>", unsafe_allow_html=True)

    with col2_2:
        st.subheader("💊 2. Cá thể hóa Điều trị & Tính liều thuốc (AHA/ACC 2026)")
        
        # Nhập thông số cân nặng chiều cao chức năng thận
        st.write("**Thông số sinh học của bệnh nhân:**")
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
        
        st.markdown("---\")
        
        # Hiển thị phác đồ điều trị cá thể hóa tương ứng với phân nhóm
        st.write(f"##### 🩺 Phác đồ Kháng đông & Phân luồng cho nhóm **{final_group}**:")
        
        if category == "A":
            st.info("📍 **Nơi điều trị (Triage):** Ngoại trú / Xuất viện an toàn từ phòng cấp cứu (Class 1, LOE A)")
            st.success("💊 **Kháng đông ưu tiên: DOACs đường uống (Class 1, LOE B-R)**")
            st.write(f"- **Apixaban:** 10mg uống x 2 lần/ngày trong 7 ngày đầu, sau đó duy trì 5mg x 2 lần/ngày.")
            st.write(f"- **Rivaroxaban:** 15mg uống x 2 lần/ngày trong 21 ngày đầu, sau đó duy trì 20mg hằng ngày.")
            st.warning("⚠️ *Lưu ý:* Tránh dùng DOACs cho bệnh nhân có thai (chuyển sang LMWH) hoặc bệnh nhân mắc hội chứng kháng Phospholipid (APS) (chuyển sang kháng Vitamin K - VKA) (Class 1, LOE A).")
            
        elif category in ["B1", "B2"]:
            st.info("📍 **Nơi điều trị (Triage):** Điều trị ngoại trú (nếu đạt tiêu chí Hestia=0/sPESI=0) hoặc nhập viện ngắn ngày khoa thường.")
            
            if category == "B1":
                st.warning("👉 **Nhánh dưới phân thùy (B1):** Hướng dẫn AHA/ACC 2026 cho phép cân nhắc theo dõi lâm sàng và siêu âm tĩnh mạch sâu chi dưới định kỳ mà **chưa cần dùng kháng đông ngay** nếu bệnh nhân có nguy cơ chảy máu cao, không kèm theo triệu chứng lâm sàng và KHÔNG CÓ DVT tĩnh mạch sâu (Class 2b). Nếu có DVT đi kèm, bắt buộc dùng kháng đông tiêu chuẩn.")
            
            st.success("💊 **Kháng đông ưu tiên: DOACs đường uống (Class 1, LOE B-R)**")
            st.write(f"- **Apixaban:** 10mg x 2 lần/ngày trong 7 ngày, sau đó 5mg x 2 lần/ngày.")
            st.write(f"- **Rivaroxaban:** 15mg x 2 lần/ngày trong 21 ngày, sau đó 20mg x 1 lần/ngày.")
            if crcl < 30:
                st.error("Cảnh báo: Bệnh nhân suy thận nặng CrCl < 30 mL/phút, cân nhắc chuyển sang LMWH hoặc VKA chỉnh liều.")
                
        elif category in ["C1", ["C2", "C3"]]:
            if category == "C3":
                st.markdown("<div class='u-card urgency-medium'><strong>📍 Nơi điều trị: NHẬP ICU HOẶC ĐƠN VỊ ĐỆM (Intermediate/Step-down)</strong><br>Theo dõi sát huyết động liên tục trong 24-72 giờ đầu tại ICU/Step-down (Class 2a) do đây là nhóm có nguy cơ sụp đổ tuần hoàn cao nhất trong nhóm C.</div>", unsafe_allow_html=True)
            else:
                st.info("📍 **Nơi điều trị (Triage):** Nhập viện điều trị nội trú tại Khoa Thường (Nội tim mạch/Nội chung).")
                
            st.write("💊 **Kháng đông khởi đầu ưu tiên: LMWH (Enoxaparin) (Class 1, LOE B-R)**")
            
            # Tính liều Enoxaparin
            if crcl >= 30:
                enox_dose = weight * 1.0
                st.write(f"- **LMWH (Enoxaparin) liều chuẩn theo cân nặng:** **{enox_dose:.1f} mg tiêm dưới da mỗi 12 giờ** (1 mg/kg mỗi 12h).")
                
                # Clinical Note cho béo phì độ III (Class 2b)
                if bmi >= 40 or weight > 150:
                    enox_reduced = weight * 0.8
                    st.warning(f"⚠️ *Lưu ý lâm sàng béo phì độ III (BMI = {bmi:.1f} | Nặng {weight}kg):* Việc điều chỉnh giảm liều Enoxaparin xuống **{enox_reduced:.1f} mg mỗi 12 giờ** (0.8 mg/kg mỗi 12h) **có thể được cân nhắc** để giảm nguy cơ chảy máu (Class 2b, LOE B-NR). Tùy thuộc vào quyết định của bác sĩ tại giường.")
            elif 15 <= crcl < 30:
                enox_dose = weight * 1.0
                st.write(f"- **LMWH (Enoxaparin) chỉnh liều suy thận nặng:** Giảm tần suất xuống **{enox_dose:.1f} mg tiêm dưới da mỗi 24 giờ** (1 mg/kg mỗi 24h). Khuyến cáo theo dõi nồng độ đỉnh Anti-Xa.")
            else:
                st.error("- **LMWH (Enoxaparin):** Chống chỉ định do CrCl < 15 mL/phút. Bắt buộc chuyển sang dùng Heparin không phân đoạn (UFH) truyền tĩnh mạch.")
                
            # Tính liều UFH
            ufh_bolus = min(80 * weight, 10000)
            ufh_maint = 18 * weight
            st.write(f"- **UFH (Heparin không phân đoạn) truyền tĩnh mạch (lựa chọn thay thế ở C3):** Bolus tĩnh mạch **{ufh_bolus:.0f} UI** (áp trần tối đa 10,000 UI), sau đó truyền tĩnh mạch liên tục khởi đầu **{ufh_maint:.0f} UI/giờ**, chỉnh liều theo APTT hoặc Anti-Xa.")
            
        else: # Nhóm D hoặc E (Nguy cơ rất cao / Sụp đổ)
            st.markdown("<div class='u-card urgency-high'><strong>📍 Nơi điều trị: KHOA HỒI SỨC TÍCH CỰC (ICU/CCU) tối khẩn cấp</strong><br>Kích hoạt ngay đội phản ứng nhanh PERT để phối hợp đa chuyên khoa đưa ra quyết định tái tưới máu sớm.</div>", unsafe_allow_html=True)
            
            st.write("💊 **Kháng đông khởi đầu bắt buộc: Heparin không phân đoạn (UFH) truyền tĩnh mạch**")
            ufh_bolus = min(80 * weight, 10000)
            ufh_maint = 18 * weight
            st.write(f"- **Liều nạp Bolus tĩnh mạch:** **{ufh_bolus:.0f} UI** (Áp trần tối đa 10,000 UI để tránh quá liều cấp ở người béo phì).")
            st.write(f"- **Liều truyền tĩnh mạch duy trì ban đầu:** **{ufh_maint:.0f} UI/giờ**, điều chỉnh sát theo APTT.")
            
            st.write("---")
            st.write("##### ⚡ Liệu pháp Can thiệp tái tưới máu nâng cao (AHA/ACC 2026):")
            
            # Bảng kiểm chống chỉ định tiêu sợi huyết
            st.write("**Bảng kiểm Chống chỉ định của Tiêu sợi huyết Hệ thống:**")
            with st.expander("Bấm vào để rà soát chống chỉ định tiêu sợi huyết"):
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
                    st.success("Không phát hiện chống chỉ định tiêu sợi huyết.")

            # Chỉ định tiêu sợi huyết hệ thống theo Guideline
            st.write("**Chỉ định Tiêu sợi huyết Hệ thống (Systemic Thrombolysis):**")
            if category in ["E1", "E2"]:
                st.success("👉 **Khuyến cáo (Class 2a, LOE C-LD):** Tiêu sợi huyết hệ thống kết hợp kháng đông là hợp lý đối với bệnh nhân Nhóm E (Sốc tim/Ngừng tuần hoàn) nếu nguy cơ chảy máu chấp nhận được.")
            elif category in ["D1", "D2"]:
                st.warning("👉 **Khuyến cáo (Class 2b, LOE C-LD):** Tiêu sợi huyết hệ thống có thể được cân nhắc để tránh diễn tiến xấu thêm ở bệnh nhân Nhóm D (Sắp sụp đổ/Sốc ẩn).")
            elif category == "C3":
                st.write("👉 **Khuyến cáo (Class 2b, LOE C-LD):** Hiệu quả của tiêu sợi huyết hệ thống ở nhóm C3 là chưa rõ ràng (uncertain). Không khuyến cáo sử dụng thường quy trừ khi lâm sàng suy sụp rõ rệt.")
                
            # Phác đồ thuốc tiêu sợi huyết chuẩn
            st.info("💊 **Phác đồ Tiêu sợi huyết Hệ thống chuẩn (Alteplase):**")
            st.write("- **Alteplase (rt-PA) liều chuẩn:** **100 mg truyền tĩnh mạch liên tục trong 2 giờ** (đây là phác đồ chuẩn duy nhất được FDA phê duyệt và khuyến cáo chính thức bởi AHA/ACC).")
            st.write("- **Xem xét liều thấp (Lower-dose):** Phác đồ **50 mg rt-PA truyền tĩnh mạch trong 2 giờ** có thể được cân nhắc để giảm nguy cơ chảy máu (Class 2b, LOE C-LD), đặc biệt ở bệnh nhân nhẹ cân (<65kg) hoặc nguy cơ chảy máu cao.")
            st.write("- **Lưu ý về các thuốc khác:** Tenecteplase (TNK-tPA) **không được FDA phê duyệt** cho điều trị PE (chỉ mang tính chất nghiên cứu/off-label). Các thuốc thế hệ cũ (Streptokinase, Urokinase) hiếm khi được sử dụng trong thực hành lâm sàng hiện đại do đòi hỏi thời gian truyền kéo dài và độ an toàn thấp.")

            st.write("**Khuyến cáo can thiệp cơ học bằng dụng cụ (Mechanical Thrombectomy - MT) (AHA 2026):**")
            st.info("💡 Lấy huyết khối bằng dụng cụ cơ học (MT) là lựa chọn can thiệp nâng cao quan trọng (Class 2a cho nhóm E1, Class 2b cho nhóm D) đặc biệt khi bệnh nhân có chống chỉ định tuyệt đối hoặc thất bại với tiêu sợi huyết hệ thống.")
            
        # Hiển thị Respiratory Modifier nếu có R
        if resp_modifier:
            st.error("📢 **Cảnh báo Modifier R (Hô hấp):** Bệnh nhân có suy hô hấp nặng đi kèm. Hạn chế đặt nội khí quản máy thở áp lực dương lớn trừ khi bắt buộc để tránh làm sụp đổ tuần hoàn tim phải đang suy cấp. Ưu tiên tối đa hỗ trợ oxy dòng cao (HFNC) hoặc thở máy không xâm lấn.")

    # Nút chuyển về GĐ 1 ở cuối trang
    st.markdown("---")
    if st.button("⬅️ Quay lại Giai đoạn 1"):
        st.session_state.active_tab = "GIAI ĐOẠN 1"
        st.rerun()
