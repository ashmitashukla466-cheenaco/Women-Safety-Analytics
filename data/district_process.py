import pandas as pd
import os

df = pd.read_csv("data/raw/districtwise-crime-against-women-2017-onwards.csv")
output_folder = "data/processed"
print("saving to:", os.path.abspath(output_folder))
os.makedirs(output_folder, exist_ok=True)

print("shape:", df.shape)
print(df.isnull().sum()[df.isnull().sum() > 0])
print("year range:", df["year"].min(), df["year"].max())
print("states:", df["state_name"].nunique())
print("districts:", df["district_name"].nunique())
print("negative values:", (df.select_dtypes(include="number") < 0).sum().sum())
print(df[df["kidnapping_for_ransom"].isnull()]["year"].value_counts().sort_index())

df = df.drop(columns=["id", "kidnapping_for_ransom"])
print("duplicates:", df.duplicated().sum())
df = df.drop_duplicates()

for c in ["state_name", "district_name"]:
    df[c] = df[c].astype(str).str.strip().str.title()

state_fix = {
    "Andaman And Nicobar Islands": "A&N Islands",
    "Jammu And Kashmir": "Jammu & Kashmir",
    "The Dadra And Nagar Haveli And Daman And Diu": "D&N Haveli and Daman & Diu",
}
df["state_name"] = df["state_name"].replace(state_fix)

district_fix = {
    ("Andhra Pradesh", "Anantapur"): "Ananthapuramu",
    ("Andhra Pradesh", "Spsr Nellore"): "Sri Potti Sriramulu Nellore",
    ("Andhra Pradesh", "Visakhapatanam"): "Visakhapatnam",
    ("Haryana", "Charki Dadri"): "Charkhi Dadri",
}
for (state, old), new in district_fix.items():
    df.loc[(df["state_name"] == state) & (df["district_name"] == old), "district_name"] = new

id_cols = ["year", "state_name", "state_code", "district_name"]
crime_cols = [c for c in df.columns if c not in id_cols + ["district_code", "registration_circles"]]
df = df.groupby(id_cols, as_index=False)[crime_cols].sum()

print("final shape:", df.shape)
print("nulls:", df.isnull().sum().sum())
print(df.groupby("year").size())

df.to_csv(os.path.join(output_folder, "crime_against_women_clean.csv"), index=False)