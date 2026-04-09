import psycopg2
from connect import get_connection

def search_contacts(pattern):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_phonebook(%s)", (pattern,))
    rows = cur.fetchall()
    for row in rows:
        print(f"ID: {row[0]}, Имя: {row[1]}, Телефон: {row[2]}")
    cur.close()
    conn.close()

def get_page(limit, offset):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM get_phonebook_page(%s, %s)", (limit, offset))
    rows = cur.fetchall()
    for row in rows:
        print(f"ID: {row[0]}, Имя: {row[1]}, Телефон: {row[2]}")
    cur.close()
    conn.close()

def upsert_contact(name, phone):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
    conn.commit()
    cur.close()
    conn.close()
    print("Контакт добавлен или обновлён!")

def insert_many(contacts):
    import json
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL insert_many_contacts(%s)", (json.dumps(contacts),))
    conn.commit()
    cur.close()
    conn.close()
    print("Контакты добавлены!")

def delete_contact(value):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL delete_contact(%s)", (value,))
    conn.commit()
    cur.close()
    conn.close()
    print("Контакт удалён!")

def main():
    while True:
        print("\n--- PhoneBook Practice8 ---")
        print("1 - Поиск по паттерну")
        print("2 - Показать страницу")
        print("3 - Добавить или обновить контакт")
        print("4 - Массовая вставка")
        print("5 - Удалить контакт")
        print("0 - Выход")
        choice = input("Выбери: ")

        if choice == "1":
            pattern = input("Введи паттерн: ")
            search_contacts(pattern)
        elif choice == "2":
            limit = int(input("Сколько записей: "))
            offset = int(input("С какой позиции: "))
            get_page(limit, offset)
        elif choice == "3":
            name = input("Имя: ")
            phone = input("Телефон: ")
            upsert_contact(name, phone)
        elif choice == "4":
            contacts = []
            n = int(input("Сколько контактов добавить: "))
            for _ in range(n):
                name = input("Имя: ")
                phone = input("Телефон: ")
                contacts.append({"name": name, "phone": phone})
            insert_many(contacts)
        elif choice == "5":
            value = input("Введи имя или телефон: ")
            delete_contact(value)
        elif choice == "0":
            break

if __name__ == "__main__":
    main()