import pandas as pd
import os
import sys
import re

sys.path.append(r'C:\Users\phoeb\PycharmProjects\CSV-Parser')
from sales_invoice import fill_data_for_sales_invoice
from purchase_invoice import fill_data_for_purchase_invoice
from new_customer_supplier import check_for_new_customer, check_for_new_supplier


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


def format_excel(writer, sheet):
    '''
    Formats the output excel so value formats are correct and column widths are set
    so all column headers can be seen.
    '''
    workbook = writer.book
    worksheet = writer.sheets[sheet]
    money_format = workbook.add_format({'num_format': '#,##0.00'})
    # Setting column formats
    worksheet.set_column('E:Q', 12)
    worksheet.set_column('H:H', 12, money_format)
    worksheet.set_column('J:J', 12, money_format)

    small_columns = ['A:A', 'I:I', 'R:R']
    for col in small_columns:
        worksheet.set_column(col, 8)

    big_columns = ['B:D', 'G:G', 'L:L', 'O:P']
    for col in big_columns:
        worksheet.set_column(col, 17)

    writer.close()


def convert_to_excel(df, output_path, invoice_type, invoice_or_credit="Invoice"):
    # Likely that purchase credit has no entries so don't want to output if this is the case
    if not df.empty:
        # Setting column back to emtpy after using it to filter credit or invoice
        df.loc[:, "Department Code"] = ""
        # Pushing to excel and ensuring date column is in the correct format
        writer = pd.ExcelWriter(f"{output_path} {invoice_type} {invoice_or_credit}.xlsx", engine='xlsxwriter',
                                date_format="dd/mm/yyyy", datetime_format="dd/mm/yyyy")
        df.to_excel(writer, index=False, sheet_name=invoice_type + invoice_or_credit)
        # Formatting excel
        format_excel(writer, invoice_type + invoice_or_credit)


def convert_to_excel_new(df, output_path, invoice_type):
    if not df.empty:
        print(df)
        if invoice_type == 'Sales':
            account_type = "Customer"
        else:
            account_type = "Supplier"
        # Pushing to excel
        writer = pd.ExcelWriter(f"{output_path} New {account_type} List.xlsx", engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name=f"New {account_type} List")
        # Formatting
        worksheet = writer.sheets[f"New {account_type} List"]
        worksheet.set_column('A:B', 16)
        writer.close()


def generate_dataframe_output(df, invoice_type, output_path, date_column_name):
    # only pulling rows where the date is not empty
    df = df.dropna(subset=[date_column_name])
    # Creating the output dataframe to be filled with data
    df_formatted_empty = create_empty_df(df)
    # Filling the output dataframe with data
    if invoice_type == 'Sales':
        df_formatted = fill_data_for_sales_invoice(df, df_formatted_empty)
        # Checking if new customers are in the data and producing excel for those new customers
        df_new_customers_suppliers = check_for_new_customer(df)
    else:
        df_formatted = fill_data_for_purchase_invoice(df, df_formatted_empty, date_column_name)
        df_new_customers_suppliers = check_for_new_supplier(df)

    # Splitting data frame into credit transactions and invoice transactions
    df_invoice = df_formatted.loc[df_formatted["Department Code"] == "1"]
    df_credit = df_formatted.loc[df_formatted["Department Code"] == "0"]

    convert_to_excel(df_invoice, output_path, invoice_type)
    convert_to_excel(df_credit, output_path, invoice_type, "Credit")
    convert_to_excel_new(df_new_customers_suppliers, output_path, invoice_type)


def tab_name_check(tab_name, check):
    '''
    Checking that the tabs we have found are a close match for what we are expecting to ensure pulling data from
    correct tab.
    '''
    print("Name of the sheet:", tab_name)
    if not check.match(tab_name):
        print("Tab name match failure.")
        return 1


def find_date_column(df):
    '''
    Finding the date column header name by searching for the column with a date time format
    '''
    for column in df.columns:
        if df[column].dtype == 'datetime64[ns]':
            print(f"column = {column}")
            return column


def excel_parser(excel_file):
    # Path for Excel
    xls = pd.ExcelFile(excel_file)

    # Want to grab the correct tabs to be formatted
    # Finding first sheet
    first_sheet_name = xls.sheet_names[0]
    second_sheet_name = xls.sheet_names[1]
    # Compare the name of the first sheet with a regular expression
    first_sheet_check = re.compile(r'.*sale\w*\s*invoice\w*\s*vat\s*20%\s*.*', re.IGNORECASE)
    second_sheet_check = re.compile(r'.*uk\s*purchase\w*\s*invoice\w*\s*.*', re.IGNORECASE)
    # Checking tab name is expected
    if (tab_name_check(first_sheet_name, first_sheet_check) == 1 or
            tab_name_check(second_sheet_name, second_sheet_check) == 1):
        return "Error tab name"

    # convert one tab into a dataframe - setting the column headers to be the 2nd row
    df1 = pd.read_excel(xls, first_sheet_name, header=1)
    df2 = pd.read_excel(xls, second_sheet_name, header=1)

    # Saving output path for generated files to be saved into
    output_path = os.path.splitext(excel_file)[0]

    # Finding the date column name to ensure pulling data from correct columns
    date_column = find_date_column(df2)

    generate_dataframe_output(df1, 'Sales', output_path, 'Date')
    generate_dataframe_output(df2, 'Purchase', output_path, date_column)

    return output_path


# excel_parser(
#    r"C:\Users\phoeb\Documents\Work\Company software solutions\Excels Run\VAT Return Nov 23 till Jan 24 TTDL.xlsx")
