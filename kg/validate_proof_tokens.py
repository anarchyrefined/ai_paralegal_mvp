import pandas as pd
import sys

def main():
    try:
        df = pd.read_csv("kg/edges_final.csv")
        if df.empty:
            print("⚠️  edges_final.csv is empty. Skipping proof validation.")
            return
    except FileNotFoundError:
        print("⚠️  edges_final.csv not found. Skipping proof validation.")
        return
    except pd.errors.EmptyDataError:
        print("⚠️  edges_final.csv is empty. Skipping proof validation.")
        return
    invalid = df[~df["proof"].str.match(r"^doc:.+\|page:\d+\|sha256=[a-f0-9]{64}$", na=False)]

    if not invalid.empty:
        print(f"❌ {len(invalid)} edges missing valid proof tokens")
        sys.exit(1)
    else:
        print("✅ All edges have valid proof tokens")

if __name__ == "__main__":
    main()
