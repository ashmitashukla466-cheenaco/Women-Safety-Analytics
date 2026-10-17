import pandas as pd
import os

url = "data/raw/Women_Safety_NCRB_2024_Data.xlsx"
year = "2024"
output_folder = "data/processed"
print("saving to:", os.path.abspath(output_folder))
os.makedirs(output_folder, exist_ok=True)

xls = pd.ExcelFile(url)
print(xls.sheet_names)

for sheet in xls.sheet_names:
    if sheet == "README":
        continue

    df = pd.read_excel(url, sheet_name=sheet)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    df = df.dropna(how="all")
    df = df.dropna(axis=1, how="all")
    df = df.drop_duplicates()
    first_col = df.columns[0]
    df = df[~df[first_col].astype(str).str.upper().str.startswith("TOTAL")]
    name = sheet.lower()
    if year[-2:] not in name:
        name = name + "_" + year
    df.to_csv(os.path.join(output_folder, name + ".csv"), index=False)
    print(sheet, "→", df.shape)