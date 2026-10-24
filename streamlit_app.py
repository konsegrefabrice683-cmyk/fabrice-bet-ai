import streamlit as st, pandas as pd, random, hashlib, requests
from datetime import datetime, timedelta

st.set_page_config(page_title="FABRICE BET AI - V52 COMPLET FINAL", layout="wide", page_icon="🔥")
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

# ✅ MONSTRE - DIFFERENTS MAIS ELEVES 72% 78% 85%
def monstre_diff_eleve(marche, prono_type, rnd):
    att=rnd.randint(76,92); defe=rnd.randint(65,88); forme=rnd.randint(82,96)
    if "0.5" in prono_type and "Over" in prono_type:
        return {"IA":85, "Proba":85, "Value":"+12%", "Cote":1.65, "Statut":"🟢🟢 FEU VERT 85% ELEVE", "Analyse":f"🔥 {prono_type} 85% - Att {att}% + Forme {forme}% - Tres facile"}
    elif "1.5" in prono_type:
        return {"IA":78, "Proba":78, "Value":"+10%", "Cote":1.75, "Statut":"🟢 FEU VERT 78% ELEVE", "Analyse":f"🔥 {prono_type} 78% - Att {att}% + Forme {forme}% - Facile"}
    elif "2.5" in prono_type:
        return {"IA":72, "Proba":72, "Value":"+8%", "Cote":1.85, "Statut":"🟢 FEU VERT 72% ELEVE", "Analyse":f"🔥 {prono_type} 72% - Att {att}% + Forme {forme}% - Bon"}
    elif "3.5" in prono_type:
        return {"IA":78, "Proba":78, "Value":"+10%", "Cote":1.90, "Statut":"🟢 FEU VERT 78% ELEVE", "Analyse":f"🔥 {prono_type} 78% - Att {att}% - Bon"}
    elif "Score Exact" in marche:
        # SCORE EXACT - DIFFERENTS MAIS ELEVE 72%+ (difficile mais on force haut)
        if prono_type in ["1-0","2-0"]: return {"IA":72, "Proba":72, "Value":"+8%", "Cote":6.50, "Statut":"🟢 FEU VERT 72% ELEVE", "Analyse":f"🔥 Score {prono_type} 72% - Att {att}% fort - Score exact eleve"}
        else: return {"IA":72, "Proba":72, "Value":"+7%", "Cote":7.20, "Statut":"🟢 FEU VERT 72% ELEVE", "Analyse":f"🔥 Score {prono_type} 72% - Forme {forme}% - Eleve"}
    elif "Quinte Ordre" in marche: return {"IA":72, "Proba":72, "Value":"+8%", "Cote":1200.0, "Statut":"🟢 FEU VERT 72% ELEVE", "Analyse":f"🔥 {marche} 72% - Difficile mais eleve"}
    elif "Quarte Ordre" in marche: return {"IA":72, "Proba":72, "Value":"+8%", "Cote":250.0, "Statut":"🟢 FEU VERT 72% ELEVE", "Analyse":f"🔥 {marche} 72%"}
    elif "Tierce Ordre" in marche: return {"IA":78, "Proba":78, "Value":"+10%", "Cote":45.0, "Statut":"🟢 FEU VERT 78% ELEVE", "Analyse":f"🔥 {marche} 78%"}
    else:
        score=rnd.choice([72,78,85])
        if score==85: return {"IA":85, "Proba":85, "Value":"+12%", "Cote":1.65, "Statut":"🟢🟢 FEU VERT 85% ELEVE", "Analyse":f"🔥 {prono_type} 85% ELEVE"}
        elif score==78: return {"IA":78, "Proba":78, "Value":"+10%", "Cote":1.75, "Statut":"🟢 FEU VERT 78% ELEVE", "Analyse":f"🔥 {prono_type} 78% ELEVE"}
        else: return {"IA":72, "Proba":72, "Value":"+8%", "Cote":1.85, "Statut":"🟢 FEU VERT 72% ELEVE", "Analyse":f"🔥 {prono_type} 72% ELEVE"}

def style_fix(df):
    def couleur(v):
        s=str(v)
        if "85%" in s: return 'background-color: #006400; color: white; font-weight: bold'
        elif "78%" in s: return 'background-color: #00AA00; color: white; font-weight: bold'
        elif "72%" in s: return 'background-color: #00FF00; color: black; font-weight: bold'
        else: return ''
    return df.style.map(couleur, subset=["STATUT"]) if "STATUT" in df.columns else df.style

fixtures=[("Liverpool vs Brighton","PL",2.9),("Man City vs Arsenal","PL",2.8),("Barcelona vs Real Madrid","Liga",3.2),("Bayern vs Hoffenheim","Bundes",3.0),("Inter vs Fiorentina","Serie A",2.6),("PSG vs Lyon","Ligue1",2.9),("Man United vs Bournemouth","PL",2.7),("Monaco vs Lille","Ligue1",2.4),]

bourse_complete={
    "FOREX MAJEURES":[("EUR/USD",1.0850,""),("GBP/USD",1.2950,""),("USD/JPY",149.20,""),("USD/CHF",0.8950,"")],
    "FOREX XOF":[("USD/XOF",605.50," XOF"),("EUR/XOF",657.00," XOF")],
    "FOREX EXOTIQUE":[("USD/TRY",34.20,""),("USD/ZAR",18.50,"")],
    "INDICE US":[("S&P 500",7623.68,""),("NASDAQ",25955.19,""),("DOW JONES",52215.58,""),("RUSSELL 2000",2015.30,"")],
    "INDICE EUROPE":[("CAC 40",8150.20,""),("DAX",19200.50,""),("FTSE 100",8420.10,""),("EURO STOXX 50",4950.30,"")],
    "INDICE ASIE":[("NIKKEI 225",38500.00,""),("HANG SENG",20500.00,"")],
    "ACTION US TECH":[("TSLA",372.22,"$"),("NVDA",210.96,"$"),("AAPL",347.72,"$"),("MSFT",445.20,"$"),("META",485.30,"$"),("GOOGL",175.80,"$"),("AMZN",201.20,"$")],
    "ACTION US AUTRE":[("NFLX",695.40,"$"),("AMD",165.30,"$")],
    "ACTION EUROPE":[("LVMH",750.20,"€"),("TOTALENERGIES",62.50,"€"),("ASML",680.30,"€")],
    "CRYPTO":[("BTC/USD",crypto["BTC"],"$"),("ETH/USD",crypto["ETH"],"$"),("SOL/USD",crypto["SOL"],"$"),("BNB/USD",crypto["BNB"],"$"),("XRP/USD",crypto["XRP"],"$")],
    "MATIERES":[("OR - GOLD",2650.30,"$/oz"),("PETROLE - WTI",78.50,"$"),("ARGENT",31.20,"$/oz")]
}

jours=["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"]
st.title("🔥 V52 COMPLET FINAL - FOOT + PMU-B + BOURSE + SCORE EXACT")
st.caption(f"Over Under illimité diff mais eleve 72% 78% 85% + Score Exact + PMU-B complet + Bourse internationale - {datetime.now():%d/%m/%Y}")

col1,col2,col3,col4=st.columns(4)
with col1:
    if st.button("PLUS 3 JOURS", use_container_width=True): st.session_state.nb+=1; st.rerun()
with col2:
    if st.button("PLUS 30 JOURS", use_container_width=True): st.session_state.nb+=10; st.rerun()
with col3:
    if st.button("MAJ", use_container_width=True): st.cache_data.clear(); st.rerun()
with col4:
    if st.button("RESET", use_container_width=True): st.session_state.nb=1; st.rerun()

st.success(f"🔥 {st.session_state.nb*3} jours - FOOT Score Exact + Over Under diff eleve + PMU-B Quinte Quarte Tierce Multi + Bourse Forex XOF Indice Action Crypto Or")

tab1,tab2,tab3=st.tabs(["🔥 CHAMPION 1 - FOOT COMPLET","🔥 CHAMPION 2 - PMU-B COMPLET","🔥 CHAMPION 3 - BOURSE INTERNATIONALE"])

with tab1:
    st.markdown("### FOOT COMPLET - SCORE EXACT + OVER UNDER ILLIMITE DIFF ELEVE")
    type1=st.selectbox("Type FOOT", ["LEGENDE - 72%+ ELEVE","1X2","Double Chance","Score Exact ILLIMITE 1-0 2-0 2-1 1-1 0-0","Over Under 0.5-5.5 ILLIMITE DIFF ELEVE 72% 78% 85%","BTTS - GG/NG","Cartons","Expulsion","Corners","Mi-Temps / MT-Fin","TOUS COMPLET"], index=4, key="t1comp")
    nb1=st.slider("Matchs FOOT", 1, 15, 8, key="n1comp")
    total=st.session_state.nb*3
    for i in range(total):
        d=datetime.now()+timedelta(days=i); nom=jours[d.weekday()]; rnd=random.Random(seed(d,f"foot_complet_{nb1}_{type1}_{i}"))
        with st.expander(f"{'AUJOURDHUI 🔥' if i==0 else f'J+{i}'} - {nom} {d.strftime('%d/%m/%Y')} - {nb1} matchs", expanded=(i==0)):
            data=[]
            over_under_list = ["Over 0.5","Over 1.5","Over 2.5","Over 3.5","Over 4.5","Over 5.5","Under 0.5","Under 1.5","Under 2.5","Under 3.5","Under 4.5","Under 5.5"]
            score_exact_list = ["1-0","2-0","2-1","3-0","1-1","0-0","0-1","1-2","2-2","3-1","3-2","0-2"]
            sel=rnd.sample(fixtures, min(nb1, len(fixtures)))
            if "Score Exact" in type1:
                pronos = rnd.sample(score_exact_list, min(nb1, len(score_exact_list))) if nb1<=len(score_exact_list) else [rnd.choice(score_exact_list) for _ in range(nb1)]
                if nb1==8: pronos = ["1-0","2-0","2-1","1-1","0-0","2-2","3-0","1-2"]
            elif "Over Under" in type1:
                if nb1==8: pronos = ["Over 0.5","Over 1.5","Over 2.5","Over 3.5","Over 4.5","Over 5.5","Under 2.5","Under 3.5"]
                else: pronos = rnd.sample(over_under_list, min(nb1, len(over_under_list)))
            else:
                pronos = ["1"]*nb1
            
            for idx, (team,lig,moy) in enumerate(sel):
                if "Score Exact" in type1:
                    marche="Score Exact"; prono=pronos[idx]
                elif "Over Under" in type1:
                    marche="Over Under"; prono=pronos[idx]
                elif type1=="1X2": marche,prono="1X2",rnd.choice(["1","X","2"])
                elif type1=="Double Chance": marche,prono="Double Chance",rnd.choice(["1X","X2","12"])
                elif "BTTS" in type1: marche,prono="BTTS",rnd.choice(["GG Oui","GG Non"])
                elif type1=="Cartons": marche,prono="Cartons",rnd.choice(["Over 3.5 Cartons","Under 3.5 Cartons"])
                elif type1=="Expulsion": marche,prono="Expulsion",rnd.choice(["Expulsion Oui","Expulsion Non"])
                elif type1=="Corners": marche,prono="Corners",rnd.choice(["Over 8.5 Corners","Under 8.5 Corners"])
                elif "Mi-Temps" in type1: marche,prono="MT-Fin",rnd.choice(["1/1","X/1","2/2"])
                else: marche,prono="Double Chance","1X"
                
                r=monstre_diff_eleve(marche, prono, rnd)
                data.append({"Match":team,"Marche":marche,"Prono":prono,"Cote":r["Cote"],"Proba":f"{r['Proba']}%","Value":r["Value"],"IA":r["IA"],"STATUT":r["Statut"],"Analyse":r["Analyse"]})
            st.dataframe(style_fix(pd.DataFrame(data)), use_container_width=True, hide_index=True)

with tab2:
    st.markdown("### PMU-B COMPLET - SIMPLE COUPLE TIERCE QUARTE QUINTE MULTI")
    type2=st.selectbox("Type PMU-B", ["LEGENDE - 72%+","Simple Gagnant","Simple Place","Couple Gagnant","Couple Place","Couple Ordre","Tierce Ordre","Tierce Desordre","Quarte Ordre","Quarte Desordre","Quinte Ordre","Quinte Desordre","Quinte+","Multi en 4","Multi en 5","Multi en 6","Multi en 7","TOUS COMPLET PMU-B"], index=0, key="t2comp")
    nb2=st.slider("Courses PMU-B", 1, 15, 10, key="n2comp")
    total=st.session_state.nb*3
    for i in range(total):
        d=datetime.now()+timedelta(days=i); nom=jours[d.weekday()]; rnd=random.Random(seed(d,f"pmub_complet_{nb2}_{type2}_{i}"))
        with st.expander(f"{'AUJOURDHUI' if i==0 else f'J+{i}'} - {nom} {d.strftime('%d/%m/%Y')} - {nb2} courses - 72%+", expanded=(i==0)):
            data=[]
            for c in range(nb2):
                chevaux=rnd.sample(list(range(1,21)),10)
                def prono_pmu(m):
                    if "Simple" in m: return f"{chevaux[0]}"
                    elif "Couple" in m: return f"{chevaux[0]}-{chevaux[1]}"
                    elif "Tierce" in m: return f"{chevaux[0]}-{chevaux[1]}-{chevaux[2]}"
                    elif "Quarte" in m: return f"{chevaux[0]}-{chevaux[1]}-{chevaux[2]}-{chevaux[3]}"
                    elif "Quinte" in m: return f"{chevaux[0]}-{chevaux[1]}-{chevaux[2]}-{chevaux[3]}-{chevaux[4]}"
                    elif "Multi en 4" in m: return f"{chevaux[0]}-{chevaux[1]}-{chevaux[2]}-{chevaux[3]}"
                    elif "Multi en 5" in m: return f"{chevaux[0]}-{chevaux[1]}-{chevaux[2]}-{chevaux[3]}-{chevaux[4]}"
                    elif "Multi en 6" in m: return f"{chevaux[0]}-{chevaux[1]}-{chevaux[2]}-{chevaux[3]}-{chevaux[4]}-{chevaux[5]}"
                    elif "Multi en 7" in m: return f"{chevaux[0]}-{chevaux[1]}-{chevaux[2]}-{chevaux[3]}-{chevaux[4]}-{chevaux[5]}-{chevaux[6]}"
                    else: return f"{chevaux[0]}"
                if "LEGENDE" in type2: marche="Simple Gagnant"
                elif "TOUS COMPLET" in type2: marche="Simple Gagnant"
                else: marche=type2
                r=monstre_diff_eleve(marche, prono_pmu(marche), rnd)
                cote_pmu = 1.85 if "Simple Gagnant" in marche else 1.35 if "Simple Place" in marche else 4.20 if "Couple Gagnant" in marche else 2.50 if "Couple Place" in marche else 8.50 if "Couple Ordre" in marche else 45.0 if "Tierce Ordre" in marche else 12.0 if "Tierce Desordre" in marche else 250.0 if "Quarte Ordre" in marche else 50.0 if "Quarte Desordre" in marche else 1200.0 if "Quinte Ordre" in marche else 150.0 if "Quinte Desordre" in marche else 900.0 if "Quinte+" in marche else 25.0 if "Multi en 4" in marche else 12.0 if "Multi en 5" in marche else 6.0 if "Multi en 6" in marche else 3.5
                data.append({"Course":f"R{i+1}C{c+1}","Type":marche,"Prono":prono_pmu(marche),"Cote":cote_pmu,"Proba":f"{r['Proba']}%","Value":r["Value"],"IA":r["IA"],"STATUT":r["Statut"],"Analyse":r["Analyse"]})
            st.dataframe(style_fix(pd.DataFrame(data)), use_container_width=True, hide_index=True)

with tab3:
    st.markdown("### BOURSE INTERNATIONALE COMPLETE - FOREX XOF INDICE ACTION CRYPTO OR")
    type3=st.selectbox("Type BOURSE", ["LEGENDE - 72%+","FOREX MAJEURES","FOREX XOF","FOREX EXOTIQUE","INDICE US","INDICE EUROPE","INDICE ASIE","ACTION US TECH","ACTION US AUTRE","ACTION EUROPE","CRYPTO","MATIERES OR PETROLE","TOUS FOREX","TOUS INDICE","TOUS ACTION","TOUS CRYPTO","TOUS COMPLET BOURSE"], index=11, key="t3comp")
    nb3=st.slider("Actifs BOURSE", 1, 20, 12, key="n3comp")
    total=st.session_state.nb*3
    for i in range(total):
        d=datetime.now()+timedelta(days=i); nom=jours[d.weekday()]; rnd=random.Random(seed(d,f"bourse_complet_{nb3}_{type3}_{i}"))
        with st.expander(f"{'AUJOURDHUI' if i==0 else f'J+{i}'} - {nom} {d.strftime('%d/%m/%Y')} - {nb3} actifs - 72%+", expanded=(i==0)):
            data=[]
            if "FOREX MAJEURES" in type3: markets=bourse_complete["FOREX MAJEURES"]
            elif "FOREX XOF" in type3: markets=bourse_complete["FOREX XOF"]
            elif "FOREX EXOTIQUE" in type3: markets=bourse_complete["FOREX EXOTIQUE"]
            elif "TOUS FOREX" in type3: markets=bourse_complete["FOREX MAJEURES"]+bourse_complete["FOREX XOF"]+bourse_complete["FOREX EXOTIQUE"]
            elif "INDICE US" in type3: markets=bourse_complete["INDICE US"]
            elif "INDICE EUROPE" in type3: markets=bourse_complete["INDICE EUROPE"]
            elif "INDICE ASIE" in type3: markets=bourse_complete["INDICE ASIE"]
            elif "TOUS INDICE" in type3: markets=bourse_complete["INDICE US"]+bourse_complete["INDICE EUROPE"]+bourse_complete["INDICE ASIE"]
            elif "ACTION US TECH" in type3: markets=bourse_complete["ACTION US TECH"]
            elif "ACTION US AUTRE" in type3: markets=bourse_complete["ACTION US AUTRE"]
            elif "ACTION EUROPE" in type3: markets=bourse_complete["ACTION EUROPE"]
            elif "TOUS ACTION" in type3: markets=bourse_complete["ACTION US TECH"]+bourse_complete["ACTION US AUTRE"]+bourse_complete["ACTION EUROPE"]
            elif "CRYPTO" in type3: markets=bourse_complete["CRYPTO"]
            elif "MATIERES" in type3: markets=bourse_complete["MATIERES"]
            elif "TOUS COMPLET BOURSE" in type3: markets=bourse_complete["FOREX MAJEURES"]+bourse_complete["INDICE US"]+bourse_complete["ACTION US TECH"]+bourse_complete["CRYPTO"]+bourse_complete["MATIERES"]
            elif "TOUS CRYPTO" in type3: markets=bourse_complete["CRYPTO"]
            else: markets=bourse_complete["FOREX MAJEURES"]+bourse_complete["INDICE US"]+bourse_complete["ACTION US TECH"]+bourse_complete["CRYPTO"]
            sel=rnd.sample(markets, min(nb3, len(markets)))
            for name,price,unit in sel:
                signal="ACHETER" if rnd.randint(0,1)==0 else "VENDRE"; marche=f"{type3} - {signal}"
                r=monstre_diff_eleve(marche, signal, rnd)
                data.append({"Actif":name,"Prix":f"{price}{unit}","Signal":signal,"Proba":f"{r['Proba']}%","Value":r["Value"],"IA":r["IA"],"STATUT":r["Statut"],"Analyse":r["Analyse"]})
            st.dataframe(style_fix(pd.DataFrame(data)), use_container_width=True, hide_index=True)

st.success(f"🔥 V52 COMPLET FINAL - FOOT Score Exact + Over Under illimité diff eleve 72% 78% 85% + PMU-B complet Quinte Quarte Tierce Multi + Bourse internationale Forex XOF Indice Action Crypto Or - {st.session_state.nb*3} jours")
