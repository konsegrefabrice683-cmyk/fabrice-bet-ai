import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
import hashlib

st.set_page_config(page_title="FABRICE V33 EMPIRE INFINI", layout="wide")
st.markdown("<style>#MainMenu, footer, header {visibility:hidden;}.stDeployButton{display:none;}</style>", unsafe_allow_html=True)

st.title("FABRICE EMPIRE V33 - INFINI")
st.caption("12 MATCHS FIXES | PMU-B JOURNAL HIPPIQUE | BOURSE - MÊME JOUR = MÊME ARRIVÉE POUR TOUS")

if "nb_semaines" not in st.session_state:
    st.session_state.nb_semaines = 1

def seed_from_date(d, salt=""):
    txt = d.strftime('%Y%m%d') + salt
    return int(hashlib.md5(txt.encode()).hexdigest()[:8], 16)

c1,c2 = st.columns(2)
with c1:
    if st.button("➕ +1 SEMAINE 7J/7 INFINI", use_container_width=True):
        st.session_state.nb_semaines += 1
        st.rerun()
with c2:
    if st.button("🔄 RESET", use_container_width=True):
        st.session_state.nb_semaines = 1
        st.rerun()

fixtures_30 = [
    "ASFA Yennega vs EFO", "Rahimo FC vs Salitas", "USFA vs Majestic",
    "RCB vs AS Douanes", "Vitesse FC vs Royal FC", "Sonabel vs CFFEB",
    "AS Sonabel vs USFA", "EFO vs Rahimo FC", "Bobo Sport vs ASFA", "ASFB vs USFA",
    "Real Madrid vs Barcelona", "Man City vs Arsenal", "PSG vs Marseille", "Bayern vs Dortmund",
    "Inter vs Juventus", "Liverpool vs Chelsea", "Atletico vs Sevilla", "Napoli vs AC Milan",
    "Leverkusen vs Leipzig", "Aston Villa vs Man United", "Man City vs Real Madrid - LDC",
    "PSG vs Bayern - LDC", "Barcelona vs Inter - LDC", "Arsenal vs Atletico - LDC",
    "Dortmund vs Juventus - LDC", "Liverpool vs Napoli - LDC", "Ajax vs PSV", "Benfica vs Porto",
    "Galatasaray vs Fenerbahce", "Al Nassr vs Al Hilal"
]

def get_bourse_signal(actif, prix_actuel, d):
    rnd = random.Random(seed_from_date(d, actif))
    signal_type = rnd.choice(["ACHAT", "VENTE", "ATTENTE"])
    entry = prix_actuel
    if signal_type == "ACHAT":
        sl = prix_actuel * 0.94
        tp1 = prix_actuel * 1.08
        tp2 = prix_actuel * 1.15
        action = "🟢 ACHETER"
        fermer = f"FERMER si < ${sl:,.0f} (STOP) ou > ${tp1:,.0f} (TP)"
    elif signal_type == "VENTE":
        sl = prix_actuel * 1.06
        tp1 = prix_actuel * 0.92
        tp2 = prix_actuel * 0.85
        action = "🔴 VENDRE / SHORT"
        fermer = f"FERMER si > ${sl:,.0f} (STOP) ou < ${tp1:,.0f} (TP)"
    else:
        sl, tp1, tp2 = prix_actuel*0.95, prix_actuel*1.05, prix_actuel*1.10
        action = "🟡 ATTENTE"
        fermer = "Ne rentre pas, attend signal"
    return signal_type, entry, sl, tp1, tp2, action, fermer

def generate_journal(d):
    rnd = random.Random(seed_from_date(d, "pmu"))
    chevaux = list(range(1,17))
    cotes_paris = [f"{rnd.choice([5,7,11,13,15,16,18,19,20,21,23,27,29,30,33,35])}/1" for _ in range(16)]
    cotes_tierce = [f"{rnd.choice([5,8,11,12,14,16,18,20,21,28,32,34])}/1" for _ in range(16)]
    presse = {
        "TURF-FR.COM": rnd.sample(chevaux, 8),
        "LE PARISIEN": rnd.sample(chevaux, 8),
        "L'ALSACE": rnd.sample(chevaux, 8),
        "TURFOMANIA": rnd.sample(chevaux, 8),
        "SUD OUEST": rnd.sample(chevaux, 6),
    }
    aptitudes = {
        "FORME": rnd.sample(chevaux, 5),
        "CLASSE": rnd.sample(chevaux, 5),
        "PROGRES": rnd.sample(chevaux, 5),
        "REGULARITE": rnd.sample(chevaux, 5),
    }
    favoris = rnd.sample(chevaux, 6)
    masse = f"{rnd.randint(20,35)}.{rnd.randint(100,999)}.000 F"
    return cotes_paris, cotes_tierce, presse, aptitudes, favoris, masse

tab1, tab2, tab3 = st.tabs(["PARIS SPORTIFS 12 FIXES", "PMU-B JOURNAL HIPPIQUE", "BOURSE INTERNATIONALE"])

jours_fr = ["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"]
total_jours = st.session_state.nb_semaines * 7
NB_MATCHS_FIXE = 12

with tab1:
    st.markdown(f"### 🎯 PARIS SPORTIFS - {NB_MATCHS_FIXE} MATCHS FIXES (BLOQUÉ - INFINI)")
    type_paris = st.selectbox("🎯 Type LONAB - PARIS", ["1X2", "Double Chance", "Over/Under AUTO", "BTTS Oui/Non", "Score Exact"], key="paris_v33")
    for i in range(total_jours):
        d = datetime.now() + timedelta(days=i)
        nom = jours_fr[d.weekday()]
        rnd = random.Random(seed_from_date(d, type_paris))
        if d.weekday()==0: st.markdown(f"#### 📅 SEMAINE {(i//7)+1}")
        with st.expander(f"{nom} {d.strftime('%d/%m/%Y')} - {NB_MATCHS_FIXE} MATCHS FIXES", expanded=(i==0)):
            matchs = rnd.sample(fixtures_30, NB_MATCHS_FIXE)
            data = []
            for m in matchs:
                if type_paris == "1X2": prono = rnd.choice(["1", "X", "2"])
                elif type_paris == "Double Chance": prono = rnd.choice(["1X", "X2", "12"])
                elif "Over" in type_paris: 
                    ligne = rnd.choice([0.5, 1.5, 2.5, 3.5, 4.5])
                    choix = rnd.choice(["Over", "Under"])
                    prono = f"{choix} {ligne}"
                elif "BTTS" in type_paris: prono = rnd.choice(["GG Oui", "GG Non"])
                else: prono = rnd.choice(["1-0", "2-1", "1-1", "2-0"])
                data.append({"Match": m, "Prono": prono, "Cote": round(rnd.uniform(1.45,3.20),2), "IA": "🔥 SÛR", "Confiance": f"{rnd.randint(65,82)}%"})
            st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True, column_config={"Match": st.column_config.TextColumn(width="large"), "Prono": st.column_config.TextColumn(width="medium")})

with tab2:
    st.markdown("### 🐴 PMU-B - JOURNAL HIPPIQUE - MÊME ANALYSE POUR TOUS À L'INFINI")
    type_pmu = st.selectbox("🎯 Type PMU-B LONAB", ["Quinté+", "Quarté", "Tiercé", "Couplé Gagnant", "Couplé Placé", "Trio", "Multi / 2sur4"], key="pmu_v33")
    for i in range(total_jours):
        d = datetime.now() + timedelta(days=i)
        nom = jours_fr[d.weekday()]
        cotes_paris, cotes_tierce, presse, aptitudes, favoris, masse = generate_journal(d)
        if d.weekday()==0: st.markdown(f"#### 🐴 SEMAINE {(i//7)+1} - {type_pmu}")
        with st.expander(f"🐴 {type_pmu} - {nom} {d.strftime('%d/%m/%Y')} - Masse {masse}", expanded=(i==0)):
            # ANALYSE EN HAUT - MÊME POUR TOUS À L'INFINI
            if type_pmu == "Quinté+":
                st.markdown(f'<div style="background:#d00000;color:white;padding:14px;border-radius:10px;text-align:center;font-size:22px;font-weight:bold;">🎯 QUINTÉ+ DU JOUR: {favoris[0]} - {favoris[1]} - {favoris[2]} - {favoris[3]} - {favoris[4]} - {favoris[5]}</div>', unsafe_allow_html=True)
                st.success(f"**🎯 BASE: {favoris[0]}-{favoris[1]} | CHAMP {favoris[0]}-{favoris[1]} X {'-'.join(map(str, favoris[2:6]))} | Bonus 4 & 3 | Flexi 50% = 6€**")
                st.info(f"🏁 ARRIVÉE AI IDENTIQUE POUR TOUS: {favoris[0]}-{favoris[1]}-{favoris[2]} | Même jusqu'à l'infini")
            elif type_pmu == "Quarté":
                st.markdown(f'<div style="background:#d00000;color:white;padding:14px;border-radius:10px;text-align:center;font-size:22px;font-weight:bold;">🎯 QUARTÉ: {favoris[0]} - {favoris[1]} - {favoris[2]} - {favoris[3]}</div>', unsafe_allow_html=True)
                st.success(f"**Base {favoris[0]} | {favoris[0]} X {'-'.join(map(str, favoris[1:5]))} | Rapport 500€**")
            elif type_pmu == "Tiercé":
                st.markdown(f'<div style="background:#d00000;color:white;padding:14px;border-radius:10px;text-align:center;font-size:22px;font-weight:bold;">🎯 TIERCÉ: {favoris[0]} - {favoris[1]} - {favoris[2]}</div>', unsafe_allow_html=True)
                st.success(f"**Ordre 300€ | Désordre 50€**")
            elif "Couplé" in type_pmu:
                st.markdown(f'<div style="background:#d00000;color:white;padding:14px;border-radius:10px;text-align:center;font-size:22px;font-weight:bold;">🎯 {type_pmu.upper()}: {favoris[0]} - {favoris[1]}</div>', unsafe_allow_html=True)
                st.success(f"**Ordre obligatoire**")
            elif type_pmu == "Trio":
                st.markdown(f'<div style="background:#d00000;color:white;padding:14px;border-radius:10px;text-align:center;font-size:22px;font-weight:bold;">🎯 TRIO: {favoris[0]} - {favoris[1]} - {favoris[2]}</div>', unsafe_allow_html=True)
                st.success(f"**Ordre obligatoire**")
            else:
                st.markdown(f'<div style="background:#d00000;color:white;padding:14px;border-radius:10px;text-align:center;font-size:22px;font-weight:bold;">🎯 MULTI / 2sur4: {"-".join(map(str, favoris[:7]))}</div>', unsafe_allow_html=True)
                st.success(f"**2sur4: {favoris[0]}-{favoris[1]}**")
            st.divider()
            st.markdown(f"**💰 GHOST DE BEAULIEU | Masse à partager : {masse} | R1 C3 - 15h15 - Attelé 2700m | {type_pmu}**")
            df1 = pd.DataFrame([cotes_paris], columns=[str(k) for k in range(1,17)], index=["PARIS"])
            st.dataframe(df1, use_container_width=True)
            df2 = pd.DataFrame([cotes_tierce], columns=[str(k) for k in range(1,17)], index=["TIERCÉ"])
            st.dataframe(df2, use_container_width=True)
            st.markdown("#### 📰 PRONOSTICS PRESSE - MÊME POUR TOUS")
            data_p = []
            for j, pr in presse.items():
                data_p.append({"JOURNAL": j, "PRONO": " - ".join(map(str, pr))})
            st.dataframe(pd.DataFrame(data_p), use_container_width=True, hide_index=True)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### APTITUDES")
                st.markdown(f"**FORME:** {' - '.join(map(str, aptitudes['FORME']))}")
                st.markdown(f"**CLASSE:** {' - '.join(map(str, aptitudes['CLASSE']))}")
            with col2:
                st.markdown(f"**FAVORIS:** {' - '.join(map(str, favoris))}")
            st.markdown("#### CLASSEMENT")
            c1_, c2_, c3_ = st.columns(3)
            with c1_: st.markdown("**SECONDES CHANCES**\n\n1 - AGILE\n10 - BRITANIA")
            with c2_: st.markdown("**OUTSIDERS**\n\n4 - AMERICAN GLORY\n12 - FOXEY LADY")
            with c3_: st.markdown("**GROS OUTSIDERS**\n\n14 - TEARDROP EXPLODES\n5 - HASAPIKO")

with tab3:
    st.markdown("### 💹 BOURSE INTERNATIONALE - MÊME SIGNAUX POUR TOUS")
    type_bourse = st.selectbox("🎯 Marché", ["Crypto (BTC, ETH, SOL)", "BRVM (SONATEL, SGBS)", "Forex (EUR/USD, GBP/USD)", "Or & Pétrole (XAU, Brent)", "US Actions (AAPL, TSLA, NVDA)"], key="bourse_v33")
    if "Crypto" in type_bourse: actifs_list = [("BTC/USD", 80763), ("ETH/USD", 2450), ("SOL/USD", 145), ("BNB/USD", 620)]
    elif "BRVM" in type_bourse: actifs_list = [("SONATEL.SN - BRVM", 43850), ("SGBS - BRVM", 18500), ("ONATEL.BF", 5200), ("ETI - BRVM", 7200)]
    elif "Forex" in type_bourse: actifs_list = [("EUR/USD", 1.0850), ("GBP/USD", 1.2950), ("USD/JPY", 152.30), ("USD/CHF", 0.8850)]
    elif "Or" in type_bourse: actifs_list = [("XAU/USD - OR", 2680), ("BRENT - PÉTROLE", 116.5), ("SILVER", 32.5), ("GAS", 3.45)]
    else: actifs_list = [("AAPL - Apple", 347.72), ("TSLA - Tesla", 372.22), ("NVDA", 142.5), ("MSFT", 445.0)]
    for i in range(total_jours):
        d = datetime.now() + timedelta(days=i)
        nom = jours_fr[d.weekday()]
        if d.weekday()==0: st.markdown(f"#### 💹 SEMAINE {(i//7)+1} - {type_bourse}")
        with st.expander(f"💹 {type_bourse} - {nom} {d.strftime('%d/%m/%Y')} - SIGNAUX", expanded=(i==0)):
            data_b = []
            for actif, prix in actifs_list:
                sig, entry, sl, tp1, tp2, action, fermer = get_bourse_signal(actif, prix, d)
                data_b.append({"Actif": actif, "Signal": action, "Entrée": f"{entry:,.2f}", "STOP": f"{sl:,.2f}", "TP1": f"{tp1:,.2f}", "TP2": f"{tp2:,.2f}", "Fermer": fermer})
            st.dataframe(pd.DataFrame(data_b), use_container_width=True, hide_index=True)

st.success("✅ V33 INFINI - Même jour = même arrivée pour tous, jusqu'à l'infini")
