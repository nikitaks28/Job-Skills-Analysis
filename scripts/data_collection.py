#!/usr/bin/env python3
# scripts/data_collection.py

import argparse
import csv
import os
import random
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd

# --------------------------
# Utilities
# --------------------------
RANDOM_SEED = 42
random.seed(RANDOM_SEED)

JOB_TITLES = [
    "Data Analyst", "Business Analyst", "Data Scientist", "Data Engineer",
    "Machine Learning Engineer", "BI Analyst", "Analytics Engineer", "SQL Developer",
    "Power BI Developer", "Python Developer"
]
COMPANIES = [
    "TechNova", "FinAxis", "HealthPlus", "RetailHub", "EduSphere", "Cloudify",
    "InnoData", "GreenBank", "MediCore", "LogiChain"
]
LOCATIONS = [
    "Bengaluru, IN", "Hyderabad, IN", "Pune, IN", "Mumbai, IN", "Chennai, IN",
    "Delhi, IN", "Noida, IN", "Gurugram, IN", "Remote, IN", "Remote"
]
INDUSTRIES = [
    "Information Technology", "Banking", "Healthcare", "Retail", "Education",
    "Consulting", "Logistics", "E-commerce"
]
EMPLOYMENT_TYPES = ["Full-time", "Contract", "Internship", "Part-time"]
SENIORITY = ["Entry", "Associate", "Mid-Senior", "Director"]

SKILL_BUCKETS = {
    "Data Analyst": ["excel", "sql", "python", "power bi", "tableau", "statistics", "etl"],
    "Business Analyst": ["excel", "sql", "requirements", "stakeholder mgmt", "power bi"],
    "Data Scientist": ["python", "pandas", "numpy", "scikit-learn", "ml", "nlp", "statistics"],
    "Data Engineer": ["python", "pyspark", "spark", "airflow", "etl", "sql", "aws"],
    "Machine Learning Engineer": ["python", "ml", "mle", "pytorch", "tensorflow", "mlops"],
    "BI Analyst": ["power bi", "dax", "excel", "sql", "reporting"],
    "Analytics Engineer": ["dbt", "sql", "elt", "bigquery", "snowflake"],
    "SQL Developer": ["sql", "t-sql", "pl/sql", "performance tuning"],
    "Power BI Developer": ["power bi", "dax", "power query", "m language", "gateway"],
    "Python Developer": ["python", "flask", "fastapi", "rest", "pandas"]
}

DESCRIPTION_SNIPPETS = [
    "Work with cross-functional teams to deliver insights.",
    "Build and maintain data pipelines and dashboards.",
    "Apply statistical methods to solve business problems.",
    "Collaborate with stakeholders to understand requirements.",
    "Optimize SQL queries and data models for performance.",
]

CURRENCY = "INR"


def ensure_dir(path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)


def generate_rows(n=1000):
    """Generate synthetic job postings."""
    rows = []
    start_date = datetime.today() - relativedelta(months=6)
    for i in range(n):
        title = random.choice(JOB_TITLES)
        company = random.choice(COMPANIES)
        location = random.choice(LOCATIONS)
        industry = random.choice(INDUSTRIES)
        etype = random.choice(EMPLOYMENT_TYPES)
        senior = random.choices(SENIORITY, weights=[45, 30, 20, 5])[0]
        post_date = start_date + timedelta(days=random.randint(0, 180))
        salary_min = random.choice([400000, 600000, 800000, 1000000, None])
        salary_max = salary_min + random.choice([100000, 200000, 400000]) if salary_min else None
        skills = ",".join(sorted(set(random.sample(SKILL_BUCKETS[title], k=min(4, len(SKILL_BUCKETS[title]))))))
        desc = random.choice(DESCRIPTION_SNIPPETS)
        url = f"https://example.com/jobs/{i}"  # placeholder

        rows.append({
            "job_id": f"J{i:06d}",
            "job_title": title,
            "company": company,
            "location": location,
            "post_date": post_date.strftime("%Y-%m-%d"),
            "employment_type": etype,
            "seniority": senior,
            "industry": industry,
            "description": desc,
            "skills": skills,
            "salary_min": salary_min,
            "salary_max": salary_max,
            "currency": CURRENCY,
            "url": url,
        })
    return rows


def write_csv(path: str, rows):
    ensure_dir(path)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def copy_validate_csv(src: str, dst: str):
    df = pd.read_csv(src)
    required = ["job_title", "company", "location", "post_date", "description"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    ensure_dir(dst)
    df.to_csv(dst, index=False)


def scrape_placeholder(out_path: str):
    rows = generate_rows(200)  # stand-in for scraping
    write_csv(out_path, rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Collect or prepare raw job data")
    parser.add_argument("--mode", choices=["generate", "from-csv", "scrape"], required=True)
    parser.add_argument("--out", required=True, help="Output CSV path under data/raw/")
    parser.add_argument("--src", help="Source CSV for from-csv mode")
    parser.add_argument("--rows", type=int, default=1000, help="Rows to generate (generate mode)")
    args = parser.parse_args()

    if args.mode == "generate":
        data = generate_rows(args.rows)
        write_csv(args.out, data)
        print(f"Generated {len(data)} rows → {args.out}")
    elif args.mode == "from-csv":
        if not args.src:
            raise SystemExit("--src is required for from-csv mode")
        copy_validate_csv(args.src, args.out)
        print(f"Validated & copied CSV → {args.out}")
    elif args.mode == "scrape":
        scrape_placeholder(args.out)
        print(f"Created placeholder scraped data → {args.out}")
