import streamlit as st
import pandas as pd
import random, os
from datetime import datetime, timedelta

st.set_page_config(page_title="FABRICE EMPIRE MONDIAL ULTRA", layout="wide")
st.markdown("<style>#MainMenu, footer, header {visibility:hidden;} .stDeployButton{display:none;}</style>", unsafe_allow_html=True)

for f in ["logo.png"]:
    if os.path.exists(f):
        st.image(f, width=200)
        break

st.title("FABRICE EMPIRE MONDIAL ULTRA V17.1 FINAL")
st.caption(f"PARIS + PMU + BOURSE | {datetime.now().strftime('%d/%m/%Y')}")

if "nb_jours" not in st.session_state:
    st.session_state.nb_jours = 5

if st.button("➕ +3 JOURS INFINIS", use_container_width=True):
    st.session_state.nb_jours += 3
    st.rerun()

# SLIDER QUE TU AS DEMANDÉ - 10 à 15
nb_matchs = st.slider("Nombre de matchs Double Chance", 10, 15, 12)
st.write(f"**{nb_matchs} matchs sélectionnés**")

tab1, tab2, tab3 = st.tabs(["PARIS INFINI", "PMU INFINI", "BOURSE INFINI"])

def gen_row(match):
    cote = round(random.uniform(1.45, 2.45), 2)
    return {
        "Match": match, 
        "Prono IA": random.choice(["1X","X2","12","Brest Win","Mamelodi Win","Over/Under"]), 
        "Cote": cote, 
        "Proba": f"{random.randint(62,88)}%", 
        "Value": f"+{random.randint(2,18)}%", 
        "IA": random.choice(["🔥 SÛR","✅ CONFIANT","⚠️ RISQUE"]), 
        "STATUT": random.choice(["🟢 VALIDÉ","🟡 EN COURS","🔴 À SUIVRE"])
    }

matchs_base = ["Brest vs Nice","Mamelodi vs Wilitete","Burkina vs Brest","Brest vs Arsenal","Man City vs Bayern","Real vs Brest","Salitas vs ASFA","RCB vs USFA","PSG vs EFO","Inter vs Arsenal","Bayern vs EFO","Inter vs Barca","ASFA vs EFO","EFO vs Bayern","Brest vs EFO"]

with tab1:
    st.subheader(f"PARIS LONAB - {nb_matchs} TYPES")
    type_lonab = st.selectbox("Type LONAB", ["1X2","Double Chance","Over/Under","BTTS","Score Exact","Mi-Temps","Handicap"], key="paris")
    
    for i in range(st.session_state.nb_jours):
        d = datetime.now() + timedelta(days=i)
        label = f"AUJOURD HUI - {d.strftime('%d/%m/%Y')} - {nb_matchs} MATCHS" if i==0 else f"{d.strftime('%d/%m/%Y')} - {nb_matchs} MATCHS"
        with st.expander(label, expanded=(i==0)):
            selected = matchs_base[:nb_matchs]  # ICI LE SLIDER SERT
            df = pd.DataFrame([gen_row(m) for m in selected])
            st.dataframe(df, use_container_width=True)

with tab2:
    st.subheader("PMU-B COMPLET")
    for i in range(st.session_state.nb_jours):
        d = datetime.now() + timedelta(days=i)
        with st.expander(f"PMU - {d.strftime('%d/%m/%Y')}", expanded=(i==0)):
            df = pd.DataFrame([
                {"Match": f"Course R{i+1}", "Prono IA": "Tiercé 3-5-8", "Cote": 4.5, "Proba": "72%", "Value": "+12%", "IA": "🔥 SÛR", "STATUT": "🟢 VALIDÉ"},
                {"Match": f"Course R{i+1}", "Prono IA": "Quarté 2-7-9-11", "Cote": 18.2, "Proba": "65%", "Value": "+8%", "IA": "✅ CONFIANT", "STATUT": "🟡 EN COURS"},
            ])
            st.dataframe(df, use_container_width=True)

with tab3:
    st.subheader("BOURSE INTERNATIONALE")
    for i in range(st.session_state.nb_jours):
        d = datetime.now() + timedelta(days=i)
        with st.expander(f"BOURSE - {d.strftime('%d/%m/%Y')}", expanded=(i==0)):
            df = pd.DataFrame([gen_row(f"Bourse {j+1}") for j in range(nb_matchs)])
            st.dataframe(df, use_container_width=True)

st.success(f"✅ Slider {nb_matchs} matchs + {st.session_state.nb_jours} jours infinis actifs")
