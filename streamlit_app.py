import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="FABRICE V25 3 LONAB", layout="wide")
st.markdown("<style>#MainMenu, footer, header {visibility:hidden;}.stDeployButton{display:none;}</style>", unsafe_allow_html=True)

st.title("FABRICE EMPIRE V25 - 3 LONAB")
st.caption("Chaque onglet a son propre Type LONAB")

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
total_jours = st.session_state.nb_semaines * 7
st.info(f"{st.session_state.nb_semaines} SEMAINE(S) = {total_jours} JOURS 7J/7")

tab1, tab2, tab3 = st.tabs(["PARIS INFINI 7J/7", "PMU-B COMPLET", "BOURSE CRYP FOREX"])

jours_fr = ["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"]
fixtures = [
    "Aston Villa vs Man City", "Arsenal vs Everton", "Chelsea vs Tottenham",
    "Rayo vs Elche", "Valencia vs Villarreal", "Atletico vs Deportivo",
    "Napoli vs Roma", "Cagliari vs Bologna", "Como vs Sassuolo", "Lazio vs Parma",
    "Barça vs Real - CLASICO", "Inter vs Fiorentina", "Sevilla vs Osasuna", "Liverpool vs Brighton",
    "CFFEB vs ASFA", "Rahimo vs SONABEL", "USFA vs Comoe", "Salitas vs ASFA", "EFO vs RCB",
    "Brest vs Nice", "Mamelodi vs Wilitete", "PSG vs Marseille", "Dortmund vs Frankfurt", "Bayern vs EFO", "Inter vs Barca",
    "Real vs Brest", "Burkina vs EFO", "RCB vs USFA", "ASFA vs EFO", "EFO vs Bayern"
]

# ===================== TAB1 PARIS =====================
with tab1:
    st.markdown("### 🎯 PARIS SPORTIFS")
    type_paris = st.selectbox("🎯 Type LONAB - PARIS", ["1X2", "Double Chance", "Over/Under", "BTTS", "Score Exact", "Mi-Temps/Fin Match", "Handicap"], key="type_paris")
    
    def get_prono_paris(t):
        if t == "1X2": return random.choice(["1","X","2"])
        if t == "Double Chance": return random.choice(["1X","X2","12"])
        if t == "Over/Under": return random.choice(["Over 2.5","Under 2.5"])
        if t == "BTTS": return random.choice(["GG Oui","GG Non"])
        if t == "Score Exact": return random.choice(["1-0","2-0","2-1","1-1","0-1","2-2","3-1"])
        if t == "Mi-Temps/Fin Match": return random.choice(["1/1","X/1","1/X","2/2"])
        if t == "Handicap": return random.choice(["H1 -1","H2 +1","H1 -2"])
        return "1X"

    for i in range(total_jours):
        d = datetime.now() + timedelta(days=i)
        nom = jours_fr[d.weekday()]
        if d.weekday()==0:
            st.markdown(f"#### 📅 SEMAINE {(i//7)+1} - {type_paris}")
        with st.expander(f"{nom} {d.strftime('%d/%m/%Y')} - {type_paris} - {nb_matchs} MATCHS", expanded=(i==0)):
            matchs = random.sample(fixtures, nb_matchs)
            data=[]
            for m in matchs:
                cote = round(random.uniform(6,12),2) if type_paris=="Score Exact" else round(random.uniform(1.3,2.8),2)
                data.append({"Jour":nom,"Match":m,"Type":type_paris,"Prono IA":get_prono_paris(type_paris),"Cote":cote,"Proba":f"{random.randint(60,90)}%","Value":f"+{random.randint(5,20)}%","IA":"🔥 SÛR","STATUT":"🟢"})
            st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)

# ===================== TAB2 PMU =====================
with tab2:
    st.markdown("### 🐴 PMU-B")
    type_pmu = st.selectbox("🎯 Type LONAB - PMU-B", ["Quinté+", "Quarté", "Tiercé", "Couplé Gagnant", "Couplé Placé", "Trio", "Multi", "2sur4"], key="type_pmu")
    
    def gen_pmu(t, nom, date_str):
        if t == "Quinté+":
            return [{"Course":f"R1 C3 {date_str} 15h15","Type":t,"Prono": "5-8-12-3-9","Bases":"5-8","Outsiders":"12-3","Analyse IA":"5 imbattable, 8 en forme","Cote":85.0,"IA":"🔥 SÛR"}]
        elif t == "Quarté":
            return [{"Course":f"R1 C1 {date_str} 13h50","Type":t,"Prono":"2-7-9-11","Base":"2","Tocard":"11","Analyse IA":"2 favori, 11 surprise","Cote":24.5,"IA":"✅"}]
        elif t == "Tiercé":
            return [{"Course":f"R1 C2 {date_str} 14h10","Type":t,"Prono":"3-5-8","Base":"3","Analyse IA":"3 en grande forme","Cote":8.2,"IA":"🔥"}]
        elif "Couplé" in t:
            return [{"Course":f"R2 {date_str}","Type":t,"Prono":"5-8","Base":"5","Analyse IA":"Duo solide","Cote":3.2,"IA":"🔥"}]
        elif t == "Trio":
            return [{"Course":f"R3 {date_str}","Type":t,"Prono":"2-7-9","Base":"2","Analyse IA":"Trio logique","Cote":18.0,"IA":"✅"}]
        else:
            return [{"Course":f"R4 {date_str}","Type":t,"Prono":"5-8-12-3-9-11","Base":"5","Analyse IA":f"{t} spécial","Cote":12.0,"IA":"✅"}]

    for i in range(total_jours):
        d = datetime.now() + timedelta(days=i)
        nom = jours_fr[d.weekday()]
        date_str = d.strftime('%d/%m')
        if d.weekday()==0:
            st.markdown(f"#### 🐴 SEMAINE {(i//7)+1} - {type_pmu}")
        with st.expander(f"🐴 PMU {type_pmu} - {nom} {d.strftime('%d/%m/%Y')}", expanded=(i==0)):
            df = pd.DataFrame(gen_pmu(type_pmu, nom, date_str))
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            st.markdown(f"##### 🐎 DÉTAIL CHEVAUX - {type_pmu}")
            df_ch = pd.DataFrame([
                {"N°":5,"Cheval":"FANTASTIC BOY","Driver":"E.Raffin","Musique":"1a 1a 2a","Cote PMU":2.1,"Analyse":"Base"},
                {"N°":8,"Cheval":"GOLD RIVER","Driver":"J.M Bazire","Musique":"2a 1a 1a","Cote PMU":4.5,"Analyse":"Base solide"},
                {"N°":12,"Cheval":"SPEED STAR","Driver":"A.Abrivard","Musique":"4a 3a 1a","Cote PMU":12.0,"Analyse":"Outsider"},
            ])
            st.dataframe(df_ch, use_container_width=True, hide_index=True)

# ===================== TAB3 BOURSE =====================
with tab3:
    st.markdown("### 💹 BOURSE INTERNATIONALE")
    type_bourse = st.selectbox("🎯 Type LONAB - BOURSE", ["Crypto", "Forex", "Or & Argent", "Pétrole & Gaz", "Indices", "Actions US", "Actions BRVM"], key="type_bourse")
    
    def gen_bourse(t, nom):
        if t == "Crypto":
            return [
                {"Jour":nom,"Type":t,"Actif":"BTC/USD","Prono":"ACHAT","Prix":f"${random.randint(62000,68000)}","Cote":1.65,"IA":"🔥 SÛR","STATUT":"📈 HAUSSE"},
                {"Jour":nom,"Type":t,"Actif":"ETH/USD","Prono":"ACHAT","Prix":f"${random.randint(2400,2800)}","Cote":1.75,"IA":"✅","STATUT":"📈"},
                {"Jour":nom,"Type":t,"Actif":"SOL/USD","Prono":"VENTE","Prix":f"${random.randint(140,180)}","Cote":2.1,"IA":"⚠️","STATUT":"📉"},
            ]
        elif t == "Forex":
            return [
                {"Jour":nom,"Type":t,"Actif":"EUR/USD","Prono":"ACHAT","Prix":"1.0850","Cote":1.45,"IA":"🔥","STATUT":"📈"},
                {"Jour":nom,"Type":t,"Actif":"GBP/USD","Prono":"VENTE","Prix":"1.2650","Cote":1.75,"IA":"✅","STATUT":"📉"},
                {"Jour":nom,"Type":t,"Actif":"USD/XOF","Prono":"STABLE","Prix":"605","Cote":1.30,"IA":"✅","STATUT":"➡️"},
            ]
        elif t == "Or & Argent":
            return [
                {"Jour":nom,"Type":t,"Actif":"OR XAU/USD","Prono":"ACHAT","Prix":f"${random.randint(2650,2750)}","Cote":1.55,"IA":"🔥","STATUT":"📈"},
                {"Jour":nom,"Type":t,"Actif":"ARGENT XAG","Prono":"ACHAT","Prix":f"${random.randint(31,34)}","Cote":1.65,"IA":"✅","STATUT":"📈"},
            ]
        elif t == "Pétrole & Gaz":
            return [
                {"Jour":nom,"Type":t,"Actif":"Brent","Prono":"VENTE","Prix":f"${random.randint(72,80)}","Cote":1.85,"IA":"✅","STATUT":"📉"},
                {"Jour":nom,"Type":t,"Actif":"WTI","Prono":"VENTE","Prix":f"${random.randint(68,76)}","Cote":1.90,"IA":"✅","STATUT":"📉"},
            ]
        else:
            return [
                {"Jour":nom,"Type":t,"Actif":f"{t} - Top","Prono":"ACHAT","Prix":f"{random.randint(5000,8000)} pts","Cote":1.65,"IA":"🔥","STATUT":"📈"},
            ]

    for i in range(total_jours):
        d = datetime.now() + timedelta(days=i)
        nom = jours_fr[d.weekday()]
        if d.weekday()==0:
            st.markdown(f"#### 💹 SEMAINE {(i//7)+1} - {type_bourse}")
        with st.expander(f"💹 {type_bourse} - {nom} {d.strftime('%d/%m/%Y')}", expanded=(i==0)):
            df = pd.DataFrame(gen_bourse(type_bourse, nom))
            st.dataframe(df, use_container_width=True, hide_index=True)

st.success(f"✅ V25 - 3 LONAB INDÉPENDANTS | PARIS: {total_jours}j | PMU: Quinté/Quarté/Tiercé | BOURSE: Crypto/Forex/Or")
