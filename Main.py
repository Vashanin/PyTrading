# !/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Програма взаємодіє з єдиною БД database.db, де є 4 таблиці:
    
    1) Providers 
            (Id int, Name TEXT, Email TEXT) - інформація про поставщиків
    2) OrderedCommodities 
            (Id int, Name TEXT, Amount int, Price float, ProviderId int) - інформація про товари, що очікують поставки
    3) Commodities 
            (Id int, Name TEXT, Amount int, Price float, ProviderId int) - інформація про товари
    4) Customers
            (Id INT, Name TEXT, Phone TEXT) - інформація про покупців

"""

from Window import *
from tkinter import *

# створення вікна, де будуть відбуватися усі подальші дії
root = Tk()
root.geometry("700x600")

# створення об'єкту класу Window з однойменного пакету
app = Window(root)

root.mainloop()