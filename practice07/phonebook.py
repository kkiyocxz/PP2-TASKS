import psycopg2
import csv
from connect import get_connection

def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            phone VARCHAR(20) NOT NULL UNIQUE
        )
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("Таблица создана!")

def insert_from_csv(filename):
    conn = get_connection()
    cur = conn.cursor()
    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("""
                INSERT INTO phonebook (first_name, phone)
                VALUES (%s, %s)
                ON CONFLICT (phone) DO NOTHING
            """, (row['first_name'], row['phone']))
    conn.commit()
    cur.close()
    conn.close()
    print("Данные из CSV добавлены!")

def insert_from_console():
    name = input("Введи имя: ")
    phone = input("Введи номер телефона: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO phonebook (first_name, phone)
        VALUES (%s, %s)
        ON CONFLICT (phone) DO NOTHING
    """, (name, phone))
    conn.commit()
    cur.close()
    conn.close()
    print("Контакт добавлен!")

def update_contact():
    name = input("Введи имя контакта которого хочешь изменить: ")
    print("1 - изменить имя")
    print("2 - изменить телефон")
    choice = input("Выбери: ")
    conn = get_connection()
    cur = conn.cursor()
    if choice == "1":
        new_name = input("Новое имя: ")
        cur.execute("UPDATE phonebook SET first_name=%s WHERE first_name=%s", (new_name, name))
    elif choice == "2":
        new_phone = input("Новый телефон: ")
        cur.execute("UPDATE phonebook SET phone=%s WHERE first_name=%s", (new_phone, name))
    conn.commit()
    cur.close()
    conn.close()
    print("Контакт обновлён!")

def search_contacts():
    print("1 - поиск по имени")
    print("2 - поиск по номеру")
    choice = input("Выбери: ")
    conn = get_connection()
    cur = conn.cursor()
    if choice == "1":
        name = input("Введи имя: ")
        cur.execute("SELECT * FROM phonebook WHERE first_name ILIKE %s", (f"%{name}%",))
    elif choice == "2":
        phone = input("Введи номер или часть номера: ")
        cur.execute("SELECT * FROM phonebook WHERE phone ILIKE %s", (f"%{phone}%",))
    rows = cur.fetchall()
    for row in rows:
        print(f"ID: {row[0]}, Имя: {row[1]}, Телефон: {row[2]}")
    cur.close()
    conn.close()

def delete_contact():
    print("1 - удалить по имени")
    print("2 - удалить по телефону")
    choice = input("Выбери: ")
    conn = get_connection()
    cur = conn.cursor()
    if choice == "1":
        name = input("Введи имя: ")
        cur.execute("DELETE FROM phonebook WHERE first_name=%s", (name,))
    elif choice == "2":
        phone = input("Введи телефон: ")
        cur.execute("DELETE FROM phonebook WHERE phone=%s", (phone,))
    conn.commit()
    cur.close()
    conn.close()
    print("Контакт удалён!")

def main():
    create_table()
    while True:
        print("\n--- PhoneBook ---")
        print("1 - Загрузить из CSV")
        print("2 - Добавить с консоли")
        print("3 - Обновить контакт")
        print("4 - Найти контакт")
        print("5 - Удалить контакт")
        print("0 - Выход")
        choice = input("Выбери действие: ")
        if choice == "1":
            insert_from_csv("contacts.csv")
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            update_contact()
        elif choice == "4":
            search_contacts()
        elif choice == "5":
            delete_contact()
        elif choice == "0":
            break

if __name__ == "__main__":
    main()