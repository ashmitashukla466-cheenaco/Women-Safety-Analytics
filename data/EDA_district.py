import pandas as pd
import os
import matplotlib.pyplot as plt

df=pd.read_csv("data/processed/crime_against_women_clean.csv")
os.makedirs("figures",exist_ok=True)

id_cols=["year","state_name","state_code","district_name"]
crime_cols=[c for c in df.columns if c not in id_cols]
df["total_cases"]=df[crime_cols].sum(axis=1)

yearly=df.groupby("year")["total_cases"].sum()
print(yearly)
yearly.plot(marker="o",title="Total Crimes Against Women Yearly")
plt.ylabel("cases")
plt.savefig("figures/yearly_total.png", bbox_inches="tight")
#plt.show()
plt.close()

top_districts = df[df["year"] == 2022].nlargest(10, "total_cases")[["state_name", "district_name", "total_cases"]]
print(top_districts)
top_states=df[df["year"]==2022].groupby("state_name")["total_cases"].sum().nlargest(10)
print(top_states)
top_states.sort_values().plot(kind="barh", title="Top 10 states by cases, 2022")
plt.savefig("figures/top_states_2022.png", bbox_inches="tight")
#plt.show()
plt.close()

crime_totals = df[crime_cols].sum().sort_values(ascending=False)
print(crime_totals.head(10))
crime_totals.head(10).sort_values().plot(kind="barh", title="Top 10 crime types, 2017-2022")
plt.savefig("figures/top_crime_types.png", bbox_inches="tight")
#plt.show()
plt.close()

print(df["total_cases"].describe())