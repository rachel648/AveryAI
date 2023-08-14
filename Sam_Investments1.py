import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
import psycopg2
from AveryAI import forms
from postgresDatabase import MyDatabase

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
sectionwidth = 320


class MyGui:

    def __init__(self):
        # Default properties

        self.root = ctk.CTk()
        self.root.geometry("640x480")
        self.root.title("Sam Investments LTD")
        self.screen_height = self.root.winfo_screenheight()

        # functions
        def authenticate(username, password):
            k = True
            try:
                conn_obj = psycopg2.connect(user=username, password=password, host="localhost", database="SamInvestments")
            except (Exception, psycopg2.DatabaseError) as err:
                k = False
            finally:
                if k:
                    conn_obj.close()
                return k

        def change_to_main():
            self.user = self.username_text.get()
            self.password = self.password_text.get()

            if authenticate(self.user, self.password):
                self.errormessage.configure(text="Connected Successfully", text_color="Green")
                self.mainframe.pack(fill="both", expand=True)
                self.loginframe.forget()
            else:
                self.errormessage.configure(text="Invalid Credentials", text_color="red")

        def return_to_login():
            self.loginframe.pack(fill="both", expand=True)
            self.mainframe.forget()
            self.tenants.forget()

        def tenant_management(event):
            self.tenants.pack(fill="both", expand=True)
            self.tenant_table.update()
            self.tenant_table.update_idletasks()
            self.mainframe.forget()

        def add_new_tenant():
            new_tenant = forms.InputDialog()
            data2 = (new_tenant.firstname, new_tenant.lastname, new_tenant.houseno)
            self.tenant_table.insert(parent='', index=0, values=data2)





        # Widgets#########################
        # framessss
        self.loginframe = ctk.CTkFrame(master=self.root)
        self.loginframe.pack(fill="both", expand=True)

        self.mainframe = ctk.CTkFrame(master=self.root)
        self.tenants = ctk.CTkFrame(master=self.root)
        # Actual widgets
        self.main_label = ctk.CTkLabel(self.loginframe, text="SAM INVESTMENTS RENTAL MANAGEMENT",
                                       font=('Lithos Pro Regular', 30), text_color='green')
        self.main_label.pack(padx=10, pady=60)

        self.title = ctk.CTkLabel(master=self.loginframe, text="LOGIN", font=('Roboto', 35))
        self.title.pack(padx=10, pady=100)

        self.email_text = ctk.CTkEntry(master=self.loginframe, height=30, placeholder_text="Enter your email",
                                       font=('Arial', 12), width=300)
        self.email_text.pack(padx=10, pady=15)

        self.username_text = ctk.CTkEntry(master=self.loginframe, height=30, placeholder_text="Enter username",
                                          font=('Arial', 12), width=300)
        self.username_text.pack(padx=10, pady=15)

        self.password_text = ctk.CTkEntry(master=self.loginframe, height=30, placeholder_text="Enter password",
                                          font=('Arial', 12), width=300, show="*")
        self.password_text.pack(padx=10, pady=15)

        self.errormessage = ctk.CTkLabel(self.loginframe, text=" ", text_color="red")
        self.errormessage.pack()

        self.loginbutton = ctk.CTkButton(master=self.loginframe, text="LOGIN", font=('Arial', 16),
                                         command=change_to_main)
        self.loginbutton.pack(padx=5, pady=10)

        # MainFrame
        self.sideframe = ctk.CTkFrame(self.mainframe, fg_color="#0c041a", height=self.screen_height, width=300)
        self.sideframe.grid_propagate(False)
        self.sideframe.pack_propagate(False)
        self.sideframe.grid(row=0, column=0, rowspan=3, padx=(0, 20), pady=10)

        self.expense_tracking_frame = ctk.CTkFrame(self.mainframe, fg_color="#0e1b52", height=300, width=sectionwidth)
        self.expense_tracking_frame.pack_propagate(False)
        self.expense_tracking_frame.grid(row=0, column=1, padx=10, pady=10)

        self.expense_tracking_label = ctk.CTkLabel(self.expense_tracking_frame, text="Expense tracking",
                                                   font=('Arial', 16))
        self.expense_tracking_label.pack(padx=10, pady=10)

        self.tenant_management_frame = ctk.CTkFrame(self.mainframe, fg_color="#0e1b52", height=300, width=sectionwidth)
        self.tenant_management_frame.pack_propagate(False)
        self.tenant_management_frame.bind("<Button-1>", tenant_management)
        self.tenant_management_frame.grid(row=1, column=1, padx=10, pady=10)

        self.tenant_management_label = ctk.CTkLabel(self.tenant_management_frame, text="Tenant Management",
                                                    font=('Arial', 16))
        self.tenant_management_label.pack(padx=10, pady=10)

        self.monitoring_frame = ctk.CTkFrame(self.mainframe, fg_color="#0e1b52", height=300, width=sectionwidth)
        self.monitoring_frame.pack_propagate(False)
        self.monitoring_frame.grid(row=0, column=2, padx=10, pady=10)

        self.monitoring_label = ctk.CTkLabel(self.monitoring_frame, text="Electricity and water monitoring",
                                             font=('Arial', 16))
        self.monitoring_label.pack(padx=5, pady=10)

        self.CCTV_frame = ctk.CTkFrame(self.mainframe, fg_color="#0e1b52", height=300, width=sectionwidth)
        self.CCTV_frame.pack_propagate(False)
        self.CCTV_frame.grid(row=1, column=2, padx=10, pady=10)

        self.CCTV_label = ctk.CTkLabel(self.CCTV_frame, text="CCTV interface", font=('Arial', 16))
        self.CCTV_label.pack(padx=10, pady=10)

        self.SMS_automation_frame = ctk.CTkFrame(self.mainframe, fg_color="#0e1b52", height=300, width=sectionwidth)
        self.SMS_automation_frame.pack_propagate(False)
        self.SMS_automation_frame.grid(row=0, column=3, padx=10, pady=10)

        self.SMS_automation_label = ctk.CTkLabel(self.SMS_automation_frame, text="SMS Automation", font=('Arial', 16))
        self.SMS_automation_label.pack(padx=5, pady=10)

        self.token_monitoring_frame = ctk.CTkFrame(self.mainframe, fg_color="#0e1b52", height=300, width=sectionwidth)
        self.token_monitoring_frame.pack_propagate(False)
        self.token_monitoring_frame.grid(row=1, column=3, padx=10, pady=5)

        self.token_monitoring_label = ctk.CTkLabel(self.token_monitoring_frame, text="Token Monitoring",
                                                   font=('Arial', 16))
        self.token_monitoring_label.pack(padx=10, pady=10)

        self.tenants_label = ctk.CTkLabel(self.tenants, text="", text_color="yellow")
        self.tenants_label.pack()
        self.entry1 = ctk.CTkEntry(self.tenants, placeholder_text="Wassuh", height=40, width=150)

        self.tenant_table = ttk.Treeview(self.tenants, columns=('tenant_id', 'First_name', 'Last_name', 'House_no'), show='headings')
        self.tenant_table.heading('tenant_id', text='Tenant_Id')
        self.tenant_table.heading('First_name', text='First_Name')
        self.tenant_table.heading('Last_name', text='Last_Name')
        self.tenant_table.heading('House_no', text='House_No')
        self.tenant_table.pack()

        self.datalist = ctk.CTkLabel(self.tenants, text="", text_color="blue")
        self.datalist.pack()

        self.returnbutton = ctk.CTkButton(master=self.sideframe, text="Return", font=('Arial', 16), command=return_to_login)
        self.returnbutton.pack(side=tk.TOP, padx=10, pady=10)


        self.returnbutton2 = ctk.CTkButton(master=self.tenants, text="Return", font=('Arial', 20), command=return_to_login)
        self.returnbutton2.pack(pady=20, side=tk.BOTTOM)

        self.create_button = ctk.CTkButton(master=self.tenants, text="Add new tenant", font=('Roboto', 14), command=add_new_tenant)
        self.create_button.pack(pady=20, side=tk.BOTTOM)

        # Tenants table put it here ndo isishinde imejicall having a redundant treeview
        conn_obj = psycopg2.connect(user=MyDatabase.username, password=MyDatabase.pwd, host=MyDatabase.hostname, database='tenants')
        cur_object = conn_obj.cursor()
        cur_object.execute('SELECT tenant_id FROM tenantinfo')
        tenant_ids = cur_object.fetchall()
        cur_object.execute('SELECT first_name FROM tenantinfo')
        first_names = cur_object.fetchall()
        cur_object.execute('SELECT last_name FROM tenantinfo')
        last_names = cur_object.fetchall()
        cur_object.execute('SELECT house_no FROM tenantinfo')
        house_nos = cur_object.fetchall()
        counter = 0
        fnames = []
        lnames = []
        hnos = []

        for hno in house_nos:
            hnos.append(hno)

        for lname in last_names:
            lnames.append(lname)

        for fname in first_names:
            fnames.append(fname)

        for tid in tenant_ids:
            tenant_id = tid
            first_name = fnames[counter]
            last_name = lnames[counter]
            house_no = hnos[counter]
            data = (tenant_id, first_name, last_name, house_no)
            self.tenant_table.insert(parent='', index=0, values=data)
            counter = counter + 1



        self.root.mainloop()


gui1 = MyGui()