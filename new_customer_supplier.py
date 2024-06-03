import pandas as pd
import logging
from database import AccountsDatabase

logger = logging.getLogger("Accounts_Formatter")

db = AccountsDatabase()
column_headers = ["Account Reference", "Account Name", "Street 1", "Street 2", "Town", "County", "Postcode",
                  "Contact Name", "Telephone Number", "Fax Number", "Analysis 1", "Analysis 2", "Analysis 3",
                  "Department", "VAT Reg No", "MTD Turnover", "YTD Turnover", "Last Year", "Credit Limit", "Terms Text",
                  "Due Days", "Settlement Discount", "Default Nominal", "Tax Code", "Trade Contact", "Telephone 2",
                  "EMail", "WWW", "Discount Rate", "Payment Due Days", "Terms Agreed?", "Bank Name", "Bank Address 1",
                  "Bank Address 2", "Bank Address 3", "Bank Address 4", "Bank Address 5", "Bank Account Name",
                  "Bank Sort Code", "Bank Account No", "Bank BACS Ref", "Online Payments?", "Currency No",
                  "Restrict Mailing?", "Date Account Opened", "Next Credit Review", "Last Credit Review",
                  "Account Status", "Can Apply Charges?", "Country Code", "Priority Trader?", "Override Stock Tax?",
                  "Override Stock Nom?", "Bank Additional 1", "Bank Additional 2", "Bank Additional 3", "Bank IBAN",
                  "Bank BIC Swift", "Bank Roll Number", "Report Password", "DUNS Number", "Payment Method",
                  "Letters Via Email?", "EMail 2", "EMail 3", "Donor Title", "Donor Forename", "Donor Surname",
                  "Gift Aid Declaration Received?", "Declaration Valid From", "Inactive Account", "Payment Due From",
                  "Direct Debit Email", "Twitter Address", "LinkedIn Address", "Facebook Address",
                  "EORI Number", "Incoterms"]


def adding_new_entries(df, df_entries, category):
    rows = len(df)
    for row in range(rows):
        reference = df.iat[row, 0]
        name = df.iat[row, 1]
        if category == "Customer":
            if db.get_customer(reference) is None:
                logger.debug(f"Adding Customer to db - reference: %s, name: %s", reference, name)
                db.add_customer(reference, name)
                df_entries.iat[row, 0] = reference
                df_entries.iat[row, 1] = name
            else:
                logger.debug(f"Customer already in db - reference: %s, name: %s", reference, name)
        else:  # category == supplier
            if db.get_supplier(reference) is None:
                logger.debug(f"Adding Supplier to db - reference: %s, name: %s", reference, name)
                db.add_supplier(reference, name)
                df_entries.iat[row, 0] = reference
                df_entries.iat[row, 1] = name
            else:
                logger.debug(f"Supplier already in db - reference: %s, name: %s", reference, name)
    return df_entries


def find_new_entries(df, category):
    # Removing duplicates
    df.drop_duplicates(inplace=True)
    # Creating df for new entries
    df_entries = pd.DataFrame(columns=column_headers, index=range(len(df)))
    # Iterating through customer df to find new customers
    df_new_entries = adding_new_entries(df, df_entries, category)
    # Removing any extra rows at the end
    df_new_entries = df_new_entries.dropna(subset=["Account Reference"])
    logger.debug(f"The df containing new {category}s columns: %s", df_new_entries.columns)
    logger.debug(f"The df containing new {category}s index: %s", df_new_entries.index)
    return df_new_entries


def check_for_new_entry(df, category="Customer"):
    logger.debug(f"Checking for new {category}s")
    # Creating a df for just cust ref and name
    if category == "Customer":
        df_category = df.iloc[:, [2, 3]].copy()
    else:
        df_category = df.iloc[:, [4, 5]].copy()
    df_new = find_new_entries(df_category, category)
    return df_new

# def check_for_new_customer(df):
#     logger.debug(f"Checking for new customer")
#     # Creating a df for just cust ref and name
#     df_customer = df.iloc[:, [2, 3]].copy()
#     # Removing duplicates
#     df_customer.drop_duplicates(inplace=True)
#     # Creating df for new customers
#     df_new = pd.DataFrame(columns=column_headers, index=range(len(df_customer)))
#     # Iterating through customer df to find new customers
#     for row in df_customer.index:
#         reference = df_customer.iat[row, 0]
#         name = df_customer.iat[row, 1]
#         # If we have a new customer we add to db and to new customer df
#         if db.get_customer(reference) is None:
#             logger.debug(f"Adding Customer to db - reference: %s, name: %s", reference, name)
#             # print(f" row = {row}")
#             db.add_customer(reference, name)
#             df_new.iat[row, 0] = reference
#             df_new.iat[row, 1] = name
#         else:
#             logger.debug(f"Customer already in db - reference: %s, name: %s", reference, name)
#     # Removing any extra rows at the end
#     df_new = df_new.dropna(subset=["Account Reference"])
#     logger.debug(f"The df containing new customers columns: %s", df_new.columns)
#     logger.debug(f"The df containing new customers index: %s", df_new.index)
#     return df_new
#
#
# def check_for_new_supplier(df):
#     # db.delete_table("supplier")
#     # Creating a df for just cust ref and name
#     df_supplier = df.iloc[:, [4, 5]].copy()
#     # Removing duplicates
#     df_supplier.drop_duplicates(inplace=True)
#     # Creating df for new suppliers
#     df_new = pd.DataFrame(columns=column_headers, index=range(len(df_supplier)))
#     # Iterating through supplier df to find new suppliers
#     for row in df_supplier.index:
#         reference = df_supplier.iat[row, 0]
#         name = df_supplier.iat[row, 1]
#         # If we have a new supplier we add to db and to new supplier df
#         if db.get_supplier(reference) is None:
#             db.add_supplier(reference, name)
#             df_new.iat[row, 0] = reference
#             df_new.iat[row, 1] = name
#     df_new = df_new.dropna(subset=["Account Reference"])
#     return df_new
