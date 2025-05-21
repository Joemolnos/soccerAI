import streamlit as st
from datetime import date
from api import get_team_id_by_name, find_fixture_id, get_prediction_by_fixture_id, get_fixtures_by_date
import os

st.set_page_config(
    page_title="Foci Meccs Előrejelző",
    layout="wide",
    page_icon="⚽"
)

# ---- Custom CSS & Google Fonts ----
st.markdown('''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;900&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Montserrat', sans-serif !important;
        background: linear-gradient(135deg, #1de9b6 0%, #1dc8e9 100%) !important;
    }
    .main {
        background: linear-gradient(135deg, #f8fafc 0%, #e0f7fa 100%) !important;
        border-radius: 24px;
        padding: 2rem 2rem 1rem 2rem;
        margin-top: 1.5rem;
        box-shadow: 0 6px 32px 0 rgba(30, 136, 229, 0.1);
    }
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #212121 0%, #1565c0 100%) !important;
        color: #fff !important;
    }
    .css-1v0mbdj, .stButton>button {
        background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 12px !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        padding: 0.6em 2em !important;
        margin-top: 0.5em;
        box-shadow: 0 2px 8px 0 rgba(30, 136, 229, 0.1);
        transition: 0.2s;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #38f9d7 0%, #43e97b 100%) !important;
        color: #222 !important;
        box-shadow: 0 6px 16px 0 rgba(30, 136, 229, 0.15);
    }
    .prediction-card {
        background: linear-gradient(135deg, #fff 0%, #e3f2fd 100%);
        border-radius: 18px;
        padding: 1.5rem 2rem;
        box-shadow: 0 2px 12px 0 rgba(30, 136, 229, 0.10);
        margin-top: 1.5rem;
    }
    .badge {
        display: inline-block;
        padding: 0.5em 1.2em;
        border-radius: 16px;
        font-size: 1.1rem;
        font-weight: 700;
        margin: 0.2em 0.4em;
        background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%);
        color: #fff;
        box-shadow: 0 2px 8px 0 rgba(30, 136, 229, 0.08);
    }
    .api-status {
        display: inline-block;
        padding: 0.3em 1em;
        border-radius: 16px;
        font-size: 1rem;
        font-weight: 600;
        margin-top: 0.8em;
        background: #f44336;
        color: #fff;
    }
    .api-status.ok {
        background: #43e97b;
    }
    .stTextInput>div>input, .stDateInput>div>input {
        border-radius: 10px;
        border: 1.5px solid #1de9b6;
        background: #f8fafc;
        padding: 0.6em 1em;
        font-size: 1.1rem;
    }
    </style>
''', unsafe_allow_html=True)

# ---- Sidebar ----
api_key = os.getenv("API_FOOTBALL_KEY", "YOUR_API_KEY_HERE")
api_status = "OK" if api_key and api_key != "YOUR_API_KEY_HERE" else "DEMÓ"
api_status_class = "ok" if api_status == "OK" else ""
with st.sidebar:
    st.markdown("""
    <div style='font-size:2.4rem; font-weight:800; margin-bottom:0.2em; text-align:center;'>⚽</div>
    <div style='font-size:1.7rem; font-weight:800; text-align:center; letter-spacing:1px; margin-bottom:0.5em;'>SoccerAI</div>
    <div style='background: linear-gradient(90deg,#e0f7fa,#fffde7); border-radius:18px; padding:1.1em 0.7em 0.7em 0.7em; margin-bottom:1em;'>
        <div style='font-size:1.13rem; color:#374151; font-weight:500; text-align:center;'>
            <span style='font-size:1.5em;'>🚀</span> "A foci nem szerencse kérdése, hanem elemzés!"
        </div>
    </div>
    <div style='background:#f5f5f5; border-radius:14px; padding:0.7em 1em; margin-bottom:1em;'>
        <div style='color:#1565c0; font-weight:600; font-size:1.08rem; text-align:center;'>
            <span style='font-size:1.3em;'>📈</span> Élő predikciók, valós adatokkal
        </div>
    </div>
    <div style='background:#fffde7; border-radius:14px; padding:0.7em 1em; margin-bottom:1em;'>
        <div style='color:#8d6e63; font-weight:600; font-size:1.08rem; text-align:center;'>
            <span style='font-size:1.3em;'>🏟️</span> Több ezer meccs statisztika
        </div>
    </div>
    <div style='background:#e8f5e9; border-radius:14px; padding:0.7em 1em; margin-bottom:1.2em;'>
        <div style='color:#388e3c; font-weight:600; font-size:1.08rem; text-align:center;'>
            <span style='font-size:1.3em;'>💡</span> Tipp: Próbáld ki a különböző ligákat!
        </div>
    </div>
    <div style='display:flex; justify-content:center; margin-bottom:1.5em;'>
        <span style='background:#00c853; color:#fff; padding:0.5em 1.2em; border-radius:22px; font-weight:700; font-size:1.09rem; display:inline-flex; align-items:center;'>
            <span style='font-size:1.2em; margin-right:0.4em;'>✔️</span> Kapcsolódva az API-hoz!
        </span>
    </div>
    <div style='font-size:0.97rem; color:#bdbdbd; text-align:center;'>SoccerAI &copy; 2025</div>
    """, unsafe_allow_html=True)
    if api_status != "OK":
        st.warning("Add meg az API_FOOTBALL_KEY környezeti változót a valódi predikciókhoz!")

# ---- Fő tartalom ----
st.markdown("""
<div class='main'>
    <h1 style='font-size:2.7rem; font-weight:900; background: linear-gradient(90deg,#1de9b6,#1dc8e9); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom:0.6em;'>
        Foci meccs előrejelző
    </h1>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([4,2])
with col1:
    match_date = st.date_input("📅 Meccs dátuma", value=date.today())

# Meccsek listázása az adott napon (1 API-hívás)
fixtures = get_fixtures_by_date(match_date)
fixture_options = []
fixture_map = {}
for f in fixtures:
    label = f"{f['home_team']} - {f['away_team']} | {f['league']} ({f['country']}) | {f['time'][11:16]}"
    fixture_options.append(label)
    fixture_map[label] = f['fixture_id']

selected_fixture_label = None
if fixture_options:
    selected_fixture_label = st.selectbox("Válassz elérhető meccset:", fixture_options)
else:
    st.info("Nincs elérhető mérkőzés ezen a napon az API-ban.")

st.markdown("<div style='margin-top:1.2em'></div>", unsafe_allow_html=True)
predict_btn = st.button("🔮 Előrejelzés!")

if predict_btn:
    with st.spinner("Predikció generálása..."):
        if not api_key or api_key == "YOUR_API_KEY_HERE":
            st.error("API-kulcs nincs megadva! Add meg az API_FOOTBALL_KEY környezeti változót.")
        elif not selected_fixture_label:
            st.warning("Nincs kiválasztott mérkőzés!")
        else:
            fixture_id = fixture_map[selected_fixture_label]
            pred = get_prediction_by_fixture_id(fixture_id)
            if not pred or not pred.get('response'):
                st.error("Nincs elérhető predikció ehhez a meccshez.")
            else:
                p = pred['response'][0]['predictions']
                # Minden fontos predikciós mező kinyerése
                winner = p.get('winner', {}).get('name', 'Nincs adat')
                winner_comment = p.get('winner', {}).get('comment', 'Nincs adat')
                percent_home = p.get('percent', {}).get('home', 'Nincs adat')
                percent_draw = p.get('percent', {}).get('draw', 'Nincs adat')
                percent_away = p.get('percent', {}).get('away', 'Nincs adat')
                advice = p.get('advice', 'Nincs adat')
                goals_home = p.get('goals', {}).get('home', 'Nincs adat')
                goals_away = p.get('goals', {}).get('away', 'Nincs adat')
                goals_first_half = p.get('goals_first_half', 'Nincs adat')
                under_over = p.get('under_over', {}).get('label', 'Nincs adat') if isinstance(p.get('under_over'), dict) else p.get('under_over', 'Nincs adat')
                win_or_draw = p.get('win_or_draw', 'Nincs adat')
                if isinstance(win_or_draw, dict):
                    win_or_draw_home = win_or_draw.get('home', 'Nincs adat')
                    win_or_draw_away = win_or_draw.get('away', 'Nincs adat')
                elif isinstance(win_or_draw, bool):
                    win_or_draw_home = 'Igen' if win_or_draw else 'Nem'
                    win_or_draw_away = 'Igen' if win_or_draw else 'Nem'
                else:
                    win_or_draw_home = win_or_draw_away = 'Nincs adat'

                def explain_goal(val):
                    try:
                        v = float(val)
                        if v < 0:
                            return f"Nincs adat <span title='A predikció szerint maximum {abs(v)} gól várható, de az érték túl alacsony vagy nem megbízható.'>ℹ️</span>"
                        return f"{v} <span title='A predikció szerint várható gólok száma.'>ℹ️</span>"
                    except:
                        return "Nincs adat <span title='Nem elérhető vagy nem megbízható adat.'>ℹ️</span>"

                def explain_under_over(val):
                    if isinstance(val, dict):
                        label = val.get('label', '')
                    else:
                        label = str(val)
                    if label.startswith('-'):
                        return f"Legfeljebb {label[1:]} gól <span title='A predikció szerint maximum {label[1:]} gól várható a meccsen.'>ℹ️</span>"
                    elif label.startswith('+'):
                        return f"Legalább {label[1:]} gól <span title='A predikció szerint minimum {label[1:]} gól várható a meccsen.'>ℹ️</span>"
                    elif label.replace('.','',1).isdigit():
                        return f"{label} gól <span title='A predikció szerint várható gólok száma.'>ℹ️</span>"
                    else:
                        return f"Nincs adat <span title='Nem elérhető vagy nem megbízható adat.'>ℹ️</span>"

                kartya_html = f"""
<div class='prediction-card' style='padding:2em 1.5em;'>
    <h2 style='font-weight:800; color:#1565c0; margin-bottom:1em;'>Előrejelzés</h2>
    <div style='margin-bottom:1.2em;'>
        <span style='font-size:1.25rem; font-weight:700; color:#2e7d32;'>🏆 Győztes: {winner} <span title='A rendszer szerint legvalószínűbb győztes csapat.'>ℹ️</span></span><br>
        <span style='font-size:1.05rem; color:#374151;'>💬 <b>Magyarázat:</b> {winner_comment} <span title='Szöveges indoklás a predikcióhoz.'>ℹ️</span></span><br>
        <span style='font-size:1.05rem; color:#1565c0;'>📝 <b>Tanács:</b> {advice} <span title='Fogadási tipp, pl. Double chance: Home or Draw = vagy hazai győzelem, vagy döntetlen.'>ℹ️</span></span>
    </div>
    <div style='margin-bottom:1em; padding:0.7em 1em; background:#f5faff; border-radius:8px;'>
        <span style='font-size:1.1rem; font-weight:600;'>📊 Esélyek: <span title='A három fő kimenetel (hazai, döntetlen, vendég) valószínűsége százalékban.'>ℹ️</span></span><br>
        <span style='margin-right:1em;'>Hazai: <b>{percent_home}%</b></span>
        <span style='margin-right:1em;'>Döntetlen: <b>{percent_draw}%</b></span>
        <span>Vendég: <b>{percent_away}%</b></span>
    </div>
    <div style='margin-bottom:1em; padding:0.7em 1em; background:#f9fbe7; border-radius:8px;'>
        <span style='font-size:1.1rem; font-weight:600;'>⚽ Gólszám predikció: <span title='A rendszer által becsült gólok száma. Ha az érték irreális (negatív vagy nem szám), Nincs adat.'>ℹ️</span></span><br>
        <span style='margin-right:1em;'>Hazai: <b>{explain_goal(goals_home)}</b></span>
        <span style='margin-right:1em;'>Vendég: <b>{explain_goal(goals_away)}</b></span>
        <span>1. félidő: <b>{explain_goal(goals_first_half)}</b></span>
    </div>
    <div style='margin-bottom:1em; padding:0.7em 1em; background:#e3f2fd; border-radius:8px;'>
        <span style='font-size:1.1rem; font-weight:600;'>⚡ Under/Over 2.5 gól:</span> <b>{explain_under_over(under_over)}</b>
    </div>
    <div style='padding:0.7em 1em; background:#ede7f6; border-radius:8px;'>
        <span style='font-size:1.1rem; font-weight:600;'>🏅 Win or Draw: <span title='A kijelölt csapat vagy nyer, vagy döntetlent játszik.'>ℹ️</span></span>
        <span style='margin-right:1em;'>Hazai: <b>{win_or_draw_home}</b></span>
        <span>Vendég: <b>{win_or_draw_away}</b></span>
    </div>
    <div style='font-size:1.02rem; color:#607d8b; margin-top:1.5em;'>Predikciók az API-ból, valós adatokkal.</div>
    <div style='margin-top:2.2em; background:#e3f2fd; border-radius:9px; padding:1.2em 1em 1.1em 1em;'>
        <b>Mit jelentenek ezek az előrejelzések?</b><br>
        <ul style='font-size:1.01rem; color:#374151; margin-left:1.2em;'>
            <li><b>Győztes:</b> A rendszer szerint legvalószínűbb győztes csapat.</li>
            <li><b>Tanács:</b> Fogadási tipp, pl. "Double chance: Home or Draw" = vagy hazai győzelem, vagy döntetlen.</li>
            <li><b>Esélyek:</b> A három fő kimenetel (hazai, döntetlen, vendég) valószínűsége százalékban.</li>
            <li><b>Gólszám predikció:</b> A rendszer által becsült gólok száma. Ha az érték irreális (negatív vagy nem szám), "Nincs adat".</li>
            <li><b>Under/Over 2.5 gól:</b> <span style='color:#1565c0;'>-1.5</span> = maximum 1 gól várható, <span style='color:#388e3c;'>+2.5</span> = legalább 3 gól várható a meccsen.</li>
            <li><b>Win or Draw:</b> A kijelölt csapat vagy nyer, vagy döntetlent játszik.</li>
        </ul>
    </div>
</div>
"""
                st.markdown(kartya_html, unsafe_allow_html=True)
