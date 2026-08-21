import streamlit as st
import math

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Hỗ trợ Quyết định Lâm sàng PE - AHA/ACC 2026",
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
    .stButton>button {
        background-color: #1E3A8A;
        color: white;
        border-radius: 6px;
        padding: 10px 24px;
        font-weight: 600;
        border: none;
    }
    .stButton>button:hover {
        background-color: #3B82F6;
        color: white;
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
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-header'>🩺 CDSS THUYÊN TẮC PHỔI CẤP (AHA/ACC 2026)</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Công cụ Hỗ trợ Quyết định Lâm sàng Tương tác tại Giường bệnh (Bản Web)</div>", unsafe_allow_html=True)

# Khởi tạo tabs chính
tab1, tab2 = st.tabs(["⚡ GIAI ĐOẠN 1: CHẨN ĐOÁN & LOẠI TRỪ PE", "📊 GIAI ĐOẠN 2 & 3: PHÂN LOẠI AHA 2026 & TÍNH LIỀU ĐIỀU TRỊ"])

# ==============================================================================
# TAB 1: GIAI ĐOẠN 1 - CHẨN ĐOÁN
# ==============================================================================
with tab1:
    st.header("⚡ Tiếp cận Chẩn đoán ban đầu (Nghi ngờ PE)")
    
    col1_1, col1_2 = st.columns([1, 1], gap="large")
    
    with col1_1:
        st.subheader("📋 Thông tin Sơ bộ & Xác suất tiền nghiệm (CPTP)")
        
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
                g_hr = st.selectbox("Tần số tim bệnh nhân:", ["< 75 ck/phút (0 điểm)", "75 - 94 ck/phút (+1 điểm)", ">= 95 ck/phút (+2 điểm)"])
                g8 = st.checkbox("Đau khi ấn dọc hệ tĩnh mạch sâu ở chân kèm sưng chân một bên (+1)")
                
                hr_score = 0
                if "75 - 94" in g_hr: hr_score = 1
                elif ">= 95" in g_hr: hr_score = 2
                
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
                st.success("Xác suất lâm sàng tiền nghiệm: THẤP (<15%)")
            elif cptp_category == "INTERMEDIATE":
                st.warning("Xác suất lâm sàng tiền nghiệm: TRUNG BÌNH (15% - 50%)")
            else:
                st.error("Xác suất lâm sàng tiền nghiệm: CAO (>50%)")
                
        else:
            st.success("Không nghi ngờ PE cấp trên lâm sàng. Tìm nguyên nhân khác.")

    with col1_2:
        st.subheader("🔍 Thuật toán Loại trừ & Chỉ định Hình ảnh học")
        
        if is_suspected:
            if cptp_category == "LOW":
                st.markdown("<div class='section-card'>", unsafe_allow_html=True)
                st.write("**Áp dụng Tiêu chuẩn loại trừ PE (PERC) tại giường:**")
                st.write("Nếu thỏa mãn tất cả 8 tiêu chí bên dưới (PERC âm tính), loại trừ PE hoàn toàn mà không cần bất cứ xét nghiệm nào!")
                
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
                    st.markdown("<div class='u-card urgency-low'><strong>>>> KẾT QUẢ PERC: ÂM TÍNH (LOẠI TRỪ PE THÀNH CÔNG)</strong><br>Bệnh nhân thỏa mãn toàn bộ 8 tiêu chí loại trừ. ĐỦ TIÊU CHUẨN LOẠI TRỪ PE HOÀN TOÀN TẠI GIƯỜNG BỆNH! Không cần làm D-dimer, không cần chụp CTPA.</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='u-card urgency-medium'><strong>>>> KẾT QUẢ PERC: DƯƠNG TÍNH</strong><br>Không thể loại trừ PE bằng PERC do có tiêu chí nguy cơ. Chuyển sang thực hiện xét nghiệm D-dimer phối hợp YEARS bên dưới.</div>", unsafe_allow_html=True)
                    
                    st.markdown("---")
                    st.write("**Đánh giá bằng Thuật toán YEARS:**")
                    y1 = st.checkbox("Có dấu hiệu lâm sàng của DVT (sưng đau chân)?")
                    y2 = st.checkbox("Có ho ra máu?")
                    y3 = st.checkbox("PE là chẩn đoán khả thi nhất trên lâm sàng?")
                    
                    years_count = (1 if y1 else 0) + (1 if y2 else 0) + (1 if y3 else 0)
                    years_cutoff = 1000 if years_count == 0 else 500
                    
                    st.write(f"Số tiêu chí YEARS thỏa mãn: **{years_count}/3**")
                    
                    if not is_pregnant and years_count >= 1:
                        age_years = st.number_input("Nhập tuổi bệnh nhân (để tính D-dimer hiệu chỉnh theo tuổi):", min_value=18, max_value=120, value=55, key="age_years")
                        if age_years > 50:
                            years_cutoff = age_years * 10
                            st.write(f"Bệnh nhân > 50 tuổi và có >=1 tiêu chí YEARS. Áp dụng D-dimer hiệu chỉnh theo tuổi: **< {years_cutoff} ng/mL**")
                        else:
                            st.write(f"Ngưỡng loại trừ D-dimer áp dụng: **< {years_cutoff} ng/mL**")
                    else:
                        st.write(f"Ngưỡng loại trừ D-dimer áp dụng: **< {years_cutoff} ng/mL**")
                        
                    d_dimer_val = st.number_input("Nhập nồng độ D-dimer thực tế đo được (ng/mL):", min_value=0, value=0, key="d_dimer_low")
                    
                    if d_dimer_val > 0:
                        if d_dimer_val < years_cutoff:
                            st.markdown(f"<div class='u-card urgency-low'><strong>>>> KẾT LUẬN: D-dimer ({d_dimer_val}) < Ngưỡng cắt ({years_cutoff})</strong><br>LOẠI TRỪ THUYÊN TẮC PHỔI (PE) THÀNH CÔNG! An toàn để KHÔNG chụp CTPA.</div>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<div class='u-card urgency-high'><strong>>>> KẾT LUẬN: D-dimer ({d_dimer_val}) >= Ngưỡng cắt ({years_cutoff})</strong><br>VƯỢT NGƯỠNG AN TOÀN. CHỈ ĐỊNH CHỤP CTPA ĐỂ XÁC ĐỊNH CHẨN ĐOÁN!</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
            elif cptp_category == "INTERMEDIATE":
                st.markdown("<div class='section-card'>", unsafe_allow_html=True)
                st.write("**Áp dụng thuật toán YEARS cho nhóm nguy cơ trung bình:**")
                y1 = st.checkbox("Có dấu hiệu lâm sàng của DVT (sưng đau chân)?", key="int_y1")
                y2 = st.checkbox("Có ho ra máu?", key="int_y2")
                y3 = st.checkbox("PE là chẩn đoán khả thi nhất trên lâm sàng?", key="int_y3")
                
                years_count = (1 if y1 else 0) + (1 if y2 else 0) + (1 if y3 else 0)
                years_cutoff = 1000 if years_count == 0 else 500
                
                st.write(f"Số tiêu chí YEARS thỏa mãn: **{years_count}/3**")
                
                if not is_pregnant and years_count >= 1:
                    age_years = st.number_input("Nhập tuổi bệnh nhân (để tính D-dimer hiệu chỉnh theo tuổi):", min_value=18, max_value=120, value=55, key="age_years_int")
                    if age_years > 50:
                        years_cutoff = age_years * 10
                        st.write(f"Bệnh nhân > 50 tuổi. Áp dụng D-dimer hiệu chỉnh theo tuổi: **< {years_cutoff} ng/mL**")
                    else:
                        st.write(f"Ngưỡng loại trừ D-dimer áp dụng: **< {years_cutoff} ng/mL**")
                else:
                    st.write(f"Ngưỡng loại trừ D-dimer áp dụng: **< {years_cutoff} ng/mL**")
                    
                d_dimer_val = st.number_input("Nhập nồng độ D-dimer thực tế đo được (ng/mL):", min_value=0, value=0, key="d_dimer_int")
                
                if d_dimer_val > 0:
                    if d_dimer_val < years_cutoff:
                        st.markdown(f"<div class='u-card urgency-low'><strong>>>> KẾT LUẬN: D-dimer ({d_dimer_val}) < Ngưỡng cắt ({years_cutoff})</strong><br>LOẠI TRỪ THUYÊN TẮC PHỔI (PE) THÀNH CÔNG! An toàn để không cần chụp CTPA.</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div class='u-card urgency-high'><strong>>>> KẾT LUẬN: D-dimer ({d_dimer_val}) >= Ngưỡng cắt ({years_cutoff})</strong><br>VƯỢT NGƯỠNG AN TOÀN. CHỈ ĐỊNH CHỤP CTPA ĐỂ XÁC ĐỊNH CHẨN ĐOÁN!</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
            else: # HIGH
                st.markdown("<div class='u-card urgency-high'><strong>>>> KẾT LUẬN: XÁC SUẤT LÂM SÀNG CỰC KỲ CAO (>50%)</strong><br><strong>HÀNH ĐỘNG NGAY:</strong> Chỉ định chụp CT động mạch phổi (CTPA) khẩn cấp lập tức! KHÔNG ĐƯỢC làm D-dimer để tránh âm tính giả nguy hiểm tính mạng. (Nếu bệnh nhân có chống chỉ định tuyệt đối với CTPA, chỉ định chụp nhấp nháy thông khí-tưới máu V/Q Scan).</div>", unsafe_allow_html=True)

# ==============================================================================
# TAB 2: GIAI ĐOẠN 2 & 3 - PHÂN NHÓM & TÍNH LIỀU ĐIỀU TRỊ
# ==============================================================================
with tab2:
    st.header("📊 Phân loại Lâm sàng Cấp tính AHA/ACC 2026 & Tính liều Điều trị")
    
    col2_1, col2_2 = st.columns([1, 1], gap="large")
    
    with col2_1:
        st.subheader("🧬 1. Nhập thông số để Phân loại Nguy cơ (Nhóm A - E)")
        
        # Sàng lọc hô hấp
        st.write("**Đánh giá Suy hô hấp đi kèm:**")
        resp_modifier = st.checkbox("Bệnh nhân có suy hô hấp nặng? (SpO2 <90% khí trời, nhịp thở >= 30 l/p, hoặc cần hỗ trợ oxy dòng cao HFNC/máy thở)")
        
        # Đánh giá tim phổi huyết động
        st.write("**Tình trạng Huyết động & Tim phổi cấp cứu:**")
        
        e_class = st.selectbox("Huyết động và tình trạng suy tim phổi:", [
            "Huyết động ổn định (Huyết áp bình thường)",
            "Tụt huyết áp thoáng qua (<15 phút, tự hồi phục hoặc đáp ứng nhanh với bù dịch, không giảm tưới máu cơ quan)",
            "Sốc ẩn (Huyết áp bình thường nhưng giảm tưới máu cơ quan: Lactate >2 mmol/L, Suy thận cấp, Thiểu niệu, Thay đổi tri giác)",
            "Sốc tim thực sự hoặc tụt huyết áp kéo dài (HA tâm thu <90 mmHg hoặc giảm >40 mmHg kéo dài >=15 phút, cần thuốc vận mạch)",
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
            # Nhóm ổn định huyết động -> Phải chọn thang điểm
            is_asymptomatic = st.checkbox("Bệnh nhân hoàn toàn KHÔNG triệu chứng và PE được phát hiện tình cờ trên CTPA vì bệnh nền khác?")
            if is_asymptomatic:
                category = "A"
            else:
                score_method = st.selectbox("Chọn thang điểm tiên lượng lâm sàng để chấm điểm:", [
                    "sPESI (Simplified PESI) - Rút gọn, nhanh chóng",
                    "PESI Đầy đủ (11 tiêu chí) - Chi tiết",
                    "Tiêu chí Hestia (Sàng lọc điều trị ngoại trú)",
                    "Thang điểm Bova (Dành cho bệnh nhân huyết động ổn định)",
                    "Thang điểm CPES (Nguy cơ sốc)"
                ])
                
                is_clinical_high = False
                
                if "sPESI" in score_method:
                    st.info("Tính điểm sPESI (Mỗi tiêu chí dương tính tính 1 điểm):")
                    sp1 = st.checkbox("Tuổi > 80")
                    sp2 = st.checkbox("Tiền sử ung thư đang tiến triển")
                    sp3 = st.checkbox("Tiền sử suy tim mạn hoặc bệnh phổi mạn tính")
                    sp4 = st.checkbox("Tần số tim >= 110 chu kỳ/phút")
                    sp5 = st.checkbox("Huyết áp tâm thu < 100 mmHg")
                    sp6 = st.checkbox("SpO2 < 90% (hoặc cần oxy hỗ trợ)")
                    
                    spesi_score = sum([sp1, sp2, sp3, sp4, sp5, sp6])
                    st.metric("Tổng điểm sPESI", f"{spesi_score} điểm")
                    is_clinical_high = spesi_score >= 1
                    
                elif "PESI Đầy đủ" in score_method:
                    st.info("Tính điểm PESI Đầy đủ:")
                    pesi_age = st.number_input("Nhập tuổi bệnh nhân:", min_value=18, max_value=120, value=60)
                    pesi_gender = st.radio("Giới tính:", ["Nam (+10)", "Nữ (0)"])
                    pesi_cancer = st.checkbox("Ung thư tiến triển (+30)")
                    pesi_hf_lung = st.checkbox("Suy tim mạn tính hoặc Bệnh phổi mạn tính (+10)")
                    pesi_hr = st.checkbox("Tần số tim >= 110 ck/phút (+20)")
                    pesi_sbp = st.checkbox("Huyết áp tâm thu < 100 mmHg (+30)")
                    pesi_rr = st.checkbox("Tần số thở >= 30 lần/phút (+20)")
                    pesi_temp = st.checkbox("Nhiệt độ cơ thể < 36 độ C (+20)")
                    pesi_mental = st.checkbox("Thay đổi trạng thái tâm thần (lẫn lộn, u ám) (+20)")
                    pesi_spo2 = st.checkbox("SpO2 < 90% (+20)")
                    
                    pesi_score = pesi_age
                    if pesi_gender == "Nam (+10)": pesi_score += 10
                    if pesi_cancer: pesi_score += 30
                    if pesi_hf_lung: pesi_score += 10
                    if pesi_hr: pesi_score += 20
                    if pesi_sbp: pesi_score += 30
                    if pesi_rr: pesi_score += 20
                    if pesi_temp: pesi_score += 20
                    if pesi_mental: pesi_score += 20
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
                    st.info("Sàng lọc tiêu chí Hestia (Tất cả phải KHÔNG để đủ điều kiện ngoại trú):")
                    h1 = st.checkbox("Huyết động không ổn định (cần vận mạch, truyền dịch, thở máy)?")
                    h2 = st.checkbox("Cần dùng tiêu sợi huyết hoặc lấy huyết khối?")
                    h3 = st.checkbox("Nguy cơ chảy máu cao (xuất huyết tiêu hóa gần đây, phẫu thuật <14 ngày, đột quỵ <1 tháng)?")
                    h4 = st.checkbox("Cần thở oxy hỗ trợ liên tục?")
                    h5 = st.checkbox("PE khởi phát khi đang dùng kháng đông liều đầy đủ?")
                    h6 = st.checkbox("Đau ngực dữ dội cần dùng thuốc giảm đau opioid đường tĩnh mạch?")
                    h7 = st.checkbox("Có lý do y khoa cần nhập viện kéo dài >24h (nhiễm trùng, suy thận nặng, suy gan)?")
                    h8 = st.checkbox("Độ thanh thải Creatinine CrCl < 30 mL/phút?")
                    h9 = st.checkbox("Có suy gan nặng hoặc xơ gan?")
                    h10 = st.checkbox("Có thai?")
                    h11 = st.checkbox("Không có mạng lưới hỗ trợ xã hội tốt, không thể tự mua thuốc hoặc không thể tái khám nhanh?")
                    
                    hestia_positive = any([h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11])
                    if hestia_positive:
                        st.error("Bệnh nhân có chống chỉ định ngoại trú theo Hestia. Bắt buộc nhập viện.")
                        is_clinical_high = True
                    else:
                        st.success("Bệnh nhân đạt tiêu chuẩn Hestia để điều trị ngoại trú an toàn!")
                        is_clinical_high = False
                        
                elif "Bova" in score_method:
                    st.info("Tính điểm Bova:")
                    b1 = st.checkbox("Nhịp tim 90 - 100 bpm (+1) hoặc >= 100 bpm (+2)")
                    b_hr = st.selectbox("Nhịp tim cụ thể cho Bova:", ["< 90 bpm (0đ)", "90 - 100 bpm (1đ)", ">= 100 bpm (2đ)"])
                    b2 = st.checkbox("Huyết áp tâm thu 90 - 100 mmHg (+2)")
                    b3 = st.checkbox("Có tăng men tim Troponin (+2)")
                    b4 = st.checkbox("Có rối loạn chức năng thất phải trên siêu âm hoặc CTPA (+2)")
                    
                    b_hr_score = 0
                    if "90 - 100" in b_hr: b_hr_score = 1
                    elif ">= 100" in b_hr: b_hr_score = 2
                    
                    bova_score = b_hr_score + (2 if b2 else 0) + (2 if b3 else 0) + (2 if b4 else 0)
                    st.metric("Tổng điểm Bova", f"{bova_score} điểm")
                    is_clinical_high = bova_score > 4 # Bova Stage III (điểm >4) là nguy cơ trung bình-cao
                    
                else: # CPES
                    st.info("Tính điểm CPES (Phát hiện nguy cơ tiến triển sốc ở người HA bình thường):")
                    c1 = st.checkbox("Có suy sụp/ngất lúc khởi phát (+1)")
                    c2 = st.checkbox("Tần số tim >= 100 chu kỳ/phút (+1)")
                    c3 = st.checkbox("SpO2 < 95% ở khí trời (+1)")
                    c4 = st.checkbox("Bất thường thất phải (RV) trên siêu âm/CT (+1)")
                    c5 = st.checkbox("Tăng Troponin (+1)")
                    c6 = st.checkbox("Có huyết khối tĩnh mạch sâu (DVT) đoạn gần kèm theo (+1)")
                    
                    cpes_score = sum([c1, c2, c3, c4, c5, c6])
                    st.metric("Tổng điểm CPES", f"{cpes_score} điểm")
                    is_clinical_high = cpes_score >= 3
                    
                # Tiến hành phân nhóm C vs B sau khi xác định điểm lâm sàng
                if is_clinical_high:
                    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
                    st.write("**Đánh giá Thất phải (RV) & Biomarkers cho nhóm C:**")
                    
                    # Siêu âm tim sâu
                    st.write("**Đánh giá chi tiết Rối loạn chức năng Thất phải (RV):**")
                    rv_ct = st.checkbox("Tỷ lệ đường kính RV/LV >= 1.0 trên CTPA hoặc siêu âm 4 buồng")
                    rv_echo_1 = st.checkbox("TAPSE < 17 mm (co bóp dọc vòng van 3 lá)")
                    rv_echo_2 = st.checkbox("Dấu hiệu McConnell (giảm động thành tự do RV, bảo tồn vùng mỏm)")
                    rv_echo_3 = st.checkbox("Vận tốc sóng S' TDI van 3 lá < 9.5 cm/s")
                    rv_echo_4 = st.checkbox("Vận tốc hở 3 lá TR >= 2.9 m/s (gợi ý tăng áp phổi cấp)")
                    rv_echo_5 = st.checkbox("Tĩnh mạch chủ dưới IVC giãn (>21mm) và xẹp < 50% khi hít vào")
                    rv_echo_6 = st.checkbox("Vách liên thất dẹt nghịch thường trong thì tâm thu/tâm trương")
                    
                    has_rv_dysfunction = rv_ct or rv_echo_1 or rv_echo_2 or rv_echo_3 or rv_echo_4 or rv_echo_5 or rv_echo_6
                    
                    if has_rv_dysfunction:
                        st.error("Xác nhận: Có Rối loạn chức năng/Quá tải Thất phải (RV Dysfunction)")
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
                    # Nhóm B
                    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
                    st.write("**Đánh giá vị trí huyết khối cho nhóm B:**")
                    is_subsegmental = st.checkbox("Huyết khối chỉ khu trú ở nhánh dưới phân thùy (Subsegmental) và KHÔNG kèm theo DVT chân?")
                    if is_subsegmental:
                        category = "B1"
                    else:
                        category = "B2"
                    st.markdown("</div>", unsafe_allow_html=True)

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
            scr = st.number_input("Creatinine (mg/dL):", min_value=0.2, max_value=15.0, value=1.0)
            
        age_calc = st.number_input("Tuổi bệnh nhân (để tính CrCl):", min_value=18, max_value=120, value=60, key="age_calc")
        gender_calc = st.radio("Giới tính sinh học:", ["Nam", "Nữ"], horizontal=True)
        
        # Tính toán chỉ số sinh học
        bmi = weight / ((height/100)**2)
        
        # Tính CrCl bằng Cockcroft-Gault
        gender_mul = 0.85 if gender_calc == "Nữ" else 1.0
        crcl = ((140 - age_calc) * weight * gender_mul) / (72 * scr)
        
        st.write(f"Chỉ số BMI: **{bmi:.1f} kg/m²** | Độ thanh thải Creatinine (CrCl): **{crcl:.1f} mL/phút**")
        
        st.markdown("---")
        
        # Hiển thị phác đồ điều trị cá thể hóa tương ứng với phân nhóm
        st.write(f"##### 🩺 Phác đồ Kháng đông & Phân luồng cho nhóm **{final_group}**:")
        
        if category == "A":
            st.info("📍 **Nơi điều trị (Triage):** Ngoại trú / Xuất viện an toàn từ phòng cấp cứu.")
            st.success("💊 **Kháng đông ưu tiên: DOACs đường uống**")
            st.write(f"- **Apixaban:** Liều tấn công **10mg uống x 2 lần/ngày trong 7 ngày đầu**, sau đó giảm liều duy trì xuống **5mg uống x 2 lần/ngày**.")
            st.write(f"- **Rivaroxaban:** Liều tấn công **15mg uống x 2 lần/ngày trong 21 ngày đầu**, sau đó giảm liều duy trì xuống **20mg uống x 1 lần/ngày**.")
            st.warning("⚠️ *Lưu ý:* Không dùng DOACs cho phụ nữ mang thai, cho con bú hoặc bệnh nhân có Hội chứng kháng Phospholipid (APS) chuyển sang VKA/LMWH.")
            
        elif category in ["B1", "B2"]:
            st.info("📍 **Nơi điều trị (Triage):** Điều trị ngoại trú (nếu đạt tiêu chí Hestia=0/sPESI=0) hoặc nhập viện ngắn ngày khoa thường.")
            if category == "B1":
                st.warning("👉 **Nhóm B1 (Dưới phân thùy):** Nếu bệnh nhân có nguy cơ chảy máu rất cao và KHÔNG có DVT chân đi kèm, hướng dẫn mới AHA 2026 cho phép theo dõi sát lâm sàng và siêu âm tĩnh mạch chân định kỳ mà **chưa cần dùng kháng đông ngay**.")
            st.success("💊 **Kháng đông ưu tiên: DOACs đường uống**")
            st.write(f"- **Apixaban:** **10mg x 2 lần/ngày** trong 7 ngày, sau đó **5mg x 2 lần/ngày**.")
            st.write(f"- **Rivaroxaban:** **15mg x 2 lần/ngày** trong 21 ngày, sau đó **20mg x 1 lần/ngày**.")
            if crcl < 30:
                st.error("Cảnh báo: Bệnh nhân suy thận nặng CrCl <30 mL/phút, cân nhắc chuyển sang LMWH hoặc kháng vitamin K truyền thống chỉnh liều sát.")
                
        elif category in ["C1", "C2", "C3"]:
            if category == "C3":
                st.markdown("<div class='u-card urgency-medium'><strong>📍 Nơi điều trị: NHẬP ICU HOẶC ĐƠN VỊ ĐỆM (Intermediate/Step-down)</strong><br>Bệnh nhân có tăng cả biomarker và có rối loạn RV (C3). Phải theo dõi sát huyết động liên tục trong 24-72 giờ đầu tại ICU/Step-down!</div>", unsafe_allow_html=True)
            else:
                st.info("📍 **Nơi điều trị (Triage):** Nhập viện điều trị nội trú tại Khoa Nội tim mạch / Nội chung.")
                
            st.write("💊 **Kháng đông ưu tiên khởi đầu: Kháng đông tiêm (LMWH hoặc UFH)**")
            
            # Tính liều Enoxaparin cá thể hóa
            if crcl >= 30:
                if bmi >= 40 or weight > 150:
                    enox_dose = weight * 0.8
                    st.write(f"- **LMWH (Enoxaparin):** Bệnh nhân béo phì độ III. Khuyến cáo giảm liều xuống **{enox_dose:.1f} mg tiêm dưới da mỗi 12 giờ** (liều 0.8 mg/kg mỗi 12h) để tránh tích lũy liều.")
                else:
                    enox_dose = weight * 1.0
                    st.write(f"- **LMWH (Enoxaparin) liều chuẩn:** **{enox_dose:.1f} mg tiêm dưới da mỗi 12 giờ** (liều 1 mg/kg mỗi 12h).")
            elif 15 <= crcl < 30:
                enox_dose = weight * 1.0
                st.write(f"- **LMWH (Enoxaparin) điều chỉnh suy thận nặng:** Giảm tần suất xuống **{enox_dose:.1f} mg tiêm dưới da mỗi 24 giờ** (liều 1mg/kg/ngày). Cần theo dõi nồng độ đỉnh Anti-Xa.")
            else:
                st.error("- **LMWH (Enoxaparin):** Chống chỉ định do CrCl < 15 mL/phút. Bắt buộc chuyển sang dùng Heparin không phân đoạn (UFH) truyền tĩnh mạch.")
                
            # Tính liều UFH
            ufh_bolus = min(80 * weight, 10000)
            ufh_maint = 18 * weight
            st.write(f"- **UFH (Heparin không phân đoạn):** Khuyên dùng ở bệnh nhân C3 để dễ kiểm soát hoặc khi có suy thận nặng. **Tiêm Bolus tĩnh mạch: {ufh_bolus:.0f} UI**, sau đó duy trì **truyền tĩnh mạch liên tục: {ufh_maint:.0f} UI/giờ**, điều chỉnh liều theo APTT hoặc Anti-Xa.")
            
        else: # Nhóm D hoặc E (Nguy cơ rất cao / Sụp đổ)
            st.markdown("<div class='u-card urgency-high'><strong>📍 Nơi điều trị: KHOA HỒI SỨC TÍCH CỰC (ICU/CCU) tối khẩn cấp</strong><br>Kích hoạt ngay đội phản ứng nhanh PERT để phối hợp đa chuyên khoa đưa ra quyết định tái tưới máu.</div>", unsafe_allow_html=True)
            
            st.write("💊 **Kháng đông khởi đầu bắt buộc:** **Heparin không phân đoạn (UFH) truyền tĩnh mạch**")
            ufh_bolus = min(80 * weight, 10000)
            ufh_maint = 18 * weight
            st.write(f"- **Liều nạp Bolus tĩnh mạch:** **{ufh_bolus:.0f} UI**.")
            st.write(f"- **Liều truyền duy trì ban đầu:** **{ufh_maint:.0f} UI/giờ**, điều chỉnh sát theo APTT.")
            
            st.write("---")
            st.write("##### ⚡ Liệu pháp Can thiệp tái tưới máu nâng cao (AHA/ACC 2026):")
            
            # Bảng kiểm chống chỉ định tiêu sợi huyết
            st.write("**Bảng kiểm Chống chỉ định của Tiêu sợi huyết Hệ thống:**")
            with st.expander("Bấm vào để rà soát chống chỉ định tiêu sợi huyết"):
                st.markdown("**Chống chỉ định tuyệt đối (Absolute):**")
                abs1 = st.checkbox("Tiền sử xuất huyết não hoặc đột quỵ không rõ nguyên nhân bất kỳ thời điểm nào")
                abs2 = st.checkbox("Đột quỵ nhồi máu não trong vòng 6 tháng qua")
                abs3 = st.checkbox("U hệ thần kinh trung ương hoặc dị dạng động tĩnh mạch não")
                abs4 = st.checkbox("Chấn thương lớn, phẫu thuật lớn hoặc chấn thương đầu nặng trong vòng 3 tuần qua")
                abs5 = st.checkbox("Xuất huyết nội tạng đang tiến triển hoặc xuất huyết tiêu hóa trong vòng 1 tháng qua")
                abs6 = st.checkbox("Phình tách động mạch chủ ngực/bụng hoặc nghi ngờ")
                
                st.markdown("**Chống chỉ định tương đối (Relative):**")
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
                    st.warning("⚠️ CẢNH BÁO: Bệnh nhân có chống chỉ định tương đối. Cần cân nhắc kỹ lợi ích/nguy cơ, ưu tiên can thiệp qua catheter (CDL) hoặc lấy huyết khối MT nếu có thể.")
                else:
                    st.success("Không phát hiện chống chỉ định tiêu sợi huyết.")

            # Cho chọn thuốc tiêu sợi huyết và tính liều
            selected_lytic = st.selectbox("Chọn thuốc tiêu sợi huyết lâm sàng muốn dùng:", [
                "Alteplase (rt-PA) - Phổ biến nhất",
                "Tenecteplase (TNK-tPA) - Bolus nhanh một lần",
                "Streptokinase",
                "Urokinase"
            ])
            
            if "Alteplase" in selected_lytic:
                st.write("**Phác đồ liều Alteplase (rt-PA) cá thể hóa:**")
                st.write("- **Phác đồ liều chuẩn (cho nhóm E1):** **100 mg truyền tĩnh mạch liên tục trong 2 giờ**.")
                if weight < 65:
                    st.write(f"- **Phác đồ liều thấp (Half-dose) khuyên dùng cho người nhẹ cân (<65kg) hoặc nguy cơ chảy máu trung bình (nhóm D2):** Truyền **{weight * 0.5:.1f} mg** (tối đa 50 mg) truyền tĩnh mạch trong 2 giờ.")
                else:
                    st.write("- **Phác đồ liều thấp (Half-dose) cho nhóm D2:** Truyền **50 mg** truyền tĩnh mạch trong 2 giờ.")
                st.write("- **Phác đồ liều siêu thấp (cho tắc động mạch phổi trung tâm nguy cơ cao):** **25 mg truyền tĩnh mạch chậm trong 6 giờ**.")
                
            elif "Tenecteplase" in selected_lytic:
                st.write("**Phác đồ liều Tenecteplase (TNK-tPA) tiêm tĩnh mạch nhanh (Bolus) một lần theo cân nặng:**")
                tnk_dose = 30
                if weight < 60: tnk_dose = 30
                elif 60 <= weight < 70: tnk_dose = 35
                elif 70 <= weight < 80: tnk_dose = 40
                elif 80 <= weight < 90: tnk_dose = 45
                else: tnk_dose = 50
                st.success(f"👉 **Liều TNK-tPA khuyến cáo cho cân nặng {weight}kg:** Tiêm tĩnh mạch nhanh (Bolus) **{tnk_dose} mg** một lần duy nhất.")
                
            elif "Streptokinase" in selected_lytic:
                st.write("**Phác đồ Streptokinase:**")
                st.write("- **Liều nạp:** **250,000 UI truyền tĩnh mạch trong 30 phút**, sau đó duy trì **100,000 UI/giờ truyền liên tục trong 12 - 24 giờ**.")
                st.write("- **Phác đồ truyền nhanh thay thế:** **1.5 triệu UI truyền tĩnh mạch liên tục trong 2 giờ**.")
                
            else: # Urokinase
                st.write("**Phác đồ Urokinase tính theo cân nặng:**")
                uro_load = 4400 * weight
                uro_maint = 4400 * weight
                st.write(f"- **Liều nạp:** Truyền tĩnh mạch **{uro_load:,.0f} UI** trong vòng 10 phút.")
                st.write(f"- **Liều duy trì:** Truyền tĩnh mạch liên tục **{uro_maint:,.0f} UI/giờ trong vòng 12 giờ**.")

            st.write("**Khuyến cáo can thiệp cơ học bằng dụng cụ (Mechanical Thrombectomy - MT) (AHA 2026):**")
            st.info("💡 Lấy huyết khối bằng dụng cụ cơ học (MT) là lựa chọn cực kỳ ưu việt đối với bệnh nhân nhóm D và E có chống chỉ định với tiêu sợi huyết, hoặc khi tiêu sợi huyết hệ thống thất bại. MT giúp giải phóng tắc nghẽn cơ học ngay lập tức, cải thiện nhanh chóng áp lực thất phải mà không gây tăng nguy cơ chảy máu hệ thống.")
            
        # Hiển thị Respiratory Modifier nếu có R
        if resp_modifier:
            st.error("📢 **Cảnh báo Modifier R (Hô hấp):** Bệnh nhân có suy hô hấp nặng đi kèm. Hạn chế đặt nội khí quản máy thở áp lực dương lớn trừ khi bắt buộc để tránh làm sụp đổ dòng máu về tim phải đang suy cấp. Ưu tiên tối đa hỗ trợ oxy dòng cao (HFNC) hoặc thở máy không xâm lấn.")
