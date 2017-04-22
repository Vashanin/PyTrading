from Customer import *
from Provider import *
from Commodity import *
from tkinter import *
import tkinter.ttk as ttk


class Score:
    def __init__(self, master):
        self.master = master

        self.customer = Customer()
        self.provider = Provider()
        self.commodity = Commodity()

        self.window_items = {}

    def init_customer_score(self):
        frame = Frame(self.master, width=600, height=500)
        frame.pack(side=TOP)

        Label(frame, text="Оберіть наступні данні для формування рахунку", font=("Courier", 14)).grid(row=1, column=1)

        self.window_items["customer_score_frame"] = frame

        Label(frame, text="{:>15}".format("Номер покупця"), font=("Courier", 11)).grid(row=3)
        customer_form = ttk.Combobox(frame, font=("Courier", 11), width=32)
        customer_form['values'] = self.customer.get_column_from_table_db(column="Phone", table="Customers")
        customer_form.current(0)
        customer_form.grid(row=3, column=1)

        Label(frame, text="{:>15}".format("Товар"), font=("Courier", 11)).grid(row=4)
        customer_form = ttk.Combobox(frame, font=("Courier", 11), width=32)
        customer_form['values'] = self.commodity.get_column_from_table_db(column="Name", table="Commodities")
        customer_form.current(0)
        customer_form.grid(row=4, column=1)


    def init_provider_score(self):
        return None