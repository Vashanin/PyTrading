import sqlite3 as lite


db = lite.connect("db/database.db")

with db:
    conn = db.cursor()

    conn.execute("DROP TABLE OrderedCommodities")

    conn.execute("CREATE TABLE OrderedCommodities (Id int, Name TEXT, Amount int, Price float, ProviderId int)")
    db.commit()

    good = (1, "Moto G7", 100, 100.0, 1)

    conn.execute("INSERT INTO OrderedCommodities (Id, Name, Amount, Price, ProviderId) VALUES (?, ?, ?, ?, ?)", good)

    db.commit()