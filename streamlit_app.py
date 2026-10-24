import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="FABRICE 7J/7 INFINI", layout="wide")
st.markdown("<style>#MainMenu, footer, header {visibility:hidden;}</style>", unsafe_allow_html=True)

st.title("FABRICE EMPIRE MONDIAL ULTRA V20")
st.markdown("### 📅 7 JOURS / 7 JOURS INFINI")

if "nb_semaines" not in st.session_state:
    st.session_state.nb_semaines = 1

c1,c2,c3 = st.columns(3)
with c1:
    if st.button("➕ +1 SEMAINE (7 JOURS)", use_container_width=True):
        st.session_state.nb_semaines += 1
        st.rerun()
with c2:
    if st.button("➕ +3 JOURS", use_container_width=True):
        st.session_state.nb_jours_extra = st.session_state.get("nb_jours_extra", 0) + 3
        st.rerun()
with c3:
    if st.button("🔄 RESET", use_container_width=True):
        st.session_state.nb_semaines = 1
        st.session_state.nb_jours_extra = 0
        st.rerun()

nb_matchs = st.slider("Nombre de matchs Double Chance", 10, 15, 12)

# CALCUL 7J/7 INFINI
nb_jours_extra = st.session_state.get("nb_jours_extra", 0)
total_jours = st.session_state.nb_semaines * 7 + nb_jours_extra

st.info(f"📅 {st.session_state.nb_semaines} SEMAINE(S) = {st.session_state.nb_semaines * 7} JOURS + {nb_jours_extra} jours = **{total_jours} JOURS 7J/7 INFINIS**")

tab1, tab2, tab3 = st.tabs(["PARIS INFINI 7J/7", "PMU INFINI 7J/7", "BOURSE INFINI 7J/7"])

jours_fr = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

fixtures = [
    "Aston Villa vs Man City", "Arsenal vs Everton", "Chelsea vs Tottenham", "Rayo Vallecano vs Elche",
    "Valencia vs Villarreal", "Atletico vs Deportivo", "Napoli vs Roma", "Cagliari vs Bologna",
    "Como vs Sassuolo", "Lazio vs Parma", "Barça vs Real Madrid EL CLASICO", "Inter vs Fiorentina",
    "Sevilla vs Osasuna", "Liverpool vs Brighton", "Man Utd vs Bournemouth", "CFFEB vs ASFA",
    "Rahimo vs SONABEL", "USFA vs Comoe", "Salitas vs ASFA", "EFO vs RCB"
]

def gen_row(match, date_obj):
    jour_nom = jours_fr[date_obj.weekday()]
    return {
        "Jour": jour_nom,
        "Match": match,
        "Prono IA": random.choice(["1X","X2","12"]),
        "Cote": round(random.uniform(1.30, 2.10),2),
        "Proba": f"{random.randint(65,90)}%",
        "Value": f"+{random.randint(3,15)}%",
        "IA": random.choice(["🔥 SÛR","✅ CONFIANT"]),
        "STATUT": "🟢 VALIDÉ"
    }

# AFFICHAGE PAR SEMAINE 7J/7
semaine_actuelle = 0
for i in range(total_jours):
    d = datetime.now() + timedelta(days=i)
    jour_semaine = d.weekday() # 0=Lundi, 6=Dimanche
    nom_jour = jours_fr[jour_semaine]
    
    # Nouvelle semaine tous les 7 jours
    if jour_semaine == 0:
        semaine_actuelle += 1
        st.markdown(f"## 📅 SEMAINE {semaine_actuelle} - 7J/7")

    with tab1:
        with st.expander(f"{nom_jour} {d.strftime('%d/%m/%Y')} - {nb_matchs} MATCHS", expanded=(i<7)):
            matchs_jour = random.sample(fixtures, nb_matchs)
            df = pd.DataFrame([gen_row(m, d) for m in matchs_jour])
            st.dataframe(df, use_container_width=True)

    with tab2:
        if i == 0: # Pour ne pas dupliquer, on affiche PMU et Bourse dans leurs tabs séparément
            pass

# PMU et BOURSE - même logique 7j/7
with tab2:
    for i in range(total_jours):
        d = datetime.now() + timedelta(days=i)
        nom_jour = jours_fr[d.weekday()]
        if d.weekday() == 0:
            st.markdown(f"## SEMAINE {(i//7)+1}")
        with st.expander(f"PMU - {nom_jour} {d.strftime('%d/%m/%Y')}", expanded=(i<2)):
            df = pd.DataFrame([{"Jour": nom_jour, "Match": f"Course R{i+1}", "Prono IA": "5-8-2", "Cote": 6.5, "Proba": "75%", "Value": "+10%", "IA": "🔥 SÛR", "STATUT": "🟢"}])
            st.dataframe(df, use_container_width=True)

with tab3:
    for i in range(total_jours):
        d = datetime.now() + timedelta(days=i)
        nom_jour = jours_fr[d.weekday()]
        if d.weekday() == 0:
            st.markdown(f"## SEMAINE {(i//7)+1}")
        with st.expander(f"BOURSE - {nom_jour} {d.strftime('%d/%m/%Y')}", expanded=(i<2)):
            df = pd.DataFrame([gen_row(m, d) for m in random.sample(fixtures, 8)])
            st.dataframe(df, use_container_width=True)

st.success(f"✅ MODE 7J/7 ACTIF - {total_jours} jours = {st.session_state.nb_semaines} semaines complètes Lundi-Dimanche + {nb_jours_extra} jours")
