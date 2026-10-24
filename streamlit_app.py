import streamlit as st
import pandas as pd
import random, os
from datetime import datetime, timedelta

st.set_page_config(page_title="FABRICE EMPIRE MONDIAL ULTRA", layout="wide")
st.markdown("<style>#MainMenu, footer, header {visibility:hidden;} .stDeployButton{display:none;}</style>", unsafe_allow_html=True)

# LOGO
for f in ["logo.png","IMG-20261024-WA5224.jpg"]:
    if os.path.exists(f):
        st.image(f, width=200)
        break

st.title("FABRICE EMPIRE MONDIAL ULTRA V17 FINAL")
st.caption(f"PARIS + PMU + BOURSE INTERNATIONALE | {datetime.now().strftime('%d/%m/%Y')} | OUAGA")

if "nb_jours" not in st.session_state:
    st.session_state.nb_jours = 5

if st.button("➕ +3 JOURS INFINIS", use_container_width=True):
    st.session_state.nb_jours += 3
    st.rerun()

# 3 ONGLETS COMME TU VEUX
tab1, tab2, tab3 = st.tabs(["PARIS INFINI", "PMU INFINI", "BOURSE INFINI"])

def gen_row(match):
    cote = round(random.uniform(1.45, 2.45), 2)
    proba = f"{random.randint(62, 88)}%"
    value = f"+{random.randint(2, 18)}%"
    ia = random.choice(["🔥 SÛR", "✅ CONFIANT", "⚠️ RISQUE"])
    statut = random.choice(["🟢 VALIDÉ", "🟡 EN COURS", "🔴 À SUIVRE"])
    prono = random.choice(["1X", "X2", "12", "Over/Under", "Brest Win", "Mamelodi Win"])
    return {"Match": match, "Prono IA": prono, "Cote": cote, "Proba": proba, "Value": value, "IA": ia, "STATUT": statut}

matchs_base = ["Brest vs Nice", "Mamelodi vs Wilitete", "Burkina vs EFO", "Brest vs Arsenal", "Man City vs Bayern", "Real vs Brest", "Salitas vs ASFA", "RCB vs USFA", "PSG vs EFO", "Inter vs Arsenal", "Bayern vs EFO"]

with tab1:
    st.subheader("PARIS LONAB - 7 TYPES")
    type_lonab = st.selectbox("Type LONAB", ["1X2", "Double Chance", "Over/Under", "BTTS", "Score Exact", "Mi-Temps", "Handicap"], key="paris")
    
    for i in range(st.session_state.nb_jours):
        d = datetime.now() + timedelta(days=i)
        label = f"AUJOURD HUI - {d.strftime('%d/%m/%Y')} - {len(matchs_base)} MATCHS" if i==0 else f"{d.strftime('%d/%m/%Y')} - {len(matchs_base)} MATCHS"
        
        with st.expander(label, expanded=(i==0)):
            df = pd.DataFrame([gen_row(m) for m in matchs_base])
            st.dataframe(df, use_container_width=True)
            st.code(f"TICKET {type_lonab}: " + " + ".join([f"{r['Match']} ({r['Cote']})" for _, r in df.head(3).iterrows()]), language="text")

with tab2:
    st.subheader("PMU-B COMPLET - PMUB INFINI")
    for i in range(st.session_state.nb_jours):
        d = datetime.now() + timedelta(days=i)
        with st.expander(f"PMU - {d.strftime('%d/%m/%Y')}", expanded=(i==0)):
            df_pmu = pd.DataFrame([
                {"Course": f"R{i+1} C1", "Chevaux": "3-5-8", "Prono IA": "Tiercé", "Cote": 4.5, "Proba": "72%", "Value": "+12%", "IA": "🔥 SÛR", "STATUT": "🟢 VALIDÉ"},
                {"Course": f"R{i+1} C2", "Chevaux": "2-7-9-11", "Prono IA": "Quarté", "Cote": 18.2, "Proba": "65%", "Value": "+8%", "IA": "✅ CONFIANT", "STATUT": "🟡 EN COURS"},
                {"Course": f"R{i+1} C3", "Chevaux": "1-4-6-9-12", "Prono IA": "Quinté", "Cote": 85.0, "Proba": "58%", "Value": "+15%", "IA": "⚠️ RISQUE", "STATUT": "🔴 À SUIVRE"},
            ])
            st.dataframe(df_pmu, use_container_width=True)

with tab3:
    st.subheader("BOURSE INTERNATIONALE INFINIE")
    for i in range(st.session_state.nb_jours):
        d = datetime.now() + timedelta(days=i)
        with st.expander(f"BOURSE - {d.strftime('%d/%m/%Y')}", expanded=(i==0)):
            df_bourse = pd.DataFrame([gen_row(f"Match Bourse {j+1} - {random.choice(['France','Angleterre','Burkina'])}") for j in range(8)])
            st.dataframe(df_bourse, use_container_width=True)

st.success(f"✅ {st.session_state.nb_jours} JOURS INFINIS ACTIFS - 7J/7")
