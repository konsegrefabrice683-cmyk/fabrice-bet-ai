import streamlit as st
import os
from datetime import datetime

st.set_page_config(page_title="FABRICE BET AI", page_icon="⚽", layout="wide")

st.markdown("<style>#MainMenu, footer, header {visibility: hidden;} .stDeployButton{display:none;}</style>", unsafe_allow_html=True)

for name in ["IMG-20261024-WA5224.jpg", "logo.png", "logo.jpg"]:
    if os.path.exists(name):
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.image(name, width=250)
        break

st.markdown("<h1 style='text-align:center; color:#FFD700;'>⚽ FABRICE BET AI</h1>", unsafe_allow_html=True)
st.caption("DOUBLE CHANCE = 10-15 MATCHS / VICTOIRE DIRECTE")

if "nb_jours" not in st.session_state:
    st.session_state.nb_jours = 1

c1, c2 = st.columns(2)
with c1:
    if st.button("+3 JOURS"):
        st.session_state.nb_jours += 3
        st.rerun()
with c2:
    if st.button("-3 JOURS"):
        st.session_state.nb_jours = max(1, st.session_state.nb_jours - 3)
        st.rerun()

st.divider()
st.success("🔥 TON APP EST MAINTENANT SANS LOGO STREAMLIT !")
st.info("LONAB - IA Burkina")
