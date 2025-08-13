import sys

def run_demo():
    from src.sdg_data import SDGDataLoader
    loader = SDGDataLoader("data/SDR2025-data.xlsx")
    print("Années disponibles :", loader.get_years())
    print("Pays disponibles :", loader.get_countries()[:10], "...")
    print("Colonnes ODD :", loader.get_goal_columns())
    df = loader.get_global_score(countries=["France", "Germany", "Finland"])
    print(df.head())

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        run_demo()
    else:
        # Importe et exécute l'app Streamlit (src/app.py) si lancé via streamlit run main.py
        import src.app
