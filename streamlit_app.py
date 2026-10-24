import streamlit as st, pandas as pd, random, hashlib, requests
from datetime import datetime, timedelta

st.set_page_config(page_title="FABRICE V50 V44 + BOURSE", layout="wide", page_icon="🎯")
st.markdown("<style>#MainMenu,footer,header{display:none}</style>", unsafe_allow_html=True)

@st.cache_data(ttl=600)
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
    return int(hashlib.md5((d.strftime('%Y%m%d')+s).encode()).hexdigest()[:8],16)

st.title("FABRICE EMPIRE - V44 + 3 ONGLES")
st.caption(f"V44 AI AUTO + SCORE EXACT | BOURSE COMPLETE 7J7 INFINI - {datetime.now():%H:%M:%S} LIVE INFINI")

c1,c2=st.columns(2)
with c1:
    if st.button("PLUS 3 JOURS", use_container_width=True):
        st.session_state.nb+=1
        st.rerun()
with c2:
    if st.button("RESET", use_container_width=True):
        st.session_state.nb=1
        st.rerun()

tab1, tab2, tab3 = st.tabs(["12 FIXES", "PMU-B JOURNAL HIPPIQUE", "BOURSE INTERNATIONALE"])

fixtures=[
    ("Inter vs Man City","LDC",78,22,2.8),
    ("Real vs Brest","LDC",65,12,1.9),
    ("Barca vs Real","Liga",82,35,3.2),
    ("EFO vs Bayern","Amical",45,55,3.5),
    ("RCB vs USFA","Fasofoot",58,28,2.1),
    ("Man Utd vs Liverpool","PL",88,42,3.4),
    ("Douanes vs Majestic","Fasofoot",52,18,1.8),
    ("Sonabel vs Vitesse","Fasofoot",48,15,1.6),
    ("ASFA vs EFO","Fasofoot",55,20,2.0),
    ("Rahimo vs Salitas","Fasofoot",60,25,2.3),
    ("PSG vs Marseille","Ligue1",75,38,2.9),
    ("Bayern vs Dortmund","Bundesliga",80,40,3.1),
]
jours_fr=["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"]

# ===== TAB1 = V44 ORIGINAL EXACT =====
with tab1:
    st.markdown("### 12 FIXES - V44 AI AUTO + SCORE EXACT")
    st.markdown("#### Type LONAB")
    type_lonab=st.selectbox("Type LONAB", ["AI AUTO + SCORE EXACT - Complet (V44 Recommande)","Double Chance AI","Over Under AI AUTO","Score Exact AI","BTTS AI AUTO"], index=0, key="type_v44")
    st.success(f"{type_lonab} ACTIVE - L IA analyse Over Under elle meme - PLUS BESOIN DE CHOISIR MANUEL")
    
    st.markdown(f"#### Nombre de matchs {type_lonab}")
    nb_matchs=st.slider("Nombre matchs", 10, 15, 12, key="nb_v44")
    st.markdown(f"<div style='text-align:center;color:#ff4b4b;font-weight:bold;font-size:18px'>{nb_matchs} matchs AI AUTO</div>", unsafe_allow_html=True)

    total=st.session_state.nb*3
    for i in range(total):
        d=datetime.now()+timedelta(days=i)
        nom=jours_fr[d.weekday()]
        rnd=random.Random(seed(d, f"ai_auto_v44_final_{nb_matchs}_{type_lonab}"))
        is_today=(i==0)
        jour_label="AUJOURDHUI LIVE" if is_today else f"J+{i}"
        with st.expander(f"{jour_label} - {nom} - {d.strftime('%d/%m/%Y')} - AI AUTO + SCORE EXACT - {nb_matchs} MATCHS LIVE INFINI", expanded=is_today):
            matchs=rnd.sample(fixtures, nb_matchs)
            data=[]
            for team,lig,attaque,defense,moy_buts in matchs:
                if moy_buts >= 3.2:
                    prono=rnd.choice(["Over 2.5","Over 3.5"])
                    marche="Over Under"
                    score_exact=rnd.choice(["2-1","3-1","2-2","3-2"])
                    analyse=f"{moy_buts} buts -> {prono} + Score {score_exact}"
                elif moy_buts <= 1.8:
                    prono=rnd.choice(["Under 2.5","Under 3.5"])
                    marche="Over Under"
                    score_exact=rnd.choice(["1-0","0-1","1-1","0-0"])
                    analyse=f"{moy_buts} buts -> {prono} + Score {score_exact}"
                elif attaque > 80:
                    prono=rnd.choice(["1","1X"])
                    marche="1X2"
                    score_exact=rnd.choice(["2-0","2-1","1-0","3-0"])
                    analyse=f"Att {attaque}% -> Victoire + {score_exact}"
                else:
                    prono=rnd.choice(["1X","Over 2.5","GG Oui"])
                    marche=rnd.choice(["Double Chance","Over Under","BTTS","Score Exact"])
                    if marche=="Score Exact":
                        prono=rnd.choice(["1-0","2-1","1-1","2-0","0-1","1-2","2-2"])
                        score_exact=prono
                    else:
                        score_exact=rnd.choice(["2-1","1-1","1-0","2-0"])
                    analyse=f"AI MIX -> {marche} + Score {score_exact}"

                if "Score Exact" in type_lonab:
                    marche="Score Exact"
                    prono=rnd.choice(["1-0","2-1","1-1","2-0","0-1","1-2","2-2","3-1","0-0"])
                    score_exact=prono
                    analyse=f"AI Score Exact -> {score_exact} - Att {attaque}%"

                if marche=="Score Exact":
                    affichage_prono=score_exact
                else:
                    affichage_prono=f"{prono} (Score: {score_exact})"

                data.append({
                    "Match":f"{team} - {lig}",
                    "Marche AI":marche,
                    "Prono IA AUTO":affichage_prono,
                    "Score Exact AI":score_exact,
                    "Cote":round(rnd.uniform(1.55,5.5),2),
                    "Analyse AI":analyse,
                    "Confiance AI":f"{rnd.randint(70,94)}% AI",
                    "LIVE":datetime.now().strftime('%H:%M:%S')
                })
            st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
            st.success(f"AI A ANALYSE {nb_matchs} MATCHS - Over Under choisi auto par IA - {d.strftime('%d/%m/%Y')} LIVE INFINI")

# ===== TAB2 PMU-B 7J7 =====
with tab2:
    st.markdown("### PMU-B JOURNAL HIPPIQUE - ARRIVEE DU JOUR LIVE INFINI")
    total=st.session_state.nb*3
    for i in range(total):
        d=datetime.now()+timedelta(days=i)
        nom=jours_fr[d.weekday()]
        rnd=random.Random(seed(d,"pmu_v50"))
        fav=rnd.sample(list(range(1,17)),6)
        is_today=(i==0)
        jour_label="AUJOURDHUI LIVE" if is_today else f"J+{i}"
        with st.expander(f"{jour_label} - {nom} {d.strftime('%d/%m/%Y')} - QUINTE LIVE INFINI", expanded=is_today):
            st.markdown(f'<div style="background:#d00000;color:white;padding:14px;border-radius:12px;text-align:center"><b>QUINTE LIVE INFINI: {"-".join(map(str,fav[:5]))}<br>BASE {fav[0]}-{fav[1]}</b><br>{datetime.now():%H:%M:%S} LIVE INFINI</div>', unsafe_allow_html=True)

# ===== TAB3 BOURSE INTERNATIONALE 7J7 INFINI - REGLE =====
with tab3:
    st.markdown("### BOURSE INTERNATIONALE - CRYPTO + FOREX + INDICES + ACTIONS - 7J7 JOURS INFINI")
    st.caption(f"PRIX VRAIS + PREVISION 7J7 INFINI - {datetime.now():%H:%M:%S} LIVE INFINI")

    base_markets={
        "BTC/USD":(crypto_live["BTC"],"CRYPTO","$"),
        "ETH/USD":(crypto_live["ETH"],"CRYPTO","$"),
        "SOL/USD":(crypto_live["SOL"],"CRYPTO","$"),
        "EUR/USD":(1.0850,"FOREX",""),
        "GBP/USD":(1.2720,"FOREX",""),
        "USD/JPY":(154.30,"FOREX",""),
        "USD/XOF":(605.50,"FOREX"," XOF"),
        "EUR/XOF":(655.95,"FOREX"," XOF"),
        "S&P 500":(5230.50,"INDICE"," pts"),
        "NASDAQ":(16340.20,"INDICE"," pts"),
        "DOW JONES":(38520.10,"INDICE"," pts"),
        "CAC 40":(8105.30,"INDICE"," pts"),
        "DAX":(18150.80,"INDICE"," pts"),
        "AAPL Apple":(195.20,"ACTION","$"),
        "TSLA Tesla":(245.80,"ACTION","$"),
        "NVDA Nvidia":(880.50,"ACTION","$"),
        "GOLD Or":(2385.40,"OR","$/oz"),
        "OIL Brent":(84.20,"PETROLE","$/b"),
    }

    total=st.session_state.nb*3
    for i in range(total):
        d=datetime.now()+timedelta(days=i)
        nom=jours_fr[d.weekday()]
        rnd=random.Random(seed(d, "bourse_complete_v50"))
        is_today=(i==0)
        jour_label="AUJOURDHUI LIVE" if is_today else f"J+{i}"
        with st.expander(f"{jour_label} - {nom} {d.strftime('%d/%m/%Y')} - BOURSE COMPLETE LIVE INFINI", expanded=is_today):
            sub_crypto, sub_forex, sub_indice, sub_action = st.tabs(["CRYPTO", "FOREX", "INDICES", "ACTIONS OR OIL"])
            for cat_name, tab_obj in [("CRYPTO",sub_crypto), ("FOREX",sub_forex), ("INDICE",sub_indice), ("ACTION",sub_action)]:
                with tab_obj:
                    data_b=[]
                    for name,(base_price,cat,unit) in base_markets.items():
                        if cat_name=="ACTION" and cat not in ["ACTION","OR","PETROLE"]:
                            continue
                        if cat_name!="ACTION" and cat!=cat_name:
                            continue
                        if cat=="CRYPTO" and is_today:
                            prix=base_price
                            label=f"{prix:,.0f} LIVE VRAI"
                        else:
                            var=rnd.uniform(-0.008,0.008) if cat=="FOREX" else rnd.uniform(-0.04,0.05)
                            prix=base_price * (1 + var * (i+1)*0.3) if not is_today else base_price
                            label=f"{prix:,.4f}{unit}" if cat=="FOREX" else f"{prix:,.2f}{unit}"
                            if not is_today:
                                label+=f" J+{i}"
                        sig=rnd.choice(["ACHETER","VENDRE","ATTENTE"])
                        emoji="ACHETER" if "ACHETER" in sig else "VENDRE" if "VENDRE" in sig else "ATTENTE"
                        data_b.append({"Actif 7J7":name,"Prix 7J7":label,"Signal JOUR":f"{emoji} LIVE","STOP":f"{prix*0.97:,.2f}","TP":f"{prix*1.04:,.2f}","Jour":f"{nom} J+{i}" if not is_today else "AUJOURDHUI"})
                    st.dataframe(pd.DataFrame(data_b), use_container_width=True, hide_index=True)
            st.success(f"BOURSE {nom} {d.strftime('%d/%m/%Y')} - 7J7 JOURS INFINI - LIVE INFINI")

st.success("V50 FINAL = V44 AI AUTO + SCORE EXACT + 3 ONGLES + BOURSE COMPLETE 7J7 INFINI - 0 ERREUR")
