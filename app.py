"""
app.py - Interface principale Streamlit pour le Chatbot ODD

Ce script lance l'interface utilisateur du chatbot ODD, permettant à l'utilisateur de poser des questions
sur les Objectifs de Développement Durable (ODD) et d'obtenir des réponses générées par IA.
Il gère aussi l'affichage, l'historique de chat, la gestion du cache et les exemples de questions.

Auteurs : [Votre nom]
Date : [Date]

Fonctions principales :
- Affichage de l'interface utilisateur Streamlit
- Gestion de l'historique de chat et des suggestions
- Appel aux fonctions du backend pour la recherche et la génération de réponses
- Gestion du cache et des statistiques
"""

import streamlit as st
from chat_bot import chercher_odd, formater_reponse_odd, clear_cache, get_cache_info
from sentence_transformers import SentenceTransformer, util
import os


# Page config
st.set_page_config(
    page_title="SDG Chatbot / Chatbot ODD",
    page_icon="🌍",
    layout="wide"
)
    
# Initialisation sûre de la langue
if "lang" not in st.session_state:
    st.session_state["lang"] = "Français"
lang = st.session_state["lang"]

# Réinitialisation automatique de l'état lors du changement de langue
def reset_on_lang_switch():
    st.session_state["messages"] = []
    st.session_state["search_input"] = ""
    st.session_state["quiz_mode"] = False
    st.session_state["feedback"] = []

# Sélecteur de langue unique en haut de page
lang_select = st.selectbox(
    "🌐 Language / Langue",
    ["English", "Français"],
    index=0 if st.session_state["lang"]=="English" else 1,
    on_change=reset_on_lang_switch
)
st.session_state["lang"] = lang_select
lang = st.session_state["lang"]
    


# Mode accessibilité (contraste élevé)
if "accessibility" not in st.session_state:
    st.session_state["accessibility"] = False
accessibility = st.sidebar.checkbox("Mode accessibilité (contraste élevé)", value=st.session_state["accessibility"])
st.session_state["accessibility"] = accessibility

# Appliquer le style contraste élevé si activé
if accessibility:
    st.markdown("""
        <style>
        body, .stApp, .stMarkdown, .stTextInput, .stButton, .stDataFrame, .stSidebar, .stSelectbox, .stChatMessage {
            background-color: #000 !important;
            color: #fff !important;
        }
        .stButton>button { background: #222 !important; color: #fff !important; border: 2px solid #fff; }
        .stTextInput>div>input { background: #222 !important; color: #fff !important; }
        .stDataFrame { background: #111 !important; color: #fff !important; }
        </style>
    """, unsafe_allow_html=True)

# Language selection (must be at the very top)
if "lang" not in st.session_state:
    st.session_state["lang"] = "Français"
lang = st.selectbox("Language / Langue", ["English", "Français"], key="lang_select", index=0 if st.session_state["lang"]=="English" else 1)
st.session_state["lang"] = lang

# Définir le dossier courant du script
BASE_DIR = os.path.dirname(__file__)


# Header with title, logo, and quiz button
header_col1, header_col2, header_col3 = st.columns([4, 1, 1])
with header_col1:
    if lang == "English":
        st.title("SDG Chatbot 🌍")
        st.markdown("Ask a question about the Sustainable Development Goals.")
    else:
        st.title("Chatbot ODD 🌍")
        st.markdown("Pose une question sur les Objectifs de Développement Durable.")
with header_col2:
    logo_path = os.path.join(BASE_DIR, "logo_ODD.png")
    if os.path.exists(logo_path):
        st.image(logo_path, width=60)
with header_col3:
    if st.button("🎲 Quiz ODD"):
        st.session_state["quiz_mode"] = True

# Feedback utilisateur (👍/👎)
def feedback_buttons(idx):
    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("👍", key=f"like_{idx}"):
            st.session_state.setdefault("feedback", []).append({"msg": idx, "feedback": "like"})
    with col2:
        if st.button("👎", key=f"dislike_{idx}"):
            st.session_state.setdefault("feedback", []).append({"msg": idx, "feedback": "dislike"})

# Texte explicatif sur les ODD (bilingue dynamique)
st.markdown(
    """
    <div style='font-size: 1.1em; background-color: #f0f2f6; padding: 15px; border-radius: 8px;'>
    {} 
    </div>
    """.format(
        "The Sustainable Development Goals (SDGs) are a call to action for all countries—poor, rich, and middle-income—to promote prosperity while protecting the planet. They recognize that ending poverty must go hand-in-hand with strategies that build economic growth and address a range of social needs including education, health, social protection, and job opportunities, while tackling climate change and environmental protection." if lang == "English" else
        "Les objectifs de développement durable sont un appel à l'action de tous les pays – pauvres, riches et à revenu intermédiaire – afin de promouvoir la prospérité tout en protégeant la planète. Ils reconnaissent que mettre fin à la pauvreté doit aller de pair avec des stratégies qui développent la croissance économique et répondent à une série de besoins sociaux, notamment l'éducation, la santé, la protection sociale et les possibilités d'emploi, tout en luttant contre le changement climatique et la protection de l'environnement."
    ),
    unsafe_allow_html=True
)

st.markdown("---")


# Affichage des cartes ODD dynamiques
import json
odd_json_path = os.path.join(BASE_DIR, "odd_data_enriched_bilingual.json")
if os.path.exists(odd_json_path):
    with open(odd_json_path, encoding="utf-8") as f:
        odd_data = json.load(f)
    odds = odd_data.get("odds", [])
    st.markdown(
        f"<h3 style='margin-top:30px;'>{'The 17 Sustainable Development Goals' if lang == 'English' else 'Les 17 Objectifs de Développement Durable'}</h3>",
        unsafe_allow_html=True
    )
    # Affichage compact : 5 cartes par ligne, padding réduit
    card_cols = st.columns(5)
    for idx, odd in enumerate(odds):
        col = card_cols[idx % 5]
        with col:
            st.markdown(f"""
                <div style='background:#fff;border-radius:8px;border:1px solid #e0e0e0;padding:10px;margin-bottom:8px;box-shadow:0 1px 4px #0001; min-height:120px;'>
                    <div style='font-size:1.1em;font-weight:bold;color:#0074d9;margin-bottom:2px;'>{'SDG' if lang == 'English' else 'ODD'} {odd['odd']}</div>
                    <div style='font-size:0.98em;font-weight:600;margin-bottom:2px;'>{odd['title']['en'] if lang == 'English' else odd['title']['fr']}</div>
                    <div style='font-size:0.90em;color:#444;'>{odd['description']['en'] if lang == 'English' else odd['description']['fr']}</div>
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
classement_df = charger_classement(CLASSEMENT_URL)
if classement_df is not None and not classement_df.empty:
    # Graphique interactif Plotly (top 20)
    st.markdown(f"<b>{'Top 20 worldwide (SDG Index)' if lang == 'English' else 'Top 20 mondial (Indice ODD)'}</b>", unsafe_allow_html=True)
    top20 = classement_df.head(20).sort_values("Indice ODD")
    fig = px.bar(
        top20,
        x="Indice ODD",
        y="Pays",
        orientation="h",
        color="Indice ODD",
        color_continuous_scale="Blues",
        labels={"Indice ODD": "Score ODD", "Pays": "Pays"},
    title="SDG Index Ranking (real-time data)" if lang == "English" else "Classement ODD (données en temps réel)"
    )
    fig.update_layout(yaxis={'categoryorder':'total ascending'}, height=600, margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(classement_df.head(20), hide_index=True, use_container_width=True)
else:
    # Fallback statique si la connexion échoue
    classement_data = [
        {"Pays": "Finlande", "Indice ODD": 86.5},
        {"Pays": "Suède", "Indice ODD": 85.7},
        {"Pays": "Danemark", "Indice ODD": 85.2},
        {"Pays": "France", "Indice ODD": 81.5},
        {"Pays": "Maroc", "Indice ODD": 70.1},
        {"Pays": "Côte d'Ivoire", "Indice ODD": 62.3},
        {"Pays": "Tchad", "Indice ODD": 51.2}
    ]
    classement_df = pd.DataFrame(classement_data)
    fig = px.bar(
        classement_df.sort_values("Indice ODD"),
        x="Indice ODD",
        y="Pays",
        orientation="h",
        color="Indice ODD",
        color_continuous_scale="Blues",
        labels={"Indice ODD": "Score ODD", "Pays": "Pays"},
    title="SDG Index Ranking (static example)" if lang == "English" else "Classement ODD (exemple statique)"
    )
    fig.update_layout(yaxis={'categoryorder':'total ascending'}, height=400, margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(classement_df, hide_index=True, use_container_width=True)

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
sidebar_logo_path = os.path.join(BASE_DIR, "logo_ODD.png")
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
st.sidebar.markdown("**⚡ Performance :**")

# Afficher les informations du cache
cache_info = get_cache_info()
if cache_info["file_count"] > 0:
    st.sidebar.success(f"✅ Cache actif ({cache_info['file_count']} fichiers, {cache_info['total_size_mb']} MB)")
    
    # Bouton pour voir les détails du cache
    if st.sidebar.button("📋 Détails du cache"):
        st.sidebar.markdown("**Fichiers en cache :**")
        for file_info in cache_info["files"]:
            st.sidebar.markdown(f"- {file_info['name']} ({file_info['size_mb']} MB)")
else:
    st.sidebar.warning("⚠️ Aucun cache trouvé")

# Bouton pour effacer l'historique
if st.sidebar.button("🗑️ Effacer l'historique"):
    st.session_state.messages = []
    st.rerun()

# Bouton pour effacer le cache
if st.sidebar.button("🧹 Effacer le cache"):
    clear_cache()
    st.sidebar.success("✅ Cache effacé ! Le prochain démarrage sera plus lent.")
    st.rerun()  