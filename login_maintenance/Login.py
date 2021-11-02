from tkinter import messagebox

from login_maintenance.login_create import Create
from login_maintenance.login_delete import Delete
from login_maintenance.login_update import Update


class Login:
    def __init__(self,user_email,dbConnection):
        self._user_email = user_email
        self._dbConnection = dbConnection

    def create_login(self,application):
        if self._is_admin() == 1:
            #close the main window
            application.destroy()
            create_login = Create()
            create_login.create_login_window(self._user_email, self._dbConnection)
            return True
        else:
            messagebox.showerror("Error","You don't have permissions to create login.")
            return False

    def update_login(self):
        update_login = Update()
        update_login.create_update_window(self._user_email,self._dbConnection)

    def delete_login(self,application):
        if self._is_admin() == 1:
            #close the main window
            application.destroy()
            delete_login = Delete()
            delete_login.delete_login(self._user_email,self._dbConnection)
            return True
        else:
            messagebox.showerror("Error","You don't have permissions to delete login.")
            return False

    def _is_admin(self):
        sql = "SELECT (is_admin) FROM login WHERE email_id = '%s'"%(self._user_email,)
        conn = self._dbConnection.get_connection_object()
        cursor = conn.cursor()
        cursor.execute(sql)
        is_admin = cursor.fetchone()[0]
        return is_admin
