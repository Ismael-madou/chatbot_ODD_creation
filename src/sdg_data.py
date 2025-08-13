import pandas as pd
import os

class SDGDataLoader:
    def __init__(self, excel_path):
        # Si le chemin n'est pas absolu, on le base sur la racine du projet
        if not os.path.isabs(excel_path):
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            excel_path = os.path.join(project_root, excel_path)
        self.excel_path = excel_path
        self.sheets = pd.ExcelFile(excel_path).sheet_names

    def get_years(self):
        df = pd.read_excel(self.excel_path, sheet_name='Backdated SDG Index')
        return sorted(df['year'].unique())

    def get_countries(self):
        df = pd.read_excel(self.excel_path, sheet_name='Backdated SDG Index')
        return sorted(df['Country'].unique())

    def get_sdg_scores(self, countries=None, years=None, goals=None):
        df = pd.read_excel(self.excel_path, sheet_name='Backdated SDG Index')
        if countries:
            df = df[df['Country'].isin(countries)]
        if years:
            df = df[df['year'].isin(years)]
        if goals:
            cols = ['Country', 'year'] + goals
            df = df[cols]
        return df

    def get_goal_columns(self):
        df = pd.read_excel(self.excel_path, sheet_name='Backdated SDG Index', nrows=1)
        return [col for col in df.columns if col.startswith('goal')]

    def get_global_score(self, countries=None, years=None):
        df = pd.read_excel(self.excel_path, sheet_name='Backdated SDG Index')
        if countries:
            df = df[df['Country'].isin(countries)]
        if years:
            df = df[df['year'].isin(years)]
        return df[['Country', 'year', 'sdgi_s']]
