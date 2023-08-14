import tkinter as tk
import customtkinter as ctk
import psycopg2
from postgresDatabase import MyDatabase


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class InputDialog:
    def __init__(self):
        self.data1 = None
        self.houseno = None
        self.lastname = None
        self.firstname = None
        self.root = ctk.CTk()
        self.root.geometry("440x480")
        self.root.title("Add new Tenant")
        self.root.resizable(False, False)

        def destruct():
            self.firstname = self.first_name_entry.get()
            self.lastname = self.last_name_entry.get()
            self.houseno = self.house_no_entry.get()
            self.data1 = (self.firstname, self.lastname, self.houseno)
            try:
                conn_obj = psycopg2.connect(user=MyDatabase.username, password=MyDatabase.pwd, host=MyDatabase.hostname,
                                            database="tenants")
                cur_obj = conn_obj.cursor()
                cur_obj.execute("INSERT INTO tenantinfo(first_name, last_name, house_no) VALUES(%s,%s,%s)", self.data1)

            except (Exception, psycopg2.DatabaseError) as err:
                self.errmessage.configure(text=err, text_color="red")
            finally:
                conn_obj.commit()
                cur_obj.close()
                conn_obj.close()
            self.root.destroy()
    
        # widgets
        label1 = ctk.CTkLabel(self.root, text="Add new tenant", font=('Arial', 30))
        label1.pack(pady=30)

        self.first_name_entry = ctk.CTkEntry(self.root, placeholder_text="Enter first name", height=4, width=300, justify=tk.CENTER, font=("Roboto", 14))
        self.first_name_entry.pack(padx=10, pady=15)

        self.last_name_entry = ctk.CTkEntry(self.root, placeholder_text="Enter last name", height=4, width=300, justify=tk.CENTER, font=("Roboto", 14))
        self.last_name_entry.pack(padx=10, pady=15)

        self.house_no_entry = ctk.CTkEntry(self.root, placeholder_text="Enter house no", height=4, width=300, justify=tk.CENTER, font=("Roboto", 14))
        self.house_no_entry.pack(padx=10, pady=15)

        self.submitButton = ctk.CTkButton(self.root, text="Submit", command=destruct)
        self.submitButton.pack(pady=30)

        self.errmessage = ctk.CTkLabel(self.root, text="l", font=('Arial', 12))
        self.errmessage.pack()

        self.root.mainloop()
        
    def getinfo(self):
        self.firstname = self.first_name_entry.get()
        self.lastname = self.last_name_entry.get()
        self.houseno = self.house_no_entry.get()
        self.data1 = (self.firstname, self.lastname, self.houseno)
        try:
            conn_obj = psycopg2.connect(user=MyDatabase.username, password=MyDatabase.pwd, host=MyDatabase.hostname,
                                        database="tenants")
            cur_obj = conn_obj.cursor()
            insert = [(self.firstname, self.lastname, self.houseno)]
            args = ','.join(cur_obj.mogrify("(%s,%s,%s)", i).decode('utf-8')
                            for i in insert)
            cur_obj.execute("""INSERT INTO tenantinfo(first_name, last_name, house_no)
                                VALUES""" + args)

        except (Exception, psycopg2.DatabaseError) as err:
            self.errmessage.configure(text=err, text_color="red")
        finally:
            conn_obj.commit()
            cur_obj.close()
            conn_obj.close()
            self.root.destroy()
        
    
