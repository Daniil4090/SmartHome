import sqlite3
import random
import os

SYMBOLS = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890"

print("Идет инициализация...")
print("Создание базы данных...")
db_file = open("Devices/HomePanel.db", "x")
db = sqlite3.connect("Devices/HomePanel.db")
dbcur = db.cursor()
dbcur.execute("""CREATE TABLE Devices (
    ID      INTEGER PRIMARY KEY
                    UNIQUE
                    NOT NULL,
    Name    TEXT    NOT NULL,
    Address TEXT    UNIQUE
                    NOT NULL,
    ApiKey  TEXT    NOT NULL
);""")
print("Создание файла конфигурации...")
config = open("config.txt", "w+")
key = ""
for i in range(16):
    key += random.choice(SYMBOLS)
config.write(key)
print("Теперь вы можете запустить панель!")