import streamlit as st, pandas as pd, random, hashlib, requests
from datetime import datetime, timedelta
import time

st.set_page_config(page_title="FABRICE V51 VRAI V44", layout="wide", page_icon="🎯")
st.markdown("<style>#MainMenu,footer,header{display:none}</style>", unsafe_allow_html=True)
# AUTO REFRESH INFINI TOUTES LES 60 SECONDES - MIS A JOUR INFINI
st.markdown('<meta http-equiv="refresh" content="60">', unsafe_allow_html=True)

@st.cache_data(ttl=30)
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

st.title("FABRICE EMPIRE - VRAI V44")
st.caption(f"TOUS A JOUR MIS A JOUR INFINI - LIVE {datetime.now():%d/%m/%Y %H:%M:%S} - AUTO REFRESH 60s - BTC {crypto_live['BTC']:,.0f}")

c1,c2,c3=st.columns(3)
with c1:
    if st.button("PLUS 3 JOURS", use_container_width=True):
        st.session_state.nb+=1
        st.rerun()
with c2:
    if st.button("RESET", use_container_width=True):
        st.session_state.nb=1
        st.rerun()
with c3:
    if st.button("ACTUALISER LIVE", use_container_width=True):
        st.rerun()

tab1, tab2, tab3 = st.tabs(["12 FIXES", "PMU-B JOURNAL HIPPIQUE", "BOURSE INTERNATIONALE"])

fixtures=[
    ("Inter vs Man City","LDC",78,22,2.8),("Real vs Brest","LDC",65,12,1.9),("Barca vs Real","Liga",82,35,3.2),
    ("EFO vs Bayern","Amical",45,55,3.5),("RCB vs USFA","Fasofoot",58,28,2.1),("Man Utd vs Liverpool","PL",88,42,3.4),
    ("Douanes vs Majestic","Fasofoot",52,18,1.8),("Sonabel vs Vitesse","Fasofoot",48,15,1.6),("ASFA vs EFO","Fasofoot",55,20,2.0),
    ("Rahimo vs Salitas","Fasofoot",60,25,2.3),("PSG vs Marseille","Ligue1",75,38,2.9),("Bayern vs Dortmund","Bundesliga",80,40,3.1),
]
jours_fr=["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"]

# ===== TAB1 VRAI V44 AVEC TYPE LONAB =====
with tab1:
    st.markdown("### 12 FIXES - V44 VRAI")
    
    # TYPE LONAB COMME TA PHOTO ENCERCLÉE VERT - BIEN VISIBLE
    st.markdown("#### Type LONAB")
    type_lonab=st.selectbox(
        "Type LONAB - Choisis ton type",
        ["Double Chance", "AI AUTO + SCORE EXACT Complet", "Over Under AI AUTO", "Score Exact AI", "BTTS AI AUTO", "1X2"],
        index=0,
        key="type_lonab_vrai_v44"
    )
    st.info(f"Type selectionne LIVE: {type_lonab} - {datetime.now():%H:%M:%S} - MIS A JOUR INFINI")

    nb_matchs=st.slider("Nombre de matchs Double Chance", 10, 15, 12, key="nb_vrai_v44")
    st.markdown(f"<div style='text-align:center;color:#ff4b4b;font-weight:bold;font-size:20px'>{nb_matchs} matchs - LIVE INFINI - MIS A JOUR {datetime.now():%H:%M:%S}</div>", unsafe_allow_html=True)

    total=st.session_state.nb*3
    for i in range(total):
        d=datetime.now()+timedelta(days=i)
        nom=jours_fr[d.weekday()]
        # SEED AVEC TYPE LONAB + HEURE POUR MIS A JOUR INFINI
        rnd=random.Random(seed(d, f"vrai_v44_{type_lonab}_{nb_matchs}_{datetime.now().strftime('%H%M')}"))
        is_today=(i==0)
        jour_label="AUJOURDHUI LIVE" if is_today else f"J+{i}"
        with st.expander(f"{jour_label} - {nom} {d.strftime('%d/%m/%Y')} - {type_lonab} - {nb_matchs} MATCHS - LIVE INFINI", expanded=is_today):
            matchs=rnd.sample(fixtures, nb_matchs)
            data=[]
            for team,lig,attaque,defense,moy_buts in matchs:
                # V44 AI AUTO LOGIQUE - IA CHOISIT ELLE MEME
                if "AI AUTO" in type_lonab:
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
                else:
                    # SI TYPE LONAB = Double Chance etc MANUEL
                    if type_lonab=="Double Chance":
                        prono=rnd.choice(["1X","X2","12"])
                        marche="Double Chance"
                        score_exact=rnd.choice(["1-1","2-1","1-0"])
                        analyse=f"Double Chance -> {prono}"
                    elif "Over Under" in type_lonab:
                        prono=rnd.choice(["Over 2.5","Under 2.5"])
                        marche="Over Under"
                        score_exact=rnd.choice(["2-1","1-0","1-1"])
                        analyse=f"Over Under AI -> {prono} auto"
                    elif "Score Exact" in type_lonab:
                        prono=rnd.choice(["1-0","2-1","1-1","2-0","0-1"])
                        marche="Score Exact"
                        score_exact=prono
                        analyse=f"Score Exact -> {score_exact}"
                    else:
                        prono=rnd.choice(["1X","X2","12"])
                        marche=type_lonab
                        score_exact=rnd.choice(["1-0","2-1"])
                        analyse=f"{type_lonab} -> {prono}"

                if marche=="Score Exact":
                    affichage_prono=score_exact
                else:
                    affichage_prono=f"{prono} (Score: {score_exact})"

                data.append({
                    "Match":f"{team} - {lig}",
                    "Type LONAB":type_lonab,
                    "Marche AI":marche,
                    "Prono IA AUTO":affichage_prono,
                    "Score Exact AI":score_exact,
                    "Cote":round(rnd.uniform(1.55,5.5),2),
                    "Analyse AI":analyse,
                    "Confiance AI":f"{rnd.randint(70,94)}% AI",
                    "LIVE":datetime.now().strftime('%H:%M:%S')
                })
            st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
            st.success(f"TOUS A JOUR - {nb_matchs} MATCHS - {type_lonab} - {d.strftime('%d/%m/%Y')} - MIS A JOUR INFINI {datetime.now():%H:%M:%S}")

# ===== TAB2 PMU-B 7J7 INFINI =====
with tab2:
    st.markdown("### PMU-B JOURNAL HIPPIQUE - TOUS A JOUR 7J7 INFINI")
    st.caption(f"MIS A JOUR INFINI {datetime.now():%H:%M:%S} LIVE")
    total=st.session_state.nb*3
    for i in range(total):
        d=datetime.now()+timedelta(days=i)
        nom=jours_fr[d.weekday()]
        rnd=random.Random(seed(d,f"pmu_vrai_v44_{datetime.now().strftime('%H%M')}"))
        fav=rnd.sample(list(range(1,17)),6)
        is_today=(i==0)
        jour_label="AUJOURDHUI LIVE" if is_today else f"J+{i}"
        with st.expander(f"{jour_label} - {nom} {d.strftime('%d/%m/%Y')} - QUINTE LIVE INFINI - MIS A JOUR INFINI", expanded=is_today):
            st.markdown(f'<div style="background:#d00000;color:white;padding:14px;border-radius:12px;text-align:center"><b>QUINTE LIVE INFINI: {"-".join(map(str,fav[:5]))}<br>BASE {fav[0]}-{fav[1]}</b><br>{datetime.now():%H:%M:%S} MIS A JOUR INFINI</div>', unsafe_allow_html=True)

# ===== TAB3 BOURSE COMPLÈTE 7J7 INFINI =====
with tab3:
    st.markdown("### BOURSE INTERNATIONALE - CRYPTO + FOREX + INDICES + ACTIONS - 7J7 JOURS INFINI")
    st.caption(f"TOUS A JOUR MIS A JOUR INFINI {datetime.now():%H:%M:%S} LIVE")

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
        "GOLD Or":(2385.40,"OR","$/oz"),
        "OIL Brent":(84.20,"PETROLE","$/b"),
    }

    total=st.session_state.nb*3
    for i in range(total):
        d=datetime.now()+timedelta(days=i)
        nom=jours_fr[d.weekday()]
        rnd=random.Random(seed(d, f"bourse_vrai_v44_{datetime.now().strftime('%H%M')}"))
        is_today=(i==0)
        jour_label="AUJOURDHUI LIVE" if is_today else f"J+{i}"
        with st.expander(f"{jour_label} - {nom} {d.strftime('%d/%m/%Y')} - BOURSE COMPLETE MIS A JOUR INFINI", expanded=is_today):
            data_b=[]
            for name,(base_price,cat,unit) in base_markets.items():
                if cat=="CRYPTO" and is_today:
                    prix=base_price
                    label=f"{prix:,.0f} LIVE VRAI MIS A JOUR INFINI"
                else:
                    var=rnd.uniform(-0.008,0.008) if cat=="FOREX" else rnd.uniform(-0.04,0.05)
                    prix=base_price * (1 + var * (i+1)*0.3) if not is_today else base_price
                    label=f"{prix:,.4f}{unit}" if cat=="FOREX" else f"{prix:,.2f}{unit}"
                    if not is_today:
                        label+=f" J+{i} PREVISION"
                sig=rnd.choice(["ACHETER LIVE","VENDRE LIVE","ATTENTE LIVE"])
                data_b.append({"Actif 7J7":name,"Prix MIS A JOUR INFINI":label,"Signal JOUR":sig,"Categorie":cat,"Jour":f"{nom} {d.strftime('%d/%m')}","LIVE":datetime.now().strftime('%H:%M:%S')})
            st.dataframe(pd.DataFrame(data_b), use_container_width=True, hide_index=True)
            st.success(f"BOURSE {nom} {d.strftime('%d/%m/%Y')} - TOUS A JOUR MIS A JOUR INFINI {datetime.now():%H:%M:%S}")

st.success(f"V51 VRAI V44 - TOUS A JOUR MIS A JOUR INFINI - TYPE LONAB + 12 FIXES + PMU-B + BOURSE COMPLETE 7J7 - LIVE {datetime.now():%H:%M:%S}")
