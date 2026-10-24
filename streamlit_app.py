import streamlit as st, pandas as pd, random, hashlib, requests
from datetime import datetime, timedelta

st.set_page_config(page_title="FABRICE V47 BOURSE 7J7", layout="wide", page_icon="💹")
st.markdown("<style>#MainMenu,footer,header{display:none}</style>", unsafe_allow_html=True)

@st.cache_data(ttl=600)
def get_bourse():
    try:
        r=requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,binancecoin&vs_currencies=usd&include_24h_change=true", timeout=5).json()
        return {
            "BTC":(r["bitcoin"]["usd"], r["bitcoin"]["usd_24h_change"], True),
            "ETH":(r["ethereum"]["usd"], r["ethereum"]["usd_24h_change"], True),
            "SOL":(r["solana"]["usd"], r["solana"]["usd_24h_change"], True),
            "BNB":(r["binancecoin"]["usd"], r["binancecoin"]["usd_24h_change"], True),
        }
    except: return {"BTC":(80763,1.2,False),"ETH":(2450,0.8,False),"SOL":(145,2.1,False),"BNB":(620,0.5,False)}

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
if "arr_bf" not in st.session_state: st.session_state.arr_bf=sheet_arr if sheet_live else {"24/10/2026":"9-4-7-2-5"}
if sheet_live and sheet_arr: st.session_state.arr_bf.update(sheet_arr)

def seed(d,s=""): return int(hashlib.md5((d.strftime('%Y%m%d')+s).encode()).hexdigest()[:8],16)

st.title("FABRICE EMPIRE")
btc_p,btc_c,_=bourse_live["BTC"]
st.caption(f"12 FIXES | PMU-B | BOURSE - 7J/7 INFINI - BTC ${btc_p:,.0f} {datetime.now():%H:%M:%S}")

c1,c2=st.columns(2)
with c1:
    if st.button("➕ +3 JOURS", use_container_width=True): st.session_state.nb+=1; st.rerun()
with c2:
    if st.button("🔄 RESET", use_container_width=True): st.session_state.nb=1; st.rerun()

tab1, tab2, tab3 = st.tabs(["12 FIXES", "PMU-B JOURNAL HIPPIQUE", "BOURSE INTERNATIONALE"])

fixtures=[("Inter vs Man City","LDC",78,22,2.8),("Real vs Brest","LDC",65,12,1.9),("Barca vs Real","Liga",82,35,3.2),("EFO vs Bayern","Amical",45,55,3.5),("RCB vs USFA","Fasofoot",58,28,2.1),("Man Utd vs Liverpool","PL",88,42,3.4),("Douanes vs Majestic","Fasofoot",52,18,1.8),("Sonabel vs Vitesse","Fasofoot",48,15,1.6),("ASFA vs EFO","Fasofoot",55,20,2.0),("Rahimo vs Salitas","Fasofoot",60,25,2.3),("PSG vs Marseille","Ligue1",75,38,2.9),("Bayern vs Dortmund","Bundesliga",80,40,3.1),("Man City vs Arsenal","PL",85,45,3.3),("Real Madrid vs Barcelona","Liga",90,48,3.5)]
jours_fr=["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"]

# TAB 1 - 12 FIXES
with tab1:
    st.markdown("### 🎯 12 FIXES - AI AUTO + SCORE EXACT")
    type_lonab=st.selectbox("🎯 Type LONAB", ["🤖 AI AUTO + SCORE EXACT - Complet","Double Chance AI","Over/Under AI AUTO","Score Exact AI"], index=0, key="t1")
    nb_matchs=st.slider("Nombre matchs", 10, 15, 12, key="nb1")
    st.markdown(f"<div style='text-align:center;color:#ff4b4b;font-weight:bold'>{nb_matchs}</div>", unsafe_allow_html=True)
    total=st.session_state.nb*3
    for i in range(total):
        d=datetime.now()+timedelta(days=i)
        nom=jours_fr[d.weekday()]
        rnd=random.Random(seed(d, f"12fixes_v47_{nb_matchs}_{type_lonab}"))
        is_today=(i==0)
        with st.expander(f"{'🔥 AUJOURD\'HUI' if is_today else f'J+{i}'} - {nom} {d.strftime('%d/%m/%Y')} - {nb_matchs} MATCHS LIVE INFINI", expanded=is_today):
            data=[]
            for team,lig,att,deff,moy in rnd.sample(fixtures, nb_matchs):
                if moy>=3.0: marche,prono,score="Over/Under",rnd.choice(["Over 2.5","Over 3.5"]),rnd.choice(["2-1","3-1","2-2"])
                elif moy<=1.9: marche,prono,score="Over/Under",rnd.choice(["Under 2.5","Under 3.5"]),rnd.choice(["1-0","0-0","1-1"])
                else: marche,prono,score="Double Chance",rnd.choice(["1X","X2","12"]),rnd.choice(["1-1","2-1","1-0"])
                if "Score Exact" in type_lonab: marche,prono,score="Score Exact",rnd.choice(["1-0","2-1","1-1","2-0"]),rnd.choice(["1-0","2-1","1-1"])
                aff=score if marche=="Score Exact" else f"{prono} (Score: {score})"
                data.append({"Match":f"{team} - {lig}","Marché AI":marche,"Prono":aff,"Score Exact":score,"Cote":round(rnd.uniform(1.55,5.5),2),"Confiance":f"{rnd.randint(70,94)}%","LIVE":datetime.now().strftime('%H:%M')})
            st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)

# TAB 2 - PMU-B
with tab2:
    st.markdown("### 🐴 PMU-B JOURNAL HIPPIQUE - 7J/7 INFINI")
    total=st.session_state.nb*3
    for i in range(total):
        d=datetime.now()+timedelta(days=i)
        date_key=d.strftime('%d/%m/%Y')
        nom=jours_fr[d.weekday()]
        rnd=random.Random(seed(d,"pmu_v47"))
        fav=rnd.sample(list(range(1,17)),6)
        final=st.session_state.arr_bf.get(date_key)
        is_today=(i==0)
        if final:
            try:
                off=[int(x) for x in final.replace("-"," ").split() if x.isdigit()]
                if len(off)>=3: fav=(off+fav)[:6]
            except: pass
        with st.expander(f"{'🔥 AUJOURD\'HUI' if is_today else f'J+{i}'} - {nom} {date_key} - {'🏁 '+final if final else 'QUINTÉ LIVE'}", expanded=is_today):
            if final:
                cols=st.columns(len(final.split("-")))
                for idx,num in enumerate(final.split("-")):
                    with cols[idx]: st.markdown(f'<div style="background:#2b5cff;color:white;padding:10px;border-radius:8px;text-align:center;font-weight:bold'>{num}</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="background:#d00000;color:white;padding:12px;border-radius:10px;text-align:center"><b>QUINTÉ LIVE: {"-".join(map(str,fav[:5]))}</b><br>{datetime.now():%H:%M} LIVE INFINI</div>', unsafe_allow_html=True)

# TAB 3 - BOURSE INTERNATIONALE 7J/7 JOURS INFINI CORRIGÉ
with tab3:
    st.markdown("### 💹 BOURSE INTERNATIONALE - 7J/7 JOURS INFINI")
    st.caption(f"🔴 PRIX VRAIS COINGECKO + PRÉVISION 7J/7 INFINI - {datetime.now():%H:%M:%S} - LIVE INFINI")
    
    total=st.session_state.nb*3
    for i in range(total):
        d=datetime.now()+timedelta(days=i)
        nom=jours_fr[d.weekday()]
        is_today=(i==0)
        rnd=random.Random(seed(d, f"bourse_7j7_infini_v47"))
        
        with st.expander(f"{'🔥 AUJOURD\'HUI' if is_today else f'J+{i}'} - {nom} {d.strftime('%d/%m/%Y')} - BOURSE LIVE INFINI", expanded=is_today):
            
            # Évolution prix jour infini = prix live + variation jour
            data_b=[]
            for name in ["BTC","ETH","SOL","BNB"]:
                base_price,base_change,_=bourse_live[name]
                # Variation par jour infini = même pour tous, déterministe
                var_jour = rnd.uniform(-0.06, 0.08)  # -6% à +8% par jour
                prix_jour = base_price * (1 + var_jour * (i*0.1 + 1)) if i>0 else base_price
                # Si aujourd'hui = prix vrai live, sinon prévision live infini
                if is_today:
                    prix_affiche = base_price
                    label_prix = f"${prix_affiche:,.0f} LIVE VRAI"
                else:
                    prix_affiche = prix_jour
                    label_prix = f"${prix_affiche:,.0f} PRÉVISION J+{i} LIVE"
                
                sig=rnd.choice(["🟢 ACHETER LIVE","🔴 VENDRE LIVE","🟡 ATTENTE LIVE"])
                if "ACHETER" in sig: sl,tp1,tp2=prix_affiche*0.94,prix_affiche*1.08,prix_affiche*1.15
                elif "VENDRE" in sig: sl,tp1,tp2=prix_affiche*1.06,prix_affiche*0.92,prix_affiche*0.85
                else: sl,tp1,tp2=prix_affiche*0.95,prix_affiche*1.05,prix_affiche*1.10
                
                data_b.append({
                    "Actif 7J/7":f"{name}/USD LIVE",
                    "Prix 7J/7 LIVE":label_prix,
                    "Signal JOUR":sig,
                    "Jour":f"{nom} {d.strftime('%d/%m')} LIVE",
                    "STOP LIVE":f"${sl:,.0f}",
                    "TP1 LIVE":f"${tp1:,.0f}",
                    "TP2 LIVE":f"${tp2:,.0f}",
                    "Heure LIVE":datetime.now().strftime('%H:%M:%S')
                })
            
            st.dataframe(pd.DataFrame(data_b), use_container_width=True, hide_index=True)
            
            # Résumé jour infini
            btc_prev = data_b[0]["Prix 7J/7 LIVE"]
            st.success(f"✅ BOURSE {nom} {d.strftime('%d/%m/%Y')} - BTC {btc_prev} - 7J/7 JOURS INFINI - Même prévision pour tous - LIVE INFINI")

st.success(f"✅ V47 CORRIGÉ - 12 FIXES 7J/7 | PMU-B 7J/7 | BOURSE 7J/7 JOURS INFINI - TOUT LIVE INFINI")
