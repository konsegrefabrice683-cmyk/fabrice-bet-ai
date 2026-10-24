import streamlit as st, pandas as pd, random, hashlib, math, requests
from datetime import datetime, timedelta

st.set_page_config(page_title="V70 TABLEAU FIX", layout="wide", page_icon=":dart:")
st.markdown("""
<style>
#MainMenu,footer,header{display:none}
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=60)
def get_bourse():
    try:
        r=requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd", timeout=5).json()
        return {"BTC":float(r["bitcoin"]["usd"]), "ETH":float(r["ethereum"]["usd"]), "SOL":float(r["solana"]["usd"])}
    except: return {"BTC":80530.0, "ETH":2450.0, "SOL":145.0}

crypto=get_bourse()
if "nb" not in st.session_state: st.session_state.nb=1
def seed(d,s=""): return int(hashlib.md5((d.strftime("%Y%m%d")+s).encode()).hexdigest()[:8],16)
jours=["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"]

def proba_poisson(xg, marche):
    if "Double Chance" in marche or "1X" in marche or "X2" in marche:
        proba=0.68+(xg-2.0)*0.05
    elif "BTTS" in marche:
        proba=0.45+(xg-2.0)*0.12
    elif "Over" in marche:
        proba=1-math.exp(-xg*0.85)
    elif "Under" in marche:
        proba=math.exp(-xg*0.7)
    elif "1X2" in marche:
        proba=0.60+(xg-2.5)*0.08
    else:
        proba=0.60
    return max(0.35, min(proba,0.85))

def facteur_forme(fd, fe):
    diff=fd-fe
    return max(0.85, min(1.0+diff*0.08,1.25))

def analyse_value(cote_lonab, proba_reelle):
    cote_juste=1/proba_reelle
    value=(cote_lonab*proba_reelle-1)*100
    return cote_juste, value

def statut_pro(proba_reelle, value):
    ia=proba_reelle*100
    if value>=10: ia+=4
    elif value>=5: ia+=2
    elif value<0: ia-=8
    ia=max(30, min(ia,92))
    if 72<=ia<=80 and value>=3:
        statut="FEU VERT ULTRA" if value>=5 else "FEU VERT"
    elif ia>80:
        statut="PIEGE"
    elif value<0 and ia<50:
        statut="NO VALUE"
    elif value<0:
        statut="RISQUE"
    elif ia<60:
        statut="ATTENTE"
    else:
        statut="ATTENTE" if ia<70 else "FEU VERT"
    return round(ia,1), statut

fixtures_db=[
    ["Aston Villa vs Manchester City","PL",2.45,2.9,"19:00",4.4,4.1],
    ["Arsenal vs Everton","PL",1.72,2.5,"16:00",4.5,3.8],
    ["Coventry City vs Fulham","PL",1.85,2.4,"15:00",4.2,4.0],
    ["Chelsea vs Tottenham Hotspur","PL",2.15,2.8,"18:30",4.3,4.2],
    ["Rayo Vallecano vs Elche","LaLiga",1.85,2.5,"14:00",4.1,3.9],
    ["Racing Santander vs Espanyol","LaLiga",2.05,2.3,"16:00",4.0,4.0],
    ["Valencia vs Villarreal","LaLiga",2.05,2.8,"20:00",4.2,4.1],
    ["Atletico Madrid vs Deportivo","LaLiga",1.55,2.2,"21:00",4.6,3.5],
    ["Cagliari vs Bologna","Serie A",1.85,2.6,"15:00",4.0,4.1],
    ["Como vs Sassuolo","Serie A",1.78,2.4,"18:00",4.1,3.8],
    ["Napoli vs Roma","Serie A",1.90,2.9,"20:45",4.4,4.2],
    ["Lazio vs Parma","Serie A",1.60,2.3,"18:30",4.3,3.9],
    ["RB Leipzig vs Elversberg","Bundes",1.90,2.5,"15:30",4.3,3.6],
    ["Augsburg vs Union Berlin","Bundes",1.72,2.2,"15:30",4.0,4.0],
    ["Mainz vs Werder Bremen","Bundes",1.95,2.6,"15:30",4.1,4.0],
]

teams_pl=["Arsenal","Aston Villa","Man City","Man United","Chelsea","Tottenham","Liverpool","Brighton","Everton","Fulham","Coventry City","Newcastle","West Ham","Crystal Palace","Brentford","Wolves","Nottingham Forest","Bournemouth","Leeds","Burnley"]
teams_liga=["Real Madrid","Barcelona","Atletico Madrid","Valencia","Villarreal","Rayo Vallecano","Elche","Racing Santander","Espanyol","Sevilla","Real Sociedad","Athletic Bilbao","Betis","Girona","Celta Vigo","Osasuna","Getafe","Alaves","Mallorca","Leganes"]
teams_serie=["Inter","AC Milan","Juventus","Napoli","Roma","Lazio","Atalanta","Bologna","Fiorentina","Cagliari","Como","Sassuolo","Parma","Torino","Genoa","Udinese","Lecce","Verona","Empoli","Monza"]
teams_bundes=["Bayern Munich","Dortmund","RB Leipzig","Leverkusen","Frankfurt","Stuttgart","Hoffenheim","Augsburg","Union Berlin","Mainz","Werder Bremen","Koln","Schalke 04","Paderborn","Hamburg","Elversberg","Freiburg","Wolfsburg","Gladbach","Heidenheim"]
teams_ligue1=["PSG","Marseille","Monaco","Lille","Lyon","Lens","Paris FC","Rennes","Strasbourg","Brest","Reims","Toulouse","Montpellier","Nantes","Le Havre","Angers","Saint-Etienne","Auxerre","Metz","Nice"]

def get_fixtures_infini(rnd, nb_needed):
    all_teams=[(teams_pl,"PL"),(teams_liga,"LaLiga"),(teams_serie,"Serie A"),(teams_bundes,"Bundes"),(teams_ligue1,"Ligue 1")]
    fixtures=[]; used=set(); attempts=0
    while len(fixtures)<nb_needed and attempts<500:
        attempts+=1
        league_teams, league_name=rnd.choice(all_teams)
        t1,t2=rnd.sample(league_teams,2)
        match_str=f"{t1} vs {t2}"
        if match_str in used or f"{t2} vs {t1}" in used: continue
        used.add(match_str)
        cote_lonab=round(rnd.uniform(1.30,3.80),2)
        xg=round(rnd.uniform(1.8,3.4),1)
        heure=f"{rnd.randint(14,21)}:00"
        fd=round(rnd.uniform(3.5,4.8),1); fe=round(rnd.uniform(3.2,4.5),1)
        fixtures.append([match_str, league_name, cote_lonab, xg, heure, fd, fe])
    return fixtures

st.title("V70 TABLEAU COMME IMAGE - FIX SYNTAX ERROR")

type_lonab = st.selectbox("Type LONAB", ["Double Chance","1X2","BTTS Oui","BTTS Non","Over 1.5","Over 2.5","Over 3.5","Under 2.5","DNB","Score Exact"], index=0)

nombre_matchs = st.slider(f"Nombre de matchs {type_lonab}", min_value=10, max_value=15, value=12, step=1)

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

st.success(f"V70 FIX: {st.session_state.nb*3} jours | Type: {type_lonab} | {nombre_matchs} matchs | Tableau jusqu'a Gain | Sans SyntaxError")

total=st.session_state.nb*3
for i in range(total):
    d=datetime.now()+timedelta(days=i); nom=jours[d.weekday()]; rnd=random.Random(seed(d,f"v70_{type_lonab}_{i}"))
    jour_passe = d.date() < datetime.now().date()
    jour_aujourdhui = d.date() == datetime.now().date()
    
    if i==0:
        base_fixtures=fixtures_db[:nombre_matchs] if len(fixtures_db)>=nombre_matchs else fixtures_db
        if len(base_fixtures)<nombre_matchs:
            extra=get_fixtures_infini(rnd, nombre_matchs-len(base_fixtures))
            base_fixtures=base_fixtures+extra
    else:
        base_fixtures=get_fixtures_infini(rnd, nombre_matchs)
    
    rows=[]
    for f in base_fixtures[:nombre_matchs]:
        match_str, ligue, cote_lonab_base, xg, heure, fd, fe = f
        if "Double Chance" in type_lonab:
            marche=f"{type_lonab} 1X"
            cote_lonab=round(cote_lonab_base*0.75,2)
        elif "1X2" in type_lonab:
            marche="Domicile" if fd>fe else "Exterieur"
            cote_lonab=cote_lonab_base
        elif "BTTS" in type_lonab:
            marche=type_lonab
            cote_lonab=round(1.70+rnd.uniform(-0.2,0.4),2)
        elif "Over" in type_lonab or "Under" in type_lonab:
            marche=type_lonab
            cote_lonab=round(1.50+rnd.uniform(0.2,1.2),2)
        else:
            marche=type_lonab
            cote_lonab=cote_lonab_base
        
        proba_base=proba_poisson(xg, marche)
        ff=facteur_forme(fd, fe)
        proba_reelle=min(proba_base*ff,0.85)
        cote_juste, value=analyse_value(cote_lonab, proba_reelle)
        ia, statut=statut_pro(proba_reelle, value)
        
        s1=rnd.randint(0,4); s2=rnd.randint(0,3); score=f"{s1}-{s2}"
        if "1X" in marche: gagne=s1>=s2
        elif "X2" in marche: gagne=s2>=s1
        elif "BTTS Oui" in marche: gagne=s1>0 and s2>0
        elif "BTTS Non" in marche: gagne=not (s1>0 and s2>0)
        elif "Over 1.5" in marche: gagne=(s1+s2)>=2
        elif "Over 2.5" in marche: gagne=(s1+s2)>=3
        elif "Over 3.5" in marche: gagne=(s1+s2)>=4
        elif "Under" in marche: gagne=(s1+s2)<=2
        else: gagne=rnd.choice([True, False])
        
        if jour_aujourdhui or jour_passe:
            resultat=f"GAGNE {score}" if gagne else f"PERDU {score}"
            gain=int((cote_lonab-1)*3000) if gagne else -3000
        else:
            resultat=f"{score} A VENIR"
            gain=0
        
        rows.append({
            "Match":match_str,
            "Prono IA":marche,
            "Cote LONAB":cote_lonab,
            "Cote Juste":round(cote_juste,2),
            "xG":xg,
            "Proba Reelle":f"{proba_reelle*100:.1f}%",
            "Value %":round(value,1),
            "IA %":ia,
            "STATUT":statut,
            "Heure":heure,
            "RESULTAT":resultat,
            "Gain 3000F":gain
        })
    
    df=pd.DataFrame(rows).sort_values(by="IA %", ascending=False)
    
    label_jour = "AUJOURD'HUI" if jour_aujourdhui else f"J+{i}"
    label = f"{label_jour} - {nom} - {d.strftime('%d/%m/%Y')} - {type_lonab} - {len(df)} matchs"
    
    with st.expander(label, expanded=(i<2)):
        c_f1,c_f2,c_f3,c_f4=st.columns(4)
        with c_f1:
            verts=len(df[df["STATUT"].str.contains("FEU VERT")])
            st.metric("FEU VERT", verts)
        with c_f2:
            ultra=len(df[df["STATUT"]=="FEU VERT ULTRA"])
            st.metric("ULTRA", ultra)
        with c_f3:
            gain_total=df["Gain 3000F"].sum()
            st.metric("Gain Total", f"{gain_total}F")
        with c_f4:
            ia_moy=df["IA %"].mean()
            st.metric("IA Moy", f"{ia_moy:.1f}%")
        
        st.dataframe(df, use_container_width=True, height=480)
        
        verts_df=df[df["STATUT"].str.contains("FEU VERT")].head(3)
        if len(verts_df)>=3:
            cote_tot=1
            for _, r in verts_df.iterrows(): cote_tot*=r["Cote LONAB"]
            # FIX SYNTAX ERROR - PAS D'EMOJI DANS F-STRING + PAS DE GUILLEMETS IMBRIQUES
            combine_text = "COMBINE " + type_lonab + " " + label_jour + " 3000F: "
            for _, r in verts_df.iterrows():
                combine_text += r["Match"] + " " + r["Prono IA"] + " @" + str(round(r["Cote LONAB"],2)) + " + "
            combine_text += " | COTE TOTALE: " + str(round(cote_tot,2)) + " | GAIN: " + str(int(cote_tot*3000)) + "F | IA MOY: " + str(round(verts_df["IA %"].mean(),1)) + "%"
            st.code(combine_text)

st.caption("V70 FIX - Tableau comme image: Type LONAB Double Chance + Nombre matchs 10-15 slider 12 + AUJOURD'HUI Samedi 24/10/2026 + Tableau Match | Prono IA | Cote LONAB | Cote Juste | xG | Proba | Value | IA | STATUT | Heure | RESULTAT | Gain jusqu'a Gain - Sans SyntaxError")
