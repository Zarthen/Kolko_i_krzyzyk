import socket
import threading
import random
import sys
import subprocess
from baza import dodaj_punkty

class TicTacToeServer:
    def __init__(self, host='0.0.0.0', port=65436):
        self.HOST = host
        self.PORT = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.nicknames = []

    def start(self):
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.HOST, self.PORT))
        self.server_socket.listen(2)
        print("Oczekiwanie na 2 graczy...")
        self.accept_clients()
        self.run_game()

    def accept_clients(self):
        while len(self.clients) < 2:
            conn, addr = self.server_socket.accept()
            nick = conn.recv(1024).decode().strip()
            print(f"Połączono: {addr}, nick: {nick}")
            self.clients.append(conn)
            self.nicknames.append(nick)

    def pokaz_plansze(self, plansza):
        return "\n".join([" ".join(row) for row in plansza])

    def policz_punkty(self, plansza, symbol):
        punkty = {2: 1, 3: 3, 4: 7, 5: 15}
        wynik = 0

        def licz_grupy(linia):
            suma = 0
            cnt = 0
            for v in linia:
                if v == symbol:
                    cnt += 1
                else:
                    if cnt in punkty:
                        suma += punkty[cnt]
                    cnt = 0
            if cnt in punkty:
                suma += punkty[cnt]
            return suma

        N = len(plansza)
        # Wiersze
        for i in range(N):
            wynik += licz_grupy(plansza[i])
        # Kolumny
        for j in range(N):
            wynik += licz_grupy([plansza[i][j] for i in range(N)])
        # Wszystkie przekątne ↘ (z lewej do prawej)
        for k in range(-N+2, N-1):
            przekatna = [plansza[i][i-k] for i in range(max(k, 0), min(N, N+k))]
            if len(przekatna) >= 2:
                wynik += licz_grupy(przekatna)
        # Wszystkie przekątne ↗ (z lewej do prawej w dół)
        for k in range(1, 2*N-2):
            przekatna = [plansza[i][k-i] for i in range(max(0, k-N+1), min(N, k+1)) if 0 <= k-i < N]
            if len(przekatna) >= 2:
                wynik += licz_grupy(przekatna)
        return wynik

    def czy_koniec(self, plansza):
        return all(plansza[i][j] != '.' for i in range(5) for j in range(5))

    def graj(self):
        plansza = [['.' for _ in range(5)] for _ in range(5)]
        aktualny_symbol = random.choice(['X', 'O'])
        socket_dict = {'X': (self.clients[0], self.nicknames[0]), 'O': (self.clients[1], self.nicknames[1])}

        # Przekazanie symboli
        self.clients[0].sendall(f"X\nSTART:{aktualny_symbol}\n".encode())
        self.clients[1].sendall(f"O\nSTART:{aktualny_symbol}\n".encode())

        running = True
        while running:
            board_str = "PLANSZA\n" + self.pokaz_plansze(plansza) + f"\nTURA:{aktualny_symbol}\n"
            for c in self.clients:
                c.sendall(board_str.encode())
            conn, nick = socket_dict[aktualny_symbol]
            try:
                data = b''
                while not data.endswith(b'\n'):
                    fragment = conn.recv(1024)
                    if not fragment:
                        running = False
                        break
                    data += fragment
                if not data:
                    break
                wiadomosc = data.decode().strip()
                if wiadomosc.startswith("CHAT|"):
                    tresc = wiadomosc.split("|", 1)[1]
                    for k in ['X', 'O']:
                        conn_k, nick_k = socket_dict[k]
                        try:
                            conn_k.sendall(f"CHAT|{nick}: {tresc}\n".encode())
                        except:
                            pass
                    continue
                if wiadomosc.startswith("RUCH "):
                    parts = wiadomosc.split()
                    if len(parts) == 2 and ',' in parts[1]:
                        try:
                            i, j = map(int, parts[1].split(','))
                        except Exception:
                            continue
                        if plansza[i][j] == '.':
                            plansza[i][j] = aktualny_symbol
                            if self.czy_koniec(plansza):
                                px = self.policz_punkty(plansza, 'X')
                                po = self.policz_punkty(plansza, 'O')
                                if px > po:
                                    msg = f"KONIEC\nWygrał gracz {self.nicknames[0]}! Punkty: X={px}, O={po}\n"
                                    dodaj_punkty(nick,5, "online")

                                    #id_turnieju = utworz_turniej_krajowy("Nazwa turnieju", zwyciezca_login)
                                    #zapisz_wynik_krajowy(id_turnieju, login, punkty)  # powtarzaj dla każdego gracza
                                elif po > px:
                                    msg = f"KONIEC\nWygrał gracz {self.nicknames[1]}! Punkty: X={px}, O={po}\n"
                                    dodaj_punkty(nick,5, "online")
                                else:
                                    msg = f"KONIEC\nRemis! Punkty: X={px}, O={po}\n"
                                for c in self.clients:
                                    c.sendall(msg.encode())
                                running = False
                                break
                            else:
                                aktualny_symbol = 'O' if aktualny_symbol == 'X' else 'X'

                                # self.root.destroy()
                                # subprocess.Popen(['python', 'menu.py', self.nick])
                                # sys.exit()

            except Exception as e:
                print("Błąd połączenia:", e)
                break

    def run_game(self):
        self.graj()
        for c in self.clients:
            try:
                c.close()
            except:
                pass
        self.server_socket.close()

if __name__ == "__main__":
    server = TicTacToeServer()
    server.start()
