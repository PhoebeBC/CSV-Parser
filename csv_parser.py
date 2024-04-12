import csv
import pandas as pd
import numpy as np
import re

# when printing columns they are all shown
pd.set_option('display.max_columns', None)


def filter_dataframe(df, col, val):
    # This should filter the column col based on the value val and return
    # the df after this has been done.
    df = df[(df[col] == val)]
    return df


def get_column_headers(df):
    column_headers = []
    for col in df.columns:
        column_headers.append(col)
    return column_headers


def get_rows(df, num_rows):
    return df.head(num_rows)


def get_info(df):
    return df.info()


def set_index_column(df, col):
    df.set_index(col, inplace=True)
    return df


def remove_rows_with_empty_cells(df):
    return df.dropna()


# inplace = True means dataframe is updated, not that a new one is created
def replace_empty_cells(df, new_val, col='all columns'):
    if col == 'all columns':
        return df.fillna(new_val, inplace=True)
    else:
        return df[col].fillna(new_val, inplace=True)


def change_cell_by_row(df, row_num, col, new_val):
    df.loc[row_num, col] = new_val
    return df


def remove_duplicate_rows(df):
    return df.drop_duplicates(inplace=True)


def dataframe_column_reorder(df):
    # creating a list of column headers, where the list index = column index
    column_headers = get_column_headers(df)
    print(f"The current column order is\n{', '.join(column_headers)}")
    new_ordering_string = input("Please enter the new column order in the same format it is given above.")
    new_ordering = re.split(r'\s*,\s*', new_ordering_string)
    new_column_index = []
    for col in column_headers:
        new_column_index.append(new_ordering.index(col))
    return new_column_index


def csv_parser(csv_file, file_location, new_file_name):
    with open(file_location + r"\\" + csv_file, mode='r') as file:
    # parsing a csv into a pandas dataframe
        dataframe = pd.read_csv(file)
    new_column_index = dataframe_column_reorder(dataframe)
    reordered_dataframe = dataframe.iloc[:, new_column_index]
    # Converting back to csv
    # reordered_csv = reordered_dataframe.to_csv(new_file_name + '.csv', sep=',', index=False, encoding='utf-8')
    with open(file_location + r"\\" + new_file_name + '.csv', mode='w', newline='') as file:
        reordered_dataframe.to_csv(file, sep=',', index=False, encoding='utf-8')


# with open(csv_file_path, mode='r') as file:

csv_parser("csv_parser_test.csv", r"C:\Users\phoeb\Documents", "csv_parser_test_reordered")
