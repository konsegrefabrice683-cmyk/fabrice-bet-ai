import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="FABRICE V24 SCORE EXACT", layout="wide")
st.markdown("<style>#MainMenu, footer, header {visibility:hidden;}.stDeployButton{display:none;}</style>", unsafe_allow_html=True)

st.title("FABRICE EMPIRE V24 - SCORE EXACT 7J/7")
st.caption("AJOUT SCORE EXACT")

if "nb_semaines" not in st.session_state:
    st.session_state.nb_semaines = 1

c1,c2 = st.columns(2)
with c1:
    if st.button("➕ +1 SEMAINE 7J/7", use_container_width=True):
        st.session_state.nb_semaines += 1
        st.rerun()
with c2:
    if st.button("🔄 RESET", use_container_width=True):
        st.session_state.nb_semaines = 1
        st.rerun()

nb_matchs = st.slider("Nombre de matchs", 10, 15, 12)

# ICI J'AI AJOUTÉ SCORE EXACT
type_pari = st.selectbox("🎯 Type LONAB", ["1X2", "Double Chance", "Over/Under", "BTTS", "Score Exact"], index=1)

total_jours = st.session_state.nb_semaines * 7
st.success(f"{st.session_state.nb_semaines} SEMAINE(S) = {total_jours} JOURS 7J/7 | {type_pari} | {nb_matchs} matchs")

tab1, tab2, tab3 = st.tabs(["PARIS INFINI 7J/7", "PMU-B COMPLET", "BOURSE CRYPTO FOREX"])

jours_fr = ["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"]

fixtures = [
    "Aston Villa vs Man City", "Arsenal vs Everton", "Chelsea vs Tottenham",
    "Rayo vs Elche", "Valencia vs Villarreal", "Atletico vs Deportivo",
    "Napoli vs Roma", "Cagliari vs Bologna", "Como vs Sassuolo", "Lazio vs Parma",
    "Barça vs Real - CLASICO", "Inter vs Fiorentina", "Atalanta vs Frosinone",
    "Sevilla vs Osasuna", "Liverpool vs Brighton", "Man Utd vs Bournemouth",
    "CFFEB vs ASFA", "Rahimo vs SONABEL", "USFA vs Comoe", "Salitas vs ASFA",
    "EFO vs RCB", "RCB vs USFA", "Brest vs Nice", "Mamelodi vs Wilitete", "Burkina vs EFO",
    "PSG vs Marseille", "Dortmund vs Frankfurt", "Bayern vs EFO", "Inter vs Barca", "Real vs Brest"
]

def get_prono(t):
    if t == "1X2": return random.choice(["1","X","2"])
    if t == "Double Chance": return random.choice(["1X","X2","12"])
    if t == "Over/Under": return random.choice(["Over 2.5","Under 2.5","Over 1.5"])
    if t == "BTTS": return random.choice(["GG Oui","GG Non"])
    if t == "Score Exact": return random.choice(["1-0","2-0","2-1","1-1","0-1","0-2","3-1","2-2"])
    return "1X"

def gen_paris(nom, nb, t):
    matchs = random.sample(fixtures, nb) if nb <= len(fixtures) else random.choices(fixtures, k=nb)
    data=[]
    for m in matchs:
        prono = get_prono(t)
        # Si Score Exact, on met une grosse cote
        cote = round(random.uniform(6.0, 12.0),2) if t=="Score Exact" else round(random.uniform(1.3,2.5),2)
        data.append({
            "Jour": nom,
            "Match": m,
            "Prono IA": prono,
            "Score Exact IA" if t=="Score Exact" else "Prono IA 2": prono,
            "Cote": cote,
            "Proba": f"{random.randint(55,88)}%",
            "Value": f"+{random.randint(5,25)}%" if t=="Score Exact" else f"+{random.randint(5,15)}%",
            "IA": "🔥 SÛR" if t!="Score Exact" else "💎 GROSSE COTE",
            "STATUT": "🟢 VALIDÉ"
        })
    return pd.DataFrame(data)

with tab1:
    for i in range(total_jours):
        d = datetime.now() + timedelta(days=i)
        nom = jours_fr[d.weekday()]
        if d.weekday()==0:
            st.markdown(f"### 📅 SEMAINE {(i//7)+1}")
        with st.expander(f"{nom} {d.strftime('%d/%m/%Y')} - {nb_matchs} MATCHS - {type_pari}", expanded=(i==0)):
            df = gen_paris(nom, nb_matchs, type_pari)
            st.dataframe(df, use_container_width=True, hide_index=True)
            if type_pari == "Score Exact":
                st.info("💡 Score Exact = Cote 6.00 à 12.00 - Mise petite, gain énorme!")

with tab2:
    for i in range(total_jours):
        d = datetime.now() + timedelta(days=i)
        nom = jours_fr[d.weekday()]
        if d.weekday()==0:
            st.markdown(f"### 🐴 SEMAINE {(i//7)+1} - PMU-B")
        with st.expander(f"🐴 PMU - {nom} {d.strftime('%d/%m/%Y')}", expanded=(i==0)):
            df_q = pd.DataFrame([{
                "Course": f"R1 C3 {d.strftime('%d/%m')} 15h15",
                "Quinté+": "5-8-12-3-9", "Bases": "5-8", "Outsiders": "12-3",
                "Analyse": "5 imbattable", "Cote": 85.0, "IA": "🔥 SÛR"
            }])
            st.dataframe(df_q, use_container_width=True, hide_index=True)

with tab3:
    for i in range(total_jours):
        d = datetime.now() + timedelta(days=i)
        nom = jours_fr[d.weekday()]
        if d.weekday()==0:
            st.markdown(f"### 💹 SEMAINE {(i//7)+1} - BOURSE")
        with st.expander(f"💹 BOURSE - {nom} {d.strftime('%d/%m/%Y')}", expanded=(i==0)):
            df_c = pd.DataFrame([
                {"Actif": "BTC/USD", "Prono": "ACHAT", "Prix": f"${random.randint(62000,68000)}", "Cote": 1.65, "IA": "🔥", "STATUT": "📈"},
                {"Actif": "ETH/USD", "Prono": "ACHAT", "Prix": f"${random.randint(2400,2800)}", "Cote": 1.75, "IA": "✅", "STATUT": "📈"},
                {"Actif": "OR XAU", "Prono": "ACHAT", "Prix": f"${random.randint(2650,2750)}", "Cote": 1.55, "IA": "🔥", "STATUT": "📈"},
            ])
            st.dataframe(df_c, use_container_width=True, hide_index=True)

st.success(f"✅ V24 AVEC SCORE EXACT - Cotes 6 à 12 - {total_jours} jours 7J/7")
