from typing import Callable, Any
import pandas as pd


def format_data_in_rows(df, df_empty):
    '''
    Fills in the data for the empty dataframe df_empty using data from the Excel tab in df and the
    requirements given. Returns a complete dataframe.
    '''
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

    rows = len(df)
    for row in range(rows):
        # Setting Type A0
        if df.iat[row, 6] == "Invoice":
            df_empty.iat[row, 0] = "SI"
        else:
            df_empty.iat[row, 0] = "SC"
        # Setting Net Amount H7
        if df.iat[row, 6] == "Invoice":
            df_empty.iat[row, 7] = abs(df.iat[row, 7]).astype(float)
        else:
            df_empty.iat[row, 7] = df.iat[row, 7].astype(float)
        # Setting Tax Amount J9
        if df.iat[row, 6] == "Invoice":
            df_empty.iat[row, 9] = format(abs(df.iat[row, 5]))
        else:
            df_empty.iat[row, 9] = format(df.iat[row, 5])

    df_empty["Net Amount"] = df_empty["Net Amount"].astype(float)
    df_empty["Tax Amount"] = df_empty["Tax Amount"].astype(float)

    return df_empty



def format_excel(writer):
    wb = writer.book
    ws = writer.sheets['report']
    money_fmt = wb.add_format({'num_format': '#,##0.00'})
    ws.set_column('E:Q', 12)
    small_columns = ['A:A', 'I:I', 'R:R']
    for col in small_columns:
        ws.set_column(col, 8)
    big_columns = ['B:D', 'G:G', 'L:L', 'O:P']
    for col in big_columns:
        ws.set_column(col, 17)
    ws.set_column('H:H', 12, money_fmt)
    ws.set_column('J:J', 12, money_fmt)
    writer.close()