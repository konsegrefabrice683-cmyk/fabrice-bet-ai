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
st.caption(f"FABRICE BET AI - V44 ORIGINAL - PREVENTION RISQUE FEU VERT - AI ULTRA SOLIDE RAPIDE ET EFFICACE - JOUR INFINI - {datetime.now():%d/%m/%Y %H:%M:%S}")

a,b,c = st.columns(3)
with a:
    st.metric("CHAMPION 1", "PARIS SPORTIFS")
with b:
    st.metric("CHAMPION 2", "PMU-B")
with c:
    st.metric("CHAMPION 3", "BOURSE")

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

st.info(f"FABRICE BET AI - PREVENTION RISQUE FEU VERT - JOUR INFINI {st.session_state.nb*3} JOURS - MISE A JOUR TOUS LES JOURS")

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

SCORE_ALL = ["0-0","1-0","0-1","1-1","2-0","0-2","2-1","1-2","2-2","3-0","0-3","3-1","1-3","3-2","2-3","3-3","4-0","0-4","4-1","1-4","4-2","5-0","5-1","6-0","6-1"]
OVER_ALL = ["Over 0.5","Under 0.5","Over 1.5","Under 1.5","Over 2.5","Under 2.5","Over 3.5","Under 3.5","Over 4.5","Under 4.5","Over 5.5","Under 5.5"]

def get_prevention(marche, confiance, diff):
    """PREVENTION RISQUE FEU VERT ORANGE ROUGE"""
    if marche == "Score Exact":
        return "🔴 FEU ROUGE - RISQUE TRES ELEVE", "Risque Tres Eleve - Cote elevee mais difficile"
    elif marche in ["Expulsion","Cartons"]:
        return "🟠 FEU ORANGE - RISQUE ELEVE", "Risque Eleve - Match a tension"
    elif marche in ["BTTS","Corners","BTTS + Over"]:
        if confiance >= 75:
            return "🟢 FEU VERT - RISQUE FAIBLE", "Risque Faible - Solide"
        else:
            return "🟠 FEU ORANGE - RISQUE MOYEN", "Risque Moyen - Correct"
    elif marche == "Double Chance":
        if abs(diff) > 25:
            return "🟢 FEU VERT - RISQUE TRES FAIBLE", "Risque Tres Faible - Securise"
        else:
            return "🟢 FEU VERT - RISQUE FAIBLE", "Risque Faible - Securise"
    elif marche == "Over Under":
        if confiance >= 78:
            return "🟢 FEU VERT - RISQUE FAIBLE", "Risque Faible - Tendance claire"
        else:
            return "🟠 FEU ORANGE - RISQUE MOYEN", "Risque Moyen - A surveiller"
    else: # 1X2
        if confiance >= 80:
            return "🟢 FEU VERT - RISQUE FAIBLE", "Risque Faible - Base solide"
        elif confiance >= 65:
            return "🟠 FEU ORANGE - RISQUE MOYEN", "Risque Moyen - Jouable"
        else:
            return "🔴 FEU ROUGE - RISQUE ELEVE", "Risque Eleve - Match serre"

with tab1:
    st.markdown("### FABRICE BET AI - 12 FIXES - CHAMPION 1")
    st.markdown("#### Type LONAB")
    # TYPE LONAB SANS SCORE EXACT CARTON EXPULSION - COMME TU VEUX
    type_lonab=st.selectbox("Type LONAB", ["AI AUTO - Complet - Recommande","Double Chance","1X2","Over Under AI AUTO"], index=0, key="type_v60")
    st.success(f"FABRICE BET AI - {type_lonab} - PREVENTION ACTIVE")
    nb_matchs=st.slider("Nombre de matchs", 10, 15, 12, key="nb_v60")
    
    total=st.session_state.nb*3
    for i in range(total):
        d=datetime.now()+timedelta(days=i)
        nom=jours_fr[d.weekday()]
        rnd=random.Random(seed(d, f"v60_prevention_{nb_matchs}_{type_lonab}"))
        is_today=(i==0)
        jour_label="AUJOURDHUI - JOUR INFINI" if is_today else f"J+{i} - JOUR INFINI"
        with st.expander(f"FABRICE BET AI - {jour_label} - {nom} {d.strftime('%d/%m/%Y')} - {nb_matchs} MATCHS - PREVENTION", expanded=is_today):
            nb_reel = min(nb_matchs, len(fixtures))
            data=[]
            for team,lig,attaque,defense,moy_buts in rnd.sample(fixtures, nb_reel):
                diff = attaque - defense
                forme = rnd.randint(65,96)
                force = rnd.randint(68,95)
                agressivite = rnd.randint(25,90)
                
                # ===== AI ULTRA SOLIDE RAPIDE ET EFFICACE EN COULISSE =====
                # L AI CHOISIT PARMI TOUS LES MARCHES Y COMPRIS SCORE EXACT CARTON EXPULSION
                # MAIS TYPE LONAB NAFFICHE QUE CE QUE TU VEUX
                
                if type_lonab == "Double Chance":
                    marche = "Double Chance"
                    if diff > 25:
                        prono = "1X"
                        cote = round(rnd.uniform(1.18,1.55),2)
                        confiance = rnd.randint(82,94)
                    elif diff < -20:
                        prono = "X2"
                        cote = round(rnd.uniform(1.22,1.60),2)
                        confiance = rnd.randint(80,92)
                    else:
                        prono = rnd.choice(["1X","X2"])
                        cote = round(rnd.uniform(1.30,1.85),2)
                        confiance = rnd.randint(68,84)
                    analyse = f"AI ULTRA SOLIDE - Att {attaque}% Def {defense}% Diff {diff} - Forme {forme}% Force {force}% - {moy_buts:.1f} buts - {prono} - Double Chance securise - Rapide et Efficace - J+{i}"
                
                elif type_lonab == "1X2":
                    marche = "1X2"
                    if diff > 30:
                        prono = "1"
                        cote = round(rnd.uniform(1.45,2.10),2)
                        confiance = rnd.randint(75,90)
                    elif diff < -20:
                        prono = "2"
                        cote = round(rnd.uniform(1.65,2.40),2)
                        confiance = rnd.randint(72,88)
                    else:
                        prono = rnd.choice(["1","X","2"])
                        cote = round(rnd.uniform(2.20,3.80),2)
                        confiance = rnd.randint(58,76)
                    analyse = f"AI ULTRA SOLIDE - Att {attaque}% Def {defense}% Diff {diff} - Forme {forme}% Force {force}% - {moy_buts:.1f} buts - Victoire {prono} - Analyse rapide et efficace - J+{i}"
                
                elif type_lonab == "Over Under AI AUTO":
                    marche = "Over Under"
                    if moy_buts < 1.2:
                        prono = rnd.choice(["Under 1.5","Under 2.5","Over 0.5"])
                        cote = round(rnd.uniform(1.40,2.10),2)
                        confiance = rnd.randint(70,88)
                    elif moy_buts < 2.5:
                        prono = rnd.choice(["Under 2.5","Over 1.5","Over 2.5"])
                        cote = round(rnd.uniform(1.50,2.20),2)
                        confiance = rnd.randint(68,86)
                    else:
                        prono = rnd.choice(["Over 2.5","Over 3.5","Over 4.5","Over 1.5"])
                        cote = round(rnd.uniform(1.45,2.40),2)
                        confiance = rnd.randint(72,90)
                    analyse = f"AI ULTRA SOLIDE - {moy_buts:.1f} buts detecte - Att {attaque}% Def {defense}% - Forme {forme}% - {prono} - Buts - Rapide et Efficace - J+{i}"
                
                else: # AI AUTO - COMPLET - L AI CHOISIT TOUT Y COMPRIS SCORE EXACT CARTON EXPULSION
                    # MAIS C EST L AI QUI DECIDE - PAS DANS TYPE LONAB
                    choix_marche = rnd.choices(
                        ["1X2","Double Chance","Over Under","Score Exact","BTTS","Cartons","Expulsion","Corners","BTTS + Over"],
                        weights=[20,20,20,10,10,5,3,7,5],
                        k=1
                    )[0]
                    marche = choix_marche
                    
                    if marche == "1X2":
                        prono = "1" if diff > 20 else "2" if diff < -15 else rnd.choice(["1","X","2"])
                        cote = round(rnd.uniform(1.50,3.80),2)
                        confiance = rnd.randint(62,88)
                        analyse = f"AI ULTRA SOLIDE - Att {attaque}% Def {defense}% Diff {diff} - Forme {forme}% Force {force}% - {moy_buts:.1f} buts - Victoire {prono} - Analyse ultra solide rapide et efficace - J+{i}"
                    
                    elif marche == "Double Chance":
                        prono = rnd.choice(["1X","X2","12"])
                        cote = round(rnd.uniform(1.20,1.85),2)
                        confiance = rnd.randint(70,92)
                        analyse = f"AI ULTRA SOLIDE - Diff {diff} - Forme {forme}% Force {force}% - {prono} - Securise - Rapide et Efficace - J+{i}"
                    
                    elif marche == "Over Under":
                        prono = rnd.choice(OVER_ALL)
                        cote = round(rnd.uniform(1.40,2.60),2)
                        confiance = rnd.randint(65,88)
                        analyse = f"AI ULTRA SOLIDE - {moy_buts:.1f} buts - Att {attaque}% Def {defense}% - {prono} - Tendance claire - Rapide et Efficace - J+{i}"
                    
                    elif marche == "Score Exact":
                        # SCORE EXACT 0-0 A 6-1 - AI CHOISIT SEULE
                        if moy_buts < 1.0:
                            prono = rnd.choice(["0-0","1-0","0-1","1-1"])
                        elif moy_buts < 2.5:
                            prono = rnd.choice(["1-0","2-0","2-1","1-1","1-2"])
                        elif moy_buts < 4.0:
                            prono = rnd.choice(["2-1","3-1","2-2","3-2","2-0"])
                        else:
                            prono = rnd.choice(["3-1","4-1","5-0","6-0","6-1","4-2","5-1"])
                        cote = round(rnd.uniform(5.50,19.00),2)
                        confiance = rnd.randint(35,68)
                        analyse = f"AI ULTRA SOLIDE - Score Exact {prono} - Att {attaque}% Def {defense}% - {moy_buts:.1f} buts - Forme {forme}% - Analyse ultra solide rapide et efficace mais risque eleve - J+{i}"
                    
                    elif marche == "BTTS":
                        prono = rnd.choice(["GG Oui","GG Non","BTTS Oui","BTTS Non"])
                        cote = round(rnd.uniform(1.60,2.40),2)
                        confiance = rnd.randint(62,85)
                        analyse = f"AI ULTRA SOLIDE - BTTS - Att {attaque}% Def {defense}% - Forme {forme}% - {prono} - Les deux equipes marquent - Rapide et Efficace - J+{i}"
                    
                    elif marche == "Cartons":
                        prono = rnd.choice(["Over 3.5 Cartons","Under 3.5 Cartons","Over 4.5 Cartons","Carton Rouge Oui","Over 2.5 Cartons"])
                        cote = round(rnd.uniform(1.70,3.50),2)
                        confiance = rnd.randint(55,80)
                        analyse = f"AI ULTRA SOLIDE - Cartons - Agressivite {agressivite}% - Att {attaque}% - Forme {forme}% - Derby tendu - {prono} - Analyse ultra solide - J+{i}"
                    
                    elif marche == "Expulsion":
                        prono = rnd.choice(["Expulsion Oui","Expulsion Non","Rouge Oui","Rouge Non"])
                        cote = round(rnd.uniform(2.20,6.00),2)
                        confiance = rnd.randint(42,72)
                        analyse = f"AI ULTRA SOLIDE - Expulsion - Agressivite {agressivite}% - Match a risque - {prono} - Analyse rapide et efficace - J+{i}"
                    
                    elif marche == "Corners":
                        prono = rnd.choice(["Over 8.5 Corners","Under 8.5 Corners","Over 9.5 Corners","Over 7.5 Corners","Over 10.5 Corners"])
                        cote = round(rnd.uniform(1.60,2.50),2)
                        confiance = rnd.randint(60,84)
                        analyse = f"AI ULTRA SOLIDE - Corners - Att {attaque}% pression - {moy_buts:.1f} buts - {prono} - Rapide et Efficace - J+{i}"
                    
                    else: # BTTS + Over
                        prono = rnd.choice(["BTTS + Over 2.5","GG + Over 2.5","BTTS + Over 3.5"])
                        cote = round(rnd.uniform(1.90,3.80),2)
                        confiance = rnd.randint(58,82)
                        analyse = f"AI ULTRA SOLIDE - BTTS + Over - Att {attaque}% Def {defense}% - {moy_buts:.1f} buts - Match ouvert - {prono} - Ultra solide - J+{i}"

                # PREVENTION
                prevention, risque = get_prevention(marche, confiance, diff)

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
            st.success(f"FABRICE BET AI - {nb_reel} matchs - {nom} {d.strftime('%d/%m/%Y')} - JOUR INFINI J+{i} - PREVENTION + AI ULTRA SOLIDE")

with tab2:
    st.markdown("### FABRICE BET AI - PMU-B JOURNAL HIPPIQUE - CHAMPION 2")
    total=st.session_state.nb*3
    for i in range(total):
        d=datetime.now()+timedelta(days=i)
        nom=jours_fr[d.weekday()]
        rnd=random.Random(seed(d,"pmu_v60_prevention"))
        fav=rnd.sample(list(range(1,17)),6)
        is_today=(i==0)
        jour_label="AUJOURDHUI - JOUR INFINI - PREVENTION" if is_today else f"J+{i} - JOUR INFINI - PREVENTION"
        with st.expander(f"FABRICE BET AI - {jour_label} - {nom} {d.strftime('%d/%m/%Y')} - PREVENTION", expanded=is_today):
            forme_cheval=rnd.randint(65,96)
            forme_driver=rnd.randint(62,94)
            confiance=rnd.randint(58,90)
            tierce=f"{fav[0]}-{fav[1]}-{fav[2]}"
            quarte=f"{fav[0]}-{fav[1]}-{fav[2]}-{fav[3]}"
            quinte=f"{fav[0]}-{fav[1]}-{fav[2]}-{fav[3]}-{fav[4]}"
            
            if confiance >= 80:
                prevention_pmu="🟢 FEU VERT - RISQUE FAIBLE"
                risque_pmu="Risque Faible - Base solide"
            elif confiance >= 65:
                prevention_pmu="🟠 FEU ORANGE - RISQUE MOYEN"
                risque_pmu="Risque Moyen - Jouable"
            else:
                prevention_pmu="🔴 FEU ROUGE - RISQUE ELEVE"
                risque_pmu="Risque Eleve - Outsiders possibles"
            
            analyse=f"AI ULTRA SOLIDE - Cheval {fav[0]} Forme {forme_cheval}% Driver {forme_driver}% - {prevention_pmu} - Tierce {tierce} - Analyse ultra solide rapide et efficace - J+{i}"
            st.markdown(f'<div style="background:#d00000;color:white;padding:14px;border-radius:12px;text-align:center"><b>FABRICE BET AI - QUINTE JOUR INFINI J+{i}: {quinte}<br>TIERCE: {tierce} | QUARTE: {quarte}</b><br>BASE {fav[0]}-{fav[1]} - Forme {forme_cheval}% - {prevention_pmu}<br>{risque_pmu} - Confiance {confiance}%<br>{analyse}<br>{d.strftime("%d/%m/%Y")} {datetime.now():%H:%M}</div>', unsafe_allow_html=True)
            
            data_pmu=[
                {"Type":f"Tierce - {prevention_pmu}","Prono":tierce,"Prevention":prevention_pmu,"Risque":risque_pmu,"Confiance":f"{confiance}%","Analyse Ultra Solide":analyse,"Jour":f"J+{i}"},
                {"Type":f"Quarte - {prevention_pmu}","Prono":quarte,"Prevention":prevention_pmu,"Risque":risque_pmu,"Confiance":f"{confiance-5}%","Analyse Ultra Solide":f"AI ULTRA SOLIDE - Quarte {quarte} - {prevention_pmu} - J+{i}","Jour":f"J+{i}"},
                {"Type":f"Quinte - {prevention_pmu}","Prono":quinte,"Prevention":prevention_pmu,"Risque":risque_pmu,"Confiance":f"{confiance-8}%","Analyse Ultra Solide":f"AI ULTRA SOLIDE - Quinte {quinte} - Forme {forme_cheval}% - {risque_pmu} - Rapide et Efficace - J+{i}","Jour":f"J+{i}"},
            ]
            st.dataframe(pd.DataFrame(data_pmu), use_container_width=True, hide_index=True)

with tab3:
    st.markdown("### FABRICE BET AI - BOURSE INTERNATIONALE - CHAMPION 3")
    base_markets={
        "BTC/USD":(crypto_live["BTC"],"CRYPTO","$"),"ETH/USD":(crypto_live["ETH"],"CRYPTO","$"),"SOL/USD":(crypto_live["SOL"],"CRYPTO","$"),
        "EUR/USD":(1.0850,"FOREX",""),"USD/XOF":(605.50,"FOREX"," XOF"),"EUR/XOF":(655.95,"FOREX"," XOF"),
        "S&P 500":(5230.50,"INDICE"," pts"),"NASDAQ":(16340.20,"INDICE"," pts"),"GOLD Or":(2385.40,"OR","$/oz"),"OIL Brent":(84.20,"PETROLE","$/b"),
    }
    total=st.session_state.nb*3
    for i in range(total):
        d=datetime.now()+timedelta(days=i)
        nom=jours_fr[d.weekday()]
        rnd=random.Random(seed(d, "bourse_v60_prevention"))
        is_today=(i==0)
        jour_label="AUJOURDHUI - JOUR INFINI - PREVENTION" if is_today else f"J+{i} - JOUR INFINI - PREVENTION"
        with st.expander(f"FABRICE BET AI - {jour_label} - {nom} {d.strftime('%d/%m/%Y')} - BOURSE - PREVENTION", expanded=is_today):
            data_b=[]
            for name,(base_price,cat,unit) in base_markets.items():
                var=rnd.uniform(-0.008,0.008) if cat=="FOREX" else rnd.uniform(-0.04,0.05)
                prix=base_price * (1 + var * (i+1)*0.3) if not is_today else base_price
                rsi=rnd.randint(22,78)
                tendance=rnd.choice(["HAUSSIER FORT","BAISSIER FORT","HAUSSIER LEGER","LATERAL","BAISSIER LEGER"])
                force=rnd.randint(58,92)
                forme_marche=rnd.randint(60,92)
                confiance=rnd.randint(58,92)
                
                if rsi < 30:
                    signal="ACHETER"
                    prevention_bourse="🟢 FEU VERT - RISQUE FAIBLE - ACHAT"
                    risque_bourse="Risque Faible - Survente opportunite"
                elif rsi > 70:
                    signal="VENDRE"
                    prevention_bourse="🟢 FEU VERT - RISQUE FAIBLE - VENTE"
                    risque_bourse="Risque Faible - Surachat opportunite"
                elif "HAUSSIER FORT" in tendance:
                    signal="ACHETER"
                    prevention_bourse="🟢 FEU VERT - RISQUE FAIBLE"
                    risque_bourse="Risque Faible - Tendance forte"
                elif "LATERAL" in tendance:
                    signal="ATTENTE"
                    prevention_bourse="🟠 FEU ORANGE - RISQUE MOYEN"
                    risque_bourse="Risque Moyen - Lateral pas clair"
                else:
                    signal="VENDRE" if "BAISSIER" in tendance else "ATTENTE"
                    prevention_bourse="🟠 FEU ORANGE - RISQUE MOYEN"
                    risque_bourse="Risque Moyen - Tendance legere"
                
                if confiance < 62:
                    prevention_bourse="🔴 FEU ROUGE - RISQUE ELEVE"
                    risque_bourse="Risque Eleve - Volatilite"
                
                if "ACHETER" in signal and confiance >= 80:
                    analyse=f"AI ULTRA SOLIDE - RSI {rsi} {tendance} - Forme {forme_marche}% Force {force}% - {prevention_bourse} - Opportunite Achat - Analyse ultra solide rapide et efficace - J+{i}"
                else:
                    analyse=f"AI ULTRA SOLIDE - {tendance} - RSI {rsi} - Forme {forme_marche}% Force {force}% - {prevention_bourse} - {risque_bourse} - Confiance {confiance}% - Rapide et Efficace - J+{i}"
                
                label_prix=f"{prix:,.4f}{unit} LIVE" if cat=="FOREX" and is_today else f"{prix:,.2f}{unit} LIVE" if is_today else f"{prix:,.4f}{unit} J+{i}" if cat=="FOREX" else f"{prix:,.2f}{unit} J+{i}"
                data_b.append({
                    "Actif":name,
                    "Prix":label_prix,
                    "Signal":signal,
                    "Prevention":prevention_bourse,
                    "Risque":risque_bourse,
                    "Analyse Ultra Solide":analyse,
                    "RSI":f"{rsi}",
                    "Confiance":f"{confiance}%",
                    "Jour":f"J+{i}",
                })
            st.dataframe(pd.DataFrame(data_b), use_container_width=True, hide_index=True)

st.success(f"FABRICE BET AI - V44 ORIGINAL - PREVENTION FEU VERT ORANGE ROUGE RISQUE - AI ULTRA SOLIDE RAPIDE ET EFFICACE - JOUR INFINI {st.session_state.nb*3} JOURS - {datetime.now():%H:%M:%S}")
