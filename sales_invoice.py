import logging
logger = logging.getLogger("Accounts_Formatter")

def fill_uniform_data_sales(df, df_empty):
    # Setting Account Reference B1
    df_empty.iloc[:, 1] = df.iloc[:, 2]
    # Setting Nominal A/C Ref C2
    df_empty.iloc[:, 2] = 4000
    # Setting Date E4
    df_empty.iloc[:, 4] = df.iloc[:, 0]
    # Setting Reference F5
    df_empty.iloc[:, 5] = df.iloc[:, 1]
    # Setting Details G6
    df_empty.iloc[:, 6] = df.iloc[:, 3]
    # Setting Tax Code I8
    df_empty.iloc[:, 8] = "T1"
    return df_empty

def fill_dependant_data_sales(df, df_to_fill):
    rows = len(df)
    for row in range(rows):
        if df.iat[row, 6] == "Invoice":
            # Setting Type A0
            df_to_fill.iat[row, 0] = "SI"
            # Setting Net Amount H7
            df_to_fill.iat[row, 7] = abs(df.iat[row, 7])
            # Setting Tax Amount J9
            df_to_fill.iat[row, 9] = abs(df.iat[row, 5])
            # Column D needs to be empty but we will use to determine if invoice or credit
            df_to_fill.iat[row, 3] = "1"
        else:
            df_to_fill.iat[row, 0] = "SC"
            df_to_fill.iat[row, 7] = df.iat[row, 7]
            df_to_fill.iat[row, 9] = df.iat[row, 5]
            df_to_fill.iat[row, 3] = "0"

    df_to_fill["Net Amount"] = df_to_fill["Net Amount"].astype(float)
    df_to_fill["Tax Amount"] = df_to_fill["Tax Amount"].astype(float)

    return df_to_fill


def fill_data_for_sales_invoice(df, df_empty):
    '''
    Fills in the data for the empty dataframe df_empty using data from the Excel tab in df and the
    requirements given. Returns a complete dataframe.
    '''
    df_partial_fill = fill_uniform_data_sales(df, df_empty)
    df_filled = fill_dependant_data_sales(df, df_partial_fill)
    logger.info("Sales invoice data filled")
    return df_filled
