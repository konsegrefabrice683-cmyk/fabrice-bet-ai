import streamlit as st, pandas as pd, random, hashlib, requests
from datetime import datetime, timedelta
from PIL import Image

st.set_page_config(page_title="FABRICE BET AI - 3 CHAMPIONS COMPLET", layout="wide", page_icon="🔥")
st.markdown("<style>#MainMenu,footer,header{display:none} .stButton>button{font-weight:bold}</style>", unsafe_allow_html=True)

@st.cache_data(ttl=60)
def get_bourse():
    try:
        r=requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd", timeout=5).json()
        return {"BTC":r["bitcoin"]["usd"], "ETH":r["ethereum"]["usd"], "SOL":r["solana"]["usd"]}
    except:
        return {"BTC":80530, "ETH":2450, "SOL":145}

crypto_live=get_bourse()
if "nb" not in st.session_state: st.session_state.nb=1
def seed(d,s=""): return int(hashlib.md5((d.strftime("%Y%m%d")+s).encode()).hexdigest()[:8],16)

def confiance_selon_analyse(attaque, defense, diff, moy_buts, marche):
    base=70
    if attaque>=82: base+=8
    elif attaque>=65: base+=4
    elif attaque<50: base-=5
    if diff>=30: base+=7
    elif diff>=15: base+=4
    elif diff<=-15: base+=3
    if defense<=30: base+=5
    if moy_buts>=2.8 and "Over" in marche: base+=6
    if moy_buts<=2.2 and "Under" in marche: base+=6
    if "Score Exact" in marche: base-=12
    elif "Expulsion" in marche or "Quinte" in marche: base-=8
    elif "Double Chance" in marche or "Simple Gagnant" in marche: base+=10
    elif "Over 0.5" in marche: base+=12
    base+=random.randint(-3,3)
    if base<68: base=68+random.randint(0,4)
    if base>92: base=92-random.randint(0,4)
    return base

st.title("FABRICE BET AI - 3 CHAMPIONS COMPLET ♾️")
st.caption(f"3 ONGLETS - TOUS TYPES LONAB - JOUR INFINI + MISE A JOUR INFINI - {datetime.now():%d/%m/%Y %H:%M:%S}")

col1,col2,col3,col4=st.columns(4)
with col1:
    if st.button("PLUS 3 JOURS ♾️", use_container_width=True): st.session_state.nb+=1; st.rerun()
with col2:
    if st.button("PLUS 30 JOURS ♾️", use_container_width=True): st.session_state.nb+=10; st.rerun()
with col3:
    if st.button("MISE A JOUR ♾️", use_container_width=True): st.cache_data.clear(); st.rerun()
with col4:
    if st.button("RESET", use_container_width=True): st.session_state.nb=1; st.rerun()

st.info(f"♾️ JOUR INFINI: {st.session_state.nb*3} jours - Jusqu'au {(datetime.now()+timedelta(days=st.session_state.nb*3-1)).strftime('%d/%m/%Y')} - Derniere MAJ: {datetime.now():%H:%M:%S}")
if st.session_state.nb>50: st.success(f"🔥 INFINI EXTREME - {st.session_state.nb*3} jours - Annee {(datetime.now()+timedelta(days=st.session_state.nb*3)).strftime('%Y')}")

fixtures=[
    ("Crystal Palace vs Newcastle","PL",48,55,2.4),("Liverpool vs Brighton","PL",82,75,2.9),
    ("Man United vs Bournemouth","PL",74,60,2.7),("Inter vs Man City","LDC",78,22,2.8),
    ("Real vs Brest","LDC",65,12,1.9),("Barca vs Real","Liga",82,35,3.2),
    ("EFO vs Bayern","Amical",45,55,3.5),("RCB vs USFA","Fasofoot",58,28,2.1),
    ("Douanes vs Majestic","Fasofoot",52,18,1.8),("Sonabel vs Vitesse","Fasofoot",48,15,1.6),
    ("ASFA vs EFO","Fasofoot",55,30,2.2),("Salitas vs Rahimo","Fasofoot",50,25,2.0),
    ("Arsenal vs Chelsea","PL",80,62,2.8),("PSG vs Marseille","L1",85,58,3.0),
    ("Bayern vs Dortmund","Bundes",84,65,3.1),("AC Milan vs Inter","Serie A",78,70,2.6),
    ("Ajax vs PSV","Eredivisie",75,60,2.9),("Al Nassr vs Al Hilal","Saudi",82,68,2.8),
    ("Wydad vs Raja","Botola",70,62,2.2),("Asec vs Africa","Ligue1 CI",68,55,2.3),
]
jours_fr=["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"]
photo=st.file_uploader("📸 Envoie photo match (optionnel) - Comme ta photo Premier League", type=["jpg","png","jpeg"], key="photo_complet")

tab1,tab2,tab3=st.tabs(["CHAMPION 1 - FOOT - 12 FIXES ♾️","CHAMPION 2 - PMU-B COMPLET ♾️","CHAMPION 3 - BOURSE COMPLET ♾️"])

# ================= CHAMPION 1 - FOOT - COMPLET =================
with tab1:
    st.markdown("### CHAMPION 1 - FOOT - TOUS TYPES LONAB - LEGENDE VARY 68-92%")
    col_type,col_nb=st.columns([2,1])
    with col_type:
        type_lonab1=st.selectbox("Type LONAB FOOT", [
            "LEGENDE - TOUS - Vary 68-92% - Recommande",
            "1X2","Double Chance","Score Exact - 0-0 a 6-1 SANS LIMITE","Over Under - 0.5 a 5.5 SANS LIMITE",
            "BTTS - GG Oui Non","BTTS + Over","Cartons - Over Under","Expulsion - Rouge Oui Non","Corners - Over Under","Mi-Temps / MT-Fin",
            "TOUS - Comme photo analyse complete"
        ], index=0, key="type1_complet")
    with col_nb:
        nb_matchs1=st.number_input("Nombre matchs FOOT", 1, 20, 3, key="nb1_complet")
    nb_slider1=st.slider(f"FOOT - Nombre matchs - {nb_matchs1} choisis", 1, 20, int(nb_matchs1), key="slider1_complet")
    nb_matchs1=nb_slider1
    if photo: 
        try: st.image(Image.open(photo), caption=f"Photo - {nb_matchs1} matchs", use_container_width=True)
        except: pass
    total=st.session_state.nb*3
    for i in range(total):
        d=datetime.now()+timedelta(days=i); nom=jours_fr[d.weekday()]; rnd=random.Random(seed(d,f"foot_complet_{nb_matchs1}_{type_lonab1}_{i}"))
        is_today=(i==0); jour_label="AUJOURDHUI" if is_today else f"J+{i}"
        with st.expander(f"{jour_label} - {nom} {d.strftime('%d/%m/%Y')} - {nb_matchs1} matchs FOOT - {type_lonab1}", expanded=is_today):
            data=[]; matches_sample=rnd.sample(fixtures, min(nb_matchs1, len(fixtures)))
            for team,lig,attaque,defense,moy_buts in matches_sample:
                diff=attaque-defense
                if "TOUS" in type_lonab1 or "LEGENDE" in type_lonab1:
                    marches=[("1X2","1" if diff>15 else "2" if diff<-10 else "1"),("Double Chance","1X" if diff>0 else "X2"),("Score Exact",rnd.choice(["2-1","1-0","2-0","1-1","3-1"])),("Score Exact",rnd.choice(["0-1","1-2"])),("Over Under","Over 0.5"),("Over Under","Over 1.5"),("Over Under","Over 2.5"),("Over Under","Under 3.5"),("Over Under","Under 5.5"),("BTTS","GG Oui"),("BTTS + Over","GG Oui + Over 2.5"),("Cartons","Over 3.5 Cartons"),("Expulsion","Expulsion Non"),("Corners","Over 8.5 Corners"),("Corners","Over 9.5 Corners"),("MT-Fin","1/1")]
                else:
                    marches=[(type_lonab1,rnd.choice(["1","X","2","1X","2-1","Over 2.5"]))]
                for marche,prono in marches:
                    cote=round(rnd.uniform(6.5,11.5),2) if "Score Exact" in marche else round(rnd.uniform(1.08,2.8),2)
                    conf=confiance_selon_analyse(attaque,defense,diff,moy_buts,marche); ai=conf+rnd.randint(-1,2); ai=min(94,max(66,ai))
                    if conf>=85: raison=f"Att {attaque}% tres fort Diff {diff} eleve {moy_buts:.1f} buts"
                    elif conf>=78: raison=f"Att {attaque}% fort Diff {diff} {moy_buts:.1f} buts"
                    else: raison=f"Att {attaque}% Diff {diff}"
                    data.append({"Match":team,"Ligue":lig,"Marche":marche,"Prono":prono,"Cote":cote,"Analyse":f"{team} - {raison} - {marche} {prono}","Confiance":f"{conf}%","AI%":f"{ai}%","Jour":f"J+{i}"})
            st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)

# ================= CHAMPION 2 - PMU-B - COMPLET =================
with tab2:
    st.markdown("### CHAMPION 2 - PMU-B - TOUS TYPES LONAB - SIMPLE TIERCE QUARTE QUINTE")
    col_type2,col_nb2=st.columns([2,1])
    with col_type2:
        type_lonab2=st.selectbox("Type LONAB PMU-B", [
            "LEGENDE - TOUS PMU-B - Vary 68-92% - Recommande",
            "Simple Gagnant","Simple Place","Couple Gagnant","Couple Place","Couple Ordre",
            "Tierce Ordre","Tierce Desordre","Quarte Ordre","Quarte Desordre","Quinte Ordre","Quinte Desordre",
            "Multi 4","Multi 5","Multi 6","Multi 7"
        ], index=0, key="type2_complet")
    with col_nb2:
        nb_matchs2=st.number_input("Nombre courses PMU-B", 1, 20, 6, key="nb2_complet")
    nb_slider2=st.slider(f"PMU-B - Nombre courses - {nb_matchs2} choisis", 1, 20, int(nb_matchs2), key="slider2_complet")
    nb_matchs2=nb_slider2
    total=st.session_state.nb*3
    for i in range(total):
        d=datetime.now()+timedelta(days=i); nom=jours_fr[d.weekday()]; rnd=random.Random(seed(d,f"pmu_complet_{nb_matchs2}_{type_lonab2}_{i}"))
        is_today=(i==0); jour_label="AUJOURDHUI" if is_today else f"J+{i}"
        with st.expander(f"{jour_label} - {nom} {d.strftime('%d/%m/%Y')} - {nb_matchs2} courses PMU-B - {type_lonab2}", expanded=is_today):
            data=[]; 
            for c in range(nb_matchs2):
                chevaux=rnd.sample(list(range(1,21)),8)
                attaque_pmu=rnd.randint(45,85); defense_pmu=rnd.randint(15,55); diff_pmu=attaque_pmu-defense_pmu; moy_pmu=round(rnd.uniform(1.5,3.5),1)
                if "TOUS" in type_lonab2 or "LEGENDE" in type_lonab2:
                    marches_pmu=[
                        ("Simple Gagnant",f"{chevaux[0]}",round(rnd.uniform(2.5,15.0),1)),
                        ("Simple Place",f"{chevaux[0]}",round(rnd.uniform(1.5,4.5),1)),
                        ("Couple Gagnant",f"{chevaux[0]}-{chevaux[1]}",round(rnd.uniform(5.0,35.0),1)),
                        ("Couple Place",f"{chevaux[0]}-{chevaux[1]}",round(rnd.uniform(2.8,12.0),1)),
                        ("Tierce Ordre",f"{chevaux[0]}-{chevaux[1]}-{chevaux[2]}",round(rnd.uniform(15.0,250.0),1)),
                        ("Tierce Desordre",f"{chevaux[0]}-{chevaux[1]}-{chevaux[2]}",round(rnd.uniform(8.0,80.0),1)),
                        ("Quarte Ordre",f"{chevaux[0]}-{chevaux[1]}-{chevaux[2]}-{chevaux[3]}",round(rnd.uniform(80.0,800.0),1)),
                        ("Quarte Desordre",f"{chevaux[0]}-{chevaux[1]}-{chevaux[2]}-{chevaux[3]}",round(rnd.uniform(25.0,250.0),1)),
                        ("Quinte Ordre",f"{chevaux[0]}-{chevaux[1]}-{chevaux[2]}-{chevaux[3]}-{chevaux[4]}",round(rnd.uniform(500.0,5000.0),1)),
                        ("Quinte Desordre",f"{chevaux[0]}-{chevaux[1]}-{chevaux[2]}-{chevaux[3]}-{chevaux[4]}",round(rnd.uniform(80.0,800.0),1)),
                        ("Multi 4",f"{chevaux[0]}-{chevaux[1]}-{chevaux[2]}-{chevaux[3]}",round(rnd.uniform(15.0,120.0),1)),
                        ("Multi 7",f"{chevaux[0]}-{chevaux[1]}-{chevaux[2]}-{chevaux[3]}-{chevaux[4]}-{chevaux[5]}-{chevaux[6]}",round(rnd.uniform(3.0,15.0),1)),
                    ]
                else:
                    if "Simple" in type_lonab2: prono=f"{chevaux[0]}"; cote=round(rnd.uniform(2.5,15.0),1)
                    elif "Couple" in type_lonab2: prono=f"{chevaux[0]}-{chevaux[1]}"; cote=round(rnd.uniform(5.0,35.0),1)
                    elif "Tierce" in type_lonab2: prono=f"{chevaux[0]}-{chevaux[1]}-{chevaux[2]}"; cote=round(rnd.uniform(15.0,250.0),1)
                    elif "Quarte" in type_lonab2: prono=f"{chevaux[0]}-{chevaux[1]}-{chevaux[2]}-{chevaux[3]}"; cote=round(rnd.uniform(80.0,800.0),1)
                    elif "Quinte" in type_lonab2: prono=f"{chevaux[0]}-{chevaux[1]}-{chevaux[2]}-{chevaux[3]}-{chevaux[4]}"; cote=round(rnd.uniform(500.0,5000.0),1)
                    else: prono=f"{chevaux[0]}-{chevaux[1]}-{chevaux[2]}-{chevaux[3]}"; cote=round(rnd.uniform(15.0,120.0),1)
                    marches_pmu=[(type_lonab2,prono,cote)]
                for marche,prono,cote in marches_pmu:
                    conf=confiance_selon_analyse(attaque_pmu,defense_pmu,diff_pmu,moy_pmu,marche); ai=conf+rnd.randint(-1,2); ai=min(94,max(66,ai))
                    if conf>=85: raison=f"Cheval {chevaux[0]} Att {attaque_pmu}% tres fort Diff {diff_pmu}"
                    elif conf>=78: raison=f"Cheval {chevaux[0]} Att {attaque_pmu}% fort Diff {diff_pmu}"
                    else: raison=f"Cheval {chevaux[0]} Att {attaque_pmu}% Diff {diff_pmu}"
                    data.append({"Course":f"R{i+1}C{c+1}","Type":marche,"Prono":prono,"Cote":cote,"Analyse":f"{raison} - {marche} {prono}","Confiance":f"{conf}%","AI%":f"{ai}%","Jour":f"J+{i}"})
            st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)

# ================= CHAMPION 3 - BOURSE - COMPLET =================
with tab3:
    st.markdown("### CHAMPION 3 - BOURSE INTERNATIONALE - FOREX INDICE ACTION CRYPTO - COMPLET")
    col_type3,col_nb3=st.columns([2,1])
    with col_type3:
        type_lonab3=st.selectbox("Type LONAB BOURSE", [
            "LEGENDE - TOUS BOURSE - Vary 68-92% - Recommande",
            "FOREX - Majeures","FOREX - USD/XOF","FOREX - EUR/XOF",
            "INDICE - US","INDICE - Europe","INDICE - Asie",
            "ACTION - US - TSLA NVDA AAPL","ACTION - Europe","CRYPTO - BTC ETH SOL",
            "ACHETER","VENDRE"
        ], index=0, key="type3_complet")
    with col_nb3:
        nb_matchs3=st.number_input("Nombre actifs", 1, 20, 8, key="nb3_complet")
    nb_slider3=st.slider(f"BOURSE - Nombre actifs - {nb_matchs3} choisis", 1, 20, int(nb_matchs3), key="slider3_complet")
    nb_matchs3=nb_slider3
    
    bourse_markets={
        "FOREX - Majeures": [("EUR/USD",1.0850,""),("GBP/USD",1.2950,""),("USD/JPY",149.20,""),("USD/CHF",0.8950,""),("AUD/USD",0.6450,""),("USD/CAD",1.3650,"")],
        "FOREX - USD/XOF": [("USD/XOF",605.50," XOF"),("EUR/XOF",657.00," XOF"),("GBP/XOF",783.00," XOF")],
        "INDICE - US": [("S&P 500",7623.68,""),("NASDAQ",25955.19,""),("DOW JONES",52215.58,""),("RUSSELL 2000",1850.20,"")],
        "INDICE - Europe": [("CAC 40",8150.20,""),("DAX",19200.50,""),("FTSE 100",8450.30,""),("EURO STOXX 50",4950.80,"")],
        "ACTION - US": [("TSLA",372.22,"$"),("NVDA",210.96,"$"),("AAPL",347.72,"$"),("MSFT",445.20,"$"),("GOOGL",185.30,"$"),("AMZN",210.50,"$"),("META",580.20,"$"),("SPY",520.50,"$")],
        "CRYPTO": [("BTC/USD",crypto_live["BTC"],"$"),("ETH/USD",crypto_live["ETH"],"$"),("SOL/USD",crypto_live["SOL"],"$"),("BNB/USD",620.50,"$"),("XRP/USD",0.52,"$")],
    }
    
    total=st.session_state.nb*3
    for i in range(total):
        d=datetime.now()+timedelta(days=i); nom=jours_fr[d.weekday()]; rnd=random.Random(seed(d,f"bourse_complet_{nb_matchs3}_{type_lonab3}_{i}"))
        is_today=(i==0); jour_label="AUJOURDHUI" if is_today else f"J+{i}"
        with st.expander(f"{jour_label} - {nom} {d.strftime('%d/%m/%Y')} - {nb_matchs3} actifs - {type_lonab3}", expanded=is_today):
            data=[]
            # Selectionne marches selon type
            if "FOREX" in type_lonab3 and "XOF" in type_lonab3: markets_list=bourse_markets["FOREX - USD/XOF"]
            elif "FOREX" in type_lonab3: markets_list=bourse_markets["FOREX - Majeures"]+bourse_markets["FOREX - USD/XOF"]
            elif "INDICE" in type_lonab3 and "US" in type_lonab3: markets_list=bourse_markets["INDICE - US"]
            elif "INDICE" in type_lonab3: markets_list=bourse_markets["INDICE - US"]+bourse_markets["INDICE - Europe"]
            elif "ACTION" in type_lonab3: markets_list=bourse_markets["ACTION - US"]
            elif "CRYPTO" in type_lonab3: markets_list=bourse_markets["CRYPTO"]
            else: markets_list=bourse_markets["FOREX - Majeures"]+bourse_markets["INDICE - US"]+bourse_markets["ACTION - US"]+bourse_markets["CRYPTO"]
            
            selected=rnd.sample(markets_list, min(nb_matchs3, len(markets_list)))
            for name,price,unit in selected:
                attaque_b=rnd.randint(45,88); defense_b=rnd.randint(15,60); diff_b=attaque_b-defense_b; moy_b=round(rnd.uniform(1.2,3.8),1)
                signal="ACHETER" if rnd.randint(0,1)==0 else "VENDRE"
                marche_b=f"{signal} - {type_lonab3}"
                conf=confiance_selon_analyse(attaque_b,defense_b,diff_b,moy_b,marche_b); ai=conf+rnd.randint(-1,2); ai=min(94,max(66,ai))
                if conf>=85: raison=f"{name} Att {attaque_b}% tres fort Diff {diff_b} + {moy_b}"
                elif conf>=78: raison=f"{name} Att {attaque_b}% fort Diff {diff_b}"
                else: raison=f"{name} Att {attaque_b}% Diff {diff_b}"
                # Valeur Risque Benefice
                per=round(rnd.uniform(12.0,45.0),1) if "ACTION" in name or name in ["TSLA","NVDA","AAPL"] else "N/A"
                roe=round(rnd.uniform(3.0,135.0),1) if "ACTION" in name or name in ["TSLA","NVDA","AAPL"] else "N/A"
                beta=round(rnd.uniform(0.8,2.3),2)
                data.append({"Actif":name,"Prix":f"{price}{unit}","Signal":signal,"PER":per,"ROE":f"{roe}%","Risque Beta":beta,"Analyse":f"{raison} - {signal}","Confiance":f"{conf}%","AI%":f"{ai}%","Jour":f"J+{i}"})
            st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)

st.success(f"♾️ V44 COMPLET FINAL - 3 CHAMPIONS - JOUR INFINI {st.session_state.nb*3} JOURS - MISE A JOUR INFINI - FOOT {nb_matchs1} MATCHS + PMU-B {nb_matchs2} COURSES + BOURSE {nb_matchs3} ACTIFS - TOUS TYPES LONAB")
st.warning("⚠️ 18+ JEU RESPONSABLE - LONAB / PMU-B / BOURSE - Pourcentage varie selon analyse 68-92% - Pas garantie")
