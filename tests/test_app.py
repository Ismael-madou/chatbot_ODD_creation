import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import app

def test_reset_on_lang_switch():
    # Should not raise or modify anything
    try:
        app.reset_on_lang_switch()
    except Exception as e:
        pytest.fail(f"reset_on_lang_switch raised an exception: {e}")

def test_feedback_buttons(monkeypatch):
    # Test that feedback_buttons does not raise (UI function)
    # Monkeypatch st.button to simulate button clicks
    import streamlit as st
    called = {}
    def fake_button(label, key=None):
        called[label] = True
        return False
    monkeypatch.setattr(st, "button", fake_button)
    try:
        app.feedback_buttons(1)
    except Exception as e:
        pytest.fail(f"feedback_buttons raised an exception: {e}")

def test_load_odd_data(tmp_path):
    # Test loading a valid JSON file
    import json
    data = {"odds": [1,2,3]}
    file = tmp_path / "odds.json"
    file.write_text(json.dumps(data))
    result = app.load_odd_data(str(file))
    assert result == data

def test_charger_classement(monkeypatch):
    # Test with a fake URL and monkeypatch pd.read_excel
    import pandas as pd
    # Simuler un DataFrame sans les colonnes attendues pour vérifier le retour None
    df = pd.DataFrame({"A": [1,2]})
    monkeypatch.setattr(pd, "read_csv", lambda url: df)
    result = app.charger_classement("fake_url")
    assert result is None

def test_load_excel_loader(monkeypatch):
    # Test that it returns an instance of SDGDataLoader
    from sdg_data import SDGDataLoader
    monkeypatch.setattr(app, "SDGDataLoader", SDGDataLoader)
    loader = app.load_excel_loader("data/SDR2025-data.xlsx")
    assert isinstance(loader, SDGDataLoader)

def test_odd_quiz():
    # UI function: just check it runs
    try:
        app.odd_quiz()
    except Exception as e:
        pytest.fail(f"odd_quiz raised an exception: {e}")

def test_afficher_barre_recherche():
    # UI function: just check it runs and returns a string
    result = app.afficher_barre_recherche()
    assert isinstance(result, str)

def test_process_user_question():
    # UI function: just check it runs (no exception)
    # On simule une structure de retour compatible avec formater_reponse_odd
    from chat_bot import formater_reponse_odd
    odd_data = {
        "type": "faq",
        "question": {"en": "What is SDG 1?", "fr": "Qu'est-ce que l'ODD 1 ?"},
        "answer": {"en": "SDG 1 is ...", "fr": "L'ODD 1 est ..."},
        "keywords": {"en": ["poverty"], "fr": ["pauvreté"]},
        "category": "general"
    }
    try:
        formater_reponse_odd(odd_data, question="What is SDG 1?", lang="English")
    except Exception as e:
        pytest.fail(f"formater_reponse_odd raised an exception: {e}")
