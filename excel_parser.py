import pandas as pd
import os


def excel_parser(excel_file):
    xls = pd.ExcelFile(excel_file)
    # convert one tab into a dataframe - setting the column headers to be the 2nd row
    df1 = pd.read_excel(xls, 'Sales Invoice VAT 20%', header=1)
    df2 = pd.read_excel(xls, 'UK purchase invoices', header=1)

    # selecting the columns needed
    df1_extracted = df1.iloc[:, [0, 1, 3, 5, 7]]
    # only pulling rows where the date is not empty
    df1_extracted = df1_extracted.dropna(subset=['Date'])
    # removing timestamp from date
    df1_extracted['Date'] = df1_extracted['Date'].dt.date
    # Using found location to find where to save new file
    df1_file_name = f"{os.path.splitext(excel_file)[0]} SIV.xlsx"
    # Write the DataFrame back to the Excel file
    df1_extracted.to_excel(df1_file_name, index=False)

    # selecting the columns needed
    df2_extracted = df2.iloc[:, [0, 5, 7,8]]
    # only pulling rows where the date is not empty
    df2_extracted = df2_extracted.dropna(subset=['Belegdatum'])
    # removing timestamp from date
    df2_extracted['Belegdatum'] = df2_extracted['Belegdatum'].dt.date
    # Using found location to find where to save new file
    df2_file_name = f"{os.path.splitext(excel_file)[0]} UKPI.xlsx"
    # Write the DataFrame back to the Excel file
    df2_extracted.to_excel(df2_file_name,index=False)


excel_parser(r"C:\Users\phoeb\Documents\Work\Company software solutions\test vat return.xlsx")

