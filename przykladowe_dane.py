# import sqlite3
#
# conn = sqlite3.connect('gra.db')
# c = conn.cursor()
#
# # Przykładowi użytkownicy
# uzytkownicy = [('kacper', 'haslo123'),
#                ('olek', 'abc123')]
#
# c.executemany('INSERT OR IGNORE INTO uzytkownicy (login, haslo) VALUES (?, ?)', uzytkownicy)
#
# # Przykładowe turnieje krajowe
# turnieje_krajowe = [('Turniej Warszawa', '2025-06-10', 'kacper'),
#                     ('Turniej Kraków', '2025-06-12', 'olek')]
#
# c.executemany('INSERT INTO turnieje_krajowe (nazwa, data, zwyciezca) VALUES (?, ?, ?)', turnieje_krajowe)
#
# # Przykładowe turnieje europejskie
# turnieje_europejskie = [('European Open', 'Niemcy', '2025-07-20', 'kacper'),
#                         ('Champions Cup', 'Francja', '2025-08-15', 'olek')]
#
# c.executemany('INSERT INTO turnieje_europejskie (nazwa, kraj, data, zwyciezca) VALUES (?, ?, ?, ?)', turnieje_europejskie)
#
# conn.commit()
# conn.close()
#
# print("Przykładowe dane dodane pomyślnie.")
