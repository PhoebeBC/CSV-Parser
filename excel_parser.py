import os
import re
import logging
import pandas as pd

from custom_exception import ExcelParserException
from sales_invoice import fill_data_for_sales_invoice
from purchase_invoice import fill_data_for_purchase_invoice
from new_customer_supplier import check_for_new_entry

logger = logging.getLogger("Accounts_Formatter")


def create_empty_df(df):
    """
    Creating an empty dataframe with the same number of rows as df to be filled with data from df later.
    """
    number_of_rows = len(df)
    # Column names
    column_names = ['Type', 'Account Reference', 'Nominal A/C Ref', 'Department Code', 'Date', 'Details',
                    'Reference', 'Net Amount', 'Tax Code', 'Tax Amount', 'Exchange Rate', 'Extra Reference',
                    'User Name', 'Project Refn', 'Cost Code Refn', 'Country of VAT', 'Report Type', 'Fund']
    # Create a DataFrame with n rows for each column
    df_formatted_empty = pd.DataFrame(columns=column_names, index=range(number_of_rows))
    return df_formatted_empty


def format_excel(writer, sheet):
    """
    Formats the output excel so value formats are correct and column widths are set
    so all column headers can be seen.
    """
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


def convert_to_excel_new_entries(df, output_path, invoice_type):
    if not df.empty:
        logger.info(f"new_customer_supplier df: {df}")
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


def splitting_data_into_credit_and_invoice_transactions(df_formatted):
    # Splitting data frame into credit transactions and invoice transactions
    df_invoice = df_formatted.loc[df_formatted["Department Code"] == "1"]
    df_credit = df_formatted.loc[df_formatted["Department Code"] == "0"]
    return df_invoice, df_credit


def generate_dataframe_output(df, tab_type, output_path, date_column_name):
    # only pulling rows where the date is not empty
    df = df.dropna(subset=[date_column_name])
    # Creating the output dataframe to be filled with data
    df_formatted_empty = create_empty_df(df)
    # Filling the output dataframe with data
    if tab_type == 'Sales':
        df_formatted = fill_data_for_sales_invoice(df, df_formatted_empty)
        logger.info("Sales data filled")
        # Checking if new customers are in the data and producing excel for those new customers
        df_new_customers_suppliers = check_for_new_entry(df)
        logger.info("New customers checked")
    else:
        df_formatted = fill_data_for_purchase_invoice(df, df_formatted_empty, date_column_name)
        logger.info("Purchases data filled")
        df_new_customers_suppliers = check_for_new_entry(df, "Supplier")
        logger.info("New Suppliers checked")

    # Splitting data frame into credit transactions and invoice transactions
    df_invoice, df_credit = splitting_data_into_credit_and_invoice_transactions(df_formatted)

    # Converting dataframes to excels
    convert_to_excel(df_invoice, output_path, tab_type)
    convert_to_excel(df_credit, output_path, tab_type, "Credit")
    convert_to_excel_new_entries(df_new_customers_suppliers, output_path, tab_type)


def tab_name_check(tab_name, check):
    """
    Checking that the tabs we have found are a close match for what we are expecting to ensure pulling data from
    correct tab.
    """
    # Checking tab name is expected
    if not check.match(tab_name):
        logger.error("Tab name match failure.")
        return 1
    return 0


def get_sheet_names(xls):
    # Finding first sheet
    first_sheet_name = xls.sheet_names[0]
    logger.info("First sheet name for Sales invoices: %s", first_sheet_name)
    second_sheet_name = xls.sheet_names[1]
    logger.info("Second sheet name for Purchase invoices: %s", second_sheet_name)

    # Compare the name of the first sheet with a regular expression
    first_sheet_check = re.compile(r'.*sale\w*\s*invoice\w*\s*vat\s*20%\s*.*', re.IGNORECASE)
    second_sheet_check = re.compile(r'.*uk\s*purchase\w*\s*invoice\w*\s*.*', re.IGNORECASE)

    # Checking tab name is expected
    if (tab_name_check(first_sheet_name, first_sheet_check) == 1 or
            tab_name_check(second_sheet_name, second_sheet_check) == 1):
        raise ExcelParserException("Tab name is incorrect")
    return first_sheet_name, second_sheet_name

def find_date_column(df):
    """
    Finding the date column header name by searching for the column with a date time format
    """
    for column in df.columns:
        if df[column].dtype == 'datetime64[ns]':
            logger.info(f"Date column name= {column}")
            return column


def create_dataframe(xls, output_path, sheet_name, tab_type):
    df = pd.read_excel(xls, sheet_name, header=1)
    generate_dataframe_output(df, tab_type, output_path, find_date_column(df))


def create_dataframes_from_excel(xls, output_path):
    # Want to grab the correct tabs to be formatted
    first_sheet_name, second_sheet_name = get_sheet_names(xls)
    create_dataframe(xls, output_path, first_sheet_name, 'Sales')
    create_dataframe(xls, output_path, second_sheet_name, 'Purchase')


def excel_parser(excel_file):
    # Path for Excel
    logger.info("Excel being parsed: %s", excel_file)
    xls = pd.ExcelFile(excel_file)
    # Saving output path for generated files to be saved into
    output_path = os.path.splitext(excel_file)[0]
    logger.info("Output path for excels: %s", output_path)
    create_dataframes_from_excel(xls, output_path)
    return output_path

excel_parser(
   r"C:\Users\phoeb\Documents\Work\Company software solutions\Excels Run\VAT Return Nov 23 till Jan 24 TTDL.xlsx")
