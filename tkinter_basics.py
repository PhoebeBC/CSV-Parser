import tkinter as tk

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