# # import secrets
# # import time
# # import mysql.connector
# #
# # class BazaUzytkownikow:
# #
# #     def get_conn(self):
# #         return mysql.connector.connect(
# #             host="localhost",
# #             user="root",
# #             password="",
# #             database="kik"
# #         )
# #
# #     def inicjalizuj_baze(self):
# #         conn = self.get_conn()
# #         c = conn.cursor()
# #         c.execute('''
# #                   CREATE TABLE IF NOT EXISTS uzytkownicy
# #                   (id INT AUTO_INCREMENT PRIMARY KEY,
# #                       login VARCHAR (255) UNIQUE,
# #                       haslo VARCHAR(255),
# #                       email VARCHAR(255) UNIQUE,
# #                       zespol VARCHAR(255)
# #                       )
# #                   ''')
# #         c.execute('''
# #             CREATE TABLE IF NOT EXISTS resety (
# #                 id INT AUTO_INCREMENT PRIMARY KEY,
# #                 login VARCHAR(255),
# #                 token VARCHAR(255),
# #                 data_czas INT
# #             )
# #         ''')
# #         conn.commit()
# #         conn.close()
# #
# #     def dodaj_uzytkownika(self, login, haslo, email, zespol):
# #         conn = self.get_conn()
# #         c = conn.cursor()
# #         try:
# #             c.execute("INSERT INTO uzytkownicy (login, haslo, email, zespol) VALUES (%s, %s, %s, %s)",
# #                       (login, haslo, email, zespol))
# #             conn.commit()
# #             return True
# #         except mysql.connector.IntegrityError:
# #             return False
# #         finally:
# #             conn.close()
# #
# #     def znajdz_email(self, login_or_email):
# #         conn = self.get_conn()
# #         c = conn.cursor()
# #         c.execute("SELECT email FROM uzytkownicy WHERE login=%s OR email=%s", (login_or_email, login_or_email))
# #         row = c.fetchone()
# #         conn.close()
# #         return row[0] if row else None
# #
# #     def generuj_token_reset(self, login_or_email):
# #         token = secrets.token_hex(4)
# #         conn = self.get_conn()
# #         c = conn.cursor()
# #         c.execute("SELECT login FROM uzytkownicy WHERE login=%s OR email=%s", (login_or_email, login_or_email))
# #         row = c.fetchone()
# #         if not row:
# #             conn.close()
# #             return None
# #         login = row[0]
# #         c.execute("INSERT INTO resety (login, token, data_czas) VALUES (%s, %s, %s)",
# #                   (login, token, int(time.time())))
# #         conn.commit()
# #         conn.close()
# #         return token
# #
# #     def ustaw_nowe_haslo(self, login_or_email, token, nowe_haslo):
# #         conn = self.get_conn()
# #         c = conn.cursor()
# #         # sprawdzamy token z ostatnich 10 minut
# #         c.execute("SELECT login FROM resety WHERE token=%s AND data_czas >= %s", (token, int(time.time()) - 600))
# #         row = c.fetchone()
# #         if not row:
# #             conn.close()
# #             return False
# #         login = row[0]
# #         c.execute("UPDATE uzytkownicy SET haslo=%s WHERE login=%s", (nowe_haslo, login))
# #         conn.commit()
# #         conn.close()
# #         return True
# #
# #     def dodaj_punkty(self, login, punkty, tryb="turniej"):
# #         conn = self.get_conn()
# #         c = conn.cursor()
# #         if tryb == "turniej":
# #             c.execute("UPDATE uzytkownicy SET punkty_turniej = IFNULL(punkty_turniej, 0) + %s WHERE login = %s", (punkty, login))
# #         elif tryb == "online":
# #             c.execute("UPDATE uzytkownicy SET punkty_online = IFNULL(punkty_online, 0) + %s WHERE login = %s", (punkty, login))
# #         elif tryb == "lokalna":
# #             c.execute("UPDATE uzytkownicy SET punkty_lokalne = IFNULL(punkty_lokalne, 0) + %s WHERE login = %s", (punkty, login))
# #         else:
# #             c.execute("UPDATE uzytkownicy SET punkty = IFNULL(punkty, 0) + %s WHERE login = %s", (punkty, login))
# #         conn.commit()
# #         conn.close()
# #
# #     # def pobierz_punkty(login, tryb="lokalne"):
# #     #     conn = mysql.connector.connect(
# #     #         host="localhost",
# #     #         user="root",
# #     #         password="",
# #     #         database="kik"
# #     #     )
# #     #     c = conn.cursor()
# #     #     if tryb == "lokalne":
# #     #         c.execute("SELECT punkty_lokalne FROM uzytkownicy WHERE login=%s", (login,))
# #     #         row = c.fetchone()
# #     #         conn.close()
# #     #         return row[0] if row else 0
# #     #     elif tryb == "online":
# #     #         c.execute("SELECT SUM(punkty) FROM wyniki_krajowe WHERE login=%s", (login,))
# #     #         row = c.fetchone()
# #     #         conn.close()
# #     #         return row[0] if row and row[0] else 0
# #     #     elif tryb == "turniej":
# #     #         c.execute("SELECT SUM(punkty) FROM wyniki_europejskie WHERE login=%s", (login,))
# #     #         row = c.fetchone()
# #     #         conn.close()
# #     #         return row[0] if row and row[0] else 0
# #     #     else:
# #     #         conn.close()
# #     #         return 0
# #
# #     def pobierz_punkty(self,login, tryb="lokalne"):
# #         conn = self.get_conn()
# #         c = conn.cursor()
# #         if tryb == "lokalne":
# #             c.execute("SELECT punkty_lokalne FROM uzytkownicy WHERE login=%s", (login,))
# #             row = c.fetchone()
# #             conn.close()
# #             return row[0] if row and row[0] is not None else 0
# #         elif tryb == "online":
# #             # Suma punktów ze wszystkich krajowych turniejów
# #             c.execute("SELECT IFNULL(SUM(punkty),0) FROM wyniki_krajowe WHERE login=%s", (login,))
# #             row = c.fetchone()
# #             conn.close()
# #             return row[0] if row and row[0] is not None else 0
# #         elif tryb == "turniej":
# #             # Suma punktów ze wszystkich europejskich turniejów
# #             c.execute("SELECT IFNULL(SUM(punkty),0) FROM wyniki_europejskie WHERE login=%s", (login,))
# #             row = c.fetchone()
# #             conn.close()
# #             return row[0] if row and row[0] is not None else 0
# #         else:
# #             conn.close()
# #             return 0
# #
# #     def dodaj_punkty_lokalne(self,login, punkty):
# #         conn = self.get_conn()
# #         c = conn.cursor()
# #         c.execute("UPDATE uzytkownicy SET punkty_lokalne = IFNULL(punkty_lokalne,0) + %s WHERE login=%s",(punkty, login))
# #         conn.commit()
# #         conn.close()
# #
# #     def zapisz_wynik_krajowy(self, id_turnieju, login, punkty):
# #         conn = self.get_conn()
# #         c = conn.cursor()
# #         c.execute("INSERT INTO wyniki_krajowe (id_turnieju, login, punkty) VALUES (%s, %s, %s)",(id_turnieju, login, punkty))
# #         conn.commit()
# #         conn.close()
# #
# #     def zapisz_wynik_europejski(self, id_turnieju, login, punkty):
# #         conn = self.get_conn()
# #         c = conn.cursor()
# #         c.execute("INSERT INTO wyniki_europejskie (id_turnieju, login, punkty) VALUES (%s, %s, %s)",(id_turnieju, login, punkty))
# #         conn.commit()
# #         conn.close()
# #
# #     def utworz_turniej_krajowy(self, nazwa, zwyciezca):
# #         conn = self.get_conn()
# #         c = conn.cursor()
# #         c.execute("INSERT INTO turnieje_krajowe (nazwa, data, zwyciezca) VALUES (%s, NOW(), %s)", (nazwa, zwyciezca))
# #         id_turnieju = c.lastrowid
# #         conn.commit()
# #         conn.close()
# #         return id_turnieju
# #
# #     def utworz_turniej_europejski(self, nazwa, zwyciezca):
# #         conn = self.get_conn()
# #         c = conn.cursor()
# #         c.execute("INSERT INTO turnieje_europejskie (nazwa, data, zwyciezca) VALUES (%s, NOW(), %s)",
# #                   (nazwa, zwyciezca))
# #         id_turnieju = c.lastrowid
# #         conn.commit()
# #         conn.close()
# #         return id_turnieju
# #
# #     def utworz_turniej_krajowy(nazwa, data, opis=""):
# #         conn = baza.get_conn()
# #         c = conn.cursor()
# #         c.execute("""
# #                   INSERT INTO turnieje_krajowe (nazwa, data, opis)
# #                   VALUES (%s, %s, %s)
# #                   """, (nazwa, data, opis))
# #         conn.commit()
# #         conn.close()
# #
# #     def zapisz_wynik_krajowy(login, punkty, turniej_id):
# #         conn = baza.get_conn()
# #         c = conn.cursor()
# #         c.execute("""
# #                   INSERT INTO wyniki_krajowe (login, punkty, turniej_id)
# #                   VALUES (%s, %s, %s)
# #                   """, (login, punkty, turniej_id))
# #         conn.commit()
# #         conn.close()
# #
# #
# # # Przykład użycia globalnego obiektu:
# # baza = BazaUzytkownikow()
# # baza.inicjalizuj_baze()
# # def inicjalizuj_baze(): return baza.inicjalizuj_baze()
# # def dodaj_uzytkownika(login, haslo, email, zespol): return baza.dodaj_uzytkownika(login, haslo, email, zespol)
# # def znajdz_email(login_or_email): return baza.znajdz_email(login_or_email)
# # def generuj_token_reset(login_or_email): return baza.generuj_token_reset(login_or_email)
# # def ustaw_nowe_haslo(login_or_email, token, nowe_haslo): return baza.ustaw_nowe_haslo(login_or_email, token, nowe_haslo)
# # def pobierz_punkty(login, tryb): return baza.pobierz_punkty(login, tryb)
# # def dodaj_punkty_lokalne(login, punkty): return baza.dodaj_punkty_lokalne(login, punkty)
#
# import mysql.connector
# import secrets
# import time
#
# class BazaUzytkownikow:
#     def __init__(self):
#         self.KRAJOWY_ID = 1  # ID aktywnego turnieju krajowego
#         self.EUROPEJSKI_ID = 1  # ID aktywnego turnieju europejskiego
#         self.inicjalizuj_baze()
#
#     def get_conn(self):
#         return mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="",    # <-- uzupełnij jeśli masz hasło
#             database="kik"
#         )
#
#     def inicjalizuj_baze(self):
#         conn = self.get_conn()
#         c = conn.cursor()
#         # Tabela użytkownicy (z punkty_lokalne)
#         c.execute('''
#             CREATE TABLE IF NOT EXISTS uzytkownicy (
#                 id INT AUTO_INCREMENT PRIMARY KEY,
#                 login VARCHAR(255) UNIQUE,
#                 haslo VARCHAR(255),
#                 email VARCHAR(255) UNIQUE,
#                 zespol VARCHAR(255),
#                 punkty_lokalne INT DEFAULT 0
#             )
#         ''')
#         # Wyniki krajowe
#         c.execute('''
#             CREATE TABLE IF NOT EXISTS wyniki_turnieje_krajowe (
#                 id INT AUTO_INCREMENT PRIMARY KEY,
#                 id_turnieju INT,
#                 login VARCHAR(255),
#                 punkty INT,
#                 UNIQUE(id_turnieju, login),
#                 FOREIGN KEY (login) REFERENCES uzytkownicy(login)
#             )
#         ''')
#         # Wyniki europejskie
#         c.execute('''
#             CREATE TABLE IF NOT EXISTS wyniki_turnieje_europejskie (
#                 id INT AUTO_INCREMENT PRIMARY KEY,
#                 id_turnieju INT,
#                 login VARCHAR(255),
#                 punkty INT,
#                 UNIQUE(id_turnieju, login),
#                 FOREIGN KEY (login) REFERENCES uzytkownicy(login)
#             )
#         ''')
#         # Dla reszty funkcji (reset hasła, itp.) możesz zostawić swoje stare tabele...
#         conn.commit()
#         conn.close()
#
#     ### --- Funkcje do punktacji --- ###
#
#     def dodaj_punkty_lokalne(self, login, punkty):
#         conn = self.get_conn()
#         c = conn.cursor()
#         c.execute(
#             "UPDATE uzytkownicy SET punkty_lokalne = IFNULL(punkty_lokalne, 0) + %s WHERE login = %s",
#             (punkty, login)
#         )
#         conn.commit()
#         conn.close()
#
#     def dodaj_punkty_online(self, login, punkty):
#         """Aktualizuje punkty w JEDNYM turnieju krajowym (ID=1)."""
#         conn = self.get_conn()
#         c = conn.cursor()
#         # Czy już jest wynik dla tego loginu?
#         c.execute(
#             "SELECT punkty FROM wyniki_turnieje_krajowe WHERE id_turnieju=%s AND login=%s",
#             (self.KRAJOWY_ID, login)
#         )
#         wynik = c.fetchone()
#         if wynik:
#             c.execute(
#                 "UPDATE wyniki_turnieje_krajowe SET punkty = punkty + %s WHERE id_turnieju=%s AND login=%s",
#                 (punkty, self.KRAJOWY_ID, login)
#             )
#         else:
#             c.execute(
#                 "INSERT INTO wyniki_turnieje_krajowe (id_turnieju, login, punkty) VALUES (%s, %s, %s)",
#                 (self.KRAJOWY_ID, login, punkty)
#             )
#         conn.commit()
#         conn.close()
#
#     def dodaj_punkty_turniejowe(self, login, punkty):
#         """Aktualizuje punkty w JEDNYM turnieju europejskim (ID=1)."""
#         conn = self.get_conn()
#         c = conn.cursor()
#         c.execute(
#             "SELECT punkty FROM wyniki_turnieje_europejskie WHERE id_turnieju=%s AND login=%s",
#             (self.EUROPEJSKI_ID, login)
#         )
#         wynik = c.fetchone()
#         if wynik:
#             c.execute(
#                 "UPDATE wyniki_turnieje_europejskie SET punkty = punkty + %s WHERE id_turnieju=%s AND login=%s",
#                 (punkty, self.EUROPEJSKI_ID, login)
#             )
#         else:
#             c.execute(
#                 "INSERT INTO wyniki_turnieje_europejskie (id_turnieju, login, punkty) VALUES (%s, %s, %s)",
#                 (self.EUROPEJSKI_ID, login, punkty)
#             )
#         conn.commit()
#         conn.close()
#
#     # def pobierz_punkty(self, login, tryb="lokalne"):
#     #     if tryb == "lokalne":
#     #         return self.pobierz_punkty_lokalne(login)
#     #     elif tryb == "online":
#     #         return self.pobierz_punkty_online(login)
#     #     elif tryb == "turniej":
#     #         return self.pobierz_punkty_turniejowe(login)
#     #     else:
#     #         return 0
#
#     def pobierz_punkty(self, login, tryb="lokalne"):
#         conn = self.get_conn()
#         c = conn.cursor()
#         # Najpierw pobierz user_id dla danego loginu
#         c.execute("SELECT id FROM uzytkownicy WHERE login=%s", (login,))
#         row = c.fetchone()
#         if not row:
#             conn.close()
#             return 0
#         user_id = row[0]
#         if tryb == "lokalne":
#             c.execute("SELECT punkty_lokalne FROM uzytkownicy WHERE id=%s", (user_id,))
#             row = c.fetchone()
#             conn.close()
#             return row[0] if row else 0
#         elif tryb == "online":
#             c.execute("SELECT SUM(punkty) FROM turnieje_krajowe WHERE user_id=%s", (user_id,))
#             row = c.fetchone()
#             conn.close()
#             return row[0] if row and row[0] is not None else 0
#         elif tryb == "turniej":
#             c.execute("SELECT SUM(punkty) FROM turnieje_europejskie WHERE user_id=%s", (user_id,))
#             row = c.fetchone()
#             conn.close()
#             return row[0] if row and row[0] is not None else 0
#         else:
#             conn.close()
#             return 0
#
#     def pobierz_punkty_lokalne(self, login):
#         conn = self.get_conn()
#         c = conn.cursor()
#         c.execute(
#             "SELECT IFNULL(punkty_lokalne,0) FROM uzytkownicy WHERE login=%s", (login,)
#         )
#         wynik = c.fetchone()
#         conn.close()
#         return wynik[0] if wynik else 0
#
#     def pobierz_punkty_online(self, login):
#         conn = self.get_conn()
#         c = conn.cursor()
#         c.execute(
#             "SELECT IFNULL(punkty,0) FROM wyniki_turnieje_krajowe WHERE id_turnieju=%s AND login=%s",
#             (self.KRAJOWY_ID, login)
#         )
#         wynik = c.fetchone()
#         conn.close()
#         return wynik[0] if wynik else 0
#
#     def pobierz_punkty_turniejowe(self, login):
#         conn = self.get_conn()
#         c = conn.cursor()
#         c.execute(
#             "SELECT IFNULL(punkty,0) FROM wyniki_turnieje_europejskie WHERE id_turnieju=%s AND login=%s",
#             (self.EUROPEJSKI_ID, login)
#         )
#         wynik = c.fetchone()
#         conn.close()
#         return wynik[0] if wynik else 0
#
#     ### --- Logika użytkowników/rejestracja --- ###
#     def dodaj_uzytkownika(self, login, haslo, email, zespol):
#         conn = self.get_conn()
#         c = conn.cursor()
#         try:
#             c.execute(
#                 "INSERT INTO uzytkownicy (login, haslo, email, zespol) VALUES (%s, %s, %s, %s)",
#                 (login, haslo, email, zespol)
#             )
#             conn.commit()
#             return True
#         except mysql.connector.IntegrityError:
#             return False
#         finally:
#             conn.close()
#
#     def znajdz_email(self, login_or_email):
#         conn = self.get_conn()
#         c = conn.cursor()
#         c.execute(
#             "SELECT email FROM uzytkownicy WHERE login=%s OR email=%s",
#             (login_or_email, login_or_email)
#         )
#         row = c.fetchone()
#         conn.close()
#         return row[0] if row else None
#
#     # --- Reset hasła (jeśli korzystasz z tej funkcji) ---
#     # Uzupełnij swoimi kodami jeśli chcesz obsługę resetowania
#     def generuj_token_reset(login_or_email):
#         token = secrets.token_hex(4)
#         conn = baza.get_conn()
#         c = conn.cursor()
#         c.execute("SELECT login FROM uzytkownicy WHERE login=%s OR email=%s", (login_or_email, login_or_email))
#         row = c.fetchone()
#         if not row:
#             conn.close()
#             return None
#         login = row[0]
#         c.execute(
#             "CREATE TABLE IF NOT EXISTS resety (id INT AUTO_INCREMENT PRIMARY KEY, login VARCHAR(255), token VARCHAR(255), data_czas INT)"
#         )
#         c.execute(
#             "INSERT INTO resety (login, token, data_czas) VALUES (%s, %s, %s)",
#             (login, token, int(time.time()))
#         )
#         conn.commit()
#         conn.close()
#         return token
#
#     def ustaw_nowe_haslo(login_or_email, token, nowe_haslo):
#         conn = baza.get_conn()
#         c = conn.cursor()
#         # sprawdzamy token z ostatnich 10 minut
#         c.execute(
#             "SELECT login FROM resety WHERE token=%s AND data_czas >= %s",
#             (token, int(time.time()) - 600)
#         )
#         row = c.fetchone()
#         if not row:
#             conn.close()
#             return False
#         login = row[0]
#         c.execute("UPDATE uzytkownicy SET haslo=%s WHERE login=%s", (nowe_haslo, login))
#         conn.commit()
#         conn.close()
#         return True
# # --- Globalny obiekt i funkcje stylu proceduralnego ---
#
# baza = BazaUzytkownikow()
# def inicjalizuj_baze(): return baza.inicjalizuj_baze()
# def dodaj_uzytkownika(login, haslo, email, zespol): return baza.dodaj_uzytkownika(login, haslo, email, zespol)
# def znajdz_email(login_or_email): return baza.znajdz_email(login_or_email)
# def dodaj_punkty(login, punkty, tryb="lokalne"):
#     if tryb == "lokalne":
#         return baza.dodaj_punkty_lokalne(login, punkty)
#     elif tryb == "online":
#         return baza.dodaj_punkty_online(login, punkty)
#     elif tryb == "turniej":
#         return baza.dodaj_punkty_turniejowe(login, punkty)
#     else:
#         return None
# def pobierz_punkty(login, tryb="lokalne"): return baza.pobierz_punkty(login, tryb)
# def pobierz_punkty(login, tryb="online"): return baza.pobierz_punkty(login, tryb)
# def pobierz_punkty(login, tryb="turniej"): return baza.pobierz_punkty(login, tryb)
# # (na końcu, pod aliasami)
# # ...
# def generuj_token_reset(login_or_email): return generuj_token_reset(login_or_email)
# def ustaw_nowe_haslo(login_or_email, token, nowe_haslo): return ustaw_nowe_haslo(login_or_email, token, nowe_haslo)
#

import mysql.connector
import secrets
import time

class BazaUzytkownikow:
    def __init__(self):
        self.KRAJOWY_ID = 1
        self.EUROPEJSKI_ID = 1
        self.inicjalizuj_baze()

    def get_conn(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",    # <-- uzupełnij jeśli masz hasło
            database="kik"
        )

    def inicjalizuj_baze(self):
        conn = self.get_conn()
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS uzytkownicy (
                id INT AUTO_INCREMENT PRIMARY KEY,
                login VARCHAR(255) UNIQUE,
                haslo VARCHAR(255),
                email VARCHAR(255) UNIQUE,
                zespol VARCHAR(255),
                punkty_lokalne INT DEFAULT 0
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS wyniki_turnieje_krajowe (
                id INT AUTO_INCREMENT PRIMARY KEY,
                id_turnieju INT,
                login VARCHAR(255),
                punkty INT,
                UNIQUE(id_turnieju, login),
                FOREIGN KEY (login) REFERENCES uzytkownicy(login)
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS wyniki_turnieje_europejskie (
                id INT AUTO_INCREMENT PRIMARY KEY,
                id_turnieju INT,
                login VARCHAR(255),
                punkty INT,
                UNIQUE(id_turnieju, login),
                FOREIGN KEY (login) REFERENCES uzytkownicy(login)
            )
        ''')
        conn.commit()
        conn.close()

    ### --- Funkcje do punktacji --- ###

    def dodaj_punkty_lokalne(self, login, punkty):
        conn = self.get_conn()
        c = conn.cursor()
        c.execute(
            "UPDATE uzytkownicy SET punkty_lokalne = IFNULL(punkty_lokalne, 0) + %s WHERE login = %s",
            (punkty, login)
        )
        conn.commit()
        conn.close()

    def dodaj_punkty_online(self, login, punkty):
        conn = self.get_conn()
        c = conn.cursor()
        c.execute(
            "SELECT punkty FROM wyniki_turnieje_krajowe WHERE id_turnieju=%s AND login=%s",
            (self.KRAJOWY_ID, login)
        )
        wynik = c.fetchone()
        if wynik:
            c.execute(
                "UPDATE wyniki_turnieje_krajowe SET punkty = punkty + %s WHERE id_turnieju=%s AND login=%s",
                (punkty, self.KRAJOWY_ID, login)
            )
        else:
            c.execute(
                "INSERT INTO wyniki_turnieje_krajowe (id_turnieju, login, punkty) VALUES (%s, %s, %s)",
                (self.KRAJOWY_ID, login, punkty)
            )
        conn.commit()
        conn.close()

    def dodaj_punkty_turniejowe(self, login, punkty):
        conn = self.get_conn()
        c = conn.cursor()
        c.execute(
            "SELECT punkty FROM wyniki_turnieje_europejskie WHERE id_turnieju=%s AND login=%s",
            (self.EUROPEJSKI_ID, login)
        )
        wynik = c.fetchone()
        if wynik:
            c.execute(
                "UPDATE wyniki_turnieje_europejskie SET punkty = punkty + %s WHERE id_turnieju=%s AND login=%s",
                (punkty, self.EUROPEJSKI_ID, login)
            )
        else:
            c.execute(
                "INSERT INTO wyniki_turnieje_europejskie (id_turnieju, login, punkty) VALUES (%s, %s, %s)",
                (self.EUROPEJSKI_ID, login, punkty)
            )
        conn.commit()
        conn.close()

    def pobierz_punkty(self, login, tryb="lokalne"):
        conn = self.get_conn()
        c = conn.cursor()
        if tryb == "lokalne":
            c.execute("SELECT IFNULL(punkty_lokalne,0) FROM uzytkownicy WHERE login=%s", (login,))
            row = c.fetchone()
            conn.close()
            return row[0] if row else 0
        elif tryb == "online":
            c.execute("SELECT IFNULL(punkty,0) FROM wyniki_turnieje_krajowe WHERE id_turnieju=%s AND login=%s", (self.KRAJOWY_ID, login))
            row = c.fetchone()
            conn.close()
            return row[0] if row else 0
        elif tryb == "turniej":
            c.execute("SELECT IFNULL(punkty,0) FROM wyniki_turnieje_europejskie WHERE id_turnieju=%s AND login=%s", (self.EUROPEJSKI_ID, login))
            row = c.fetchone()
            conn.close()
            return row[0] if row else 0
        else:
            conn.close()
            return 0

    ### --- Logika użytkowników/rejestracja --- ###

    def dodaj_uzytkownika(self, login, haslo, email, zespol):
        conn = self.get_conn()
        c = conn.cursor()
        try:
            c.execute(
                "INSERT INTO uzytkownicy (login, haslo, email, zespol) VALUES (%s, %s, %s, %s)",
                (login, haslo, email, zespol)
            )
            conn.commit()
            return True
        except mysql.connector.IntegrityError:
            return False
        finally:
            conn.close()

    def znajdz_email(self, login_or_email):
        conn = self.get_conn()
        c = conn.cursor()
        c.execute(
            "SELECT email FROM uzytkownicy WHERE login=%s OR email=%s",
            (login_or_email, login_or_email)
        )
        row = c.fetchone()
        conn.close()
        return row[0] if row else None

    def generuj_token_reset(self, login_or_email):
        return baza.generuj_token_reset(login_or_email)

# --- Globalny obiekt i funkcje proceduralne ---
baza = BazaUzytkownikow()
def inicjalizuj_baze(): return baza.inicjalizuj_baze()
def dodaj_uzytkownika(login, haslo, email, zespol): return baza.dodaj_uzytkownika(login, haslo, email, zespol)
def znajdz_email(login_or_email): return baza.znajdz_email(login_or_email)
def dodaj_punkty(login, punkty, tryb="lokalne"):
    if tryb == "lokalne":
        return baza.dodaj_punkty_lokalne(login, punkty)
    elif tryb == "online":
        return baza.dodaj_punkty_online(login, punkty)
    elif tryb == "turniej":
        return baza.dodaj_punkty_turniejowe(login, punkty)
    else:
        return None
def pobierz_punkty(login, tryb="lokalne"): return baza.pobierz_punkty(login, tryb)
# ... po klasie BazaUzytkownikow i stworzeniu instancji baza = BazaUzytkownikow() ...
def generuj_token_reset(login_or_email): return baza.generuj_token_reset(login_or_email)
def ustaw_nowe_haslo(login_or_email, token, nowe_haslo): return baza.ustaw_nowe_haslo(login_or_email, token, nowe_haslo)
