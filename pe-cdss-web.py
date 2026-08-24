import streamlit as st

st.set_page_config(
    page_title="CDSS Tool",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# KHAI BÁO CÁC TOOL
# =========================================================

pe = st.Page(
    "pages/0_🫁_Thuyên_tắc_phổi.py",
    title="Thuyên tắc phổi cấp",
    icon="🫁",
    default=True
)

ccs = st.Page(
    "pages/1_❤️_Hội_chứng_vành_mạn.py",
    title="Hội chứng vành mạn",
    icon="❤️"
)

lipid = st.Page(
    "pages/2_🩸_Rối_loạn_lipid_máu.py",
    title="Rối loạn lipid máu",
    icon="🩸"
)

# =========================================================
# MENU TRUNG TÂM
# =========================================================

menu = st.navigation(
    [
        pe,
        ccs,
        lipid
    ],
    position="sidebar",
    expanded=True
)

# =========================================================
# CHẠY TOOL ĐƯỢC CHỌN
# =========================================================

menu.run()
