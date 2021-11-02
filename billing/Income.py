from datetime import datetime
import time
from tkinter import Tk, Label, Scrollbar, Listbox, Button, N, S, NS, Frame

from common import Values
from database.DBConnection import DBConnection

class DailyIncome:
    def __init__(self):
        self.dbConnection = DBConnection()
        self.dbConnection.use_database()
        self.connect_object = self.dbConnection.get_connection_object()
        self.cur = self.connect_object.cursor()
        self.flag = None
        self.billingsto = None
        self.daily_income_window = None

    def mainmenu(self):
        if self.flag == 'dailyinco':
            self.dbConnection.close_database()
            self.daily_income_window.destroy()

    def on_closing(self):
        self.dbConnection.close_database()
        self.daily_income_window.destroy()

    def get_today_income(self):
        ''' This function will allow us to show today's total income '''
        self.flag = 'dailyinco'
        self.daily_income_window = Tk()
        self.daily_income_window.wm_iconbitmap(Values.BITMAP_IMAGE)
        self.daily_income_window.title("Today's Income")
        self.daily_income_window.geometry("900x400+400+200")
        self.daily_income_window.resizable(0,0)
        self.daily_income_window.protocol("WM_DELETE_WINDOW", self.on_closing)

        frame = Frame(self.daily_income_window)
        frame.propagate(0)
        #display today in words
        today_in_words = str(datetime.now().strftime('%A %d %B %Y'))
        Label(frame, text='Today: ' + today_in_words,pady=20,font=('Arial',12)).grid(row=0, column=1,columnspan=2)

        """We show the total income here in the label"""
        self.cur.execute('select * from bill')
        total = 0.0
        #get today in dd/mm/year format
        today = str(time.localtime()[2]) + '/' + str(time.localtime()[1]) + '/' + str(time.localtime()[0])
        for record in self.cur:
            if record[5] == today:  # record[5] is billing date
                total += float(record[4])  # record[4] is total cost

        Label(frame, width=30, text="Today's Total Income: $ " +
                                  str("{0:.2f}".format(total,)), bg='black', fg='white',font  = ('Arial',15))\
                                         .grid(row=2, column=1,columnspan=2)

        vertical_scrollbar = Scrollbar(frame,orient='vertical')
        listbox1 = Listbox(frame,width=75,yscrollcommand=vertical_scrollbar.set)
        listbox1.grid(row=3,column=1)
        listbox1.config(font=('Arial', 12))

        vertical_scrollbar.config(command=listbox1.yview)
        vertical_scrollbar.grid(row=3,column=2,sticky=NS)

        """We show the bill of each individual here"""
        index = 0
        self.cur.execute('select * from bill')
        for record in self.cur:
            if record[5] == today:  # record[5] is billing date
                index += 1
                # record[4] is total cost for particular bill
                #record[6] is bill number
                listbox1.insert(index, 'Bill No.: ' + record[6] + '    :    $ ' + record[4])
        self.connect_object.commit()
        Label(frame, text=' \n').grid(row=4, column=1, columnspan=2)
        Button(frame, text='Main Menu',width=13,
               font=('Arial',13),command=self.mainmenu)\
            .grid(row=5,padx=20, column=2,columnspan=5)
        frame.pack()
        self.daily_income_window.mainloop()
