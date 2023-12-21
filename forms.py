import tkinter as tk
import customtkinter as ctk
import psycopg2
from postgresDatabase import MyDatabase
import Sam_Investments1
from Sam_Investments1 import *

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class InputDialog:
    def __init__(self):
        self.my_tenant_id = None
        self.action = None
        self.update_data1 = None
        self.my_id = None
        self.tenant_id = None
        self.update_data = None
        self.update_entry = None
        self.house_numbers = None
        self.data1 = None
        self.houseno = None
        self.lastname = None
        self.firstname = None
        self.realdata1 = None
        self.root = ctk.CTk()
        self.root.geometry("640x480")
        self.root.title("Tenant Actions")
        self.root.resizable(False, False)

        #Frames
        self.mainframe = ctk.CTkFrame(self.root)
        self.mainframe.pack(fill="both", expand=True)

        self.update_tenant = ctk.CTkFrame(self.root)
        self.addtenant_Frame = ctk.CTkFrame(self.root)
        self.check_tenant_state = ctk.CTkFrame(self.root)

        def update_tenant():
            MyGui.option = "update"
            self.update_tenant.pack(fill="both", expand=True)
            self.mainframe.forget()
            self.addtenant_Frame.forget()

        def actual_update(event):
            combo_house_no = self.select_house_combobox.get()
            cur_obj.execute(f"SELECT * FROM tenantinfo WHERE  house_no = '{combo_house_no}'")
            tenant_to_update = cur_obj.fetchall()
            if self.select_type_combobox.get() != 'Select option':
                self.update_entry = ctk.CTkEntry(self.update_tenant, placeholder_text=f"Update {self.select_type_combobox.get()}", height=20, width=200)
                self.update_entry.grid(row=2, column=0, columnspan=1, pady=15)
                self.update_actual_button.grid(row=2, column=1, columnspan=1, pady=15)

        def update_button_clicked():

            self.update_data = (self.select_house_combobox.get(), self.select_type_combobox.get())
            print(self.select_house_combobox.get())
            cur_obj.execute(f"UPDATE tenantinfo SET {self.select_type_combobox.get()} = '{self.update_entry.get()}' WHERE house_no = '{self.select_house_combobox.get()}'")
            conn_obj.commit()
            cur_obj.execute(f"SELECT tenant_id FROM tenantinfo WHERE house_no = '{self.select_house_combobox.get()}'")
            self.my_tenant_id = cur_obj.fetchone()
            cur_obj.execute(f"SELECT first_name FROM tenantinfo WHERE house_no = '{self.select_house_combobox.get()}'")
            self.my_first_name = cur_obj.fetchone()
            cur_obj.execute(f"SELECT last_name FROM tenantinfo WHERE house_no = '{self.select_house_combobox.get()}'")
            self.my_last_name = cur_obj.fetchone()
            cur_obj.execute(f"SELECT house_no FROM tenantinfo WHERE house_no = '{self.select_house_combobox.get()}'")
            self.my_house_number = cur_obj.fetchone()
            self.update_data1 = (self.my_tenant_id, self.my_first_name, self.my_last_name, self.my_house_number)
            self.action = "update"
            self.confirm_message.configure(text=f'{self.select_type_combobox.get()} of house_no: {self.select_house_combobox.get()} has been successfully updated to {self.update_entry.get()}')
            self.update_entry.grid_forget()
            self.update_actual_button.grid_forget()
            self.root.destroy()
            self.root.quit()

        def move_to_main():
            self.mainframe.pack(fill="both", expand=True)
            self.addtenant_Frame.forget()
            self.update_tenant.forget()

        def add_tenant():
            MyGui.option = "add"
            self.addtenant_Frame.pack(fill="both", expand=True)
            self.mainframe.forget()
            self.update_tenant.forget()
            self.check_tenant_state.forget()

        def check_tenant_status():
            self.check_tenant_state.pack(fill="both", expand=True)
            self.mainframe.forget()
            self.addtenant_Frame.forget()
            self.update_tenant.forget()

        def check_tenant_status_clicked():
            house_no = self.select_house_combobox.get()
            conn_obj = psycopg2.connect(user=MyDatabase.username, password=MyDatabase.pwd, host=MyDatabase.hostname,
                                        database="SamInvestments")
            cur_obj = conn_obj.cursor()
            cur_obj.execute(f"SELECT tenant_status FROM tenantstatus WHERE house_number='{house_no}'")
            my_label = cur_obj.fetchone()
            cur_obj.execute(f"SELECT tenant_balance FROM tenantstatus WHERE house_number='{house_no}'")
            balance = cur_obj.fetchone()
            self.check_tenant_state_label.configure(text=f"Tenant state of tenant in house number: {self.select_house_combobox.get()} is {my_label[0]} and balance is {balance[0]} ", font=('Roboto', 15))
            self.check_tenant_state_label.grid(row=3, column=0, padx=10, pady=10)
        def destruct():
            self.action = "add"
            self.firstname = self.first_name_entry.get()
            self.lastname = self.last_name_entry.get()
            self.houseno = self.house_no_entry.get()
            self.data1 = (self.firstname, self.lastname, self.houseno)
            try:

                conn_obj = psycopg2.connect(user=MyDatabase.username, password=MyDatabase.pwd, host=MyDatabase.hostname,
                                            database="SamInvestments")
                cur_obj = conn_obj.cursor()
                cur_obj.execute("INSERT INTO tenantinfo(first_name, last_name, house_no) VALUES(%s,%s,%s)", self.data1)
                conn_obj.commit()
                cur_obj.execute(f"SELECT tenant_id FROM tenantinfo WHERE first_name = '{self.firstname}'")
                self.tenant_id = cur_obj.fetchone()
                cur_obj.execute(f"SELECT first_name FROM tenantinfo WHERE first_name = '{self.firstname}'")
                first_name = cur_obj.fetchone()
                cur_obj.execute(f"SELECT last_name FROM tenantinfo WHERE first_name = '{self.firstname}'")
                last_name = cur_obj.fetchone()
                cur_obj.execute(f"SELECT house_no FROM tenantinfo WHERE first_name = '{self.firstname}'")
                house_no = cur_obj.fetchone()

                self.realdata1 = (self.tenant_id, first_name, last_name, house_no)
            except (Exception, psycopg2.DatabaseError) as err:
                self.errmessage.configure(text=err, text_color="red")
            finally:
                cur_obj.close()
                conn_obj.close()
                self.root.destroy()
                self.root.quit()

        #Update tenant widgets
        conn_obj = psycopg2.connect(user=MyDatabase.username, password=MyDatabase.pwd, host=MyDatabase.hostname, database="SamInvestments")
        cur_obj = conn_obj.cursor()
        cur_obj.execute("SELECT house_no FROM tenantinfo")
        house_numbers = cur_obj.fetchall()
        house_nos = []

        for house_no in house_numbers:
            for item in house_no:
                house_nos.append(item)

        self.update_label = ctk.CTkLabel(self.update_tenant, text="Select house no of tenant you want to update", font=('Times', 30, 'bold'))
        self.update_label.grid(row=0, column=0, columnspan=6, padx=30, pady=(0, 20))

        self.select_house_combobox = ctk.CTkComboBox(self.update_tenant, values=house_nos, command=actual_update, width=200)
        self.select_house_combobox.grid(row=1, column=0, columnspan=1, padx=5, pady=10)
        self.select_house_combobox.bind("<<ComboboxSelected>>", actual_update)

        self.select_type_combobox =ctk.CTkComboBox(self.update_tenant, values=['Select option', 'first_name', 'last_name', 'house_no'], command=actual_update)
        self.select_type_combobox.grid(row=1, column=1, columnspan=1, padx=5, pady=10)
        self.select_type_combobox.bind("<<ComboboxSelected>>", actual_update)

        self.update_actual_button = ctk.CTkButton(self.update_tenant, text="Update", command=update_button_clicked)

        self.confirm_message = ctk.CTkLabel(self.update_tenant, text="", text_color="green", font=('Roboto', 18))
        self.confirm_message.grid(row=9, column=0, columnspan=6, padx=40, pady=30)

        self.update_exit_button = ctk.CTkButton(self.update_tenant, text="Exit", command=move_to_main)
        self.update_exit_button.grid(row=10, column=1, padx=10, pady=40 )



        # widgets main options
        self.mainLabel = ctk.CTkLabel(self.mainframe, text="Click on Action you want to perform :)",
                                      font=('Helvetica', 25, 'bold'))
        self.mainLabel.pack(padx=10, pady=(0, 40))

        self.update_tenant_button = ctk.CTkButton(self.mainframe, text="Update tenant", command=update_tenant)
        self.update_tenant_button.pack(padx=15, pady=15)

        self.add_new_tenant_button = ctk.CTkButton(self.mainframe, text="Add new tenant", command=add_tenant)
        self.add_new_tenant_button.pack(padx=15, pady=15)

        self.check_tenant_state_button = ctk.CTkButton(self.mainframe, text="Check tenant status", command=check_tenant_status)
        self.check_tenant_state_button.pack(padx=15, pady=15)

        # widgets add tenants
        label1 = ctk.CTkLabel(self.addtenant_Frame, text="Add new tenant", font=('Arial', 30))
        label1.pack(pady=30)

        self.first_name_entry = ctk.CTkEntry(self.addtenant_Frame, placeholder_text="Enter first name", height=4, width=300, justify=tk.CENTER, font=("Roboto", 14))
        self.first_name_entry.pack(padx=10, pady=15)

        self.last_name_entry = ctk.CTkEntry(self.addtenant_Frame, placeholder_text="Enter last name", height=4, width=300, justify=tk.CENTER, font=("Roboto", 14))
        self.last_name_entry.pack(padx=10, pady=15)

        self.house_no_entry = ctk.CTkEntry(self.addtenant_Frame, placeholder_text="Enter house no", height=4, width=300, justify=tk.CENTER, font=("Roboto", 14))
        self.house_no_entry.pack(padx=10, pady=15)

        self.submitButton = ctk.CTkButton(self.addtenant_Frame, text="Submit", command=destruct)
        self.submitButton.pack(pady=30)

        self.exit_button = ctk.CTkButton(self.addtenant_Frame, text='Exit', command=move_to_main)
        self.exit_button.pack(padx=10, pady=(0, 10))

        self.errmessage = ctk.CTkLabel(self.addtenant_Frame, text="l", font=('Arial', 12))
        self.errmessage.pack()

        print(MyGui.option)

        #Check tenant status widgets
        conn_obj = psycopg2.connect(user=MyDatabase.username, password=MyDatabase.pwd, host=MyDatabase.hostname,
                                    database="SamInvestments")
        cur_obj = conn_obj.cursor()
        cur_obj.execute("SELECT house_number FROM tenantstatus")
        house_numbers = cur_obj.fetchall()

        house_nos = []

        for house_no in house_numbers:
            for item in house_no:
                house_nos.append(item)

        self.update_label = ctk.CTkLabel(self.check_tenant_state, text="Select tenant you want to check",
                                         font=('Roboto', 30, 'bold'))
        self.update_label.grid(row=0, column=0, columnspan=6, padx=30, pady=(0, 20))

        self.select_house_combobox = ctk.CTkComboBox(self.check_tenant_state, values=house_nos,
                                                     width=200)
        self.select_house_combobox.grid(row=1, column=0, columnspan=1, padx=5, pady=10)
        self.select_house_combobox.bind("<<ComboboxSelected>>")


        self.check_tenant_button = ctk.CTkButton(self.check_tenant_state, text="Check status", command=check_tenant_status_clicked)
        self.check_tenant_button.grid(row=2, column=1, padx=10, pady=10)

        self.check_tenant_state_label = ctk.CTkLabel(self.check_tenant_state, text= "Hello")

        self.confirm_message = ctk.CTkLabel(self.check_tenant_state, text="", text_color="green", font=('Roboto', 18))
        self.confirm_message.grid(row=9, column=0, columnspan=6, padx=40, pady=30)

        self.check_status_exit_button = ctk.CTkButton(self.check_tenant_state, text="Exit", command=move_to_main)
        self.check_status_exit_button.grid(row=10, column=1, padx=10, pady=40)

        self.root.mainloop()
    def getinfo(self):
        return self.realdata1

    def getinfo2(self):
        return self.update_data1

    def getiid(self):
        return self.tenant_id

    def updatediid(self):
        return self.my_tenant_id

    def state1(self):
        return self.k

