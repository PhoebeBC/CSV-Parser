import tkinter as tk
from tkinter import messagebox, filedialog
from excel_parser import excel_parser
import os
import subprocess
import platform
import customtkinter as ct
import re


class CsvParserGui():

    def __init__(self):
        self.appearance = ct.set_appearance_mode("System")
        self.color_theme = ct.set_default_color_theme("green")

        self.root = ct.CTk()

        self.root.geometry("720x480")
        self.root.title("Vat Return Accounts Handler")

        self.title = ct.CTkLabel(self.root, text="Vat Return to Accounts Formatter", font=('Arial', 18))
        self.title.pack(padx=20, pady=20)

        self.select_file_label = ct.CTkLabel(self.root, text="Please enter the file path for your chosen file below "
                                                             "or \nclick 'Browse..' to select in your file explorer.",
                                             font=('Arial', 14))
        self.select_file_label.pack(padx=5, pady=20)

        self.enter_file_path = ct.CTkEntry(self.root, placeholder_text="Enter file pather here")
        self.enter_file_path.pack(padx=20, pady=20)

        self.browse_button = ct.CTkButton(self.root, text="Browse...", command=self.browse_file)
        self.browse_button.pack(pady=10, padx=20)

        self.clear_button = ct.CTkButton(self.root, text="Clear File Selection", font=('Arial', 14), command=self.clear)
        self.clear_button.pack(padx=10, pady=10)

        self.check_file_label = ct.CTkLabel(self.root,
                                            text="Please check the file you have entered above is correct.\nOnce sure "
                                                 "please click 'Generate Files'.", font=('Arial', 14))
        self.check_file_label.pack(padx=5, pady=20)

        self.generate_button = ct.CTkButton(self.root, text="Generate Accounts Files", command=self.generate_files)
        self.generate_button.pack(pady=10, padx=20)

        self.check_state = tk.IntVar(self.root, value=1)
        self.show_in_folder_check = ct.CTkCheckBox(self.root, text="Show files in file explorer when generated.",
                                                   font=('Arial', 14), variable=self.check_state, )
        self.show_in_folder_check.pack(padx=10, pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def show_path(self, file_path):
        if file_path == '':
            messagebox.showinfo(title="File Check", message=f"You have not selected a file.")
        else:
            messagebox.showinfo(title="File Check", message=f"You have selected the file{file_path}")

    def show_message(self, message):
        messagebox.showinfo(title="Notification", message=message)

    def on_closing(self):
        if messagebox.askyesno(title="Quit?", message="do you really want to quit?"):
            self.root.destroy()

    def clear(self):
        self.enter_file_path.delete('1.0', tk.END)

    def fill_file_path_box(self, file_path: str):
        '''After a file has been selected using the browse function
        this function fills the text box with that file path'''
        self.clear()
        self.enter_file_path.insert(index=tk.END, text=file_path)
        # self.enter_file_path.see(tk.END)

    def browse_file(self):
        '''This fuctioned is called with the browse button when the user is selecting the file'''
        file_path: str = filedialog.askopenfilename()
        print("Selected file:", file_path)
        self.fill_file_path_box(file_path)

    def get_entered_file_path(self):
        excel_to_parse = self.enter_file_path.get("1.0", tk.END)
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
        '''This funtion is called when pressing the generate files button. Want to check the file is not empty by
        retrieving the file name from the text box'''
        excel_to_parse = self.get_entered_file_path()
        try:
            file_path = excel_parser(excel_to_parse)
            self.show_message("Your files have been generated successfully.")
            if self.check_state.get() == 1:
                self.open_file_explorer(file_path)
        except FileNotFoundError:
            self.show_message("You have not selected a file.")
        except Exception as e:
            # Handle all other types of exceptions
            print("An error occurred:", e)


csv_parser = CsvParserGui()
