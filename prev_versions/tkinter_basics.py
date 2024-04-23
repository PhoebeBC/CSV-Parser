import tkinter as tk
from tkinter import messagebox, filedialog

# creating a window
root = tk.Tk()
# setting size
root.geometry("800x500")
# setting title
root.title("CVS Parser")

# adding label
label = tk.Label(root, text="Hello world", font=('Arial', 18))
label.pack(padx=20, pady=20)

textbox = tk.Text(root, height=3, font=('Arial', 16))
textbox.pack(padx=10)

# adding a button
button = tk.Button(root, text="click me", font=('Arial', 18))
button.pack(padx=10, pady=10)

buttonframe = tk.Frame(root)
buttonframe.columnconfigure(0, weight=1)
buttonframe.columnconfigure(1, weight=1)
buttonframe.columnconfigure(2, weight=1)

# making a grid fram
btn1 = tk.Button(buttonframe, text="1", font=('Ariel', 18))
btn1.grid(row=0, column=0, sticky=tk.W+tk.E)
# makes it strethed across whole row, this is what stickey does
btn2 = tk.Button(buttonframe, text="2", font=('Ariel', 18))
btn2.grid(row=0, column=1, sticky=tk.W+tk.E)
btn3 = tk.Button(buttonframe, text="3", font=('Ariel', 18))
btn3.grid(row=0, column=2, sticky=tk.W+tk.E)

# making sure stretched across row
buttonframe.pack(fill='x')

# similar to text box but only one line
# myentry = tk.Entry(root)
# myentry.pack()

root.mainloop()


################################Class

class CsvParserGui:

    def __init__(self):
        self.root = tk.Tk()

        self.menubar = tk.Menu(self.root)

        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Close", command=self.on_closing)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Close Without Question", command=exit)

        self.actionmenu = tk.Menu(self.menubar, tearoff=0)
        self.actionmenu.add_command(label="Show Message", command=self.show_message)

        self.menubar.add_cascade(menu=self.filemenu, label="File")
        self.menubar.add_cascade(menu=self.actionmenu, label="Action")

        self.root.config(menu=self.menubar)

        self.root.geometry("800x500")
        self.root.title("Vat Return Accounts Handler")

        self.label = tk.Label(self.root, text="Vat Return to Accounts Formatter", font=('Arial', 18))
        self.label.pack(padx=20, pady=20)

        self.textbox = tk.Text(self.root, height=3, font=('Arial', 16))
        self.textbox.bind("<KeyPress>", self.shortcut)
        self.textbox.pack(padx=10)

        self.check_state = tk.IntVar()

        self.check = tk.Checkbutton(self.root, text="Show Messagebox", font=('Arial', 16), variable=self.check_state)
        self.check.pack(padx=10, pady=10)

        self.button = tk.Button(self.root, text="Show message", font=('Arial', 18), command=self.show_message)
        self.button.pack(padx=10, pady=10)

        self.clearbtn = tk.Button(self.root, text="Clear", font=('Arial', 18), command=self.clear)
        self.clearbtn.pack(padx=10, pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def show_message(self):
        if self.check_state.get() == 0:
            print(self.textbox.get('1.0', tk.END))
        else:
            messagebox.showinfo(title="Message", message=self.textbox.get('1.0', tk.END))

    def show_message(self):
        if self.check_state.get() == 0:
            print(self.textbox.get('1.0', tk.END))
        else:
            messagebox.showinfo(title="Message", message=self.textbox.get('1.0', tk.END))


    def shortcut(self, event):
        if event.state == 4 and event.keysym == "Return":
            self.show_message()
        # print(f"keysym = {event.keysym}")
        # print(f"event = {event.state}")

    def on_closing(self):
        if messagebox.askyesno(title="Quite?", message="do you really want to quit?"):
            self.root.destroy()

    def clear(self):
        self.textbox.delete('1.0', tk.END)


csv_parser = CsvParserGui()

