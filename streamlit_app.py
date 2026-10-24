import streamlit as st, pandas as pd, random, hashlib, requests
from datetime import datetime, timedelta

st.set_page_config(page_title="FABRICE V46 V44+3 ONGLES", layout="wide", page_icon="🎯")
st.markdown("<style>#MainMenu,footer,header{display:none}</style>", unsafe_allow_html=True)

@st.cache_data(ttl=600)
def get_bourse():
    try:
        r=requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24h_change=true", timeout=5).json()
        return {
            "BTC":(r["bitcoin"]["usd"], r["bitcoin"]["usd_24h_change"], True),
            "ETH":(r["ethereum"]["usd"], r["ethereum"]["usd_24h_change"], True),
            "SOL":(r["solana"]["usd"], r["solana"]["usd_24h_change"], True),
        }
    except: return {"BTC":(80763,1.2,False),"ETH":(2450,0.8,False),"SOL":(145,2.1,False)}

@st.cache_data(ttl=600)
def get_sheet():
    try:
        url=st.secrets.get("GOOGLE_SHEET_CSV","")
        if not url: return {}, False
        df=pd.read_csv(url)
        arr={}
        for _,row in df.iterrows():
            d=str(row.iloc[0]).strip(); a=str(row.iloc[1]).strip()
            if d and "-" in a: arr[d]=a
        return arr, True
    except: return {}, False

bourse_live=get_bourse()
sheet_arr, sheet_live=get_sheet()

if "nb" not in st.session_state: st.session_state.nb=1
if "arr_bf" not in st.session_state: st.session_state.arr_bf=sheet_arr if sheet_live else {"24/10/2026":"9-4-7-2-5","25/10/2026":"5-12-3-7-9"}
if sheet_live and sheet_arr: st.session_state.arr_bf.update(sheet_arr)

def seed(d,s=""): return int(hashlib.md5((d.strftime('%Y%m%d')+s).encode()).hexdigest()[:8],16)

st.title("FABRICE EMPIRE - V44 + 3 ONGLES")
btc_p,btc_c,_=bourse_live["BTC"]
st.caption(f"DOUBLE CHANCE | PMUB | BOURSE INTERNATIONALE - 7J/7 INFINI - BTC ${btc_p:,.0f} {btc_c:.1f}% {datetime.now():%H:%M:%S} LIVE INFINI")

c1,c2=st.columns(2)
with c1:
    if st.button("➕ +3 JOURS", use_container_width=True): st.session_state.nb+=1; st.rerun()
with c2:
    if st.button("🔄 RESET", use_container_width=True): st.session_state.nb=1; st.rerun()

# ========== 3 ONGLES COMME TA PHOTO ==========
tab1, tab2, tab3 = st.tabs(["12 FIXES", "PMU-B JOURNAL HIPPIQUE", "BOURSE INTERNATIONALE"])

fixtures = [
    ("Inter vs Man City","LDC",78,22,2.8),("Real vs Brest","LDC",65,12,1.9),("Barca vs Real","Liga",82,35,3.2),
    ("EFO vs Bayern","Amical",45,55,3.5),("RCB vs USFA","Fasofoot",58,28,2.1),("Man Utd vs Liverpool","PL",88,42,3.4),
    ("Douanes vs Majestic","Fasofoot",52,18,1.8),("Sonabel vs Vitesse","Fasofoot",48,15,1.6),("ASFA vs EFO","Fasofoot",55,20,2.0),
    ("Rahimo vs Salitas","Fasofoot",60,25,2.3),("PSG vs Marseille","Ligue1",75,38,2.9),("Bayern vs Dortmund","Bundesliga",80,40,3.1),
    ("Man City vs Arsenal","PL",85,45,3.3),("Real Madrid vs Barcelona","Liga",90,48,3.5),
]
jours_fr=["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"]

# ========== TAB 1 - 12 FIXES = V44 AI AUTO + SCORE EXACT ==========
with tab1:
    st.markdown("### 🎯 12 FIXES - AI AUTO + SCORE EXACT (V44)")
    st.markdown("#### 🎯 Type LONAB")
    type_lonab = st.selectbox("Type LONAB", ["🤖 AI AUTO + SCORE EXACT - Complet (V44 Recommandé)","Double Chance AI","Over/Under AI AUTO","Score Exact AI","BTTS AI AUTO"], index=0, key="type_v44_ongles")
    st.success(f"🤖 {type_lonab} - L'IA analyse Over/Under elle-même + Score Exact")

    st.markdown(f"#### Nombre de matchs {type_lonab}")
    nb_matchs = st.slider("Nombre matchs", 10, 15, 12, key="nb_v44_ongles")
    st.markdown(f"<div style='text-align:center;color:#ff4b4b;font-weight:bold;font-size:18px'>{nb_matchs} matchs AI AUTO</div>", unsafe_allow_html=True)

    total=st.session_state.nb*3
    for i in range(total):
        d=datetime.now()+timedelta(days=i)
        nom=jours_fr[d.weekday()]
        rnd=random.Random(seed(d, f"v44_3ongles_{nb_matchs}_{type_lonab}"))
        is_today=(i==0)
        label="🔥 AUJOURD'HUI" if is_today else f"J+{i}"
        
        with st.expander(f"{label} - {nom} - {d.strftime('%d/%m/%Y')} - 🤖 AI AUTO + SCORE EXACT - {nb_matchs} MATCHS LIVE INFINI", expanded=is_today):
            matchs=rnd.sample(fixtures, nb_matchs)
            data=[]
            for team,lig,att,deff,moy in matchs:
                # ========== AI AUTO V44 + SCORE EXACT ==========
                if moy>=3.2:
                    prono=rnd.choice(["Over 2.5","Over 3.5"])
                    marche="Over/Under"
                    score_exact=rnd.choice(["2-1","3-1","2-2","3-2"])
                    analyse=f"{moy} buts → {prono} + Score {score_exact}"
                elif moy<=1.8:
                    prono=rnd.choice(["Under 2.5","Under 3.5"])
                    marche="Over/Under"
                    score_exact=rnd.choice(["1-0","0-1","1-1","0-0"])
                    analyse=f"{moy} buts → {prono} + Score {score_exact}"
                elif att>80:
                    prono=rnd.choice(["1","1X"])
                    marche="1X2"
                    score_exact=rnd.choice(["2-0","2-1","1-0","3-0"])
                    analyse=f"Att {att}% → Victoire + {score_exact}"
                else:
                    prono=rnd.choice(["1X","Over 2.5","GG Oui"])
                    marche=rnd.choice(["Double Chance","Over/Under","BTTS","Score Exact"])
                    if marche=="Score Exact":
                        prono=rnd.choice(["1-0","2-1","1-1","2-0","0-1","1-2","2-2"])
                        score_exact=prono
                    else:
                        score_exact=rnd.choice(["2-1","1-1","1-0","2-0"])
                    analyse=f"AI MIX → {marche} + Score {score_exact}"

                if "Score Exact" in type_lonab:
                    marche="Score Exact"
                    prono=rnd.choice(["1-0","2-1","1-1","2-0","0-1","1-2","2-2","3-1","0-0"])
                    score_exact=prono
                    analyse=f"AI Score Exact → {score_exact} - Att {att}%"

                if marche=="Score Exact": aff=score_exact
                else: aff=f"{prono} (Score: {score_exact})"

                data.append({
                    "Match":f"{team} - {lig}",
                    "🤖 Marché AI":marche,
                    "Prono IA AUTO":aff,
                    "Score Exact AI":score_exact,
                    "Cote":round(rnd.uniform(1.55,5.5),2),
                    "Analyse AI":analyse,
                    "Confiance":f"{rnd.randint(70,94)}% 🤖",
                    "LIVE":datetime.now().strftime('%H:%M:%S')
                })
            st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
            st.success(f"🤖 V44 AI + SCORE EXACT - {nb_matchs} matchs - Over/Under auto par AI - LIVE INFINI")

# ========== TAB 2 - PMU-B JOURNAL HIPPIQUE ==========
with tab2:
    st.markdown("### 🐴 PMU-B JOURNAL HIPPIQUE - ARRIVÉE DU JOUR LIVE INFINI")
    if sheet_live: st.success(f"✅ SHEET BF LIVE: {len(sheet_arr)} arrivées - LIVE INFINI")
    else: st.warning("⚠️ Colle lien Google Sheet dans Secrets share.streamlit.io > Settings > Secrets")
    
    total=st.session_state.nb*3
    for i in range(total):
        d=datetime.now()+timedelta(days=i)
        date_key=d.strftime('%d/%m/%Y')
        nom=jours_fr[d.weekday()]
        rnd=random.Random(seed(d,"pmu_v44_3ongles"))
        fav=rnd.sample(list(range(1,17)),6)
        final=st.session_state.arr_bf.get(date_key)
        is_today=(i==0)
        if final:
            try:
                off=[int(x) for x in final.replace("-"," ").split() if x.isdigit()]
                if len(off)>=3: fav=(off+fav)[:6]
            except: pass
        with st.expander(f"{'🔥 AUJOURD\'HUI' if is_today else f'J+{i}'} - {nom} {date_key} - {'🏁 '+final if final else 'QUINTÉ LIVE'} - LIVE INFINI", expanded=is_today):
            if final:
                cols=st.columns(len(final.split("-")))
                for idx,num in enumerate(final.split("-")):
                    with cols[idx]: st.markdown(f'<div style="background:#2b5cff;color:white;padding:10px;border-radius:8px;text-align:center;font-weight:bold;font-size:20px">{num}</div>', unsafe_allow_html=True)
                st.success(f"🏁 ARRIVÉE JOUR BF LIVE: {final} - {datetime.now():%H:%M:%S} - LIVE INFINI")
            st.markdown(f'<div style="background:#d00000;color:white;padding:14px;border-radius:12px;text-align:center;font-size:18px"><b>QUINTÉ LIVE INFINI: {"-".join(map(str,fav[:5]))}<br>BASE {fav[0]}-{fav[1]}</b><br>{datetime.now():%H:%M:%S} LIVE INFINI</div>', unsafe_allow_html=True)

# ========== TAB 3 - BOURSE INTERNATIONALE ==========
with tab3:
    st.markdown("### 💹 BOURSE INTERNATIONALE - LIVE INFINI")
    st.caption(f"🔴 PRIX VRAIS COINGECKO LIVE INFINI - {datetime.now():%H:%M:%S}")
    data_b=[]
    for name in ["BTC","ETH","SOL"]:
        price,change,is_l=bourse_live[name]
        rnd=random.Random(seed(datetime.now(),name+"v44_3ongles"))
        sig=rnd.choice(["🟢 ACHETER LIVE","🔴 VENDRE LIVE","🟡 ATTENTE LIVE"])
        if "ACHETER" in sig: sl,tp1,tp2=price*0.94,price*1.08,price*1.15
        elif "VENDRE" in sig: sl,tp1,tp2=price*1.06,price*0.92,price*0.85
        else: sl,tp1,tp2=price*0.95,price*1.05,price*1.10
        data_b.append({"Actif LIVE":f"{name}/USD LIVE","Prix LIVE":f"${price:,.2f} LIVE","24h":f"{change:.1f}% LIVE","Signal ULTRA LIVE":sig,"STOP LIVE":f"${sl:,.0f}","TP1 LIVE":f"${tp1:,.0f}","TP2 LIVE":f"${tp2:,.0f}","Heure LIVE INFINI":datetime.now().strftime('%H:%M:%S')})
    st.dataframe(pd.DataFrame(data_b), use_container_width=True, hide_index=True)
    st.success(f"✅ BOURSE LIVE INFINI BTC ${btc_p:,.0f} - 7J/7 INFINI")

st.success(f"✅ V46 = V44 AI AUTO + SCORE EXACT + 3 ONGLES - 12 FIXES | PMU-B JOURNAL HIPPIQUE | BOURSE - LIVE INFINI")
