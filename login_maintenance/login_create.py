import re
from tkinter import Tk, Label, RIGHT, Entry, Button, messagebox, Checkbutton, IntVar
from common import Values
from common.Hashing import Hash
from common.User import User
#import common.Config as properties
#from common import Values
from mailing.mail import Mail

"""username = 'admin'
password = 'admin123$'
email_id= 'admin484@gmail.com'

def generate_login():
    hashing = Hash()
    salt = hashing.generate_salt()
    hashed_string = hashing.generate_hash(password,salt)
    user = User(username,salt,hashed_string,email_id)
    return user"""

class Create:
    def __init__(self):
        self.create_window = None
        #user email of user who is creating the login
        self._current_logged_in_user_email = None
        #entry fields for taking username, email id and confirm email id
        self.entries_for_creating_login = None
        self.checkbutton = None
        self.col = ('Full Name', 'Email Id', 'Confirm Email Id', 'Make Admin')
        #create a root window before creating this Intvar, otherwise we get an error
        self.check_var = None
        self.dbConnection = None
        self.EMAIL_REGEX = re.compile(Values.PASSWORD_REGEX)

    def user_email_exists(self, email_id):
        sql = "SELECT * FROM login WHERE email_id = '%s'"%(email_id,)
        conn = self.dbConnection.get_connection_object()
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        conn.commit()
        if result is not None:
            return True
        else:
            return False

    """This method sends the username and password to the user who created the login"""
    def _send_email(self,receiver_email,username,password):
        #this sends the mail in background in a thread
        #this avoids the user not to block the interaction with the GUI
        mailing = Mail(receiver_email,username,password)
        mailing.set_create_login_message()
        mailing.start()

    """Check the full name,email and confirm email and then add an account by
    generating a random string with secret key and then insert it into database"""
    def add_login(self):
        full_name = self.entries_for_creating_login[0].get()
        if full_name == '' or full_name is None:
            messagebox.showerror("Error", "Please enter your full name")
        else:
            email_id = self.entries_for_creating_login[1].get()
            confirm_email_id = self.entries_for_creating_login[2].get()
            # print("Check box = %s"%(self.check_var.get()))

            if (email_id == '') or (email_id is None) or (not self.EMAIL_REGEX.match(email_id)):
                messagebox.showerror("Error", "Please enter valid email id")
            elif self.user_email_exists(email_id):
                messagebox.showerror("Error", "User Email Id already exists.")
            else:
                if confirm_email_id == '' or confirm_email_id is None:
                    messagebox.showerror("Error", "Please enter confirm email id")

                if (email_id == confirm_email_id):
                    hashing = Hash()
                    salt = hashing.generate_salt()
                    # create a random password
                    random_pass = hashing.generate_random_password()
                    print(random_pass)
                    password_hash = hashing.generate_hash(random_pass, salt)
                    # create user
                    user = User(full_name, salt, password_hash, email_id, self.check_var.get())
                    #save details into the database
                    self.insert_login_into_database(user)
                    #send the user credentials to the current_logged_in_user email
                    self._send_email(self._current_logged_in_user_email, email_id, random_pass)
                    self.reset_window()
                else:
                    messagebox.showerror("Error", "Email Id and Confirm Email Id Not Matching")

    """ Insert login details into the database"""
    def insert_login_into_database(self, user):
        try:
            self.dbConnection.insert_login_into_db(user)
        except Exception as ex:
            messagebox.showerror("Error","Unable To Add Account\nError : {}"
                                 .format(str(ex),))
        else:
            messagebox.showinfo("Success","Login Created\nPlease Check Your Email Id For Credentials")

    """Resets all the entry fields and the checkbutton"""
    def reset_window(self):
        for entry in self.entries_for_creating_login:
            entry.delete(0,'end')
        self.check_var.set(0)

    """Create login window GUI with entry fields,checkbutton and buttons"""
    def create_login_window(self,current_user_email,dbConnection):
        self.dbConnection = dbConnection
        self._current_logged_in_user_email = current_user_email
        self.create_window = Tk()
        self.create_window.title("Create Login Account")
        self.create_window.wm_iconbitmap(Values.BITMAP_IMAGE)
        self.create_window.geometry("640x350+500+200")
        self.create_window.resizable(0, 0)
        #bind the enter key to the add_login function
        self.create_window.bind("<Return>", self.add_login)

        Label(self.create_window, text='Enter Details Of User',
              padx=80, pady=40, font=('Arial', 16)) \
            .grid(row=0, column=0, rowspan=2, columnspan=2)
        Label(self.create_window, text='-' * 110, padx=35) \
            .grid(row=1, column=0, columnspan=2)


        # take self.entries_for_creating_login as a list of Entry objects whose
        # length equal to the col tuple above that means self.entries_for_creating_login
        # contains 4 Entry objects
        self.entries_for_creating_login = [''] * (len(self.col)-1)

        Label(self.create_window, pady=7, text=self.col[0], font=('Arial', 12), justify=RIGHT) \
            .grid(row=2, column=0)
        self.entries_for_creating_login[0] = Entry(self.create_window, width=50)
        self.entries_for_creating_login[0].grid(row=2, column=1)

        Label(self.create_window, text=self.col[1], font=('Arial', 12), justify=RIGHT) \
            .grid(row=4, column=0)
        self.entries_for_creating_login[1] = Entry(self.create_window, width=50)
        self.entries_for_creating_login[1].grid(row=4, column=1)

        Label(self.create_window, text=self.col[2], font=('Arial', 12), justify=RIGHT) \
            .grid(row=5, column=0)
        self.entries_for_creating_login[2] = Entry(self.create_window, width=50)
        self.entries_for_creating_login[2].grid(row=5, column=1)

        #create check button for making admin account
        self.check_var = IntVar()
        self.checkbutton = Checkbutton(self.create_window,
                                       text=self.col[3],
                                       font=('Arial',12),
                                       variable = self.check_var,
                                       onvalue=1, offvalue=0, height=5)
        self.checkbutton.grid(row=6, column=1)

        Button(self.create_window, width=15, text='Create',
               font=('Arial', 14), command=self.add_login)\
            .grid(row=7, column=0,columnspan=3)
        Button(self.create_window, width=15, text='Cancel',
               font=('Arial', 14), command=self.cancel)\
            .grid(row=7, column=0)
        self.create_window.mainloop()

    """Cancel adding a login account"""
    def cancel(self):
        self.create_window.destroy()

