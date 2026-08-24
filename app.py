import streamlit as st

pe_page = st.Page(
    "pe-cdss-web.py",
    title="Thuyên tắc phổi cấp",
    icon="🫁",
    default=True
)

ccs_page = st.Page(
    "pages/1_❤️_Hoi_chung_vanh_man.py",
    title="Hội chứng vành mạn",
    icon="❤️"
)

lipid_page = st.Page(
    "pages/2_🩸_Roi_loan_lipid_mau.py",
    title="Rối loạn lipid máu",
    icon="🩸"
)

menu = st.navigation([
    pe_page,
    ccs_page,
    lipid_page
])

menu.run()
