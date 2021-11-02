import time
from tkinter import Tk, Label, Button, Scrollbar, Listbox, SINGLE, END, Entry, LEFT, messagebox, N, S

from common import Values
from database.DBConnection import DBConnection


class Expiry:
    def __init__(self):
        self._dbConnection = DBConnection()
        self._dbConnection.use_database()
        self._connection_object = self._dbConnection.get_connection_object()
        self._cursor = self._connection_object.cursor()
        # root window
        self.expiry_check_window = None
        # list box for showing the item list
        self.item_name_list_box = None
        # AN Entry field for entering item name
        self.search_entry_field = None
        # selected item in the list box
        self.selected_item = None
        #list variable for storing all items
        self.item_list = None

    """This method retrieves all Item Names and stores in a list."""
    def get_items_by_name(self):
        if self.item_list == None:
            self._cursor.execute("select Item_Name from grocerylist")
            list = self._cursor.fetchall()
            self.item_list = []
            # item_list is a list of tuples. So item in the for loop gives tuple everytime
            # take first element of the tuple as every tuple contains only one element
            for item in list:
                self.item_list.append(item[0])

        return self.item_list

    """This method is invoked automatically when the user enters any input in the Entry field"""
    def search_items(self,event=None):

        text = self.search_entry_field.get()
        #clear the item_list_box field
        self.item_name_list_box.delete(0, 'end')
        #get items of the listbox
        lbox_list = self.get_items_by_name()
        for item in lbox_list:
            if text.lower() in item.lower():
                self.item_name_list_box.insert(END, item)


    """This method shows the main window for the expiry menu"""
    def expiry(self):
        ''' Expiry GUI '''
        # localtime() gives us a tuple consisting hour,minute,day,year,mon_year....
        # get day , month and year from the local time
        today = str(time.localtime()[2]) + '/' + str(time.localtime()[1]) + '/' + str(time.localtime()[0])

        self._connection_object.commit()
        self.expiry_check_window = Tk()
        self.expiry_check_window.title('Check Expiry of the Items')
        self.expiry_check_window.wm_iconbitmap(Values.BITMAP_IMAGE)
        self.expiry_check_window.geometry("650x380+400+200")
        self.expiry_check_window.resizable(0, 0)
        self.expiry_check_window.protocol("WM_DELETE_WINDOW", self.on_closing)

        Label(self.expiry_check_window, text='Today: ' + today, pady=5, font=('Arial', 12)) \
            .grid(row=0, column=0, columnspan=3)
        Label(self.expiry_check_window, text='Its Illegal to sell expired items', font=('Arial', 12)) \
            .grid(row=1, column=0, columnspan=3)
        Label(self.expiry_check_window, text='-' * 125) \
            .grid(row=2, column=0, columnspan=3)

        Label(self.expiry_check_window, text='Enter Item Name   :  ', font=('Arial', 12), justify=LEFT) \
            .grid(row=3, column=0)
        # create an entry field for searching the item name
        self.search_entry_field = Entry(self.expiry_check_window, width=30, justify=LEFT)
        self.search_entry_field.grid(row=3, column=1)
        self.search_entry_field.bind('<KeyRelease>', self.search_items)
        Label(self.expiry_check_window, text=' ', justify=LEFT) \
            .grid(row=4, column=0)

        """An inner function that is called by the scroll bar automatically when
         the user interacts with it """
        def onvsb(*args):
            self.item_name_list_box.yview(*args)

        def on_mouse_wheel(event=None):
            self.item_name_list_box.yview("scroll", event.delta, "units")
            # this prevents default bindings from firing, which
            # would end up scrolling the widget twice
            return "break"

        vsb = Scrollbar(orient='vertical', command=onvsb)
        self.item_name_list_box = Listbox(self.expiry_check_window,
                                          width=35,
                                          yscrollcommand=vsb.set,
                                          selectmode=SINGLE,
                                          exportselection=False)
        self.item_name_list_box.bind('<<ListboxSelect>>', self.get_current_selected_item)
        self.item_name_list_box.bind("<MouseWheel>", on_mouse_wheel)
        self.item_name_list_box.grid(row=5, column=0)
        vsb.grid(row=5, column=0,columnspan=2, sticky=N + S)

        item_list = self.get_items_by_name()
        # add items to the listbox

        for item in item_list:
            self.item_name_list_box.insert(END, item)

        # create check expiry date button
        Button(self.expiry_check_window, text='Check Expiry date', font=('Arial', 12), command=self.check_expiry) \
            .grid(row=5, column=1, columnspan=2)
        Label(self.expiry_check_window, text='-' * 125) \
            .grid(row=6, column=0, columnspan=3)
        # create main menu button
        Button(self.expiry_check_window, text='Main Menu', font=('Arial', 12), command=self.mainmenu) \
            .grid(row=7, column=2)
        self.expiry_check_window.mainloop()

    """This method is invoked when the user clicks on the Check Expiry button"""
    def check_expiry(self):
        ''' Check Expiry Date button will navigate here '''
        if self.selected_item == None:
            messagebox.showerror("Error", "Please Select an Item")
        else:
            self._cursor.execute("select * from grocerylist where Item_Name='%s'" % (self.selected_item,))
            result = self._cursor.fetchone()
            if result:  # result[4] gives you expiry date
                Label(self.expiry_check_window, text=result[4], font=('Arial', 12)).grid(row=3, column=2)

            self._connection_object.commit()

    """This method is invoked when the user clicks on any item of the list box"""
    def get_current_selected_item(self, evt):
        #get current selected item from the list box
        self.selected_item = str((self.item_name_list_box.get(self.item_name_list_box.curselection())))
        # clear the Search Entry field
        self.search_entry_field.delete(0, 'end')
        # set the selected item into the Search Entry field
        self.search_entry_field.insert(0, str(self.selected_item))

    """This method is invoked when the user wants to navigate to the Main Window"""
    def mainmenu(self):
        self._dbConnection.close_database()
        self.expiry_check_window.destroy()

    def on_closing(self):
        self.mainmenu()