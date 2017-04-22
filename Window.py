from Customer import *
from Provider import *
from Commodity import *
from Score import *

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        self.window_items = {}
        self.init_window()

        self.provider = Provider(self.master)
        self.commodity = Commodity(self.master)
        self.customer = Customer(self.master)
        self.score = Score(self.master)

    def refresh_all(self):
        items = self.master.winfo_children()

        for item in items:
            item.pack_forget()

    def make_customer_score(self):
        self.refresh_all()
        self.score.init_customer_score()

    def make_provider_score(self):
        self.refresh_all()
        self.score.init_provider_score()

    def run_provider(self):
        self.refresh_all()
        self.provider.init_provider_window()

    def run_commodity(self):
        self.refresh_all()
        self.commodity.init_commodity_window()

    def run_customer(self):
        self.refresh_all()
        self.customer.init_customer_window()

    def init_window(self):
        menubar = Menu(self.master)

        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Постачальники", command=self.run_provider)
        filemenu.add_command(label="Товари", command=self.run_commodity)
        filemenu.add_command(label="Покупці", command=self.run_customer)
        filemenu.add_separator()
        filemenu.add_command(label="Створити замовлення постачальнику", command=self.make_provider_score)
        filemenu.add_command(label="Створити рахунок клієнту", command=self.make_customer_score)
        filemenu.add_separator()
        filemenu.add_command(label="Вихід", command=self.client_exit)
        filemenu.config(font=("Courier", 10))

        menubar.add_cascade(label="Менеджер складу", menu=filemenu)
        menubar.config(font=("Courier", 10))
        self.master.config(menu=menubar)

    def client_exit(self):
        exit()