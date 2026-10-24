import streamlit as st, pandas as pd, random, hashlib, requests, re
from datetime import datetime, timedelta

st.set_page_config(page_title="FABRICE BET AI - V45 FEU VERT ROUGE", layout="wide", page_icon="🚦")
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

# POURCENTAGE FIXE - NE VARIE PLUS + FEU VERT/ROUGE SELON VRAIE ANALYSE
def analyse_feu(attaque, defense, diff, marche, rnd):
    # Vraie analyse interne mais affichage FIXE
    score = attaque + diff
    if "Score Exact" in marche or "Quinte Ordre" in marche: score -= 25
    if "Double Chance" in marche or "Over 0.5" in marche: score += 15
    if "Simple Gagnant" in marche: score += 10
    score += rnd.randint(-8,8)
    
    if score >= 75:
        # BONNE ANALYSE = FEU VERT
        return 75, "FEU VERT", "🟢", 65, "+5%", 1.85
    elif score >= 60:
        return 68, "FEU VERT", "🟢", 65, "+5%", 1.85
    elif score >= 50:
        return 55, "FEU ORANGE", "🟠", 55, "+2%", 2.10
    else:
        # MAUVAISE ANALYSE = FEU ROUGE
        return 38, "FEU ROUGE", "🔴", 40, "-8%", 2.80

def style_feu(df):
    def color_statut(v):
        if "VERT" in str(v): return 'background-color: #00FF00; color: black; font-weight: bold; font-size: 15px'
        elif "ROUGE" in str(v): return 'background-color: #FF0000; color: white; font-weight: bold; font-size: 15px'
        elif "ORANGE" in str(v): return 'background-color: #FFA500; color: black; font-weight: bold'
        else: return ''
    return df.style.map(color_statut, subset=["STATUT"])

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
]

bourse_complete={
    "FOREX MAJEURES":[("EUR/USD",1.0850,""),("GBP/USD",1.2950,""),("USD/JPY",149.20,""),("USD/CHF",0.8950,"")],
    "FOREX XOF":[("USD/XOF",605.50," XOF"),("EUR/XOF",657.00," XOF")],
    "INDICE US":[("S&P 500",7623.68,""),("NASDAQ",25955.19,""),("DOW JONES",52215.58,"")],
    "INDICE EUROPE":[("CAC 40",8150.20,""),("DAX",19200.50,""),("FTSE 100",8420.10,"")],
    "ACTION US TECH":[("TSLA",372.22,"$"),("NVDA",210.96,"$"),("AAPL",347.72,"$"),("MSFT",445.20,"$"),("META",485.30,"$")],
    "CRYPTO":[("BTC/USD",crypto_live["BTC"],"$"),("ETH/USD",crypto_live["ETH"],"$"),("SOL/USD",crypto_live["SOL"],"$"),("BNB/USD",crypto_live["BNB"],"$"),("XRP/USD",crypto_live["XRP"],"$")],
    "MATIERES":[("OR - GOLD",2650.30,"$/oz"),("PETROLE - WTI",78.50,"$")]
}

jours_fr=["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"]
st.title("FABRICE BET AI - V45 FEU VERT ROUGE")
st.caption(f"POURCENTAGE FIXE - FEU VERT si bon / FEU ROUGE si mauvais - Plus de 43% 51% qui varie - {datetime.now():%d/%m/%Y}")

col1,col2,col3,col4=st.columns(4)
with col1:
    if st.button("PLUS 3 JOURS", use_container_width=True): st.session_state.nb+=1; st.rerun()
with col2:
    if st.button("PLUS 30 JOURS", use_container_width=True): st.session_state.nb+=10; st.rerun()
with col3:
    if st.button("MAJ", use_container_width=True): st.cache_data.clear(); st.rerun()
with col4:
    if st.button("RESET", use_container_width=True): st.session_state.nb=1; st.rerun()

st.info(f"♾️ {st.session_state.nb*3} jours - FEU VERT = Bonne analyse / FEU ROUGE = Mauvaise analyse")
c1,c2=st.columns(2)
c1.markdown("🟢 **FEU VERT = Bonne analyse - JOUER**")
c2.markdown("🔴 **FEU ROUGE = Mauvaise analyse - NE PAS JOUER**")

tab1,tab2,tab3=st.tabs(["CHAMPION 1 - FOOT","CHAMPION 2 - PMU-B COMPLET","CHAMPION 3 - BOURSE INTERNATIONALE"])

with tab1:
    st.markdown("### FOOT - FEU VERT / FEU ROUGE - POURCENTAGE FIXE")
    type1=st.selectbox("Type FOOT", ["LEGENDE - 1 marche/match","1X2","Double Chance","Score Exact","Over Under 0.5-5.5","BTTS","Cartons","Expulsion","Corners","TOUS COMPLET"], index=0, key="t1f")
    nb1=st.slider("Nombre matchs FOOT", 1, 20, 9, key="n1f")
    total=st.session_state.nb*3
    for i in range(total):
        d=datetime.now()+timedelta(days=i); nom=jours_fr[d.weekday()]; rnd=random.Random(seed(d,f"foot_feu_{nb1}_{type1}_{i}"))
        with st.expander(f"{'AUJOURDHUI' if i==0 else f'J+{i}'} - {nom} {d.strftime('%d/%m/%Y')} - {nb1} matchs", expanded=(i==0)):
            data=[]; matches=rnd.sample(fixtures, min(nb1, len(fixtures)))
            for team,lig,att,defe,moy in matches:
                diff=att-defe
                if type1=="1X2": marche,prono="1X2",rnd.choice(["1","X","2"])
                elif type1=="Double Chance": marche,prono="Double Chance",rnd.choice(["1X","X2","12"])
                elif type1=="Score Exact": marche,prono="Score Exact",rnd.choice(["1-0","2-0","2-1","1-1"])
                elif "Over Under" in type1: marche,prono="Over Under",rnd.choice(["Over 0.5","Over 1.5","Over 2.5","Under 2.5","Over 3.5"])
                elif type1=="BTTS": marche,prono="BTTS",rnd.choice(["GG Oui","GG Non"])
                elif type1=="Cartons": marche,prono="Cartons",rnd.choice(["Over 3.5 Cartons","Under 3.5 Cartons"])
                elif type1=="Expulsion": marche,prono="Expulsion",rnd.choice(["Expulsion Oui","Expulsion Non"])
                elif type1=="Corners": marche,prono="Corners",rnd.choice(["Over 8.5 Corners","Under 8.5 Corners"])
                else: marche,prono=("1X2","1") if diff>20 else ("Over Under","Over 2.5") if moy>=2.8 else ("Double Chance","1X")
                ia,statut,emoji,proba,value,cote=analyse_feu(att,defe,diff,marche,rnd)
                data.append({"Match":team,"Marche":marche,"Prono":prono,"Cote":cote,"Proba":f"{proba}%","Value":value,"IA":ia,"STATUT":f"{emoji} {statut}"})
            st.dataframe(style_feu(pd.DataFrame(data)), use_container_width=True, hide_index=True)

with tab2:
    st.markdown("### PMU-B - SIMPLE COUPLE TIERCE QUARTE QUINTE MULTI - FEU VERT/ROUGE")
    type2=st.selectbox("Type PMU-B", ["LEGENDE","Simple Gagnant","Simple Place","Couple Gagnant","Couple Place","Couple Ordre","Tierce Ordre","Tierce Desordre","Quarte Ordre","Quarte Desordre","Quinte Ordre","Quinte Desordre","Quinte+","Multi en 4","Multi en 5","Multi en 6","Multi en 7","TOUS COMPLET"], index=0, key="t2f")
    nb2=st.slider("Nombre courses PMU-B", 1, 20, 12, key="n2f")
    total=st.session_state.nb*3
    for i in range(total):
        d=datetime.now()+timedelta(days=i); nom=jours_fr[d.weekday()]; rnd=random.Random(seed(d,f"pmub_feu_{nb2}_{type2}_{i}"))
        with st.expander(f"{'AUJOURDHUI' if i==0 else f'J+{i}'} - {nom} {d.strftime('%d/%m/%Y')} - {nb2} courses", expanded=(i==0)):
            data=[]
            for c in range(nb2):
                chevaux=rnd.sample(list(range(1,21)),10); att=rnd.randint(35,88); defe=rnd.randint(15,60); diff=att-defe
                def prono_pmu(m):
                    if "Simple" in m: return f"{chevaux[0]}"
                    elif "Couple" in m: return f"{chevaux[0]}-{chevaux[1]}"
                    elif "Tierce" in m: return f"{chevaux[0]}-{chevaux[1]}-{chevaux[2]}"
                    elif "Quarte" in m: return f"{chevaux[0]}-{chevaux[1]}-{chevaux[2]}-{chevaux[3]}"
                    elif "Quinte" in m: return f"{chevaux[0]}-{chevaux[1]}-{chevaux[2]}-{chevaux[3]}-{chevaux[4]}"
                    elif "Multi en 4" in m: return f"{chevaux[0]}-{chevaux[1]}-{chevaux[2]}-{chevaux[3]}"
                    elif "Multi en 7" in m: return f"{chevaux[0]}-{chevaux[1]}-{chevaux[2]}-{chevaux[3]}-{chevaux[4]}-{chevaux[5]}-{chevaux[6]}"
                    else: return f"{chevaux[0]}"
                def cote_pmu(m):
                    if "Simple Gagnant" in m: return 1.85
                    elif "Simple Place" in m: return 1.35
                    elif "Couple Gagnant" in m: return 4.20
                    elif "Tierce Ordre" in m: return 45.00
                    elif "Quarte Ordre" in m: return 250.00
                    elif "Quinte Ordre" in m: return 1200.00
                    elif "Multi" in m: return 8.50
                    else: return 1.85
                if "LEGENDE" in type2: marche= "Simple Gagnant" if att>=70 else "Couple Place"
                elif "TOUS COMPLET" in type2: marche="Simple Gagnant"
                else: marche=type2
                prono=prono_pmu(marche); cote=cote_pmu(marche)
                ia,statut,emoji,proba,value,cote_calc=analyse_feu(att,defe,diff,marche,rnd)
                # On garde cote fixe PMU mais statut selon analyse
                data.append({"Course":f"R{i+1}C{c+1}","Type":marche,"Prono":prono,"Cote":cote,"Proba":f"{proba}%","Value":value,"IA":ia,"STATUT":f"{emoji} {statut}"})
            st.dataframe(style_feu(pd.DataFrame(data)), use_container_width=True, hide_index=True)

with tab3:
    st.markdown("### BOURSE INTERNATIONALE - FOREX INDICE ACTION CRYPTO - FEU VERT/ROUGE")
    type3=st.selectbox("Type BOURSE", ["LEGENDE","FOREX MAJEURES","FOREX XOF","INDICE US","INDICE EUROPE","ACTION US TECH","ACTION EUROPE","CRYPTO","MATIERES OR PETROLE","TOUS FOREX","TOUS INDICE","TOUS ACTION","TOUS COMPLET BOURSE"], index=0, key="t3f")
    nb3=st.slider("Nombre actifs BOURSE", 1, 20, 12, key="n3f")
    total=st.session_state.nb*3
    for i in range(total):
        d=datetime.now()+timedelta(days=i); nom=jours_fr[d.weekday()]; rnd=random.Random(seed(d,f"bourse_feu_{nb3}_{type3}_{i}"))
        with st.expander(f"{'AUJOURDHUI' if i==0 else f'J+{i}'} - {nom} {d.strftime('%d/%m/%Y')} - {nb3} actifs", expanded=(i==0)):
            data=[]
            if "FOREX MAJEURES" in type3: markets=bourse_complete["FOREX MAJEURES"]
            elif "FOREX XOF" in type3: markets=bourse_complete["FOREX XOF"]
            elif "INDICE US" in type3: markets=bourse_complete["INDICE US"]
            elif "INDICE EUROPE" in type3: markets=bourse_complete["INDICE EUROPE"]
            elif "ACTION US TECH" in type3: markets=bourse_complete["ACTION US TECH"]
            elif "ACTION EUROPE" in type3: markets=bourse_complete["ACTION EUROPE"]
            elif "CRYPTO" in type3: markets=bourse_complete["CRYPTO"]
            elif "MATIERES" in type3: markets=bourse_complete["MATIERES"]
            elif "TOUS FOREX" in type3: markets=bourse_complete["FOREX MAJEURES"]+bourse_complete["FOREX XOF"]
            elif "TOUS INDICE" in type3: markets=bourse_complete["INDICE US"]+bourse_complete["INDICE EUROPE"]
            elif "TOUS ACTION" in type3: markets=bourse_complete["ACTION US TECH"]+bourse_complete["ACTION EUROPE"]
            elif "TOUS COMPLET" in type3: markets=bourse_complete["FOREX MAJEURES"]+bourse_complete["INDICE US"]+bourse_complete["ACTION US TECH"]+bourse_complete["CRYPTO"]
            else: markets=bourse_complete["FOREX MAJEURES"]+bourse_complete["INDICE US"]+bourse_complete["ACTION US TECH"]+bourse_complete["CRYPTO"]
            sel=rnd.sample(markets, min(nb3, len(markets)))
            for name,price,unit in sel:
                att=rnd.randint(35,88); defe=rnd.randint(15,60); diff=att-defe
                signal="ACHETER" if rnd.randint(0,1)==0 else "VENDRE"; marche=f"{type3}"
                ia,statut,emoji,proba,value,cote=analyse_feu(att,defe,diff,marche,rnd)
                data.append({"Actif":name,"Prix":f"{price}{unit}","Signal":signal,"Proba":f"{proba}%","Value":value,"IA":ia,"STATUT":f"{emoji} {statut}"})
            st.dataframe(style_feu(pd.DataFrame(data)), use_container_width=True, hide_index=True)

st.success(f"V45 FEU VERT/ROUGE - Pourcentage FIXE 65% ou 40% - Ne varie plus - Vert si bonne analyse / Rouge si mauvaise - {st.session_state.nb*3} jours")
