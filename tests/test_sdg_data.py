import os
import pytest
from src.sdg_data import SDGDataLoader

def test_loader_years():
    excel_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'SDR2025-data.xlsx')
    loader = SDGDataLoader(excel_path)
    years = loader.get_years()
    assert isinstance(years, list)
    assert len(years) > 0

def test_loader_countries():
    excel_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'SDR2025-data.xlsx')
    loader = SDGDataLoader(excel_path)
    countries = loader.get_countries()
    assert isinstance(countries, list)
    assert 'France' in countries or 'Germany' in countries
