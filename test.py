import sqlite3 as lite


db = lite.connect("db/database.db")

with db:
    conn = db.cursor()

    conn.execute("DROP TABLE Commodities")
    db.commit()

    conn.execute("CREATE TABLE Commodities (Id int, Name TEXT, Amount int, Price TEXT, ProviderId int)")
    db.commit()

    good = (1, "Moto G7", 100, "100$", 1)

    conn.execute("INSERT INTO Commodities (Id, Name, Amount, Price, ProviderId) VALUES (?, ?, ?, ?, ?)", good)

    db.commit()