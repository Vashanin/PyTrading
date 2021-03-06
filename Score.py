from Customer import *
from Provider import *
from Commodity import *
from tkinter import *
import tkinter.ttk as ttk


class Score:
    """
        Клас Score відповідає за операції пов`язані з замовленнями. Тут присутні функції для генерування замовлення
        поставки товарів від провайдерів, та для генерування замовлення для покупця.
        
        Також присутні функції для підтверждення надходження поставки від провайдерів.
        
        Функції:
            
        1)  self.init_customer_score - генерування початкового вікна для користувача, де обирається який товар бажає придбати
                                  покупець
            self.add_commodity_to_list - виведення на екран форми для додання нового товару та дії пов'язані з цим 
            self.summarize_commodity - підтвердження замовлення, генерація 'чеку'
    
    
        2)  self.init_provider_score - генерування початкового вікна, виведення форми для вибору провайдера, у якого
                                       будемо замовляти продукцію
            self.submit_provider - підтвердження вибору провайдера. Тепер можна обирати лише ті товари, які надаються
                                       даним провайдером та зазначені в таблиці Commodities нашої БД
            self.add_commodity_to_provider_order - додання нового товару до замовлення
            self.make_provider_order - підтвердження замовлення
    
        3)  self.init_submit_order - генерування вікна для підтвердження надходження поставок
    """
    def __init__(self, master):
        self.master = master

        self.customer = Customer()
        self.provider = Provider()
        self.commodity = Commodity()

        self.window_items = {}

    # функції для генерування замовлення користувача
    def add_commodity_to_list(self):
        try:
            frame = Frame(self.master, width=600, height=500)
            frame.pack(side=TOP)

            self.window_items["list_of_items"].append(frame)

            Label(frame, text="{:>15}".format("Товар"), font=("Courier", 11)).grid(row=4, pady=5)
            commodity_form = ttk.Combobox(frame, font=("Courier", 11), width=45)
            commodity_form['values'] = self.commodity.get_column_from_table_db(column="Name", table="Commodities")
            commodity_form.current(0)
            commodity_form.grid(row=4, column=1, pady=5)

            self.window_items["list_of_entries"].append(commodity_form)
        except Exception as e:
            print("Troubles with add_commodity_to_list: " + e.args[0])

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
        try:
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
        except Exception as e:
            print("Troubles with init_customer_score: " + e.args[0])

    # функції для генерування замовлення поставки товарів
    def add_commodity_to_provider_order(self):
        try:
            frame = Frame(self.master, width=600, height=500)
            frame.pack(side=TOP, pady=15)

            self.window_items["list_of_provider_items"].append(frame)

            provider_name = self.window_items["provider"].get()
            commodities = self.commodity.get_all_data_from_db()

            available_commodities = []
            for item in commodities:
                if (self.commodity.get_provider_by_id(item[4]) == provider_name):
                    available_commodities.append(item[1])

            commodity_form = ttk.Combobox(frame, font=("Courier", 11), width=45)
            commodity_form['values'] = tuple(available_commodities)
            try:
                commodity_form.current(0)
            except Exception as e:
                raise Exception("Unfortunatelly, this provider hasn't got connected commodities")

            Label(frame, text="{:>15}".format("Товар"), font=("Courier", 11)).grid(row=4, pady=5)
            commodity_form.grid(row=4, column=1, pady=5)

            Label(frame, text="{:>15}".format("Кількість"), font=("Courier", 11)).grid(row=5)
            amount_entry = Entry(frame, width=46, font=("Courier", 11))
            amount_entry.grid(row=5, column=1)

            commodity_info = [commodity_form, amount_entry]


            self.window_items["list_of_provider_items"].append(frame)
            self.window_items["list_of_provider_entries"].append(commodity_info)
        except Exception as e:
            print("Troubles with add_commodity_to_provider_order: " + e.args[0])

    def make_provider_order(self):
        try:
            self.window_items["provider_frame"].pack_forget()
            self.window_items["provider_tool_bar"].pack_forget()
            for item in self.window_items["list_of_provider_items"]:
                item.pack_forget()

            Label(self.master, text="Замовлення надіслано! Очікуйте поставки.\nПідтвердити поставку ви можете в іншому вікні",
                  font=("Courier", 14)).pack(side=TOP)

            commodity_dict = {}
            all_commodities_info = self.commodity.get_all_data_from_db()
            for commodity in all_commodities_info:
                commodity_dict[commodity[1]] = commodity

            for item in self.window_items["list_of_provider_entries"]:
                commodity_name = item[0].get()
                commodity_amount = item[1].get()

                commodity_price = commodity_dict[commodity_name][3]
                provider_id = commodity_dict[commodity_name][4]

                self.commodity.add_commodity_to_db(name=commodity_name, amount=commodity_amount, price=commodity_price,
                                                   providerId=provider_id, table="OrderedCommodities")
        except Exception as e:
            print("Troubles with make_provider_order: " + e.args[0])

    def submit_provider(self):
        try:
            if (not self.provider_is_submited):
                self.window_items["provider_frame"].pack_forget()

                frame = Frame(self.master)
                frame.pack(side=TOP)
                Label(frame, text="{:>15}".format("Постачальник"), font=("Courier", 11))\
                    .grid(row=3)
                Label(frame, text="{:^40}".format(self.window_items["provider"].get()), font=("Courier", 12))\
                    .grid(row=3, column=1, pady=20)
                ttk.Separator(frame, orient=HORIZONTAL).grid(row=4, columnspan=3, sticky="ew")

                self.window_items["provider_frame"] = frame

                self.provider_is_submited = True

            self.add_commodity_to_provider_order()
        except Exception as e:
            print("Troubles with submit_provider: " + e.args[0])

    def init_provider_score(self):
        try:
            tool_bar = Frame(self.master)

            self.provider_is_submited = False

            Button(tool_bar, text="Додати товар", command=self.submit_provider, font=("Courier", 11)) \
                .pack(side=RIGHT, padx=2, pady=2)
            Button(tool_bar, text="Замовити", command=self.make_provider_order, font=("Courier", 11)) \
                .pack(side=RIGHT, padx=2, pady=2)

            tool_bar.pack(side=TOP, fill=X)

            frame = Frame(self.master)
            frame.pack(side=TOP)
            Label(frame, text="{:>15}".format("Постачальник"), font=("Courier", 11)).grid(row=3)
            provider_form = ttk.Combobox(frame, font=("Courier", 11), width=45)

            provider_ids = self.provider.get_column_from_table_db(column="Id", table="Providers")
            providers = []

            for id in provider_ids:
                providers.append(self.commodity.get_provider_by_id(id))

            provider_form['values'] = tuple(providers)
            provider_form.current(0)
            provider_form.grid(row=3, column=1, pady=20)

            self.window_items["provider_frame"] = frame
            self.window_items["provider_tool_bar"] = tool_bar
            self.window_items["list_of_provider_items"] = []
            self.window_items["list_of_provider_entries"] = []
            self.window_items["provider"] = provider_form

            ttk.Separator(frame, orient=HORIZONTAL).grid(row=4, columnspan=3, sticky="ew")
        except Exception as e:
            print("Trouble with init_provider_score: " + e.args[0])

    # функції для підтвердження поставки
    def init_submit_order(self):
        # CREATE TABLE OrderedCommodities (Id int, Name TEXT, Amount int, Price float, ProviderId int)
        try:
            orders = self.commodity.get_all_data_from_db(table="OrderedCommodities")

            header = Label(self.master, text="Список поставок товарів", font=("Courier", 14))
            header.pack(side=TOP)
            self.window_items["orders_list_header"] = header

            # в table_frame вміщується таблиця та колесо прокрутки
            table_frame = Frame(self.master, width="670", height="350")

            canvas = Canvas(table_frame, width="680", height="350")
            canvas.pack(side=LEFT)
            table_frame.pack(side=TOP)

            scrollbar = Scrollbar(table_frame, command=canvas.yview)
            scrollbar.pack(side=LEFT, fill=Y)

            self.window_items["order_table_frame"] = table_frame

            canvas.configure(yscrollcommand=scrollbar.set)

            def on_configure(event):
                canvas.configure(scrollregion=canvas.bbox('all'))

            canvas.bind('<Configure>', on_configure)

            frame = Frame(canvas)
            canvas.create_window((0, 0), window=frame, anchor='nw')

            frame.config(relief=RAISED, bd=3)

            # виведення список товарів, що очікують поставок з таблиці OrderedCommodities
            entity = "{:^4}{:^20}{:^20}{:^10}{:^15}".format("#", "Назва", "Кількість", "Ціна(USD)", "Продавець")
            Label(frame, text=entity, fg="red", bd=2, bg="lightgrey", font=("Courier", 12)).pack(side=TOP)

            for order in orders:
                provider_id = self.commodity.get_provider_by_id(order[4])
                entry = '\n{:^4}{:^25}{:^25}{:^12}{:^20}' \
                    .format(order[0], str(order[1]), str(order[2]), str(order[3]), provider_id)

                Label(frame, text=entry, bd=1, bg="white", font=("Courier", 10)).pack(side=TOP)
            frame.pack(side=TOP)

            submit_frame = Frame(self.master)

            id_for_sumbit = ttk.Combobox(submit_frame, font=("Courier", 12))
            id_for_sumbit['values'] = self.commodity.get_column_from_table_db(column="Id", table="OrderedCommodities")
            id_for_sumbit.current(0)
            id_for_sumbit.grid(row=1, column=0)

            submit_frame.pack(side=TOP, pady=15)
            self.window_items["submit_frame"] = submit_frame

            def submit_order():
                frame.pack_forget()
                self.window_items["order_table_frame"].pack_forget()
                self.window_items["orders_list_header"].pack_forget()
                self.window_items["submit_frame"].pack_forget()

                try:
                    submited_id = id_for_sumbit.get()
                    submited_order = None
                    for order in orders:
                        if int(order[0]) == int(submited_id):
                            submited_order = order
                            self.commodity.remove_commodity_from_db(id=submited_id, table="OrderedCommodities")
                            break

                    name_of_ordered_commodity = submited_order[1]
                    amount_of_ordered_commodity = submited_order[2]

                    commodities = self.commodity.get_all_data_from_db()
                    for commodity in commodities:
                        # якщо співпадають назви продукту, то додаємо зазначену кількість поставленого товару до БД
                        if (commodity[1] == name_of_ordered_commodity):
                            new_amount_of_commodity = commodity[2] + amount_of_ordered_commodity
                            self.commodity.edit_commodity_in_db(id=commodity[0], amount=new_amount_of_commodity)
                            break
                except Exception as e:
                    print("Troubles with submitting order funtion: " + e.args[0])
                self.init_submit_order()

            Button(submit_frame, text="Підтвердити поставку", font=("Courier", 11), command=submit_order).grid(row=1, column=1)
        except Exception as e:
            print("Troubles with init_submit_order: " + e.args[0])