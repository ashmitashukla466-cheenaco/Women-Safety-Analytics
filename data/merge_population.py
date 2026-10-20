import pandas as pd
import re

crime = pd.read_csv("data/processed/crime_against_women_clean.csv")
id_cols = ["year", "state_name", "state_code", "district_name"]
crime["total_cases"] = crime[[c for c in crime.columns if c not in id_cols]].sum(axis=1)

census = pd.read_excel("data/raw/DDW_PCA0000_2011_Indiastatedist.xlsx")
census = census[(census["Level"] == "DISTRICT") & (census["TRU"] == "Total")]
census = census[["State", "Name", "TOT_P", "TOT_F"]].copy()
census.columns = ["state_code_2011", "district_name", "pop_total_2011", "pop_female_2011"]

state_map = {
    1: "Jammu & Kashmir", 2: "Himachal Pradesh", 3: "Punjab", 4: "Chandigarh",
    5: "Uttarakhand", 6: "Haryana", 7: "Delhi", 8: "Rajasthan", 9: "Uttar Pradesh",
    10: "Bihar", 11: "Sikkim", 12: "Arunachal Pradesh", 13: "Nagaland", 14: "Manipur",
    15: "Mizoram", 16: "Tripura", 17: "Meghalaya", 18: "Assam", 19: "West Bengal",
    20: "Jharkhand", 21: "Odisha", 22: "Chhattisgarh", 23: "Madhya Pradesh",
    24: "Gujarat", 25: "D&N Haveli and Daman & Diu", 26: "D&N Haveli and Daman & Diu",
    27: "Maharashtra", 28: "Andhra Pradesh", 29: "Karnataka", 30: "Goa",
    31: "Lakshadweep", 32: "Kerala", 33: "Tamil Nadu", 34: "Puducherry",
    35: "A&N Islands",
}
census["state_name"] = census["state_code_2011"].map(state_map)
census["district_name"] = census["district_name"].str.strip().str.title()

telangana = ["Adilabad", "Nizamabad", "Karimnagar", "Medak", "Hyderabad",
             "Rangareddy", "Mahbubnagar", "Nalgonda", "Warangal", "Khammam"]
census.loc[(census["state_name"] == "Andhra Pradesh") & census["district_name"].isin(telangana), "state_name"] = "Telangana"
census.loc[census["district_name"].isin(["Leh(Ladakh)", "Kargil"]), "state_name"] = "Ladakh"

name_fix = {
    ("Assam", "Marigaon"): "Morigaon",
    ("Bihar", "Purbi Champaran"): "Purba Champaran",
    ("Jammu & Kashmir", "Bandipora"): "Bandipore",
    ("Jammu & Kashmir", "Baramulla"): "Baramula",
    ("Jharkhand", "Koderma"): "Kodarma",
    ("Jharkhand", "Sahebganj"): "Sahibganj",
    ("Karnataka", "Bagalkote"): "Bagalkot",
    ("Karnataka", "Chamarajanagara"): "Chamarajanagar",
    ("Karnataka", "Chikkamagaluru"): "Chikmagalur",
    ("Karnataka", "Davangere"): "Davanagere",
    ("Karnataka", "Tumakuru"): "Tumkur",
    ("Maharashtra", "Ahmednagar"): "Ahmadnagar",
    ("Maharashtra", "Buldhana"): "Buldana",
    ("Maharashtra", "Gondia"): "Gondiya",
    ("Odisha", "Nabarangpur"): "Nabarangapur",
    ("Rajasthan", "Chittorgarh"): "Chittaurgarh",
    ("Rajasthan", "Jalore"): "Jalor",
    ("Rajasthan", "Jhunjhunu"): "Jhunjhunun",
    ("Tamil Nadu", "Kanchipuram"): "Kancheepuram",
    ("Tamil Nadu", "Villupuram"): "Viluppuram",
    ("Telangana", "Mahabubnagar"): "Mahbubnagar",
    ("West Bengal", "Malda"): "Maldah",
    ("West Bengal", "Purulia"): "Puruliya",
    ("Uttarakhand", "Haridwar"): "Hardwar",
    ("Uttarakhand", "Udam Singh Nagar"): "Udham Singh Nagar",
    ("A&N Islands", "South Andamans"): "South Andaman",
    ("Andhra Pradesh", "Ananthapuramu"): "Anantapur",
    ("Assam", "Kamrup Metro"): "Kamrup Metropolitan",
    ("Chhattisgarh", "Korea"): "Koriya",
    ("Gujarat", "Dang"): "The Dangs",
    ("Haryana", "Gurugram"): "Gurgaon",
    ("Haryana", "Nuh"): "Mewat",
    ("Jammu & Kashmir", "Budgam"): "Badgam",
    ("Jammu & Kashmir", "Poonch"): "Punch",
    ("Jammu & Kashmir", "Shopian"): "Shupiyan",
    ("Jharkhand", "East Singhbum"): "Purbi Singhbhum",
    ("Jharkhand", "West Singhbhum"): "Pashchimi Singhbhum",
    ("Karnataka", "Ballari"): "Bellary",
    ("Karnataka", "Belagavi"): "Belgaum",
    ("Karnataka", "Bengaluru Urban"): "Bangalore",
    ("Karnataka", "Kalaburagi"): "Gulbarga",
    ("Karnataka", "Mysuru"): "Mysore",
    ("Karnataka", "Shivamogga"): "Shimoga",
    ("Karnataka", "Vijayapura"): "Bijapur",
    ("Lakshadweep", "Lakshadweep District"): "Lakshadweep",
    ("Madhya Pradesh", "Narmadapuram"): "Hoshangabad",
    ("Maharashtra", "Beed"): "Bid",
    ("Maharashtra", "Chhatrapati Sambhajinagar"): "Aurangabad",
    ("Maharashtra", "Dharashiv"): "Osmanabad",
    ("Maharashtra", "Raigad"): "Raigarh",
    ("Mizoram", "Siaha"): "Saiha",
    ("Odisha", "Boudh"): "Baudh",
    ("Odisha", "Deogarh"): "Debagarh",
    ("Odisha", "Sonepur"): "Subarnapur",
    ("Puducherry", "Pondicherry"): "Puducherry",
    ("Punjab", "Ferozepur"): "Firozpur",
    ("Punjab", "Sri Muktsar Sahib"): "Muktsar",
    ("Punjab", "S.A.S Nagar"): "Sahibzada Ajit Singh Nagar",
    ("Rajasthan", "Dholpur"): "Dhaulpur",
    ("Sikkim", "Gangtok"): "East District",
    ("Sikkim", "Mangan"): "North District",
    ("Sikkim", "Namchi"): "South District",
    ("Sikkim", "Gyalshing"): "West District",
    ("Tamil Nadu", "Tuticorin"): "Thoothukkudi",
    ("Uttar Pradesh", "Prayagraj"): "Allahabad",
    ("Uttar Pradesh", "Ayodhya"): "Faizabad",
    ("Uttar Pradesh", "Bhadohi"): "Sant Ravidas Nagar (Bhadohi)",
    ("Uttar Pradesh", "Amroha"): "Jyotiba Phule Nagar",
    ("Uttar Pradesh", "Hathras"): "Mahamaya Nagar",
    ("Uttar Pradesh", "Kasganj"): "Kanshiram Nagar",
    ("Uttarakhand", "Pauri Garhwal"): "Garhwal",
    ("West Bengal", "Cooch Behar"): "Koch Bihar",
    ("West Bengal", "Darjeeling"): "Darjiling",
    ("West Bengal", "Hooghly"): "Hugli",
    ("West Bengal", "Howrah"): "Haora",
    ("West Bengal", "North 24 Parganas"): "North Twenty Four Parganas",
    ("West Bengal", "South 24 Parganas"): "South Twenty Four Parganas",
}

def key(s):
    return re.sub(r"[^a-z0-9]", "", s.lower().replace("&", "and"))

crime["census_name"] = [name_fix.get((s, d), d) for s, d in zip(crime["state_name"], crime["district_name"])]
crime["key"] = crime["census_name"].map(key)
census["key"] = census["district_name"].map(key)

df = crime.merge(census[["state_name", "key", "pop_total_2011", "pop_female_2011"]], on=["state_name", "key"], how="left")
df = df.drop(columns=["census_name", "key"])

matched = df["pop_female_2011"].notna()
print("rows matched:", matched.sum(), "of", len(df))
print("share of cases matched:", round(df.loc[matched, "total_cases"].sum() / df["total_cases"].sum() * 100, 1), "%")
print(df.assign(matched=matched).groupby("year")["matched"].mean().round(3))
print("unmatched districts:", df[~matched][["state_name", "district_name"]].drop_duplicates().shape[0])

df = df[matched].copy()
unreliable = (df["state_name"] == "Delhi") | df["district_name"].isin(["Mumbai", "Hyderabad"])
df["rate_reliable"] = ~unreliable

crime_cols = [c for c in crime.columns if c not in id_cols + ["total_cases", "census_name", "key"]]
for c in crime_cols + ["total_cases"]:
    df[c + "_rate"] = df[c] / df["pop_female_2011"] * 100000

print(df["total_cases_rate"].describe())
print(df[(df["year"] == 2022) & df["rate_reliable"]].nlargest(10, "total_cases_rate")[["state_name", "district_name", "total_cases", "total_cases_rate"]])

df.to_csv("data/processed/district_rates.csv", index=False)
print("saved", df.shape)