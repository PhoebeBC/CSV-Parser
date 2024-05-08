def fill_data_for_purchase_invoice(df, df_empty):
    '''
    Fills in the data for the empty dataframe df_empty using data from the Excel tab in df and the
    requirements given. Returns a complete dataframe.
    '''
    # Setting Account Reference B1
    df_empty.iloc[:, 1] = df.iloc[:, 4]
    # Setting Date E4
    df_empty.iloc[:, 4] = df.iloc[:, 0]
    # Setting Reference F5
    df_empty.iloc[:, 5] = df.iloc[:, 1]
    # Setting Details G6
    df_empty.iloc[:, 6] = df.iloc[:, 5]
    # Setting Tax Code I8
    df_empty.iloc[:, 8] = "T1"

    rows = len(df)
    for row in range(rows):
        if df.iat[row, 3] == "Eingangsrechnung":
            # Setting Type A0
            df_empty.iat[row, 0] = "PI"
            # Setting Net Amount H7
            df_empty.iat[row, 7] = abs(df.iat[row, 7])
            # Setting Tax Amount J9
            df_empty.iat[row, 9] = abs(df.iat[row, 8])
        else:
            df_empty.iat[row, 0] = "PC"
            df_empty.iat[row, 7] = df.iat[row, 7]
            df_empty.iat[row, 9] = df.iat[row, 8]
        # Setting Nominal A/C Ref C2
        if df.iat[row, 5] == "THE TAX DEPARTM":
            df_empty.iat[row, 2] = 7601
        else:
            df_empty.iat[row, 2] = 5000

    df_empty["Net Amount"] = df_empty["Net Amount"].astype(float)
    df_empty["Tax Amount"] = df_empty["Tax Amount"].astype(float)

    return df_empty
