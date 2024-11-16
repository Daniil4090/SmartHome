from flask import Flask, request
import sqlite3
import os
import random

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LETTERS += LETTERS.lower()
LETTERS +="1234567890"

app = Flask(__name__)


def generate_key(a):
    key = ""
    for i in range(a):
        key += random.choice(LETTERS)
    return key


@app.route('/')
def index():
    auth_key = request.args.get("auth_key")
    if auth_key != key:
        print(" * Запрос отклонен.")
        return "Запрос отклонен."
    return 'Приветствуем в нашей панели управления!'


@app.route('/add_device', methods=['post', 'get'])
def add_device():
    auth_key = request.args.get("auth_key")
    if auth_key != key:
        print(" * Запрос отклонен.")
        return "Запрос отклонен."
    device_name = request.args.get("device_name")
    device_address = request.args.get("device_address")
    device_apiKey = request.args.get("device_apiKey")
    device_conf = request.args.get("device_conf")
    print(" ! Запрос на добавление устройства со следующими параметрами:", device_name, device_address, device_apiKey)
    try:
        cur.execute(f"""INSERT INTO Devices (Name, Address, ApiKey) VALUES ("{device_name}", "{device_address}", "{device_apiKey}")""")
        cur.execute("COMMIT")
    except sqlite3.IntegrityError:
        print(" * Устройство уже добавлено в базу данных.")
    device_id = cur.execute(f"""SELECT ID FROM Devices WHERE Address="{device_address}" """).fetchone()[0]
    device_conf_f = open(f"Devices/{device_id}.json", "w+")
    device_conf_f.write(device_conf)
    device_conf_f.close()
    return 'Добавление умного устройства завершено.'


@app.route('/delete_device')
def delete_device():
    auth_key = request.args.get("auth_key")
    if auth_key != key:
        print(" * Запрос отклонен.")
        return "Запрос отклонен."
    device_id = request.args.get("device_id")
    print(f" ! Запрос на удаление устройства под ID: {device_id}.")
    try:
        os.remove(f"Devices/{device_id}.json")
    except FileNotFoundError:
        print(" * Файл устройства уже удален.")
    cur.execute(f"""DELETE FROM Devices WHERE ID={device_id}""")
    cur.execute("""COMMIT""")
    return 'Удаление умного устройства завершено.'


if __name__ == "__main__":
    try:
        print(" * Чтение ключа...")
        config = open("config.txt", "r")
        key = config.read()
        config.close()
        print(" * Выполнено!")
    except FileNotFoundError:
        print(" * Возникла ошибка при чтении. Идет создание конфигурации...")
        key = generate_key(16)
        config = open("config.txt", "w+")
        config.write(key)
        config.close()
        print(" * Выполнено!")
    print(" * Ключ для взаимодействия с панелью:", key)
    print(" ! НИКОМУ НЕ СООБЩАЙТЕ ЭТОТ КЛЮЧ!")
    print(" * Подключение базы данных...")
    con = sqlite3.connect("Devices/HomePanel.db", check_same_thread=False)
    cur = con.cursor()
    print(" * Успешно!")
    print(" * Запуск сервера...")
    app.run(host="0.0.0.0")