import pandas as pd
import os
import matplotlib.pyplot as plt

df = pd.read_csv("data/processed/crime_against_women_clean.csv")
os.makedirs("figures", exist_ok=True)

# Every column except the identifiers is a crime count; total_cases is their sum per district-year
id_cols = ["year", "state_name", "state_code", "district_name"]
crime_cols = [c for c in df.columns if c not in id_cols]
df["total_cases"] = df[crime_cols].sum(axis=1)

# Trend over time: total cases across all districts for each year
yearly = df.groupby("year")["total_cases"].sum()
print(yearly)
yearly.plot(marker="o", title="Total Crimes Against Women Yearly")
plt.ylabel("cases")
plt.savefig("figures/yearly_total.png", bbox_inches="tight")
# plt.show()  # enable to preview the chart; the script pauses until the window is closed
plt.close()

# Districts with the most reported cases in 2022 (raw counts, so large districts and cities rank high)
top_districts = df[df["year"] == 2022].nlargest(10, "total_cases")[["state_name", "district_name", "total_cases"]]
print(top_districts)

# State totals for 2022, summing the districts in each state
top_states = df[df["year"] == 2022].groupby("state_name")["total_cases"].sum().nlargest(10)
print(top_states)
top_states.sort_values().plot(kind="barh", title="Top 10 states by cases, 2022")
plt.savefig("figures/top_states_2022.png", bbox_inches="tight")
# plt.show()
plt.close()

# Most common crime types over all years (sorted so the largest bar appears at the top)
crime_totals = df[crime_cols].sum().sort_values(ascending=False)
print(crime_totals.head(10))
crime_totals.head(10).sort_values().plot(kind="barh", title="Top 10 crime types, 2017-2022")
plt.savefig("figures/top_crime_types.png", bbox_inches="tight")
# plt.show()
plt.close()

# Mean far above median shows the data is skewed by a few very large districts,
# which is why rates per lakh and a log transform are used later
print(df["total_cases"].describe())