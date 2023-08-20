import customtkinter as ctk
import tkinter as tk
from tkinter import ttk

class trial:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Trying sth")
        self.root.geometry("640x720")

        def getid():
            for item in self.treeview1.selection():
                print(item)

        idis = []
        self.treeview1 = ttk.Treeview(self.root, columns=('sth', 'else', 'entirely'), show='headings')
        self.treeview1.heading('sth', text= 'Sth')
        self.treeview1.heading('else', text='Else')
        self.treeview1.heading('entirely', text='Entirely')
        self.treeview1.pack()
        self.treeview1.insert(parent='', index=0,  values=('hello', 'there', 'stanger'))
        self.somebutton = ctk.CTkButton(self.root, text='button', command=getid)
        self.somebutton.pack()




        self.root.mainloop()


trial1 = trial()