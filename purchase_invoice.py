import logging
import re

from custom_exception import ExcelParserException

logger = logging.getLogger("Accounts_Formatter")

# creating reg expression for each column we need data from
check_gegenkonto = re.compile(r'^\s*gegenkonto\s*$', re.IGNORECASE)
check_belegnummer = re.compile(r'^\s*belegnummer\s*$', re.IGNORECASE)
check_kurzbezeichnung = re.compile(r'^\s*kurzbezeichnung\s*$', re.IGNORECASE)
check_typ = re.compile(r'^\s*typ\s*$', re.IGNORECASE)
check_net_amount = re.compile(r'^\s*net\samount\s*$', re.IGNORECASE)
check_amount_vat = re.compile(r'^\s*amount\svat\s*$', re.IGNORECASE)
# column_headers_needed = [gegenkonto, date_column_name, belegnummer, kurzbezeichnung, typ, net_amount, amount_vat]


def tab_header_name_check(name, check, name_type):
    """
    Checking that the tabs we have found are a close match for what we are expecting to ensure pulling data from
    correct tab or clumn header.
    """
    if check.match(name):
        logger.info("name match for %s", name)
        logger.info("name match for type %s", name_type)
        return 0
    return 1


def check_header_names(df, date_column_name):
    # grabbing column name from df to check
    column_headers = df.columns.tolist()
    # creating empty list to be filled when we find a column header match
    column_headers_needed = [""]*7
    for column_name in column_headers:
        if tab_header_name_check(column_name, check_gegenkonto, "header") == 0:
            column_headers_needed[0] = column_name
        elif tab_header_name_check(column_name, check_belegnummer, "header") == 0:
            column_headers_needed[2] = column_name
        elif tab_header_name_check(column_name, check_kurzbezeichnung, "header") == 0:
            column_headers_needed[3] = column_name
        elif tab_header_name_check(column_name, check_typ, "header") == 0:
            column_headers_needed[4] = column_name
        elif tab_header_name_check(column_name, check_net_amount, "header") == 0:
            column_headers_needed[5] = column_name
        elif tab_header_name_check(column_name, check_amount_vat, "header") == 0:
            column_headers_needed[6] = column_name
    column_headers_needed[1] = date_column_name

    # if any elements are empty we havent found all the right column names
    for column in column_headers_needed:
        if column == "":
            raise ExcelParserException("Column names for purchases are incorrect")
    return column_headers_needed


def fill_uniform_data_purchase(df, df_empty, column_headers_for_data):
    df_empty.iloc[:, 1] = df.loc[:, column_headers_for_data[0]]
    # Setting Date E4
    df_empty.iloc[:, 4] = df.loc[:, column_headers_for_data[1]]
    # Setting Reference F5
    df_empty.iloc[:, 5] = df.loc[:, column_headers_for_data[2]]
    # Setting Details G6
    df_empty.iloc[:, 6] = df.loc[:, column_headers_for_data[3]]
    # Setting Tax Code I8
    df_empty.iloc[:, 8] = "T1"
    return df_empty


def fill_dependant_data_purchase(df, df_partial_fill, column_headers_for_data):
    rows = len(df)
    for row in range(rows):
        if df.at[row, column_headers_for_data[4]] == "Eingangsrechnung":
            logger.info("Name for invoice type found in purchase invoices")
            # Setting Type A0
            df_partial_fill.iat[row, 0] = "PI"
            # Setting Net Amount H7
            df_partial_fill.iat[row, 7] = abs(df.at[row, column_headers_for_data[5]])
            # Setting Tax Amount J9
            df_partial_fill.iat[row, 9] = abs(df.at[row, column_headers_for_data[6]])
            # Column D needs to be empty, but we will use to determine if invoice or credit
            df_partial_fill.iat[row, 3] = "1"
        else:
            df_partial_fill.iat[row, 0] = "PC"
            df_partial_fill.iat[row, 7] = df.at[row, column_headers_for_data[5]]
            df_partial_fill.iat[row, 9] = df.at[row, column_headers_for_data[6]]
            df_partial_fill.iat[row, 3] = "0"
        # Setting Nominal A/C Ref C2
        if df.iat[row, 5] == "THE TAX DEPARTM":
            df_partial_fill.iat[row, 2] = 7601
        else:
            df_partial_fill.iat[row, 2] = 5000
    df_partial_fill["Net Amount"] = df_partial_fill["Net Amount"].astype(float)
    df_partial_fill["Tax Amount"] = df_partial_fill["Tax Amount"].astype(float)
    return df_partial_fill


def fill_data_for_purchase_invoice(df, df_empty, date_column_name):
    """
    Fills in the data for the empty dataframe df_empty using data from the Excel tab in df and the
    requirements given. Returns a complete dataframe.
    """
    # column_headers = ["Belegdatum", "Belegnummer", "Sequenznummer", "Typ", "Gegenkonto", "Kurzbezeichnung",
    # "BW", "Net Amount", "Amount VAT", "Notiz"]
    column_headers_for_data = check_header_names(df, date_column_name)
    df_partial_fill = fill_uniform_data_purchase(df, df_empty, column_headers_for_data)
    df_filled = fill_dependant_data_purchase(df, df_partial_fill, column_headers_for_data)
    logger.info("Sales invoice data filled")
    return df_filled
