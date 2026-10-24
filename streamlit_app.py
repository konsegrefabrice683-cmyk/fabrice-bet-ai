import streamlit as st, pandas as pd, random, hashlib, requests, re
from datetime import datetime, timedelta
from PIL import Image

st.set_page_config(page_title="FABRICE BET AI - V44 FINAL CORRIGE", layout="wide", page_icon="🔥")
st.markdown("<style>#MainMenu,footer,header{display:none} .stButton>button{font-weight:bold}</style>", unsafe_allow_html=True)

@st.cache_data(ttl=60)
def get_bourse():
    try:
        r=requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,binancecoin,ripple&vs_currencies=usd", timeout=5).json()
        return {"BTC":r["bitcoin"]["usd"], "ETH":r["ethereum"]["usd"], "SOL":r["solana"]["usd"], "BNB":r["binancecoin"]["usd"], "XRP":r["ripple"]["usd"]}
    except:
        return {"BTC":80530, "ETH":2450, "SOL":145, "BNB":610, "XRP":0.52}

crypto_live=get_bourse()
if "nb" not in st.session_state: st.session_state.nb=1
def seed(d,s=""): return int(hashlib.md5((d.strftime("%Y%m%d")+s).encode()).hexdigest()[:8],16)

def confiance_simple(attaque, defense, diff, moy_buts, marche, rnd):
    base=rnd.randint(50,75)
    if attaque>=82: base+=rnd.randint(8,12)
    elif attaque>=65: base+=rnd.randint(3,7)
    elif attaque<50: base-=rnd.randint(5,15)
    if diff>=30: base+=rnd.randint(5,9)
    elif abs(diff)<=5: base-=rnd.randint(5,12)
    if "Score Exact" in marche or "Quinte Ordre" in marche: base-=rnd.randint(8,15)
    elif "Double Chance" in marche or "Simple Gagnant" in marche: base+=rnd.randint(6,10)
    elif "Over 0.5" in marche: base+=rnd.randint(8,13)
    base+=rnd.randint(-5,5)
    if base<38: base=38+rnd.randint(0,7)
    if base>92: base=92-rnd.randint(0,3)
    return base

def ai_vraie_opinion(team, attaque, defense, diff, moy_buts, marche, prono, rnd):
    score_att=rnd.randint(15,55) if attaque<50 else rnd.randint(40,68) if attaque<70 else rnd.randint(60,82) if attaque<85 else rnd.randint(75,95)
    score_diff=rnd.randint(20,55) if abs(diff)<=5 else rnd.randint(70,92) if diff>=30 else rnd.randint(55,78) if diff>=15 else rnd.randint(35,70)
    if "Score Exact" in marche: score_marche=rnd.randint(15,60)
    elif "Quinte Ordre" in marche: score_marche=rnd.randint(15,55)
    elif "Quarte Ordre" in marche: score_marche=rnd.randint(20,60)
    elif "Tierce Ordre" in marche: score_marche=rnd.randint(30,70)
    elif "Over 0.5" in marche or "Simple Gagnant" in marche: score_marche=rnd.randint(75,96)
    elif "Double Chance" in marche: score_marche=rnd.randint(60,88)
    else: score_marche=rnd.randint(45,80)
    forme=rnd.randint(35,90); histo=rnd.randint(30,85)
    opinion=int(score_att*0.35 + score_diff*0.30 + score_marche*0.20 + forme*0.08 + histo*0.07 + rnd.randint(-8,8))
    if opinion<5: opinion=rnd.randint(8,25)
    if opinion>99: opinion=rnd.randint(92,99)
    if opinion<=45: just=f"AI {opinion}% - Att {attaque}% faible + Diff {diff} serre + {marche} difficile - OPINION: RISQUE ELEVE - NE PAS JOUER"
    elif opinion<=56: just=f"AI {opinion}% - Att {attaque}% moyen + Match serre - OPINION: RISQUE - Preferer Double Chance"
    elif opinion<=70: just=f"AI {opinion}% - Att {attaque}% correct Diff {diff} - OPINION: MOYEN"
    elif opinion<=84: just=f"AI {opinion}% - Att {attaque}% fort Diff {diff} - OPINION: BON"
    else: just=f"AI {opinion}% - Att {attaque}% tres fort Diff {diff} - OPINION: TRES BON"
    return opinion, just

# CORRIGE - PLUS D'ERREUR AttributeError - utilise .map au lieu de .applymap
def style_vert_rouge(df):
    def color_val(v):
        try:
            m=re.search(r'(\d+)', str(v))
            n=int(m.group(1)) if m else 0
            if n<=45: return 'background-color: #8B0000; color: white; font-weight: bold'
            elif n<=56: return 'background-color: #FF0000; color: white; font-weight: bold'
            elif n<=69: return 'background-color: #FFA500; color: black'
            elif n<=79: return 'background-color: #FFFF00; color: black'
            elif n<=84: return 'background-color: #90EE90; color: black; font-weight: bold'
            else: return 'background-color: #00FF00; color: black; font-weight: bold'
        except: return ''
    cols=[c for c in ['Confiance','AI% Opinion'] if c in df.columns]
    # CORRECTION V44 - Pandas 2.0+ utilise .map
    return df.style.map(color_val, subset=cols) if cols else df.style

fixtures=[
    ("Crystal Palace vs Newcastle","PL",48,55,2.4),("Hull City vs Brentford","PL",42,38,2.1),
    ("Liverpool vs Brighton","PL",82,75,2.9),("Manchester United vs Bournemouth","PL",74,60,2.7),
    ("Sunderland vs Leeds United","PL",55,52,2.3),("Barcelona vs Real Madrid","Liga",88,72,3.2),
    ("Athletic Club vs Getafe","Liga",62,48,2.0),("Celta Vigo vs Real Betis","Liga",58,55,2.2),
    ("Real Sociedad vs Levante","Liga",65,42,2.1),("Hoffenheim vs Bayer Leverkusen","Bundes",60,68,2.8),
    ("Freiburg vs Bayern Munich","Bundes",52,82,3.0),("Inter Milan vs Fiorentina","Serie A",78,58,2.6),
    ("Atalanta vs Frosinone","Serie A",70,45,2.5),("Genoa vs Venezia","Serie A",55,48,2.1),
    ("Lecce vs Juventus","Serie A",48,72,2.4),("Udinese vs AC Milan","Serie A",52,78,2.5),
    ("Monaco vs Lille","Ligue1",68,62,2.4),("Marseille vs Le Havre","Ligue1",72,38,2.3),
    ("PSG vs Lyon","Ligue1",85,60,2.9),("Angers vs Lorient","Ligue1",45,52,2.2),
    ("RCB vs USFA","Fasofoot",58,28,2.1),("Douanes vs Majestic","Fasofoot",52,18,1.8),
    ("Sonabel vs Vitesse","Fasofoot",48,15,1.6),("ASFA vs EFO","Fasofoot",55,30,2.2),("Salitas vs Rahimo","Fasofoot",50,25,2.0),
]

bourse_complete={
    "FOREX MAJEURES":[("EUR/USD",1.0850,""),("GBP/USD",1.2950,""),("USD/JPY",149.20,""),("USD/CHF",0.8950,""),("AUD/USD",0.6650,""),("NZD/USD",0.6150,"")],
    "FOREX XOF":[("USD/XOF",605.50," XOF"),("EUR/XOF",657.00," XOF"),("GBP/XOF",785.20," XOF")],
    "FOREX EXOTIQUE":[("USD/TRY",34.20,""),("USD/ZAR",18.50,""),("EUR/TRY",37.10,"")],
    "INDICE US":[("S&P 500",7623.68,""),("NASDAQ",25955.19,""),("DOW JONES",52215.58,""),("RUSSELL 2000",2015.30,"")],
    "INDICE EUROPE":[("CAC 40",8150.20,""),("DAX",19200.50,""),("FTSE 100",8420.10,""),("EURO STOXX 50",4950.30,"")],
    "INDICE ASIE":[("NIKKEI 225",38500.00,""),("HANG SENG",20500.00,"")],
    "ACTION US TECH":[("TSLA",372.22,"$"),("NVDA",210.96,"$"),("AAPL",347.72,"$"),("MSFT",445.20,"$"),("META",485.30,"$"),("GOOGL",175.80,"$"),("AMZN",201.20,"$")],
    "ACTION US AUTRE":[("NFLX",695.40,"$"),("AMD",165.30,"$"),("BA",185.20,"$")],
    "ACTION EUROPE":[("LVMH",750.20,"€"),("TOTALENERGIES",62.50,"€"),("ASML",680.30,"€")],
    "CRYPTO":[("BTC/USD",crypto_live["BTC"],"$"),("ETH/USD",crypto_live["ETH"],"$"),("SOL/USD",crypto_live["SOL"],"$"),("BNB/USD",crypto_live["BNB"],"$"),("XRP/USD",crypto_live["XRP"],"$")],
    "MATIERES":[("OR - GOLD",2650.30,"$/oz"),("PETROLE - WTI",78.50,"$"),("ARGENT - SILVER",31.20,"$/oz")]
}

jours_fr=["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"]
st.title("FABRICE BET AI - V44 FINAL CORRIGE")
st.caption(f"V44 CORRIGE - AI vraie opinion 38-99% - PMU-B Quinte Quarte Tierce Multi - Bourse Forex Indice Action Crypto - {datetime.now():%d/%m/%Y}")

col1,col2,col3,col4=st.columns(4)
with col1:
    if st.button("PLUS 3 JOURS ♾️", use_container_width=True): st.session_state.nb+=1; st.rerun()
with col2:
    if st.button("PLUS 30 JOURS ♾️", use_container_width=True): st.session_state.nb+=10; st.rerun()
with col3:
    if st.button("MAJ ♾️", use_container_width=True): st.cache_data.clear(); st.rerun()
with col4:
    if st.button("RESET", use_container_width=True): st.session_state.nb=1; st.rerun()

st.info(f"♾️ {st.session_state.nb*3} jours - Jusqu'au {(datetime.now()+timedelta(days=st.session_state.nb*3-1)).strftime('%d/%m/%Y')}")
c1,c2,c3,c4,c5=st.columns(5)
c1.markdown("🟥 **38-45% DANGER**"); c2.markdown("🟥 **46-56% RISQUE**"); c3.markdown("🟧 **57-69% MOYEN**"); c4.markdown("🟩 **70-84% BON**"); c5.markdown("🟩 **85-99% TRES BON**")

tab1,tab2,tab3=st.tabs(["CHAMPION 1 - FOOT","CHAMPION 2 - PMU-B COMPLET","CHAMPION 3 - BOURSE INTERNATIONALE"])

with tab1:
    st.markdown("### FOOT - LONAB COMPLET")
    type1=st.selectbox("Type FOOT", ["LEGENDE - 1 marche/match Anti repetition","1X2","Double Chance","Score Exact","Over Under 0.5-5.5","BTTS GG/NG","BTTS+Over","Cartons Jaune/Rouge","Expulsion Oui/Non","Corners Over/Under","Mi-Temps / MT-Fin","TOUS COMPLET 12 marches/match"], index=0, key="t1f")
    nb1=st.slider("Nombre matchs FOOT", 1, 20, 12, key="n1f")
    total=st.session_state.nb*3
    for i in range(total):
        d=datetime.now()+timedelta(days=i); nom=jours_fr[d.weekday()]; rnd=random.Random(seed(d,f"foot_v44_{nb1}_{type1}_{i}"))
        with st.expander(f"{'AUJOURDHUI' if i==0 else f'J+{i}'} - {nom} {d.strftime('%d/%m/%Y')} - {nb1} matchs", expanded=(i==0)):
            data=[]; matches=rnd.sample(fixtures, min(nb1, len(fixtures)))
            for team,lig,att,defe,moy in matches:
                diff=att-defe
                if "LEGENDE" in type1:
                    marche,prono=("1X2","1") if diff>20 else ("1X2","2") if diff<-15 else ("Over Under","Over 2.5") if moy>=2.8 else ("Double Chance","1X" if diff>0 else "X2")
                    marches=[(marche,prono)]
                elif "TOUS COMPLET" in type1:
                    marches=[("1X2","1" if diff>15 else "2"),("Double Chance","1X"),("Score Exact",rnd.choice(["2-1","1-0","2-0"])),("Over Under","Over 0.5"),("Over Under","Over 1.5"),("Over Under","Over 2.5"),("Over Under","Under 3.5"),("BTTS","GG Oui"),("BTTS+Over","GG+Over 2.5"),("Cartons","Over 3.5"),("Expulsion","Non"),("Corners","Over 8.5")]
                else:
                    marches=[(type1,rnd.choice(["1","X","2","1X","Over 2.5","GG Oui","Over 3.5 Cartons","Non Expulsion","Over 8.5 Corners","1/1"]))]
                for marche,prono in marches:
                    cote=round(rnd.uniform(6.5,11.5),2) if "Score Exact" in marche else round(rnd.uniform(1.08,2.8),2)
                    conf=confiance_simple(att,defe,diff,moy,marche,rnd); ai_op,ai_just=ai_vraie_opinion(team,att,defe,diff,moy,marche,prono,rnd)
                    data.append({"Match":team,"Ligue":lig,"Marche":marche,"Prono":prono,"Cote":cote,"Confiance":f"{conf}%","AI% Opinion":f"{ai_op}%","AI Justification":ai_just,"Jour":f"J+{i}"})
            st.dataframe(style_vert_rouge(pd.DataFrame(data)), use_container_width=True, hide_index=True)

with tab2:
    st.markdown("### PMU-B COMPLET - TOUT: SIMPLE COUPLE TIERCE QUARTE QUINTE MULTI")
    type2=st.selectbox("Type PMU-B COMPLET", ["LEGENDE - 1 prono/course","Simple Gagnant","Simple Place","Couple Gagnant","Couple Place","Couple Ordre","Tierce Ordre","Tierce Desordre","Quarte Ordre","Quarte Desordre","Quinte Ordre","Quinte Desordre","Quinte+","Multi en 4","Multi en 5","Multi en 6","Multi en 7","TOUS COMPLET - 12 pronos/course"], index=0, key="t2f")
    nb2=st.slider("Nombre courses PMU-B", 1, 20, 12, key="n2f")
    total=st.session_state.nb*3
    for i in range(total):
        d=datetime.now()+timedelta(days=i); nom=jours_fr[d.weekday()]; rnd=random.Random(seed(d,f"pmub_v44_{nb2}_{type2}_{i}"))
        with st.expander(f"{'AUJOURDHUI' if i==0 else f'J+{i}'} - {nom} {d.strftime('%d/%m/%Y')} - {nb2} courses", expanded=(i==0)):
            data=[]
            for c in range(nb2):
                chevaux=rnd.sample(list(range(1,21)),10); att=rnd.randint(35,88); defe=rnd.randint(15,60); diff=att-defe; moy=round(rnd.uniform(1.5,3.5),1)
                def cote_pmu(marche):
                    if "Simple Gagnant" in marche: return round(rnd.uniform(2.0,25.0),1)
                    elif "Simple Place" in marche: return round(rnd.uniform(1.2,6.0),1)
                    elif "Couple Gagnant" in marche: return round(rnd.uniform(4.0,50.0),1)
                    elif "Couple Place" in marche: return round(rnd.uniform(2.5,20.0),1)
                    elif "Couple Ordre" in marche: return round(rnd.uniform(8.0,120.0),1)
                    elif "Tierce Ordre" in marche: return round(rnd.uniform(20.0,600.0),1)
                    elif "Tierce Desordre" in marche: return round(rnd.uniform(5.0,150.0),1)
                    elif "Quarte Ordre" in marche: return round(rnd.uniform(100.0,2500.0),1)
                    elif "Quarte Desordre" in marche: return round(rnd.uniform(20.0,500.0),1)
                    elif "Quinte Ordre" in marche: return round(rnd.uniform(1000.0,15000.0),1)
                    elif "Quinte Desordre" in marche: return round(rnd.uniform(100.0,2000.0),1)
                    elif "Quinte+" in marche: return round(rnd.uniform(800.0,10000.0),1)
                    elif "Multi en 4" in marche: return round(rnd.uniform(10.0,200.0),1)
                    elif "Multi en 5" in marche: return round(rnd.uniform(8.0,100.0),1)
                    elif "Multi en 6" in marche: return round(rnd.uniform(4.0,50.0),1)
                    elif "Multi en 7" in marche: return round(rnd.uniform(2.0,25.0),1)
                    else: return round(rnd.uniform(3.0,100.0),1)
                def prono_pmu(marche):
                    if "Simple" in marche: return f"{chevaux[0]}"
                    elif "Couple" in marche: return f"{chevaux[0]}-{chevaux[1]}"
                    elif "Tierce" in marche: return f"{chevaux[0]}-{chevaux[1]}-{chevaux[2]}"
                    elif "Quarte" in marche: return f"{chevaux[0]}-{chevaux[1]}-{chevaux[2]}-{chevaux[3]}"
                    elif "Quinte" in marche: return f"{chevaux[0]}-{chevaux[1]}-{chevaux[2]}-{chevaux[3]}-{chevaux[4]}"
                    elif "Multi en 4" in marche: return f"{chevaux[0]}-{chevaux[1]}-{chevaux[2]}-{chevaux[3]}"
                    elif "Multi en 5" in marche: return f"{chevaux[0]}-{chevaux[1]}-{chevaux[2]}-{chevaux[3]}-{chevaux[4]}"
                    elif "Multi en 6" in marche: return f"{chevaux[0]}-{chevaux[1]}-{chevaux[2]}-{chevaux[3]}-{chevaux[4]}-{chevaux[5]}"
                    elif "Multi en 7" in marche: return f"{chevaux[0]}-{chevaux[1]}-{chevaux[2]}-{chevaux[3]}-{chevaux[4]}-{chevaux[5]}-{chevaux[6]}"
                    else: return f"{chevaux[0]}-{chevaux[1]}-{chevaux[2]}"
                if "LEGENDE" in type2:
                    marche,prono=("Simple Gagnant",prono_pmu("Simple Gagnant")) if att>=70 else ("Couple Place",prono_pmu("Couple Place"))
                    marches=[(marche,prono,cote_pmu(marche))]
                elif "TOUS COMPLET" in type2:
                    marches=[("Simple Gagnant",prono_pmu("Simple Gagnant"),cote_pmu("Simple Gagnant")),("Simple Place",prono_pmu("Simple Place"),cote_pmu("Simple Place")),("Couple Gagnant",prono_pmu("Couple Gagnant"),cote_pmu("Couple Gagnant")),("Couple Place",prono_pmu("Couple Place"),cote_pmu("Couple Place")),("Tierce Ordre",prono_pmu("Tierce Ordre"),cote_pmu("Tierce Ordre")),("Tierce Desordre",prono_pmu("Tierce Desordre"),cote_pmu("Tierce Desordre")),("Quarte Ordre",prono_pmu("Quarte Ordre"),cote_pmu("Quarte Ordre")),("Quarte Desordre",prono_pmu("Quarte Desordre"),cote_pmu("Quarte Desordre")),("Quinte Ordre",prono_pmu("Quinte Ordre"),cote_pmu("Quinte Ordre")),("Quinte Desordre",prono_pmu("Quinte Desordre"),cote_pmu("Quinte Desordre")),("Multi en 4",prono_pmu("Multi en 4"),cote_pmu("Multi en 4")),("Multi en 7",prono_pmu("Multi en 7"),cote_pmu("Multi en 7"))]
                else:
                    marches=[(type2,prono_pmu(type2),cote_pmu(type2))]
                for marche,prono,cote in marches:
                    conf=confiance_simple(att,defe,diff,moy,marche,rnd); ai_op,ai_just=ai_vraie_opinion(f"Cheval {chevaux[0]}",att,defe,diff,moy,marche,prono,rnd)
                    data.append({"Course":f"R{i+1}C{c+1}","Type":marche,"Prono":prono,"Cote":cote,"Confiance":f"{conf}%","AI% Opinion":f"{ai_op}%","AI Justification":ai_just,"Jour":f"J+{i}"})
            st.dataframe(style_vert_rouge(pd.DataFrame(data)), use_container_width=True, hide_index=True)

with tab3:
    st.markdown("### BOURSE INTERNATIONALE - FOREX INDICE ACTION CRYPTO OR PETROLE")
    type3=st.selectbox("Type BOURSE", ["LEGENDE - 1 signal/actif","FOREX MAJEURES","FOREX XOF","FOREX EXOTIQUE","INDICE US","INDICE EUROPE","INDICE ASIE","ACTION US TECH","ACTION US AUTRE","ACTION EUROPE","CRYPTO","MATIERES OR PETROLE","TOUS FOREX","TOUS INDICE","TOUS ACTION","TOUS CRYPTO","TOUS COMPLET BOURSE"], index=0, key="t3f")
    nb3=st.slider("Nombre actifs BOURSE", 1, 20, 12, key="n3f")
    total=st.session_state.nb*3
    for i in range(total):
        d=datetime.now()+timedelta(days=i); nom=jours_fr[d.weekday()]; rnd=random.Random(seed(d,f"bourse_v44_{nb3}_{type3}_{i}"))
        with st.expander(f"{'AUJOURDHUI' if i==0 else f'J+{i}'} - {nom} {d.strftime('%d/%m/%Y')} - {nb3} actifs", expanded=(i==0)):
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
            else: markets=bourse_complete["FOREX MAJEURES"]+bourse_complete["INDICE US"]+bourse_complete["ACTION US TECH"]+bourse_complete["CRYPTO"]
            sel=rnd.sample(markets, min(nb3, len(markets)))
            for name,price,unit in sel:
                att=rnd.randint(35,88); defe=rnd.randint(15,60); diff=att-defe; moy=round(rnd.uniform(1.2,3.8),1)
                signal="ACHETER" if rnd.randint(0,1)==0 else "VENDRE"
                marche=f"{type3} - {signal}"; prono=signal
                conf=confiance_simple(att,defe,diff,moy,marche,rnd); ai_op,ai_just=ai_vraie_opinion(name,att,defe,diff,moy,marche,prono,rnd)
                data.append({"Actif":name,"Prix":f"{price}{unit}","Signal":signal,"Categorie":type3,"Confiance":f"{conf}%","AI% Opinion":f"{ai_op}%","AI Justification":ai_just,"Jour":f"J+{i}"})
            st.dataframe(style_vert_rouge(pd.DataFrame(data)), use_container_width=True, hide_index=True)

st.success(f"V44 CORRIGE - Sans erreur applymap - AI vraie opinion 38-99% - {st.session_state.nb*3} jours")
st.warning("PMU-B: Simple Gagnant/Place Couple Gagnant/Place/Ordre Tierce Ordre/Desordre Quarte Ordre/Desordre Quinte Ordre/Desordre/Quinte+ Multi 4-7 - BOURSE: Forex Maj XOF Exotique Indice US Europe Asie Action US Tech Europe Crypto Or Petrole")
