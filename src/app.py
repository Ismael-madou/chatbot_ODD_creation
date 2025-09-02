

# All imports at the very top
from chat_bot import chercher_odd, formater_reponse_odd, clear_cache, get_cache_info
from sentence_transformers import SentenceTransformer, util
from sdg_data import SDGDataLoader
import streamlit as st
import os
import sys
import json
import pandas as pd
import requests
import plotly.express as px



# Prevent direct execution of this file
if __name__ == "__main__":
    print("\n[ERROR]: Please launch the application via main.py at the project root:\n\n    streamlit run main.py\n\nDo not run src/app.py directly.\n")
    sys.exit(1)

# Determine the project root (folder containing main.py)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

"""
app.py - Main Streamlit interface for the SDG Chatbot

This script launches the user interface for the SDG Chatbot, allowing users to ask questions
about the Sustainable Development Goals (SDGs) and get AI-generated answers.
It also manages the display, chat history, cache management, and example questions.

Main features:
- Streamlit user interface display
- Chat history and suggestions management
- Calls backend functions for search and answer generation
- Cache and statistics management
"""



# Page config
st.set_page_config(
    page_title="SDG Chatbot / Chatbot ODD",
    page_icon="🌍",
    layout="wide"
)
    


# Safe initialization of language
if "lang" not in st.session_state:
    st.session_state["lang"] = "Français"

# Always use the session value for language
lang = st.session_state.get("lang", "Français")





# Ultra-safe reset on language change: only update language
def reset_on_lang_switch():
    pass  # Do not reset anything, let Streamlit handle the key change

# Unique language selector at the top of the page
lang_select = st.selectbox(
    "🌐 Language / Langue",
    ["English", "Français"],
    index=0 if st.session_state.get("lang", "Français")=="English" else 1,
    key="lang_select",
    on_change=reset_on_lang_switch
)
if lang_select != st.session_state.get("lang", "Français"):
    st.session_state["lang"] = lang_select
lang = st.session_state["lang"]
    



# Accessibility mode (high contrast)
if "accessibility" not in st.session_state:
    st.session_state["accessibility"] = False
accessibility = st.sidebar.checkbox("Accessibility mode (high contrast)", value=st.session_state["accessibility"], key="accessibility_checkbox")
if accessibility != st.session_state["accessibility"]:
    st.session_state["accessibility"] = accessibility

# Apply high contrast style if enabled
if accessibility:
    st.markdown("""
        <style>
        .stButton>button { background: #222 !important; color: #fff !important; border: 2px solid #fff; }
        .stTextInput>div>input { background: #222 !important; color: #fff !important; }
        .stDataFrame { background: #111 !important; color: #fff !important; }
        </style>
    """, unsafe_allow_html=True)






# Header with title, logo, and quiz button
header_col1, header_col2, header_col3 = st.columns([4, 1, 1])
with header_col1:
    if lang == "English":
        st.title("SDG Chatbot 🌍")
        st.markdown("Ask a question about the Sustainable Development Goals.")
    else:
        st.title("Chatbot ODD 🌍")
        st.markdown("Ask a question about the Sustainable Development Goals.")
with header_col2:
    logo_path = os.path.join(PROJECT_ROOT, "pictures", "logo_ODD.png")
    if os.path.exists(logo_path):
        st.image(logo_path, width=60)
with header_col3:
    if st.button("🎲 Quiz ODD"):
        st.session_state["quiz_mode"] = True

# User feedback (👍/👎)
def feedback_buttons(idx):
    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("👍", key=f"like_{idx}"):
            st.session_state.setdefault("feedback", []).append({"msg": idx, "feedback": "like"})
    with col2:
        if st.button("👎", key=f"dislike_{idx}"):
            st.session_state.setdefault("feedback", []).append({"msg": idx, "feedback": "dislike"})


# Explanatory text about SDGs (dynamic bilingual)
st.markdown(
    """
    <div style='font-size: 1.1em; background-color: #f0f2f6; padding: 15px; border-radius: 8px;'>
    {} 
    </div>
    """.format(
        "The Sustainable Development Goals (SDGs) are a call to action for all countries—poor, rich, and middle-income—to promote prosperity while protecting the planet. They recognize that ending poverty must go hand-in-hand with strategies that build economic growth and address a range of social needs including education, health, social protection, and job opportunities, while tackling climate change and environmental protection." if lang == "English" else
        "The Sustainable Development Goals (SDGs) are a call to action for all countries—poor, rich, and middle-income—to promote prosperity while protecting the planet. They recognize that ending poverty must go hand-in-hand with strategies that build economic growth and address a range of social needs including education, health, social protection, and job opportunities, while tackling climate change and environmental protection."
    ),
    unsafe_allow_html=True
)

st.markdown("---")



# Display dynamic SDG cards

# --- Accessibility: text size slider ---
from sdg_data import SDGDataLoader
st.session_state["font_size"] = 1.0
font_size = st.sidebar.slider("Text size", 0.8, 2.0, st.session_state["font_size"], 0.1, key="font_size_slider")
if font_size != st.session_state["font_size"]:
    st.session_state["font_size"] = font_size
st.markdown(f"<style>html, body, .stApp {{ font-size: {st.session_state['font_size']}em !important; }}</style>", unsafe_allow_html=True)

# --- Optimisation : cache Streamlit pour chargement JSON et Excel ---
import json
@st.cache_data
def load_odd_data(json_path):
    with open(json_path, encoding="utf-8") as f:
        return json.load(f)

odd_json_path = os.path.join(PROJECT_ROOT, "data", "odd_data_enriched_bilingual.json")
odds = []
if os.path.exists(odd_json_path):
    odd_data = load_odd_data(odd_json_path)
    odds = odd_data.get("odds", [])
    st.markdown(
        f"<h3 style='margin-top:30px;'>{'The 17 Sustainable Development Goals' if lang == 'English' else 'Les 17 Objectifs de Développement Durable'}</h3>",
        unsafe_allow_html=True
    )
    # Affichage compact : 5 cartes par ligne, padding réduit
    card_cols = st.columns(5)
    card_bg = "#111" if st.session_state.get("accessibility", False) else "#fff"
    card_text = "#fff" if st.session_state.get("accessibility", False) else "#444"
    card_title = "#fff" if st.session_state.get("accessibility", False) else "#0074d9"
    card_border = "#fff" if st.session_state.get("accessibility", False) else "#e0e0e0"
    for idx, odd in enumerate(odds):
        col = card_cols[idx % 5]
        with col:
            st.markdown(f"""
                <div style='background:{card_bg};border-radius:8px;border:1px solid {card_border};padding:10px;margin-bottom:8px;box-shadow:0 1px 4px #0001; min-height:120px;'>
                    <div style='font-size:1.1em;font-weight:bold;color:{card_title};margin-bottom:2px;'>{'SDG' if lang == 'English' else 'ODD'} {odd['odd']}</div>
                    <div style='font-size:0.98em;font-weight:600;margin-bottom:2px;color:{card_text};'>{odd['title']['en'] if lang == 'English' else odd['title']['fr']}</div>
                    <div style='font-size:0.90em;color:{card_text};'>{odd['description']['en'] if lang == 'English' else odd['description']['fr']}</div>
                </div>
            """, unsafe_allow_html=True)
else:
    st.warning("Unable to load SDG data to display cards." if lang == "English" else "Impossible de charger les données ODD pour afficher les cartes.")





# Classement dynamique des pays (connexion API/CSV/JSON)

import pandas as pd
import requests
import plotly.express as px


# URL officielle du SDG Index 2024 (SDSN) - lien direct RAW
CLASSEMENT_URL = "https://raw.githubusercontent.com/sdsna/SDG-Index-Data/main/2024/SDR2024_Data.csv"


def charger_classement(url: str) -> pd.DataFrame:
    """
    Tente de charger le classement ODD mondial depuis le CSV officiel SDSN. Retourne un DataFrame ou None.
    """
    try:
        df = pd.read_csv(url)
        # Le CSV SDSN contient les colonnes 'Country' et 'SDG Index Score'
        if 'Country' in df.columns and 'SDG Index Score' in df.columns:
            df = df.rename(columns={"Country": "Pays", "SDG Index Score": "Indice ODD"})
            df = df[["Pays", "Indice ODD"]]
            df = df.dropna(subset=["Indice ODD"])
            df = df.sort_values("Indice ODD", ascending=False)
            return df
        else:
            st.warning("Colonnes attendues non trouvées dans le CSV SDSN.")
            return None
    except Exception as e:
        st.warning(f"Impossible de charger le classement dynamique : {e}")
        return None

st.markdown(
    f"<h4 style='margin-top:24px;'>{'Country ranking by SDG Index' if lang == 'English' else 'Classement des pays par Indice ODD'}</h4>",
    unsafe_allow_html=True
)


from sdg_data import SDGDataLoader
@st.cache_data
def load_excel_loader(excel_path):
    return SDGDataLoader(excel_path)
excel_path = os.path.join(PROJECT_ROOT, "data", "SDR2025-data.xlsx")
loader = load_excel_loader(excel_path)
years = sorted(loader.get_years())
if "selected_year" not in st.session_state:
    st.session_state["selected_year"] = years[-1]
selected_year = st.sidebar.selectbox(
    "Année des données" if st.session_state.get("lang", "Français") != "English" else "Data year",
    years,
    index=years.index(st.session_state["selected_year"]),
    key="select_year"
)
if selected_year != st.session_state["selected_year"]:
    st.session_state["selected_year"] = selected_year
selected_year = st.session_state["selected_year"]
classement_df = loader.get_global_score(years=[selected_year])
classement_df = classement_df.rename(columns={"sdgi_s": "Indice ODD", "Country": "Pays"})

# --- Sélection libre de pays (minimum 2) ---
st.markdown(f"<b>{'Country selection (at least 2)' if st.session_state.get('lang', 'Français') == 'English' else 'Sélection de pays (au moins 2)'}:</b>", unsafe_allow_html=True)
pays_options = sorted(classement_df['Pays'].tolist())
default_selection = pays_options[:5] if len(pays_options) > 5 else pays_options
if "selected_countries" not in st.session_state:
    st.session_state["selected_countries"] = default_selection
selected_pays = st.multiselect(
    'Select countries to compare (at least 2)' if st.session_state.get('lang', 'Français') == 'English' else 'Sélectionne des pays à comparer (au moins 2)',
    options=pays_options,
    default=st.session_state["selected_countries"],
    key='select_countries'
)
# On évite de réinitialiser la sélection si elle n'a pas changé
if set(selected_pays) != set(st.session_state["selected_countries"]):
    st.session_state["selected_countries"] = selected_pays
selected_pays = st.session_state["selected_countries"]
if len(selected_pays) < 2:
    st.warning('Please select at least 2 countries.' if st.session_state.get('lang', 'Français') == 'English' else 'Merci de sélectionner au moins 2 pays.')
    filtered_df = pd.DataFrame(columns=classement_df.columns)
else:
    filtered_df = classement_df[classement_df['Pays'].isin(selected_pays)]
    fig = px.bar(
        filtered_df,
        x="Indice ODD",
        y="Pays",
        orientation="h",
        color="Indice ODD",
        color_continuous_scale="Blues",
        labels={"Indice ODD": "Score ODD", "Pays": "Pays"},
        title="SDG Index Ranking (real-time data)" if st.session_state.get('lang', 'Français') == 'English' else "Classement ODD (données en temps réel)"
    )
    fig.update_layout(yaxis={'categoryorder':'total ascending'}, height=600, margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": True, "displaylogo": False})
    st.dataframe(filtered_df, hide_index=True, use_container_width=True)

st.markdown(f"## {'Ask your question 👇' if lang == 'English' else 'Pose ta question 👇'}")


# Suggestions dynamiques depuis le JSON bilingue
suggestions = []
if odds:
    for odd in odds:
        for q in odd.get("example_questions", {}).get("en" if lang == "English" else "fr", []):
            suggestions.append(q)
suggestions = suggestions[:5] if len(suggestions) > 5 else suggestions
suggestions_label = "**Suggestions:**" if lang == "English" else "**Suggestions :**"
st.markdown("<div style='margin-bottom:10px;'></div>", unsafe_allow_html=True)
st.markdown(suggestions_label, unsafe_allow_html=True)
cols = st.columns(max(1, len(suggestions)))
for i, q in enumerate(suggestions):
    if cols[i % len(cols)].button(q, key=f"suggestion_{lang}_{i}"):
        st.session_state["search_input"] = q

# Barre de recherche unique
if "messages" not in st.session_state:
    st.session_state.messages = []

# Barre de recherche unique et historique
def odd_quiz():
    import random
    if not odds:
        st.warning("Aucune donnée ODD pour le quiz.")
        return
    odd = random.choice(odds)
    q = odd.get("example_questions", {}).get("en" if lang == "English" else "fr", [])[0] if odd.get("example_questions") else None
    answer = odd.get("title", {}).get("en" if lang == "English" else "fr", "")
    st.markdown(f"<b>{'Quiz:' if lang == 'English' else 'Quiz :'} {q}</b>", unsafe_allow_html=True)
    user_ans = st.text_input("Votre réponse :" if lang != "English" else "Your answer:", key="quiz_input")
    if st.button("Valider" if lang != "English" else "Submit", key="quiz_submit"):
        if user_ans.strip().lower() == answer.strip().lower():
            st.success("Bravo !" if lang != "English" else "Correct!")
        else:
            st.error(f"La bonne réponse était : {answer}" if lang != "English" else f"The correct answer was: {answer}")
    if st.button("Quitter le quiz" if lang != "English" else "Exit quiz", key="quiz_exit"):
        st.session_state["quiz_mode"] = False

if st.session_state.get("quiz_mode", False):
    odd_quiz()
    st.stop()

def afficher_barre_recherche() -> str:
    """
    Affiche la barre de recherche principale et retourne la question saisie.
    Returns:
        str: La question saisie par l'utilisateur.
    """
    return st.text_input(
        "Pose ta question sur les ODD :",
        value=st.session_state.get("search_input", ""),
        key="search_input",
        placeholder="Tape ta question ici...",
        help="Exemple : Qu'est-ce que l'ODD 1 ?"
    )

search = afficher_barre_recherche()



def process_user_question(question: str) -> None:
    st.session_state.messages.append({"role": "user", "content": question})
    idx = len(st.session_state.messages)
    with st.chat_message("user"):
        if lang == "English":
            st.markdown(f"<div style='background:#f5f5f5; border-radius:8px; padding:10px; margin-bottom:2px;'><b>👤 You:</b> {question}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='background:#f5f5f5; border-radius:8px; padding:10px; margin-bottom:2px;'><b>👤 Toi :</b> {question}</div>", unsafe_allow_html=True)
    with st.chat_message("assistant"):
        spinner_text = "🤖 Thinking about your question..." if lang == "English" else "🤖 Je réfléchis à ta question..."
        with st.spinner(spinner_text):
            result = chercher_odd(question, lang=lang)
            formatted_response = formater_reponse_odd(result, question, lang=lang)
            if lang == "English":
                st.markdown(f"<div style='background:#e6f7ff; border-radius:8px; padding:10px;'><b>🤖 SDGbot:</b><br>{formatted_response}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='background:#e6f7ff; border-radius:8px; padding:10px;'><b>🤖 ODDbot :</b><br>{formatted_response}</div>", unsafe_allow_html=True)
        feedback_buttons(idx)

if search:
    process_user_question(search)

# Historique compact (optionnel, n'affiche que les 5 derniers échanges)
if len(st.session_state.messages) > 1:
    st.markdown("---")
    st.markdown("<b>Historique récent :</b>", unsafe_allow_html=True)
    for msg in st.session_state.messages[-5:]:
        if msg["role"] == "user":
            st.markdown(f"<div style='color:#333; margin-bottom:2px;'><b>👤</b> {msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='color:#0074d9; margin-bottom:2px;'><b>🤖</b> {msg['content']}</div>", unsafe_allow_html=True)

# Informations sur l'IA
st.info("🤖 Ce chatbot utilise l'IA avancée (LLM) pour vous aider à comprendre les ODD de manière naturelle et engageante. [En savoir plus](https://www.un.org/sustainabledevelopment/fr/)")

# Sidebar
sidebar_logo_path = os.path.join(PROJECT_ROOT, "pictures", "logo_ODD.png")
if os.path.exists(sidebar_logo_path):
    st.sidebar.image(sidebar_logo_path, width=80)
else:
    st.sidebar.warning(f"Logo non trouvé : {sidebar_logo_path}")

st.sidebar.title("About")
st.sidebar.info("This chatbot uses AI to answer your questions about the SDGs.")

# Statistiques dans la sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("**📊 Statistiques :**")
st.sidebar.markdown("- 17 ODD")
st.sidebar.markdown("- 169 cibles")
st.sidebar.markdown("- 232 indicateurs")
st.sidebar.markdown("- Objectif 2030")

# Gestion du cache dans la sidebar
st.sidebar.markdown("---")


# Section importante et valorisante pour les utilisateurs
st.sidebar.markdown("---")
if lang == "English":
    st.sidebar.markdown("**🌍 This tool helps you discover and act for the 17 Sustainable Development Goals.**")
    st.sidebar.info("Your questions and actions contribute to a better world for 2030.")
else:
    st.sidebar.markdown("**🌍 Cet outil vous aide à découvrir et agir pour les 17 Objectifs de Développement Durable.**")
    st.sidebar.info("Vos questions et vos actions comptent pour un monde meilleur à l’horizon 2030.")


# Bouton pour effacer l'historique
if st.sidebar.button("🗑️ Effacer l'historique"):
    st.session_state.messages = []

# Bouton pour effacer le cache
if st.sidebar.button("🧹 Effacer le cache"):
    clear_cache()
    st.sidebar.success("✅ Cache effacé ! Le prochain démarrage sera plus lent.")