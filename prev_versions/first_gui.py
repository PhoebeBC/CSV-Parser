import tkinter as tk
from tkinter import messagebox, filedialog
from excel_parser import excel_parser
import os
import subprocess
import platform
import customtkinter as ct

class CsvParserGui:

    def __init__(self):
        self.root = tk.Tk()

        self.appearance = ct.set_appearance_mode("System")
        self.color_theme = ct.set_default_color_theme("blue")

        self.menubar = tk.Menu(self.root)

        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Close", command=self.on_closing)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Close Without Question", command=exit)

        self.actionmenu = tk.Menu(self.menubar, tearoff=0)
        self.actionmenu.add_command(label="Show Message", command=self.show_path)

        self.menubar.add_cascade(menu=self.filemenu, label="File")
        self.menubar.add_cascade(menu=self.actionmenu, label="Action")

        self.root.config(menu=self.menubar)

        self.root.geometry("800x500")
        self.root.title("Vat Return Accounts Handler")

        self.label = tk.Label(self.root, text="Vat Return to Accounts Formatter", font=('Arial', 18))
        self.label.pack(padx=20, pady=20)

        # self.textbox = tk.Text(self.root, height=3, font=('Arial', 16))
        # self.textbox.bind("<KeyPress>", self.shortcut)
        # self.textbox.pack(padx=10)

        # self.check_state = tk.IntVar()
        #
        # self.check = tk.Checkbutton(self.root, text="Show Messagebox", font=('Arial', 16), variable=self.check_state)
        # self.check.pack(padx=10, pady=10)

        self.browse_button = tk.Button(self.root, text="Browse...", command=self.browse_file)
        self.browse_button.pack(pady=10, padx=20)

        self.generate_button = tk.Button(self.root, text="Generate Accounts Files", command=self.generate_files)
        self.generate_button.pack(pady=10, padx=20)

        # self.button = tk.Button(self.root, text="Show message", font=('Arial', 18))
        # self.button.pack(padx=10, pady=10)

        # self.clearbtn = tk.Button(self.root, text="Clear", font=('Arial', 18), command=self.clear)
        # self.clearbtn.pack(padx=10, pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def show_path(self, file_path):
        if file_path == '':
            messagebox.showinfo(title="File Check", message=f"You have not selected a file.")
        else:
            messagebox.showinfo(title="File Check", message=f"You have selected the file{file_path}")

    def show_message(self, message):
        messagebox.showinfo(title="Notification", message=message)


    def browse_file(self):
        file_path: str = filedialog.askopenfilename()
        print("Selected file:", file_path)
        self.show_path(file_path)
        global excel_to_parse
        excel_to_parse = file_path
        # You can save the file_path variable to use it in your program
        return file_path

    def open_file_explorer(self, file_path):
        # Get the directory of the file
        directory = os.path.dirname(file_path)
        # Open file explorer to the directory
        if platform.system() == 'Windows':
            os.startfile(directory)
        else:
            subprocess.Popen(['xdg-open', directory])

    def generate_files(self):
        file_path = excel_parser(excel_to_parse)
        self.show_message("Your files have been generated successfully.")
        self.open_file_explorer(file_path)


    def on_closing(self):
        if messagebox.askyesno(title="Quit?", message="do you really want to quit?"):
            self.root.destroy()

    # def clear(self):
    #     self.textbox.delete('1.0', tk.END)

csv_parser = CsvParserGui()

