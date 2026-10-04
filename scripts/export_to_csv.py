#!/usr/bin/env python3
# scripts/export_to_csv.py

import os
import argparse
import pandas as pd

# -----------------------------
# Export consolidated ETL results
# -----------------------------

def ensure_dir(path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)


def merge_and_export(input_dir: str, output_file: str):
    datasets = {}

    # Load job counts
    job_counts_dir = os.path.join(input_dir, "job_counts")
    if os.path.exists(job_counts_dir):
        job_counts = pd.concat([pd.read_csv(os.path.join(job_counts_dir, f)) 
                                for f in os.listdir(job_counts_dir) if f.endswith(".csv")])
        datasets['job_counts'] = job_counts

    # Load salary trends
    salary_dir = os.path.join(input_dir, "salary_trends")
    if os.path.exists(salary_dir):
        salary_trends = pd.concat([pd.read_csv(os.path.join(salary_dir, f)) 
                                   for f in os.listdir(salary_dir) if f.endswith(".csv")])
        datasets['salary_trends'] = salary_trends

    # Load skills frequency
    skills_dir = os.path.join(input_dir, "skills_freq")
    if os.path.exists(skills_dir):
        skills_freq = pd.concat([pd.read_csv(os.path.join(skills_dir, f)) 
                                 for f in os.listdir(skills_dir) if f.endswith(".csv")])
        datasets['skills_freq'] = skills_freq

    # Save each dataset to Excel with multiple sheets
    ensure_dir(output_file)
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        for name, df in datasets.items():
            df.to_excel(writer, sheet_name=name, index=False)

    print(f"Export complete → {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export ETL results to Excel for Power BI")
    parser.add_argument("--input", required=True, help="ETL output directory")
    parser.add_argument("--output", required=True, help="Path to Excel file")
    args = parser.parse_args()

    merge_and_export(args.input, args.output)
