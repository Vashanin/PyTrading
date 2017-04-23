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

    def donothing(self):
        print("nothing yet")

    def add_commodity_to_list(self):
        frame = Frame(self.master, width=600, height=500)
        frame.pack(side=TOP)

        self.window_items["list_of_items"].append(frame)

        Label(frame, text="{:>15}".format("Товар"), font=("Courier", 11)).grid(row=4, pady=5)
        commodity_form = ttk.Combobox(frame, font=("Courier", 11), width=45)
        commodity_form['values'] = self.commodity.get_column_from_table_db(column="Name", table="Commodities")
        commodity_form.current(0)
        commodity_form.grid(row=4, column=1, pady=5)

        self.window_items["list_of_entries"].append(commodity_form)

    def summarize_commodity(self):
        try:
            customers = self.customer.get_customers_from_db()
            commodities = self.commodity.get_all_data_from_db()

            customer_phone = self.window_items["customer"].get()

            current_customer = None

            for customer in customers:
                if (customer[2] == customer_phone):
                    current_customer = customer

            commodity_dict = {}
            for commodity in commodities:
                commodity_dict[commodity[1]] = commodity

            sum = 0.0
            goods = []
            for entry in self.window_items["list_of_entries"]:
                product = entry.get()
                goods.append(product)
                sum += commodity_dict[product][3]

            for item in goods:
                self.commodity.edit_commodity_in_db(id=commodity_dict[item][0],
                                                    amount=(commodity_dict[item][2] - 1))
                lst = list(commodity_dict[item])
                lst[2] -= 1
                commodity_dict[item] = tuple(lst)

            self.window_items["customer_frame"].pack_forget()
            self.window_items["customer_tool_bar"].pack_forget()

            for item in self.window_items["list_of_items"]:
                item.pack_forget()

            frame = Frame(self.master)
            Label(self.master, text="Замовлення", font=("Courier", 15)).pack(side=TOP, pady=20)
            frame.pack(side=TOP, pady=10)

            ttk.Separator(frame, orient=HORIZONTAL).grid(row=2, columnspan=5, sticky="ew")

            Label(frame, text="{:>15}".format("Покупець: "), font=("Courier", 11)).grid(row=3, column=0)
            Label(frame, text="{:^45}".format(current_customer[1]), font=("Courier", 11)).grid(row=3, column=1)

            Label(frame, text="{:>15}".format("Номер покупця: "), font=("Courier", 11)).grid(row=4, column=0)
            Label(frame, text="{:^45}".format(current_customer[2]), font=("Courier", 11)).grid(row=4, column=1)

            Label(frame, text="{:>15}".format("Товари: "), font=("Courier", 11)).grid(row=5, column=0)
            Label(frame, text="{:^45}".format(", ".join(goods)), font=("Courier", 11)).grid(row=5, column=1)

            Label(frame, text="{:>15}".format("Вартість: "), font=("Courier", 11)).grid(row=6, column=0)
            Label(frame, text="{:^45}".format(str(sum)+" $"), font=("Courier", 11)).grid(row=6, column=1)
        except Exception as e:
            print("Trouble with summarize_commodity function: " + e.args[0])

    def init_customer_score(self):
        tool_bar = Frame(self.master)

        Button(tool_bar, text="Додати товар", command=self.add_commodity_to_list, font=("Courier", 11)) \
            .pack(side=RIGHT, padx=2, pady=2)
        Button(tool_bar, text="Підсумувати", command=self.summarize_commodity, font=("Courier", 11)) \
            .pack(side=RIGHT, padx=2, pady=2)

        tool_bar.pack(side=TOP, fill=X)

        frame = Frame(self.master)
        frame.pack(side=TOP)
        Label(frame, text="{:>15}".format("Номер покупця"), font=("Courier", 11)).grid(row=3)
        customer_form = ttk.Combobox(frame, font=("Courier", 11), width=45)
        customer_form['values'] = self.customer.get_column_from_table_db(column="Phone", table="Customers")
        customer_form.current(0)
        customer_form.grid(row=3, column=1, pady=20)

        self.window_items["customer_frame"] = frame
        self.window_items["customer_tool_bar"] = tool_bar
        self.window_items["list_of_items"] = []
        self.window_items["list_of_entries"] = []
        self.window_items["customer"] = customer_form

        ttk.Separator(frame, orient=HORIZONTAL).grid(row=4, columnspan=3, sticky="ew")


    def init_provider_score(self):
        return None