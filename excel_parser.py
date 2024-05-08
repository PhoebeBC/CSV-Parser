import pandas as pd
import os
from sales_invoice import fill_data_for_sales_invoice
from purchase_invoice import fill_data_for_purchase_invoice


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


def generate_dataframe_output(df, invoice_type, output_path, date_column_name):
    # only pulling rows where the date is not empty
    df = df.dropna(subset=[date_column_name])
    # Creating the output dataframe to be filled with data
    df_formatted_empty = create_empty_df(df)
    # Filling the output dataframe with data
    if invoice_type == 'Sales':
        df_formatted = fill_data_for_sales_invoice(df, df_formatted_empty)
    else:
        df_formatted = fill_data_for_purchase_invoice(df, df_formatted_empty)
    # Outputting the dataframe to an excel
    writer = pd.ExcelWriter(f"{output_path} {invoice_type} Invoice.xlsx", engine='xlsxwriter',date_format="dd/mm/yyyy", datetime_format="dd/mm/yyyy")
    df_formatted.to_excel(writer, index=False, sheet_name=invoice_type+'Invoice')
    # Formatting excel
    format_excel(writer, invoice_type+'Invoice')

def excel_parser(excel_file):
    # Path for Excel
    xls = pd.ExcelFile(excel_file)
    # convert one tab into a dataframe - setting the column headers to be the 2nd row
    df1 = pd.read_excel(xls, 'Sales Invoice VAT 20%', header=1)
    df2 = pd.read_excel(xls, 'UK purchase invoices', header=1)

    output_path = os.path.splitext(excel_file)[0]
    generate_dataframe_output(df1, 'Sales', output_path, 'Date')
    generate_dataframe_output(df2,  'Purchase', output_path,'Belegdatum')

    return output_path

# excel_parser(r"C:\Users\phoeb\Documents\Work\Company software solutions\test vat return.xlsx")
