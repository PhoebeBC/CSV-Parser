import pandas as pd
from database import AccountsDatabase

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


def check_for_new_customer(df):
    #db.delete_table("customer")
    # Creating a df for just cust ref and name
    df_customer = df.iloc[:, [2, 3]].copy()
    # Removing duplicates
    df_customer.drop_duplicates(inplace=True)
    # Getting num of rows for for loop to iterate through
    rows = len(df_customer)
    # Creating df for new customers
    df_new = pd.DataFrame(columns=column_headers, index=range(rows))
    # Iterating through customer df to find new customers
    for row in range(rows):
        reference = df_customer.iat[row, 0]
        print(f"reference = {reference}")
        name = df_customer.iat[row, 1]
        print(f"name = {name}")
        # If we have a new customer we add to db and to new customer df
        if db.get_customer(reference) is None:
            print(f" row = {row}")
            db.add_customer(reference, name)
            df_new.iat[row, 0] = reference
            df_new.iat[row, 1] = name
    # Removing any extra rows at the end
    df_new = df_new.dropna(subset=["Account Reference"])
    print(f"the df containing new customers:\n {df_new}")
    return df_new


def check_for_new_supplier(df):
    #db.delete_table("supplier")
    # Creating a df for just cust ref and name
    df_supplier = df.iloc[:, [4, 5]].copy()
    # Removing duplicates
    df_supplier.drop_duplicates(inplace=True)
    # Getting num of rows for for loop to iterate through
    rows = len(df_supplier)
    # Creating df for new suppliers
    df_new = pd.DataFrame(columns=column_headers, index=range(rows))
    # Iterating through supplier df to find new suppliers
    for row in range(rows):
        reference = df_supplier.iat[row, 0]
        name = df_supplier.iat[row, 1]
        # If we have a new supplier we add to db and to new supplier df
        if db.get_supplier(reference) is None:
            db.add_supplier(reference, name)
            df_new.iat[row, 0] = reference
            df_new.iat[row, 1] = name
    df_new = df_new.dropna(subset=["Account Reference"])
    return df_new
