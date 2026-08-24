import streamlit as st

# =========================
# MENU TRUNG TÂM
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

menu = st.navigation([
    pe,
    ccs,
    lipid
])

menu.run()
