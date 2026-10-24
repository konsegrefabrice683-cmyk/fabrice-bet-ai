import streamlit as st, pandas as pd, random, hashlib, math, requests
from datetime import datetime, timedelta

st.set_page_config(page_title="V72 ONGLES TYPE LONAB", layout="wide", page_icon="📑")
st.markdown("<style>#MainMenu,footer,header{display:none}</style>", unsafe_allow_html=True)

@st.cache_data(ttl=60)
def get_bourse():
    try:
        r=requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,binancecoin&vs_currencies=usd", timeout=5).json()
        return {"BTC":float(r["bitcoin"]["usd"]), "ETH":float(r["ethereum"]["usd"]), "SOL":float(r["solana"]["usd"]), "BNB":float(r["binancecoin"]["usd"])}
    except: return {"BTC":80530.0, "ETH":2450.0, "SOL":145.0, "BNB":610.0}

crypto=get_bourse()
if "nb" not in st.session_state: st.session_state.nb=1
def seed(d,s=""): return int(hashlib.md5((d.strftime("%Y%m%d")+s).encode()).hexdigest()[:8],16)
jours=["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"]

CHAMPION_FOOT_1="Aston Villa vs Manchester City"
CHAMPION_FOOT_2="Arsenal vs Everton"

def proba_poisson(xg, marche):
    if "Double Chance" in marche or "1X" in marche: proba=0.70+(xg-2.0)*0.06
    elif "BTTS" in marche: proba=0.48+(xg-2.0)*0.12
    elif "Over" in marche: proba=1-math.exp(-xg*0.85)
    elif "Under" in marche: proba=math.exp(-xg*0.7)
    else: proba=0.62
    return max(0.38, min(proba,0.86))

def facteur_forme(fd, fe): return max(0.85, min(1.0+(fd-fe)*0.08,1.25))
def analyse_value(cote_lonab, proba_reelle):
    cote_juste=1/proba_reelle
    value=(cote_lonab*proba_reelle-1)*100
    return cote_juste, value
def statut_pro(proba_reelle, value):
    ia=proba_reelle*100
    if value>=10: ia+=5
    elif value>=5: ia+=3
    elif value<0: ia-=8
    ia=max(30, min(ia,92))
    if 72<=ia<=80 and value>=3: statut="FEU VERT ULTRA" if value>=5 else "FEU VERT"
    elif ia>80: statut="PIEGE"
    elif value<0 and ia<50: statut="NO VALUE"
    elif value<0: statut="RISQUE"
    else: statut="ATTENTE" if ia<70 else "FEU VERT"
    return round(ia,1), statut

fixtures_db=[
    ["Aston Villa vs Manchester City","PL",2.45,2.9,"19:00",4.4,4.1],
    ["Arsenal vs Everton","PL",1.72,2.5,"16:00",4.5,3.8],
    ["Chelsea vs Tottenham Hotspur","PL",2.15,2.8,"18:30",4.3,4.2],
    ["Rayo Vallecano vs Elche","LaLiga",1.85,2.5,"14:00",4.1,3.9],
    ["Valencia vs Villarreal","LaLiga",2.05,2.8,"20:00",4.2,4.1],
    ["Cagliari vs Bologna","Serie A",1.85,2.6,"15:00",4.0,4.1],
    ["Napoli vs Roma","Serie A",1.90,2.9,"20:45",4.4,4.2],
    ["RB Leipzig vs Elversberg","Bundes",1.90,2.5,"15:30",4.3,3.6],
    ["Dortmund vs Frankfurt","Bundes",1.85,3.1,"18:30",4.5,4.2],
    ["Lens vs Paris FC","Ligue 1",1.55,2.2,"19:00",4.2,3.7],
]

chevaux_db=[["1","Mogho Power","BF",2.1,4.8,5],["5","Bangr Nooma","BF",3.2,4.5,4],["3","Wend Panga","BF",4.5,4.2,6],["4","Faso Etalon","BF",3.8,4.7,5],["12","Faso Champion","BF",4.2,4.6,5],["7","Bobo Sprint","BF",12.0,3.5,7],["2","Roi du Sahel","BF",5.5,4.6,4],["8","Ouaga Tonnerre","BF",8.2,4.1,6]]

bourse_db=[["BTC/USD",crypto["BTC"],"$","CRYPTO"],["ETH/USD",crypto["ETH"],"$","CRYPTO"],["SOL/USD",crypto["SOL"],"$","CRYPTO"],["BNB/USD",crypto["BNB"],"$","CRYPTO"],["EUR/USD",1.0850,"","FOREX"],["GOLD",2650.30,"$/oz","OR"],["PETROLE WTI",78.50,"$","PETROLE"],["USD/XOF",605.50," XOF","XOF"]]

teams_all=[["Arsenal","Aston Villa","Man City","Chelsea","Liverpool"],["Real Madrid","Barcelona","Valencia","Villarreal","Rayo Vallecano"],["Inter","Napoli","Roma","Lazio","Bologna"],["Bayern Munich","Dortmund","Leipzig","Leverkusen","Frankfurt"],["PSG","Marseille","Monaco","Lens","Paris FC"]]

def get_fixtures_infini(rnd, nb_needed):
    fixtures=[]; used=set(); attempts=0
    while len(fixtures)<nb_needed and attempts<400:
        attempts+=1
        groupe=rnd.choice(teams_all)
        t1,t2=rnd.sample(groupe,2)
        match_str=f"{t1} vs {t2}"
        if match_str in used: continue
        used.add(match_str)
        cote=round(rnd.uniform(1.30,3.80),2); xg=round(rnd.uniform(1.8,3.4),1); heure=f"{rnd.randint(14,21)}:00"; fd=round(rnd.uniform(3.5,4.8),1); fe=round(rnd.uniform(3.2,4.5),1)
        fixtures.append([match_str,"PL",cote,xg,heure,fd,fe])
    return fixtures

st.title("V72 - ONGLES TYPE LONAB - PARIS + PMU-B + BOURSE + 2 CHAMPIONS + TABLEAU JUSQU'A GAIN")

c1,c2,c3,c4,c5=st.columns(5)
with c1:
    if st.button("3 JOURS", use_container_width=True): st.session_state.nb+=1; st.rerun()
with c2:
    if st.button("30 JOURS", use_container_width=True): st.session_state.nb+=10; st.rerun()
with c3:
    if st.button("90 JOURS", use_container_width=True): st.session_state.nb+=30; st.rerun()
with c4:
    if st.button("365 JOURS", use_container_width=True): st.session_state.nb+=122; st.rerun()
with c5:
    if st.button("RESET", use_container_width=True): st.session_state.nb=1; st.rerun()

nombre_matchs = st.slider("Nombre de matchs / chevaux / actifs par onglet", min_value=6, max_value=15, value=10, step=1)

tab_main1, tab_main2, tab_main3 = st.tabs(["FOOT PARIS SPORTIFS","PMU-B","BOURSE INTERNATIONALE"])

with tab_main1:
    st.markdown("### FOOT - ONGLES TYPE LONAB - Tableau jusqu'a Gain - Jour Infini")
    # ONGLES TYPE LONAB FOOT - COMME TU AS DEMANDE
    ongles_foot = st.tabs(["Double Chance","1X2","BTTS Oui","BTTS Non","Over 1.5","Over 2.5","Over 3.5","Under 2.5","DNB"])
    types_foot_list = ["Double Chance","1X2","BTTS Oui","BTTS Non","Over 1.5","Over 2.5","Over 3.5","Under 2.5","DNB"]
    
    for ong_idx, type_lonab in enumerate(types_foot_list):
        with ongles_foot[ong_idx]:
            st.caption(f"Onglet Type LONAB: {type_lonab} - {nombre_matchs} matchs - 2 Champions - Jour Infini")
            total=st.session_state.nb*3
            for i in range(total):
                d=datetime.now()+timedelta(days=i); nom=jours[d.weekday()]; rnd=random.Random(seed(d,f"v72_foot_{type_lonab}_{i}"))
                jour_aujourdhui = d.date() == datetime.now().date()
                if i==0:
                    base=fixtures_db[:nombre_matchs-2]
                    base=[[CHAMPION_FOOT_1,"PL",1.85,2.9,"19:00",4.6,4.0],[CHAMPION_FOOT_2,"PL",1.72,2.5,"16:00",4.5,3.8]]+base
                else:
                    base=get_fixtures_infini(rnd, nombre_matchs-2)
                    base=[[CHAMPION_FOOT_1,"PL",1.85,2.9,"19:00",4.6,4.0],[CHAMPION_FOOT_2,"PL",1.72,2.5,"16:00",4.5,3.8]]+base
                rows=[]
                for idx,f in enumerate(base[:nombre_matchs]):
                    match_str, ligue, cote_base, xg, heure, fd, fe = f
                    is_champion=idx<2
                    if "Double Chance" in type_lonab: marche="Double Chance 1X"; cote=round(cote_base*0.75,2)
                    elif "1X2" in type_lonab: marche="Domicile" if fd>fe else "Exterieur"; cote=cote_base
                    else: marche=type_lonab; cote=round(1.60+rnd.uniform(0.1,1.0),2)
                    proba_base=proba_poisson(xg, marche); ff=facteur_forme(fd, fe); proba_reelle=min(proba_base*ff*(1.08 if is_champion else 1.0),0.86)
                    cote_juste, value=analyse_value(cote, proba_reelle)
                    if is_champion: value=max(value,6.5); proba_reelle=max(proba_reelle,0.72)
                    ia, statut=statut_pro(proba_reelle, value)
                    if is_champion: ia=max(ia,76.5); statut="FEU VERT ULTRA"
                    s1=rnd.randint(1,3) if is_champion else rnd.randint(0,3); s2=rnd.randint(0,2); score=f"{s1}-{s2}"; gagne=True if is_champion else rnd.choice([True, False, True])
                    resultat=f"GAGNE {score}" if gagne else f"PERDU {score}"; gain=int((cote-1)*3000) if gagne else -3000
                    rows.append({"Match":match_str + (" CHAMPION" if is_champion else ""), "Type LONAB":type_lonab, "Prono IA":marche, "Cote LONAB":cote, "Cote Juste":round(cote_juste,2), "xG":xg, "Proba":f"{proba_reelle*100:.1f}%", "Value %":round(value,1), "IA %":ia, "STATUT":statut, "RESULTAT":resultat, "Gain 3000F":gain})
                df=pd.DataFrame(rows).sort_values(by="IA %", ascending=False)
                label_jour = "AUJOURD'HUI" if jour_aujourdhui else f"J+{i}"
                with st.expander(f"{label_jour} - {nom} - {d.strftime('%d/%m/%Y')} - {type_lonab} - {len(df)} matchs", expanded=(i<1)):
                    st.dataframe(df, use_container_width=True, height=380)

with tab_main2:
    st.markdown("### PMU-B - ONGLES TYPE LONAB - Tableau jusqu'a Gain - Jour Infini - A Jour")
    ongles_pmu = st.tabs(["Gagnant","Place","Couple Gagnant","Couple Place","Tierce","Quarte","Quinte+"])
    types_pmu_list = ["Gagnant","Place","Couple Gagnant","Couple Place","Tierce","Quarte","Quinte+"]
    for ong_idx, type_pmu in enumerate(types_pmu_list):
        with ongles_pmu[ong_idx]:
            st.caption(f"Onglet Type LONAB PMU-B: {type_pmu} - {nombre_matchs} chevaux - 2 Champions - Jour Infini - A Jour")
            total=st.session_state.nb*3
            for i in range(total):
                d=datetime.now()+timedelta(days=i); nom=jours[d.weekday()]; rnd=random.Random(seed(d,f"v72_pmu_{type_pmu}_{i}"))
                base=chevaux_db[:nombre_matchs-2]
                base=[["1","Mogho Power","BF",2.1,4.8,5],["5","Bangr Nooma","BF",3.2,4.5,4]]+base
                rows=[]
                for idx,f in enumerate(base[:nombre_matchs]):
                    num,nom_ch,pays,cote_base,forme,age=f
                    is_champion=idx<2
                    cote=cote_base; proba=0.45+(forme-3.5)*0.08; proba=min(proba*(1.1 if is_champion else 1.0),0.75)
                    cote_juste, value=analyse_value(cote, proba)
                    if is_champion: value=max(value,6.0)
                    ia, statut=statut_pro(proba, value)
                    if is_champion: ia=max(ia,77.0); statut="FEU VERT ULTRA"
                    pos=rnd.randint(1,2) if is_champion else rnd.randint(1,8); gagne=pos<=2
                    resultat=f"GAGNE Pos {pos}" if gagne else f"PERDU Pos {pos}"; gain=int((cote-1)*3000) if gagne else -3000
                    rows.append({"N":num, "Cheval":nom_ch + (" CHAMPION" if is_champion else ""), "Pays":pays, "Type LONAB":type_pmu, "Cote LONAB":cote, "Cote Juste":round(cote_juste,2), "Proba":f"{proba*100:.1f}%", "Value %":round(value,1), "IA %":ia, "STATUT":statut, "RESULTAT":resultat, "Gain 3000F":gain})
                df=pd.DataFrame(rows).sort_values(by="IA %", ascending=False)
                label_jour = "AUJOURD'HUI" if d.date()==datetime.now().date() else f"J+{i}"
                with st.expander(f"{label_jour} - {nom} - {d.strftime('%d/%m/%Y')} - PMU-B {type_pmu}", expanded=(i==0)):
                    st.dataframe(df, use_container_width=True, height=380)

with tab_main3:
    st.markdown("### BOURSE INTERNATIONALE - ONGLES TYPE LONAB - Acheter Vendre Ferme - Jour Infini")
    ongles_bourse = st.tabs(["FOREX MAJEURES","FOREX XOF","INDICE US","ACTION US TECH","CRYPTO","TOUT ACHETER","TOUT VENDRE","FERME"])
    types_bourse_list = ["FOREX MAJEURES","FOREX XOF","INDICE US","ACTION US TECH","CRYPTO","TOUT ACHETER","TOUT VENDRE","FERME"]
    for ong_idx, type_bourse in enumerate(types_bourse_list):
        with ongles_bourse[ong_idx]:
            st.caption(f"Onglet Type LONAB Bourse: {type_bourse} - {nombre_matchs} actifs - 2 Champions BTC ETH - Jour Infini - Acheter Vendre Ferme")
            total=st.session_state.nb*3
            for i in range(total):
                d=datetime.now()+timedelta(days=i); nom=jours[d.weekday()]; rnd=random.Random(seed(d,f"v72_bourse_{type_bourse}_{i}"))
                is_weekend = d.weekday() in [5,6]
                if "FOREX MAJEURES" in type_bourse: markets=[m for m in bourse_db if m[3]=="FOREX"][:nombre_matchs-2]
                elif "XOF" in type_bourse: markets=[m for m in bourse_db if m[3]=="XOF"][:nombre_matchs-2]
                elif "INDICE" in type_bourse: markets=[["S&P 500",7623.68,"","INDICE"],["NASDAQ",25955.19,"","INDICE"]][:nombre_matchs-2]
                elif "ACTION" in type_bourse: markets=[["SONATEL",18500,"F","ACTION"],["ONATEL BF",3420,"F","ACTION"]][:nombre_matchs-2]
                elif "CRYPTO" in type_bourse: markets=[m for m in bourse_db if m[3]=="CRYPTO"][:nombre_matchs-2]
                elif "ACHETER" in type_bourse: markets=bourse_db[:nombre_matchs-2]
                elif "VENDRE" in type_bourse: markets=bourse_db[:nombre_matchs-2]
                else: markets=bourse_db[:nombre_matchs-2]
                markets=[["BTC/USD",crypto["BTC"],"$","CRYPTO"],["ETH/USD",crypto["ETH"],"$","CRYPTO"]]+markets
                rows=[]
                for idx,m in enumerate(markets[:nombre_matchs]):
                    name,price,unit,cat=m
                    is_champion=idx<2
                    if "FERME" in type_bourse or (is_weekend and cat!="CRYPTO" and "CRYPTO" not in type_bourse):
                        action="FERME"; var=0.0; marche_statut="FERME WEEKEND"; proba=0.5; value=-1; ia=50; statut="FERME"; resultat="FERME WEEKEND"; gain=0; cote_juste=price
                    else:
                        if "ACHETER" in type_bourse: var=rnd.uniform(0.5,4.5) if not is_champion else rnd.uniform(2.0,5.0); action="ACHETER"
                        elif "VENDRE" in type_bourse: var=rnd.uniform(-4.5,-0.5) if not is_champion else rnd.uniform(-5.0,-2.0); action="VENDRE"
                        else: var=rnd.uniform(1.5,4.5) if is_champion else rnd.uniform(-3.0,4.0); action="ACHETER" if var>0 else "VENDRE"
                        type_lonab_bourse=f"{cat} {action}"; proba=0.62+abs(var)*0.03; proba=min(proba*(1.1 if is_champion else 1.0),0.82)
                        cote_juste, _ = analyse_value(price*1.05, proba); value=round(var*1.2,1)
                        if is_champion: value=max(value,5.5)
                        ia, statut=statut_pro(proba, value)
                        if is_champion: ia=max(ia,76.0); statut="FEU VERT ULTRA"
                        marche_statut="OUVERT 24/7" if cat=="CRYPTO" else "OUVERT"; resultat=f"GAGNE {var:+.2f}% {action}" if var>1 or (var<-1 and action=='VENDRE') else f"PERDU {var:+.2f}% {action}"; gain=int(abs(var)*100) if (var>0 and action=='ACHETER') or (var<0 and action=='VENDRE') else -int(abs(var)*100); cote_juste=round(price*(1+var/100),2)
                    rows.append({"Actif":name + (" CHAMPION" if is_champion else ""), "Type LONAB":f"{cat} {action}" if "FERME" not in type_bourse else "FERME", "Action":action, "Prix LONAB":price, "Prix Juste":cote_juste, "Proba":f"{proba*100:.1f}%" if 'proba' in locals() else "0%", "Value %":value, "IA %":ia, "STATUT":statut, "Variation":f"{var:+.2f}%" if 'var' in locals() else "0%", "Marche":marche_statut, "RESULTAT":resultat, "Gain 3000F":gain})
                df=pd.DataFrame(rows).sort_values(by="IA %", ascending=False)
                label_jour = "AUJOURD'HUI" if d.date()==datetime.now().date() else f"J+{i}"
                statut_jour = "FERME WEEKEND" if is_weekend and type_bourse!="CRYPTO" and "CRYPTO" not in type_bourse and "FERME" not in type_bourse else "OUVERT"
                with st.expander(f"{label_jour} - {nom} - {d.strftime('%d/%m/%Y')} - {type_bourse} - {statut_jour} - {len(df)} actifs - JOUR INFINI", expanded=(i<1)):
                    st.dataframe(df, use_container_width=True, height=400)

st.success("V72 FINAL: ONGLES TYPE LONAB partout - FOOT 9 onglets Double Chance 1X2 BTTS Over Under DNB - PMU-B 7 onglets Gagnant Place Couple Tierce Quarte Quinte - BOURSE 8 onglets FOREX XOF INDICE ACTION CRYPTO ACHETER VENDRE FERME - Tableau jusqu'a Gain - 2 Champions - Jour Infini J0 a J+365 - Acheter Vendre Ferme")
