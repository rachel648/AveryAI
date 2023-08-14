
import customtkinter as ctk
import tkinter as tk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class MyGui:
    def __init__(self):
        # Default properties
        self.root = ctk.CTk()
        self.root.geometry("640x480")


        # Widgets
        self.frame = ctk.CTkFrame(master=self.root)
        self.frame.pack(padx=60, pady=20,fill="both", expand=True)

        self.label = ctk.CTkLabel(master=self.frame, text="LOGIN", font=('Roboto', 25))
        self.label.pack(padx=10, pady=100)

        self.username_text = ctk.CTkEntry(master=self.frame, width=250, placeholder_text="Enter Username")
        self.username_text.pack(padx=10, pady=32)

        self.password_text = ctk.CTkEntry(master=self.frame, width=250, placeholder_text="Enter password", show="*")
        self.password_text.pack(padx=10, pady=12)

        self.loginButton = ctk.CTkButton(master=self.frame, text="LOGIN", font=('Arial', 18))
        self.loginButton.pack(pady=20, padx=10)

        self.remember_me = ctk.CTkCheckBox(master=self.frame, text="Remember Me")
        self.remember_me.pack(padx=10, pady=10)

        #FUNTIONS!!!!!!!!!
        def login():
            print("Test")
        self.root.mainloop()

gui1 = MyGui()