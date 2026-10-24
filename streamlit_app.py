import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="FABRICE BET AI", layout="wide", page_icon="⚽")
st.title("⚽ FABRICE BET AI")
st.caption("DOUBLE CHANCE = 10-15 MATCHS | AUTRES = FIXE")

if "nb_jours" not in st.session_state:
    st.session_state.nb_jours = 1

c1, c2 = st.columns(2)
with c1:
    if st.button("➕ +3 JOURS", use_container_width=True):
        st.session_state.nb_jours += 3
        st.rerun()
with c2:
    if st.button("🔄 RESET", use_container_width=True):
        st.session_state.nb_jours = 1
        st.rerun()

type_paris = st.selectbox("🎯 Type LONAB", ["Double Chance", "1X2", "BTTS Oui/Non", "Over/Under", "Score Exact"], index=0)

# --- SEULEMENT DOUBLE CHANCE A LE SLIDER 10-15 ---
if type_paris == "Double Chance":
    nb_matchs = st.slider("🔢 Nombre de matchs Double Chance", 10, 15, 12, step=1)
else:
    nb_matchs = None

def get_label(j, d, nb, tp):
    ds = d.strftime("%d/%m/%Y")
    if tp == "Double Chance":
        if j==0: return f"AUJOURD HUI - {ds} - {nb} MATCHS DOUBLE CHANCE"
        return f"JOUR +{j} - {ds} - {nb} MATCHS DOUBLE CHANCE"
    else:
        if j==0: return f"AUJOURD HUI - {ds} - {tp}"
        return f"JOUR +{j} - {ds} - {tp}"

today = datetime.now()

ALL_MATCHS = {
    "Double Chance": [
        ["Inter vs Arsenal", "1X", 1.72, "82%", "+7.2%", 92.5, "FEU VERT ULTRA"],
        ["Inter vs Barca", "X2", 1.45, "79%", "+5.5%", 89.2, "FEU VERT ULTRA"],
        ["PSG vs EFO", "1X", 1.32, "88%", "+6.5%", 94.1, "FEU VERT ULTRA"],
        ["Inter vs Man City", "12", 1.52, "76%", "+4.8%", 86.3, "FEU VERT"],
        ["EFO vs Bayern", "X2", 1.28, "84%", "+5.8%", 88.7, "FEU VERT ULTRA"],
        ["Real vs Brest", "1X", 1.42, "80%", "+5.0%", 87.5, "FEU VERT ULTRA"],
        ["ASFA vs EFO", "1X", 1.65, "72%", "+4.2%", 82.1, "FEU VERT"],
        ["Barca vs PSG", "12", 1.55, "78%", "+5.5%", 85.8, "FEU VERT ULTRA"],
        ["Man City vs EFO", "1X", 1.38, "86%", "+6.2%", 91.2, "FEU VERT ULTRA"],
        ["Barca vs Nice", "X2", 1.35, "83%", "+6.0%", 90.5, "FEU VERT ULTRA"],
        ["Brest vs Nice", "1X", 1.55, "81%", "+8.5%", 89.8, "FEU VERT ULTRA"],
        ["Mamelodi vs Wiliete", "1X", 1.72, "80%", "+7.2%", 88.2, "FEU VERT ULTRA"],
        ["Real Madrid vs Barca", "X2", 1.45, "77%", "+5.5%", 86.5, "FEU VERT ULTRA"],
        ["Bayern vs Dortmund", "1X", 1.28, "85%", "+5.1%", 90.1, "FEU VERT ULTRA"],
        ["PSG vs Lyon", "1X", 1.22, "89%", "+4.2%", 93.5, "FEU VERT ULTRA"],
    ],
    "1X2": [
        ["Inter vs Arsenal", "1", 2.45, "62%", "+5.5%", 82.3, "FEU VERT"],
        ["PSG vs EFO", "1", 1.65, "70%", "+7.1%", 88.5, "FEU VERT ULTRA"],
        ["Man City vs EFO", "1", 1.38, "76%", "+6.2%", 91.2, "FEU VERT ULTRA"],
    ],
    "BTTS Oui/Non": [
        ["Inter vs Arsenal", "BTTS Oui", 1.85, "72%", "+6.2%", 88.1, "FEU VERT ULTRA"],
        ["PSG vs EFO", "BTTS Non", 1.55, "80%", "+5.8%", 91.1, "FEU VERT ULTRA"],
    ],
    "Over/Under": [
        ["Inter vs Arsenal", "Over 2.5", 1.85, "74%", "+6.8%", 88.5, "FEU VERT ULTRA"],
        ["PSG vs EFO", "Over 1.5", 1.28, "90%", "+4.8%", 93.5, "FEU VERT ULTRA"],
    ],
    "Score Exact": [
        ["Inter vs Arsenal", "2-1", 8.50, "18%", "+8.5%", 78.2, "FEU VERT"],
        ["PSG vs EFO", "2-0", 7.20, "20%", "+7.5%", 79.8, "FEU VERT"],
    ]
}

for j in range(st.session_state.nb_jours):
    dj = today + timedelta(days=j)
    with st.expander(get_label(j, dj, nb_matchs, type_paris), expanded=(j==0)):
        base_rows = ALL_MATCHS.get(type_paris, ALL_MATCHS["Double Chance"])
        
        if type_paris == "Double Chance":
            rows = base_rows[:nb_matchs]
        else:
            rows = base_rows
        
        df = pd.DataFrame(rows, columns=["Match","Prono IA","Cote LONAB","Proba IA","Value","IA %","STATUT"])
        st.dataframe(df, use_container_width=True)
        
        if type_paris == "Double Chance":
            st.caption(f"✅ {len(rows)} matchs Double Chance - FIX 1X / X2 / 12")
        else:
            st.caption(f"✅ {len(rows)} matchs {type_paris}")

st.success("✅ DOUBLE CHANCE 10-15 OK - AUTRES TYPES FIXES")
