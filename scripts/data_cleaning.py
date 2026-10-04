# scripts/data_cleaning.py
import pandas as pd

def clean_data(input_path: str, output_path: str) -> pd.DataFrame:
    """
    Reads raw jobs CSV, applies cleaning steps, saves cleaned CSV,
    and returns cleaned DataFrame.
    """
    df = pd.read_csv(input_path)

    # Example cleaning steps – adjust for your data
    df = df.drop_duplicates()
    df = df.dropna(subset=["job_title", "company", "skills"])

    # Strip whitespace from column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Save cleaned CSV
    df.to_csv(output_path, index=False)

    print(f"✅ Cleaned data written to {output_path}, rows: {len(df)}")

    return df   # <-- THIS IS CRUCIAL
