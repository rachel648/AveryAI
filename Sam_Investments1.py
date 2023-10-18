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
    j = None
    option = None
    k = False

    def __init__(self):
        # Default properties
        self.k = MyGui.k
        self.j = MyGui.j
        self.new_tenant = None
        self.updated_iid = None
        self.updated_data = None
        self.root = ctk.CTk()
        self.root.geometry("1280x720")
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
            self.tenants.forget()
            self.expenses.forget()
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

        def tenant_management(event):
            self.tenants.pack(fill="both", expand=True)
            self.mainframe.forget()

        def expense_tracking_event(event):
            self.expenses.pack(fill="both", expand=True)
            self.mainframe.forget()
            self.tenant_management_frame.forget()


        def actions():
            self.new_tenant = forms.InputDialog()
            self.data2 = self.new_tenant.getinfo()
            self.updated_iid = self.new_tenant.updatediid()
            self.updated_data = self.new_tenant.getinfo2()
            self.added_iid = self.new_tenant.getiid()
            if self.new_tenant.action == "add":
                self.added_iid = self.added_iid[0]
                self.tenant_table.insert(parent='', index=100, values=self.data2, iid=self.added_iid)
            elif self.new_tenant.action == "update":
                self.updated_iid_real = self.updated_iid[0]
                self.tenant_table.delete(self.updated_iid_real)
                print("Deleted")
                print(self.updated_data)
                self.tenant_table.insert(parent='', index=100, values=self.updated_data, iid=self.updated_iid_real)

        def delete_tenant(event):
            for i in self.tenant_table.selection():
                self.to_be_deleted = str(self.tenant_table.item(i)['values'][1])
                self.tenant_table.delete(i)
                query1 = f"DELETE FROM tenantinfo WHERE first_name= '{self.to_be_deleted}'"
                self.cur_object.execute(query1)
                self.conn_obj.commit()

        def update_tenant1():
            self.tenant_table.delete(f'{self.updated_iid}')
            self.tenant_table.insert(parent='', index=20, values=self.updated_data)

        def getids(event):
            for item in self.tenant_table.selection():
                print(item)
        def change_cursor(my_frame):
            my_frame.configure(cursor="star")
        def fill_tenant_table():
            for item in self.tenant_table.get_children():
                self.tenant_table.delete(item)
            self.conn_obj = psycopg2.connect(user=MyDatabase.username, password=MyDatabase.pwd, host=MyDatabase.hostname, database='tenants')
            self.cur_object = self.conn_obj.cursor()
            self.cur_object.execute('SELECT tenant_id FROM tenantinfo')
            tenant_ids = self.cur_object.fetchall()
            self.cur_object.execute('SELECT first_name FROM tenantinfo')
            first_names = self.cur_object.fetchall()
            self.cur_object.execute('SELECT last_name FROM tenantinfo')
            last_names = self.cur_object.fetchall()
            self.cur_object.execute('SELECT house_no FROM tenantinfo')
            house_nos = self.cur_object.fetchall()
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
                self.tenant_table.insert(parent='', index=counter, values=data , iid=tenant_id)
                counter = counter + 1

        def search_for_tenant(event):
            name = self.search_tenant.get()
            result = None
            conn_obj = psycopg2.connect(user=MyDatabase.username, password=MyDatabase.pwd, host=MyDatabase.hostname, database='tenants')
            cur_obj = conn_obj.cursor()
            cur_obj.execute(f"SELECT * FROM tenantinfo WHERE first_name = '{name}'")
            result = cur_obj.fetchall()
            if not result:
                cur_obj.execute(f"SELECT * FROM tenantinfo WHERE last_name = '{name}'")
                if not result:
                    print("Not found")
                else:
                    pass
            else:

                for name1 in first_names:
                    name2 = name1[0]
                    if name2 == name:
                        cur_obj.execute(f"SELECT tenant_id FROM tenantinfo WHERE first_name = '{name}'")
                        id_late = cur_obj.fetchone()
                for ten_id in tenant_ids:
                    print(ten_id[0])
                    self.tenant_table.focus(ten_id[0])
                    item = self.tenant_table.focus()
                    id_late1 = str(id_late[0])
                    print(id_late1 + ":::::" + item)

                    if item == id_late1:
                        print("I am mr meeseeks look at me")
                    else:
                        self.tenant_table.delete(ten_id)
                self.k = True

        # Widgets#########################
        # framessss
        self.loginframe = ctk.CTkFrame(master=self.root)
        self.loginframe.pack(fill="both", expand=True)

        self.mainframe = ctk.CTkFrame(master=self.root)
        self.tenants = ctk.CTkFrame(master=self.root)
        self.expenses = ctk.CTkFrame(master=self.root)
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
        self.expense_tracking_frame.bind("<Enter>", command=change_cursor(self.expense_tracking_frame))
        self.expense_tracking_frame.bind("<Button-1>", expense_tracking_event)
        self.expense_tracking_frame.bind("<Enter>", command=lambda e: self.expense_tracking_frame.configure(fg_color="green", height=310, width=(sectionwidth+10)))
        self.expense_tracking_frame.bind("<Leave>", command=lambda e: self.expense_tracking_frame.configure(fg_color="#0e1b52", height=300, width=sectionwidth))
        self.expense_tracking_frame.grid(row=0, column=1, padx=10, pady=10)

        self.expense_tracking_label = ctk.CTkLabel(self.expense_tracking_frame, text="Expense tracking", font=('Arial', 16))
        self.expense_tracking_label.pack(padx=10, pady=10)

        self.tenant_management_frame = ctk.CTkFrame(self.mainframe, fg_color="#0e1b52", height=300, width=sectionwidth)
        self.tenant_management_frame.pack_propagate(False)
        self.tenant_management_frame.bind("<Enter>", command=change_cursor(self.tenant_management_frame))
        self.tenant_management_frame.bind("<Button-1>", tenant_management)
        self.tenant_management_frame.bind("<Enter>", command= lambda e: self.tenant_management_frame.configure(fg_color="green", height=310, width=(sectionwidth+10)))
        self.tenant_management_frame.bind("<Leave>", command= lambda e: self.tenant_management_frame.configure(fg_color="#0e1b52", height=300, width=sectionwidth))
        self.tenant_management_frame.grid(row=1, column=1, padx=10, pady=10)

        self.tenant_management_label = ctk.CTkLabel(self.tenant_management_frame, text="Tenant Management",
                                                    font=('Arial', 16))
        self.tenant_management_label.pack(padx=10, pady=10)

        self.monitoring_frame = ctk.CTkFrame(self.mainframe, fg_color="#0e1b52", height=300, width=sectionwidth)
        self.monitoring_frame.pack_propagate(False)
        self.monitoring_frame.bind("<Enter>", command=change_cursor(self.monitoring_frame))
        self.monitoring_frame.bind("<Enter>", command=lambda e: self.monitoring_frame.configure(fg_color="green", height=310, width=(sectionwidth+10)))
        self.monitoring_frame.bind("<Leave>", command=lambda e: self.monitoring_frame.configure(fg_color="#0e1b52", height=300, width=sectionwidth))
        self.monitoring_frame.grid(row=0, column=2, padx=10, pady=10)

        self.monitoring_label = ctk.CTkLabel(self.monitoring_frame, text="Electricity and water monitoring",
                                             font=('Arial', 16))
        self.monitoring_label.pack(padx=5, pady=10)

        self.CCTV_frame = ctk.CTkFrame(self.mainframe, fg_color="#0e1b52", height=300, width=sectionwidth)
        self.CCTV_frame.pack_propagate(False)
        self.CCTV_frame.bind("<Enter", change_cursor(self.CCTV_frame))
        self.CCTV_frame.bind("<Enter>", command=lambda e: self.CCTV_frame.configure(fg_color="green", height=310, width=(sectionwidth+10)))
        self.CCTV_frame.bind("<Leave>", command=lambda e: self.CCTV_frame.configure(fg_color="#0e1b52",  height=300, width=sectionwidth))
        self.CCTV_frame.grid(row=1, column=2, padx=10, pady=10)

        self.CCTV_label = ctk.CTkLabel(self.CCTV_frame, text="CCTV interface", font=('Arial', 16))
        self.CCTV_label.pack(padx=10, pady=10)

        self.SMS_automation_frame = ctk.CTkFrame(self.mainframe, fg_color="#0e1b52", height=300, width=sectionwidth)
        self.SMS_automation_frame.pack_propagate(False)
        self.SMS_automation_frame.bind("<Enter>", command=change_cursor(self.SMS_automation_frame))
        self.SMS_automation_frame.bind("<Enter>", command=lambda e: self.SMS_automation_frame.configure(fg_color="green", height=310, width=(sectionwidth+10)))
        self.SMS_automation_frame.bind("<Leave>", command=lambda e: self.SMS_automation_frame.configure(fg_color="#0e1b52", height=300, width=sectionwidth))
        self.SMS_automation_frame.grid(row=0, column=3, padx=10, pady=10)

        self.SMS_automation_label = ctk.CTkLabel(self.SMS_automation_frame, text="SMS Automation", font=('Arial', 16))
        self.SMS_automation_label.pack(padx=5, pady=10)

        self.token_monitoring_frame = ctk.CTkFrame(self.mainframe, fg_color="#0e1b52", height=300, width=sectionwidth)
        self.token_monitoring_frame.pack_propagate(False)
        self.token_monitoring_frame.bind("<Enter>", command=change_cursor(self.token_monitoring_frame))
        self.token_monitoring_frame.bind("<Enter>", command=lambda e: self.token_monitoring_frame.configure(fg_color="green", height=310, width=(sectionwidth+10)))
        self.token_monitoring_frame.bind("<Leave>", command=lambda e: self.token_monitoring_frame.configure(fg_color="#0e1b52", height=300, width=sectionwidth))
        self.token_monitoring_frame.grid(row=1, column=3, padx=10, pady=5)

        self.token_monitoring_label = ctk.CTkLabel(self.token_monitoring_frame, text="Token Monitoring", font=('Arial', 16))
        self.token_monitoring_label.pack(padx=10, pady=10)

        self.loginreturnbutton = ctk.CTkButton(master=self.sideframe, text="Return", font=('Arial', 16), command=return_to_login)
        self.loginreturnbutton.pack(side=tk.TOP, padx=10, pady=5)

        # Tenants Frame!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.tenants_label = ctk.CTkLabel(self.tenants, text="TENANT MANAGEMENT",font=('Times', 30), text_color="green")
        self.tenants_label.pack(pady=5)
        self.search_tenant = ctk.CTkEntry(self.tenants, placeholder_text="Search", height=10, width=250, justify=tk.CENTER)
        self.search_tenant.pack(padx=10, pady=(20, 10))
        self.search_tenant.bind("<Return>", search_for_tenant)
        self.search_tenantbutton = ctk.CTkButton(self.tenants, text="Clear", width=100, command=fill_tenant_table)
        self.search_tenantbutton.pack(padx=10, pady=10)

        self.tenant_table = ttk.Treeview(self.tenants, columns=('tenant_id', 'First_name', 'Last_name', 'House_no'), show='headings', height=20)
        self.tenant_table.heading('tenant_id', text='Tenant_Id')
        self.tenant_table.heading('First_name', text='First_Name')
        self.tenant_table.heading('Last_name', text='Last_Name')
        self.tenant_table.heading('House_no', text='House_No')
        self.tenant_table.bind("<Delete>", delete_tenant)
        self.tenant_table.bind("<<TreeviewSelect>>", getids)
        self.tenant_table.pack(pady=10)

        self.datalist = ctk.CTkLabel(self.tenants, text="", text_color="blue")
        self.datalist.pack()

        self.mainreturnbutton = ctk.CTkButton(master=self.tenants, text="Return", font=('Arial', 14), command=change_to_main)
        self.mainreturnbutton.pack(pady=5, side=tk.BOTTOM)

        self.create_button = ctk.CTkButton(master=self.tenants, text="Actions", font=('Roboto', 14), command=actions, height=30)
        self.create_button.bind("<Button-1>", actions)
        self.create_button.pack(pady=5, side=tk.BOTTOM)

        # Expense Tracking frame
        self.mpesa_balance = 300
        self.bank_balance = 26000


        self.bank_account_frame = ctk.CTkFrame(self.expenses, height=200, width=500, fg_color="#0B0B45", corner_radius=10)
        self.bank_account_frame.grid_propagate(False)
        self.bank_account_frame.pack_propagate(False)
        self.bank_account_frame.grid(row=1, column=1, columnspan=40, padx=20, pady=40)

        self.bank_account_label = ctk.CTkLabel(self.bank_account_frame, height=10, text="Bank Account Balance", font=('Roboto', 20), text_color="#00FF0F")
        self.bank_balance_label = ctk.CTkLabel(self.bank_account_frame, text=f"Kshs.{self.bank_balance}", font=('Roboto', 15))
        self.bank_balance_label.pack(padx=10, pady=10, side=tk.BOTTOM)
        self.bank_account_label.grid(row=1, column=1, columnspan=30, padx=10, pady=10)

        self.mpesa_account_frame = ctk.CTkFrame(self.expenses, height=200, width=500, fg_color="#0B0B45", corner_radius=10)
        self.mpesa_account_frame.grid_propagate(False)
        self.mpesa_account_frame.pack_propagate(False)
        self.mpesa_account_frame.grid(row=1, column=41, columnspan=40, padx=20, pady=40)

        self.mpesa_account_label = ctk.CTkLabel(self.mpesa_account_frame, height=10, text="Mpesa Account Balance", font=('Roboto', 20), text_color="#00FF0F")
        self.mpesa_balance_label = ctk.CTkLabel(self.mpesa_account_frame, text=f"Kshs.{self.mpesa_balance}", font=("Roboto", 15))
        self.mpesa_balance_label.pack(padx=10, pady=10, side=tk.BOTTOM)
        # self.mpesa_balance_label.grid(row=100, column=20, columnspan=20, padx=10, pady=30)
        # self.mpesa_account_label.pack(padx=10, pady=10)
        self.mpesa_account_label.grid(row=1, column=1, columnspan=30, padx=10, pady=10)

        self.data_analysis_label = ctk.CTkLabel(self.expenses, text="Data Analysis", font=('Arial', 25), text_color="white")
        self.data_analysis_label.grid(row=2, column=0, padx=10, pady=10, columnspan=15)

        self.target_track = ctk.CTkFrame(self.expenses, height= 300, width= 350)
        self.target_track.grid(row=3, rowspan = 10 ,column = 1, columnspan = 10, padx=20, pady = 10)

        self.data_track = ctk.CTkFrame(self.expenses, height=250, width = 250, corner_radius=20 )
        self.data_track.grid(row=4, rowspan=10, column=1, columnspan=10, padx=20, pady=10 )

        self.expensereturn_button = ctk.CTkButton(self.expenses, text="Return", font=('Roboto', 14), command=change_to_main, height=30 )
        self.expensereturn_button.grid(row=100, column=2, columnspan=4, padx=10, pady=10)








#Add something
        # Tenants table put it here ndo isishinde imejicall having a redundant treeview
<<<<<<< Updated upstream
        for item in self.tenant_table.get_children():
            self.tenant_table.delete(item)
        self.conn_obj = psycopg2.connect(user=MyDatabase.username, password=MyDatabase.pwd, host=MyDatabase.hostname,
                                         database='tenants')
=======
        self.conn_obj = psycopg2.connect(user=MyDatabase.username, password=MyDatabase.pwd, host=MyDatabase.hostname, database='SamInvestments')
>>>>>>> Stashed changes
        self.cur_object = self.conn_obj.cursor()
        self.cur_object.execute('SELECT tenant_id FROM tenantinfo')
        tenant_ids = self.cur_object.fetchall()
        self.cur_object.execute('SELECT first_name FROM tenantinfo')
        first_names = self.cur_object.fetchall()
        self.cur_object.execute('SELECT last_name FROM tenantinfo')
        last_names = self.cur_object.fetchall()
        self.cur_object.execute('SELECT house_no FROM tenantinfo')
        house_nos = self.cur_object.fetchall()
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
            self.tenant_table.insert(parent='', index=counter, values=data, iid=tenant_id)
            counter = counter + 1
        if self.j:
            update_tenant1()

        self.root.mainloop()

if __name__ == "__main__":
    gui1 = MyGui()
    