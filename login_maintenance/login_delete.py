import re
from tkinter import Tk, Label, Entry, RIGHT, Button, messagebox
from common import Values
from mailing.mail import Mail


class Delete:
    def __init__(self):
        self.create_window = None
        # user email of user who is creating the login
        self._current_loggedin_username = None
        self._dbConnection = None
        # entry fields for taking username, email id and confirm email id
        self.entries_for_deleting_login = None
        self.EMAIL_REGEX = re.compile(Values.PASSWORD_REGEX)
        self.col = ('Email Id', 'Confirm Email Id')

    """Check if the email exists"""
    def _user_email_exists(self, email_id):
        sql = "SELECT * FROM login WHERE email_id = '%s'"%(email_id,)
        conn = self._dbConnection.get_connection_object()
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        conn.commit()
        if result is not None:
            return True
        else:
            return False

    """Check if the email user is admin or not"""
    def _is_admin(self,email_id):
        sql = "SELECT (is_admin) FROM login WHERE email_id = '%s'"%(email_id,)
        conn = self._dbConnection.get_connection_object()
        cursor = conn.cursor()
        cursor.execute(sql)
        is_admin = cursor.fetchone()[0]
        conn.commit()
        return is_admin

    """Create root window"""
    def _create_delete_window(self):
        self.create_window = Tk()
        self.create_window.title("Delete Login Account")
        self.create_window.wm_iconbitmap(Values.BITMAP_IMAGE)
        self.create_window.geometry("640x250+500+200")
        self.create_window.resizable(0, 0)

    """Resets all the entry fields and the checkbutton"""
    def _reset_window(self):
        for entry in self.entries_for_deleting_login:
            entry.delete(0, 'end')

    def delete_login(self, _current_loggedin_username, _dbConnection):
        self._dbConnection = _dbConnection
        self._current_loggedin_username = _current_loggedin_username
        #create the window
        self._create_delete_window()
        #create labels and Entry fields
        Label(self.create_window, text='Enter Details Of User You Want To Delete',
              padx=80, pady=40, font=('Arial', 16)) \
            .grid(row=0, column=0, rowspan=2, columnspan=2)
        Label(self.create_window, text='-' * 110, padx=35) \
            .grid(row=1, column=0, columnspan=2)


        # take self.entries_for_deleting_login as a list of Entry objects whose
        # length equal to the col tuple above that means self.entries_for_deleting_login
        # contains 2 Entry objects
        self.entries_for_deleting_login = [''] * (len(self.col))

        Label(self.create_window, pady=7, text=self.col[0], font=('Arial', 12), justify=RIGHT) \
            .grid(row=2, column=0)
        self.entries_for_deleting_login[0] = Entry(self.create_window, width=50)
        self.entries_for_deleting_login[0].grid(row=2, column=1)

        Label(self.create_window, text=self.col[1], font=('Arial', 12), justify=RIGHT) \
            .grid(row=4, column=0)
        self.entries_for_deleting_login[1] = Entry(self.create_window, width=50)
        self.entries_for_deleting_login[1].grid(row=4, column=1)

        Label(self.create_window, text=' ', justify=RIGHT) \
            .grid(row=5, column=0)

        Button(self.create_window, width=15, text='Delete',
               font=('Arial', 14), command=self.delete_account) \
            .grid(row=6, column=0, columnspan=3)
        Button(self.create_window, width=15, text='Cancel',
               font=('Arial', 14), command=self.cancel) \
            .grid(row=6, column=0)
        self.create_window.mainloop()

    """Check for the email id and then delete the account"""
    def delete_account(self):
        email_id = self.entries_for_deleting_login[0].get()
        confirm_email_id = self.entries_for_deleting_login[1].get()
        # print("Check box = %s"%(self.check_var.get()))
        if (email_id == '') or (email_id is None) or (not self.EMAIL_REGEX.match(email_id)):
            messagebox.showerror("Error", "Please enter valid email id")
        #check if the email_id exists
        elif not self._user_email_exists(email_id):
            messagebox.showerror("Error", "User Email doesn't exist.")

        #check if the email_id user is admin. If it is another admin account
        #then we can't delete the account
        elif self._is_admin(email_id) == 1:
            messagebox.showerror("Error","You can't delete an account\nwhich is having Admin privileges")
        else: #if it is not an admin account we can delete it
            if confirm_email_id == '' or confirm_email_id is None:
                messagebox.showerror("Error", "Please enter confirm email id")
            elif email_id == confirm_email_id:
                self.delete_account_from_database(email_id)
                self._reset_window()
                self._send_mail(email_id)

    """Delete the account from database. We don't delete. We just deactivate the account"""
    def delete_account_from_database(self,email_id):
        sql = "SELECT is_active FROM login WHERE email_id='%s'"%(email_id,)
        conn = self._dbConnection.get_connection_object()
        cursor = conn.cursor()
        cursor.execute(sql)
        record = cursor.fetchone()
        is_active = record[0]
        if is_active == 1:
            sql = "UPDATE login SET is_active='%s' WHERE email_id='%s'"%(0,email_id)
            cursor.execute(sql)
            conn.commit()
            messagebox.showinfo("Success", "User Account Deleted")
        else:
            messagebox.showerror("Error","User Account Already Deactivated")

    """This method sends deleted message mail to the currently logged in user"""
    def _send_mail(self, email_id):
        # this sends the mail in background in a thread
        # this avoids the user not to block the interaction with the GUI
        mailing = Mail(self._current_loggedin_username,email_id)
        mailing.set_delete_login_message()
        mailing.start()

    """Cancel deleting a login account"""
    def cancel(self):
        self.create_window.destroy()


