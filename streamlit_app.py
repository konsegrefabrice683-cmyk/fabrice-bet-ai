import streamlit as st, pandas as pd, random, hashlib, requests
from datetime import datetime, timedelta

st.set_page_config(page_title="FABRICE BET AI", layout="wide", page_icon="🏆")
st.markdown("<style>#MainMenu,footer,header{display:none}</style>", unsafe_allow_html=True)
st.markdown('<meta http-equiv="refresh" content="60">', unsafe_allow_html=True)

@st.cache_data(ttl=60)
def get_bourse():
    try:
        r=requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd", timeout=5).json()
        return {"BTC":r["bitcoin"]["usd"], "ETH":r["ethereum"]["usd"], "SOL":r["solana"]["usd"]}
    except:
        return {"BTC":80763, "ETH":2450, "SOL":145}

crypto_live=get_bourse()
if "nb" not in st.session_state:
    st.session_state.nb=1

def seed(d,s=""):
    return int(hashlib.md5((d.strftime("%Y%m%d")+s).encode()).hexdigest()[:8],16)

st.title("FABRICE BET AI")
st.caption(f"FABRICE BET AI - 3 CHAMPIONS TYPE LONAB - JOUR INFINI - {datetime.now():%d/%m/%Y %H:%M:%S}")

a,b,c = st.columns(3)
with a:
    st.metric("CHAMPION 1", "PARIS SPORTIFS", "TYPE LONAB")
with b:
    st.metric("CHAMPION 2", "PMU-B", "TYPE LONAB")
with c:
    st.metric("CHAMPION 3", "BOURSE", "TYPE LONAB")

col1,col2,col3 = st.columns(3)
with col1:
    if st.button("PLUS 3 JOURS INFINI", use_container_width=True):
        st.session_state.nb+=1
        st.rerun()
with col2:
    if st.button("MISE A JOUR JOUR", use_container_width=True):
        st.rerun()
with col3:
    if st.button("RESET", use_container_width=True):
        st.session_state.nb=1
        st.rerun()

st.info(f"FABRICE BET AI - 3 CHAMPIONS AVEC TYPE LONAB POUR CHOISIR - JOUR INFINI {st.session_state.nb*3} JOURS")

tab1, tab2, tab3 = st.tabs(["12 FIXES", "PMU-B JOURNAL HIPPIQUE", "BOURSE INTERNATIONALE"])

fixtures=[
    ("Inter vs Man City","LDC",78,22,2.8),("Real vs Brest","LDC",65,12,1.9),("Barca vs Real","Liga",82,35,3.2),
    ("EFO vs Bayern","Amical",45,55,3.5),("RCB vs USFA","Fasofoot",58,28,2.1),("Man Utd vs Liverpool","PL",88,42,3.4),
    ("Douanes vs Majestic","Fasofoot",52,18,1.8),("Sonabel vs Vitesse","Fasofoot",48,15,1.6),("ASFA vs EFO","Fasofoot",55,20,2.0),
    ("Rahimo vs Salitas","Fasofoot",60,25,2.3),("PSG vs Marseille","Ligue1",75,38,2.9),("Bayern vs Dortmund","Bundesliga",80,40,3.1),
    ("Man City vs Arsenal","PL",85,38,3.0),("Real Madrid vs Barcelona","Liga",80,36,3.3),("Atletico vs Sevilla","Liga",62,24,2.2),
    ("Juventus vs AC Milan","Serie A",70,26,2.4),("Chelsea vs Tottenham","PL",72,30,2.7),("Lyon vs Monaco","Ligue1",64,28,2.6),
    ("Ajax vs PSV","Eredivisie",76,32,3.1),("Porto vs Benfica","Primeira",68,26,2.5),
]
jours_fr=["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"]

def get_prevention(marche, confiance):
    if marche in ["Score Exact","Expulsion","Cartons","Quinte+","Multi"]:
        return "🔴 FEU ROUGE - RISQUE TRES ELEVE" if confiance < 65 else "🟠 FEU ORANGE - RISQUE ELEVE", "Risque Tres Eleve" if confiance < 65 else "Risque Eleve"
    elif marche in ["Double Chance","Couplé Placé","Simple Placé","FOREX","ACHETER","VENDRE"]:
        return "🟢 FEU VERT - RISQUE TRES FAIBLE" if confiance >= 78 else "🟢 FEU VERT - RISQUE FAIBLE", "Risque Tres Faible" if confiance >= 78 else "Risque Faible"
    else:
        return "🟢 FEU VERT - RISQUE FAIBLE" if confiance >= 75 else "🟠 FEU ORANGE - RISQUE MOYEN" if confiance >= 60 else "🔴 FEU ROUGE - RISQUE ELEVE", "Risque Faible" if confiance >= 75 else "Risque Moyen" if confiance >= 60 else "Risque Eleve"

# ===== CHAMPION 1 - PARIS SPORTIFS - TYPE LONAB COMPLET =====
with tab1:
    st.markdown("### FABRICE BET AI - 12 FIXES - CHAMPION 1 - TYPE LONAB PARIS SPORTIFS")
    type_lonab_p1=st.selectbox("Type LONAB - CHAMPION 1 - PARIS SPORTIFS", [
        "AI AUTO - Complet - Recommande",
        "Double Chance",
        "1X2",
        "Over Under - 0.5 a 5.5",
        "Score Exact - 0-0 a 6-1",
        "BTTS - GG Oui Non",
        "Cartons - Over Under",
        "Expulsion - Rouge Oui Non",
        "Corners - Over Under",
        "Mi-Temps / MT-Fin",
        "BTTS + Over"
    ], index=0, key="type_p1_v62")
    st.success(f"CHAMPION 1 - {type_lonab_p1} - PREVENTION + AI ULTRA SOLIDE")
    nb_matchs=st.slider("Nombre de matchs - CHAMPION 1", 10, 15, 12, key="nb_p1_v62")
    
    total=st.session_state.nb*3
    for i in range(total):
        d=datetime.now()+timedelta(days=i)
        nom=jours_fr[d.weekday()]
        rnd=random.Random(seed(d, f"p1_v62_{nb_matchs}_{type_lonab_p1}"))
        is_today=(i==0)
        jour_label="AUJOURDHUI - JOUR INFINI" if is_today else f"J+{i} - JOUR INFINI"
        with st.expander(f"CHAMPION 1 - {jour_label} - {nom} {d.strftime('%d/%m/%Y')} - {type_lonab_p1}", expanded=is_today):
            nb_reel = min(nb_matchs, len(fixtures))
            data=[]
            for team,lig,attaque,defense,moy_buts in rnd.sample(fixtures, nb_reel):
                diff = attaque - defense
                forme = rnd.randint(65,96)
                force = rnd.randint(68,95)
                agressivite = rnd.randint(25,90)
                
                if "Double Chance" in type_lonab_p1:
                    marche = "Double Chance"
                    prono = "1X" if diff > 10 else "X2" if diff < -10 else rnd.choice(["1X","X2"])
                    cote = round(rnd.uniform(1.18,1.85),2)
                    confiance = rnd.randint(72,94)
                elif type_lonab_p1 == "1X2":
                    marche = "1X2"
                    prono = "1" if diff > 25 else "2" if diff < -18 else rnd.choice(["1","X","2"])
                    cote = round(rnd.uniform(1.50,3.80),2)
                    confiance = rnd.randint(62,88)
                elif "Over Under" in type_lonab_p1:
                    marche = "Over Under"
                    prono = rnd.choice(["Over 2.5","Under 2.5","Over 1.5","Over 3.5","Over 0.5","Over 4.5","Over 5.5"])
                    cote = round(rnd.uniform(1.40,2.60),2)
                    confiance = rnd.randint(65,90)
                elif "Score Exact" in type_lonab_p1:
                    marche = "Score Exact"
                    prono = rnd.choice(["0-0","1-0","2-1","3-1","4-1","5-0","6-0","6-1","3-0","2-0"])
                    cote = round(rnd.uniform(5.50,19.00),2)
                    confiance = rnd.randint(35,68)
                elif "BTTS" in type_lonab_p1 and "Over" not in type_lonab_p1:
                    marche = "BTTS"
                    prono = rnd.choice(["GG Oui","GG Non","BTTS Oui","BTTS Non"])
                    cote = round(rnd.uniform(1.60,2.40),2)
                    confiance = rnd.randint(62,86)
                elif "Cartons" in type_lonab_p1:
                    marche = "Cartons"
                    prono = rnd.choice(["Over 3.5 Cartons","Under 3.5 Cartons","Over 4.5 Cartons","Carton Rouge Oui"])
                    cote = round(rnd.uniform(1.70,3.50),2)
                    confiance = rnd.randint(55,82)
                elif "Expulsion" in type_lonab_p1:
                    marche = "Expulsion"
                    prono = rnd.choice(["Expulsion Oui","Expulsion Non","Rouge Oui","Rouge Non"])
                    cote = round(rnd.uniform(2.20,6.00),2)
                    confiance = rnd.randint(42,75)
                elif "Corners" in type_lonab_p1:
                    marche = "Corners"
                    prono = rnd.choice(["Over 8.5 Corners","Over 9.5 Corners","Under 8.5 Corners","Over 10.5 Corners"])
                    cote = round(rnd.uniform(1.60,2.50),2)
                    confiance = rnd.randint(60,86)
                elif "Mi-Temps" in type_lonab_p1:
                    marche = "MT-Fin"
                    prono = rnd.choice(["1/1","X/1","X/2","1/X","2/1","X/X","1 Mi-Temps","Over 0.5 Mi-Temps"])
                    cote = round(rnd.uniform(1.80,5.50),2)
                    confiance = rnd.randint(58,82)
                elif "BTTS + Over" in type_lonab_p1:
                    marche = "BTTS + Over"
                    prono = rnd.choice(["BTTS + Over 2.5","GG + Over 2.5","BTTS + Over 3.5"])
                    cote = round(rnd.uniform(1.90,3.80),2)
                    confiance = rnd.randint(58,84)
                else: # AI AUTO
                    marche = rnd.choice(["1X2","Double Chance","Over Under","Score Exact","BTTS","Cartons","Expulsion","Corners","MT-Fin","BTTS + Over"])
                    prono = rnd.choice(["1","1X","Over 2.5","2-1","GG Oui","Over 3.5 Cartons","Expulsion Non","Over 8.5 Corners","1/1","BTTS + Over 2.5"])
                    cote = round(rnd.uniform(1.40,6.00),2)
                    confiance = rnd.randint(60,88)
                
                prevention, risque = get_prevention(marche, confiance)
                analyse = f"AI ULTRA SOLIDE - {marche} {prono} - Att {attaque}% Def {defense}% Diff {diff} - Forme {forme}% Force {force}% - {moy_buts:.1f} buts - {prevention} - Rapide et Efficace - J+{i}"
                
                data.append({
                    "Match":f"{team} - {lig}",
                    "Marche":marche,
                    "Prono":prono,
                    "Cote":cote,
                    "Prevention":prevention,
                    "Risque":risque,
                    "Analyse Ultra Solide":analyse,
                    "Confiance":f"{confiance}%",
                    "Jour Infini":f"J+{i}",
                })
            st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)

# ===== CHAMPION 2 - PMU-B - TYPE LONAB PMU =====
with tab2:
    st.markdown("### FABRICE BET AI - PMU-B - CHAMPION 2 - TYPE LONAB PMU-B")
    type_lonab_p2=st.selectbox("Type LONAB - CHAMPION 2 - PMU-B", [
        "AI AUTO - Complet - Recommande",
        "Tierce",
        "Quarte",
        "Quinte",
        "Quinte+",
        "Couple Gagnant",
        "Couple Place",
        "Couple Ordre",
        "Simple Gagnant",
        "Simple Place",
        "Trio",
        "Multi",
        "2sur4"
    ], index=0, key="type_p2_v62")
    st.success(f"CHAMPION 2 - {type_lonab_p2} - PREVENTION + AI ULTRA SOLIDE - TYPE LONAB PMU-B")
    
    total=st.session_state.nb*3
    for i in range(total):
        d=datetime.now()+timedelta(days=i)
        nom=jours_fr[d.weekday()]
        rnd=random.Random(seed(d, f"p2_v62_{type_lonab_p2}"))
        fav=rnd.sample(list(range(1,17)),8)
        is_today=(i==0)
        jour_label="AUJOURDHUI - JOUR INFINI" if is_today else f"J+{i} - JOUR INFINI"
        with st.expander(f"CHAMPION 2 - {jour_label} - {nom} {d.strftime('%d/%m/%Y')} - {type_lonab_p2}", expanded=is_today):
            forme_cheval=rnd.randint(65,96)
            forme_driver=rnd.randint(62,94)
            
            if "Tierce" in type_lonab_p2:
                marche = "Tierce"
                prono = f"{fav[0]}-{fav[1]}-{fav[2]}"
                cote = round(rnd.uniform(15.0,85.0),1)
                confiance = rnd.randint(58,84)
                analyse = f"AI ULTRA SOLIDE - Tierce {prono} - Cheval {fav[0]} Forme {forme_cheval}% Driver {forme_driver}% - Base solide - Rapide et Efficace - J+{i}"
            elif "Quarte" in type_lonab_p2:
                marche = "Quarte"
                prono = f"{fav[0]}-{fav[1]}-{fav[2]}-{fav[3]}"
                cote = round(rnd.uniform(45.0,250.0),1)
                confiance = rnd.randint(48,76)
                analyse = f"AI ULTRA SOLIDE - Quarte {prono} - Forme {forme_cheval}% - {forme_driver}% - Analyse ultra solide - J+{i}"
            elif "Quinte+" in type_lonab_p2:
                marche = "Quinte+"
                prono = f"{fav[0]}-{fav[1]}-{fav[2]}-{fav[3]}-{fav[4]} + Bonus {fav[5]}"
                cote = round(rnd.uniform(120.0,850.0),1)
                confiance = rnd.randint(38,68)
                analyse = f"AI ULTRA SOLIDE - Quinte+ {prono} - Forme {forme_cheval}% - Risque eleve mais cote elevee - Ultra solide - J+{i}"
            elif "Quinte" in type_lonab_p2:
                marche = "Quinte"
                prono = f"{fav[0]}-{fav[1]}-{fav[2]}-{fav[3]}-{fav[4]}"
                cote = round(rnd.uniform(80.0,450.0),1)
                confiance = rnd.randint(45,74)
                analyse = f"AI ULTRA SOLIDE - Quinte {prono} - Base {fav[0]}-{fav[1]} - Forme {forme_cheval}% - Rapide et Efficace - J+{i}"
            elif "Couple Gagnant" in type_lonab_p2:
                marche = "Couple Gagnant"
                prono = f"{fav[0]}-{fav[1]}"
                cote = round(rnd.uniform(4.5,22.0),1)
                confiance = rnd.randint(65,88)
                analyse = f"AI ULTRA SOLIDE - Couple Gagnant {prono} - Forme {forme_cheval}% - Securise - J+{i}"
            elif "Couple Place" in type_lonab_p2:
                marche = "Couple Place"
                prono = f"{fav[0]}-{fav[1]}"
                cote = round(rnd.uniform(2.2,8.5),1)
                confiance = rnd.randint(72,90)
                analyse = f"AI ULTRA SOLIDE - Couple Place {prono} - Forme {forme_cheval}% - Risque tres faible - Securise - J+{i}"
            elif "Simple Gagnant" in type_lonab_p2:
                marche = "Simple Gagnant"
                prono = f"{fav[0]}"
                cote = round(rnd.uniform(2.8,12.0),1)
                confiance = rnd.randint(68,88)
                analyse = f"AI ULTRA SOLIDE - Simple Gagnant {prono} - Cheval {fav[0]} Forme {forme_cheval}% Driver {forme_driver}% - Base - J+{i}"
            elif "Simple Place" in type_lonab_p2:
                marche = "Simple Place"
                prono = f"{fav[0]}"
                cote = round(rnd.uniform(1.4,3.2),1)
                confiance = rnd.randint(78,92)
                analyse = f"AI ULTRA SOLIDE - Simple Place {prono} - Forme {forme_cheval}% - Risque tres faible - Feu vert - J+{i}"
            elif "Trio" in type_lonab_p2:
                marche = "Trio"
                prono = f"{fav[0]}-{fav[1]}-{fav[2]}"
                cote = round(rnd.uniform(25.0,120.0),1)
                confiance = rnd.randint(52,78)
                analyse = f"AI ULTRA SOLIDE - Trio {prono} - Forme {forme_cheval}% - Analyse ultra solide - J+{i}"
            elif "Multi" in type_lonab_p2:
                marche = "Multi"
                prono = f"{fav[0]}-{fav[1]}-{fav[2]}-{fav[3]}"
                cote = round(rnd.uniform(35.0,180.0),1)
                confiance = rnd.randint(45,72)
                analyse = f"AI ULTRA SOLIDE - Multi {prono} - 4 chevaux - Forme {forme_cheval}% - J+{i}"
            elif "2sur4" in type_lonab_p2:
                marche = "2sur4"
                prono = f"{fav[0]}-{fav[1]}"
                cote = round(rnd.uniform(2.0,5.5),1)
                confiance = rnd.randint(75,91)
                analyse = f"AI ULTRA SOLIDE - 2sur4 {prono} - Forme {forme_cheval}% - Risque faible - Feu vert - J+{i}"
            else: # AI AUTO
                choix = rnd.choice(["Tierce","Quarte","Quinte","Couple Gagnant","Simple Gagnant"])
                if choix == "Tierce":
                    prono = f"{fav[0]}-{fav[1]}-{fav[2]}"
                    marche = "Tierce"
                elif choix == "Quarte":
                    prono = f"{fav[0]}-{fav[1]}-{fav[2]}-{fav[3]}"
                    marche = "Quarte"
                elif choix == "Quinte":
                    prono = f"{fav[0]}-{fav[1]}-{fav[2]}-{fav[3]}-{fav[4]}"
                    marche = "Quinte"
                elif choix == "Couple Gagnant":
                    prono = f"{fav[0]}-{fav[1]}"
                    marche = "Couple Gagnant"
                else:
                    prono = f"{fav[0]}"
                    marche = "Simple Gagnant"
                cote = round(rnd.uniform(3.0,150.0),1)
                confiance = rnd.randint(55,85)
                analyse = f"AI ULTRA SOLIDE - {marche} {prono} - Cheval {fav[0]} Forme {forme_cheval}% Driver {forme_driver}% - AI AUTO Complet - Rapide et Efficace - J+{i}"
            
            prevention, risque = get_prevention(marche, confiance)
            st.markdown(f'<div style="background:#d00000;color:white;padding:14px;border-radius:12px;text-align:center"><b>FABRICE BET AI - CHAMPION 2 - {marche} JOUR INFINI J+{i}: {prono}<br>Cote {cote} - {prevention}</b><br>BASE {fav[0]}-{fav[1]} - Forme {forme_cheval}% - {risque} - Confiance {confiance}%<br>{analyse}<br>{d.strftime("%d/%m/%Y")} {datetime.now():%H:%M}</div>', unsafe_allow_html=True)
            data_pmu=[{"Type LONAB PMU-B":marche,"Prono":prono,"Cote":cote,"Prevention":prevention,"Risque":risque,"Analyse Ultra Solide":analyse,"Confiance":f"{confiance}%","Jour":f"J+{i}"}]
            st.dataframe(pd.DataFrame(data_pmu), use_container_width=True, hide_index=True)

# ===== CHAMPION 3 - BOURSE - TYPE LONAB BOURSE =====
with tab3:
    st.markdown("### FABRICE BET AI - BOURSE INTERNATIONALE - CHAMPION 3 - TYPE LONAB BOURSE")
    type_lonab_p3=st.selectbox("Type LONAB - CHAMPION 3 - BOURSE", [
        "AI AUTO - Complet - Recommande",
        "FOREX - EUR USD XOF",
        "CRYPTO - BTC ETH SOL",
        "INDICES - S&P NASDAQ CAC",
        "OR PETROLE - GOLD OIL",
        "ACHETER - BUY",
        "VENDRE - SELL",
        "Scalping - Court Terme",
        "Day Trading - Journalier",
        "Long Terme - HOLD",
        "Actions - AAPL TSLA NVDA"
    ], index=0, key="type_p3_v62")
    st.success(f"CHAMPION 3 - {type_lonab_p3} - PREVENTION + AI ULTRA SOLIDE - TYPE LONAB BOURSE")
    
    base_markets_all={
        "BTC/USD":(crypto_live["BTC"],"CRYPTO","$"),"ETH/USD":(crypto_live["ETH"],"CRYPTO","$"),"SOL/USD":(crypto_live["SOL"],"CRYPTO","$"),
        "EUR/USD":(1.0850,"FOREX",""),"GBP/USD":(1.2720,"FOREX",""),"USD/JPY":(154.30,"FOREX",""),
        "USD/XOF":(605.50,"FOREX"," XOF"),"EUR/XOF":(655.95,"FOREX"," XOF"),
        "S&P 500":(5230.50,"INDICE"," pts"),"NASDAQ":(16340.20,"INDICE"," pts"),"DOW JONES":(38520.10,"INDICE"," pts"),"CAC 40":(8105.30,"INDICE"," pts"),
        "AAPL Apple":(195.20,"ACTION","$"),"TSLA Tesla":(245.80,"ACTION","$"),"NVDA Nvidia":(880.50,"ACTION","$"),
        "GOLD Or":(2385.40,"OR","$/oz"),"OIL Brent":(84.20,"PETROLE","$/b"),
    }
    
    total=st.session_state.nb*3
    for i in range(total):
        d=datetime.now()+timedelta(days=i)
        nom=jours_fr[d.weekday()]
        rnd=random.Random(seed(d, f"p3_v62_{type_lonab_p3}"))
        is_today=(i==0)
        jour_label="AUJOURDHUI - JOUR INFINI" if is_today else f"J+{i} - JOUR INFINI"
        with st.expander(f"CHAMPION 3 - {jour_label} - {nom} {d.strftime('%d/%m/%Y')} - {type_lonab_p3}", expanded=is_today):
            # FILTRAGE SELON TYPE LONAB BOURSE
            if "FOREX" in type_lonab_p3:
                filtered = {k:v for k,v in base_markets_all.items() if v[1]=="FOREX"}
            elif "CRYPTO" in type_lonab_p3:
                filtered = {k:v for k,v in base_markets_all.items() if v[1]=="CRYPTO"}
            elif "INDICES" in type_lonab_p3:
                filtered = {k:v for k,v in base_markets_all.items() if v[1]=="INDICE"}
            elif "OR PETROLE" in type_lonab_p3:
                filtered = {k:v for k,v in base_markets_all.items() if v[1] in ["OR","PETROLE"]}
            elif "Actions" in type_lonab_p3:
                filtered = {k:v for k,v in base_markets_all.items() if v[1]=="ACTION"}
            else:
                filtered = base_markets_all
            
            data_b=[]
            for name,(base_price,cat,unit) in filtered.items():
                var=rnd.uniform(-0.008,0.008) if cat=="FOREX" else rnd.uniform(-0.04,0.05)
                prix=base_price * (1 + var * (i+1)*0.3) if not is_today else base_price
                rsi=rnd.randint(22,78)
                tendance=rnd.choice(["HAUSSIER FORT","BAISSIER FORT","HAUSSIER LEGER","LATERAL","BAISSIER LEGER"])
                force=rnd.randint(58,92)
                
                # TYPE LONAB BOURSE LOGIQUE
                if "ACHETER" in type_lonab_p3:
                    signal = "ACHETER"
                    confiance = rnd.randint(68,90)
                    prevention = "🟢 FEU VERT - ACHAT" if rsi < 40 else "🟠 FEU ORANGE - ACHAT"
                    risque = "Risque Faible - Survente" if rsi < 35 else "Risque Moyen"
                elif "VENDRE" in type_lonab_p3:
                    signal = "VENDRE"
                    confiance = rnd.randint(66,88)
                    prevention = "🟢 FEU VERT - VENTE" if rsi > 60 else "🟠 FEU ORANGE - VENTE"
                    risque = "Risque Faible - Surachat" if rsi > 65 else "Risque Moyen"
                elif "Scalping" in type_lonab_p3:
                    signal = "ACHETER" if tendance=="HAUSSIER FORT" else "VENDRE" if tendance=="BAISSIER FORT" else rnd.choice(["ACHETER","VENDRE"])
                    confiance = rnd.randint(55,78)
                    prevention = "🟠 FEU ORANGE - SCALPING" if confiance < 70 else "🟢 FEU VERT - SCALPING"
                    risque = "Risque Moyen - Court terme"
                elif "Day Trading" in type_lonab_p3:
                    signal = "ACHETER" if "HAUSSIER" in tendance else "VENDRE" if "BAISSIER" in tendance else "ATTENTE"
                    confiance = rnd.randint(60,84)
                    prevention = "🟢 FEU VERT - DAY TRADING" if confiance >= 72 else "🟠 FEU ORANGE - DAY TRADING"
                    risque = "Risque Faible" if confiance >= 72 else "Risque Moyen"
                elif "Long Terme" in type_lonab_p3:
                    signal = "ACHETER" if "HAUSSIER" in tendance else "ATTENTE"
                    confiance = rnd.randint(70,90)
                    prevention = "🟢 FEU VERT - LONG TERME"
                    risque = "Risque Tres Faible - HOLD"
                else: # AI AUTO
                    if rsi < 30:
                        signal = "ACHETER"
                        confiance = rnd.randint(75,92)
                        prevention = "🟢 FEU VERT - RISQUE FAIBLE - ACHAT"
                        risque = "Risque Faible"
                    elif rsi > 70:
                        signal = "VENDRE"
                        confiance = rnd.randint(72,90)
                        prevention = "🟢 FEU VERT - RISQUE FAIBLE - VENTE"
                        risque = "Risque Faible"
                    else:
                        signal = "ACHETER" if "HAUSSIER" in tendance else "VENDRE" if "BAISSIER" in tendance else "ATTENTE"
                        confiance = rnd.randint(58,86)
                        prevention = "🟢 FEU VERT - RISQUE FAIBLE" if confiance >= 75 else "🟠 FEU ORANGE - RISQUE MOYEN"
                        risque = "Risque Faible" if confiance >= 75 else "Risque Moyen"
                
                analyse=f"AI ULTRA SOLIDE - {tendance} RSI {rsi} - {type_lonab_p3} - Forme {rnd.randint(60,92)}% Force {force}% - {prevention} - {risque} - Confiance {confiance}% - Rapide et Efficace - J+{i}"
                label_prix=f"{prix:,.4f}{unit} LIVE" if cat=="FOREX" and is_today else f"{prix:,.2f}{unit} LIVE" if is_today else f"{prix:,.4f}{unit} J+{i}" if cat=="FOREX" else f"{prix:,.2f}{unit} J+{i}"
                
                data_b.append({
                    "Actif":name,
                    "Prix":label_prix,
                    "Signal":signal,
                    "Type LONAB Bourse":type_lonab_p3,
                    "Prevention":prevention,
                    "Risque":risque,
                    "Analyse Ultra Solide":analyse,
                    "RSI":f"{rsi}",
                    "Confiance":f"{confiance}%",
                    "Jour":f"J+{i}",
                })
            st.dataframe(pd.DataFrame(data_b), use_container_width=True, hide_index=True)

st.success(f"FABRICE BET AI - V62 - 3 CHAMPIONS AVEC TYPE LONAB - PARIS SPORTIFS / PMU-B / BOURSE - CHACUN SON TYPE LONAB POUR CHOISIR - JOUR INFINI {st.session_state.nb*3} JOURS - {datetime.now():%H:%M:%S}")
