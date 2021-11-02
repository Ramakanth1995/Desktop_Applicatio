from tkinter import Scrollbar, Listbox, Label, Entry, Button, messagebox, END, MULTIPLE, SINGLE, RIGHT, LEFT
from tkinter import N, S
from tkinter import Tk

from common import Values
from database.DBConnection import DBConnection


class Delete:

    def __init__(self):
        self._dbConnection = DBConnection()
        self._dbConnection.use_database()
        self._connection_object = self._dbConnection.get_connection_object()
        self._cursor = self._connection_object.cursor()
        """Variables for Deleting Stocks"""
        #root window
        self.delete_window = None
        #listboxes
        self.item_name_listbox = None
        self.qty_listbox = None
        self.cost_listbox = None
        self.expiry_listbox = None
        self.item_code_listbox = None

        self.selected_item = None
        self.item_list = None

        # Entry field for searching the Item
        self.search_entry_field = None

    def clear_listboxes(self):
        # clear the item_list_box field
        self.item_name_listbox.delete(0, 'end')
        self.qty_listbox.delete(0, 'end')
        self.cost_listbox.delete(0, 'end')
        self.expiry_listbox.delete(0, 'end')
        self.item_code_listbox.delete(0,'end')

    """This method retrieves all Item Names and stores in a list."""
    def get_items(self):
        self._cursor.execute("select (Item_Name) from grocerylist")
        list = self._cursor.fetchall()
        self.item_list = []
        # item_list is a list of tuples. So item in the for loop gives tuple everytime
        # take first element of the tuple as every tuple contains only one element
        for item in list:
            self.item_list.append(item[0])

        return self.item_list

    """
       This method is invoked automatically when the user enters
       any input in the Entry field
    """
    def search_items(self, event=None):
        text = self.search_entry_field.get()
        # clear the listboxes
        self.clear_listboxes()
        # get items of the listboxes
        item_list = self.get_items()
        for item in item_list:
            if text.lower() in item.lower():
                self.item_name_listbox.insert(END, item)
                # get quantity remaining of the item and update in the list box
                self._cursor.execute("select "
                                 "(Quantity_Remain),"
                                 "(Item_Cost),"
                                 "(Expiry_Date),"
                                 "(Item_Code)"
                                 "from grocerylist where Item_Name='%s'" % (item,))
                record = self._cursor.fetchone()
                if record is not None:
                    self.qty_listbox.insert(END, record[0])
                    # get cost of the item and update in the list box
                    self.cost_listbox.insert(END, record[1])
                    # get expiry date of the item and update in the list box
                    self.expiry_listbox.insert(END, record[2])
                    #get Item_Code of the item and update in the list box
                    self.item_code_listbox.insert(END,record[3])

    def mainmenu(self):
        self._dbConnection.close_database()
        self.delete_window.destroy()

    def on_closing(self):
        self.mainmenu()

    def delete_item(self):
        ''' Delete Stock GUI '''
        self.delete_window = Tk()
        self.delete_window.title("Delete grocery item from Stock")
        self.delete_window.wm_iconbitmap(Values.BITMAP_IMAGE)
        self.delete_window.geometry("800x350+400+200")
        self.delete_window.resizable(0,0)
        self.delete_window.protocol("WM_DELETE_WINDOW", self.on_closing)

        Label(self.delete_window,padx=20,pady=30,text='Select Item To Delete Item',font=('Arial', 12), justify=RIGHT)\
        .grid(row=1, column=0)
        # create an entry field for searching the item name
        self.search_entry_field = Entry(self.delete_window, width=30, justify=LEFT)
        self.search_entry_field.grid(row=1, column=1,columnspan=2)
        self.search_entry_field.bind('<KeyRelease>', self.search_items)
        Label(self.delete_window, text='Item',font=('Arial', 12), justify=RIGHT)\
            .grid(row=2, column=0)
        Label(self.delete_window, text='Qty Remain',font=('Arial', 12), justify=RIGHT)\
            .grid(row=2, column=1)
        Label(self.delete_window, text='Cost',font=('Arial', 12), justify=RIGHT)\
            .grid(row=2, column=2)
        Label(self.delete_window, text='Expiry Date',font=('Arial', 12), justify=RIGHT)\
            .grid(row=2, column=3)
        Label(self.delete_window, text='Item Code', font=('Arial', 12), justify=RIGHT) \
            .grid(row=2, column=4)

        #fetch the records from the database
        # create the GUI window and set all the vertical scroll bars
        # create Listboxes for displaying the records
        self.update_window()
        Label(self.delete_window, text=' ', justify=RIGHT) \
            .grid(row=5, column=2)
        Button(self.delete_window,width=20, text='Main Menu', command=self.mainmenu)\
            .grid(row=6, column=4)
        Button(self.delete_window, width=20, text='Delete', command=self.delete_stock_button) \
                        .grid(row=6, column=3)

        self.delete_window.mainloop()

    def get_current_selected_item(self,evt):
        self.selected_item  = str((self.item_name_listbox.get(self.item_name_listbox.curselection())))
        self.search_entry_field.delete(0, 'end')
        self.search_entry_field.insert(END, self.selected_item)

    """This method refreshes the data present in the GUI 
        windows after deleting the item"""
    def update_window(self):

        # global lb1, delete_window, cur, connectObject
        # this function is called by the Scroll bar class when the user scrolls the Listboxes
        def onvsb(*args):
            self.item_name_listbox.yview(*args)
            self.qty_listbox.yview(*args)
            self.cost_listbox.yview(*args)
            self.expiry_listbox.yview(*args)
            self.item_code_listbox.yview(*args)

        index = 0
        vsb = Scrollbar(orient='vertical', command=onvsb)

        """
        set exportselection=False for the listbox
        You should always include the exportselection=0/False option
        in the Tkinter Listbox,especially when we have more than one 
        of them onscreen at the same time.The default without this 
        option is a bizarre mode in which the list selection is
        tied to the system clipboard; simultaneous selections in
        multiple lists simply cannot exist (and you're trashing
        anything the user might have put in the clipboard themselves
        """
        self.item_name_listbox = Listbox(self.delete_window,
                                         width=25,
                                         yscrollcommand=vsb.set,
                                         selectmode = SINGLE,
                                         exportselection=False)
        self.item_name_listbox.bind('<<ListboxSelect>>', self.get_current_selected_item)

        self.qty_listbox = Listbox(self.delete_window,
                                   width=15,
                                   yscrollcommand=vsb.set)
        self.cost_listbox = Listbox(self.delete_window,
                                    width=15,
                                    yscrollcommand=vsb.set)
        self.expiry_listbox = Listbox(self.delete_window,
                                      width=15,
                                      yscrollcommand=vsb.set)
        self.item_code_listbox = Listbox(self.delete_window,
                                      width=22,
                                      yscrollcommand=vsb.set)

        self.item_name_listbox.grid(row=3, column=0)
        self.qty_listbox.grid(row=3, column=1)
        self.cost_listbox.grid(row=3, column=2)
        self.expiry_listbox.grid(row=3, column=3)
        self.item_code_listbox.grid(row=3, column=4)

        self.item_name_listbox.bind("<MouseWheel>", self._on_mouse_wheel)
        self.qty_listbox.bind("<MouseWheel>", self._on_mouse_wheel)
        self.cost_listbox.bind("<MouseWheel>", self._on_mouse_wheel)
        self.expiry_listbox.bind("<MouseWheel>", self._on_mouse_wheel)
        self.item_code_listbox.bind("<MouseWheel>", self._on_mouse_wheel)

        vsb.grid(row=3, column=5, sticky=N + S)

        self._cursor.execute("select * from grocerylist")
        #get records one by one. Here i represent record in the cursor tuple
        for record in self._cursor:
            index += 1
            self.item_name_listbox.insert(index, record[1])
            self.qty_listbox.insert(index, record[2])
            self.cost_listbox.insert(index, record[3])
            self.expiry_listbox.insert(index, record[4])
            self.item_code_listbox.insert(index, record[7])

        #commit changes to the database
        self._connection_object.commit()

    def delete_stock_button(self):
        ''' Deleting from the table '''
        if self.selected_item is None:
            messagebox.showerror("Error", "Please Select An Item")
        else:
            result = messagebox.askquestion("Confirm Your Action",
                                            "Do You Want To Delete {} ?".format(self.selected_item), icon='warning')
            if result == 'yes':
                self._cursor.execute("delete from grocerylist where Item_Name='%s'" % (self.selected_item,))
                # commit the database
                self._connection_object.commit()
                # update the GUI window as the item is deleted
                self.search_entry_field.delete(0,'end')
                self.update_window()

    """This method is invoked when the user scrolls on the List boxes"""
    def _on_mouse_wheel(self, event=None):
        self.item_name_listbox.yview("scroll", event.delta, "units")
        self.qty_listbox.yview("scroll", event.delta, "units")
        self.cost_listbox.yview("scroll", event.delta, "units")
        self.expiry_listbox.yview("scroll", event.delta, "units")
        self.item_code_listbox.yview("scroll", event.delta, "units")
        # this prevents default bindings from firing, which
        # would end up scrolling the widget twice
        return "break"

