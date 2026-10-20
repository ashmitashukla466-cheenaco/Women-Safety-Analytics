import pandas as pd
df=pd.read_csv("data/processed/district_rates.csv")
print("all rows:",df.shape)
#2022 is the latest year and has the most districts; 2020 is distorted by COVID
df=df[df["year"]==2022]
print("2022 rows:",len(df))
#Delhi, Mumbai and Hyderabad have police boundaries that don't match Census districts, so their rates are unreliable
df=df[df["rate_reliable"]]
print("reliable rows:",len(df))
#districts with under 1 lakh women have unstable rates (a few cases swing the rate a lot)
small=df[df["pop_female_2011"]<100000]
print("dropped for small population:",len(small))
print(small["state_name"].value_counts())
df=df[df["pop_female_2011"]>=100000]
print("final rows:",len(df))
print(df["total_cases_rate"].describe())
df.to_csv("data/processed/district_2022_selected.csv",index=False)