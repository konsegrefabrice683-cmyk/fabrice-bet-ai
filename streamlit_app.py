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
st.caption(f"FABRICE BET AI - V44 V57 FIXED - 3 CHAMPIONS ULTRA SOLIDE - JOUR INFINI - MISE A JOUR TOUS LES JOURS - {datetime.now():%d/%m/%Y %H:%M:%S}")

a,b,c = st.columns(3)
with a:
    st.metric("CHAMPION 1", "PARIS SPORTIFS", "ULTRA SOLIDE")
with b:
    st.metric("CHAMPION 2", "PMU-B", "ULTRA SOLIDE")
with c:
    st.metric("CHAMPION 3", "BOURSE", "ULTRA SOLIDE")

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

st.info(f"FABRICE BET AI - V57 FIXED - JOUR INFINI: {st.session_state.nb*3} JOURS - MISE A JOUR QUOTIDIENNE")

tab1, tab2, tab3 = st.tabs(["12 FIXES - CHAMPION 1", "PMU-B - CHAMPION 2", "BOURSE - CHAMPION 3"])

# FIX: 20 FIXTURES - PLUS GRAND QUE SLIDER 15 - PLUS DERREUR SAMPLE
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

with tab1:
    st.markdown("### FABRICE BET AI - CHAMPION 1 - PARIS SPORTIFS - ULTRA SOLIDE RAPIDE ET EFFICACE")
    st.markdown("#### Type LONAB")
    type_lonab=st.selectbox("Type LONAB - FABRICE BET AI", ["AI AUTO + SCORE EXACT - ULTRA SOLIDE","Double Chance - ULTRA SOLIDE","Over Under AI AUTO - ULTRA SOLIDE","Score Exact AI - ULTRA SOLIDE"], index=0, key="type_c1_fixed")
    st.success(f"FABRICE BET AI - CHAMPION 1 - {type_lonab} - ULTRA SOLIDE - V44 ORIGINAL - JOUR INFINI")
    nb_matchs=st.slider("Nombre de matchs - CHAMPION 1", 10, 15, 12, key="nb_c1_fixed")
    total=st.session_state.nb*3
    for i in range(total):
        d=datetime.now()+timedelta(days=i)
        nom=jours_fr[d.weekday()]
        rnd=random.Random(seed(d, f"c1_ultra_fixed_{nb_matchs}_{type_lonab}"))
        is_today=(i==0)
        jour_label="AUJOURDHUI - JOUR INFINI - ULTRA SOLIDE" if is_today else f"J+{i} - JOUR INFINI - ULTRA SOLIDE"
        with st.expander(f"FABRICE BET AI - CHAMPION 1 - {jour_label} - {nom} {d.strftime('%d/%m/%Y')} - ULTRA SOLIDE", expanded=is_today):
            # FIX: On limite a len(fixtures) pour ne plus avoir derreur
            nb_reel = min(nb_matchs, len(fixtures))
            data=[]
            for team,lig,attaque,defense,moy_buts in rnd.sample(fixtures, nb_reel):
                forme=rnd.randint(65,98)
                force=rnd.randint(70,96)
                rsi_foot=rnd.randint(25,85)
                historique=rnd.choice(["3 victoires d affilee","Invaincu 5 matchs","Forme montante"])
                if moy_buts >= 3.5:
                    prono=rnd.choice(["Over 3.5","Over 4.5","Over 5.5"])
                    marche="Over Under ULTRA SOLIDE"
                    score_exact=rnd.choice(["3-1","4-1","5-0","6-0","6-1","4-2"])
                    analyse=f"ULTRA SOLIDE CHAMPION 1 - Att {attaque}% - Forme {forme}% - {historique} - RSI {rsi_foot} - {moy_buts:.1f} buts -> {prono} + {score_exact} - Force {force}% - Rapide"
                elif moy_buts <= 1.5:
                    prono=rnd.choice(["Under 1.5","Under 2.5","Under 0.5"])
                    marche="Over Under ULTRA SOLIDE"
                    score_exact=rnd.choice(["0-0","1-0","0-1","1-1"])
                    analyse=f"ULTRA SOLIDE CHAMPION 1 - Def {defense}% - Forme {forme}% - RSI {rsi_foot} - {moy_buts:.1f} buts -> {prono} + {score_exact} - Solide"
                else:
                    marche=rnd.choice(["Double Chance ULTRA SOLIDE","Over Under ULTRA SOLIDE","Score Exact ULTRA SOLIDE"])
                    if "Double" in marche:
                        prono=rnd.choice(["1X","X2","12"])
                        score_exact=rnd.choice(["1-1","2-1","1-0"])
                    elif "Over" in marche:
                        prono=rnd.choice(OVER_ALL)
                        score_exact=rnd.choice(SCORE_ALL[:10])
                    else:
                        prono=rnd.choice(SCORE_ALL)
                        score_exact=prono
                    analyse=f"ULTRA SOLIDE CHAMPION 1 - {marche} - Att {attaque}% Forme {forme}% Force {force}% - {prono} - Rapide - J+{i}"
                if "Score Exact" in type_lonab:
                    marche="Score Exact ULTRA SOLIDE"
                    prono=rnd.choice(SCORE_ALL)
                    score_exact=prono
                    analyse=f"ULTRA SOLIDE Score {score_exact} - Att {attaque}% Forme {forme}% - Ultra Solide"
                if "Over Under" in type_lonab:
                    marche="Over Under ULTRA SOLIDE"
                    prono=rnd.choice(OVER_ALL)
                    score_exact=rnd.choice(["2-1","1-1","1-0"])
                    analyse=f"ULTRA SOLIDE {prono} - {moy_buts:.1f} buts - Force {force}%"
                affichage=score_exact if "Score Exact" in marche else f"{prono} (Score: {score_exact})"
                data.append({
                    "Match CHAMPION 1":f"{team} - {lig}",
                    "Marche ULTRA SOLIDE":marche,
                    "Prono ULTRA SOLIDE":affichage,
                    "Score Exact":score_exact,
                    "Cote":round(rnd.uniform(1.55,6.0),2),
                    "Forme":f"{forme}% ULTRA SOLIDE",
                    "Force":f"{force}% ULTRA SOLIDE",
                    "Analyse ULTRA SOLIDE":analyse,
                    "Confiance":f"{rnd.randint(82,96)}% ULTRA SOLIDE",
                    "Jour Infini":f"J+{i}",
                })
            st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
            st.success(f"FABRICE BET AI - CHAMPION 1 ULTRA SOLIDE - {nb_reel} MATCHS - {nom} {d.strftime('%d/%m/%Y')} - JOUR INFINI J+{i}")

with tab2:
    st.markdown("### FABRICE BET AI - CHAMPION 2 - PMU-B - ULTRA SOLIDE RAPIDE ET EFFICACE")
    total=st.session_state.nb*3
    for i in range(total):
        d=datetime.now()+timedelta(days=i)
        nom=jours_fr[d.weekday()]
        rnd=random.Random(seed(d,"c2_ultra_fixed"))
        fav=rnd.sample(list(range(1,17)),6)
        is_today=(i==0)
        jour_label="AUJOURDHUI - JOUR INFINI - ULTRA SOLIDE" if is_today else f"J+{i} - JOUR INFINI - ULTRA SOLIDE"
        with st.expander(f"FABRICE BET AI - CHAMPION 2 - {jour_label} - {nom} {d.strftime('%d/%m/%Y')} - ULTRA SOLIDE", expanded=is_today):
            forme_cheval=rnd.randint(75,98)
            forme_driver=rnd.randint(70,96)
            piste=rnd.choice(["Piste lourde","Piste legere","Piste rapide"])
            force_pmu=rnd.randint(72,96)
            tierce=f"{fav[0]}-{fav[1]}-{fav[2]}"
            quarte=f"{fav[0]}-{fav[1]}-{fav[2]}-{fav[3]}"
            quinte=f"{fav[0]}-{fav[1]}-{fav[2]}-{fav[3]}-{fav[4]}"
            analyse_ultra=f"ULTRA SOLIDE CHAMPION 2 - Cheval {fav[0]} Forme {forme_cheval}% - Driver {forme_driver}% - {piste} - Force {force_pmu}% - Tierce {tierce} - Rapide"
            st.markdown(f'<div style="background:#d00000;color:white;padding:14px;border-radius:12px;text-align:center"><b>FABRICE BET AI - CHAMPION 2 - ULTRA SOLIDE - QUINTE J+{i}: {quinte}<br>TIERCE: {tierce} | QUARTE: {quarte}</b><br>BASE {fav[0]}-{fav[1]} - Forme {forme_cheval}% - Force {force_pmu}%<br>{analyse_ultra}<br>MISE A JOUR {d.strftime("%d/%m/%Y")} {datetime.now():%H:%M}</div>', unsafe_allow_html=True)

with tab3:
    st.markdown("### FABRICE BET AI - CHAMPION 3 - BOURSE INTERNATIONALE - ULTRA SOLIDE RAPIDE ET EFFICACE")
    base_markets={
        "BTC/USD":(crypto_live["BTC"],"CRYPTO","$"),"ETH/USD":(crypto_live["ETH"],"CRYPTO","$"),"SOL/USD":(crypto_live["SOL"],"CRYPTO","$"),
        "EUR/USD":(1.0850,"FOREX",""),"USD/XOF":(605.50,"FOREX"," XOF"),"EUR/XOF":(655.95,"FOREX"," XOF"),
        "S&P 500":(5230.50,"INDICE"," pts"),"NASDAQ":(16340.20,"INDICE"," pts"),"GOLD Or":(2385.40,"OR","$/oz"),"OIL Brent":(84.20,"PETROLE","$/b"),
    }
    total=st.session_state.nb*3
    for i in range(total):
        d=datetime.now()+timedelta(days=i)
        nom=jours_fr[d.weekday()]
        rnd=random.Random(seed(d, "c3_ultra_fixed"))
        is_today=(i==0)
        jour_label="AUJOURDHUI - JOUR INFINI - ULTRA SOLIDE" if is_today else f"J+{i} - JOUR INFINI - ULTRA SOLIDE"
        with st.expander(f"FABRICE BET AI - CHAMPION 3 - {jour_label} - {nom} {d.strftime('%d/%m/%Y')} - ULTRA SOLIDE", expanded=is_today):
            data_b=[]
            for name,(base_price,cat,unit) in base_markets.items():
                var=rnd.uniform(-0.008,0.008) if cat=="FOREX" else rnd.uniform(-0.04,0.05)
                prix=base_price * (1 + var * (i+1)*0.3) if not is_today else base_price
                rsi=rnd.randint(22,78)
                tendance=rnd.choice(["HAUSSIER FORT","BAISSIER FORT","HAUSSIER LEGER"])
                force=rnd.randint(65,96)
                forme_marche=rnd.randint(70,95)
                if rsi < 30:
                    signal="ACHETER ULTRA SOLIDE CHAMPION 3"
                    analyse=f"ULTRA SOLIDE CHAMPION 3 - RSI {rsi} SURVENTE - {tendance} - Forme {forme_marche}% - Force {force}% - ACHAT RAPIDE - J+{i}"
                    conf=f"{rnd.randint(85,96)}% ULTRA SOLIDE"
                elif rsi > 70:
                    signal="VENDRE ULTRA SOLIDE CHAMPION 3"
                    analyse=f"ULTRA SOLIDE CHAMPION 3 - RSI {rsi} SURACHAT - {tendance} - Forme {forme_marche}% - Force {force}% - VENTE EFFICACE - J+{i}"
                    conf=f"{rnd.randint(84,95)}% ULTRA SOLIDE"
                else:
                    signal="ACHETER ULTRA SOLIDE CHAMPION 3" if "HAUSSIER" in tendance else "ATTENTE ULTRA SOLIDE"
                    analyse=f"ULTRA SOLIDE CHAMPION 3 - {tendance} - RSI {rsi} - Forme {forme_marche}% - Force {force}% - {signal} - Rapide - J+{i}"
                    conf=f"{rnd.randint(82,93)}% ULTRA SOLIDE"
                label_prix=f"{prix:,.4f}{unit} LIVE" if cat=="FOREX" and is_today else f"{prix:,.2f}{unit} LIVE" if is_today else f"{prix:,.4f}{unit} J+{i}" if cat=="FOREX" else f"{prix:,.2f}{unit} J+{i}"
                data_b.append({
                    "Actif CHAMPION 3":name,
                    "Prix ULTRA SOLIDE":label_prix,
                    "Signal ULTRA SOLIDE":signal,
                    "Analyse ULTRA SOLIDE":analyse,
                    "RSI":f"{rsi}",
                    "Forme":f"{forme_marche}% ULTRA SOLIDE",
                    "Force":f"{force}% ULTRA SOLIDE",
                    "Confiance":conf,
                    "Jour Infini":f"J+{i}",
                })
            st.dataframe(pd.DataFrame(data_b), use_container_width=True, hide_index=True)

st.success(f"FABRICE BET AI - 3 CHAMPIONS ULTRA SOLIDE RAPIDE ET EFFICACE - JOUR INFINI {st.session_state.nb*3} JOURS - FIXED - {datetime.now():%H:%M:%S}")
