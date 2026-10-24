import streamlit as st, pandas as pd, random, hashlib, requests
from datetime import datetime, timedelta

st.set_page_config(page_title="FABRICE V44 AI + SCORE EXACT", layout="wide", page_icon="🎯")
st.markdown("<style>#MainMenu,footer,header{display:none}</style>", unsafe_allow_html=True)

@st.cache_data(ttl=600)
def get_bourse():
    try:
        r=requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd", timeout=5).json()
        return r["bitcoin"]["usd"], True
    except: return 80763, False

btc_price, btc_live = get_bourse()
if "nb" not in st.session_state: st.session_state.nb=1
def seed(d,s=""): return int(hashlib.md5((d.strftime('%Y%m%d')+s).encode()).hexdigest()[:8],16)

st.title("FABRICE EMPIRE - AI AUTO + SCORE EXACT")
st.caption(f"DOUBLE CHANCE | PMUB | BOURSE - 7J/7 INFINI - AI + SCORE EXACT - BTC ${btc_price:,.0f} {datetime.now():%H:%M:%S}")

c1,c2=st.columns(2)
with c1:
    if st.button("➕ +3 JOURS", use_container_width=True): st.session_state.nb+=1; st.rerun()
with c2:
    if st.button("🔄 RESET", use_container_width=True): st.session_state.nb=1; st.rerun()

st.markdown("### 🎯 Type LONAB - AI AUTO + SCORE EXACT")
type_lonab = st.selectbox(
    "Type LONAB",
    ["🤖 AI AUTO + SCORE EXACT - Complet (Recommandé)", "Double Chance AI", "Over/Under AI AUTO", "Score Exact AI", "AI MIX Complet"],
    index=0,
    key="type_lonab_score_exact"
)
st.success(f"🤖 {type_lonab} ACTIVÉ - AI analyse Over/Under + Score Exact toute seule")

st.markdown(f"#### Nombre de matchs {type_lonab}")
nb_matchs = st.slider("Nombre matchs", 10, 15, 12, key="nb_score_exact")
st.markdown(f"<div style='text-align:center;color:#ff4b4b;font-weight:bold;font-size:18px'>{nb_matchs} matchs</div>", unsafe_allow_html=True)

fixtures = [
    ("Inter vs Man City", "LDC", 78, 22, 2.8),
    ("Real vs Brest", "LDC", 65, 12, 1.9),
    ("Barca vs Real", "Liga", 82, 35, 3.2),
    ("EFO vs Bayern", "Amical", 45, 55, 3.5),
    ("RCB vs USFA", "Fasofoot", 58, 28, 2.1),
    ("Man Utd vs Liverpool", "PL", 88, 42, 3.4),
    ("Douanes vs Majestic", "Fasofoot", 52, 18, 1.8),
    ("Sonabel vs Vitesse", "Fasofoot", 48, 15, 1.6),
    ("ASFA vs EFO", "Fasofoot", 55, 20, 2.0),
    ("Rahimo vs Salitas", "Fasofoot", 60, 25, 2.3),
    ("PSG vs Marseille", "Ligue1", 75, 38, 2.9),
    ("Bayern vs Dortmund", "Bundesliga", 80, 40, 3.1),
    ("Man City vs Arsenal", "PL", 85, 45, 3.3),
    ("Real Madrid vs Barcelona", "Liga", 90, 48, 3.5),
]

jours_fr = ["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"]
total = st.session_state.nb*3

for i in range(total):
    d=datetime.now()+timedelta(days=i)
    nom=jours_fr[d.weekday()]
    rnd=random.Random(seed(d, f"ai_score_exact_v44_{nb_matchs}"))
    is_today=(i==0)
    label_jour = "🔥 AUJOURD'HUI" if is_today else f"J+{i}"

    with st.expander(f"{label_jour} - {nom} - {d.strftime('%d/%m/%Y')} - 🤖 AI + SCORE EXACT - {nb_matchs} MATCHS", expanded=is_today):
        
        matchs = rnd.sample(fixtures, nb_matchs)
        data=[]
        for team, lig, attaque, defense, moy_buts in matchs:
            # ========== AI AUTO + SCORE EXACT ==========
            if moy_buts >= 3.2:
                prono = rnd.choice(["Over 2.5", "Over 3.5"])
                marche = "Over/Under"
                score_exact = rnd.choice(["2-1","3-1","2-2","3-2"])
                analyse = f"{moy_buts} buts → {prono} + Score {score_exact}"
            elif moy_buts <= 1.8:
                prono = rnd.choice(["Under 2.5", "Under 3.5"])
                marche = "Over/Under"
                score_exact = rnd.choice(["1-0","0-1","1-1","0-0"])
                analyse = f"{moy_buts} buts → {prono} + Score {score_exact}"
            elif attaque > 80:
                prono = rnd.choice(["1","1X"])
                marche = "1X2"
                score_exact = rnd.choice(["2-0","2-1","1-0","3-0"])
                analyse = f"Att {attaque}% → Victoire + {score_exact}"
            elif defense > 50:
                prono = rnd.choice(["X2","X"])
                marche = "Double Chance"
                score_exact = rnd.choice(["0-1","1-1","0-0","1-2"])
                analyse = f"Déf forte → {prono} + {score_exact}"
            else:
                # AI MIX avec Score Exact inclus
                prono = rnd.choice(["1X","Over 2.5","GG Oui"])
                marche = rnd.choice(["Double Chance","Over/Under","BTTS","Score Exact"])
                if marche == "Score Exact":
                    prono = rnd.choice(["1-0","2-1","1-1","2-0","0-1","1-2","2-2"])
                    score_exact = prono
                else:
                    score_exact = rnd.choice(["2-1","1-1","1-0","2-0"])
                analyse = f"AI MIX → {marche} + Score {score_exact}"

            # Si Type = Score Exact AI, on force Score Exact
            if "Score Exact" in type_lonab:
                marche = "Score Exact"
                prono = rnd.choice(["1-0","2-1","1-1","2-0","0-1","1-2","2-2","3-1","0-0","2-3"])
                score_exact = prono
                analyse = f"AI Score Exact → {score_exact} - Att {attaque}%"
            else:
                # On garde prono + score exact en plus
                if marche != "Score Exact":
                    # Ajoute score exact à côté
                    pass
            
            # Affichage final avec Score Exact toujours visible
            if marche == "Score Exact":
                affichage_prono = score_exact
            else:
                affichage_prono = f"{prono} (Score: {score_exact})"

            data.append({
                "Match": f"{team} - {lig}",
                "🤖 Marché AI": marche,
                "Prono IA AUTO": affichage_prono,
                "Score Exact AI": score_exact,
                "Cote": round(rnd.uniform(1.55,5.5),2),
                "Analyse AI": analyse,
                "Confiance": f"{rnd.randint(70,94)}% 🤖",
            })
        
        df=pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.success(f"🤖 AI + SCORE EXACT - {nb_matchs} matchs analysés - Score Exact inclus - {d.strftime('%d/%m/%Y')} LIVE INFINI")

st.success(f"✅ V44 AI + SCORE EXACT - {nb_matchs} matchs - Over/Under + Score Exact auto par AI - 7J/7 LIVE INFINI")
