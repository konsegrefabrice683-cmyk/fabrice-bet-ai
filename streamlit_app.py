import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="FABRICE BET AI", page_icon="⚽", layout="wide")
st.markdown("<style>#MainMenu, footer, header {visibility:hidden;} .stDeployButton{display:none;}</style>", unsafe_allow_html=True)

# LOGO
for f in ["logo.png", "IMG-20261024-WA5224.jpg"]:
    if os.path.exists(f):
        st.image(f, width=220)
        break

st.markdown("<h1 style='text-align:center; color:#FFD700;'>FABRICE BET AI</h1>", unsafe_allow_html=True)
st.caption("LONAB - PMUB - BOURSE INTERNATIONALE - 7J/7")

# JOURS INFINIS
if "nb_jours" not in st.session_state:
    st.session_state.nb_jours = 1

col1, col2 = st.columns(2)
with col1:
    if st.button("➕ +3 JOURS", use_container_width=True):
        st.session_state.nb_jours += 3
        st.rerun()
with col2:
    if st.button("🔄 RESET", use_container_width=True):
        st.session_state.nb_jours = 1
        st.rerun()

# TYPES LONAB COMPLETS
type_lonab = st.selectbox("🎯 Type LONAB", ["Double Chance (10-15 matchs)", "PMUB (Chevaux)", "Bourse Internationale", "1X2 Direct", "Score Exact", "Under/Over"])

nb_matchs = st.slider("🔢 Nombre de matchs Double Chance", 10, 15, 12)

# GENERATION 7 JOURS
jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
start_date = datetime.now()

for i in range(st.session_state.nb_jours):
    date_jour = start_date + timedelta(days=i)
    nom_jour = jours[date_jour.weekday()]
    titre = f"{nom_jour} - {date_jour.strftime('%d/%m/%Y')} - {nb_matchs} MATCHS - {type_lonab}"

    with st.expander(f"📅 AUJOURD'HUI - {titre}" if i==0 else f"📅 {titre}", expanded=(i==0)):
        # Exemples matchs selon type
        if "PMUB" in type_lonab:
            data = {"Course": [f"Course {j+1} - R{random.randint(1,5)}" for j in range(6)], "Prono IA": [f"{random.randint(1,8)}-{random.randint(1,8)}" for _ in range(6)], "Cote": [round(random.uniform(2.5,15),2) for _ in range(6)]}
        elif "Bourse" in type_lonab:
            data = {"Match": ["Inter vs Arsenal", "Real vs Brest", "PSG vs EFO", "Man City vs Bayern"], "Prono IA": ["1X", "Victoire Real", "Over 2.5", "12"], "Cote LONAB": [1.45, 1.90, 1.75, 1.60]}
        else:
            matchs = ["Inter vs Arsenal", "Inter vs Barca", "PSG vs EFO", "Inter vs Man City", "EFO vs Bayern", "Real vs Brest", "Salitas vs ASFA", "RCB vs USFA", "Douanes vs Vitesse", "Majestic vs Sonabel", "Al Hilal vs Al Nassr", "Barca vs Real"]
            data = {"Match": matchs[:nb_matchs], "Prono IA": [random.choice(["1X", "X2", "12", "1", "X", "2"]) for _ in range(nb_matchs)], "Cote LONAB": [round(random.uniform(1.30,2.10),2) for _ in range(nb_matchs)]}
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)

st.success(f"✅ {st.session_state.nb_jours} jours générés - PMUB + Bourse Internationale ajoutés !")
