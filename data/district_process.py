import pandas as pd
import os

df = pd.read_csv("data/raw/districtwise-crime-against-women-2017-onwards.csv")
output_folder = "data/processed"
print("saving to:", os.path.abspath(output_folder))
os.makedirs(output_folder, exist_ok=True)

# Inspect the raw data before changing anything
print("shape:", df.shape)
print(df.isnull().sum()[df.isnull().sum() > 0])
print("year range:", df["year"].min(), df["year"].max())
print("states:", df["state_name"].nunique())
print("districts:", df["district_name"].nunique())
print("negative values:", (df.select_dtypes(include="number") < 0).sum().sum())
print(df[df["kidnapping_for_ransom"].isnull()]["year"].value_counts().sort_index())

# "id" is unique per row, so it hides duplicates; "kidnapping_for_ransom" is NaN from 2019 (no longer reported)
df = df.drop(columns=["id", "kidnapping_for_ransom"])
print("duplicates:", df.duplicated().sum())
df = df.drop_duplicates()

# Consistent text formatting for names
for c in ["state_name", "district_name"]:
    df[c] = df[c].astype(str).str.strip().str.title()

# State names standardised to match the NCRB 2023/2024 files
state_fix = {
    "Andaman And Nicobar Islands": "A&N Islands",
    "Jammu And Kashmir": "Jammu & Kashmir",
    "The Dadra And Nagar Haveli And Daman And Diu": "D&N Haveli and Daman & Diu",
}
df["state_name"] = df["state_name"].replace(state_fix)

# The source file mislabels some districts in certain years:
# Uttarakhand's districts appear under Uttar Pradesh in 2017
uttarakhand = ["Almora", "Bageshwar", "Chamoli", "Champawat", "Dehradun", "Haridwar", "Nainital",
               "Pauri Garhwal", "Pithoragarh", "Rudra Prayag", "Tehri Garhwal", "Udam Singh Nagar", "Uttar Kashi"]
m = (df["state_name"] == "Uttar Pradesh") & df["district_name"].isin(uttarakhand)
df.loc[m, ["state_name", "state_code"]] = ["Uttarakhand", 5]

# Pondicherry appears under Lakshadweep in 2017
m = df["district_name"] == "Pondicherry"
df.loc[m, ["state_name", "state_code"]] = ["Puducherry", 34]

# Leh and Kargil are listed under Jammu & Kashmir until 2019 and under Ladakh from 2020;
# Ladakh is used for all years so each district keeps one state
m = df["district_name"].isin(["Kargil", "Leh Ladakh"])
df.loc[m, ["state_name", "state_code"]] = ["Ladakh", 37]

# Same district spelled differently across years
district_fix = {
    ("Andhra Pradesh", "Anantapur"): "Ananthapuramu",
    ("Andhra Pradesh", "Spsr Nellore"): "Sri Potti Sriramulu Nellore",
    ("Andhra Pradesh", "Visakhapatanam"): "Visakhapatnam",
    ("Haryana", "Charki Dadri"): "Charkhi Dadri",
}
for (state, old), new in district_fix.items():
    df.loc[(df["state_name"] == state) & (df["district_name"] == old), "district_name"] = new

# A district can have several registration circles (e.g. GRP, Railway);
# sum them so there is one row per district per year
id_cols = ["year", "state_name", "state_code", "district_name"]
crime_cols = [c for c in df.columns if c not in id_cols + ["district_code", "registration_circles"]]
df = df.groupby(id_cols, as_index=False)[crime_cols].sum()

# Expected: (4334, 45), no nulls, 703-750 districts per year
print("final shape:", df.shape)
print("nulls:", df.isnull().sum().sum())
print(df.groupby("year").size())

df.to_csv(os.path.join(output_folder, "crime_against_women_clean.csv"), index=False)