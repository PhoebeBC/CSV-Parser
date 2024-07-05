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
                logger.debug("Adding Customer to db - reference: %s, name: %s", reference, name)
                db.add_customer(reference, name)
                df_entries.iat[row, 0] = reference
                df_entries.iat[row, 1] = name
            else:
                logger.debug("Customer already in db - reference: %s, name: %s", reference, name)
        else:  # category == supplier
            if db.get_supplier(reference) is None: # This went wrong
                logger.debug("Adding Supplier to db - reference: %s, name: %s", reference, name)
                db.add_supplier(reference, name)
                df_entries.iat[row, 0] = reference
                df_entries.iat[row, 1] = name
            else:
                logger.debug("Supplier already in db - reference: %s, name: %s", reference, name)
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
        df_category = df.loc[:, ["Gegenkonto", "Kurzbezeichnung"]].copy()
    df_new = find_new_entries(df_category, category)
    return df_new
