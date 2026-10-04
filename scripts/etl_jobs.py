# scripts/etl_jobs.py
import argparse
from ydata_profiling import ProfileReport
from scripts.data_cleaning import clean_data

def run_etl(input_path: str, cleaned_path: str, profile_path: str):
    print("🔄 Cleaning data...")
    df = clean_data(input_path, cleaned_path)

    if df is None:  # safeguard
        raise ValueError("❌ clean_data() returned None. Please check data_cleaning.py")

    print(f"✅ Cleaned data saved → {cleaned_path} ({len(df)} rows)")

    print("🔄 Generating profiling report...")
    profile = ProfileReport(df, title="Job Skills Profiling Report", explorative=True)
    profile.to_file(profile_path)
    print(f"✅ Profiling report saved → {profile_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ETL pipeline for job skills analysis")
    parser.add_argument("--input", required=True, help="Path to raw input CSV")
    parser.add_argument("--cleaned", required=True, help="Path to save cleaned CSV")
    parser.add_argument("--profile", required=True, help="Path to save profiling report (HTML)")
    args = parser.parse_args()

    run_etl(args.input, args.cleaned, args.profile)
