from tkinter import *
import tkinter.ttk as ttk
import sqlite3 as lite


class Provider:
    """
        Клас Provider відповідає за вивід на екран усіх дій щодо постачальника.

        Перелік методів:
            self.add_provider - вивід на екран форм для внесення інформації про нового постачальника,
                                та подальше занесення інформації до БД
            self.remove_provider - видалення користувача за id та внесення змін до БД
            self.edit_provider - редагування інформації про вже існуючого в БД користувача з заданим id
            self.init_provider_window - створення тулбару(кнопки додання/редагування/видалення),
                                        виведення існуючих в БД даних у вигляді таблиці
            self.refresh_window - видаляє з екрану форми введення імені/пошти/номеру постачальника,
                                  якщо вони є на екрані
                                  
        Інші методи даного класу створені задля взаємодії з БД. Їх назви говорять самі за себе.
    """

    def __init__(self, master=None):
        # master - це кореневий фрейм, який містить усі інші елементи
        self.master = master

        # до словнику window_items заносяться та зберігаються віджети виведені на екран
        self.window_items = {}

    def add_provider(self):
        try:
            # перед доданням нової форми, попередньо очистимо екран від інших
            self.refresh_window()

            frame = Frame(self.master, width=600, height=200)

            self.window_items["add_provider_frame"] = frame

            name_form = Entry(frame, width=40, font=("Courier", 12))
            email_form = Entry(frame, width=40, font=("Courier", 12))

            def add():
                name = name_form.get()
                email = email_form.get()

                self.add_provider_to_db(name, email)
                frame.pack_forget()

                self.window_items["table_frame"].pack_forget()
                self.window_items["providers_list_header"].pack_forget()
                self.window_items["tool_bar"].pack_forget()

                self.init_provider_window()

            Label(frame, text="Введіть дані постачальника:", font=("Courier", 12)).grid(row=0, column=1)
            Label(frame, text="Назва компанії", font=("Courier", 12)).grid(row=1, column=0)
            name_form.grid(row=1, column=1)
            Label(frame, text="Електронна пошта", font=("Courier", 12)).grid(row=2, column=0)
            email_form.grid(row=2, column=1)
            Button(frame, text="Додати", command=add, font=("Courier", 11)).grid(row=3, column=1)

            frame.pack(side=TOP, pady=15)

        except Exception as e:
            print(e.args)

    def remove_provider(self):
        try:
            # перед доданням нової форми, попередньо очистимо екран від інших
            self.refresh_window()

            frame = Frame(self.master, width=600, height=100, pady=15)

            self.window_items["remove_provider_frame"] = frame

            Label(frame, text="Оберіть номер постачальника для видалення: ", font=("Courier", 12)).grid(row=0, column=0)

            box = ttk.Combobox(frame, font=("Courier", 11))
            box['values'] = self.get_column_from_table_db(column="Id", table="Providers")
            box.current(0)
            box.grid(row=0, column=1)

            def remove():
                self.remove_provider_from_db(box.get())

                frame.pack_forget()
                self.window_items["table_frame"].pack_forget()
                self.window_items["providers_list_header"].pack_forget()
                self.window_items["tool_bar"].pack_forget()
                self.init_provider_window()

            Button(frame, text="Видалити", font=("Courier", 11), command=remove).grid(row=1, column=1)
            frame.pack(side=TOP)

        except Exception as e:
            print(e.args)

    def edit_provider(self):
        try:
            # перед доданням нової форми, попередньо очистимо екран від інших
            self.refresh_window()

            frame = Frame(self.master, width=600, height=100, pady=15)

            self.window_items["edit_provider_frame"] = frame

            Label(frame, text="# ", font=("Courier", 12)).grid(row=0, column=0)

            box = ttk.Combobox(frame, font=("Courier", 11), width=32)
            box['values'] = self.get_column_from_table_db(column="Id", table="Providers")
            box.current(0)
            box.grid(row=0, column=1)

            name_form = Entry(frame, width=30, font=("Courier", 12))
            email_form = Entry(frame, width=30, font=("Courier", 12))

            name_form.insert(0, "без змін")
            email_form.insert(0, "без змін")

            Label(frame, text="Назва компанії", font=("Courier", 12)).grid(row=1, column=0)
            name_form.grid(row=1, column=1)
            Label(frame, text="Електронна пошта", font=("Courier", 12)).grid(row=2, column=0)
            email_form.grid(row=2, column=1)

            def change():
                user_id = box.get()
                user_name = name_form.get()
                user_email = email_form.get()
                self.edit_provider_in_db(user_id, user_name, user_email)

                frame.pack_forget()
                self.window_items["table_frame"].pack_forget()
                self.window_items["providers_list_header"].pack_forget()
                self.window_items["tool_bar"].pack_forget()
                self.init_provider_window()

            Button(frame, text="Змінити", command=change, font=("Courier", 11)).grid(row=3, column=1)

            frame.pack(side=TOP)

        except Exception as e:
            print(e.args)

    def init_provider_window(self):
        try:
            # перед доданням нової форми, попередньо очистимо екран від інших
            self.refresh_window()

            # створюємо toolbar
            tool_bar = Frame(self.master)
            Button(tool_bar, text="Додати постачальника", command=self.add_provider, font=("Courier", 11)) \
                .pack(side=RIGHT, padx=2, pady=2)
            Button(tool_bar, text="Редагувати запис", command=self.edit_provider, font=("Courier", 11)) \
                .pack(side=RIGHT, padx=2, pady=2)
            Button(tool_bar, text="Видалити постачальника", command=self.remove_provider, font=("Courier", 11)) \
                .pack(side=RIGHT, padx=2, pady=2)

            tool_bar.pack(side=TOP, fill=X)

            self.window_items["tool_bar"] = tool_bar;

            # виводимо перелік постачальників з бази данних
            providers = self.get_providers_from_db()

            header = Label(self.master, text="Список постачальників", font=("Courier", 14))
            header.pack(side=TOP)
            self.window_items["providers_list_header"] = header

            # в table_frame вміщується таблиця та колесо прокрутки
            table_frame = Frame(self.master, width="600", height="350")

            canvas = Canvas(table_frame, width="600", height="350")
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

            entity = "{:^7}{:^30}{:^20}".format("#", "Назва компанії", "Електронна пошта")
            Label(frame, text=entity, fg="red", bd=2, bg="lightgrey", font=("Courier", 12)).pack(side=TOP)

            for provider in providers:
                entry = '\n{:^10}{:^37}{:^25}'.format(provider[0], provider[1], provider[2])
                Label(frame, text=entry, bd=1, bg="white", font=("Courier", 10)).pack(side=TOP)

        except Exception as e:
            print(e.args)

    def refresh_window(self):
        if "edit_provider_frame" in self.window_items:
            self.window_items["edit_provider_frame"].pack_forget()

        if "remove_provider_frame" in self.window_items:
            self.window_items["remove_provider_frame"].pack_forget()

        if "add_provider_frame" in self.window_items:
            self.window_items["add_provider_frame"].pack_forget()

    def get_providers_from_db(self, path="db/database.db", table="Providers"):
        try:
            db = lite.connect(path)
            with db:
                conn = db.cursor()
                conn.execute("SELECT * FROM {}".format(table))
                data = conn.fetchall()

                return data

        except Exception as e:
            print(e.args)

    def add_provider_to_db(self, name, email, path="db/database.db", table="Providers"):

        try:
            db = lite.connect(path)
            with db:
                conn = db.cursor()
                id = 1

                try:
                    conn.execute("SELECT MAX(Id) FROM {}".format(table))
                    db.commit()
                    max_id = conn.fetchall()
                    id = max_id[0][0] + 1
                except Exception as e:
                    print("Inserting into empty table: " + table + " new index equals " + str(id))

                user = (id, name, email)
                conn.execute("INSERT INTO {} (Id,Name,Email) VALUES (?,?,?)".format(table), user)

        except Exception as e:
            print(e.args)

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

    def remove_provider_from_db(self, id, table="Providers", path="db/database.db"):
        try:
            db = lite.connect(path)
            with db:
                conn = db.cursor()
                conn.execute("DELETE FROM {} WHERE Id={}".format(table, id))
        except Exception as e:
            print(e.args)

    # в даній функції значення параметру table установлено Providers за замовчуванням,
    # оскільки використовуємо саме ця таблия використовується для збереження інформації про постачальників
    def edit_provider_in_db(self, id, name, email, table="Providers", path="db/database.db"):
        try:
            db = lite.connect(path)
            with db:
                conn = db.cursor()

                conn.execute("SELECT * FROM {} WHERE Id={}".format(table, id))

                if (name == "без змін"):
                    name = conn.fetchall()[0][1]

                if (email == "без змін"):
                    email = conn.fetchall()[0][2]

                conn.execute("UPDATE {} SET Name = '{}', Email = '{}' WHERE Id = {}".format(table, name, email, id))
        except Exception as e:
            print(e.args)


    def __del__(self):
        self.refresh_window()