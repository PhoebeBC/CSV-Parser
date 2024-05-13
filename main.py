import tkinter as ct
from tkinter import IntVar, Canvas, Entry, Button, PhotoImage, messagebox, filedialog, END, Checkbutton
# import sys
# sys.path.append(r'C:\Users\phoeb\PycharmProjects\CSV-Parser')
# from excel_parser import excel_parser
import os
import subprocess
import platform
import re
import pandas as pd
from pathlib import Path
import sys

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    bundle_dir = Path(sys._MEIPASS)
else:
    bundle_dir = Path(__file__).parent

bundle_dir = Path.cwd() / bundle_dir


def fill_data_for_sales_invoice(df, df_empty):
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
        if df.iat[row, 6] == "Invoice":
            # Setting Type A0
            df_empty.iat[row, 0] = "SI"
            # Setting Net Amount H7
            df_empty.iat[row, 7] = abs(df.iat[row, 7])
            # Setting Tax Amount J9
            df_empty.iat[row, 9] = abs(df.iat[row, 5])
        else:
            df_empty.iat[row, 0] = "SC"
            df_empty.iat[row, 7] = df.iat[row, 7]
            df_empty.iat[row, 9] = df.iat[row, 5]

    df_empty["Net Amount"] = df_empty["Net Amount"].astype(float)
    df_empty["Tax Amount"] = df_empty["Tax Amount"].astype(float)

    return df_empty



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

def create_empty_df(df):
    '''
    Creating an empty dataframe with the same number of rows as df to be filled with data from df later.
    '''
    number_of_rows = len(df)
    # Column names
    column_names = ['Type', 'Account Reference', 'Nominal A/C Ref', 'Department Code', 'Date', 'Details',
                        'Reference', 'Net Amount', 'Tax Code', 'Tax Amount', 'Exchange Rate', 'Extra Reference',
                        'User Name', 'Project Refn', 'Cost Code Refn', 'Country of VAT', 'Report Type', 'Fund']
    # Create a DataFrame with n rows for each column
    df_formatted_empty = pd.DataFrame(columns=column_names, index=range(number_of_rows))
    return df_formatted_empty


def format_excel(writer, sheet):
    '''
    Formats the output excel so value formats are correct and column widths are set
    so all column headers can be seen.
    '''
    workbook = writer.book
    worksheet = writer.sheets[sheet]
    money_format = workbook.add_format({'num_format': '#,##0.00'})
    # Setting column formats
    worksheet.set_column('E:Q', 12)
    worksheet.set_column('H:H', 12, money_format)
    worksheet.set_column('J:J', 12, money_format)

    small_columns = ['A:A', 'I:I', 'R:R']
    for col in small_columns:
        worksheet.set_column(col, 8)

    big_columns = ['B:D', 'G:G', 'L:L', 'O:P']
    for col in big_columns:
        worksheet.set_column(col, 17)

    writer.close()


def generate_dataframe_output(df, invoice_type, output_path, date_column_name):
    # only pulling rows where the date is not empty
    df = df.dropna(subset=[date_column_name])
    # Creating the output dataframe to be filled with data
    df_formatted_empty = create_empty_df(df)
    # Filling the output dataframe with data
    if invoice_type == 'Sales':
        df_formatted = fill_data_for_sales_invoice(df, df_formatted_empty)
    else:
        df_formatted = fill_data_for_purchase_invoice(df, df_formatted_empty)
    # Outputting the dataframe to an excel
    writer = pd.ExcelWriter(f"{output_path} {invoice_type} Invoice.xlsx", engine='xlsxwriter',date_format="dd/mm/yyyy", datetime_format="dd/mm/yyyy")
    df_formatted.to_excel(writer, index=False, sheet_name=invoice_type+'Invoice')
    # Formatting excel
    format_excel(writer, invoice_type+'Invoice')

def excel_parser(excel_file):
    # Path for Excel
    xls = pd.ExcelFile(excel_file)
    # convert one tab into a dataframe - setting the column headers to be the 2nd row
    df1 = pd.read_excel(xls, 'Sales Invoice VAT 20%', header=1)
    df2 = pd.read_excel(xls, 'UK purchase invoices', header=1)

    output_path = os.path.splitext(excel_file)[0]
    generate_dataframe_output(df1, 'Sales', output_path, 'Date')
    generate_dataframe_output(df2,  'Purchase', output_path,'Belegdatum')

    return output_path


class CsvParserGui():

    def __init__(self):

        self.root = ct.Tk()

        self.root.geometry("700x500")
        self.root.configure(bg="#ffffff")
        self.root.title("Accounts Software Developed for The Tax Department Ltd")

        self.window = Canvas(self.root, bg="#FFFFFF", height=500, width=700, bd=0,
                             highlightthickness=0, relief="ridge")
        self.window.place(x=0, y=0)

        self.title_background_image = PhotoImage(file=bundle_dir / "images/image_1.png")
        self.title_background = self.window.create_image(350.0, 41.0, image=self.title_background_image)

        self.title_image = PhotoImage(file=bundle_dir / "images/image_2.png")
        self.title = self.window.create_image(237.0, 41.0, image=self.title_image)

        self.background_image = PhotoImage(file=bundle_dir / "images/image_3.png")
        self.background = self.window.create_image(350.0, 291.0, image=self.background_image)

        self.generate_section_image = PhotoImage(file=bundle_dir / "images/image_4.png")
        self.generate_section = self.window.create_image(350.0, 390.0, image=self.generate_section_image)

        self.message_box_text = self.window.create_text(70.0, 411.0, anchor="nw",
                                                        text="Show in file explorer when generated.",
                                                        fill="#000000", font=("Inter", 14 * -1))

        self.check_state = IntVar(self.root, value=1)
        self.click_button = Checkbutton(command=lambda: print("click_button clicked"), anchor="center",
                                        variable=self.check_state, bg="#2f655b")
        self.click_button.place(x=50.0, y=412.0, width=15.0, height=13.0)

        self.check_file_text = self.window.create_text(40.0, 315.0, anchor="nw",
                                                       text="Check you hae selected the correct file, it must be in a "
                                                            ".xlsx format. \nClick Generate Files to proceed.",
                                                       fill="#000000", font=("Inter", 16 * -1))

        self.generate_button_image = PhotoImage(file=bundle_dir / "images/button_2.png")
        self.generate_button = Button(image=self.generate_button_image, borderwidth=0, highlightthickness=0,
                                      command=self.generate_files, relief="flat")
        self.generate_button.place(x=360.0, y=380.0, width=280.0, height=80.0)

        self.select_section_image = PhotoImage(file=bundle_dir / "images/image_5.png")
        self.select_section = self.window.create_image(350.0, 190.0, image=self.select_section_image)

        self.clear_button_image = PhotoImage(file=bundle_dir / "images/button_3.png")
        self.clear_button = Button(image=self.clear_button_image, borderwidth=0, highlightthickness=0,
                                   command=self.clear, relief="flat")
        self.clear_button.place(x=40.0, y=220.0, width=180.0, height=40.0)

        self.browse_button_image = PhotoImage(file=bundle_dir / "images/button_4.png")
        self.browse_button = Button(image=self.browse_button_image, borderwidth=0, highlightthickness=0,
                                    command=self.browse_file, relief="flat")
        self.browse_button.place(x=539.0, y=160.0, width=120.0, height=40.0)

        self.file_entry_image = PhotoImage(file=bundle_dir / "images/entry_1.png")
        self.file_entry_bg = self.window.create_image(280.0, 180.0, image=self.file_entry_image)
        self.enter_file_path = Entry(bd=0, bg="#DCEEEB", fg="#000716", highlightthickness=0, font=("Inter", 16 * -1))
        self.enter_file_path.place(x=40.0, y=160.0, width=480.0, height=38.0)

        self.select_file_text = self.window.create_text(39.0, 120.0, anchor="nw",
                                                        text="Please select the excel you would like to convert for the"
                                                             " accounting system.",
                                                        fill="#000000",
                                                        font=("Inter", 16 * -1))

        #self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def clear(self):
        self.enter_file_path.delete(0, END)

    def on_closing(self):
        if messagebox.askyesno(title="Quit?", message="Are you sure you want to quit?"):
            self.root.destroy()

    def show_message(self, message):
        messagebox.showinfo(title="Notification", message=message)

    def fill_file_path_box(self, file_path: str):
        """
        After a file has been selected using the browse function
        this function fills the text box with that file path
        """
        self.clear()
        self.enter_file_path.insert(0, file_path)

    def browse_file(self):
        """This fuctioned is called with the browse button when the user is selecting the file"""
        file_path: str = filedialog.askopenfilename()
        print("Selected file:", file_path)
        self.fill_file_path_box(file_path)

    def get_entered_file_path(self):
        excel_to_parse = self.enter_file_path.get()
        excel_to_parse = re.sub(r'\n', '', excel_to_parse)
        print("Text saved:", excel_to_parse)
        return excel_to_parse

    def open_file_explorer(self, file_path):
        # Get the directory of the file
        directory = os.path.dirname(file_path)
        # Open file explorer to the directory
        if platform.system() == 'Windows':
            os.startfile(directory)
        else:
            subprocess.Popen(['xdg-open', directory])

    def excel_parser(self, excel_file):
        # Path for Excel
        xls = pd.ExcelFile(excel_file)
        # convert one tab into a dataframe - setting the column headers to be the 2nd row
        df1 = pd.read_excel(xls, 'Sales Invoice VAT 20%', header=1)
        df2 = pd.read_excel(xls, 'UK purchase invoices', header=1)

        output_path = os.path.splitext(excel_file)[0]
        generate_dataframe_output(df1, 'Sales', output_path, 'Date')
        generate_dataframe_output(df2, 'Purchase', output_path, 'Belegdatum')

        return output_path

    def generate_files(self):
        """This function is called when pressing the generate files button. Want to check the file is not empty by
        retrieving the file name from the text box"""
        excel_to_parse = self.get_entered_file_path()
        try:
            file_path = excel_parser(excel_to_parse)
            print(file_path)
            self.show_message("Your files have been generated successfully.")
            if self.check_state.get() == 1:
                self.open_file_explorer(file_path)
        except FileNotFoundError:
            self.show_message("You have not selected a file.")
        except Exception as e:
            # Handle all other types of exceptions
            self.show_message("An error occurred:", e)


csv_parser = CsvParserGui()
