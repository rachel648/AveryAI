from Sam_Investments1 import *
from postgresDatabase import MyDatabase

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class Payment_Input_Dialogue:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.geometry("640x480")
        self.root.title("Payment Options")
        self.root.resizable(False, False)
        self.mainframe = ctk.CTkFrame(self.root)
        self.mainframe.pack(fill="both", expand=True)

        #functions
        def pay_button_clicked():
            print(self.pay_reason_entry.get())
            print(self.pay_amount_entry.get())
            try:
                conn_obj = psycopg2.connect(user=MyDatabase.username, password=MyDatabase.pwd, host=MyDatabase.hostname,
                                            database="SamInvestments")
                cur_obj = conn_obj.cursor()
                cur_obj.execute(f"INSERT INTO payments(pay_reason, pay_amount) VALUES('{self.pay_reason_entry.get()}',{self.pay_amount_entry.get()})")
                conn_obj.commit()
                conn_obj.close()
            except (Exception, psycopg2.DatabaseError) as err:
                print(err)

            self.root.quit()
            self.root.destroy()
        def pay_option_selected(event):
            print("Worked")

        self.pay_label = ctk.CTkLabel(self.mainframe, text="Payment", font=('Roboto',20))
        self.pay_label.pack(padx=10, pady=10)

        self.pay_reason_entry = ctk.CTkEntry(self.mainframe, placeholder_text="Enter reason for payment", height=30, width=300)
        self.pay_reason_entry.pack(padx=10, pady=10)

        self.pay_amount_entry = ctk.CTkEntry(self.mainframe, placeholder_text="Enter Amount", height=30,width=300)
        self.pay_amount_entry.pack(padx=10, pady=10)

        self.select_pay_option = ctk.CTkComboBox(self.mainframe, values=['Send Money', 'Buy Goods and services','Paybill', 'Pochi la Biashara'])
        self.select_pay_option.pack(padx=10, pady=10)
        self.select_pay_option.bind("<<ComboboxSelected>>", pay_option_selected)

        self.pay_number = ctk.CTkEntry(self.mainframe, placeholder_text="Enter payment number", height=30, width=300)
        self.pay_number.pack(padx=10, pady=10)

        self.pay_button = ctk.CTkButton(self.mainframe, text="Pay",command=pay_button_clicked)
        self.pay_button.pack(padx=10, pady=10)

        self.root.mainloop()

