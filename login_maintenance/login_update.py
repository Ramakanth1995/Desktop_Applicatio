from tkinter import Tk, Label, Entry, RIGHT, Button, messagebox
from common import Values
from common.Hashing import Hash
from mailing.mail import Mail


class Update:
    def __init__(self):
        self._dbConnection = None
        self._entries_for_updating_login = None
        self._current_loggedin_username = None
        self._create_window = None
        self.col = ('Email Id','Username','Password','Confirm Password')

    """Check if the email exists"""
    def _user_email_exists(self, email_id):
        sql = "SELECT * FROM login WHERE email_id = '%s'" % (email_id,)
        conn = self._dbConnection.get_connection_object()
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        conn.commit()
        if result is not None:
            return True
        else:
            return False

    """Create root window"""
    def _create_update_root_window(self):
        self._create_window = Tk()
        self._create_window.title("Update Details of User")
        self._create_window.wm_iconbitmap(Values.BITMAP_IMAGE)
        self._create_window.geometry("640x350+500+200")
        #self._create_window.resizable(0, 0)

    """Resets all the entry fields and the checkbutton"""
    def _reset_window(self):
        for entry in self._entries_for_updating_login:
            entry.delete(0, 'end')

    """Create the GUI window for updating the user details"""
    def create_update_window(self,current_user_email,dbConnection):
        self._dbConnection = dbConnection
        self._current_loggedin_username = current_user_email
        self._create_update_root_window()

        rows = 0
        columns = 0
        Label(self._create_window, text='Update Details Of User',
              padx=80, pady=40, font=('Arial', 16)) \
            .grid(row=rows, column=0, rowspan=2, columnspan=2)
        rows = rows +1
        Label(self._create_window, text='-' * 110, padx=35) \
            .grid(row=rows, column=0, columnspan=2)

        self._entries_for_updating_login = []

        #create entry fields in the window
        for entry in self.col:
            rows = rows + 1
            Label(self._create_window,
                  pady=7,
                  text=self.col[columns],
                  font=('Arial', 12),
                  justify=RIGHT) \
            .grid(row=rows, column=0)
            columns = columns + 1
            entry = Entry(self._create_window, width=50)
            entry.grid(row=rows, column=1)
            if self.col[columns - 1] == self.col[0]:
                entry.insert(0, str(self._current_loggedin_username))
                entry.configure(state='disabled')
            elif self.col[columns-1] == Values.PASSWORD.title()\
                    or self.col[columns-1] == self.col[len(self.col)-1]:
                entry.configure(show = "*")
            #add the entry field to the entries list
            self._entries_for_updating_login.append(entry)

        rows = rows + 1
        Label(self._create_window, text=' ') \
            .grid(row=rows, column=0)
        rows = rows + 1
        #create buttons update and cancel
        Button(self._create_window, width=15, text='Update',
               font=('Arial', 14), command=self.update_account) \
            .grid(row=rows, column=0)
        Button(self._create_window, width=15, text='Cancel',
               font=('Arial', 14), command=self.cancel) \
            .grid(row=rows, column=0,columnspan=3)

        self._create_window.mainloop()

    """Check for the email id and then update details"""
    def update_account(self):
        dictionary = {}
        index = 0
        for entry in self._entries_for_updating_login:
            dictionary[self.col[index]] = entry.get()
            index +=1
        #print(dictionary)
        if dictionary.get(Values.PASSWORD.title()) != dictionary.get('Confirm Password'):
            messagebox.showerror("Error","Password Not Matching")
        else:
            self._update_details_in_database(dictionary)
            messagebox.showinfo("Success", "User Account Updated")
            self._send_mail(dictionary)
            self._reset_window()

    """Update the user details in database. """
    def _update_details_in_database(self, dictionary):
        hashing = Hash()
        salt = hashing.generate_salt()
        #print(dictionary.get(Values.PASSWORD.title()))
        password_hash = hashing.generate_hash(dictionary.get(Values.PASSWORD.title()), salt)

        sql = """UPDATE login SET username=%s,salt=%s,hash=%s,is_active=%s WHERE email_id=%s"""
        data =(dictionary.get(Values.USER_NAME),
               salt,
               password_hash,
               1,
               self._current_loggedin_username)
        conn = self._dbConnection.get_connection_object()
        cursor = conn.cursor()
        cursor.execute(sql,data)
        conn.commit()

    """This method sends the username and password to the user who created the login"""
    def _send_mail(self,dictionary):
        # this sends the mail in background in a thread
        # this avoids the user not to block the interaction with the GUI
        mailing = Mail(self._current_loggedin_username,
                       dictionary.get(Values.USER_NAME),
                       dictionary.get(Values.PASSWORD.title()))
        mailing.set_update_login_message()
        mailing.start()

    """Cancel updating a login account"""
    def cancel(self):
        self._create_window.destroy()



