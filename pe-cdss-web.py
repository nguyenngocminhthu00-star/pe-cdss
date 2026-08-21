import streamlit as st
import math

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="CDSS Thuyên Tắc Phổi Cấp - AHA/ACC 2026",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS cho giao diện y tế chuyên nghiệp, tối ưu
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

st.markdown("<div class='main-header'>🩺 CDSS TIẾP CẬN THUYÊN TẮC PHỔI CẤP (AHA/ACC 2026)</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Hệ Thống Hỗ Trợ Ra Quyết Định Lâm Sàng Chuẩn Hóa Theo Hướng Dẫn Mới Nhất</div>", unsafe_allow_html=True)

# Khởi tạo hai phân hệ chính bằng tabs
tab1, tab2 = st.tabs(["⚡ GIAI ĐOẠN 1: CHẨN ĐOÁN & LOẠI TRỪ PE", "📊 GIAI ĐOẠN 2 & 3: PHÂN LOẠI AHA 2026 & ĐIỀU TRỊ"])

# ==============================================================================
# TAB 1: GIAI ĐOẠN 1 - CHẨN ĐOÁN VÀ LOẠI TRỪ
# ==============================================================================
with tab1:
    st.header("⚡ Tiếp cận Chẩn đoán ban đầu (Nghi ngờ PE)")
    
    col1_1, col1_2 = st.columns([1, 1], gap="large")
    
    with col1_1:
        st.subheader("📋 1. Đánh giá Xác suất lâm sàng tiền nghiệm (CPTP)")
        
        is_suspected = st.checkbox("Bệnh nhân có triệu chứng/dấu hiệu nghi ngờ PE cấp tính (khó thở, đau ngực, ho ra máu, ngất...)?", value=True)
        is_pregnant = st.checkbox("Bệnh nhân hiện tại đang mang thai?")
        
        if is_suspected:
            score_type = st.radio("Lựa chọn Thang điểm tính CPTP:", [
                "Thang điểm Wells (Tiêu chuẩn)",
                "Thang điểm Geneva cải biên (Revised Geneva Score)"
            ])
            
            cptp_category = "LOW"
            cptp_score = 0.0
            
            if "Wells" in score_type:
                st.info("Tính điểm Wells (Standard Wells Score):")
                w1 = st.checkbox("Triệu chứng lâm sàng của DVT (sưng chân, đau khi ấn dọc tĩnh mạch) (+3.0)")
                w2 = st.checkbox("PE là chẩn đoán khả thi nhất hoặc có khả năng xảy ra cao nhất (+3.0)")
                w3 = st.checkbox("Tần số tim > 100 chu kỳ/phút (+1.5)")
                w4 = st.checkbox("Bất động >= 3 ngày liên tục hoặc mới phẫu thuật trong vòng 4 tuần trước (+1.5)")
                w5 = st.checkbox("Tiền sử cá nhân bị DVT hoặc PE trước đây (+1.5)")
                w6 = st.checkbox("Ho ra máu (+1.0)")
                w7 = st.checkbox("Ung thư đang hoạt động/tiến triển (+1.0)")
                
                cptp_score = (3.0 if w1 else 0.0) + (3.0 if w2 else 0.0) + (1.5 if w3 else 0.0) + (1.5 if w4 else 0.0) + (1.5 if w5 else 0.0) + (1.0 if w6 else 0.0) + (1.0 if w7 else 0.0)
                
                # Hiển thị kết quả Wells
                st.metric(label="Tổng điểm Wells", value=f"{cptp_score} điểm")
                if cptp_score < 2.0:
                    cptp_category = "LOW"
                elif cptp_score <= 6.0:
                    cptp_category = "INTERMEDIATE"
                else:
                    cptp_category = "HIGH"
                
                # Wells cải biên (Likely vs Unlikely)
                is_likely = cptp_score > 4.0
                st.write(f"Phân loại Wells cải biên: **{ 'PE LIKELY (>4đ)' if is_likely else 'PE UNLIKELY (<=4đ)' }**")
                
            else:
                st.info("Chấm điểm Geneva cải biên & rút gọn:")
                g_method = st.radio("Chọn phiên bản Geneva:", ["Geneva cải biên đầy đủ (Revised)", "Geneva cải biên rút gọn (Simplified Revised)"])
                
                g1 = st.checkbox("Tuổi > 65 tuổi")
                g2 = st.checkbox("Tiền sử cá nhân bị DVT hoặc PE")
                g3 = st.checkbox("Phẫu thuật (gây mê toàn thân) hoặc gãy xương chi dưới trong vòng 1 tháng qua")
                g4 = st.checkbox("Ung thư đang tiến triển")
                g5 = st.checkbox("Đau chân một bên")
                g6 = st.checkbox("Ho ra máu")
                g8 = st.checkbox("Đau khi ấn dọc hệ tĩnh mạch sâu ở chân kèm sưng phù chân một bên")
                
                if g_method == "Geneva cải biên đầy đủ (Revised)":
                    g_hr = st.selectbox("Tần số tim của bệnh nhân:", ["< 75 bpm (0 điểm)", "75 - 94 bpm (+3 điểm)", ">= 95 bpm (+5 điểm)"])
                    hr_pts = 0
                    if "75 - 94" in g_hr: hr_pts = 3
                    elif ">= 95" in g_hr: hr_pts = 5
                    
                    cptp_score = (1 if g1 else 0) + (3 if g2 else 0) + (2 if g3 else 0) + (2 if g4 else 0) + (3 if g5 else 0) + (2 if g6 else 0) + hr_pts + (4 if g8 else 0)
                    st.metric(label="Tổng điểm Revised Geneva", value=f"{cptp_score} điểm")
                    
                    if cptp_score <= 3:
                        cptp_category = "LOW"
                    elif cptp_score <= 10:
                        cptp_category = "INTERMEDIATE"
                    else:
                        cptp_category = "HIGH"
                else:
                    g_hr = st.selectbox("Tần số tim của bệnh nhân:", ["< 75 bpm (0 điểm)", "75 - 94 bpm (+1 điểm)", ">= 95 bpm (+1 điểm)"])
                    hr_pts = 0
                    if "75 - 94" in g_hr or ">= 95" in g_hr: hr_pts = 1
                    
                    cptp_score = (1 if g1 else 0) + (1 if g2 else 0) + (1 if g3 else 0) + (1 if g4 else 0) + (1 if g5 else 0) + (1 if g6 else 0) + hr_pts + (1 if g8 else 0)
                    st.metric(label="Tổng điểm Simplified Geneva", value=f"{cptp_score} điểm")
                    
                    if cptp_score <= 1:
                        cptp_category = "LOW"
                    elif cptp_score <= 4:
                        cptp_category = "INTERMEDIATE"
                    else:
                        cptp_category = "HIGH"
            
            # Hiển thị CPTP cảnh báo màu
            if cptp_category == "LOW":
                st.success("Xác suất lâm sàng tiền nghiệm: THẤP (<15% dựa trên Wells/Geneva)")
            elif cptp_category == "INTERMEDIATE":
                st.warning("Xác suất lâm sàng tiền nghiệm: TRUNG BÌNH (15% - 50% dựa trên Wells/Geneva)")
            else:
                st.error("Xác suất lâm sàng tiền nghiệm: CAO (>50% dựa trên Wells/Geneva)")
        else:
            st.success("Không nghi ngờ lâm sàng thuyên tắc phổi. Tiếp tục tìm nguyên nhân khác.")

    with col1_2:
        st.subheader("🔍 2. Quy trình Sàng lọc loại trừ không hình ảnh học")
        
        if is_suspected:
            if cptp_category == "LOW":
                st.markdown("<div class='section-card'>", unsafe_allow_html=True)
                st.write("**Áp dụng Tiêu chuẩn loại trừ PE (PERC) tại giường:**")
                st.write("Nếu thỏa mãn toàn bộ 8 tiêu chí bên dưới (PERC âm tính), bạn được phép loại trừ PE hoàn toàn mà không cần bất kỳ xét nghiệm cận lâm sàng nào (Kể cả D-dimer)!")
                
                p1 = st.checkbox("Tuổi >= 50 tuổi")
                p2 = st.checkbox("Tần số tim >= 100 bpm")
                p3 = st.checkbox("SpO2 < 95% ở khí trời")
                p4 = st.checkbox("Sưng chân một bên")
                p5 = st.checkbox("Ho ra máu")
                p6 = st.checkbox("Chấn thương hoặc phẫu thuật gần đây (yêu cầu nhập viện trong vòng 4 tuần trước)")
                p7 = st.checkbox("Tiền sử cá nhân bị DVT hoặc PE")
                p8 = st.checkbox("Sử dụng estrogen (thuốc tránh thai, liệu pháp hormone thay thế)")
                
                any_perc_positive = p1 or p2 or p3 or p4 or p5 or p6 or p7 or p8
                
                if not any_perc_positive:
                    st.markdown("<div class='u-card urgency-low'><strong>>>> KẾT QUẢ PERC: ÂM TÍNH (LOẠI TRỪ PE THÀNH CÔNG)</strong><br>Bệnh nhân thỏa mãn toàn bộ 8 tiêu chuẩn loại trừ. Loại trừ hoàn toàn chẩn đoán PE tại giường bệnh! Không cần làm D-dimer, không cần chụp CTPA.</div> division", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='u-card urgency-medium'><strong>>>> KẾT QUẢ PERC: DƯƠNG TÍNH</strong><br>Bệnh nhân có ít nhất 1 yếu tố nguy cơ của PERC. Không thể loại trừ PE trực tiếp. Bắt buộc thực hiện D-dimer và đối chiếu bằng thuật toán YEARS dưới đây.</div>", unsafe_allow_html=True)
                    
                    st.markdown("---")
                    st.write("**Áp dụng Thuật toán YEARS:**")
                    y1 = st.checkbox("Có dấu hiệu lâm sàng của DVT (sưng đau chân)?", key="low_y1")
                    y2 = st.checkbox("Có ho ra máu?", key="low_y2")
                    y3 = st.checkbox("PE là chẩn đoán khả thi nhất trên lâm sàng?", key="low_y3")
                    
                    years_count = (1 if y1 else 0) + (1 if y2 else 0) + (1 if y3 else 0)
                    cutoff = 1000 if years_count == 0 else 500
                    
                    if not is_pregnant and years_count >= 1:
                        age = st.number_input("Nhập tuổi bệnh nhân (để tính D-dimer hiệu chỉnh theo tuổi):", min_value=18, max_value=120, value=55, key="age_years_low")
                        if age > 50:
                            cutoff = age * 10
                            st.write(f"Bệnh nhân >50 tuổi và có >=1 tiêu chí YEARS. Ngưỡng cắt D-dimer hiệu chỉnh: **< {cutoff} ng/mL**")
                        else:
                            st.write(f"Ngưỡng cắt D-dimer loại trừ áp dụng: **< {cutoff} ng/mL**")
                    else:
                        st.write(f"Ngưỡng cắt D-dimer loại trừ áp dụng: **< {cutoff} ng/mL**")
                        
                    d_dimer_val = st.number_input("Nhập nồng độ D-dimer thực tế đo được (ng/mL hoặc mcg/L FEU):", min_value=0, value=0, key="d_dimer_low_input")
                    
                    if d_dimer_val > 0:
                        if d_dimer_val < cutoff:
                            st.markdown(f"<div class='u-card urgency-low'><strong>>>> KẾT LUẬN: D-dimer ({d_dimer_val}) < Ngưỡng cắt ({cutoff})</strong><br>LOẠI TRỪ THUYÊN TẮC PHỔI (PE) THÀNH CÔNG! An toàn để KHÔNG chụp CTPA.</div>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<div class='u-card urgency-high'><strong>>>> KẾT LUẬN: D-dimer ({d_dimer_val}) >= Ngưỡng cắt ({cutoff})</strong><br>VƯỢT NGƯỠNG AN TOÀN. CHỈ ĐỊNH CHỤP CTPA NGAY ĐỂ CHẨN ĐOÁN XÁC ĐỊNH!</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
            elif cptp_category == "INTERMEDIATE":
                st.markdown("<div class='section-card'>", unsafe_allow_html=True)
                st.write("**Áp dụng thuật toán YEARS cho nhóm nguy cơ trung bình:**")
                y1 = st.checkbox("Có dấu hiệu lâm sàng của DVT (sưng đau chân)?", key="int_y1")
                y2 = st.checkbox("Có ho ra máu?", key="int_y2")
                y3 = st.checkbox("PE là chẩn đoán khả thi nhất trên lâm sàng?", key="int_y3")
                
                years_count = (1 if y1 else 0) + (1 if y2 else 0) + (1 if y3 else 0)
                cutoff = 1000 if years_count == 0 else 500
                
                if not is_pregnant and years_count >= 1:
                    age = st.number_input("Nhập tuổi bệnh nhân (để tính D-dimer hiệu chỉnh theo tuổi):", min_value=18, max_value=120, value=55, key="age_years_int")
                    if age > 50:
                        cutoff = age * 10
                        st.write(f"Bệnh nhân >50 tuổi và có >=1 tiêu chí YEARS. Ngưỡng cắt D-dimer hiệu chỉnh: **< {cutoff} ng/mL**")
                    else:
                        st.write(f"Ngưỡng cắt D-dimer loại trừ áp dụng: **< {cutoff} ng/mL**")
                else:
                    st.write(f"Ngưỡng cắt D-dimer loại trừ áp dụng: **< {cutoff} ng/mL**")
                    
                d_dimer_val = st.number_input("Nhập nồng độ D-dimer thực tế đo được (ng/mL hoặc mcg/L FEU):", min_value=0, value=0, key="d_dimer_int_input")
                
                if d_dimer_val > 0:
                    if d_dimer_val < cutoff:
                        st.markdown(f"<div class='u-card urgency-low'><strong>>>> KẾT LUẬN: D-dimer ({d_dimer_val}) < Ngưỡng cắt ({cutoff})</strong><br>LOẠI TRỪ THUYÊN TẮC PHỔI (PE) THÀNH CÔNG! An toàn để không cần chụp CTPA.</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div class='u-card urgency-high'><strong>>>> KẾT LUẬN: D-dimer ({d_dimer_val}) >= Ngưỡng cắt ({cutoff})</strong><br>VƯỢT NGƯỠNG AN TOÀN. CHỈ ĐỊNH CHỤP CTPA ĐỂ CHẨN ĐOÁN XÁC ĐỊNH!</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
            else: # HIGH
                st.markdown("<div class='u-card urgency-high'><strong>>>> KẾT LUẬN: XÁC SUẤT LÂM SÀNG CỰC KỲ CAO (>50%)</strong><br><strong>CHỈ ĐỊNH BẮT BUỘC:</strong> Chụp ngay CT động mạch phổi (CTPA) lập tức! Tuyệt đối không làm D-dimer vì tỷ lệ âm tính giả rất cao ở nhóm này.<br>*(Nếu bệnh nhân có chống chỉ định tuyệt đối với CTPA như suy thận nặng/dị ứng thuốc cản quang, ưu tiên chỉ định chụp nhấp nháy thông khí - tưới máu V/Q SPECT).*</div>", unsafe_allow_html=True)

# =============================================================================
# TAB 2: GIAI ĐOẠN 2 & 3 - PHÂN NHÓM NGUY CƠ AHA 2026 & ĐIỀU TRỊ CHUYÊN SÂU
# =============================================================================
with tab2:
    st.header("📊 Phân loại Lâm sàng Cấp tính AHA/ACC 2026 & Tính liều Điều trị")
    
    col2_1, col2_2 = st.columns([1, 1], gap="large")
    
    with col2_1:
        st.subheader("🧬 1. Sàng lọc huyết động & Chấm điểm nguy cơ")
        
        # Đánh giá tim phổi huyết động cấp cứu
        st.write("**Tình trạng Huyết động & Tim phổi cấp cứu:**")
        
        hemodynamic_state = st.selectbox("Đánh giá huyết động tại giường:", [
            "Huyết động ổn định (Huyết áp bình thường)",
            "D1: Tụt huyết áp thoáng qua (<15 phút, tự phục hồi hoặc đáp ứng nhanh với bù dịch, không giảm tưới máu cơ quan)",
            "D2: Sốc ẩn (Huyết áp bình thường nhưng có bằng chứng GIẢM TƯỚI MÁU cơ quan/sốc ẩn)",
            "E1: Sốc tim thực sự hoặc tụt huyết áp kéo dài (HA tâm thu <90 mmHg hoặc giảm >40 mmHg kéo dài >=15 phút, cần thuốc vận mạch)",
            "E2: Ngừng tim hoặc Sốc tim kháng trị (đòi hỏi hồi sức CPR hoặc sử dụng vận mạch liều tối đa)"
        ])
        
        category = "A"
        is_d2 = False
        
        if "E2" in hemodynamic_state:
            category = "E2"
        elif "E1" in hemodynamic_state:
            category = "E1"
        elif "D1" in hemodynamic_state:
            category = "D1"
        elif "D2" in hemodynamic_state:
            category = "D2"
            is_d2 = True
        else:
            # Nhóm ổn định huyết động -> Phải hỏi xem có triệu chứng không
            is_asymptomatic = st.checkbox("Bệnh nhân hoàn toàn KHÔNG triệu chứng, PE phát hiện tình cờ trên CTPA chỉ định vì lý do khác?")
            if is_asymptomatic:
                category = "A"
            else:
                st.write("**Chấm điểm Tiên lượng Lâm sàng để phân nhóm B hay C:**")
                score_method = st.selectbox("Chọn thang điểm lâm sàng muốn áp dụng:", [
                    "sPESI (Simplified PESI) - Rút gọn, khuyên dùng",
                    "PESI Đầy đủ (11 tiêu chí)",
                    "Tiêu chí Hestia (Sàng lọc xuất viện ngoại trú)",
                    "Thang điểm Bova (Dành cho bệnh nhân huyết động ổn định)"
                ])
                
                is_clinical_high = False
                
                if "sPESI" in score_method:
                    st.info("Tính điểm sPESI (Mỗi tiêu chí dương tính tính 1 điểm):")
                    sp1 = st.checkbox("Tuổi > 80")
                    sp2 = st.checkbox("Tiền sử ung thư đang hoạt động")
                    sp3 = st.checkbox("Tiền sử suy tim mạn hoặc bệnh phổi mạn tính")
                    sp4 = st.checkbox("Tần số tim >= 110 chu kỳ/phút")
                    sp5 = st.checkbox("Huyết áp tâm thu < 100 mmHg")
                    sp6 = st.checkbox("SpO2 < 90% (ở khí trời)")
                    
                    spesi_score = sum([sp1, sp2, sp3, sp4, sp5, sp6])
                    st.metric("Tổng điểm sPESI", f"{spesi_score} điểm")
                    is_clinical_high = spesi_score >= 1
                    
                elif "PESI Đầy đủ" in score_method:
                    st.info("Tính điểm PESI đầy đủ:")
                    pesi_age = st.number_input("Nhập tuổi bệnh nhân:", min_value=18, max_value=120, value=60, key="pesi_age_input")
                    pesi_gender = st.radio("Giới tính sinh học:", ["Nam (+10)", "Nữ (0)"], horizontal=True)
                    pesi_cancer = st.checkbox("Ung thư đang hoạt động (+30)")
                    pesi_hf_lung = st.checkbox("Suy tim mạn tính hoặc Bệnh phổi mạn tính (+10)")
                    pesi_hr = st.checkbox("Tần số tim >= 110 bpm (+20)")
                    pesi_sbp = st.checkbox("Huyết áp tâm thu < 100 mmHg (+30)")
                    pesi_rr = st.checkbox("Tần số thở >= 30 lần/phút (+20)")
                    pesi_temp = st.checkbox("Nhiệt độ cơ thể < 36 độ C (+20)")
                    pesi_mental = st.checkbox("Thay đổi trạng thái tinh thần (mơ màng, lơ mơ, lẫn lộn) (+20)")
                    pesi_spo2 = st.checkbox("SpO2 < 90% ở khí trời (+20)")
                    
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
                    
                    st.write(f"Phân lớp PESI: **Class {pesi_class}**")
                    is_clinical_high = pesi_score > 85 # Class III trở lên là nguy cơ cao lâm sàng
                    
                elif "Hestia" in score_method:
                    st.info("Sàng lọc 11 tiêu chí Hestia (Tất cả phải 'KHÔNG' để đủ điều kiện ngoại trú):")
                    h1 = st.checkbox("1. Bệnh nhân huyết động không ổn định (cần vận mạch, truyền dịch, thở máy)?")
                    h2 = st.checkbox("2. Cần điều trị tiêu sợi huyết hoặc phẫu thuật lấy huyết khối?")
                    h3 = st.checkbox("3. Bệnh nhân đang xuất huyết hoạt động hoặc có nguy cơ chảy máu rất cao?")
                    h4 = st.checkbox("4. Cần thở oxy hỗ trợ liên tục >24h để duy trì SpO2 >90%?")
                    h5 = st.checkbox("5. PE khởi phát khi đang dùng kháng đông liều đầy đủ?")
                    h6 = st.checkbox("6. Đau ngực dữ dội cần dùng thuốc giảm đau opioid đường tĩnh mạch >24h?")
                    h7 = st.checkbox("7. Có lý do y khoa cần nhập viện kéo dài >24h (ví dụ: nhiễm trùng nặng)?")
                    h8 = st.checkbox("8. Độ thanh thải Creatinine CrCl < 30 mL/phút?")
                    h9 = st.checkbox("9. Có suy gan nặng hoặc xơ gan?")
                    h10 = st.checkbox("10. Bệnh nhân đang mang thai?")
                    h11 = st.checkbox("11. Tiền sử giảm tiểu cầu do heparin (HIT) đã được xác nhận?")
                    h12 = st.checkbox("12. Không có mạng lưới hỗ trợ xã hội tốt, không thể liên lạc tái khám nhanh hoặc tự mua thuốc?")
                    
                    hestia_positive = any([h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12])
                    if hestia_positive:
                        st.error("Bệnh nhân có chống chỉ định ngoại trú theo Hestia. Bắt buộc nhập viện.")
                        is_clinical_high = True
                    else:
                        st.success("Bệnh nhân đủ tiêu chuẩn Hestia để điều trị ngoại trú an toàn!")
                        is_clinical_high = False
                        
                else: # Bova
                    st.info("Tính điểm Bova (0-7 điểm):")
                    b1 = st.checkbox("1. Huyết áp tâm thu trong khoảng 90 - 100 mmHg (+2 điểm)")
                    b2 = st.checkbox("2. Có tăng men tim Troponin (+2 điểm)")
                    b3 = st.checkbox("3. Có rối loạn chức năng thất phải trên siêu âm tim hoặc CTPA (+2 điểm)")
                    b4 = st.checkbox("4. Tần số tim >= 110 chu kỳ/phút (+1 điểm)")
                    
                    bova_score = (2 if b1 else 0) + (2 if b2 else 0) + (2 if b3 else 0) + (1 if b4 else 0)
                    st.metric("Tổng điểm Bova", f"{bova_score} điểm")
                    is_clinical_high = bova_score > 4 # Bova Stage III (>4 điểm) là nguy cơ trung bình-cao
                    
                # Tiến hành phân nhóm C vs B sau khi xác định điểm lâm sàng
                if is_clinical_high:
                    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
                    st.write("**Đánh giá quá tải Thất phải (RV) & Biomarkers cho Nhóm C:**")
                    
                    # Siêu âm tim sâu theo AHA 2026 Table 4
                    st.write("##### *Đánh giá chi tiết Rối loạn chức năng Thất phải (RV):*")
                    rv_ct = st.checkbox("CTPA: Tỷ lệ đường kính RV/LV >= 1.0 (mặt cắt axial hoặc 4 buồng)")
                    rv_echo_1 = st.checkbox("Siêu âm: Tỷ lệ RV/LV > 0.9 (ở mỏm hoặc dưới sườn)")
                    rv_echo_2 = st.checkbox("Siêu âm: TAPSE < 17 mm (giảm co bóp dọc cơ tim phải)")
                    rv_echo_3 = st.checkbox("Siêu âm: Vận tốc TDI sóng S' vòng van 3 lá < 9.5 cm/s")
                    rv_echo_4 = st.checkbox("Siêu âm: Vận tốc hở 3 lá TR >= 2.9 m/s (gợi ý tăng áp lực phổi cấp)")
                    rv_echo_5 = st.checkbox("Siêu âm: Có dấu hiệu McConnell (giảm động thành tự do RV, bảo tồn vùng mỏm)")
                    rv_echo_6 = st.checkbox("Siêu âm: Tĩnh mạch chủ dưới IVC giãn (>21mm) và xẹp < 50% khi hít vào")
                    rv_echo_7 = st.checkbox("Siêu âm: Phình hoặc vách liên thất di động nghịch thường")
                    
                    has_rv_dysfunction = rv_ct or rv_echo_1 or rv_echo_2 or rv_echo_3 or rv_echo_4 or rv_echo_5 or rv_echo_6 or rv_echo_7
                    
                    if has_rv_dysfunction:
                        st.error("Xác nhận: Có rối loạn chức năng Thất phải (RV Dysfunction)")
                    else:
                        st.success("Xác nhận: Thất phải hoạt động bình thường")
                        
                    has_elevated_biomarkers = st.checkbox("Có tăng men tim Troponin (I hoặc T) HOẶC peptide lợi niệu (BNP / NT-proBNP)?")
                    
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
                    st.write("**Đánh giá vị trí huyết khối cho Nhóm B:**")
                    is_subsegmental = st.checkbox("Bệnh nhân chỉ bị thuyên tắc nhánh dưới phân thùy (Subsegmental PE) và không kèm theo DVT chân?")
                    if is_subsegmental:
                        category = "B1"
                    else:
                        category = "B2"
                    st.markdown("</div>", unsafe_allow_html=True)

        # ----------------------------------------------------------------------
        # Sàng lọc Sốc Ẩn chi tiết (Category D2) sử dụng thang điểm CPES và dấu hiệu malperfusion
        # ----------------------------------------------------------------------
        if is_d2:
            st.markdown("<div class='section-card'>", unsafe_allow_html=True)
            st.write("**Đánh giá thang điểm Sốc ẩn CPES (Composite PE Shock) cho Nhóm D2:**")
            st.write("Dự báo nguy cơ tiến triển thành sốc ở bệnh nhân huyết động ổn ban đầu (Cần thỏa mãn cả 6/6 điểm):")
            
            cp1 = st.checkbox("1. Có tăng men tim Troponin? (+1 điểm)")
            cp2 = st.checkbox("2. Có tăng peptide lợi niệu BNP hoặc NT-proBNP? (+1 điểm)")
            cp3 = st.checkbox("3. Rối loạn chức năng RV mức độ trung bình - nặng trên siêu âm? (+1 điểm)")
            cp4 = st.checkbox("4. Thể tích huyết khối trung tâm lớn (Saddle PE - Yên ngựa) trên CTPA? (+1 điểm)")
            cp5 = st.checkbox("5. Có DVT đoạn gần chi dưới kèm theo? (+1 điểm)")
            cp6 = st.checkbox("6. Tần số tim >= 100 bpm? (+1 điểm)")
            
            cpes_score = sum([cp1, cp2, cp3, cp4, cp5, cp6])
            st.metric("Tổng điểm CPES", f"{cpes_score} điểm")
            if cpes_score == 6:
                st.error("Bệnh nhân đạt điểm tối đa CPES = 6. Nguy cơ tiến triển sốc ẩn cực kỳ cao!")
            else:
                st.write("Bệnh nhân có điểm CPES thấp hơn, cần rà soát thêm các tiêu chuẩn giảm tưới máu khác dưới đây.")
                
            st.write("**Kiểm tra các tiêu chuẩn giảm tưới máu cơ quan thực tế (AHA 2026):**")
            m1 = st.checkbox("Nồng độ Lactate máu > 2 mmol/L (mẫu tĩnh mạch hoặc động mạch)")
            m2 = st.checkbox("Suy thận cấp (Creatinine tăng >= 0.3 mg/dL hoặc >= 1.5 lần trong 24h)")
            m3 = st.checkbox("Urine output < 0.5 mL/kg/giờ (Thiểu niệu)")
            m4 = st.checkbox("Thay đổi trạng thái tâm thần (lờ đờ, u ám, lẫn lộn)")
            m5 = st.checkbox("SCAI Shock Stage B hoặc C (e.g., tay chân lạnh, ẩm, mạch nhanh nhỏ nhưng HA bình thường)")
            
            if not (m1 or m2 or m3 or m4 or m5 or cpes_score == 6):
                st.warning("⚠️ Chú ý: Nếu không có bằng chứng giảm tưới máu hoặc CPES < 6, bệnh nhân không thỏa mãn D2. Hệ thống sẽ tự động hạ cấp xuống nhóm C3.")
                category = "C3"
            st.markdown("</div>", unsafe_allow_html=True)

        # ----------------------------------------------------------------------
        # ĐÁNH GIÁ ĐỘNG RESPIRATORY MODIFIER (R) CHO TỪNG PHÂN LOẠI
        # ----------------------------------------------------------------------
        st.write("---")
        st.write("**Đánh giá Suy hô hấp đi kèm (Respiratory Modifier - R) chuẩn AHA/ACC 2026:**")
        resp_modifier = False
        
        if category in ["C1", "C2", "C3"]:
            st.info("Tiêu chí R cho Nhóm C: Suy hô hấp thông thường")
            rc1 = st.checkbox("Có tình trạng giảm oxy máu (SpO2 < 90% ở khí trời)?")
            rc2 = st.checkbox("Tần số thở nhanh RR >= 30 lần/phút?")
            rc3 = st.checkbox("Đang cần hỗ trợ oxy thông thường (qua gọng kính/mặt nạ đơn giản)?")
            resp_modifier = rc1 or rc2 or rc3
            
        elif category in ["D1", "D2"]:
            st.warning("Tiêu chí R cho Nhóm D: Suy hô hấp tiến triển")
            rd1 = st.checkbox("Bệnh nhân đòi hỏi oxy dòng cao qua gọng mũi HFNC (>6 L/phút)?")
            rd2 = st.checkbox("Bệnh nhân đang phải sử dụng mặt nạ không thở lại (NRB mask)?")
            resp_modifier = rd1 or rd2
            
        elif category in ["E1", "E2"]:
            st.error("Tiêu chí R cho Nhóm E: Suy hô hấp nguy kịch/Ventilatory Failure")
            re1 = st.checkbox("Suy hô hấp giảm oxy máu nặng hoặc suy thông khí đòi hỏi thở máy không xâm lấn (NIV/BiPAP)?")
            re2 = st.checkbox("Bệnh nhân suy hô hấp nguy kịch đòi hỏi đặt nội khí quản thở máy xâm lấn?")
            resp_modifier = re1 or re2

        # Xuất kết quả phân nhóm lớn cuối cùng
        r_str = "R" if resp_modifier else ""
        final_group = f"{category}{r_str}"
        st.markdown(f"<div class='result-card'><h3>KẾT QUẢ PHÂN NHÓM: <span style='color:#DC2626;'>NHÓM {final_group}</span></h3></div>", unsafe_allow_html=True)

    with col2_2:
        st.subheader("💊 2. Cá thể hóa Điều trị & Tính liều thuốc")
        
        # Nhập thông số sinh học bệnh nhân
        st.write("**Nhập thông số cơ bản của bệnh nhân để tính liều:**")
        col_w, col_h, col_cr = st.columns(3)
        with col_w:
            weight = st.number_input("Cân nặng (kg):", min_value=30, max_value=250, value=70, key="weight_input")
        with col_h:
            height = st.number_input("Chiều cao (cm):", min_value=100, max_value=250, value=165, key="height_input")
        with col_cr:
            scr = st.number_input("Creatinine (mg/dL):", min_value=0.2, max_value=15.0, value=1.0, key="scr_input")
            
        age_calc = st.number_input("Tuổi bệnh nhân (tính CrCl):", min_value=18, max_value=120, value=60, key="age_calc_input")
        gender_calc = st.radio("Giới tính sinh học:", ["Nam", "Nữ"], horizontal=True, key="gender_calc_input")
        
        # Tính toán BMI và CrCl
        bmi = weight / ((height/100)**2)
        gender_mul = 0.85 if gender_calc == "Nữ" else 1.0
        crcl = ((140 - age_calc) * weight * gender_mul) / (72 * scr)
        
        st.write(f"Chỉ số BMI: **{bmi:.1f} kg/m²** | Độ thanh thải Creatinine (CrCl): **{crcl:.1f} mL/phút**")
        
        st.markdown("---")
        
        # Hiển thị phác đồ điều trị cá thể hóa
        st.write(f"##### 🩺 Phác đồ xử trí chuẩn hóa cho nhóm **{final_group}**:")
        
        if category == "A":
            st.info("📍 **Nơi điều trị (Triage):** Ngoại trú / Xuất viện an toàn từ phòng cấp cứu.")
            st.success("💊 **Kháng đông ưu tiên: DOACs đường uống**")
            st.write("- **Apixaban:** Liều tấn công **10mg uống x 2 lần/ngày trong 7 ngày đầu**, sau đó duy trì **5mg uống x 2 lần/ngày**.")
            st.write("- **Rivaroxaban:** Liều tấn công **15mg uống x 2 lần/ngày trong 21 ngày đầu**, sau đó duy trì **20mg uống x 1 lần/ngày**.")
            st.warning("⚠️ *Cảnh báo bắt buộc:* Tuyệt đối không dùng DOACs cho phụ nữ mang thai, cho con bú hoặc bệnh nhân có Hội chứng kháng Phospholipid (APS) - bắt buộc chuyển sang LMWH hoặc VKA (Warfarin) [Class 1].")
            
        elif category in ["B1", "B2"]:
            st.info("📍 **Nơi điều trị (Triage):** Điều trị ngoại trú (nếu sPESI=0, Hestia=0 và đủ điều kiện hỗ trợ xã hội) hoặc nhập viện ngắn ngày khoa thường.")
            if category == "B1":
                st.warning("👉 *Lưu ý Nhóm B1 (Dưới phân thùy):* Hướng dẫn AHA 2026 cho phép cân nhắc chỉ theo dõi lâm sàng sát và siêu âm tĩnh mạch chân định kỳ mà **chưa cần dùng kháng đông ngay** nếu nguy cơ huyết khối thấp và không có DVT chân.")
            st.success("💊 **Kháng đông ưu tiên: DOACs đường uống** (Apixaban hoặc Rivaroxaban) tương tự Nhóm A.")
            if crcl < 30:
                st.error("Cảnh báo: Bệnh nhân suy thận nặng CrCl < 30 mL/phút. DOACs chống chỉ định, chuyển sang dùng Heparin không phân đoạn (UFH) truyền tĩnh mạch hoặc Kháng vitamin K truyền thống.")
                
        elif category in ["C1", "C2", "C3"]:
            if category == "C3":
                st.markdown("<div class='u-card urgency-medium'><strong>📍 Nơi điều trị: NHẬP KHOA ICU HOẶC ĐƠN VỊ ĐỆM (Intermediate/Step-down)</strong><br>Bệnh nhân thuộc nhóm nguy cơ trung bình-cao (C3). Bắt buộc nhập ICU hoặc đơn vị theo dõi sát liên tục trong 24-72 giờ đầu (đây là cửa sổ nguy cơ sụp đổ huyết động cao nhất dựa trên nghiên cứu PEITHO). Nếu MAP < 80 mmHg, kích hoạt PERT hội chẩn khẩn cấp!</div>", unsafe_allow_html=True)
            else:
                st.info("📍 **Nơi điều trị (Triage):** Nhập viện điều trị nội trú khoa Tim mạch / Nội chung.")
                
            st.write("💊 **Kháng đông ưu tiên khởi đầu: Kháng đông tiêm (LMWH hoặc UFH)**")
            
            # Tính liều Enoxaparin cá thể hóa chuẩn
            if crcl >= 30:
                if bmi >= 40 or weight > 150:
                    enox_dose = weight * 0.8
                    st.write(f"- **LMWH (Enoxaparin) điều chỉnh Béo phì độ III (BMI >= 40):** Khuyến cáo giảm liều xuống **{enox_dose:.1f} mg tiêm dưới da mỗi 12 giờ** (liều 0.8 mg/kg mỗi 12h) thay vì liều chuẩn để tránh supratherapeutic gây chảy máu nặng.")
                else:
                    enox_dose = weight * 1.0
                    st.write(f"- **LMWH (Enoxaparin) liều chuẩn:** **{enox_dose:.1f} mg tiêm dưới da mỗi 12 giờ** (liều 1 mg/kg mỗi 12h).")
            elif 15 <= crcl < 30:
                enox_dose = weight * 1.0
                st.write(f"- **LMWH (Enoxaparin) hiệu chỉnh suy thận nặng:** Giảm tần suất xuống **{enox_dose:.1f} mg tiêm dưới da mỗi 24 giờ** (liều 1mg/kg/ngày). Bắt buộc theo dõi nồng độ đỉnh Anti-Xa từ sau liều thứ 3 (đo 3-5h sau tiêm).")
            else:
                st.error("- **LMWH (Enoxaparin):** Chống chỉ định hoàn toàn do CrCl < 15 mL/phút. Bắt buộc chuyển sang dùng UFH truyền tĩnh mạch.")
                
            # Liều UFH (thích hợp hơn ở nhóm C3)
            ufh_bolus = min(80 * weight, 10000)
            ufh_maint = 18 * weight
            st.write(f"- **UFH (Heparin không phân đoạn):** Khuyên dùng ở nhóm C3 có nguy cơ diễn tiến xấu cần thủ thuật can thiệp khẩn cấp. **Tiêm Bolus: {ufh_bolus:.0f} UI**, sau đó duy trì **truyền tĩnh mạch liên tục ban đầu: {ufh_maint:.0f} UI/giờ**, chỉnh liều theo aPTT.")
            
        else: # Nhóm D hoặc E (Nguy cơ rất cao / Sụp sụp tuần hoàn)
            st.markdown("<div class='u-card urgency-high'><strong>📍 Nơi điều trị: KHOA HỒI SỨC TÍCH CỰC (ICU/CCU) tối khẩn cấp</strong><br>Kích hoạt khẩn cấp đội phản ứng nhanh PERT để đưa ra quyết định can thiệp tái tưới máu sớm cứu mạng bệnh nhân.</div>", unsafe_allow_html=True)
            
            st.write("💊 **Kháng đông khởi đầu bắt buộc:** **Heparin không phân đoạn (UFH) truyền tĩnh mạch**")
            ufh_bolus = min(80 * weight, 10000)
            ufh_maint = 18 * weight
            st.write(f"- **Liều nạp Bolus tĩnh mạch:** **{ufh_bolus:.0f} UI** (đã áp trần tối đa 10,000 UI theo quy chuẩn).")
            st.write(f"- **Liều truyền duy trì ban đầu:** **{ufh_maint:.0f} UI/giờ**, hiệu chỉnh sát để duy trì aPTT trong khoảng điều trị.")
            
            st.write("---")
            st.write("##### ⚡ Liệu pháp Can thiệp tái tưới máu nâng cao (AHA/ACC 2026):")
            
            # Bảng kiểm chống chỉ định tiêu sợi huyết
            st.write("**Bảng kiểm rà soát chống chỉ định của Tiêu sợi huyết:**")
            with st.expander("Bấm vào để rà soát chống chỉ định"):
                st.markdown("**Chống chỉ định tuyệt đối (Absolute):**")
                abs1 = st.checkbox("Tiền sử xuất huyết não hoặc đột quỵ không rõ nguyên nhân bất kỳ thời điểm nào")
                abs2 = st.checkbox("Đột quỵ nhồi máu não trong vòng 6 tháng qua")
                abs3 = st.checkbox("U hệ thần kinh trung ương hoặc dị dạng động tĩnh mạch não")
                abs4 = st.checkbox("Chấn thương lớn, phẫu thuật lớn hoặc chấn thương đầu nặng trong vòng 3 tuần qua")
                abs5 = st.checkbox("Xuất huyết nội tạng đang tiến triển hoặc xuất huyết tiêu hóa trong vòng 1 tháng qua")
                abs6 = st.checkbox("Phình tách động mạch chủ ngực/bụng hoặc nghi ngờ")
                
                st.markdown("**Chống chỉ định tương đối (Relative):**")
                rel1 = st.checkbox("Cơn thiếu máu não cục bộ thoáng qua (TIA) trong vòng 6 tháng qua")
                rel2 = st.checkbox("Bệnh nhân đang sử dụng kháng đông đường uống (VKA hoặc DOACs)")
                rel3 = st.checkbox("Đang mang thai hoặc trong vòng 1 tuần đầu sau sinh")
                rel4 = st.checkbox("Chọc dò mạch máu ở vị trí không ép được (ví dụ: sinh thiết gan)")
                rel5 = st.checkbox("Hồi sức tim phổi (CPR) kéo dài hoặc chấn thương lớn do hồi sức")
                rel6 = st.checkbox("Tăng huyết áp nặng không kiểm soát (HA tâm thu >180 mmHg hoặc tâm trương >110 mmHg)")
                rel7 = st.checkbox("Bệnh gan mạn tính tiến triển (xơ gan Child-Pugh C) hoặc viêm màng ngoài tim cấp")
                
                has_absolute = abs1 or abs2 or abs3 or abs4 or abs5 or abs6
                has_relative = rel1 or rel2 or rel3 or rel4 or rel5 or rel6 or rel7
                
                if has_absolute:
                    st.error("🚨 CẢNH BÁO: Bệnh nhân có chống chỉ định TUYỆT ĐỐI với tiêu sợi huyết hệ thống! Bắt buộc ưu tiên phương pháp can thiệp cơ học lấy huyết khối (MT) bằng dụng cụ hoặc Phẫu thuật lấy huyết khối.")
                elif has_relative:
                    st.warning("⚠️ CẢNH BÁO: Bệnh nhân có chống chỉ định tương đối. Cần hội chẩn PERT cân nhắc kỹ lợi ích/nguy cơ, ưu tiên can thiệp qua catheter (CDL) hoặc lấy huyết khối cơ học (MT) hơn là tiêu sợi huyết hệ thống.")
                else:
                    st.success("Không phát hiện chống chỉ định tiêu sợi huyết.")

            # Lựa chọn và tính liều thuốc tiêu sợi huyết
            selected_lytic = st.selectbox("Lựa chọn thuốc tiêu sợi huyết lâm sàng:", [
                "Alteplase (rt-PA) - Phổ biến nhất",
                "Tenecteplase (TNK-tPA) - Bolus một lần (Nghiên cứu PEITHO)",
                "Streptokinase",
                "Urokinase"
            ])
            
            if "Alteplase" in selected_lytic:
                st.write("**Phác đồ liều Alteplase (rt-PA) cá thể hóa:**")
                st.write("- **Phác đồ liều chuẩn (cho nhóm E1):** **100 mg truyền tĩnh mạch liên tục trong vòng 2 giờ**.")
                if weight < 65:
                    st.write(f"- **Phác đồ liều thấp (Half-dose) cho người nhẹ cân (<65kg) hoặc nhóm Sốc ẩn (D2):** Truyền tĩnh mạch **{weight * 0.5:.1f} mg** (truyền tĩnh mạch trong 2 giờ) để giảm thiểu nguy cơ xuất huyết não.")
                else:
                    st.write("- **Phác đồ liều thấp (Half-dose) cho nhóm D2:** Truyền tĩnh mạch **50 mg** truyền tĩnh mạch liên tục trong 2 giờ.")
                st.write("- **Phác đồ liều siêu thấp (Ultra-low dose):** **25 mg truyền tĩnh mạch chậm trong vòng 6 giờ**.")
                
            elif "Tenecteplase" in selected_lytic:
                st.write("**Phác đồ liều Tenecteplase (TNK-tPA) tiêm bolus tĩnh mạch chậm một lần duy nhất theo cân nặng thực tế (PEITHO):**")
                tnk_dose = 30
                if weight < 60: tnk_dose = 30
                elif 60 <= weight < 70: tnk_dose = 35
                elif 70 <= weight < 80: tnk_dose = 40
                elif 80 <= weight < 90: tnk_dose = 45
                else: tnk_dose = 50
                st.success(f"👉 **Liều TNK-tPA khuyến cáo cho cân nặng {weight}kg:** Tiêm tĩnh mạch nhanh (Bolus) một lần duy nhất **{tnk_dose} mg**.")
                
            elif "Streptokinase" in selected_lytic:
                st.write("**Phác đồ Streptokinase:**")
                st.write("- **Liều nạp:** **250,000 UI truyền tĩnh mạch trong 30 phút**, sau đó duy trì **100,000 UI/giờ truyền liên tục trong 12 - 24 giờ**.")
                st.write("- **Phác đồ truyền nhanh thay thế:** **1.5 triệu UI truyền tĩnh mạch liên tục trong vòng 2 giờ**.")
                
            else: # Urokinase
                st.write("**Phác đồ Urokinase tính theo cân nặng thực tế:**")
                uro_load = 4400 * weight
                uro_maint = 4400 * weight
                st.write(f"- **Liều nạp:** Truyền tĩnh mạch **{uro_load:,.0f} UI** trong vòng 10 phút.")
                st.write(f"- **Liều duy trì:** Truyền tĩnh mạch liên tục **{uro_maint:,.0f} UI/giờ kéo dài trong 12 giờ**.")

            st.write("**Khuyến cáo can thiệp lấy huyết khối bằng dụng cụ cơ học (Mechanical Thrombectomy - MT) (AHA 2026):**")
            st.info("💡 Lấy huyết khối cơ học bằng dụng cụ (MT) là lựa chọn cực kỳ ưu việt cho bệnh nhân nhóm D và E có chống chỉ định tuyệt đối với tiêu sợi huyết, hoặc khi tiêu sợi huyết hệ thống thất bại. MT giúp giải áp gánh nặng tim phải ngay lập tức mà không làm tăng nguy cơ xuất huyết não.")
            
        # Hiển thị Respiratory Modifier nếu có R
        if resp_modifier:
            st.error(f"📢 **Cảnh báo Modifier R (Hô hấp): Bệnh nhân được phân loại {final_group}**")
            if "C" in category:
                st.write("- Bệnh nhân có suy hô hấp đi kèm. Thở oxy hỗ trợ thông thường qua gọng mũi hoặc mặt nạ.")
            elif "D" in category:
                st.write("- Bệnh nhân suy hô hấp tiến triển nặng. Ưu tiên sử dụng oxy dòng cao (HFNC) >6 L/p hoặc mặt nạ không thở lại (NRB mask) để tránh tăng gánh tim phải.")
            else: # E
                st.write("- Bệnh nhân suy hô hấp nguy kịch/Ventilatory Failure. Bắt buộc hỗ trợ hô hấp bằng NIV/BiPAP hoặc thông khí xâm lấn. Hạn chế tối đa đặt nội khí quản máy thở áp lực dương lớn trừ khi bắt buộc (áp lực dương làm sụp đổ dòng máu về thất phải đang suy cấp, có thể gây ngừng tuần hoàn ngay khi đặt ống). Sẵn sàng chuẩn bị các thuốc vận mạch hoặc VA-ECMO khi đặt ống.")
