def fill_data_for_purchase_invoice(df, df_empty, date_column_name):
    '''
    Fills in the data for the empty dataframe df_empty using data from the Excel tab in df and the
    requirements given. Returns a complete dataframe.
    '''
    #column_headers = ["Belegdatum", "Belegnummer", "Sequenznummer", "Typ", "Gegenkonto", "Kurzbezeichnung", "BW", "Net Amount", "Amount VAT", "Notiz"]
    # Setting Account Reference B1
    df_empty.iloc[:, 1] = df.loc[:, "Gegenkonto"]
    # Setting Date E4
    df_empty.iloc[:, 4] = df.loc[:, date_column_name]
    # Setting Reference F5
    df_empty.iloc[:, 5] = df.loc[:, "Belegnummer"]
    # Setting Details G6
    df_empty.iloc[:, 6] = df.loc[:, "Kurzbezeichnung"]
    # Setting Tax Code I8
    df_empty.iloc[:, 8] = "T1"

    rows = len(df)
    for row in range(rows):
        if df.iat[row, 3] == "Eingangsrechnung":
            # Setting Type A0
            df_empty.iat[row, 0] = "PI"
            # Setting Net Amount H7
            df_empty.iat[row, 7] = abs(df.at[row, "Net Amount"])
            # Setting Tax Amount J9
            df_empty.iat[row, 9] = abs(df.at[row, "Amount VAT"])
        else:
            df_empty.iat[row, 0] = "PC"
            df_empty.iat[row, 7] = df.at[row, "Net Amount"]
            df_empty.iat[row, 9] = df.at[row, "Amount VAT"]
        # Setting Nominal A/C Ref C2
        if df.iat[row, 5] == "THE TAX DEPARTM":
            df_empty.iat[row, 2] = 7601
        else:
            df_empty.iat[row, 2] = 5000

    df_empty["Net Amount"] = df_empty["Net Amount"].astype(float)
    df_empty["Tax Amount"] = df_empty["Tax Amount"].astype(float)

    return df_empty
