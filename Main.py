from PIL import ImageTk, Image
from tkinter import Tk
from tkinter import Label
from tkinter import Menu
from tkinter import Frame
from tkinter import Button
from tkinter import Entry
from tkinter import messagebox
from billing.Bill import Billing
from billing.Income import DailyIncome
from common import Values
from common.Hashing import Hash
from database.DBConnection import DBConnection
from login_maintenance.Login import Login
from stock_maintenance.AddItems import AddItems
from stock_maintenance.CheckExpiry import Expiry
from stock_maintenance.DeleteItems import Delete
from stock_maintenance.UpdateItems import Update


class Main:
    ''' Constructor '''
    def __init__(self):
        self.WinStat = ''
        self.application = None
        self.root = None
        self.user_email_entry = None
        self.passwordEntry = None
        self.dbConnection = DBConnection()
        self.user_email_id = None

    def get_root_window(self):
        # create root window
        root = Tk()
        root.title('My Grocery Store')
        # set image to the root window
        root.wm_iconbitmap(Values.BITMAP_IMAGE)
        root.configure(background="#d9d9d9")
        root.geometry("980x590+150+100")
        # bind the enter key to check button of the root window
        root.bind("<Return>", self.check_login)
        root.resizable(0, 0)
        root.protocol("WM_DELETE_WINDOW", self.on_closing)
        return root

    '''This is the Main Login window from where the application starts'''
    def process_main_window(self):
        if self.WinStat == 'application':
            self.application.destroy()
        # create main window
        self.root = self.get_root_window()
        # create a frame in the window
        frame = Frame(self.root, height=1050, width=590, bg="#d9d9d9")
        frame.propagate(0)
        frame.pack()

        # take main image and add it to a label and place it in a grid
        img = ImageTk.PhotoImage(Image.open(Values.LOGIN_PHOTO))
        panel = Label(frame, image=img)
        panel.grid(row=0, column=5, pady=50, columnspan=7)

        Label(frame, text='Grocery Store', bg="#d9d9d9", font=('Arial', 16))\
            .grid(row=1, column=5, columnspan=3)
        Label(frame, text="********************", bg="#d9d9d9", font=('Arial', 16)) \
            .grid(row=2, column=5, columnspan=3)
        Label(frame, text='-'*130, background="#d9d9d9") \
            .grid(row=3, column=5, columnspan=3)
        Label(frame, text='User Email ', bg="#d9d9d9", font=('Arial', 14))\
            .grid(row=4, column=4, columnspan=2)
        Label(frame, text='Password', bg="#d9d9d9", font=('Arial', 14))\
            .grid(row=5, column=4,columnspan=2)
        # create username and password entry fields
        self.user_email_entry = Entry(frame, width=35)
        self.user_email_entry.grid(row=4, column=5, columnspan=3)
        self.passwordEntry = Entry(frame, width=35, show="*")
        self.passwordEntry.grid(row=5, column=5, columnspan=3)

        Label(frame, text='', bg="#d9d9d9").grid(row=6, column=0, columnspan=4)
        Label(frame, text='', bg="#d9d9d9").grid(row=7, column=0, columnspan=4)
        # create enter button and add it to the grid. Also bind mouse left click to the button
        enterButton = Button(frame, width=10, text='Enter', font=('Arial', 16))
        enterButton.grid(row=8, column=5, columnspan=2)
        enterButton.bind('<Button-1>', self.check_login)

        # create close button and add it to the grid
        closeButton = Button(frame, width=10,text='Close',
                             command=self.root.destroy,
                             font=('Arial', 16))
        closeButton.grid(row=8, column=6, columnspan=3)
        self.root.mainloop()

    def check_login(self, event=None):
        ''' Check Button for Login Window '''
        self.user_email_id = self.user_email_entry.get()
        #self.user_email_id = 'hemachandra484@gmail.com'

        if self.user_email_id is None or self.user_email_id == '':
            messagebox.showerror("Error","User Email Id can't be blank")
        else:
            conn = self.dbConnection.get_connection_object()
            cursor = conn.cursor()
            cursor.execute("Select is_active,salt,hash from login where email_id='%s'" % (self.user_email_id,))
            record = cursor.fetchone()

            if record is None:
                messagebox.showerror("Error", "Wrong Email Address")
            else:
                password = self.passwordEntry.get()
                #password = 'admin123$'

                if password is None or password == '':
                    messagebox.showerror("Error", "Password can't be blank")
                #check if account is active or not
                elif record[0] == 1: #account active
                    db_salt = record[1]  # salt
                    db_hash = record[2]  # hash
                    hash_object = Hash()
                    # generate hash string for entered password
                    hashed_string = hash_object.generate_hash(password, db_salt)
                    #print(hashed_string)
                    # compare with already existing hash in the database
                    # if same then allow the access. else user authentication failed
                    if db_hash == hashed_string:
                        # username and password are matching.
                        #update the database that user is the current logged in user
                        self.set_currently_loggedin_val(1)
                        # Allow user to login by closing current window
                        self.root.destroy()
                        self.open_window()
                    else:
                        messagebox.showerror("Error", "Wrong Password")
                else:
                    messagebox.showerror("Error", "Account Deactivated by Admin."
                                                  "\n Please contact Administrator.")

    def open_window(self):
        ''' Opens Main Window '''
        self.WinStat = 'application'
        self.application = Tk()
        self.application.wm_iconbitmap(Values.BITMAP_IMAGE)
        self.application.title("Indian Grocery Store")
        self.application.geometry("1050x590")
        self.application.resizable(0,0)
        self.application.protocol("WM_DELETE_WINDOW", self.on_closing)

        ''' Main Window Picture '''
        img = ImageTk.PhotoImage(Image.open(Values.MAIN_WINDOW_PHOTO))
        Label(self.application, image=img).grid(row=0, column=0, columnspan=5)
        """Create Menus for stock,expiry,billing and login"""
        menu_bar = Menu(self.application)
        stock_menu = Menu(menu_bar, tearoff=0)
        expiry_menu = Menu(menu_bar, tearoff=0)
        billing_menu = Menu(menu_bar, tearoff=0)
        login_menu = Menu(menu_bar,tearoff=0)

        '''Creating menu items for Adding,Deleting and Updating Items In Stock'''
        #creating menu items for Stock Maintainance
        stock_menu.add_command(label="Add Items", command=self.addItemsIntoStock)
        stock_menu.add_command(label="Update Items", command=self.updateItemsInStock)
        stock_menu.add_command(label="Delete Items", command=self.deleteItemsFromStock)
        #creating menu items for Expiry Check
        expiry_menu.add_command(label="Check Expiry", command=self.checkExpiryOfItem)
        #creating menu items for Billing
        billing_menu.add_command(label="Billing", command=self.billingItems)
        billing_menu.add_command(label="Check Today's Income", command=self.calculateDailyIncome)
        #creating menu items for login maintenance
        login_menu.add_command(label="Create Login", command=self.create_login)
        login_menu.add_command(label="Update Login", command=self.update_login)
        login_menu.add_command(label="Delete Login", command=self.delete_login)

        '''We have created the menus. Now add them to Menu Bar'''
        menu_bar.add_cascade(label="Stock Maintenance", menu=stock_menu)
        menu_bar.add_cascade(label="Expiry", menu=expiry_menu)
        menu_bar.add_cascade(label="Billing", menu=billing_menu)
        menu_bar.add_cascade(label="Login Maintenance", menu=login_menu)
        menu_bar.add_cascade(label="Logout", command=self.logout)

        self.application.config(menu=menu_bar)
        self.application.mainloop()

    def addItemsIntoStock(self):
        #close the current window
        self.application.destroy()
        #create object to the class and call the method
        maintenance = AddItems()
        maintenance.add_items()
        #when the add items windows is closed open the main window again
        self.open_window()

    def deleteItemsFromStock(self):
        #delete items from the addItems
        # close the current window
        self.application.destroy()
        #call the delete class method
        delete_stock = Delete()
        delete_stock.delete_item()
        # when the delete items windows is closed open the main window again
        self.open_window()

    def updateItemsInStock(self):
        # update items in addItems
        # close the current window
        self.application.destroy()
        #call the Update class method
        update_stock = Update()
        update_stock.update_stock()
        # when the update item window is closed open the main window again
        self.open_window()

    def checkExpiryOfItem(self):
        # check expiry of the item
        # close the current window
        self.application.destroy()
        check = Expiry()
        check.expiry()
        # when the check expiry item window is closed open the main window again
        self.open_window()

    def calculateDailyIncome(self):
        self.application.destroy()
        income = DailyIncome()
        income.get_today_income()
        # when the calculate items window is closed open the main window again
        self.open_window()

    def billingItems(self):
        self.application.destroy()
        billing = Billing()
        billing.billingitems()
        # when the billing items window is closed open the main window again
        self.open_window()

    def create_login(self):
        login_maintenance = Login(self.user_email_id, self.dbConnection)
        destroyed = login_maintenance.create_login(self.application)
        #if the main window is destroyed open the main window again
        if destroyed:
            self.open_window()

    def update_login(self):
        self.application.destroy()
        login_maintenance = Login(self.user_email_id, self.dbConnection)
        login_maintenance.update_login()
        self.open_window()

    def delete_login(self):
        login_maintenance = Login(self.user_email_id, self.dbConnection)
        destroyed = login_maintenance.delete_login(self.application)
        # if the main window is destroyed open the main window again
        if destroyed:
            self.open_window()

    def logout(self):
        result = messagebox.askquestion("Confirm Your Action", "Do You Want To Logout?", icon='warning')
        if result == 'yes':
            #set currently_loggedin value to false which indicates that the user has
            #logged out from the app
            self.set_currently_loggedin_val(0)
            self.process_main_window()

    def on_closing(self):
        #print("Closing Database.Please Wait")
        # set currently_loggedin value to false which indicates that the user has
        # logged out from the app
        self.set_currently_loggedin_val(0)
        #close the database
        self.dbConnection.close_database()
        if self.application is not None:
            self.application.destroy()
        else:
            self.root.destroy()

    def set_currently_loggedin_val(self,value):
        # if value is 1 logged in is true else if 0 logout
        if self.user_email_id is not None:
            sql = """UPDATE login SET currently_loggedin=%s WHERE username=%s"""
            data = (value, self.user_email_id)
            conn = self.dbConnection.get_connection_object()
            cursor = conn.cursor()
            cursor.execute(sql,data)
            conn.commit()

"""End of class.
 Initialize The Database.
 Create the object and start the window"""

try:
    main = Main()
    main.dbConnection.run_sql_file(Values.SQL_FILE)
    main.process_main_window()
except Exception as ex:
    main = Main()
    #print(str(ex))
    #reset the current logged in user value to logged out if username not none
    main.set_currently_loggedin_val(0)
    messagebox.showerror("Error",str(ex))

"""
hashing = Hash()
salt = hashing.generate_salt()
print(salt)
hashed_string = hashing.generate_hash("admin123$",salt)
print(hashed_string)
"""