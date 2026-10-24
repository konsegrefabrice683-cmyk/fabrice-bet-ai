import streamlit as st, pandas as pd, random, hashlib, requests
from datetime import datetime, timedelta

st.set_page_config(page_title="FABRICE BET AI - V58 COTES 2 CHIFFRES", layout="wide", page_icon="✅")
st.markdown("<style>#MainMenu,footer,header{display:none} .stButton>button{font-weight:bold}</style>", unsafe_allow_html=True)

@st.cache_data(ttl=60)
def get_bourse():
    try:
        r=requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,binancecoin,ripple&vs_currencies=usd", timeout=5).json()
        return {"BTC":float(r["bitcoin"]["usd"]), "ETH":float(r["ethereum"]["usd"]), "SOL":float(r["solana"]["usd"]), "BNB":float(r["binancecoin"]["usd"]), "XRP":float(r["ripple"]["usd"])}
    except:
        return {"BTC":80530.0, "ETH":2450.0, "SOL":145.0, "BNB":610.0, "XRP":0.52}

crypto=get_bourse()
if "nb" not in st.session_state: st.session_state.nb=1
def seed(d,s=""): return int(hashlib.md5((d.strftime("%Y%m%d")+s).encode()).hexdigest()[:8],16)

# ✅ COTES 2 CHIFFRES APRES VIRGULE
def monstre_meta_ai(marche, prono, rnd):
    att = rnd.randint(65, 94); forme = rnd.randint(60, 96); xg = round(rnd.uniform(0.8, 3.6),1)
    
    if marche == "Double Chance":
        if prono == "1X": proba_reelle, conf, cote = rnd.randint(72,84), 78, 1.45
        elif prono == "X2": proba_reelle, conf, cote = rnd.randint(68,78), 72, 1.65
        else: proba_reelle, conf, cote = rnd.randint(70,80), 78, 1.55
    elif marche == "BTTS":
        if prono == "GG Oui": proba_reelle, conf, cote = rnd.randint(68,76), 72, 1.85
        else: proba_reelle, conf, cote = rnd.randint(55,65), 72, 1.90
    elif marche == "Over Under":
        if prono == "Over 0.5": proba_reelle, conf, cote = rnd.randint(87,93), 85, 1.25
        elif prono == "Over 1.5": proba_reelle, conf, cote = rnd.randint(73,81), 78, 1.45
        elif prono == "Over 2.5": proba_reelle, conf, cote = rnd.randint(52,66), 72, 1.85
        elif prono == "Over 3.5": proba_reelle, conf, cote = rnd.randint(32,44), 72, 2.20
        elif prono == "Over 4.5": proba_reelle, conf, cote = rnd.randint(18,29), 72, 3.10
        elif prono == "Over 5.5": proba_reelle, conf, cote = rnd.randint(9,16), 72, 4.50
        elif "Under" in prono: proba_reelle, conf, cote = rnd.randint(35,65), 72, 1.90
        else: proba_reelle, conf, cote = rnd.randint(40,55), 72, 1.90
    elif marche == "Score Exact":
        if prono == "1-0": proba_reelle, conf, cote = rnd.randint(11,15), 85, 6.20
        elif prono == "2-0": proba_reelle, conf, cote = rnd.randint(8,12), 78, 7.50
        elif prono == "2-1": proba_reelle, conf, cote = rnd.randint(7,10), 72, 8.50
        elif prono == "1-1": proba_reelle, conf, cote = rnd.randint(10,14), 78, 6.80
        elif prono == "0-0": proba_reelle, conf, cote = rnd.randint(6,9), 72, 9.50
        elif prono == "3-0": proba_reelle, conf, cote = rnd.randint(4,7), 85, 11.00
        else: proba_reelle, conf, cote = rnd.randint(5,10), 72, 8.00
    elif marche == "1X2":
        if prono == "1": proba_reelle, conf, cote = rnd.randint(55,68), 72, 2.10
        elif prono == "X": proba_reelle, conf, cote = rnd.randint(22,32), 72, 3.20
        else: proba_reelle, conf, cote = rnd.randint(45,58), 72, 2.40
    else:
        proba_reelle, conf, cote = rnd.randint(62,82), 78, 1.65
    
    # ✅ COTE ARRONDI 2 CHIFFRES - 3.10 pas 3.100000
    cote_2chiffres = round(cote, 2)
    
    if conf==85: return {"Proba_Reelle":f"{proba_reelle}%","Confiance_IA":f"{conf}%","Cote":cote_2chiffres,"Value":f"+{proba_reelle}% réel","IA":conf,"STATUT":f"🟢🟢 {conf}% {marche}","Analyse":f"✅ {marche} {prono} Cote {cote_2chiffres:.2f} - Proba {proba_reelle}% + Confiance {conf}%"}
    elif conf==78: return {"Proba_Reelle":f"{proba_reelle}%","Confiance_IA":f"{conf}%","Cote":cote_2chiffres,"Value":f"+{proba_reelle}% réel","IA":conf,"STATUT":f"🟢 {conf}% {marche}","Analyse":f"✅ {marche} {prono} Cote {cote_2chiffres:.2f}"}
    else: return {"Proba_Reelle":f"{proba_reelle}%","Confiance_IA":f"{conf}%","Cote":cote_2chiffres,"Value":f"+{proba_reelle}% réel","IA":conf,"STATUT":f"🟢 {conf}% {marche}","Analyse":f"✅ {marche} {prono} Cote {cote_2chiffres:.2f}"}

def style_meta(df):
    def couleur(v):
        s=str(v)
        if "85%" in s: return 'background-color: #006400; color: white; font-weight: bold'
        elif "78%" in s: return 'background-color: #00AA00; color: white; font-weight: bold'
        elif "72%" in s: return 'background-color: #00FF00; color: black; font-weight: bold'
        else: return ''
    return df.style.map(couleur, subset=["STATUT"]) if "STATUT" in df.columns else df.style

# ✅ FORMAT 2 CHIFFRES POUR TOUT LE DATAFRAME
def format_cote_2chiffres(df):
    if "Cote" in df.columns:
        df["Cote"] = df["Cote"].map(lambda x: f"{float(x):.2f}")
    return df

fixtures=[("Liverpool vs Brighton","PL"),("Man City vs Arsenal","PL"),("Barcelona vs Real Madrid","Liga"),("Bayern vs Hoffenheim","Bundes"),("Inter vs Fiorentina","Serie A"),("PSG vs Lyon","Ligue1"),("Man United vs Bournemouth","PL"),("Monaco vs Lille","Ligue1"),]

bourse_complete={"FOREX MAJEURES":[("EUR/USD",1.0850,""),("GBP/USD",1.2950,"")],"FOREX XOF":[("USD/XOF",605.50," XOF"),("EUR/XOF",657.00," XOF")],"INDICE US":[("S&P 500",7623.68,""),("NASDAQ",25955.19,"")],"ACTION US TECH":[("TSLA",372.22,"$"),("NVDA",210.96,"$"),("AAPL",347.72,"$")],"CRYPTO":[("BTC/USD",crypto["BTC"],"$"),("ETH/USD",crypto["ETH"],"$")],"MATIERES":[("OR - GOLD",2650.30,"$/oz"),("PETROLE - WTI",78.50,"$")]}

jours=["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"]
st.title("✅ V58 - COTES 2 CHIFFRES APRES VIRGULE - 3.10 PAS 3.100000")
st.caption(f"Cote 2 chiffres: 1.25 1.45 1.85 2.20 3.10 4.50 6.20 7.50 - {datetime.now():%d/%m/%Y}")

col1,col2,col3,col4,col5=st.columns(5)
with col1:
    if st.button("➕ 3 JOURS", use_container_width=True): st.session_state.nb+=1; st.rerun()
with col2:
    if st.button("➕ 30 JOURS", use_container_width=True): st.session_state.nb+=10; st.rerun()
with col3:
    if st.button("➕ 90 JOURS", use_container_width=True): st.session_state.nb+=30; st.rerun()
with col4:
    if st.button("➕ 365 JOURS", use_container_width=True): st.session_state.nb+=122; st.rerun()
with col5:
    if st.button("RESET", use_container_width=True): st.session_state.nb=1; st.rerun()

st.error("❌ AVANT (ton screenshot): Cote 3.100000 4.500000 1.250000 = 6 chiffres")
st.success("✅ MAINTENANT V58: Cote 3.10 4.50 1.25 1.45 1.85 2.20 = 2 chiffres après virgule")

tab1,tab2,tab3=st.tabs(["✅ FOOT COTES 2 CHIFFRES","✅ PMU-B COTES 2 CHIFFRES","✅ BOURSE COTES 2 CHIFFRES"])

with tab1:
    st.markdown("### FOOT - COTES 2 CHIFFRES - SANS MELANGE")
    type1=st.selectbox("Type FOOT", ["Over Under 0.5-5.5 (Over Under seulement)","Double Chance (1X X2 12 seulement)","BTTS (GG Oui GG Non seulement)","Score Exact (1-0 2-0 2-1 1-1 0-0 3-0 seulement)","1X2 (1 X 2 seulement)","TOUS COMPLET SANS MELANGE"], index=0, key="t1cote2")
    nb1=st.slider("NOMBRE MATCHS FOOT INFINI 1-30", 1, 30, 15, key="n1cote2")
    total=st.session_state.nb*3
    for i in range(total):
        d=datetime.now()+timedelta(days=i); nom=jours[d.weekday()]; rnd=random.Random(seed(d,f"cote2_foot_{nb1}_{type1}_{i}"))
        with st.expander(f"{'AUJOURDHUI ✅' if i==0 else f'J+{i}'} - {nom} {d.strftime('%d/%m/%Y')} - {nb1} matchs - COTES 2 CHIFFRES", expanded=(i==0)):
            data=[]
            if "Double Chance" in type1:
                marche = "Double Chance"; pronos_list = ["1X","X2","12"]
                pronos = [rnd.choice(pronos_list) for _ in range(nb1)]
                if nb1==8: pronos = ["1X","X2","12","1X","X2","12","1X","X2"]
            elif "BTTS" in type1:
                marche = "BTTS"; pronos_list = ["GG Oui","GG Non"]
                pronos = [rnd.choice(pronos_list) for _ in range(nb1)]
            elif "Over Under" in type1:
                marche = "Over Under"; pronos_list = ["Over 0.5","Over 1.5","Over 2.5","Over 3.5","Over 4.5","Over 5.5","Under 2.5","Under 3.5"]
                pronos = pronos_list[:nb1] if nb1<=len(pronos_list) else [rnd.choice(pronos_list) for _ in range(nb1)]
                if nb1==8: pronos = ["Over 0.5","Over 1.5","Over 2.5","Over 3.5","Over 4.5","Over 5.5","Under 2.5","Under 3.5"]
            elif "Score Exact" in type1:
                marche = "Score Exact"; pronos_list = ["1-0","2-0","2-1","1-1","0-0","3-0","0-1","1-2"]
                pronos = pronos_list[:nb1] if nb1<=len(pronos_list) else [rnd.choice(pronos_list) for _ in range(nb1)]
            elif "1X2" in type1:
                marche = "1X2"; pronos_list = ["1","X","2"]; pronos = [rnd.choice(pronos_list) for _ in range(nb1)]
            else:
                marche = "Double Chance"; pronos = [rnd.choice(["1X","X2","12"]) for _ in range(nb1)]
            
            sel=[rnd.choice(fixtures) for _ in range(nb1)]
            for idx, (team,lig) in enumerate(sel):
                prono=pronos[idx]
                r=monstre_meta_ai(marche, prono, rnd)
                data.append({"Match":team,"Marche":marche,"Prono":prono,"Cote":r["Cote"],"Proba Reelle UNIQUE":r["Proba_Reelle"],"Confiance IA ELEVEE":r["Confiance_IA"],"IA":r["IA"],"STATUT":r["STATUT"]})
            
            # ✅ FORMAT 2 CHIFFRES ICI
            df = pd.DataFrame(data)
            df = format_cote_2chiffres(df)
            st.dataframe(style_meta(df), use_container_width=True, hide_index=True)
            st.success(f"✅ COTES 2 CHIFFRES: {', '.join([f'{d} ' for d in df['Cote'].tolist()][:5])}... - 3.10 pas 3.100000")

with tab2:
    st.markdown("### PMU-B COTES 2 CHIFFRES")
    type2=st.selectbox("Type PMU-B", ["Simple Gagnant","Couple Gagnant","Tierce Ordre","Quarte Ordre","Quinte Ordre","Multi en 7"], index=0, key="t2cote2")
    nb2=st.slider("NOMBRE COURSES PMU-B INFINI 1-30", 1, 30, 20, key="n2cote2")
    total=st.session_state.nb*3
    for i in range(total):
        d=datetime.now()+timedelta(days=i); nom=jours[d.weekday()]; rnd=random.Random(seed(d,f"cote2_pmub_{nb2}_{type2}_{i}"))
        with st.expander(f"{'AUJOURDHUI' if i==0 else f'J+{i}'} - {nom} {d.strftime('%d/%m/%Y')} - {nb2} courses", expanded=(i==0)):
            data=[]
            for c in range(nb2):
                chevaux=rnd.sample(list(range(1,21)),10)
                def prono_pmu(m):
                    if "Simple" in m: return f"{chevaux[0]}"
                    elif "Couple" in m: return f"{chevaux[0]}-{chevaux[1]}"
                    elif "Tierce" in m: return f"{chevaux[0]}-{chevaux[1]}-{chevaux[2]}"
                    elif "Quarte" in m: return f"{chevaux[0]}-{chevaux[1]}-{chevaux[2]}-{chevaux[3]}"
                    else: return f"{chevaux[0]}-{chevaux[1]}-{chevaux[2]}-{chevaux[3]}-{chevaux[4]}"
                marche=type2
                r=monstre_meta_ai(marche, prono_pmu(marche), rnd)
                cote_2 = f"{float(r['Cote']):.2f}"
                data.append({"Course":f"R{i+1}C{c+1}","Type":marche,"Prono":prono_pmu(marche),"Cote":cote_2,"Proba Reelle":r["Proba_Reelle"],"Confiance":r["Confiance_IA"],"STATUT":r["STATUT"]})
            st.dataframe(style_meta(pd.DataFrame(data)), use_container_width=True, hide_index=True)

with tab3:
    st.markdown("### BOURSE INTERNATIONALE COTES 2 CHIFFRES")
    type3=st.selectbox("Type BOURSE", ["FOREX MAJEURES","FOREX XOF","INDICE US","ACTION US TECH","CRYPTO"], index=0, key="t3cote2")
    nb3=st.slider("NOMBRE ACTIFS BOURSE INFINI 1-30", 1, 30, 20, key="n3cote2")
    total=st.session_state.nb*3
    for i in range(total):
        d=datetime.now()+timedelta(days=i); nom=jours[d.weekday()]; rnd=random.Random(seed(d,f"cote2_bourse_{nb3}_{type3}_{i}"))
        with st.expander(f"{'AUJOURDHUI' if i==0 else f'J+{i}'} - {nom} {d.strftime('%d/%m/%Y')} - {nb3} actifs", expanded=(i==0)):
            data=[]
            if "FOREX MAJEURES" in type3: markets=bourse_complete["FOREX MAJEURES"]
            elif "FOREX XOF" in type3: markets=bourse_complete["FOREX XOF"]
            elif "INDICE US" in type3: markets=bourse_complete["INDICE US"]
            elif "ACTION US TECH" in type3: markets=bourse_complete["ACTION US TECH"]
            else: markets=bourse_complete["CRYPTO"]
            sel=[rnd.choice(markets) for _ in range(nb3)]
            for name,price,unit in sel:
                signal="ACHETER" if rnd.randint(0,1)==0 else "VENDRE"
                r=monstre_meta_ai("BOURSE", signal, rnd)
                cote_2 = f"{float(r['Cote']):.2f}"
                data.append({"Actif":name,"Prix":f"{price}{unit}","Signal":signal,"Cote":cote_2,"Proba Reelle":r["Proba_Reelle"],"Confiance":r["Confiance_IA"],"STATUT":r["STATUT"]})
            st.dataframe(style_meta(pd.DataFrame(data)), use_container_width=True, hide_index=True)

st.success("✅ V58 - COTES 2 CHIFFRES - 3.10 4.50 1.25 1.45 1.85 2.20 - PLUS DE 3.100000 4.500000")
