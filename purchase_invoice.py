import logging
logger = logging.getLogger("Accounts_Formatter")


def fill_uniform_data_purchanse(df, df_empty, date_column_name):
    df_empty.iloc[:, 1] = df.loc[:, "Gegenkonto"]
    # Setting Date E4
    df_empty.iloc[:, 4] = df.loc[:, date_column_name]
    # Setting Reference F5
    df_empty.iloc[:, 5] = df.loc[:, "Belegnummer"]
    # Setting Details G6
    df_empty.iloc[:, 6] = df.loc[:, "Kurzbezeichnung"]
    # Setting Tax Code I8
    df_empty.iloc[:, 8] = "T1"
    return df_empty


def fill_dependant_data_purchase(df, df_partial_fill):
    rows = len(df)
    for row in range(rows):
        if df.iat[row, 3] == "Eingangsrechnung":
            logger.info("Name for invoice type found in purchase invoices")
            # Setting Type A0
            df_partial_fill.iat[row, 0] = "PI"
            # Setting Net Amount H7
            df_partial_fill.iat[row, 7] = abs(df.at[row, "Net Amount"])
            # Setting Tax Amount J9
            df_partial_fill.iat[row, 9] = abs(df.at[row, "Amount VAT"])
            # Column D needs to be empty, but we will use to determine if invoice or credit
            df_partial_fill.iat[row, 3] = "1"
        else:
            df_partial_fill.iat[row, 0] = "PC"
            df_partial_fill.iat[row, 7] = df.at[row, "Net Amount"]
            df_partial_fill.iat[row, 9] = df.at[row, "Amount VAT"]
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
    df_partial_fill = fill_uniform_data_purchanse(df, df_empty, date_column_name)
    df_filled = fill_dependant_data_purchase(df, df_partial_fill)
    logger.info("Sales invoice data filled")
    return df_filled
