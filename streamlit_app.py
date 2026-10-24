import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="FABRICE BET AI", layout="wide", page_icon="⚽")
st.title("⚽ FABRICE BET AI")
st.caption("V1.0 - 24/10/2026 - OUAGA - FIX 1X/X2")

if "nb_jours" not in st.session_state:
    st.session_state.nb_jours = 1

c1, c2 = st.columns(2)
with c1:
    if st.button("➕ +3 JOURS INFINIS", width='stretch'):
        st.session_state.nb_jours += 3
        st.rerun()
with c2:
    if st.button("🔄 RESET", width='stretch'):
        st.session_state.nb_jours = 1
        st.rerun()

def get_label(j, d):
    ds = d.strftime("%d/%m/%Y")
    if j==0: return f"AUJOURD HUI - {ds} - 15 MATCHS IA"
    return f"JOUR +{j} - {ds} - 15 MATCHS IA"

today = datetime.now()
type_paris = st.selectbox("🎯 Type LONAB", ["Double Chance", "1X2", "BTTS Oui/Non", "Over/Under", "Score Exact"], index=0)

for j in range(st.session_state.nb_jours):
    dj = today + timedelta(days=j)
    with st.expander(get_label(j, dj), expanded=(j==0)):
        if type_paris == "Double Chance":
            rows = [
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
            ]
        elif type_paris == "1X2":
            rows = [
                ["Inter vs Arsenal", "1", 2.45, "62%", "+5.5%", 82.3, "FEU VERT"],
                ["PSG vs EFO", "1", 1.65, "70%", "+7.1%", 88.5, "FEU VERT ULTRA"],
                ["Man City vs EFO", "1", 1.38, "76%", "+6.2%", 91.2, "FEU VERT ULTRA"],
            ]
        elif type_paris == "BTTS Oui/Non":
            rows = [
                ["Inter vs Arsenal", "BTTS Oui", 1.85, "72%", "+6.2%", 88.1, "FEU VERT ULTRA"],
                ["Inter vs Barca", "BTTS Oui", 1.65, "78%", "+6.5%", 90.2, "FEU VERT ULTRA"],
                ["PSG vs EFO", "BTTS Non", 1.90, "65%", "+4.0%", 82.0, "FEU VERT"],
            ]
        elif type_paris == "Over/Under":
            rows = [
                ["Inter vs Arsenal", "Over 2.5", 1.85, "74%", "+6.8%", 88.5, "FEU VERT ULTRA"],
                ["Inter vs Barca", "Over 1.5", 1.34, "88%", "+5.2%", 92.2, "FEU VERT ULTRA"],
                ["PSG vs EFO", "Over 1.5", 1.28, "90%", "+4.8%", 93.5, "FEU VERT ULTRA"],
            ]
        else:
            rows = [
                ["Inter vs Arsenal", "2-1", 8.50, "18%", "+8.5%", 78.2, "FEU VERT"],
                ["PSG vs EFO", "2-0", 7.20, "20%", "+7.5%", 79.8, "FEU VERT"],
            ]
        df = pd.DataFrame(rows, columns=["Match","Prono IA","Cote LONAB","Proba IA","Value","IA %","STATUT"])
        st.dataframe(df, width='stretch')

st.success("✅ FABRICE BET AI V1.0 - FIX: Prono = 1X / X2 / 12 - PLUS Double C")
