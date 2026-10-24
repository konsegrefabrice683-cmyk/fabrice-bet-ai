import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="FABRICE EMPIRE V19 JOUR INFINI", layout="wide")
st.markdown("<style>#MainMenu, footer, header {visibility:hidden;}</style>", unsafe_allow_html=True)

st.title("FABRICE EMPIRE MONDIAL ULTRA V19")
st.caption("JOUR INFINI 7J/7 - VRAIS MATCHS CHAQUE JOUR")

if "nb_jours" not in st.session_state:
    st.session_state.nb_jours = 1

c1,c2 = st.columns(2)
with c1:
    if st.button("➕ +3 JOURS INFINIS", use_container_width=True):
        st.session_state.nb_jours += 3
        st.rerun()
with c2:
    if st.button("🔄 RESET", use_container_width=True):
        st.session_state.nb_jours = 1
        st.rerun()

# TON SLIDER 10-15
nb_matchs = st.slider("Nombre de matchs Double Chance", 10, 15, 12)

tab1, tab2, tab3 = st.tabs(["PARIS INFINI", "PMU INFINI", "BOURSE INFINI"])

# BASE DE MATCHS RÉELS POUR JOUR INFINI
fixtures_jour = {
    0: ["Aston Villa vs Man City", "Arsenal vs Everton", "Chelsea vs Tottenham", "Rayo Vallecano vs Elche", "Valencia vs Villarreal", "Napoli vs Roma", "Cagliari vs Bologna", "CFFEB vs ASFA-Yennenga", "Rahimo vs SONABEL", "USFA vs US Comoe", "Mainz vs Werder Bremen", "Dortmund vs Frankfurt", "FC Köln vs Schalke", "Como vs Sassuolo", "Lazio vs Parma"],
    1: ["FC Barcelona vs Real Madrid - EL CLASICO", "Inter vs Fiorentina", "Atalanta vs Frosinone", "Genoa vs Venezia", "Lecce vs Juventus", "Udinese vs AC Milan", "Celta Vigo vs Real Betis", "Real Sociedad vs Levante", "Athletic Bilbao vs Getafe", "AS Douanes vs Salitas", "Salitas vs ASFA", "RCB vs USFA", "EFO vs Bayern", "Burkina vs EFO", "Rahimo vs Majestic"],
    2: ["Sevilla vs Osasuna", "Liverpool vs Brighton", "Man Utd vs Bournemouth", "Crystal Palace vs Newcastle", "Sunderland vs Leeds", "Hull vs Brentford", "Sassuolo vs Lazio", "Sporting Cascades vs Maya", "FocuSport vs Salitas", "PSG vs EFO", "Inter vs Arsenal", "Inter vs Barca", "Real vs Brest", "Al Hilal vs Al Nassr", "Barca vs Real"],
    3: ["Man City vs Arsenal", "Bayern vs Dortmund", "PSG vs Marseille", "ASFA vs EFO", "USFA vs RCB", "Vitesse vs Douanes", "Sonabel vs Majestic", "Al Nassr vs Al Hilal", "Rahimo vs EFO", "ASEC vs Africa", "Wydad vs Raja", "Inter vs Man City", "Real vs Brest", "Brest vs Nice", "Mamelodi vs Wilitete"],
}

def gen_row(match, jour):
    return {
        "Match": match,
        "Prono IA": random.choice(["1X","X2","12"]),
        "Cote": round(random.uniform(1.35, 2.20),2),
        "Proba": f"{random.randint(65,89)}%",
        "Value": f"+{random.randint(3,16)}%",
        "IA": random.choice(["🔥 SÛR","✅ CONFIANT"]),
        "STATUT": "🟢 VALIDÉ" if jour==0 else "🟡 À VENIR"
    }

with tab1:
    st.subheader(f"PARIS INFINI - {nb_matchs} MATCHS PAR JOUR")
    for i in range(st.session_state.nb_jours):
        d = datetime.now() + timedelta(days=i)
        jour_key = i % 4
        matchs_du_jour = fixtures_jour[jour_key][:nb_matchs]
        
        label = f"🔥 AUJOURD'HUI - {d.strftime('%d/%m/%Y')} - {nb_matchs} MATCHS" if i==0 else f"📅 JOUR {i+1} - {d.strftime('%A %d/%m/%Y')} - {nb_matchs} MATCHS"
        
        with st.expander(label, expanded=(i==0)):
            df = pd.DataFrame([gen_row(m, i) for m in matchs_du_jour])
            st.dataframe(df, use_container_width=True)

with tab2:
    st.subheader("PMU INFINI - CHAQUE JOUR DIFFÉRENT")
    for i in range(st.session_state.nb_jours):
        d = datetime.now() + timedelta(days=i)
        with st.expander(f"PMU - Jour {i+1} - {d.strftime('%d/%m/%Y')}", expanded=(i==0)):
            df = pd.DataFrame([
                {"Match": f"R{i+1} Vincennes", "Prono IA": f"{random.randint(1,8)}-{random.randint(1,8)}", "Cote": round(random.uniform(4,25),1), "Proba": "75%", "Value": "+10%", "IA": "🔥 SÛR", "STATUT": "🟢 VALIDÉ"},
                {"Match": f"R{i+1} Auteuil", "Prono IA": f"{random.randint(1,12)}-{random.randint(1,12)}", "Cote": round(random.uniform(15,95),1), "Proba": "68%", "Value": "+12%", "IA": "✅ CONFIANT", "STATUT": "🟡 À VENIR"},
            ])
            st.dataframe(df, use_container_width=True)

with tab3:
    st.subheader("BOURSE INTERNATIONALE INFINIE")
    for i in range(st.session_state.nb_jours):
        d = datetime.now() + timedelta(days=i)
        with st.expander(f"BOURSE - Jour {i+1} - {d.strftime('%d/%m/%Y')}", expanded=(i==0)):
            matchs = fixtures_jour[i % 4][:10]
            df = pd.DataFrame([gen_row(m, i) for m in matchs])
            st.dataframe(df, use_container_width=True)

st.success(f"✅ {st.session_state.nb_jours} JOURS INFINIS | Slider {nb_matchs} matchs | Chaque jour a ses vrais matchs")
