import tkinter as tk
from tkinter import messagebox

class MyGui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("640x480")

        self.menuBar = tk.Menu(self.root)

        self.filemenu = tk.Menu(self.menuBar, tearoff=0)
        self.filemenu.add_command(label="close", command=self.on_closing)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="force close", command=exit)

        self.actionBar = tk.Menu(self.menuBar, tearoff=0)
        self.actionBar.add_command(label="Show Message", command=self.show_message)


        self.menuBar.add_cascade(menu=self.actionBar, label="Action")
        self.menuBar.add_cascade(menu=self.filemenu, label="File")


        self.root.config(menu=self.menuBar)

        self.label = tk.Label(self.root, text="Login", font=('Arial', 20))
        self.label.pack(padx=40, pady=80)

        self.loginForm = tk.Frame(self.root)
        self.loginForm.columnconfigure(0, weight=1)
        self.loginForm.columnconfigure(1, weight=1)
        self.loginForm.columnconfigure(2, weight=1)

        username_label = tk.Label(self.loginForm, text="UserName", font=("Arial", 11))
        username_label.grid(row=0, column=0, sticky=tk.W + tk.E, padx=0, pady=10)

        username_text = tk.Entry(self.loginForm, font=("Arial", 11))
        username_text.grid(row=1, column=0, sticky=tk.W + tk.E)

        password_label = tk.Label(self.loginForm, text="Password", font=("Arial", 11))
        password_label.grid(row=2, column=0, sticky=tk.W + tk.E, padx=0, pady=10)

        password_text = tk.Entry(self.loginForm, font=("Arial", 11))
        password_text.grid(row=3, column=0, sticky=tk.W + tk.E)

        loginButton = tk.Button(self.loginForm, text="LOGIN", width=10, font=('Arial', 16))
        loginButton.grid(row=4, column=0, sticky=tk.W + tk.E, padx=0, pady=30)
        self.loginForm.pack()



        self.root.mainloop()

    def show_message(self):
        if self.check_state.get() == 0:
            print(self.textbox1.get('1.0',tk.END))
        else:
            messagebox.showinfo(title="Message", message=self.textbox1.get('1.0',tk.END))

    def on_closing(self):
        if messagebox.askyesno(title="Quit", message="Are you sure you want to quit?"):
            self.root.destroy()

    def clear(self):
        self.textbox1.delete('1.0',tk.END)


gui1 = MyGui()
