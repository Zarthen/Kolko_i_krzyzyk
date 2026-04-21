# import mysql.connector
# import sys
#
# conn = mysql.connector.connect(host="localhost", user="root", password="", database="kik")
# c = conn.cursor()
# print("Użytkownicy:")
# c.execute("SELECT * FROM uzytkownicy")
# for row in c.fetchall():
#     print(row)
# conn.close()
#
# try:
#     conn = mysql.connector.connect(host="localhost", user="root", password="", database="kik")
#     print("Połączono z bazą MySQL!")
# except mysql.connector.Error as err:
#     print("Błąd połączenia:", err)
#     exit(1)
#
# c = conn.cursor()
#
# print("Użytkownicy:")
# c.execute('SELECT * FROM uzytkownicy')
# for row in c.fetchall():
#     print(row)
#
# def print_table(cursor, table_name):
#     print(f"\n{table_name.capitalize()}:")
#     c = cursor
#     # Pobierz nazwy kolumn
#     c.execute(f'PRAGMA table_info({table_name})')
#     columns = [desc[1] for desc in c.fetchall()]
#     # Pobierz wszystkie dane
#     c.execute(f'SELECT * FROM {table_name}')
#     rows = c.fetchall()
#     # Wypisz nagłówki
#     print(" | ".join(columns))
#     print("-" * (len(columns)*15))
#     # Wypisz dane
#     for row in rows:
#         print(" | ".join(str(x) for x in row))
#     print()
#
# conn = mysql.connector.connect('gra.db.sql')
# c = conn.cursor()
#
# for table in ['uzytkownicy', 'turnieje_krajowe', 'turnieje_europejskie']:
#     print_table(c, table)
#
# conn.close()

import mysql.connector

def print_table(cursor, table_name):
    print(f"\n{table_name.capitalize()}:")
    # Pobierz nazwy kolumn
    cursor.execute(f"DESCRIBE {table_name}")
    columns = [desc[0] for desc in cursor.fetchall()]
    # Pobierz wszystkie dane
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    # Wypisz nagłówki
    print(" | ".join(columns))
    print("-" * (len(columns)*15))
    # Wypisz dane
    for row in rows:
        print(" | ".join(str(x) for x in row))
    print()

try:
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="kik")
    print("Połączono z bazą MySQL!")
except mysql.connector.Error as err:
    print("Błąd połączenia:", err)
    exit(1)

c = conn.cursor()

c.execute("SELECT DATABASE()")
db_name = c.fetchone()[0]
print(f"\nDane są pobierane z bazy: {db_name}\n")

# for table in ['uzytkownicy', 'turnieje_krajowe', 'turnieje_europejskie']:
#     print_table(c, table)
#
# conn.close()

for table in ['uzytkownicy', 'turnieje_krajowe', 'turnieje_europejskie']:
    print(f"Wyświetlanie tabeli: {table} (baza: {db_name})")
    c.execute(f"DESCRIBE {table}")
    columns = [desc[0] for desc in c.fetchall()]
    c.execute(f"SELECT * FROM {table}")
    rows = c.fetchall()
    print(" | ".join(columns))
    print("-" * (len(columns)*15))
    for row in rows:
        print(" | ".join(str(x) for x in row))
    print()

conn.close()