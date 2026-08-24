import streamlit as st

# =========================
# KHAI BÁO CÁC TRANG
# =========================

pe = st.Page(
    "pages/0_🫁_Thuyen_tac_phoi.py",
    title="Thuyên tắc phổi cấp",
    icon="🫁",
    default=True
)

ccs = st.Page(
    "pages/1_❤️_Hoi_chung_vanh_man.py",
    title="Hội chứng vành mạn",
    icon="❤️"
)

lipid = st.Page(
    "pages/2_🩸_Roi_loan_lipid_mau.py",
    title="Rối loạn lipid máu",
    icon="🩸"
)

# =========================
# ĐĂNG KÝ ĐIỀU HƯỚNG
# Ẩn menu tự động của Streamlit
# =========================

menu = st.navigation(
    [pe, ccs, lipid],
    position="hidden"
)

# =========================
# MENU TRUNG TÂM BÊN TRÁI
# =========================

with st.sidebar:
    st.page_link(
        pe,
        label="Thuyên tắc phổi cấp",
        icon="🫁"
    )

    st.page_link(
        ccs,
        label="Hội chứng vành mạn",
        icon="❤️"
    )

    st.page_link(
        lipid,
        label="Rối loạn lipid máu",
        icon="🩸"
    )

# =========================
# CHẠY TRANG ĐƯỢC CHỌN
# =========================

menu.run()
