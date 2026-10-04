import pandas as pd
from ydata_profiling import ProfileReport

# Load your cleaned dataset
df = pd.read_csv("data/cleaned/cleaned_jobs.csv")

# Generate the profile report
profile = ProfileReport(
    df,
    title="Job Skills Data Profiling Report",
    explorative=True
)

# Save the HTML report
output_path = "artifacts/job_skills_profile.html"
profile.to_file(output_path)

print(f"✅ Profiling report saved at: {output_path}")
