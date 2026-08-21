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
st.markdown("<div class='sub-header'>Công cụ Hỗ trợ Quyết định Lâm sàng Tương tác tại Giường bệnh (Bản Chuẩn hóa Guideline v15)</div>", unsafe_allow_html=True)

# Quản lý State bằng Session State
if 'step' not in st.session_state:
    st.session_state.step = 1  # 1: Chẩn đoán, 2: Phân loại lâm sàng, 3: Điều trị

if 'is_pregnant' not in st.session_state:
    st.session_state.is_pregnant = False

if 'final_category' not in st.session_state:
    st.session_state.final_category = None

if 'resp_modifier' not in st.session_state:
    st.session_state.resp_modifier = False

if 'g2_stable_flow' not in st.session_state:
    st.session_state.g2_stable_flow = "organ_damage"  # Tuần tự mới: organ_damage -> cpes -> prognosis

# Tạo các cột điều hướng bước ở đầu trang
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
# BƯỚC 1: CHẨN ĐOÁN & LOẠI TRỪ PE
# ==============================================================================
if st.session_state.step == 1:
    st.subheader("⚡ GIAI ĐOẠN 1: TIẾP CẬN CHẨN ĐOÁN BAN ĐẦU")
    
    col1_1, col1_2 = st.columns([1, 1], gap="large")
    
    with col1_1:
        st.subheader("📋 Đánh giá Sơ bộ & Xác suất lâm sàng tiền nghiệm (CPTP)")
        
        # Câu hỏi sàng lọc chống chỉ định loại trừ không hình ảnh học
        is_anticoagulated = st.checkbox("Bệnh nhân ĐANG sử dụng thuốc kháng đông liều đầy đủ (therapeutic anticoagulation)?")
        
        if is_anticoagulated:
            st.markdown("""
            <div class='u-card urgency-medium'>
                <strong>⚠️ CẢNH BÁO LÂM SÀNG:</strong> Bệnh nhân đang dùng kháng đông liều đầy đủ không phù hợp để áp dụng các chiến lược loại trừ dựa trên D-dimer (như PERC hay YEARS) vì D-dimer bị ảnh hưởng mạnh bởi thuốc kháng đông. Hãy tiến hành đánh giá lâm sàng trực tiếp hoặc chỉ định hình ảnh học nếu nghi ngờ tắc mạch tái phát/tiến triển.
            </div>
            """, unsafe_allow_html=True)
            
        is_suspected = st.checkbox("Bệnh nhân có triệu chứng/dấu hiệu nghi ngờ PE cấp tính (khó thở, đau ngực, ho ra máu, ngất...)?", value=True)
        is_pregnant_input = st.checkbox("Bệnh nhân hiện tại đang mang thai?", value=st.session_state.is_pregnant)
        st.session_state.is_pregnant = is_pregnant_input
        
        cptp_category = "LOW"
        cptp_score = 0.0
        
        if is_suspected:
            # Nhánh mang thai thích ứng YEARS
            if st.session_state.is_pregnant:
                st.markdown("<div class='section-card'>", unsafe_allow_html=True)
                st.write("🤰 **Quy trình thích ứng thai kỳ (Pregnancy-adapted YEARS):**")
                has_dvt_sym = st.checkbox("Bệnh nhân mang thai có triệu chứng sưng đau một bên chân gợi ý DVT?")
                
                if has_dvt_sym:
                    st.markdown("""
                    <div class='u-card urgency-high'>
                        <strong>🚨 CHỈ ĐỊNH SIÊU ÂM DOOPLER TĨNH MẠCH CHI DƯỚI (CUS):</strong><br>
                        Theo Guideline, thai phụ có triệu chứng DVT phải thực hiện siêu âm CUS trước tiên.
                    </div>
                    """, unsafe_allow_html=True)
                    
                    cus_result = st.radio("Kết quả siêu âm CUS chi dưới:", [
                        "Chưa thực hiện / Kết quả Âm tính (Không thấy huyết khối)",
                        "DƯƠNG TÍNH (Xác nhận có DVT chi dưới)"
                    ])
                    
                    if "DƯƠNG TÍNH" in cus_result:
                        st.markdown("""
                        <div class='u-card urgency-low'>
                            <strong>>>> KẾT LUẬN CHẨN ĐOÁN: XÁC NHẬN DVT (KHỞI TRỊ KHÁNG ĐÔNG NGAY)</strong><br>
                            Có bằng chứng DVT chân -> Chỉ định điều trị kháng đông LMWH ngay lập tức mà không cần chụp CTPA hay làm D-dimer để tránh phơi nhiễm phóng xạ!
                        </div>
                        """, unsafe_allow_html=True)
                        st.session_state.final_category = "B2"  # Giả định nhóm B
                        if st.button("📊 Chuyển ngay sang Bước 3: Điều trị", type="primary"):
                            st.session_state.step = 3
                            st.rerun()
                        st.markdown("</div>", unsafe_allow_html=True)
                        st.stop()
                st.markdown("</div>", unsafe_allow_html=True)
                
            # Đánh giá Wells/Geneva tiêu chuẩn
            score_type = st.radio("Chọn Thang điểm Đánh giá Xác suất lâm sàng tiền nghiệm:", ["Thang điểm Wells (Khuyên dùng)", "Thang điểm Geneva Rút gọn"])
            
            if score_type == "Thang điểm Wells (Khuyên dùng)":
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
                g3 = st.checkbox("Phẫu thuật hoặc gãy xương chi dưới trong vòng 1 tháng qua (+1)")
                g4 = st.checkbox("Ung thư đang hoạt động/tiến triển (+1)")
                g5 = st.checkbox("Đau chân một bên (+1)")
                g6 = st.checkbox("Ho ra máu (+1)")
                g_hr = st.selectbox("Tần số tim bệnh nhân:", ["< 75 ck/phút (0 điểm)", "75 - 94 ck/phút (+1 điểm)", ">= 95 ck/phút (+1 điểm)"])
                g8 = st.checkbox("Sưng và đau khi ấn dọc hệ tĩnh mạch sâu ở chân một bên (+1)")
                
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
            
            if not is_anticoagulated and cptp_category == "LOW":
                st.markdown("<div class='section-card'>", unsafe_allow_html=True)
                st.write("**1. Áp dụng Tiêu chuẩn loại trừ PE (PERC) tại giường:**")
                st.caption("Chỉ áp dụng khi xác suất lâm sàng tiền nghiệm <15% (Wells < 2). Nếu thỏa mãn tất cả 8 tiêu chí bên dưới (PERC âm tính), loại trừ PE hoàn toàn mà không cần xét nghiệm.")
                
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
                    if st.button("📊 Vẫn chuyển sang Phân loại & Điều trị (Đóng giả định)", type="secondary"):
                        st.session_state.step = 2
                        st.rerun()
                else:
                    st.markdown("<div class='u-card urgency-medium'><strong>>>> KẾT QUẢ PERC: DƯƠNG TÍNH</strong><br>Không thể loại trừ bằng PERC. Bắt buộc phải thực hiện xét nghiệm D-dimer theo một trong hai chiến lược bên dưới.</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Khách hàng không dùng kháng đông mới chạy tiếp D-dimer
            if not is_anticoagulated and cptp_category in ["LOW", "INTERMEDIATE"] and (cptp_category == "INTERMEDIATE" or any_perc_positive):
                st.markdown("<div class='section-card'>", unsafe_allow_html=True)
                st.write("**2. Lựa chọn Chiến lược D-dimer để loại trừ:**")
                st.warning("⚠️ CHÚ Ý: Chọn duy nhất 1 trong 2 chiến lược độc lập bên dưới. Tuyệt đối không trộn lẫn (không áp dụng hiệu chỉnh tuổi vào YEARS).")
                
                strategy = st.radio("Chọn chiến lược D-dimer:", [
                    "Chiến lược A: D-dimer theo độ tuổi (Age-Adjusted D-dimer)",
                    "Chiến lược B: Thuật toán YEARS (Adapted YEARS nếu có thai)"
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
                                st.session_state.step = 2
                                st.rerun()
                        else:
                            st.markdown(f"<div class='u-card urgency-high'><strong>>>> KẾT LUẬN: D-dimer ({d_dimer_val_a}) >= Ngưỡng cắt ({cutoff_a})</strong><br>CHỈ ĐỊNH HÌNH ẢNH HỌC (CTPA) ĐỂ XÁC ĐỊNH CHẨN ĐOÁN!</div>", unsafe_allow_html=True)
                
                else: # YEARS
                    if st.session_state.is_pregnant:
                        st.info("Chiến lược B: Thuật toán YEARS thích ứng thai kỳ (Pregnancy-Adapted YEARS) (Class 2b, LOE B-R)")
                    else:
                        st.info("Chiến lược B: Thuật toán YEARS tiêu chuẩn (Class 2a, LOE B-R)")
                        
                    st.write("Đánh giá 3 tiêu chí YEARS:")
                    y1 = st.checkbox("1. Có dấu hiệu lâm sàng của DVT (sưng đau chân)?", key="years_y1")
                    y2 = st.checkbox("2. Có ho ra máu?", key="years_y2")
                    y3 = st.checkbox("3. PE là chẩn đoán khả thi nhất trên lâm sàng?", key="years_y3")
                    
                    years_count = (1 if y1 else 0) + (1 if y2 else 0) + (1 if y3 else 0)
                    st.write(f"Số tiêu chí YEARS thỏa mãn: **{years_count}/3**")
                    
                    # Ngưỡng cắt YEARS cố định hoàn toàn (Không hiệu chỉnh tuổi!)
                    years_cutoff = 1000 if years_count == 0 else 500
                    st.write(f"Ngưỡng cắt D-dimer theo YEARS (cố định): **{years_cutoff} ng/mL**")
                    
                    d_dimer_val_b = st.number_input("Nhập nồng độ D-dimer thực tế đo được (ng/mL):", min_value=0, value=0, key="d_dimer_strategy_b")
                    
                    if d_dimer_val_b > 0:
                        if d_dimer_val_b < years_cutoff:
                            st.markdown(f"<div class='u-card urgency-low'><strong>>>> KẾT LUẬN: D-dimer ({d_dimer_val_b}) < Ngưỡng YEARS ({years_cutoff})</strong><br>LOẠI TRỪ THUYÊN TẮC PHỔI (PE) THÀNH CÔNG! An toàn để không chụp CTPA.</div>", unsafe_allow_html=True)
                            if st.button("📊 Vẫn chuyển sang Phân loại & Điều trị (Giả định)", type="secondary"):
                                st.session_state.step = 2
                                st.rerun()
                        else:
                            st.markdown(f"<div class='u-card urgency-high'><strong>>>> KẾT LUẬN: D-dimer ({d_dimer_val_b}) >= Ngưỡng YEARS ({years_cutoff})</strong><br>CHỈ ĐỊNH HÌNH ẢNH HỌC (CTPA) ĐỂ XÁC ĐỊNH CHẨN ĐOÁN!</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
            elif cptp_category == "HIGH" or is_anticoagulated:
                st.markdown("<div class='u-card urgency-high'><strong>>>> KẾT LUẬN: CHỈ ĐỊNH CHỤP HÌNH ẢNH HỌC PHỔI KHẨN CẤP LẬP TỨC!</strong><br>Bệnh nhân có xác suất lâm sàng rất cao (hoặc đang dùng kháng đông liều đầy đủ nghi ngờ tái phát). Tiến hành chụp CT động mạch phổi (CTPA) ngay mà không làm D-dimer.</div>", unsafe_allow_html=True)
                
            # Phần hướng dẫn thay thế CTPA nếu có chống chỉ định
            st.markdown("<div class='section-card'>", unsafe_allow_html=True)
            st.write("🌿 **Nhánh chẩn đoán thay thế (Nếu chống chỉ định CTPA):**")
            st.caption("Nếu bệnh nhân có chống chỉ định tuyệt đối với CTPA (như suy thận rất nặng CrCl < 30 mL/phút, dị ứng nặng với thuốc cản quang có iod, hoặc phụ nữ mang thai mong muốn giảm thiểu tia xạ vú tối đa):")
            st.info("👉 **Khuyến cáo (Class 2a):** Thực hiện **Xạ hình thông khí - tưới máu phổi (V/Q Scan)**. Trong đó, **V/Q SPECT được khuyến cáo ưu tiên hơn V/Q phẳng thông thường (planar V/Q)** nhờ độ nhạy và độ đặc hiệu cao hơn đáng kể.")
            
            if st.button("📊 Chuyển sang Giai đoạn Phân loại & Điều trị sau khi có kết quả CTPA hoặc V/Q", type="primary"):
                st.session_state.step = 2
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    # Nút chuyển tiếp nhanh ở cuối trang
    st.markdown("---")
    col_nav = st.columns([4, 1])
    with col_nav[1]:
        if st.button("Tiếp tục sang GĐ 2 ➡️", use_container_width=True):
            st.session_state.step = 2
            st.rerun()

# ==============================================================================
# BƯỚC 2: PHÂN LOẠI LÂM SÀNG CẤP TÍNH AHA/ACC 2026 (RẼ NHÁNH TUẦN TỰ)
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
            "Tụt huyết áp thoáng qua (<15 phút, tự hồi phục nhanh hoặc đáp ứng nhanh sau bù dịch)",
            "Tụt huyết áp kéo dài / Sốc tim thực sự (Huyết áp tâm thu <90 mmHg hoặc giảm >40 mmHg kéo dài >=15 phút, hoặc cần thuốc vận mạch để duy trì HA)",
            "Sốc tim kháng trị hoặc Ngừng tuần hoàn (SCAI Stage D/E, hoặc cardiac arrest không đạt ROSC sau 30 phút hồi sức)",
            "Thuyên tắc phổi phát hiện tình cờ, hoàn toàn không có triệu chứng (Category A - Subclinical PE)"
        ])
        
        # Xử lý các nhánh huyết động không ổn định rõ rệt
        if "Sốc tim kháng trị" in primary_hemo:
            st.session_state.final_category = "E2"
            st.markdown("""
            <div class='u-card urgency-high'>
                <strong>>>> CHẨN ĐOÁN LÂM SÀNG: NHÓM E2 (Suy tim phổi hoàn toàn - Sốc kháng trị / Ngừng tuần hoàn)</strong><br>
                <em>Định nghĩa:</em> Sốc tim kháng trị (SCAI Stage D hoặc E) hoặc ngừng tuần hoàn (cardiac arrest) không đạt ROSC sau 30 phút hồi sức tích cực. Đòi hỏi hồi sức nâng cao khẩn cấp.
            </div>
            """, unsafe_allow_html=True)
            
            # Sàng lọc suy hô hấp (Modifier R) cho nhóm E
            st.write("---")
            st.write("##### 📢 Đánh giá Modifier R cho nhóm E")
            r_e = st.checkbox("Đang cần thông khí áp lực dương không xâm lấn (NIV/BiPAP) HOẶC đang phải thông khí xâm lấn (đặt nội khí quản thở máy)?")
            st.session_state.resp_modifier = r_e
            
            if st.button("Xác nhận & Đi tới Bước 3: Điều trị ➡️", type="primary", use_container_width=True):
                st.session_state.step = 3
                st.rerun()
            
        elif "Tụt huyết áp kéo dài" in primary_hemo:
            st.session_state.final_category = "E1"
            st.markdown("""
            <div class='u-card urgency-high'>
                <strong>>>> CHẨN ĐOÁN LÂM SÀNG: NHÓM E1 (Suy tim phổi hoàn toàn - Sốc tim thực sự)</strong><br>
                <em>Định nghĩa:</em> Sốc tim hoặc tụt huyết áp kéo dài (HA tâm thu <90 mmHg hoặc giảm >40 mmHg kéo dài >=15 phút, hoặc cần dùng vận mạch). Cần điều trị tích cực tại ICU.
            </div>
            """, unsafe_allow_html=True)
            
            # Sàng lọc suy hô hấp (Modifier R) cho nhóm E
            st.write("---")
            st.write("##### 📢 Đánh giá Modifier R cho nhóm E")
            r_e = st.checkbox("Đang cần thông khí áp lực dương không xâm lấn (NIV/BiPAP) HOẶC đang phải thông khí xâm lấn (đặt nội khí quản thở máy)?")
            st.session_state.resp_modifier = r_e
            
            if st.button("Xác nhận & Đi tới Bước 3: Điều trị ➡️", type="primary", use_container_width=True):
                st.session_state.step = 3
                st.rerun()

        elif "phát hiện tình cờ" in primary_hemo:
            st.session_state.final_category = "A"
            st.markdown("""
            <div class='u-card urgency-low'>
                <strong>>>> CHẨN ĐOÁN LÂM SÀNG: NHÓM A (Thuyên tắc phổi dưới lâm sàng - Subclinical PE)</strong><br>
                Bệnh nhân hoàn toàn không có triệu chứng nghi ngờ và được phát hiện tình cờ trên CTPA khi làm vì mục đích khác. Thích hợp để quản lý ngoại trú an toàn.
            </div>
            """, unsafe_allow_html=True)
            st.session_state.resp_modifier = False
            
            if st.button("Xác nhận & Đi tới Bước 3: Điều trị ➡️", type="primary", use_container_width=True):
                st.session_state.step = 3
                st.rerun()

        # ==============================================================================
        # LUỒNG TUẦN TỰ CHO HUYẾT ÁP ỔN ĐỊNH VÀ TỤT HUYẾT ÁP THOÁNG QUA (YÊU CẦU MỚI: ĐÁNH TỔN THƯƠNG CƠ QUAN TRƯỚC!)
        # ==============================================================================
        if primary_hemo in ["Huyết động ổn định (Huyết áp bình thường)", "Tụt huyết áp thoáng qua (<15 phút, tự hồi phục nhanh hoặc đáp ứng nhanh sau bù dịch)"]:
            
            # --------------------------------------------------------------------------
            # BƯỚC 2.1: ĐÁNH GIÁ TỔN THƯƠNG CƠ QUAN TRƯỚC (QUY TRÌNH MỚI!)
            # --------------------------------------------------------------------------
            if st.session_state.g2_stable_flow == "organ_damage":
                st.markdown("<div class='section-card'>", unsafe_allow_html=True)
                st.write("##### 📋 BƯỚC 2.1: Đánh giá Tổn thương cơ quan đích & Giảm tưới máu mô")
                st.caption("Hãy rà soát kỹ các dấu hiệu giảm tưới máu hoặc suy chức năng cơ quan đích dưới đây:")
                
                opt_lactate = st.checkbox("Nồng độ Lactate huyết thanh > 2.0 mmol/L")
                opt_aki = st.checkbox("Suy thận cấp (AKI) (Creatinine tăng >= 0.3 mg/dL hoặc gấp >= 1.5 lần nền trong 24h)")
                opt_oliguria = st.checkbox("Thiểu niệu tiến triển (Lượng nước tiểu < 0.5 mL/kg/giờ kéo dài >= 2 giờ)")
                opt_mental = st.checkbox("Thay đổi trạng thái tâm thần cấp tính (lờ đờ, u ám, ngủ gà, vật vã do thiếu máu não)")
                opt_ci_map = st.checkbox("Huyết áp trung bình MAP < 60 mmHg HOẶC Chỉ số tim (Cardiac Index) <= 2.2 L/min/m²")
                
                has_hypoperfusion = opt_lactate or opt_aki or opt_oliguria or opt_mental or opt_ci_map
                
                if has_hypoperfusion:
                    st.session_state.final_category = "D2"
                    st.markdown("""
                    <div class='u-card urgency-high'>
                        <strong>>>> CHẨN ĐOÁN LÂM SÀNG: NHÓM D2 (Sốc ẩn - Incipient Cardiopulmonary Failure)</strong><br>
                        Phát hiện thấy bằng chứng giảm tưới máu mô/tổn thương cơ quan đích mặc dù huyết áp vẫn đang được cơ thể bù trừ. Bệnh nhân có nguy cơ sụp đổ tuần hoàn cao!
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Đánh giá Respiratory Modifier cho nhóm D
                    st.write("---")
                    st.write("##### 📢 Đánh giá Modifier R cho nhóm D")
                    r_d = st.checkbox("Đang cần thở oxy lưu lượng >6 L/phút qua gọng mũi thường HOẶC mặt nạ không thở lại (NRB)?")
                    st.session_state.resp_modifier = r_d
                    
                    if st.button("Xác nhận & Đi tới Bước 3: Điều trị ➡️", type="primary", use_container_width=True):
                        st.session_state.step = 3
                        st.rerun()
                else:
                    st.success("Không phát hiện dấu hiệu giảm tưới máu cơ quan đích nào.")
                    
                    if primary_hemo == "Tụt huyết áp thoáng qua (<15 phút, tự hồi phục nhanh hoặc đáp ứng nhanh sau bù dịch)":
                        # Tụt HA thoáng qua + Không giảm tưới máu -> D1
                        st.session_state.final_category = "D1"
                        st.markdown("""
                        <div class='u-card urgency-medium'>
                            <strong>>>> CHẨN ĐOÁN LÂM SÀNG: NHÓM D1 (Tụt huyết áp thoáng qua)</strong><br>
                            Huyết động có biểu hiện mất bù thoáng qua nhưng chưa tiến triển thành tổn thương cơ quan đích.
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Đánh giá Respiratory Modifier cho nhóm D
                        st.write("---")
                        st.write("##### 📢 Đánh giá Modifier R cho nhóm D")
                        r_d = st.checkbox("Đang cần thở oxy lưu lượng >6 L/phút qua gọng mũi thường HOẶC mặt nạ không thở lại (NRB)?")
                        st.session_state.resp_modifier = r_d
                        
                        if st.button("Xác nhận & Đi tới Bước 3: Điều trị ➡️", type="primary", use_container_width=True):
                            st.session_state.step = 3
                            st.rerun()
                    else:
                        # Huyết áp bình thường + Không giảm tưới máu -> Đánh giá CPES
                        st.info("Huyết áp bình thường và không có giảm tưới máu. Hãy bấm nút dưới đây để chuyển sang đánh giá thang điểm CPES.")
                        if st.button("Xác nhận Không giảm tưới máu -> Tiếp tục đánh giá CPES ➡️", type="primary", use_container_width=True):
                            st.session_state.g2_stable_flow = "cpes"
                            st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

            # --------------------------------------------------------------------------
            # BƯỚC 2.2: ĐÁNH GIÁ CPES (CHỈ CHO HUYẾT ÁP BÌNH THƯỜNG KHÔNG GIẢM TƯỚI MÁU)
            # --------------------------------------------------------------------------
            elif st.session_state.g2_stable_flow == "cpes" and primary_hemo == "Huyết động ổn định (Huyết áp bình thường)":
                st.markdown("<div class='section-card'>", unsafe_allow_html=True)
                st.write("##### 📊 BƯỚC 2.2: Đánh giá Thang điểm CPES (Composite Pulmonary Embolism Shock)")
                st.caption("CPES (0-6 điểm) giúp sàng lọc sớm nguy cơ tiến triển thành Sốc ẩn ở bệnh nhân có huyết áp ổn định và không có tổn thương cơ quan trước đó.")
                
                c1 = st.checkbox("1. Tăng men tim Troponin tim (+1)")
                c2 = st.checkbox("2. Tăng peptide lợi niệu BNP hoặc NT-proBNP (+1)")
                c3 = st.checkbox("3. Giảm chức năng RV mức độ trung bình hoặc nặng trên siêu âm (+1)")
                c4 = st.checkbox("4. Có gánh nặng huyết khối trung tâm (Saddle PE) trên CTPA (+1)")
                c5 = st.checkbox("5. Có huyết khối tĩnh mạch sâu (DVT) đoạn gần kèm theo (+1)")
                c6 = st.checkbox("6. Tần số tim >= 100 chu kỳ/phút (+1)")
                
                cpes_score = sum([c1, c2, c3, c4, c5, c6])
                st.metric("Tổng điểm CPES", f"{cpes_score}/6 điểm")
                
                if cpes_score == 6:
                    st.markdown("""
                    <div class='u-card urgency-high'>
                        <strong>>>> ĐẠT ĐIỂM CPES TỐI ĐA 6/6!</strong><br>
                        Bệnh nhân đạt CPES 6/6 -> Tự động quy đổi phân loại vào <strong>Nhóm D2 (Sốc ẩn - Nguy cơ rất cao)</strong> theo AHA/ACC 2026.
                    </div>
                    """, unsafe_allow_html=True)
                    st.session_state.final_category = "D2"
                    
                    # Đánh giá Respiratory Modifier cho nhóm D
                    st.write("---")
                    st.write("##### 📢 Đánh giá Modifier R cho nhóm D")
                    r_d = st.checkbox("Đang cần thở oxy lưu lượng >6 L/phút qua gọng mũi thường HOẶC mặt nạ không thở lại (NRB)?")
                    st.session_state.resp_modifier = r_d
                    
                    if st.button("Xác nhận & Đi tới Bước 3: Điều trị ➡️", type="primary", use_container_width=True):
                        st.session_state.step = 3
                        st.rerun()
                else:
                    st.info(f"Điểm CPES = {cpes_score}/6 (< 6/6). Hãy tiếp tục chuyển sang đánh giá các thang điểm tiên lượng lâm sàng để phân loại nhóm B hay C.")
                    if st.button("Xác nhận CPES < 6 -> Đánh giá Thang điểm Tiên lượng Lâm sàng ➡️", type="primary", use_container_width=True):
                        st.session_state.g2_stable_flow = "prognosis"
                        st.rerun()
                        
                if st.button("⬅️ Quay lại đánh giá Tổn thương cơ quan", type="secondary"):
                    st.session_state.g2_stable_flow = "organ_damage"
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

            # --------------------------------------------------------------------------
            # BƯỚC 2.3: ĐÁNH GIÁ THANG ĐIỂM TIÊN LƯỢNG LÂM SÀNG
            # --------------------------------------------------------------------------
            elif st.session_state.g2_stable_flow == "prognosis":
                st.markdown("<div class='section-card'>", unsafe_allow_html=True)
                st.write("##### 📋 BƯỚC 2.3: Đánh giá Thang điểm Tiên lượng Lâm sàng")
                st.caption("Do không có giảm tưới máu hay CPES 6/6, bệnh nhân sẽ được phân loại vào Nhóm B (Nguy cơ thấp) hoặc Nhóm C (Nguy cơ trung bình). Hãy lựa chọn 1 thang điểm duy nhất:")
                
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
                    is_clinical_high = pesi_score > 85 # Class III trở lên là nguy cơ cao lâm sàng (C)
                    
                elif "Hestia" in score_method:
                    st.info("Sàng lọc tiêu chí Hestia (11 mục loại trừ chuẩn):")
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
                        st.error("Hestia dương tính: Bệnh nhân không thể điều trị ngoại trú -> Xếp vào nguy cơ trung bình (Nhóm C).")
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
                    st.markdown("<div class='u-card urgency-medium'><strong>KẾT QUẢ ĐÁNH GIÁ: LÂM SÀNG NGUY CƠ CAO (Category C)</strong><br>Bệnh nhân được xếp vào Nhóm C. Hãy bấm nút dưới đây để đánh giá Thất phải (RV) và Biomarkers để phân nhóm sâu hơn (C1, C2, C3).</div>", unsafe_allow_html=True)
                    if st.button("Đánh giá Thất phải (RV) & Biomarkers ➡️", type="primary", use_container_width=True):
                        st.session_state.g2_stable_flow = "rv_biomarkers"
                        st.rerun()
                else:
                    st.markdown("<div class='u-card urgency-low'><strong>KẾT QUẢ ĐÁNH GIÁ: LÂM SÀNG NGUY CƠ THẤP (Category B)</strong><br>Bệnh nhân được xếp vào Nhóm B. Hãy bấm nút dưới đây để đánh giá vị trí huyết khối để phân loại B1 hay B2.</div>", unsafe_allow_html=True)
                    if st.button("Đánh giá vị trí huyết khối ➡️", type="primary", use_container_width=True):
                        st.session_state.g2_stable_flow = "hk_position"
                        st.rerun()
                        
                if st.button("⬅️ Quay lại đánh giá CPES", type="secondary"):
                    st.session_state.g2_stable_flow = "cpes"
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
                rv_echo_4 = st.checkbox("Vận tốc hở 3 lá TR >= 2.9 m/s")
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
                
                if st.button("Xác nhận Phân nhóm & Chuyển sang Bước 3: Điều trị ➡️", type="primary", use_container_width=True):
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
                st.caption("Xác định vị trí giải phẫu của huyết khối để chia nhóm B thành B1 (Dưới phân thùy) hoặc B2 (Phân thùy trở lên).")
                
                is_subsegmental = st.checkbox("Huyết khối chỉ khu trú ở nhánh dưới phân thùy (Subsegmental PE) trên CTPA?")
                
                if is_subsegmental:
                    st.session_state.final_category = "B1"
                else:
                    st.session_state.final_category = "B2"
                
                st.write("---")
                st.success(f"Xác lập phân nhóm: **Nhóm {st.session_state.final_category}**")
                
                # BỔ SUNG RESPIRATORY MODIFIER CHO NHÓM B
                st.write("##### 📢 Đánh giá Modifier R cho nhóm B")
                r_b = st.checkbox("SpO2 < 90% ở khí trời, HOẶC nhịp thở (RR) >= 30 lần/phút, HOẶC đang cần bổ sung oxy hỗ trợ thông thường (qua gọng kính/mặt nạ)?")
                st.session_state.resp_modifier = r_b
                
                if st.button("Xác nhận Phân nhóm & Chuyển sang Bước 3: Điều trị ➡️", type="primary", use_container_width=True):
                    st.session_state.step = 3
                    st.rerun()
                    
                if st.button("⬅️ Quay lại chọn Thang điểm tiên lượng", type="secondary"):
                    st.session_state.g2_stable_flow = "prognosis"
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

    with col2_2:
        st.subheader("📋 Sơ đồ Tóm tắt Phân tầng AHA/ACC 2026")
        st.markdown("""
        *   **Nhóm E (Nguy kịch):** Ngừng tuần hoàn / Sốc tim thực sự.
        *   **Nhóm D (Chớm suy):** Sốc ẩn (D2) hoặc Tụt huyết áp thoáng qua (D1).
        *   **Nhóm C (Nguy cơ trung bình):** Thang điểm sPESI/PESI/Hestia cao.
            *   *C3:* Có cả rối loạn chức năng RV và tăng men tim.
            *   *C2:* Có rối loạn chức năng RV HOẶC tăng men tim.
            *   *C1:* Không có rối loạn chức năng RV và men tim bình thường.
        *   **Nhóm B (Nguy cơ thấp):** Thang điểm tiên lượng lâm sàng thấp.
            *   *B2:* Huyết khối từ nhánh phân thùy trở lên.
            *   *B1:* Huyết khối khu trú ở nhánh dưới phân thùy.
        *   **Nhóm A:** Thuyên tắc phổi phát hiện tình cờ, không triệu chứng.
        """)

# ==============================================================================
# BƯỚC 3: CÁ THỂ HÓA ĐIỀU TRỊ & TÍNH LIỀU
# ==============================================================================
elif st.session_state.step == 3:
    st.subheader("💊 GIAI ĐOẠN 3: CÁ THỂ HÓA ĐIỀU TRỊ VÀ TÍNH LIỀU THUỐC")
    
    col3_1, col3_2 = st.columns([1, 1], gap="large")
    
    with col3_1:
        st.subheader("🧬 1. Nhập thông số sinh học & Tình huống đặc biệt")
        
        # Nhập thông số cân nặng chiều cao chức năng thận
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
        
        # TÌNH HUỐNG LÂM SÀNG ĐẶC BIỆT
        st.markdown("---")
        st.write("💼 **Các tình huống lâm sàng đặc biệt:**")
        has_aps = st.checkbox("Bệnh nhân mắc Hội chứng kháng Phospholipid (APS) xác định?", key="has_aps")
        is_pregnant_t2 = st.checkbox("Bệnh nhân đang mang thai hoặc cho con bú?", value=st.session_state.is_pregnant, key="is_pregnant_t2")
        st.session_state.is_pregnant = is_pregnant_t2
        
        has_cancer = st.checkbox("Bệnh nhân mắc ung thư đang hoạt động / tiến triển (Cancer-associated thrombosis)?", key="has_cancer")
        has_drug_interactions = st.checkbox("Đang sử dụng thuốc tương tác mạnh (như Ketoconazole, Itraconazole, Ritonavir, Rifampicin, Phenytoin, Carbamazepine)?", key="has_drug_interactions")
        
        # Rà soát chống chỉ định tiêu sợi huyết hệ thống
        st.markdown("---")
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
                st.success("Không phát hiện chống chỉ định tiêu sợi huyết hệ thống.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col3_2:
        r_suffix = "R" if st.session_state.resp_modifier else ""
        final_group = f"{st.session_state.final_category}{r_suffix}" if st.session_state.final_category else "Chưa xác định"
        
        st.markdown(f"<div class='result-card'><h3>PHÂN NHÓM LÂM SÀNG: <span style='color:#DC2626;'>NHÓM {final_group}</span></h3></div>", unsafe_allow_html=True)
        
        # --------------------------------------------------------------------------
        # PHÁC ĐỒ TRIAGE & KHUYẾN CÁO PERT (Class 2a, LOE C-LD cho C, D, E)
        # --------------------------------------------------------------------------
        st.write("##### 📍 Phân luồng điều trị (Triage) & Khuyến cáo PERT:")
        
        if st.session_state.final_category in ["A", "B1", "B2"]:
            st.info("""
            **Khuyến cáo Quản lý Ngoại trú (Class 1, LOE A):**<br>
            Có thể cân nhắc điều trị ngoại trú hoặc xuất viện sớm cho các bệnh nhân thuộc **Nhóm A** hoặc một số ít bệnh nhân **Nhóm B** nếu thỏa mãn đầy đủ các điều kiện y khoa - xã hội sau:<br>
            1. Điểm sPESI = 0 hoặc Hestia âm tính (đã rà soát ở Giai đoạn 2).<br>
            2. Bệnh nhân có điều kiện gia đình, xã hội ổn định, có người hỗ trợ.<br>
            3. Tiếp cận thuốc kháng đông ngay lập tức và thuận tiện.<br>
            4. Có kế hoạch theo dõi y khoa và hẹn tái khám chuyên khoa nhanh chóng, tin cậy (trong vòng 24-72 giờ đầu).
            """, unsafe_allow_html=True)
            
        elif st.session_state.final_category in ["C1", "C2", "C3"]:
            pert_text = "📞 **Khuyến cáo kích hoạt PERT (Pulmonary Embolism Response Team):** Cân nhắc hội chẩn đa chuyên khoa PERT (Class 2a, LOE C-LD) để tối ưu hóa quyết định điều trị nâng cao nếu cần thiết, đặc biệt là nhóm C3."
            if st.session_state.final_category == "C3":
                st.markdown(f"""
                <div class='u-card urgency-medium'>
                    <strong>📍 Nơi điều trị: ICU HOẶC ĐƠN VỊ ĐỆM (Intermediate/Step-down)</strong><br>
                    Theo dõi sát huyết động liên tục trong 24-72 giờ đầu (Class 2a) do có nguy cơ tiến triển thành sốc ẩn rất cao.<br>
                    {pert_text}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info(f"📍 **Nơi điều trị:** Nhập viện điều trị nội trú tại Khoa Thường (Nội tim mạch/Nội chung).\n\n{pert_text}")
                
        elif st.session_state.final_category in ["D1", "D2", "E1", "E2"]:
            st.markdown(f"""
            <div class='u-card urgency-high'>
                <strong>📍 Nơi điều trị: KHOA HỒI SỨC TÍCH CỰC (ICU/CCU) tối khẩn cấp</strong><br>
                Theo dõi huyết động liên tục.<br>
                📞 **BẮT BUỘC KÍCH HOẠT NGAY ĐỘI PHẢN ỨNG NHANH PERT:** Phối hợp đa chuyên khoa khẩn cấp (Class 2a, LOE C-LD) để đưa ra quyết định tái tưới máu can thiệp nâng cao.
            </div>
            """, unsafe_allow_html=True)

        st.write("---")
        
        # --------------------------------------------------------------------------
        # PHÁC ĐỒ ĐIỀU TRỊ CHUẨN CHO NHÓM A, B (KHÁNG ĐÔNG ĐƯỜNG UỐNG ƯU TIÊN)
        # --------------------------------------------------------------------------
        if st.session_state.final_category in ["A", "B1", "B2"]:
            st.success("💊 **Kháng đông ưu tiên: DOACs đường uống (Class 1, LOE B-R)**")
            
            if st.session_state.final_category == "B1":
                st.warning("👉 *Lưu ý Nhóm B1 (Dưới phân thùy):* Guideline cho phép theo dõi sát lâm sàng và siêu âm tĩnh mạch chi dưới định kỳ mà chưa cần dùng kháng đông ngay nếu bệnh nhân có nguy cơ chảy máu cao, không có triệu chứng lâm sàng và KHÔNG CÓ DVT chi dưới (Class 2b). Nếu có DVT đi kèm, bắt buộc dùng kháng đông tiêu chuẩn.")
            
            # Check tình huống bắt buộc VKA hoặc LMWH
            if st.session_state.is_pregnant:
                st.error("🤰 **CHỈ ĐỊNH BẮT BUỘC CHO THAI KỲ (CHỐNG CHỈ ĐỊNH DOACs/VKA):**\nChống chỉ định dùng DOACs và VKA trong thai kỳ. Bắt buộc sử dụng LMWH (Enoxaparin) liều chuẩn theo cân nặng suốt thai kỳ và ít nhất 6 tuần sau sinh (tối thiểu 3 tháng tổng thời gian điều trị).")
                st.write(f"- **Phác đồ Enoxaparin đề xuất:** **{weight * 1.0:.1f} mg tiêm dưới da mỗi 12 giờ** (1.0 mg/kg mỗi 12h).")
            elif has_aps:
                st.error("🩸 **HỘI CHỨNG KHÁNG PHOSPHOLIPID - APS (CHỐNG CHỈ ĐỊNH DOACs):**\nChống chỉ định dùng DOACs do tăng nguy cơ tắc mạch tái phát. Bắt buộc khởi đầu bằng kháng đông tiêm (LMWH/UFH) sau đó gối sang **Kháng Vitamin K (VKA - Warfarin)** duy trì lâu dài với đích **INR 2.0 - 3.0 (Class 1)**.")
            elif has_drug_interactions:
                st.warning("⚠️ **TƯƠNG TÁC THUỐC MẠNH (CHỐNG CHỈ ĐỊNH DOACs):**\nThuốc đồng vận làm biến đổi nồng độ DOACs nguy hiểm. Khuyến cáo dùng LMWH dài hạn hoặc chuyển sang VKA (theo dõi sát INR).")
            else:
                if has_cancer:
                    st.info("🎗️ *Bệnh nhân Ung thư (CAT):* Khuyến cáo ưu tiên dùng DOACs hoặc LMWH hơn là VKA (Class 1).")
                
                # CHUẨN HÓA LIỀU DOAC (BỎ LỖI GIẢM LIỀU CỦA AF!)
                st.write("**• Apixaban:**")
                st.write(f"  - *Liều tấn công:* **10 mg uống x 2 lần/ngày** (10 mg BID) trong 7 ngày đầu.")
                st.write("  - *Liều duy trì:* **5 mg uống x 2 lần/ngày** (5 mg BID).")
                st.caption("⚠️ *Lưu ý y khoa:* Không áp dụng công thức giảm liều AF (giảm xuống 2.5 mg BID dựa trên tuổi, cân nặng, creatinine) trong điều trị PE cấp tính. Liều 2.5 mg BID chỉ dùng ở giai đoạn kéo dài (extended phase) sau 3-6 tháng điều trị ban đầu.")
                
                st.write("**• Rivaroxaban:**")
                st.write(f"  - *Liều tấn công:* **15 mg uống x 2 lần/ngày** (15 mg BID) trong 21 ngày đầu.")
                st.write("  - *Liều duy trì:* **20 mg uống hằng ngày** (20 mg QD) cùng thức ăn.")
                st.caption("⚠️ *Lưu ý y khoa:* Không giảm liều duy trì xuống 15 mg QD cho bệnh nhân suy thận CrCl 30-49 mL/phút trong điều trị PE cấp tính. Nếu bệnh nhân suy thận nặng (CrCl < 30 mL/phút), chống chỉ định DOACs, cân nhắc dùng LMWH hoặc VKA.")

        # --------------------------------------------------------------------------
        # PHÁC ĐỒ KHÁNG ĐÔNG TIÊM CHO NHÓM C1, C2, C3, D1, D2, E1 (LMWH > UFH)
        # --------------------------------------------------------------------------
        elif st.session_state.final_category in ["C1", "C2", "C3", "D1", "D2", "E1"]:
            st.success("💊 **Kháng đông tiêm khởi đầu (C1 - E1): LMWH được khuyến cáo hơn UFH (Class 1)**")
            st.caption("Kháng đông tiêm được chỉ định ngay lập tức trong thời gian chờ đánh giá thêm hoặc can thiệp.")
            
            # Tính liều Enoxaparin (LMWH) - ƯU TIÊN HÀNG ĐẦU
            st.write("🌟 **LỰA CHỌN ƯU TIÊN: Heparin trọng lượng phân tử thấp (LMWH - Enoxaparin)**")
            if is_pregnant_t2:
                st.info("🤰 *Bệnh nhân đang mang thai:* Enoxaparin là lựa chọn an toàn và bắt buộc (không qua bánh nhau).")
                
            if crcl >= 30:
                enox_dose = weight * 1.0
                st.write(f"- **Liều Enoxaparin tiêu chuẩn:** **{enox_dose:.1f} mg tiêm dưới da mỗi 12 giờ** (1.0 mg/kg Q12h).")
                if bmi >= 40 or weight > 150:
                    enox_reduced = weight * 0.8
                    st.warning(f"⚠️ *Lưu ý béo phì độ III (BMI = {bmi:.1f}):* Có thể cân nhắc điều chỉnh giảm liều xuống **{enox_reduced:.1f} mg mỗi 12 giờ** (0.8 mg/kg Q12h) để giảm nguy cơ chảy máu (Class 2b, LOE B-NR).")
            elif 15 <= crcl < 30:
                enox_dose = weight * 1.0
                st.write(f"- **Liều Enoxaparin hiệu chỉnh suy thận nặng (CrCl 15-29 mL/phút):** **{enox_dose:.1f} mg tiêm dưới da mỗi 24 giờ** (1.0 mg/kg Q24h). Cần theo dõi nồng độ đỉnh Anti-Xa (đạt 3-5h sau liều thứ 3).")
            else:
                st.error("- **Enoxaparin (LMWH):** Chống chỉ định tuyệt đối do CrCl < 15 mL/phút.")

            # Tính liều UFH - THAY THẾ
            st.write("👉 **LỰA CHỌN THAY THẾ: Heparin không phân đoạn (UFH) truyền tĩnh mạch**")
            st.caption("Chỉ định thay thế khi bệnh nhân có chống chỉ định với LMWH (CrCl < 15), hoặc khi bác sĩ dự kiến sẽ can thiệp tái tưới máu ngay lập tức và cần tính đảo ngược nhanh của UFH.")
            
            ufh_bolus = min(80 * weight, 10000)
            ufh_maint = min(18 * weight, 1600)  # SỬA LỖI: ÁP TRẦN 1600 UI/h
            st.write(f"- **Liều nạp Bolus tĩnh mạch ban đầu:** **{ufh_bolus:.0f} UI** (Áp trần tối đa 10,000 UI).")
            st.write(f"- **Tốc độ truyền tĩnh mạch duy trì ban đầu:** **{ufh_maint:.0f} UI/giờ** (Áp trần tối đa **1,600 UI/giờ** để phòng ngừa quá liều ban đầu trước khi có kết quả aPTT/Anti-Xa), chỉnh liều theo aPTT.")

        # --------------------------------------------------------------------------
        # PHÁC ĐỒ KHÁNG ĐÔNG TIÊM CHO NHÓM E2 (YÊU CẦU: LINH HOẠT LMWH/UFH)
        # --------------------------------------------------------------------------
        elif st.session_state.final_category == "E2":
            st.success("💊 **Kháng đông tiêm khởi đầu ở Nhóm E2: Cần linh hoạt giữa UFH và LMWH**")
            st.caption("Trong tình huống ngừng tuần hoàn hoặc sốc tim kháng trị (E2), việc lựa chọn giữa UFH và LMWH cần được quyết định linh hoạt tùy theo bối cảnh cụ thể (khả năng đảo ngược tác dụng nhanh, chức năng thận và kế hoạch can thiệp hỗ trợ tuần hoàn ECMO/phẫu thuật).")
            
            tab_ufh, tab_lmwh = st.tabs(["🌟 Lựa chọn UFH (Dễ kiểm soát)", "🌟 Lựa chọn LMWH (Hạn chế HIT)"])
            
            with tab_ufh:
                st.write("**Heparin không phân đoạn (UFH) truyền tĩnh mạch:**")
                st.caption("Được ưa chuộng hơn trong pha cấp cứu cực kỳ nguy kịch cần can thiệp ngoại khoa khẩn cấp, ECMO hoặc khi chức năng thận chưa xác định được ngay.")
                ufh_bolus = min(80 * weight, 10000)
                ufh_maint = min(18 * weight, 1600)
                st.write(f"- **Liều nạp Bolus tĩnh mạch ban đầu:** **{ufh_bolus:.0f} UI** (Áp trần tối đa 10,000 UI).")
                st.write(f"- **Tốc độ truyền tĩnh mạch duy trì ban đầu:** **{ufh_maint:.0f} UI/giờ** (Áp trần tối đa **1,600 UI/giờ**), chỉnh liều sát theo aPTT.")
                
            with tab_lmwh:
                st.write("**Heparin trọng lượng phân tử thấp (LMWH - Enoxaparin):**")
                st.caption("Có thể cân nhắc nhờ tính tiện dụng, không đòi hỏi theo dõi xét nghiệm đông máu liên tục và nguy cơ bị giảm tiểu cầu do Heparin (HIT) thấp hơn.")
                if crcl >= 30:
                    enox_dose = weight * 1.0
                    st.write(f"- **Liều Enoxaparin tiêu chuẩn:** **{enox_dose:.1f} mg tiêm dưới da mỗi 12 giờ** (1.0 mg/kg Q12h).")
                elif 15 <= crcl < 30:
                    enox_dose = weight * 1.0
                    st.write(f"- **Liều Enoxaparin hiệu chỉnh:** **{enox_dose:.1f} mg tiêm dưới da mỗi 24 giờ** (1.0 mg/kg Q24h).")
                else:
                    st.error("- Chống chỉ định Enoxaparin do CrCl < 15 mL/phút.")

        # --------------------------------------------------------------------------
        # LIỆU PHÁP CAN THIỆP TÁI TƯỚI MÁU NÂNG CAO (CDL, SURGERY, VA-ECMO THEO TABLE 7)
        # --------------------------------------------------------------------------
        if st.session_state.final_category in ["C3", "D1", "D2", "E1", "E2"]:
            st.write("---")
            st.write("##### ⚡ Liệu pháp Can thiệp tái tưới máu nâng cao (AHA/ACC 2026):")
            
            # Đồng bộ phác đồ Alteplase chuẩn (Bỏ lỗi tự ý chia liều unapproved)
            st.info("💊 **Phác đồ Tiêu sợi huyết Hệ thống chuẩn (Alteplase):**\n- **rt-PA liều chuẩn:** **100 mg truyền tĩnh mạch liên tục trong 2 giờ** (Phác đồ chuẩn duy nhất được FDA phê duyệt và khuyến cáo mạnh bởi AHA/ACC).\n- *Cân nhắc liều thấp (Lower-dose):* Có thể cân nhắc **50 mg rt-PA truyền trong 2 giờ** ở bệnh nhân có nguy cơ chảy máu cao hoặc nhẹ cân (<65kg) (Class 2b, LOE C-LD).\n- *Lưu ý về Tenecteplase (TNK-tPA):* Đã được nghiên cứu lâm sàng nhưng **CHƯA ĐƯỢC FDA PHÊ DUYỆT** cho chỉ định thuyên tắc phổi (off-label).")
            
            if st.session_state.final_category == "C3":
                st.warning("👉 **Khuyến cáo Nhóm C3 (Nguy cơ trung bình-cao):**\n- **Theo dõi sát tại ICU/Step-down** và duy trì kháng đông tiêu chuẩn.\n- **KHÔNG chỉ định tiêu sợi huyết hệ thống thường quy** ngay từ đầu (Class 3: Harm do tăng nguy cơ xuất huyết nặng).\n- **Tiêu sợi huyết giải cứu (Rescue Thrombolysis):** Chỉ chỉ định khi bệnh nhân có biểu hiện suy sụp huyết động rõ rệt trên lâm sàng (Class 2a).\n- **Can thiệp Catheter (CDL/MT):** Xem xét can thiệp qua Catheter (CDL) hoặc lấy huyết khối cơ học (MT) khi bệnh nhân có suy sụp huyết động mà có chống chỉ định tuyệt đối hoặc thất bại với tiêu sợi huyết hệ thống.")
                
            elif st.session_state.final_category in ["D1", "D2"]:
                st.warning("👉 **Khuyến cáo Nhóm D (Sắp sụp đổ / Sốc ẩn):**\n- Liệu pháp can thiệp có thể được cân nhắc để ngăn ngừa diễn tiến xấu hơn (Class 2b).\n- **Tiêu sợi huyết hệ thống:** Có thể cân nhắc (Class 2b) nếu nguy cơ chảy máu thấp.\n- **Can thiệp Catheter qua da (CDL / MT):** Là lựa chọn hợp lý (Class 2b), đặc biệt hữu ích khi bệnh nhân có nguy cơ chảy máu cao.\n- **Phẫu thuật lấy huyết khối (Surgical Embolectomy):** Có thể cân nhắc (Class 2b) bởi phẫu thuật viên giàu kinh nghiệm.")
                
            elif st.session_state.final_category == "E1":
                st.success("👉 **Khuyến cáo Nhóm E1 (Sốc tim thực sự - Nguy cơ rất cao):**\n- **Tiêu sợi huyết hệ thống hệ thống kết hợp kháng đông:** Được khuyến cáo mạnh mẽ nếu nguy cơ xuất huyết chấp nhận được (**Class 2a, LOE C-LD**).\n- **Lấy huyết khối cơ học (MT) hoặc Phẫu thuật lấy huyết khối (Surgical Embolectomy):** Được khuyến cáo (**Class 2a**) khi bệnh nhân có chống chỉ định tuyệt đối với tiêu sợi huyết hệ thống, hoặc tiêu sợi huyết hệ thống thất bại.\n- **Tiêu sợi huyết qua Catheter (CDL):** Có thể cân nhắc (**Class 2b**).")
                
            elif st.session_state.final_category == "E2":
                st.success("👉 **Khuyến cáo Nhóm E2 (Sốc kháng trị / Ngừng tuần hoàn):**\n- **Tiêu sợi huyết hệ thống:** Được chỉ định khẩn cấp kết hợp hồi sức tích cực (**Class 2a**).\n- **Phẫu thuật lấy huyết khối giải cứu hoặc MT:** Được khuyến cáo mạnh mẽ (**Class 2a**).\n- **Hỗ trợ tuần hoàn ngoài cơ thể VA-ECMO:** Khuyến cáo sử dụng **VA-ECMO (Veno-Arterial ECMO) (Class 2a)** ở bệnh nhân sốc tim kháng trị (SCAI Stage D/E) hoặc trong quá trình hồi sức tim phổi tích cực (E-CPR) để duy trì tưới máu cơ quan và nâng đỡ thất phải.")

        # Hiển thị Respiratory Modifier nếu có R
        if st.session_state.resp_modifier:
            st.error("📢 **CẢNH BÁO SUY HÔ HẤP (Respiratory Modifier R):**\nBệnh nhân có suy hô hấp nặng đi kèm. Hạn chế đặt nội khí quản máy thở áp lực dương lớn trừ khi bắt buộc để tránh làm sụp đổ tuần hoàn tim phải đang suy cấp. Ưu tiên tối đa hỗ trợ oxy dòng cao (HFNC) hoặc thở máy không xâm lấn.")

        # Nút chuyển tiếp ngược
        st.markdown("---")
        if st.button("⬅️ Quay lại Giai đoạn Phân loại (Bước 2)"):
            st.session_state.step = 2
            st.rerun()
