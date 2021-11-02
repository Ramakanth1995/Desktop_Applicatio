from tkinter import Tk,LEFT, RIGHT, SINGLE, END
from tkinter import Label,Entry,Button,Listbox
from tkinter import N,S
from tkinter import Scrollbar
from tkinter import messagebox

from common import Values
from database.DBConnection import DBConnection


class Update:

    def __init__(self):
        self._dbConnection = DBConnection()
        self._dbConnection.use_database()
        self._connection_object = self._dbConnection.get_connection_object()
        self._cur = self._connection_object.cursor()
        """Variables for Updating Stocks"""
        # root window when update button clicked
        self.update_stock_button_window = None
        # root window when update menu item is clicked
        self.update_stock_window = None
        self.flag = None
        #self.update_item_no = None

        # Entry Fields
        self.entries_for_updating_item = None
        # Entry field for searching the Item
        self.search_entry_field = None

        #listboxes
        self.item_name_listbox = None
        self.qty_listbox = None
        self.cost_listbox = None
        self.expirydate_listbox = None
        self.item_code_listbox = None
        #name of the item after selected from the listbox is stored in this variable
        self.selected_item_name = None
        self.item_list = None

    # this function gets the id value of from the database and increaments it and shows in the text box
    # this can also be done in the database automatically
    def _auto_increament(self):
        ''' To auto-generate item No '''
        self._cur.execute("select max(Item_No) from grocerylist")
        incval = self._cur.fetchone()
        incval = incval[0] + 1
        return incval

    def mainmenu(self):
        ''' Main Menu Button '''
        if self.flag == 'update_stock_button':
            #self.dbConnection.close_database()
            self.update_stock_button_window.destroy()
        elif self.flag == 'update_stock':
            self._dbConnection.close_database()
            self.update_stock_window.destroy()

    def on_closing(self):
        if self.flag == "update_stock_button":
            self.update_stock_button_window.destroy()
            self.flag = "update_stock"
        else:
            self._dbConnection.close_database()
            self.update_stock_window.destroy()

    def clear_listboxes(self):
        # clear the item_list_box field
        self.item_name_listbox.delete(0, 'end')
        self.qty_listbox.delete(0, 'end')
        self.cost_listbox.delete(0, 'end')
        self.expirydate_listbox.delete(0, 'end')
        self.item_code_listbox.delete(0,'end')

    """This method retrieves all Item Names and stores in a list."""
    def get_items(self):
        if self.item_list is None:
            self._cur.execute("select Item_Name from grocerylist")
            list = self._cur.fetchall()
            self.item_list = []
            # item_list is a list of tuples. So item in the for loop gives tuple everytime
            # take first element of the tuple as every tuple contains only one element
            for item in list:
                self.item_list.append(item[0])

        return self.item_list

    """This method is invoked automatically when the user
        enters any input in the Entry field"""

    def search_items(self, event=None):
        text = self.search_entry_field.get()
        #clear the listboxes
        self.clear_listboxes()
        # get item names of the listboxes
        item_list = self.get_items()
        for item in item_list:
            if text.lower() in item.lower():
                self.item_name_listbox.insert(END, item)
                self._cur.execute("select "
                                 "(Quantity_Remain),"
                                 "(Item_Cost),"
                                 "(Expiry_Date),"
                                 "(Item_Code)"
                                 "from grocerylist where Item_Name='%s'" % (item,))
                record = self._cur.fetchone()
                #get qty of the item
                self.qty_listbox.insert(END, record[0])
                # get cost of the item and update in the list box
                self.cost_listbox.insert(END, record[1])
                # get expiry date of the item and update in the list box
                self.expirydate_listbox.insert(END, record[2])
                #get Item_code of the item and update in the list box
                self.item_code_listbox.insert(END,record[3])

    """This function updates the stock items"""
    def update_stock(self):
        ''' Which item to Update GUI '''
        self.flag = 'update_stock'
        # create root window for updating items
        self.update_stock_window = Tk()
        self.update_stock_window.title("Update grocery item from Stock")
        self.update_stock_window.wm_iconbitmap(Values.BITMAP_IMAGE)
        self.update_stock_window.geometry("930x330+400+200")
        self.update_stock_window.resizable(0,0)
        self.update_stock_window.protocol("WM_DELETE_WINDOW", self.on_closing)

        Label(self.update_stock_window, text='Enter Item Name To Update   :  ',
              padx = 10,pady =25,font=('Arial', 12), justify=LEFT) \
            .grid(row=1, column=0)
        # create an entry field for searching the item name
        self.search_entry_field = Entry(self.update_stock_window, width=30, justify=LEFT)
        self.search_entry_field.grid(row=1, column=1)
        self.search_entry_field.bind('<KeyRelease>', self.search_items)

        Label(self.update_stock_window, text='Item',font=('Arial', 10))\
            .grid(row=2, column=0)
        Label(self.update_stock_window, text='Qty Remain',font=('Arial', 10))\
            .grid(row=2, column=1)
        Label(self.update_stock_window, text='Cost',font=('Arial', 10))\
            .grid(row=2, column=2)
        Label(self.update_stock_window, text='Expiry Date',font=('Arial', 10))\
            .grid(row=2, column=3)
        Label(self.update_stock_window, text='Item Code', font=('Arial', 10)) \
            .grid(row=2, column=4)

        #call update_window() method so that it gets data from the dataabase
        #and loads the data into the GUI
        self.update_window()
        Label(self.update_stock_window, text=' ').grid(row=5, column=0)

        Button(self.update_stock_window, width=20, text='Main Menu', command=self.mainmenu) \
            .grid(row=6,column=3)
        Button(self.update_stock_window, width=20, text='Update', command=self.update_button_action) \
            .grid(row=6,column=4)
        self.update_stock_window.mainloop()

    """This function takes data from the database and inserts into the columns created 
        in the update window."""
    def update_window(self):
        ''' Display data from database for Update Window'''

        def scroll(*args):
            self.item_name_listbox.yview(*args)
            self.qty_listbox.yview(*args)
            self.cost_listbox.yview(*args)
            self.expirydate_listbox.yview(*args)
            self.item_code_listbox.yview(*args)

        index = 0
        vsb = Scrollbar(orient='vertical', command=scroll)
        self.item_name_listbox = Listbox(self.update_stock_window,
                                         width=22,
                                         yscrollcommand=vsb.set,
                                         selectmode=SINGLE,
                                         exportselection=False)
        self.item_name_listbox.bind('<<ListboxSelect>>', self.get_current_selected_item)

        self.qty_listbox = Listbox(self.update_stock_window,
                                   width=20,
                                   yscrollcommand=vsb.set)
        self.cost_listbox = Listbox(self.update_stock_window,
                                    width=20,
                                    yscrollcommand=vsb.set)
        self.expirydate_listbox = Listbox(self.update_stock_window,
                                          width=20,
                                          yscrollcommand=vsb.set)
        self.item_code_listbox = Listbox(self.update_stock_window,
                                          width=22,
                                          yscrollcommand=vsb.set)

        self.item_name_listbox.grid(row=3, column=0)
        self.qty_listbox.grid(row=3, column=1)
        self.cost_listbox.grid(row=3, column=2)
        self.expirydate_listbox.grid(row=3, column=3)
        self.item_code_listbox.grid(row=3,column=4)
        vsb.grid(row=3, column=5, sticky=N + S)

        # bind the mouse wheel property
        self.item_name_listbox.bind("<MouseWheel>", self._on_mouse_wheel)
        self.qty_listbox.bind("<MouseWheel>", self._on_mouse_wheel)
        self.cost_listbox.bind("<MouseWheel>", self._on_mouse_wheel)
        self.expirydate_listbox.bind("<MouseWheel>", self._on_mouse_wheel)
        self.item_code_listbox.bind("<MouseWheel>", self._on_mouse_wheel)
        # add items to the List boxes
        self._cur.execute("select * from grocerylist")
        for record in self._cur:
            index += 1
            self.item_name_listbox.insert(index, record[1])  # item_name
            self.qty_listbox.insert(index, record[2])  # quantity_remain
            self.cost_listbox.insert(index, record[3])  # item_cost
            self.expirydate_listbox.insert(index, record[4])  # Expiry Date
            self.item_code_listbox.insert(index,record[7]) #Item_Code

        # commit changes to the database
        self._connection_object.commit()

    """This method is invoked automatically when we click on Update button"""
    def update_button_action(self):
        ''' Update Stock Button GUI '''
        self.flag = 'update_stock_button'
        # open new window for updating the item having the item no entered by the user
        # create root window for Updating stock Items
        self.update_stock_button_window = Tk()
        self.update_stock_button_window.title("Update Item")
        self.update_stock_button_window.wm_iconbitmap(Values.BITMAP_IMAGE)
        self.update_stock_button_window.geometry("630x330+500+200")
        self.update_stock_button_window.resizable(0, 0)
        self.update_stock_button_window.protocol("WM_DELETE_WINDOW", self.on_closing)

        Label(self.update_stock_button_window, text='Enter Details To Update Item',
              padx=80, pady=40, font=('Arial', 16)) \
            .grid(row=0, column=0, rowspan=2, columnspan=2)
        Label(self.update_stock_button_window, text='-' * 110, padx=35) \
            .grid(row=1, column=0, columnspan=2)

        col = ('ItemName', 'QtyRem', 'Cost', 'Expiry')
        # take entries_for_updating_item as a list of Entry objects whose
        # length equal to the col tuple above that means entries_for_updating_item
        # contains 4 Entry objects
        self.entries_for_updating_item = [''] * len(col)

        Label(self.update_stock_button_window, pady=7, text='Item_Name', font=('Arial', 12), justify=RIGHT) \
            .grid(row=2, column=0)
        self.entries_for_updating_item[0] = Entry(self.update_stock_button_window, width=30)
        self.entries_for_updating_item[0].grid(row=2, column=1)

        Label(self.update_stock_button_window, text='Quantity_Remain', font=('Arial', 12), justify=RIGHT) \
            .grid(row=4, column=0)
        self.entries_for_updating_item[1] = Entry(self.update_stock_button_window, width=30)
        self.entries_for_updating_item[1].grid(row=4, column=1)

        Label(self.update_stock_button_window, text='Cost', font=('Arial', 12), justify=RIGHT) \
            .grid(row=6, column=0)
        self.entries_for_updating_item[2] = Entry(self.update_stock_button_window, width=30)
        self.entries_for_updating_item[2].grid(row=6, column=1)

        Label(self.update_stock_button_window, text='Expiry_Date', font=('Arial', 12), justify=RIGHT) \
            .grid(row=8, column=0)
        self.entries_for_updating_item[3] = Entry(self.update_stock_button_window, width=30)
        lb4 = self.entries_for_updating_item[3].grid(row=8, column=1)

        Label(self.update_stock_button_window, text=' ', justify=RIGHT) \
            .grid(row=9, column=0)

        ''' This will automatically show data of respective itemno in the textbox '''
        self._cur.execute("select * from grocerylist where Item_Name='%s'" % (self.selected_item_name,))
        index = 0
        for record in self._cur:
            index += 1
            self.entries_for_updating_item[0].insert(index, record[1]) #item_name
            self.entries_for_updating_item[1].insert(index, record[2]) #quantity remaining
            self.entries_for_updating_item[2].insert(index, record[3]) #cost
            self.entries_for_updating_item[3].insert(index, record[4]) #Expiry date
        self._connection_object.commit()

        Button(self.update_stock_button_window, width=15, text='Update',
               font=('Arial', 12), command=self.update_database).grid(row=10, column=1)
        self.update_stock_button_window.mainloop()

    """This method gets the current selected item from the Item_Name listbox
    and adds that to the search entry field"""
    def get_current_selected_item(self,evt):
        self.selected_item_name  = str((self.item_name_listbox.get(self.item_name_listbox.curselection())))
        self.search_entry_field.delete(0,'end')
        self.search_entry_field.insert(END, self.selected_item_name)

    def update_database(self):
        ''' Update in the database '''
        selected_item_name = self.selected_item_name
        update_item_name = self.entries_for_updating_item[0].get()
        qty_remain = self.entries_for_updating_item[1].get()
        cost = "{0:.2f}".format(float(self.entries_for_updating_item[2].get()),)
        expiry = self.entries_for_updating_item[3].get()
        self._cur.execute("update grocerylist set "
                         "Item_Name='%s',Quantity_Remain='%s',Item_Cost='%s',Expiry_Date='%s'"
                         "where Item_Name='%s'" %
                          (update_item_name, qty_remain, cost, expiry, selected_item_name))
        self._connection_object.commit()
        messagebox.showinfo("Success","Updated Successfully")
        self.update_stock_button_window.destroy()
        self.flag = 'update_stock'
        #update the window as the database is updated now
        self.update_window()

    """This method is invoked when the user scrolls on the List boxes"""
    def _on_mouse_wheel(self, event=None):
        self.item_name_listbox.yview("scroll", event.delta, "units")
        self.qty_listbox.yview("scroll", event.delta, "units")
        self.cost_listbox.yview("scroll", event.delta, "units")
        self.expirydate_listbox.yview("scroll", event.delta, "units")
        self.item_code_listbox.yview("scroll", event.delta, "units")
        # this prevents default bindings from firing, which
        # would end up scrolling the widget twice
        return "break"