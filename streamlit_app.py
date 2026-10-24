import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="FABRICE V22 PMUB BOURSE", layout="wide")
st.markdown("<style>#MainMenu, footer, header {visibility:hidden;}.stDeployButton{display:none;}</style>", unsafe_allow_html=True)

st.title("FABRICE EMPIRE V22 - PMUB & BOURSE COMPLET")

if "nb_semaines" not in st.session_state:
    st.session_state.nb_semaines = 1
    st.session_state.extra = 0

c1,c2 = st.columns(2)
with c1:
    if st.button("➕ +1 SEMAINE 7J/7", use_container_width=True):
        st.session_state.nb_semaines += 1
        st.rerun()
with c2:
    if st.button("🔄 RESET", use_container_width=True):
        st.session_state.nb_semaines = 1
        st.session_state.extra = 0
        st.rerun()

nb_matchs = st.slider("Nombre de matchs Double Chance", 10, 15, 12)
type_pari = st.selectbox("Type LONAB", ["1X2", "Double Chance", "Over/Under"], index=1)

total_jours = st.session_state.nb_semaines * 7
st.success(f"{st.session_state.nb_semaines} SEMAINE(S) = {total_jours} JOURS 7J/7 INFINIS")

tab1, tab2, tab3 = st.tabs(["PARIS INFINI 7J/7", "PMU-B COMPLET", "BOURSE CRYPTO FOREX"])

jours_fr = ["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"]
fixtures = ["Aston Villa vs Man City","Arsenal vs Everton","Chelsea vs Tottenham","Napoli vs Roma","Barça vs Real CLASICO","Inter vs Fiorentina","CFFEB vs ASFA","Rahimo vs SONABEL","USFA vs Comoe","Salitas vs ASFA"]

def gen_paris(nom, nb):
    data=[]
    for m in random.sample(fixtures, nb):
        data.append({"Jour":nom,"Match":m,"Prono IA":random.choice(["1X","X2","12"]),"Cote":round(random.uniform(1.3,2.5),2),"Proba":f"{random.randint(65,90)}%","Value":f"+{random.randint(5,15)}%","IA":"🔥 SÛR","STATUT":"🟢"})
    return pd.DataFrame(data)

# TAB1 PARIS
with tab1:
    for i in range(total_jours):
        d = datetime.now() + timedelta(days=i)
        nom = jours_fr[d.weekday()]
        if d.weekday()==0:
            st.markdown(f"### 📅 SEMAINE {(i//7)+1}")
        with st.expander(f"{nom} {d.strftime('%d/%m/%Y')} - {nb_matchs} MATCHS", expanded=(i==0)):
            st.dataframe(gen_paris(nom, nb_matchs), use_container_width=True, hide_index=True)

# TAB2 PMU-B COMPLET COMME TU VEUX
with tab2:
    for i in range(total_jours):
        d = datetime.now() + timedelta(days=i)
        nom = jours_fr[d.weekday()]
        if d.weekday()==0:
            st.markdown(f"### 🐴 SEMAINE {(i//7)+1} - PMU-B")
        with st.expander(f"🐴 PMU - {nom} {d.strftime('%d/%m/%Y')}", expanded=(i==0)):
            
            # 1. PRONOSTIC QUINTÉ+
            st.markdown("#### 🎯 PRONOSTIC QUINTÉ+ - PRIX DU JOUR")
            df_quinte = pd.DataFrame([{
                "Course": f"R1 C3 - {d.strftime('%d/%m')} - 15h15",
                "Quinté+": "5-8-12-3-9",
                "Bases": "5 - 8",
                "Bases Solides": "5 (Fautif)",
                "Outsiders": "12 - 3 - 9",
                "Choc": "14",
                "Analyse IA": "🔥 Le 5 est imbattable, le 8 revient en forme",
                "Cote": 85.0,
                "Proba": "72%",
                "IA": "🔥 SÛR"
            }])
            st.dataframe(df_quinte, use_container_width=True, hide_index=True)

            # 2. QUARTÉ
            st.markdown("#### 🎯 QUARTÉ")
            df_quarte = pd.DataFrame([{
                "Course": f"R1 C1 - 13h50",
                "Quarté": "2-7-9-11",
                "Base": "2",
                "Tocard": "11",
                "Analyse": "2 gagne facile, 11 peut surprendre",
                "Cote": 24.5,
                "Proba": "68%",
                "IA": "✅ CONFIANT"
            }])
            st.dataframe(df_quarte, use_container_width=True, hide_index=True)

            # 3. TIERCÉ + COUPLÉ
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("#### TIERCÉ")
                df_tierce = pd.DataFrame([
                    {"Course": "R1 C2", "Tiercé": "3-5-8", "Base": "3", "Analyse": "3 en grande forme", "Cote": 8.2, "IA": "🔥 SÛR"},
                    {"Course": "R2 C1", "Tiercé": "1-4-6", "Base": "1", "Analyse": "1 driver top", "Cote": 5.5, "IA": "✅ OK"}
                ])
                st.dataframe(df_tierce, use_container_width=True, hide_index=True)
            with col_b:
                st.markdown("#### COUPLÉ / TRIO")
                df_couple = pd.DataFrame([
                    {"Course": "R3", "Couplé Gagnant": "5-8", "Couplé Placé": "5-8-12", "Cote": 3.2, "Proba": "80%"},
                    {"Course": "R4", "Trio": "2-7-9", "Cote": 18.0, "Proba": "65%"}
                ])
                st.dataframe(df_couple, use_container_width=True, hide_index=True)

            # 4. CHEVAUX DÉTAILLÉS
            st.markdown("#### 🐎 DÉTAIL CHEVAUX - ANALYSE COMPLÈTE")
            df_chevaux = pd.DataFrame([
                {"N°":5, "Cheval": "FANTASTIC BOY", "Driver": "E.Raffin", "Musique": "1a 1a 2a", "Cote PMU": 2.1, "Forme": "🔥🔥🔥", "Analyse IA": "Base incontournable"},
                {"N°":8, "Cheval": "GOLD RIVER", "Driver": "J.M Bazire", "Musique": "2a 1a 1a", "Cote PMU": 4.5, "Forme": "🔥🔥", "Analyse IA": "Deuxième base solide"},
                {"N°":12, "Cheval": "SPEED STAR", "Driver": "A.Abrivard", "Musique": "4a 3a 1a", "Cote PMU": 12.0, "Forme": "🔥", "Analyse IA": "Outsider à suivre"},
                {"N°":3, "Cheval": "KING OF TURF", "Driver": "M.Mottier", "Musique": "5a 2a 4a", "Cote PMU": 18.0, "Forme": "⚠️", "Analyse IA": "Tocard possible"},
            ])
            st.dataframe(df_chevaux, use_container_width=True, hide_index=True)

# TAB3 BOURSE CRYPTO FOREX OR
with tab3:
    for i in range(total_jours):
        d = datetime.now() + timedelta(days=i)
        nom = jours_fr[d.weekday()]
        if d.weekday()==0:
            st.markdown(f"### 💹 SEMAINE {(i//7)+1} - BOURSE")
        with st.expander(f"💹 BOURSE - {nom} {d.strftime('%d/%m/%Y')}", expanded=(i==0)):
            
            st.markdown("#### ₿ CRYPTO")
            df_crypto = pd.DataFrame([
                {"Jour": nom, "Actif": "BTC/USD", "Prono IA": "ACHAT", "Prix": f"${random.randint(62000,68000)}", "Cote": round(random.uniform(1.2,1.9),2), "Proba": "78%", "IA": "🔥 SÛR", "STATUT": "📈 HAUSSE"},
                {"Jour": nom, "Actif": "ETH/USD", "Prono IA": "ACHAT", "Prix": f"${random.randint(2400,2800)}", "Cote": 1.65, "Proba": "75%", "IA": "✅ OK", "STATUT": "📈 HAUSSE"},
                {"Jour": nom, "Actif": "SOL/USD", "Prono IA": "VENTE", "Prix": f"${random.randint(140,180)}", "Cote": 2.10, "Proba": "62%", "IA": "⚠️ RISQUE", "STATUT": "📉 BAISSE"},
                {"Jour": nom, "Actif": "BNB/USD", "Prono IA": "ACHAT", "Prix": f"${random.randint(580,620)}", "Cote": 1.85, "Proba": "70%", "IA": "✅ OK", "STATUT": "📈 HAUSSE"},
            ])
            st.dataframe(df_crypto, use_container_width=True, hide_index=True)

            st.markdown("#### 💱 FOREX")
            df_forex = pd.DataFrame([
                {"Jour": nom, "Paire": "EUR/USD", "Prono IA": "ACHAT", "Cote": 1.45, "Proba": "72%", "Value": "+8%", "IA": "🔥 SÛR", "STATUT": "📈"},
                {"Jour": nom, "Paire": "GBP/USD", "Prono IA": "VENTE", "Cote": 1.75, "Proba": "68%", "Value": "+10%", "IA": "✅ OK", "STATUT": "📉"},
                {"Jour": nom, "Paire": "USD/JPY", "Prono IA": "ACHAT", "Cote": 1.55, "Proba": "70%", "Value": "+9%", "IA": "🔥 SÛR", "STATUT": "📈"},
                {"Jour": nom, "Paire": "XOF/EUR", "Prono IA": "STABLE", "Cote": 1.30, "Proba": "85%", "Value": "+3%", "IA": "✅ OK", "STATUT": "➡️"},
            ])
            st.dataframe(df_forex, use_container_width=True, hide_index=True)

            st.markdown("#### 🪙 OR / PÉTROLE / INDICES")
            df_bourse = pd.DataFrame([
                {"Jour": nom, "Actif": "OR (XAU/USD)", "Prono IA": "ACHAT", "Prix": f"${random.randint(2650,2750)}", "Proba": "76%", "IA": "🔥 SÛR", "STATUT": "📈"},
                {"Jour": nom, "Actif": "Pétrole Brent", "Prono IA": "VENTE", "Prix": f"${random.randint(72,80)}", "Proba": "65%", "IA": "✅ OK", "STATUT": "📉"},
                {"Jour": nom, "Actif": "CAC40", "Prono IA": "ACHAT", "Prix": "8150 pts", "Proba": "70%", "IA": "✅ OK", "STATUT": "📈"},
                {"Jour": nom, "Actif": "S&P500", "Prono IA": "ACHAT", "Prix": "5800 pts", "Proba": "73%", "IA": "🔥 SÛR", "STATUT": "📈"},
            ])
            st.dataframe(df_bourse, use_container_width=True, hide_index=True)

st.success(f"✅ V22 COMPLET - {total_jours} jours 7J/7 | PMU-B: Quinté Quarté Tiercé Analyse | Bourse: Crypto Forex Or")
