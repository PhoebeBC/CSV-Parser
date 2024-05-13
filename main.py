import tkinter as ct
from excel_parser import excel_parser
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

    def generate_files(self):
        """This function is called when pressing the generate files button. Want to check the file is not empty by
        retrieving the file name from the text box"""
        excel_to_parse = self.get_entered_file_path()
        try:
            file_path = excel_parser(excel_to_parse)
            if file_path == "Error tab name":
                self.show_message("Tabs in Excel are not correctly named, please check that the first tab is the"
                                  "'Sales Invoice VAT 20%' and the second tab is 'UK purchase invoices'.")
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
