import pandas as pd
from datetime import datetime
import xlsxwriter

def get_column_headers(df):
    column_headers = []
    for col in df.columns:
        column_headers.append(col)
    return column_headers


# Read the Excel file into pandas
xls = pd.ExcelFile(r"C:\Users\phoeb\Documents\Work\Company software solutions\test vat return.xlsx")
# convert one tab into a dataframe - setting the column headers to be the 2nd row
df1 = pd.read_excel(xls, 'Sales Invoice VAT 20%', header=1)
# selecting the columns needed
df1_extracted = df1.iloc[:, [0, 1, 3, 5, 7]]
# only pulling rows where the date is not empty
df1_extracted = df1_extracted.dropna(subset=['Date'])
print(df1_extracted)
df1_extracted['Date'] = df1_extracted['Date'].dt.date
# Write the DataFrame back to the Excel file
df1_extracted.to_excel(r"C:\Users\phoeb\Documents\Work\Company software solutions\test vat return siv.xlsx",
                      index=False)