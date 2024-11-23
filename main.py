from flask import Flask, request, render_template
import sqlite3
import os
import random
import json

app = Flask(__name__)


@app.route('/')
def index():
    auth_key = request.args.get("auth_key")
    if auth_key != key:
        print(" * Запрос отклонен.")
        return "Запрос отклонен."
    devices = cur.execute("""SELECT ID, Name FROM Devices""").fetchall()
    return render_template("Hello.html", devices=devices)


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
    device_conf_f.write(json.dumps(json.loads(device_conf), sort_keys=True, indent=4))
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


@app.route('/get_device/<dev_id>')
def get_device(dev_id):
    return dev_id


if __name__ == "__main__":
    print(" * Чтение ключа...")
    try:
        config = open("config.txt", "r")
        key = config.read()
        config.close()
        print(" * Выполнено!")
    except FileNotFoundError:
        print(" * Возникла ошибка при чтении ключа, запустите программу инициализацию.")
        exit()
    print(" * Ключ для взаимодействия с панелью:", key)
    print(" ! НИКОМУ НЕ СООБЩАЙТЕ ЭТОТ КЛЮЧ!")
    print(" * Подключение базы данных...")
    try:
        con = sqlite3.connect("Devices/HomePanel.db", check_same_thread=False)
    except FileNotFoundError:
        print(" * Возникла ошибка при подключении базы данных, запустите программу инициализацию.")
        exit()
    cur = con.cursor()
    print(" * Успешно!")
    print(" * Запуск сервера...")
    app.run(host="0.0.0.0")