from typing import Callable, Any
import pandas as pd
import os
from sales_invoice import format_data_in_rows, format_excel


def date_format(df, date):
    '''
    Adjusts the date column to the required format of dd/mm/yyyy
    '''
    df[date] = pd.to_datetime(df[date])
    date_format: Callable[[Any], Any] = lambda x: x.strftime('%d/%m/%Y')
    df[date] = df[date].apply(date_format)
    return df


def create_empty_df(df):
    '''
    Creating an empty dataframe with the same number of rows as df to be filled with data from df later.
    '''
    number_of_rows = len(df)
    # Column names
    column_names = ['Type', 'Account Reference', 'Nominal A/C Ref', 'Department Code', 'Date', 'Details',
                        'Reference', 'Net Amount', 'Tax Code', 'Tax Amount', 'Exchange Rate', 'Extra Reference',
                        'User Name', 'Project Refn', 'Cost Code Refn', 'Country of VAT', 'Report Type', 'Fund']
    # Create a DataFrame with n rows for each column
    df_formatted_empty = pd.DataFrame(columns=column_names, index=range(number_of_rows))
    return df_formatted_empty


def excel_parser(excel_file):
    # Path for Excel
    xls = pd.ExcelFile(excel_file)
    # convert one tab into a dataframe - setting the column headers to be the 2nd row
    df1 = pd.read_excel(xls, 'Sales Invoice VAT 20%', header=1)
    df2 = pd.read_excel(xls, 'UK purchase invoices', header=1)

    # only pulling rows where the date is not empty
    df1 = df1.dropna(subset=['Date'])
    # Adjusting date column to correct format
    df1 = date_format(df1, 'Date')
    # Creating the output dataframe to be filled with data
    df1_formatted_empty = create_empty_df(df1)
    # Filling the output dataframe with data
    df1_formatted = format_data_in_rows(df1, df1_formatted_empty)
    # Outputting the dataframe to an excel
    writer = pd.ExcelWriter(f"{os.path.splitext(excel_file)[0]} FANCY.xlsx", engine='xlsxwriter')
    df1_formatted.to_excel(writer, index=False, sheet_name='report')
    # Formatting excel
    format_excel(writer)

    # only pulling rows where the date is not empty
    df2 = df2.dropna(subset=['Belegdatum'])
    # Adjusting date column to correct format
    df2 = date_format(df2, 'Belegdatum')
    # Creating the output dataframe to be filled with data
    df2_formatted_empty = create_empty_df(df2)
    # Filling the output dataframe with data
    df2_formatted = format_data_in_rows(df2, df2_formatted_empty)
    # Outputting the dataframe to an excel
    writer = pd.ExcelWriter(f"{os.path.splitext(excel_file)[0]} FANCY2.xlsx", engine='xlsxwriter')
    df2_formatted.to_excel(writer, index=False, sheet_name='report')
    # Formatting excel
    format_excel(writer)

    # # selecting the columns needed
    # df2_extracted = df2.iloc[:, [0, 5, 7,8]]
    # # only pulling rows where the date is not empty
    # df2_extracted = df2_extracted.dropna(subset=['Belegdatum'])
    # # removing timestamp from date
    # df2_extracted['Belegdatum'] = df2_extracted['Belegdatum'].dt.date
    # # Using found location to find where to save new file
    # df2_file_name = f"{os.path.splitext(excel_file)[0]} UKPI.xlsx"
    # # Write the DataFrame back to the Excel file
    # df2_extracted.to_excel(df2_file_name,index=False)
    # return df1_file_name


excel_parser(r"C:\Users\phoeb\Documents\Work\Company software solutions\test vat return.xlsx")
