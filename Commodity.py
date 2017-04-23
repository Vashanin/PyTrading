from tkinter import *
import tkinter.ttk as ttk
import sqlite3 as lite


class Commodity:
    """
        Клас Сommodity відповідає за вивід на екран усіх дій щодо товару.

        Перелік методів:
            self.add_commodity - вивід на екран форм для внесення інформації про новий товар,
                                та подальше занесення інформації до БД
            self.remove_commodity - видалення товару за id та внесення змін до БД
            self.edit_commodity - редагування інформації про вже існуючого в БД товара з заданим id
            self.init_commodity_window - створення тулбару(кнопки додання/редагування/видалення),
                                         виведення існуючих в БД даних у вигляді таблиці
            self.refresh_window - видаляє з екрану форми введення імені/телефону/номеру користувача,
                                  якщо вони є на екрані

        Інші визначені методи пов'язані з взаємодією з БД. Назви говорять самі за себе.
    """

    def __init__(self, master=None):
        # master - це кореневий фрейм, який містить усі інші елементи
        self.master = master

        # до словнику window_items заносяться та зберігаються віджети виведені на екран
        self.window_items = {}

    def add_commodity(self):
        try:
            # перед доданням нової форми, попередньо очистимо екран від інших
            self.refresh_window()

            frame = Frame(self.master, width=600, height=200)

            self.window_items["add_commodity_frame"] = frame

            name_form = Entry(frame, width=40, font=("Courier", 12))
            description_form = Entry(frame, width=40, font=("Courier", 12))
            price_form = Entry(frame, width=40, font=("Courier", 12))

            # при доданні товару, постачальник має обиратися з вже існуючого списку: необхідно отримати ці дані з БД
            providers_data = self.get_all_data_from_db(table="Providers")

            dict_of_providers = {}
            for providers in providers_data:
                dict_of_providers[providers[0]] = providers[1]

            provider_form = ttk.Combobox(frame, font=("Courier", 11), width=43)
            provider_form['values'] = tuple(dict_of_providers.values())
            provider_form.current(0)

            def add():
                name = name_form.get()
                description = description_form.get()
                price = price_form.get()

                provider_id = 0
                for key in dict_of_providers:
                    if (dict_of_providers[key] == provider_form.get()):
                        provider_id = key
                        break

                self.add_commodity_to_db(name, description, price, provider_id)
                frame.pack_forget()

                self.window_items["table_frame"].pack_forget()
                self.window_items["commodities_list_header"].pack_forget()
                self.window_items["tool_bar"].pack_forget()

                self.init_commodity_window()

            Label(frame, text="Введіть дані товару:", font=("Courier", 12)).grid(row=0, column=1)

            Label(frame, text="{:>12}".format("Назва"), font=("Courier", 12)).grid(row=1, column=0)
            name_form.grid(row=1, column=1)

            Label(frame, text="{:>12}".format("Кількість"), font=("Courier", 12)).grid(row=2, column=0)
            description_form.grid(row=2, column=1)

            Label(frame, text="{:>12}".format("Ціна(USD)"), font=("Courier", 12)).grid(row=3, column=0)
            price_form.grid(row=3, column=1)

            Label(frame, text="{:>12}".format("Постачальник"), font=("Courier", 12)).grid(row=4, column=0)
            provider_form.grid(row=4, column=1)

            Button(frame, text="Додати", command=add, font=("Courier", 11)).grid(row=5, column=1)

            frame.pack(side=TOP, pady=15)

        except Exception as e:
            print("Troubles with add_commodity method: " + e.args[0])

    def remove_commodity(self):
        try:
            # перед доданням нової форми, попередньо очистимо екран від інших
            self.refresh_window()

            frame = Frame(self.master, width=600, height=100, pady=15)

            self.window_items["remove_commodity_frame"] = frame

            Label(frame, text="Оберіть номер товару для видалення: ", font=("Courier", 12)).grid(row=0, column=0)

            box = ttk.Combobox(frame, font=("Courier", 11))
            box['values'] = self.get_column_from_table_db(column="Id", table="Commodities")
            box.current(0)
            box.grid(row=0, column=1)

            def remove():
                self.remove_commodity_from_db(box.get())

                frame.pack_forget()
                self.window_items["table_frame"].pack_forget()
                self.window_items["commodities_list_header"].pack_forget()
                self.window_items["tool_bar"].pack_forget()
                self.init_commodity_window()

            Button(frame, text="Видалити", font=("Courier", 11), command=remove).grid(row=1, column=1)
            frame.pack(side=TOP)

        except Exception as e:
            print("Troubles with remove commodities method: " + e.args[0])

    def edit_commodity(self):
        try:
            # перед доданням нової форми, попередньо очистимо екран від інших
            self.refresh_window()

            frame = Frame(self.master, width=600, height=100, pady=15)

            self.window_items["edit_commodity_frame"] = frame

            Label(frame, text="{:>12}".format("#"), font=("Courier", 12)).grid(row=0, column=0)

            box = ttk.Combobox(frame, font=("Courier", 11), width=43)
            box['values'] = self.get_column_from_table_db(column="Id", table="Commodities")
            box.current(0)
            box.grid(row=0, column=1)

            name_form = Entry(frame, width=40, font=("Courier", 12))
            name_form.insert(0, "без змін")
            description_form = Entry(frame, width=40, font=("Courier", 12))
            description_form.insert(0, "без змін")
            price_form = Entry(frame, width=40, font=("Courier", 12))
            price_form.insert(0, "без змін")

            # при доданні товару, постачальник має обиратися з вже існуючого списку: необхідно отримати ці дані з БД
            providers_data = self.get_all_data_from_db(table="Providers")

            list_of_providers = {0 : "без змін"}
            for providers in providers_data:
                list_of_providers[providers[0]] = providers[1]

            provider_form = ttk.Combobox(frame, font=("Courier", 11), width=43)
            provider_form['values'] = tuple(list_of_providers.values())
            provider_form.current(0)

            Label(frame, text="{:>12}".format("Назва"), font=("Courier", 12)).grid(row=1, column=0)
            name_form.grid(row=1, column=1)

            Label(frame, text="{:>12}".format("Кількість"), font=("Courier", 12)).grid(row=2, column=0)
            description_form.grid(row=2, column=1)

            Label(frame, text="{:>12}".format("Ціна(USD)"), font=("Courier", 12)).grid(row=3, column=0)
            price_form.grid(row=3, column=1)

            Label(frame, text="{:>12}".format("Постачальник"), font=("Courier", 12)).grid(row=4, column=0)
            provider_form.grid(row=4, column=1)

            def change():
                id = box.get()
                name = name_form.get()
                description = description_form.get()
                price = price_form.get()
                provider_id = 0

                for key in list_of_providers:
                    if list_of_providers[key] == provider_form.get():
                        provider_id = key
                        break

                self.edit_commodity_in_db(id, name, description, price, provider_id)
                frame.pack_forget()

                self.window_items["table_frame"].pack_forget()
                self.window_items["commodities_list_header"].pack_forget()
                self.window_items["tool_bar"].pack_forget()

                self.init_commodity_window()

            Button(frame, text="Змінити", command=change, font=("Courier", 11)).grid(row=5, column=1)

            frame.pack(side=TOP)

        except Exception as e:
            print("Troubles with edit_commodity method: " + e.args[0])

    def init_commodity_window(self):
        try:
            # перед доданням нової форми, попередньо очистимо екран від інших
            self.refresh_window()

            # створюємо toolbar
            tool_bar = Frame(self.master)
            Button(tool_bar, text="Додати товар", command=self.add_commodity, font=("Courier", 11)) \
                .pack(side=RIGHT, padx=2, pady=2)
            Button(tool_bar, text="Редагувати запис", command=self.edit_commodity, font=("Courier", 11)) \
                .pack(side=RIGHT, padx=2, pady=2)
            Button(tool_bar, text="Видалити товар", command=self.remove_commodity, font=("Courier", 11)) \
                .pack(side=RIGHT, padx=2, pady=2)

            tool_bar.pack(side=TOP, fill=X)

            self.window_items["tool_bar"] = tool_bar

            # виводимо перелік покупців з бази данних
            commodities = self.get_all_data_from_db()

            header = Label(self.master, text="Список товарів", font=("Courier", 14))
            header.pack(side=TOP)
            self.window_items["commodities_list_header"] = header

            # в table_frame вміщується таблиця та колесо прокрутки
            table_frame = Frame(self.master, width="670", height="350")

            canvas = Canvas(table_frame, width="680", height="350")
            canvas.pack(side=LEFT)
            table_frame.pack(side=TOP)

            scrollbar = Scrollbar(table_frame, command=canvas.yview)
            scrollbar.pack(side=LEFT, fill=Y)

            self.window_items["table_frame"] = table_frame

            canvas.configure(yscrollcommand=scrollbar.set)

            def on_configure(event):
                canvas.configure(scrollregion=canvas.bbox('all'))

            canvas.bind('<Configure>', on_configure)

            frame = Frame(canvas)
            canvas.create_window((0, 0), window=frame, anchor='nw')

            frame.config(relief=RAISED, bd=3)

            entity = "{:^4}{:^20}{:^20}{:^10}{:^15}".format("#", "Назва", "Кількість", "Ціна(USD)", "Продавець")
            Label(frame, text=entity, fg="red", bd=2, bg="lightgrey", font=("Courier", 12)).pack(side=TOP)

            for commodity in commodities:
                provider_id = self.get_provider_by_id(commodity[4])
                entry = '\n{:^4}{:^25}{:^25}{:^12}{:^20}'\
                    .format(commodity[0], str(commodity[1]), str(commodity[2]), str(commodity[3]), provider_id)

                Label(frame, text=entry, bd=1, bg="white", font=("Courier", 10)).pack(side=TOP)

        except Exception as e:
            print("Troubles with init_commodities_window: " + e.args[0])

    def refresh_window(self):
        if "edit_commodity_frame" in self.window_items:
            self.window_items["edit_commodity_frame"].pack_forget()

        if "remove_commodity_frame" in self.window_items:
            self.window_items["remove_commodity_frame"].pack_forget()

        if "add_commodity_frame" in self.window_items:
            self.window_items["add_commodity_frame"].pack_forget()

    def get_all_data_from_db(self, path="db/database.db", table="Commodities"):
        try:
            db = lite.connect(path)
            with db:
                conn = db.cursor()
                conn.execute("SELECT * FROM {}".format(table))
                data = conn.fetchall()

                return data

        except Exception as e:
            print("Troubles with get_all_data_from_db funcion: " + e.args[0])

    def get_provider_by_id(self, id, path="db/database.db", table="Providers"):
        try:
            all_data_in_providers_db = self.get_all_data_from_db(path=path, table=table)

            list_of_providers = {}
            for provider in all_data_in_providers_db:
                list_of_providers[provider[0]] = provider[1]

            return list_of_providers[id]
        except Exception as e:
            print("Troubles with get_provider_by_id method: " + e.args[0])

    def remove_commodity_from_db(self, id, table="Commodities", path="db/database.db"):
        try:
            db = lite.connect(path)
            with db:
                conn = db.cursor()
                conn.execute("DELETE FROM {} WHERE Id={}".format(table, id))
        except Exception as e:
            print(e.args)

    def edit_commodity_in_db(self, id, name="без змін", amount="без змін", price="без змін", providerId=0, table="Commodities", path="db/database.db"):
        try:
            db = lite.connect(path)
            with db:
                conn = db.cursor()

                conn.execute("SELECT * FROM {} WHERE Id={}".format(table, id))

                responce = conn.fetchall()

                if (name == "без змін"):
                    name = responce[0][1]

                if (amount == "без змін"):
                    amount = responce[0][2]

                if (price == "без змін"):
                    price = responce[0][3]

                if (providerId == 0):
                    providerId = responce[0][4]

                conn.execute(
                    "UPDATE {} SET Name = '{}', Amount = '{}', Price = '{}', ProviderId = '{}' WHERE Id = {}"
                        .format(table, name, amount, price, providerId, id)
                )
        except Exception as e:
            print("Troubles with edit_commodity_in_db: " + e.args[0])

    def get_column_from_table_db(self, column, table, path="db/database.db"):
        try:
            db = lite.connect(path)
            with db:
                conn = db.cursor()
                conn.execute("SELECT {} FROM {}".format(column, table))
                db.commit()

                content = ()

                for raw in conn.fetchall():
                    content += (raw[0],)

                return content
        except Exception as e:
            print(e.args)

    def add_commodity_to_db(self, name, description, price, providerId, path="db/database.db", table="Commodities"):

        try:
            db = lite.connect(path)
            with db:
                conn = db.cursor()
                conn.execute("SELECT MAX(Id) FROM {}".format(table))
                db.commit()

                max_id = conn.fetchall()
                user = (max_id[0][0] + 1, name, description, price, providerId)

                conn.execute(
                    "INSERT INTO {} (Id, Name, Amount, Price, ProviderId) VALUES (?,?,?,?,?)".format(table), user
                )

        except Exception as e:
            print(e.args)

    def __del__(self):
        self.refresh_window()