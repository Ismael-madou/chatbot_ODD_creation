import pytest
from sdg_data import SDGDataLoader
import os

def test_init_loader():
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'SDR2025-data.xlsx')
    loader = SDGDataLoader(path)
    assert loader.excel_path.endswith('.xlsx')

def test_get_years():
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'SDR2025-data.xlsx')
    loader = SDGDataLoader(path)
    years = loader.get_years()
    assert isinstance(years, list)

def test_get_countries():
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'SDR2025-data.xlsx')
    loader = SDGDataLoader(path)
    countries = loader.get_countries()
    assert isinstance(countries, list)

def test_get_goal_columns():
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'SDR2025-data.xlsx')
    loader = SDGDataLoader(path)
    cols = loader.get_goal_columns()
    assert isinstance(cols, list)

def test_get_global_score():
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'SDR2025-data.xlsx')
    loader = SDGDataLoader(path)
    df = loader.get_global_score(countries=['France'])
    assert hasattr(df, 'head')
