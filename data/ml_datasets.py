import pandas as pd

df = pd.read_csv("data/processed/district_rates.csv")
df = df[df["rate_reliable"]].copy()
df = df.sort_values(["state_name", "district_name", "year"])

df["district_id"] = df["state_name"] + "_" + df["district_name"]
df["previous_year_cases"] = df.groupby("district_id")["total_cases"].shift(1)
df["previous_year_rate"] = df.groupby("district_id")["total_cases_rate"].shift(1)

df = df.dropna(subset=["previous_year_cases", "previous_year_rate"])
df.to_csv("data/processed/ml_dataset.csv", index=False)

print("Dataset shape:", df.shape)
print("Years:", sorted(df["year"].unique()))
print("Unique districts:", df["district_id"].nunique())
print("Saved: data/processed/ml_dataset.csv")