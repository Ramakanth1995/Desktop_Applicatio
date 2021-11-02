import random
from tkinter import Tk, StringVar, END
from tkinter import Label,Entry,Button,Listbox
from tkinter import N,S,LEFT,W
from tkinter import Scrollbar
from tkinter import messagebox
from tkinter.ttk import Combobox
from common import Values, Config as properties
from database.DBConnection import DBConnection


class AddItems:
    def __init__(self):

        self._columns = [
            'Item_No', 'Item_Name','Quantity_Remain','Item_Cost',
            'Expiry_Date', 'Manufactured_By','Item_Type','Item_Code'
        ]
        self._dbConnection = DBConnection()
        self._dbConnection.use_database()
        self._connect_object = self._dbConnection.get_connection_object()
        self._cursor = self._connect_object.cursor()
        self.root = None
        self.top = None
        self.delsto = None
        self.entry_fields = None
        self.flag = None

        """Variables for Updating Stocks"""
        #root window when update button clicked
        self.updatestobutton = None
        #root window when update menu item is clicked
        self.updatesto = None

        self.updateitemno = None
        #combo box for showing the Item_types
        self.item_type_combo = None
        #Entry field
        self.valueupx = None
        #Entry Field
        self.valueupxy = None
        #variable for copying the columns list
        self.entry_cols = None

    """this function gets the id value of from the database 
        and increaments it and shows in the text box
        this can also be done in the database automatically."""
    def auto_increament(self):
        ''' To auto-generate item No '''
        self._cursor.execute("select MAX(Item_No) from grocerylist")
        incval = self._cursor.fetchone()
        incval = incval[0] + 1
        return incval

    def mainmenu(self):
        ''' Main Menu Button '''
        self._dbConnection.close_database()
        self.root.destroy()

    def on_closing(self):
        self.mainmenu()

    def reset(self):
        for entry in self.entry_fields:
            if entry != '':
                entry.delete(0,'end')

    def get_item_types(self):
        item_types = sorted(Values.ITEM_TYPE)
        return item_types

    def add_items(self):
        ''' Stock User GUI here '''
        self.flag = 'sto'
        #take a temporary list of length equal to columns tuple and initiate it with ''
        self.entry_fields = [''] * (len(self._columns)-1)
        #create root window
        self.root = Tk()
        self.root.title('Add Stock')
        self.root.wm_iconbitmap(Values.BITMAP_IMAGE)
        self.root.geometry("1100x550+300+50")
        self.root.resizable(0,0)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        Label(self.root, text='Enter a New Item to the Stock',font=('Arial',12))\
            .grid(row=0, column=0, pady=20, columnspan=2)

        Label(self.root, text='-' * 200)\
            .grid(row=1, column=0, columnspan=7)

        autovalue = self.auto_increament()

        """Add Item No field to the window"""
        Label(self.root, width=20, text=str(self._columns[0]) + '  :', justify=LEFT)\
            .grid(row=3, column=0, sticky=W)
        self.entry_fields[0] = Entry(self.root)
        self.entry_fields[0].grid(row=3, column=1)
        self.entry_fields[0].insert(0, str(autovalue))
        self.entry_fields[0].configure(state='disabled')

        val = 1
        column = 1
        row = 4

        #take a copy of the colmns list
        self.entry_cols = self._columns.copy()
        self.entry_cols.remove('Item_Type')
        self.entry_cols.remove('Item_Code')

        #create Entry fields in the GUI window
        for index in range(1,len(self.entry_cols)):
            Label(self.root, width=20, text=str(self.entry_cols[column]) + '  :', justify=LEFT) \
                .grid(row=row, column=0, sticky=W)
            self.entry_fields[val] = Entry(self.root)
            self.entry_fields[val].grid(row=row, column=1)

            column = column + 1
            row = row +1
            val = val + 1

        """Add Item_Type Combobox Menu """
        self.item_type_combo = StringVar(self.root)
        item_types = self.get_item_types()
        Label(self.root, width=20, text=str('Item Type') + '  :', justify=LEFT) \
            .grid(row=row, column=0, sticky=W)
        options = Combobox(self.root, textvariable=self.item_type_combo,
                           values=item_types)
        options.grid(row = row,column = 1)
        options.config(width = 17)

        self.refresh()

        Label(self.root, text=' ').grid(row=11, column=0, columnspan=7)
        #submit button
        Button(self.root, width=15, text='Submit', command=self.submit_items).grid(row=12, column=1)
        # "------" text
        Label(self.root, text='-' * 200).grid(row=13, column=0, columnspan=7)

        #Refresh Button
        Button(self.root, width=25, text='Refresh add_items', command=self.refresh).grid(row=12, column=4)

        for index in range(1, len(self._columns)):
            Label(self.root, text=self._columns[index]).grid(row=14, column=index - 1)

        Button(self.root, width=10, text='Main Menu', command=self.mainmenu).grid(row=12, column=5)
        self.root.mainloop()

    """This function refreshes all the List boxes and fetches the data and sets them"""
    def refresh(self):
        ''' Multilistbox to show all the data in database '''
        listboxes = ['']*7

        def scrollbarv(*args):
            for listbox in listboxes:
                listbox.yview(*args)

        """This method is invoked when the user scrolls on the List boxes"""
        def on_mouse_wheel(event=None):
            for listbox in listboxes:
                listbox.yview("scroll", event.delta, "units")
            # this prevents default bindings from firing, which
            # would end up scrolling the widget twice
            return "break"

        sc_bar = Scrollbar(orient='vertical', command=scrollbarv)

        for listboxIndex in range(7):
            listboxes[listboxIndex] = Listbox(self.root,
                                              yscrollcommand=sc_bar.set,
                                              width=23)
            listboxes[listboxIndex].grid(row=15,column=listboxIndex)
            listboxes[listboxIndex].bind("<MouseWheel>", on_mouse_wheel)

        sc_bar.grid(row=15, column=listboxIndex+1, sticky=N + S)

        self._cursor.execute("select * from grocerylist")
        index = 1
        for record in self._cursor:
            recordIndex = 1
            for listbox in listboxes:
                listbox.insert(index,str(record[recordIndex]))
                index = index + 1
                recordIndex = recordIndex + 1
        self._connect_object.commit()

    def submit_items(self):
        ''' Add new Stock Item '''
        database_fields = [''] * (len(self.entry_cols))

        self._cursor.execute("select * from grocerylist")

        for record in self._cursor:
            itemNo = self.auto_increament() #Item_No

        for index in range(1, len(self.entry_cols)):
            #get values of the Entry fields entered by the user in the GUI
            database_fields[index] = self.entry_fields[index].get()

        #last column is Item_Code. So add a unique number to the Entry
        #depending on the Item_type and disable it.
        item_type = self.item_type_combo.get()
        item_Code = self.generate_random_code(item_type)

        sql = "insert into grocerylist values('%s','%s','%s','%s','%s','%s','%s','%s')"\
              % (itemNo,   #Item_No
                 database_fields[1],#Item_Name
                 database_fields[2], #Qty Remain
                 "{0:.2f}".format(float(database_fields[3]),), #Item_Cost
                 database_fields[4], #Expiry Date
                 database_fields[5], #Manufactured By
                 item_type,#Item_type
                 item_Code) #Item_code

        #insert the values into the database
        self._cursor.execute(sql)
        #self.cursor.execute("select * from grocerylist")
        self._connect_object.commit()

        messagebox.showinfo("Confirm","Item Added")
        #refresh_stock the list boxes
        self.refresh()
        self.reset()

    """Generate a random 10 digit code"""
    @staticmethod
    def generate_random_code(item_type):
        num = random.randint(1000000000,
                             int(properties.get_setting(section=Values.GENERAL_SECTION,
                                                               key=Values.ITEM_CODE_MAX_RANGE)) )
        return (item_type[:5] + '-' + str(num))
