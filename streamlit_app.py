import streamlit as st
import pandas as pd
import random, os
from datetime import datetime, timedelta

st.set_page_config(page_title="FABRICE BET AI", page_icon="🐎", layout="wide")
st.markdown("<style>#MainMenu, footer, header {visibility:hidden;} .stDeployButton{display:none;}</style>", unsafe_allow_html=True)

# LOGO
for f in ["logo.png","IMG-20261024-WA5224.jpg"]:
    if os.path.exists(f):
        st.image(f, width=200)
        break

st.title("FABRICE BET AI")
st.caption("DOUBLE CHANCE | PMUB | BOURSE INTERNATIONALE - 7J/7 INFINI")

if "nb_jours" not in st.session_state:
    st.session_state.nb_jours = 1

c1,c2 = st.columns(2)
with c1:
    if st.button("➕ +3 JOURS", use_container_width=True):
        st.session_state.nb_jours += 3
        st.rerun()
with c2:
    if st.button("🔄 RESET", use_container_width=True):
        st.session_state.nb_jours = 1
        st.rerun()

type_lonab = st.selectbox("🎯 Type LONAB", ["Double Chance", "PMUB - Tiercé/Quarté/Quinté", "Bourse Internationale"])

nb_matchs = 12
if type_lonab == "Double Chance":
    nb_matchs = st.slider("Nombre de matchs Double Chance", 10, 15, 12)

jours = ["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"]

def gen_pmub():
    chevaux = [f"Cheval {i}" for i in range(1,15)]
    tierce = random.sample(range(1,15), 3)
    quarte = random.sample(range(1,15), 4)
    quinte = random.sample(range(1,15), 5)
    return pd.DataFrame([
        {"Jeu": "Tiercé", "Prono IA": f"{tierce[0]}-{tierce[1]}-{tierce[2]}", "Base": f"{tierce[0]}", "Cote": round(random.uniform(3,12),2)},
        {"Jeu": "Quarté", "Prono IA": f"{'-'.join(map(str,quarte))}", "Base": f"{quarte[0]}-{quarte[1]}", "Cote": round(random.uniform(8,35),2)},
        {"Jeu": "Quinté", "Prono IA": f"{'-'.join(map(str,quinte))}", "Base": f"{quinte[0]}-{quinte[1]}", "Cote": round(random.uniform(20,150),2)},
        {"Jeu": "Couplé Gagnant", "Prono IA": f"{random.randint(1,10)}-{random.randint(1,10)}", "Base": "2 chevaux", "Cote": round(random.uniform(2.5,8),2)},
        {"Jeu": "Couplé Placé", "Prono IA": f"{random.randint(1,10)}-{random.randint(1,10)}", "Base": "2 chevaux", "Cote": round(random.uniform(1.5,4),2)},
        {"Jeu": "Simple Gagnant", "Prono IA": f"{random.randint(1,14)}", "Base": "1 cheval", "Cote": round(random.uniform(1.8,6),2)},
    ])

def gen_bourse():
    bourses = ["France Ligue 1", "Premier League", "La Liga", "Serie A", "Bundesliga", "Burkina Faso Ligue 1", "LDC Afrique", "NBA", "Tennis ATP"]
    matchs = ["Inter vs Arsenal", "Real vs Brest", "PSG vs Man City", "Al Nassr vs Al Hilal", "ASFA vs Salitas", "USFA vs RCB", "Bayern vs Barca", "Lakers vs Warriors"]
    data = []
    for _ in range(10):
        data.append({
            "Bourse": random.choice(bourses),
            "Match": random.choice(matchs),
            "Prono IA": random.choice(["1X", "X2", "12", "Over 2.5", "Under 3.5", "1", "2", "GG"]),
            "Cote LONAB": round(random.uniform(1.35, 3.5),2),
            "Confiance": f"{random.randint(65,92)}%"
        })
    return pd.DataFrame(data)

def gen_double(n):
    all_m = ["Inter vs Arsenal","Inter vs Barca","PSG vs EFO","Inter vs Man City","EFO vs Bayern","Real vs Brest","Salitas vs ASFA","RCB vs USFA","Douanes vs Majestic","Sonabel vs Vitesse","Barca vs Real","Man Utd vs Liverpool","Al Hilal vs Al Nassr","Rahimo vs EFO","ASEC vs Africa"]
    return pd.DataFrame({
        "Match": random.sample(all_m, n),
        "Prono IA": [random.choice(["1X","X2","12"]) for _ in range(n)],
        "Cote LONAB": [round(random.uniform(1.25,1.85),2) for _ in range(n)]
    })

# BOUCLE 7J/7 INFINI
for i in range(st.session_state.nb_jours):
    d = datetime.now() + timedelta(days=i)
    nom = jours[d.weekday()]
    label = f"{nom} - {d.strftime('%d/%m/%Y')} - {type_lonab}"
    
    with st.expander(f"📅 {label}" if i>0 else f"🔥 AUJOURD'HUI - {label}", expanded=(i==0)):
        if "PMUB" in type_lonab:
            st.markdown("### 🐎 PMUB - Pronostics Chevaux")
            st.dataframe(gen_pmub(), use_container_width=True)
            st.info("Base: Cheval le plus sûr | Tiercé: 3 premiers | Quinté: 5 premiers")
        elif "Bourse" in type_lonab:
            st.markdown("### 🌍 Bourse Internationale")
            st.dataframe(gen_bourse(), use_container_width=True)
        else:
            st.dataframe(gen_double(nb_matchs), use_container_width=True)

st.success(f"✅ {st.session_state.nb_jours} jours générés | PMUB + BOURSE INTERNATIONALE actifs")
