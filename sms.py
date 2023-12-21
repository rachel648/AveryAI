from Sam_Investments1 import *
from twilio.rest import Client
from postgresDatabase import MyDatabase

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

account_sid = 'AC72ed2a3576f72dea6a9768320c4bfb02'
auth_token = '0118b72cd1c56be583ecc944a26a8c8e'
client = Client(account_sid, auth_token)

class sms_input_dialogue:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.geometry("640x480")
        self.root.title("SMS Actions")
        self.root.resizable(False, False)
        self.mainframe = ctk.CTkFrame(self.root)
        self.mainframe.pack(fill="both", expand=True)

        #functions
        def send_sms():
            self.message = self.sms_content.get()
            message = client.messages.create(
                from_='whatsapp:+14155238886',
                body=self.message,
                to='whatsapp:+254115856604'
            )
            try:
                conn_obj = psycopg2.connect(user=MyDatabase.username, password=MyDatabase.pwd, host=MyDatabase.hostname,
                                            database="SamInvestments")
                cur_obj = conn_obj.cursor()
                cur_obj.execute(f"INSERT INTO messages(message_title, message_content) VALUES('{self.sms_title.get()}','{self.sms_content.get()}')")
                conn_obj.commit()
                conn_obj.close()
                #Here2
            except (Exception, psycopg2.DatabaseError) as err:
                print(err)
            self.root.destroy()
            self.root.quit()

        self.sms_actions_label = ctk.CTkLabel(self.mainframe, text="SMS", font=('Roboto', 30), text_color="green")
        self.sms_actions_label.pack(padx=10, pady=(10,30))

        self.sms_title = ctk.CTkEntry(self.mainframe, height=30, width=500, placeholder_text="Enter title of SMS")
        self.sms_title.pack(padx=10, pady=10)

        self.sms_content = ctk.CTkEntry(self.mainframe,height=100, width=500, placeholder_text="Enter content of SMS")
        self.sms_content.pack(padx=0, pady=0)

        self.sms_button = ctk.CTkButton(self.mainframe, height=30, width=100, text="Send SMS", command=send_sms)
        self.sms_button.pack(padx=10, pady=10)

        self.root.mainloop()





