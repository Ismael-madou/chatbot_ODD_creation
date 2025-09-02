import sys

def run_demo():
    from src.sdg_data import SDGDataLoader
    loader = SDGDataLoader("data/SDR2025-data.xlsx")
    print("Available years:", loader.get_years())
    print("Available countries:", loader.get_countries()[:10], "...")
    print("SDG columns:", loader.get_goal_columns())
    df = loader.get_global_score(countries=["France", "Germany", "Finland"])
    print(df.head())

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        run_demo()
    else:
        # Import and run the Streamlit app (src/app.py) if launched via streamlit run main.py
        import src.app
