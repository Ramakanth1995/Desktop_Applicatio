import os
import win32api
import win32print
import random
import time
from tkinter import Tk, Label, Entry, Button, Scrollbar, Listbox,messagebox
from tkinter import N, S, END, SINGLE, NS
from common import Values
from database.DBConnection import DBConnection

class Billing:
    def __init__(self):
        self.dbConnection = DBConnection()
        self.dbConnection.use_database()
        self.connect_object = self.dbConnection.get_connection_object()
        self.cur = self.connect_object.cursor()
        self.flag = None
        self.lineadd = None
        self.final_price = 0

        #root window = None
        self.billing_window = None
        #list box for storing item names
        self.item_listbox = None
        self.qty_listbox = None
        self.cost_listbox = None
        self.expiry_listbox = None
        self.item_code_listbox = None
        #listbox for adding the items at that bottom
        self.add_bill_listbox = None
        self.added = False
        
        # variable for storing selected item name in the item list box
        self.selected_item_name = None
        #Entry field for searching Item
        self.search_entry_field = None
        #Entry field for quantity
        self.quantity_entry_field = None
        #Entry Field for Name
        self.name_entry_field = None
        #Entry Field for Address
        self.address_entry_field = None
        #Entry field for phone number
        self.phone_entry_field = None
        #Entry field for getting how much customer given the money
        self.amtpaid_entry_field = None

        #list variable for adding names of items to the bill
        self.item_names_list = []
        # list variable for adding item_no of items to the bill
        self.item_no_list = []
        #list variable for adding quantities of the selected item
        self.qty_list = []
        #variable for storing cost of each item
        self.cost_of_items = []
        #variable for storing item_no of the selected item name
        self.item_no = None
        #variable for stroing quantity of selected item
        self.qty_of_selected_item = None

        self.item_list = None

    def clear_listboxes(self):
        # clear the item_list_box field
        self.item_listbox.delete(0, 'end')
        self.qty_listbox.delete(0, 'end')
        self.cost_listbox.delete(0, 'end')
        self.expiry_listbox.delete(0, 'end')
        self.item_code_listbox.delete(0,'end')
        if self.added is False:
            self.add_bill_listbox.delete(0, 'end')

    """This method retrieves all Item Names and stores in a list."""
    def get_items(self):
        if self.item_list == None:
            self.cur.execute("select Item_Name from grocerylist")
            list = self.cur.fetchall()
            self.item_list = []
            # item_list is a list of tuples. So item in the for loop gives tuple everytime
            # take first element of the tuple as every tuple contains only one element
            for item in list:
                self.item_list.append(item[0])

        return self.item_list

    """This method is invoked automatically when the user enters any input in the Entry field"""
    def search_items(self, event=None):
        text = self.search_entry_field.get()
        #clear the listboxes
        self.clear_listboxes()
        # get items of the listboxes
        item_list = self.get_items()
        for item in item_list:
            if text.lower() in item.lower():
                self.item_listbox.insert(END, item)
                self.cur.execute("select"
                                 " (Quantity_Remain),"
                                 "(Item_Cost),"
                                 "(Expiry_Date), "
                                 "(Item_Code)"
                                 "from grocerylist where Item_Name='%s'"%(item,))
                record =self.cur.fetchone()
                # get qty of the item
                self.qty_listbox.insert(END, record[0])
                # get cost of the item and update in the list box
                self.cost_listbox.insert(END, record[1])
                # get expiry date of the item and update in the list box
                self.expiry_listbox.insert(END, record[2])
                # get item code of the item and update in the list box
                self.item_code_listbox.insert(END, record[3])

    def mainmenu(self):
        self.added = False
        self.dbConnection.close_database()
        self.billing_window.destroy()

    def on_closing(self):
        self.mainmenu()

    def billingitems(self):
        ''' Billing GUI '''
        #create root window
        self.billing_window = Tk()
        self.billing_window.title('BILLING')
        self.billing_window.wm_iconbitmap(Values.BITMAP_IMAGE)
        self.billing_window.geometry("1180x650+250+50")
        self.billing_window.resizable(0, 0)
        self.billing_window.protocol("WM_DELETE_WINDOW", self.on_closing)

        Label(self.billing_window,pady=20, text='-' * 150 + 'Billing' + '-' * 130,font=('Arial',10))\
            .grid(row=0, column=0, columnspan=8, sticky='W')
        Label(self.billing_window, text='Enter Name: ',font=('Arial',10))\
            .grid(row=1, column=0)
        self.name_entry_field = Entry(self.billing_window,width=30)
        self.name_entry_field.grid(row=1, column=1,columnspan=2)
        Label(self.billing_window, text='Amount Paid: ', font=('Arial', 10)) \
            .grid(row=1, column=2,columnspan=4)
        self.amtpaid_entry_field = Entry(self.billing_window, width=15)
        self.amtpaid_entry_field.grid(row=1, column=3, columnspan=4)

        Label(self.billing_window, text='Total Amount: ', font=('Arial', 10)) \
            .grid(row=2, column=2, columnspan=4)
        self.total_amount_entry_field = Entry(self.billing_window, width=15)
        self.total_amount_entry_field.grid(row=2, column=3, columnspan=4)

        Label(self.billing_window, text='Enter Address: ',font=('Arial',10))\
            .grid(row=2, column=0)
        self.address_entry_field = Entry(self.billing_window, width=30)
        self.address_entry_field.grid(row=2, column=1, columnspan=2)
        Label(self.billing_window, text='Enter Phone Number: ', font=('Arial', 10)) \
            .grid(row=3, column=0)
        self.phone_entry_field = Entry(self.billing_window, width=30)
        self.phone_entry_field.grid(row=3, column=1, columnspan=2)

        Label(self.billing_window, text='Enter Item Name To Select: ',font=('Arial',10))\
            .grid(row=4, column=0)
        self.search_entry_field = Entry(self.billing_window,width=30)
        self.search_entry_field.grid(row=4, column=1,columnspan=2)
        self.search_entry_field.bind('<KeyRelease>', self.search_items)

        Label(self.billing_window, text='-' * 285,font=('Arial',10))\
            .grid(row=6, column=0, columnspan=8, sticky='W')
        Label(self.billing_window, text='Select Item', relief='ridge', width=15,font=('Arial',10))\
            .grid(row=7, column=0)
        Label(self.billing_window, text='Qty_Remain', relief='ridge', width=10,font=('Arial',10))\
            .grid(row=7, column=1)
        Label(self.billing_window, text='Cost', relief='ridge', width=4,font=('Arial',10))\
            .grid(row=7, column=2)
        Label(self.billing_window, text='Expiry Date', width=10, relief='ridge',font=('Arial',10))\
            .grid(row=7, column=3)
        Label(self.billing_window, text='Item Code', width=10, relief='ridge', font=('Arial', 10)) \
            .grid(row=7, column=4)
        #here column 5 is for scrollbar
        Label(self.billing_window, text='QUANTITY',font=('Arial',10), width=20, relief='ridge')\
            .grid(row=7, column=6)
        self.quantity_entry_field = Entry(self.billing_window)
        self.quantity_entry_field.grid(row=8, column=6)

        Button(self.billing_window, text='Add to bill', font=('Arial', 10), width=15, command=self.addtothebill) \
            .grid(row=8, column=7)

        #refresh_stock the windows
        self.refresh_stock()

        Button(self.billing_window, width=15, text='Main Menu',font=('Arial',10), command=self.mainmenu)\
            .grid(row=1, column=7)
        Button(self.billing_window, width=15, text='Refresh Stock',font=('Arial',10), command=self.refresh_stock)\
            .grid(row=3, column=7)
        Button(self.billing_window, width=15, text='Reset Bill',font=('Arial',10), command=self.resetbill)\
            .grid(row=4, column=7)
        Button(self.billing_window, width=15, text='Print Bill',font=('Arial',10), command=self.printbill)\
            .grid(row=5, column=7)
        Button(self.billing_window, width=15, text='Save Bill',font=('Arial',10), command=self.savebill)\
            .grid(row=7, column=7)
        
        self.billing_window.mainloop()

    def refresh_stock(self):
        ''' Displays all the data from the database '''
        #vertical scroll bar action
        def onvsb(*args):
            self.item_listbox.yview(*args)
            self.qty_listbox.yview(*args)
            self.cost_listbox.yview(*args)
            self.expiry_listbox.yview(*args)
            self.item_code_listbox.yview(*args)

        index = 0
        vsb = Scrollbar(orient='vertical', command=onvsb)
        self.item_listbox = Listbox(self.billing_window, width=25, yscrollcommand=vsb.set,
                                    selectmode=SINGLE, exportselection=False)
        self.item_listbox.grid(row=8, column=0)
        self.item_listbox.config(font=('Arial', 10))
        self.item_listbox.bind('<<ListboxSelect>>', self.get_current_selected_item)

        self.qty_listbox = Listbox(self.billing_window, width=10, yscrollcommand=vsb.set)
        self.qty_listbox.config(font=('Arial', 10))
        self.cost_listbox = Listbox(self.billing_window,width=10, yscrollcommand=vsb.set)
        self.cost_listbox.config(font=('Arial', 10))
        self.expiry_listbox = Listbox(self.billing_window, width=15, yscrollcommand=vsb.set)
        self.expiry_listbox.config(font=('Arial', 10))
        self.item_code_listbox = Listbox(self.billing_window,width=22, yscrollcommand=vsb.set )
        self.item_code_listbox.config(font=('Arial', 10))


        self.qty_listbox.grid(row=8, column=1)
        self.cost_listbox.grid(row=8, column=2)
        self.expiry_listbox.grid(row=8, column=3)
        self.item_code_listbox.grid(row=8, column=4)
        vsb.grid(row=8, column=5, sticky=N + S)

        self.item_listbox.bind('<MouseWheel>', self.onmousewheel)
        self.qty_listbox.bind('<MouseWheel>', self.onmousewheel)
        self.cost_listbox.bind('<MouseWheel>', self.onmousewheel)
        self.expiry_listbox.bind('<MouseWheel>', self.onmousewheel)
        self.item_code_listbox.bind('<MouseWheel>', self.onmousewheel)

        #ADD LIST BOX AT THAT BOTTOM FOR ADDING ITEM TO THE BILL
        Label(self.billing_window, text=' ').grid(row=9, column=0)
        vertical_scrollbar = Scrollbar(self.billing_window, orient='vertical')
        self.add_bill_listbox = Listbox(self.billing_window, width=100, yscrollcommand=vertical_scrollbar.set)
        self.add_bill_listbox.grid(row=10, column=0, padx=70, columnspan=8)
        self.add_bill_listbox.config(font=('Arial', 10))
        #ATTACH SCROLL BAR TO THE LISTBOX
        vertical_scrollbar.config(command=self.add_bill_listbox.yview)
        vertical_scrollbar.grid(row=10, column=1, sticky=NS)

        #add data to the window by retrieving data from the database
        self.cur.execute("select * from grocerylist")
        for record in self.cur:
            index += 1
            self.item_listbox.insert(index, record[1])#record[1] - item_name
            self.qty_listbox.insert(index, record[2]) #record[2] - Quantity Remaining
            self.cost_listbox.insert(index, record[3]) #record[3] - Item_cost
            self.expiry_listbox.insert(index, record[4]) #record[4] - Expiry_Date
            self.item_code_listbox.insert(index, record[7]) #record[7] - Item Code

        self.connect_object.commit()
        self.final_price = 0
        self.total_amount_entry_field.delete(0, 'end')

    # mouse wheel action
    def onmousewheel(self, event=None):
        self.item_listbox.yview('scroll', event.delta, 'units')
        self.qty_listbox.yview('scroll', event.delta, 'units')
        self.cost_listbox.yview('scroll', event.delta, 'units')
        self.expiry_listbox.yview('scroll', event.delta, 'units')
        self.item_code_listbox.yview('scroll', event.delta, 'units')
        return 'break'

    def get_current_selected_item(self,evt):
        self.selected_item_name  = str((self.item_listbox.get(self.item_listbox.curselection())))
        self.search_entry_field.delete(0,'end')
        self.search_entry_field.insert(END, self.selected_item_name)
        # find the selected item no and qty in the database
        self.cur.execute("select "
                         "(Item_No),"
                         "(Quantity_Remain)"
                         " from grocerylist where Item_Name='%s'"%
                     (self.selected_item_name,))
        record = self.cur.fetchone()
        #get item_no from the record
        self.item_no = record[0] #Item_No
        #get item_qty from the record
        self.qty_of_selected_item = int(record[1])
        #print("Item No : {}, Item Qty : {}".format(self.item_no,self.qty_of_selected_item))

    def addtothebill(self):
        ''' Add to bill button which allows to append the data in the bill'''
        #global st, item_names_list, item_name, qty_list, item_no_list, cur, connect_object, sl1
        #self.quantity_entry_field = [''] * 10
        self.added = True
        self.item_no_list.append(self.item_no)
        self.item_names_list.append(self.selected_item_name)
        try:
            #get entered qty of the selected item.
            #check if user entered the qty in correct format
            entered_qty_of_selected_item = int(self.quantity_entry_field.get())
        except:
            messagebox.showerror("Error","Please Enter Valid Qty For The Selected Item")
        else:
            #entered qty cannot be None or zero and also cannot be greater than the total qty of the item
            if (entered_qty_of_selected_item == None) or \
                    (entered_qty_of_selected_item==0) or \
                    (entered_qty_of_selected_item > self.qty_of_selected_item):
                messagebox.showerror("Error","Insufficient Stock\nEntered Quantity Cannot Be Zero or More than Total Quantity.")
            else:
                self.qty_list.append(self.quantity_entry_field.get())
                #get price of the item
                self.cur.execute("select "
                                 "(Item_cost) "
                                 "from grocerylist where Item_No='%s'"%self.item_no,)
                cost = "{0:.2f}".format(float(self.cur.fetchone()[0]),)
                price = (float(cost)*entered_qty_of_selected_item)

                central_gst = (Values.CGST / 100) * price
                state_gst = (Values.SGST / 100) * price
                net_total = "{0:.2f}".format((price+central_gst+state_gst),)
                self.total_amount = net_total
                self.final_price = float(self.total_amount)+float(self.final_price)

                self.total_amount_entry_field.delete(0,'end')
                self.total_amount_entry_field.insert(END,"{0:.2f}".format(float(self.final_price), ))


                #add details to the list box
                price = "{0:.2f}".format(price,)
                self.add_bill_listbox.insert(END,
                    ("Item No: {}    Item Name: {}       Qty: {}     Cost: {}     Price: {}   Total: {}"
                                             .format(self.item_no, self.selected_item_name,
                                             entered_qty_of_selected_item ,cost,price,net_total)))

    def printbill(self):
        if self.added is False:
            #self.add_bill_listbox.delete(0, 'end')
            self.addtothebill()

        self.savebill(True)
        random_int = random.randint(100, 999)
        file = os.getcwd() + '/bill'+ str(random_int)+'.txt'

        open(file, "w").write(self.lineadd)
        win32api.ShellExecute(
            0,
            "print",
            file,
            #
            # If this is None, the default printer will
            # be used anyway.
            #
            '/d:"%s"' % win32print.GetDefaultPrinter(),
            ".",
            0
        )

    def resetbill(self):
        ''' CLears all the textboxes in the bill '''
        self.added = False
        self.item_no_list = []
        self.item_names_list = []
        self.qty_list = []
        self.cost_of_items = []
        self.name_entry_field.delete(0,'end')
        self.address_entry_field.delete(0,'end')
        self.phone_entry_field.delete(0,'end')
        self.amtpaid_entry_field.delete(0,'end')
        self.search_entry_field.delete(0,'end')
        self.quantity_entry_field.delete(0,'end')
        #also refresh the stock
        self.refresh_stock()
        self.final_price = 0
        self.total_amount_entry_field.delete(0, 'end')

    def savebill(self,printbill=None):

        length_of_item_nos = len(self.item_no_list)
        amt_paid = self.amtpaid_entry_field.get()
        #check whether user has added an item to the bill
        if (length_of_item_nos == 0):
            messagebox.showerror("Error","Please add an item to the bill")
        elif(amt_paid == ''):
            messagebox.showerror("Error","Enter Amount Given By The Customer")
        else:
            if self.added is False:
                self.addtothebill()

            entered_user_name = self.name_entry_field.get()
            if entered_user_name == '':
                messagebox.showerror("Error","Please Enter Customer Name")
            entered_user_address = self.address_entry_field.get()
            if entered_user_address == '':
                messagebox.showerror("Error", "Please Enter Customer Address")
            entered_user_phone = self.phone_entry_field.get()
            if entered_user_phone == '':
                messagebox.showerror("Error", "Please Enter Customer Phone")
            elif len(entered_user_phone) >= 11:
                messagebox.showerror("Error","Phone Number Length Cannot Be Greater than 10")

            if(entered_user_phone !='' and len(entered_user_phone) <11
                    and entered_user_address != ''
                    and entered_user_name != ''):
                ''' Create Text File of Bill Format'''
                details = ['', '', '', '', '', '', '', '', '']
                details[2] = str(self.item_no_list)

                details_len = len(details)

                #for index in range(len(self.item_no_list)):
                    #print(self.item_no_list[index], ' ', self.qty_list[index], ' ', self.item_names_list[index])

                total_price = self.get_total_amount(length_of_item_nos)
                # store the cost list into the details last index pos
                details[details_len - 1] = self.cost_of_items
                random_int = str(random.randint(100, 999))
                details[5] = random_int
                # Find total price of the bill
                total = 0.00
                for index in range(20):
                    if total_price[index] != 0.0 and total_price[index] != '':
                        total += float(total_price[index])  # totalling"""

                amt_paid = float(amt_paid)
                central_gst = (Values.CGST / 100) * total
                state_gst = (Values.SGST / 100) * total
                net_total = "{0:.2f}".format(float(total + central_gst + state_gst))
                #check if amount given by the customer is sufficient for the bill amt
                if amt_paid < float(net_total):
                    messagebox.showerror("Error","Amount Paid By Customer Is Insufficent."
                                                 " Total Bill Amount is {}".format(net_total,))
                else:
                    self.lineadd = '\n\n'
                    self.lineadd += "======================================================\n"
                    self.lineadd += "                                  No :%s\n" % details[5]
                    self.lineadd += "          MY GROCERY STORE\n"
                    self.lineadd += "  Bill Details\n\n"
                    self.lineadd += "------------------------------------------------------\n"

                    # get user name and address for the bill

                    self.lineadd += "Name: %s\n" % entered_user_name
                    self.lineadd += "Address: %s\n" % entered_user_address

                    self.lineadd += "------------------------------------------------------\n"
                    self.lineadd += "Product        Cost          Qty.       Price\n"
                    self.lineadd += "------------------------------------------------------\n"

                    details[0] = entered_user_name
                    details[1] = entered_user_address

                    # save the customer details into the database customer table
                    self.cur.execute("insert into customer values('%s','%s','%s')"
                                     % (entered_user_name.lower(),
                                        entered_user_address.lower(),
                                        entered_user_phone))

                    length_of_item_nos = len(self.item_no_list)
                    for index in range(length_of_item_nos):
                        if self.item_names_list[index] != ' ':
                            s1 = ' '
                            s1 = (self.item_names_list[index]) \
                                 + (s1 * (15 - len(self.item_names_list[index]))) + \
                                 details[details_len - 1][index] + \
                                 s1 * (11 - len(self.qty_list[index])) + self.qty_list[index] + \
                                 s1 * (15 - len(str(total_price[index]))) + str(total_price[index]) + '\n'
                            self.lineadd += s1

                    self.lineadd += "\n------------------------------------------------------\n"
                    #format the variables
                    total = "{0:.2f}".format(total, )
                    central_gst = "{0:.2f}".format(central_gst,)
                    state_gst = "{0:.2f}".format(state_gst, )
                    amt_paid = ("{0:.2f}".format(amt_paid,))

                    self.lineadd += 'Total' + (' ' * 30) + \
                                    (' ' * (10 - len(total))) + 'Rs ' + total + '\n'
                    # apply taxes on the bill
                    self.lineadd += 'CGST %' + (' ' * 30) +\
                                    str(Values.CGST) +\
                                    (' ' * (8 - len(total))) +\
                                    'Rs ' + central_gst + '\n'
                    self.lineadd += 'SGST %' + (' ' * 30) +\
                                    str(Values.SGST)+ \
                                    (' ' * (8 - len(total))) + \
                                    'Rs ' + state_gst + '\n'
                    self.lineadd += "------------------------------------------------------\n\n"
                    self.lineadd += 'Net Total' + (' ' * 28) + \
                                    (' ' * (8 - len(net_total))) + 'Rs ' + net_total + '\n'

                    self.lineadd += 'Amount Paid' + (' ' * 25) +\
                                    (' ' * (10 - len(amt_paid))) + 'Rs ' + \
                                    amt_paid + '\n'

                    return_amt = float(amt_paid) - float(net_total)
                    return_amt = ("{0:.2f}".format(return_amt,))
                    self.lineadd += 'Return Amt' + (' ' * 25) +\
                                    (' ' * (10 - len(return_amt))) + 'Rs ' + \
                                    (return_amt) + '\n'

                    self.lineadd += "------------------------------------------------------\n\n"
                    self.lineadd += "Dealer's signature:_________________________________\n"
                    self.lineadd += "======================================================\n"

                    #print(self.lineadd)
                    details[3] = total
                    local_time = time.localtime()
                    details[4] = str(local_time[2]) + '/' + str(local_time[1]) + '/' + str(local_time[0])
                    details[6] = self.lineadd

                    # update the quantity in the database
                    self.update_stock(length_of_item_nos)

                    # save the bill details
                    sql = "Insert into bill (cusname,cusphone,cusaddress,items,totalcost,billingdate,billno,bill) values(%s,%s,%s,%s,%s,%s,%s,%s)"
                    val = (details[0], entered_user_phone, details[1], details[2],
                           details[3], details[4], details[5], str(details[6]))
                    self.cur.execute(sql, val)
                    self.connect_object.commit()
                    if printbill is not True:
                        bill = open('bill_' + random_int + '.txt', 'w')
                        bill.write(self.lineadd)
                        bill.close()
                        messagebox.showinfo("Success", "Bill Is Saved")

                        self.resetbill()
                        self.final_price = 0
                        self.total_amount_entry_field.delete(0, 'end')


    def get_total_amount(self,length_of_item_nos):
        price = [0.0] * 20
        for k in range(length_of_item_nos):
            self.cur.execute("select * from grocerylist where Item_No='%s'" % (self.item_no_list[k],))
            for record in self.cur:
                # find the total price of the item for the selected quantity
                # store the cost of the item
                self.cost_of_items.append("{0:.2f}".format(float(record[3]), ))
                # record[3] - cost of the item
                total_price_of_item = "{:.2f}".format(int(self.qty_list[k]) * float(record[3]))
                price[k] = total_price_of_item
                # print(self.qty_list[k], price[k])
        return price

    def update_stock(self,length_of_item_nos):
        for k in range(length_of_item_nos):
            self.cur.execute("select * from grocerylist where Item_No='%s'" % (self.item_no_list[k],))
            for record in self.cur:
                # update the final qty in the database
                # record[2] -- Remaining Qty
                # qty_list[k] -- Entered qty of the item by the user
                # item_no_list[k] -- Item no of the item selected by the user
                self.cur.execute("update grocerylist set Quantity_Remain='%s' where Item_No='%s'" %
                                 (int(record[2]) - int(self.qty_list[k]), self.item_no_list[k]))
        self.connect_object.commit()

