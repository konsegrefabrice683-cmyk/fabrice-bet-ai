import streamlit as st, random, hashlib, requests
from datetime import datetime, timedelta

st.set_page_config(page_title="V67 JOUR INFINI BOURSE", layout="wide", page_icon="🌍")
st.markdown("""
<style>
#MainMenu,footer,header{display:none}
.card { border-radius:14px; padding:13px; margin:9px 0; box-shadow:0 2px 8px rgba(0,0,0,0.1); }
.ultra { background:linear-gradient(135deg,#dcfce7 0%,#bbf7d0 100%); border:2px solid #006400; border-left:7px solid #006400; }
.vert { background:#f0fdf4; border:2px solid #16a34a; border-left:6px solid #16a34a; }
.attente { background:#fffbeb; border:2px solid #f59e0b; border-left:6px solid #f59e0b; }
.risque { background:#fef2f2; border:2px solid #ef4444; border-left:6px solid #ef4444; }
.novalue { background:#f3f4f6; border:2px solid #9ca3af; border-left:6px solid #6b7280; }
.piege { background:#1f2937; color:white; border:2px solid #ef4444; border-left:6px solid #ef4444; }
.result-win { background:#16a34a; color:white; padding:6px 12px; border-radius:20px; font-weight:bold; font-size:12px; }
.result-lose { background:#ef4444; color:white; padding:6px 12px; border-radius:20px; font-weight:bold; font-size:12px; }
.result-pending { background:#f59e0b; color:white; padding:6px 12px; border-radius:20px; font-weight:bold; font-size:12px; }
.result-ferme { background:#6b7280; color:white; padding:6px 12px; border-radius:20px; font-weight:bold; font-size:12px; }
.badge { padding:4px 10px; border-radius:20px; font-weight:bold; font-size:11px; color:white; }
.b-ultra{background:#006400}.b-vert{background:#16a34a}.b-orange{background:#f59e0b}.b-rouge{background:#ef4444}.b-gris{background:#6b7280}.b-noir{background:#111827}
.badge-acheter{background:#16a34a}.badge-vendre{background:#ef4444}.badge-ferme{background:#6b7280}
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=60)
def get_bourse():
    try:
        r=requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,binancecoin,ripple&vs_currencies=usd", timeout=5).json()
        return {"BTC":float(r["bitcoin"]["usd"]), "ETH":float(r["ethereum"]["usd"]), "SOL":float(r["solana"]["usd"]), "BNB":float(r["binancecoin"]["usd"]), "XRP":float(r["ripple"]["usd"])}
    except: return {"BTC":80530.0, "ETH":2450.0, "SOL":145.0, "BNB":610.0, "XRP":0.52}

crypto=get_bourse()
if "nb" not in st.session_state: st.session_state.nb=1
def seed(d,s=""): return int(hashlib.md5((d.strftime("%Y%m%d")+s).encode()).hexdigest()[:8],16)
jours=["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"]

teams_pl=["Arsenal","Aston Villa","Man City","Man United","Chelsea","Tottenham","Liverpool","Brighton","Everton","Fulham","Coventry City","Newcastle","West Ham","Crystal Palace","Brentford","Wolves","Nottingham Forest","Bournemouth","Leeds","Burnley"]
teams_liga=["Real Madrid","Barcelona","Atletico Madrid","Valencia","Villarreal","Rayo Vallecano","Elche","Racing Santander","Espanyol","Sevilla","Real Sociedad","Athletic Bilbao","Betis","Girona","Celta Vigo","Osasuna","Getafe","Alaves","Mallorca","Leganes"]
teams_serie=["Inter","AC Milan","Juventus","Napoli","Roma","Lazio","Atalanta","Bologna","Fiorentina","Cagliari","Como","Sassuolo","Parma","Torino","Genoa","Udinese","Lecce","Verona","Empoli","Monza"]
teams_bundes=["Bayern Munich","Dortmund","RB Leipzig","Leverkusen","Frankfurt","Stuttgart","Hoffenheim","Augsburg","Union Berlin","Mainz","Werder Bremen","Köln","Schalke 04","Paderborn","Hamburg","Elversberg","Freiburg","Wolfsburg","Gladbach","Heidenheim"]
teams_ligue1=["PSG","Marseille","Monaco","Lille","Lyon","Lens","Paris FC","Rennes","Strasbourg","Brest","Reims","Toulouse","Montpellier","Nantes","Le Havre","Angers","Saint-Etienne","Auxerre","Metz"]

fixtures_today_real=[
    ("Aston Villa vs Manchester City","PL"),("Arsenal vs Everton","PL"),("Coventry City vs Fulham","PL"),("Chelsea vs Tottenham Hotspur","PL"),
    ("Rayo Vallecano vs Elche","LaLiga"),("Racing Santander vs Espanyol","LaLiga"),("Valencia vs Villarreal","LaLiga"),("Atletico Madrid vs Deportivo","LaLiga"),
    ("Cagliari vs Bologna","Serie A"),("Como vs Sassuolo","Serie A"),("Napoli vs Roma","Serie A"),("Lazio vs Parma","Serie A"),
    ("RB Leipzig vs Elversberg","Bundes"),("Augsburg vs Union Berlin","Bundes"),("Mainz vs Werder Bremen","Bundes"),("Köln vs Schalke 04","Bundes"),("Paderborn vs Hamburg","Bundes"),("Dortmund vs Frankfurt","Bundes"),
    ("Lens vs Paris FC","Ligue 1"),
]

def get_fixtures_infini(rnd, nb_needed):
    fixtures=[]; all_teams=[(teams_pl,"PL"),(teams_liga,"LaLiga"),(teams_serie,"Serie A"),(teams_bundes,"Bundes"),(teams_ligue1,"Ligue 1")]
    used=set(); attempts=0
    while len(fixtures)<nb_needed and attempts<300:
        attempts+=1
        league_teams, league_name=rnd.choice(all_teams)
        t1,t2=rnd.sample(league_teams,2)
        match_str=f"{t1} vs {t2}"
        if match_str in used or f"{t2} vs {t1}" in used: continue
        if "Brest vs Nice" in match_str or "Nice vs Brest" in match_str: continue
        if "Raja" in match_str or "Mamelodi" in match_str: continue
        used.add(match_str)
        lonab=round(rnd.uniform(1.25,3.20),2); juste=round(lonab+rnd.uniform(-0.3,0.6),2)
        proba_val=rnd.randint(28,82); value_val=round((juste-lonab)/lonab*100+rnd.uniform(1,3),1)
        value_str=f"+{value_val}%" if value_val>0 else f"{value_val}%"
        proba_str=f"{proba_val}%"
        if value_val>=5 and proba_val>=60: ia=rnd.randint(74,80); statut="FEU VERT ULTRA"
        elif value_val>=3 and proba_val>=55: ia=rnd.randint(71,77); statut="FEU VERT"
        elif value_val>=0: ia=rnd.randint(60,72); statut="ATTENTE"
        elif value_val>=-3: ia=rnd.randint(50,65); statut="RISQUE"
        elif value_val>=-8: ia=rnd.randint(40,55); statut="NO VALUE"
        else: ia=rnd.randint(30,50); statut="PIEGE"
        fixtures.append((match_str, league_name, lonab, juste, proba_str, value_str, ia, statut))
    return fixtures

def simuler_resultat_foot(rnd):
    s1=rnd.randint(0,4); s2=rnd.randint(0,3); return f"{s1}-{s2}", rnd.choice([True, True, False])

def simuler_resultat_bourse_avec_statut(rnd, marche_nom, jour_weekday):
    # ✅ LOGIQUE ACHETER / VENDRE / FERME SELON JOUR + MARCHE
    is_weekend = jour_weekday in [5,6]  # Samedi Dimanche
    is_crypto = "BTC" in marche_nom or "ETH" in marche_nom or "SOL" in marche_nom or "BNB" in marche_nom or "XRP" in marche_nom
    
    # Crypto = jamais fermé (24/7)
    if is_crypto:
        variation=rnd.uniform(-4.5,5.5)
        if variation>=2: action="ACHETER"; gagne=True
        elif variation<=-2: action="VENDRE"; gagne=True
        elif variation>0: action="ACHETER"; gagne=rnd.choice([True,False])
        else: action="VENDRE"; gagne=rnd.choice([True,False])
        statut_marche="OUVERT 24/7"
    # Forex / Bourse = fermé weekend
    elif is_weekend:
        variation=0.0
        action="FERME"
        gagne=False
        statut_marche="FERME WEEKEND"
    else:
        variation=rnd.uniform(-3.5,4.0)
        if variation>=1.5: action="ACHETER"; gagne=True
        elif variation<=-1.5: action="VENDRE"; gagne=True
        elif variation>0.3: action="ACHETER"; gagne=rnd.choice([True, True, False])
        elif variation<-0.3: action="VENDRE"; gagne=rnd.choice([True, True, False])
        else: action="FERME"; gagne=False; variation=0.0
        statut_marche="OUVERT" if action!="FERME" else "FERME"
    
    return round(variation,2), action, statut_marche

def afficher_cards_avec_resultats(liste, type_match, rnd, jour_passe, jour_weekday):
    for idx, m in enumerate(liste):
        match_str, ligue, lonab, juste, proba, value, ia, statut=m
        if "ULTRA" in statut: typ="ultra"; badge="b-ultra"
        elif "FEU VERT" in statut: typ="vert"; badge="b-vert"
        elif "ATTENTE" in statut: typ="attente"; badge="b-orange"
        elif "RISQUE" in statut: typ="risque"; badge="b-rouge"
        elif "NO VALUE" in statut: typ="novalue"; badge="b-gris"
        else: typ="piege"; badge="b-noir"
        text_color="color:white;" if typ=="piege" else ""
        analyse_bg="background:#111827; color:#d1d5db;" if typ=="piege" else "background:#f9fafb; color:#555;"
        
        if type_match=="FOOT":
            score, gagne=simuler_resultat_foot(random.Random(seed(datetime.now(), f"res_foot_{match_str}_{idx}")))
            if jour_passe:
                result_badge=f'<span class="result-win">✅ GAGNE {score}</span>' if gagne else f'<span class="result-lose">❌ PERDU {score}</span>'
                result_text=f"Score: {score} | {'GAGNE ✅' if gagne else 'PERDU ❌'} | {'+'+str(int((lonab-1)*3000))+'F' if gagne else '-3000F'}"
            else:
                result_badge='<span class="result-pending">⏳ EN COURS</span>'
                result_text=f"Score estimé: {score} - En attente"
            action_badge=""
        elif type_match=="PMU":
            arrivee=["1","7","5"]; gagne=rnd.choice([True, False, True])
            if jour_passe:
                result_badge=f'<span class="result-win">✅ GAGNE {"-".join(arrivee)}</span>' if gagne else f'<span class="result-lose">❌ PERDU {"-".join(arrivee)}</span>'
                result_text=f"Arrivée: {'-'.join(arrivee)} | {'GAGNE ✅' if gagne else 'PERDU ❌'}"
            else:
                result_badge='<span class="result-pending">⏳ COURSE A VENIR</span>'
                result_text=f"Arrivée estimée: {'-'.join(arrivee)}"
            action_badge=""
        else:  # BOURSE AVEC ACHETER VENDRE FERME
            var, action, statut_marche = simuler_resultat_bourse_avec_statut(rnd, match_str, jour_weekday)
            if action=="ACHETER": action_badge='<span class="badge badge-acheter">🟢 ACHETER</span>'
            elif action=="VENDRE": action_badge='<span class="badge badge-vendre">🔴 VENDRE</span>'
            else: action_badge='<span class="badge badge-ferme">⚪ FERME</span>'
            
            if jour_passe or True:  # Bourse = toujours resultat car crypto 24/7
                if action=="FERME":
                    result_badge='<span class="result-ferme">⚪ FERME</span>'
                    result_text=f"{statut_marche} | Marché fermé | Pas de trade"
                elif var>0:
                    result_badge=f'<span class="result-win">✅ +{var:.2f}%</span>' if var>1 else f'<span class="result-win">✅ GAGNE {var:+.2f}%</span>'
                    result_text=f"Variation: {var:+.2f}% | {action} | {'GAGNE ✅' if var>0.5 else 'PERDU ❌'} | {statut_marche}"
                else:
                    result_badge=f'<span class="result-lose">❌ {var:.2f}%</span>' if var<-1 else f'<span class="result-lose">❌ PERDU {var:+.2f}%</span>'
                    result_text=f"Variation: {var:+.2f}% | {action} | {'GAGNE ✅' if var<-0.5 and action=='VENDRE' else 'PERDU ❌'} | {statut_marche}"
            else:
                result_badge='<span class="result-pending">⏳ MARCHE OUVERT</span>'
                result_text=f"Variation estimée: {var:+.2f}% - En attente"
        
        st.markdown(f"""
        <div class="card {typ}" style="{text_color}">
          <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:5px;">
            <b>{match_str}</b>
            <div style="display:flex; gap:5px; align-items:center; flex-wrap:wrap;">
              <span class="badge {badge}">{statut} {ia}%</span> {action_badge} {result_badge}
            </div>
          </div>
          <div style="margin-top:8px; font-size:13px; font-family:monospace;">
            {ligue} | LONAB <b>{lonab:.2f}</b> vs Juste <b>{juste:.2f}</b> | Proba <b>{proba}</b> | Value <b>{value}</b> | IA <b>{ia}%</b>
          </div>
          <div style="font-size:11px; margin-top:6px; padding:6px; border-radius:8px; {analyse_bg}">📊 {statut} | {ligue}</div>
          <div style="margin-top:8px; font-size:12px; font-weight:bold; background:#000; color:#0f0; padding:6px; border-radius:8px; font-family:monospace;">
            🏆 RESULTAT: {result_text}
          </div>
        </div>
        """, unsafe_allow_html=True)

bourse_complete={"FOREX MAJEURES":[("EUR/USD",1.0850,""),("GBP/USD",1.2950,""),("USD/JPY",154.20,""),("AUD/USD",0.6650,"")],"FOREX XOF":[("USD/XOF",605.50," XOF"),("EUR/XOF",657.00," XOF"),("GBP/XOF",785.00," XOF")],"INDICE US":[("S&P 500",7623.68,""),("NASDAQ",25955.19,""),("DOW JONES",42800.00,"")],"ACTION US TECH":[("TSLA",372.22,"$"),("NVDA",210.96,"$"),("AAPL",347.72,"$"),("MSFT",415.32,"$"),("SONATEL",18500,"F"),("ONATEL BF",3420,"F"),("ORANGE CI",11200,"F")],"CRYPTO":[("BTC/USD",crypto["BTC"],"$"),("ETH/USD",crypto["ETH"],"$"),("SOL/USD",crypto["SOL"],"$"),("BNB/USD",crypto["BNB"],"$"),("XRP/USD",crypto["XRP"],"$"),("GOLD",2650.30,"$/oz"),("PETROLE WTI",78.50,"$")]}

st.title("🌍 V67 FINAL - JOUR INFINI BOURSE + ACHETER VENDRE FERME + RESULTATS")
st.caption(f"JOUR INFINI ACTIF POUR FOOT + PMU + BOURSE + ACHETER VENDRE FERME + RESULTATS - {datetime.now():%d/%m/%Y}")

col1,col2,col3,col4,col5=st.columns(5)
with col1:
    if st.button("➕ 3 JOURS", use_container_width=True): st.session_state.nb+=1; st.rerun()
with col2:
    if st.button("➕ 30 JOURS", use_container_width=True): st.session_state.nb+=10; st.rerun()
with col3:
    if st.button("➕ 90 JOURS", use_container_width=True): st.session_state.nb+=30; st.rerun()
with col4:
    if st.button("➕ 365 JOURS", use_container_width=True): st.session_state.nb+=122; st.rerun()
with col5:
    if st.button("RESET", use_container_width=True): st.session_state.nb=1; st.rerun()

st.info(f"✅ JOUR INFINI: {st.session_state.nb*3} jours = J0 à J+{st.session_state.nb*3-1} | FOOT: 19 matchs J0 + 15 matchs J+1 à J+365 | PMU: 7 chevaux chaque jour | BOURSE: JOUR INFINI AVEC ACHETER/VENDRE/FERME - Crypto 24/7, Forex/Bourse fermé weekend")

tab1,tab2,tab3=st.tabs(["🏆 FOOT JOUR INFINI + RESULTATS","🏆 PMU-B JOUR INFINI + RESULTATS","🌍 BOURSE JOUR INFINI + ACHETER VENDRE FERME + RESULTATS"])

with tab1:
    total=st.session_state.nb*3
    for i in range(total):
        d=datetime.now()+timedelta(days=i); nom=jours[d.weekday()]; rnd=random.Random(seed(d,f"v67_foot_{i}"))
        jour_passe=i==0
        if i==0:
            fixtures=[]
            for match_str, ligue in fixtures_today_real:
                lonab=round(rnd.uniform(1.25,3.20),2); juste=round(lonab+rnd.uniform(-0.3,0.6),2)
                proba_val=rnd.randint(28,82); value_val=round((juste-lonab)/lonab*100+rnd.uniform(1,3),1)
                value_str=f"+{value_val}%" if value_val>0 else f"{value_val}%"
                proba_str=f"{proba_val}%"
                if value_val>=5 and proba_val>=60: ia=rnd.randint(74,80); statut="FEU VERT ULTRA"
                elif value_val>=3 and proba_val>=55: ia=rnd.randint(71,77); statut="FEU VERT"
                elif value_val>=0: ia=rnd.randint(60,72); statut="ATTENTE"
                elif value_val>=-3: ia=rnd.randint(50,65); statut="RISQUE"
                elif value_val>=-8: ia=rnd.randint(40,55); statut="NO VALUE"
                else: ia=rnd.randint(30,50); statut="PIEGE"
                fixtures.append((match_str, ligue, lonab, juste, proba_str, value_str, ia, statut))
            label=f"AUJOURD'HUI 🔥 24/10/2026 - RESULTATS - 19 matchs"
        else:
            fixtures=get_fixtures_infini(rnd, 15)
            label=f"J+{i} - {nom} {d.strftime('%d/%m/%Y')} - 15 matchs"
        with st.expander(label, expanded=(i<2)):
            afficher_cards_avec_resultats(fixtures, "FOOT", rnd, jour_passe, d.weekday())

with tab2:
    chevaux_pool=[("1","Mogho Power",2.1),("7","Bangr Nooma",3.2),("5","Etalon dOr",3.8),("3","Wend Panga",4.5),("2","Roi du Sahel",5.5),("8","Faso Vitesse",6.8),("12","Bobo Sprint",12.0)]
    type2=st.selectbox("Type PMU-B", ["Gagnant","Placé","Couplé Gagnant","Couplé Placé","Tiercé","Quarté","Quinté+"], index=0, key="t2v67")
    total=st.session_state.nb*3
    for i in range(total):
        d=datetime.now()+timedelta(days=i); nom=jours[d.weekday()]; rnd=random.Random(seed(d,f"v67_pmu_{type2}_{i}"))
        jour_passe=i==0
        with st.expander(f"{'AUJOURD HUI' if i==0 else f'J+{i}'} - {nom} {d.strftime('%d/%m/%Y')} - PMU {type2} JOUR INFINI", expanded=(i==0)):
            rows=[]
            for num,nom_ch,cote_lonab in rnd.sample(chevaux_pool,7):
                juste=round(cote_lonab+rnd.uniform(-0.5,1.5),2)
                proba_val=rnd.randint(8,65)
                value_val=round((juste-cote_lonab)/cote_lonab*100+rnd.uniform(-1,4),1)
                if value_val>=5: ia=rnd.randint(74,80); statut="FEU VERT ULTRA"
                elif value_val>=3: ia=rnd.randint(71,77); statut="FEU VERT"
                elif value_val>=0: ia=rnd.randint(60,72); statut="ATTENTE"
                elif value_val>=-3: ia=rnd.randint(50,65); statut="RISQUE"
                elif value_val>=-8: ia=rnd.randint(40,55); statut="NO VALUE"
                else: ia=rnd.randint(30,45); statut="PIEGE"
                value_str=f"+{value_val}%" if value_val>0 else f"{value_val}%"
                rows.append((f"N°{num} {nom_ch}", "PMU", cote_lonab, juste, f"{proba_val}%", value_str, ia, statut))
            afficher_cards_avec_resultats(rows, "PMU", rnd, jour_passe, d.weekday())

with tab3:
    st.markdown("### 🌍 BOURSE INTERNATIONALE JOUR INFINI + ACHETER VENDRE FERME")
    st.warning("🟢 ACHETER = Hausse prévue | 🔴 VENDRE = Baisse prévue | ⚪ FERME = Marché fermé weekend - Crypto 24/7 toujours ouvert")
    type3=st.selectbox("Type BOURSE", ["FOREX MAJEURES","FOREX XOF","INDICE US","ACTION US TECH","CRYPTO"], index=4, key="t3v67")
    total=st.session_state.nb*3
    for i in range(total):
        d=datetime.now()+timedelta(days=i); nom=jours[d.weekday()]; rnd=random.Random(seed(d,f"v67_bourse_{type3}_{i}"))
        jour_passe=i==0
        is_weekend = d.weekday() in [5,6]
        statut_jour = "⚪ FERME WEEKEND" if is_weekend and type3!="CRYPTO" else "🟢 OUVERT" if not is_weekend else "🟢 OUVERT 24/7 CRYPTO"
        with st.expander(f"{'AUJOURD HUI' if i==0 else f'J+{i}'} - {nom} {d.strftime('%d/%m/%Y')} - {type3} - {statut_jour} - JOUR INFINI", expanded=(i<3)):
            if "FOREX MAJEURES" in type3: markets=bourse_complete["FOREX MAJEURES"]
            elif "FOREX XOF" in type3: markets=bourse_complete["FOREX XOF"]
            elif "INDICE US" in type3: markets=bourse_complete["INDICE US"]
            elif "ACTION US TECH" in type3: markets=bourse_complete["ACTION US TECH"]
            else: markets=bourse_complete["CRYPTO"]
            rows=[]
            for name,price,unit in [rnd.choice(markets) for _ in range(8)]:  # 8 pour montrer tous acheter vendre ferme
                juste=round(price*rnd.uniform(0.92,1.12),2)
                proba_val=rnd.randint(35,80)
                value_val=round((juste-price)/price*100,1)
                if value_val>=3 and proba_val>=60: ia=rnd.randint(74,80); statut="FEU VERT ULTRA"
                elif value_val>=1: ia=rnd.randint(70,76); statut="FEU VERT"
                elif value_val>=0: ia=rnd.randint(60,70); statut="ATTENTE"
                elif value_val>=-2: ia=rnd.randint(50,62); statut="RISQUE"
                elif value_val>=-5: ia=rnd.randint(40,53); statut="NO VALUE"
                else: ia=rnd.randint(30,45); statut="PIEGE SURACHETE"
                value_str=f"+{value_val}%" if value_val>0 else f"{value_val}%"
                # Pour bourse, ligue = action va être recalculée dans afficher
                rows.append((f"{name} {price}{unit}", "BOURSE", price, juste, f"{proba_val}%", value_str, ia, statut))
            afficher_cards_avec_resultats(rows, "BOURSE", rnd, jour_passe, d.weekday())

st.success("✅ V67 - JOUR INFINI POUR TOUS: FOOT 19 matchs J0 + 15 matchs J+1 à J+365 | PMU 7 chevaux chaque jour J0 à J+365 | BOURSE 8 assets chaque jour J0 à J+365 + ACHETER VENDRE FERME + Crypto 24/7 + Forex/Bourse fermé weekend + RESULTATS")
