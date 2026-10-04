# scripts/analysis.py
import os
import pandas as pd
import matplotlib.pyplot as plt

def analyze_jobs(input_path: str, output_dir: str, figures_dir: str):
    # Ensure output directories exist
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(figures_dir, exist_ok=True)

    print("🔄 Loading cleaned dataset...")
    df = pd.read_csv(input_path)
    print(f"✅ Loaded dataset with {len(df)} rows and {len(df.columns)} columns")

    # ---- Top Companies ----
    top_companies = df['company'].value_counts().head(10)
    top_companies.to_csv(os.path.join(output_dir, "top_companies.csv"))
    plt.figure(figsize=(10,6))
    top_companies.plot(kind='bar', color="skyblue", edgecolor="black")
    plt.title("Top 10 Hiring Companies")
    plt.xlabel("Company")
    plt.ylabel("Job Postings")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, "top_companies.png"))
    plt.close()
    print("✅ Top companies analysis saved")

    # ---- Top Skills ----
    if "skills" in df.columns:
        all_skills = df['skills'].dropna().str.split(",").explode().str.strip()
        top_skills = all_skills.value_counts().head(10)
        top_skills.to_csv(os.path.join(output_dir, "top_skills.csv"))
        plt.figure(figsize=(10,6))
        top_skills.plot(kind='bar', color="lightgreen", edgecolor="black")
        plt.title("Top 10 Skills in Job Postings")
        plt.xlabel("Skills")
        plt.ylabel("Frequency")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(os.path.join(figures_dir, "top_skills.png"))
        plt.close()
        print("✅ Top skills analysis saved")

    # ---- Job Trends Over Time ----
    if "date_posted" in df.columns:
        df["date_posted"] = pd.to_datetime(df["date_posted"], errors="coerce")
        df["month"] = df["date_posted"].dt.to_period("M")
        trends = df["month"].value_counts().sort_index()
        trends.to_csv(os.path.join(output_dir, "job_trends.csv"))
        plt.figure(figsize=(10,6))
        trends.plot(kind="line", marker="o", color="orange")
        plt.title("Job Postings Over Time")
        plt.xlabel("Month")
        plt.ylabel("Job Postings")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(figures_dir, "job_trends.png"))
        plt.close()
        print("✅ Job trends over time saved")

    # ---- Jobs by Location ----
    if "location" in df.columns:
        top_locations = df["location"].value_counts().head(10)
        top_locations.to_csv(os.path.join(output_dir, "top_locations.csv"))
        plt.figure(figsize=(10,6))
        top_locations.plot(kind="bar", color="salmon", edgecolor="black")
        plt.title("Top 10 Job Locations")
        plt.xlabel("Location")
        plt.ylabel("Job Postings")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(os.path.join(figures_dir, "top_locations.png"))
        plt.close()
        print("✅ Job locations analysis saved")

    print(f"🎉 All analyses completed. CSVs → {output_dir}, Figures → {figures_dir}")


if __name__ == "__main__":
    input_file = "data/cleaned/cleaned_jobs.csv"
    output_dir = "outputs/analysis"
    figures_dir = "outputs/figures"

    analyze_jobs(input_file, output_dir, figures_dir)
