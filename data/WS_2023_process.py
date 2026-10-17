import pandas as pd
import os
url="data/raw/Women_Safety_NCRB_2023_Data.xlsx"
year="2023"
output_folder =r"C:\Users\ashmi\OneDrive\ML_demo\Documents\Attachments\Desktop\ML_project\data\processed"
os.makedirs(output_folder, exist_ok=True)

xls=pd.ExcelFile(url)
print(xls.sheet_names) #prints the sheets name in the workbook

for sheet in xls.sheet_names:
    if sheet=='README':
        continue #skips the processing in the information sheet

    df=pd.read_excel(url,sheet_name=sheet)
    df.columns=df.columns.str.strip().str.lower().str.replace(" ","_")
    df=df.dropna(how="all")
    df=df.dropna(axis=1,how="all")
    df=df.drop_duplicates()
    first_col=df.columns[0]
    df=df[~df[first_col].astype(str).str.upper().str.startswith("TOTAL")]
    name = sheet.lower()
    if year not in name:
        name = name + "_" + year
    df.to_csv(os.path.join(output_folder, name + ".csv"), index=False)
    print(sheet, "→", df.shape)
