import socket
import threading
import random
import sys
from baza import dodaj_punkty

print("Wywołano serwer_turniejowy.py z argumentami:", sys.argv)

class TicTacToeTournamentServer:
    def __init__(self, host='0.0.0.0', port=65436, ilosc_graczy=0):
        self.HOST = host
        self.PORT = port
        self.ILOSC_GRACZY = ilosc_graczy
        self.gracze = []
        self.nicki = []
        self.wszyscy_gracze = []
        self.start_server()
        print("Serwer startuje na ilość graczy:", ilosc_graczy)

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
        for i in range(N):
            wynik += licz_grupy(plansza[i])
        for j in range(N):
            wynik += licz_grupy([plansza[i][j] for i in range(N)])
        for k in range(-N+2, N-1):
            przekatna = [plansza[i][i-k] for i in range(max(k,0), min(N,N+k))]
            if len(przekatna) >= 2:
                wynik += licz_grupy(przekatna)
        for k in range(1, 2*N-2):
            przekatna = [plansza[i][k-i] for i in range(max(0, k-N+1), min(N, k+1)) if 0 <= k-i < N]
            if len(przekatna) >= 2:
                wynik += licz_grupy(przekatna)
        return wynik

    def czy_koniec(self, plansza):
        return all(plansza[i][j] != '.' for i in range(5) for j in range(5))

    def losuj_pary(self, lista):
        lista = list(lista)
        random.shuffle(lista)
        return [(lista[i], lista[i+1]) for i in range(0, len(lista), 2)]

    def graj_pojedynek(self, conn1, nick1, conn2, nick2):
        while True:
            plansza = [['.' for _ in range(5)] for _ in range(5)]
            aktualny_symbol = random.choice(['X', 'O'])
            socket_dict = {'X': (conn1, nick1), 'O': (conn2, nick2)}
            try:
                conn1.sendall(f"X\nSTART:{aktualny_symbol}\n".encode())
                conn2.sendall(f"O\nSTART:{aktualny_symbol}\n".encode())
            except:
                return None, None, None, (nick1, nick2)
            running = True
            while running:
                board_str = "PLANSZA\n" + self.pokaz_plansze(plansza) + f"\nTURA:{aktualny_symbol}\n"
                for c in [conn1, conn2]:
                    try:
                        c.sendall(board_str.encode())
                    except:
                        running = False
                        break
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
                                        winner = 'X'
                                        wygrany_nick = nick1 if winner == 'X' else nick2
                                        przegrany_nick = nick2 if winner == 'X' else nick1
                                        msg = f"KONIEC\nWygrał gracz {wygrany_nick}! Punkty: X={px}, O={po}\n"
                                        for c in [conn1, conn2]:
                                            try:
                                                c.sendall(msg.encode())
                                            except:
                                                pass
                                        return winner, wygrany_nick, przegrany_nick, (nick1, nick2)
                                    elif po > px:
                                        winner = 'O'
                                        wygrany_nick = nick2 if winner == 'O' else nick1
                                        przegrany_nick = nick1 if winner == 'O' else nick2
                                        msg = f"KONIEC\nWygrał gracz {wygrany_nick}! Punkty: X={px}, O={po}\n"
                                        for c in [conn1, conn2]:
                                            try:
                                                c.sendall(msg.encode())
                                            except:
                                                pass
                                        return winner, wygrany_nick, przegrany_nick, (nick1, nick2)
                                    else:
                                        msg = f"KONIEC\nRemis! Punkty: X={px}, O={po}\n"
                                        for c in [conn1, conn2]:
                                            try:
                                                c.sendall(msg.encode())
                                            except:
                                                pass
                                        continue  # powtarza pojedynek
                                else:
                                    aktualny_symbol = 'O' if aktualny_symbol == 'X' else 'X'
                    elif wiadomosc.startswith("RESET"):
                        for x in range(5):
                            for y in range(5):
                                plansza[x][y] = '.'
                        aktualny_symbol = random.choice(['X', 'O'])
                    elif wiadomosc.startswith("PLANSZA"):
                        conn.sendall(("PLANSZA\n" + self.pokaz_plansze(plansza) + f"\nTURA:{aktualny_symbol}\n").encode())
                except Exception as e:
                    print("Błąd połączenia:", e)
                    break
            continue

    def czekaj_na_ready(self, conn, nick, gotowi, ready_lock):
        try:
            conn.sendall("READY_BTN|Kliknij przycisk, aby przejść do kolejnej rundy.\n".encode())
            print(f"Wysłano komunikat READY_BTN do {nick}")
            data = b''
            while not data.endswith(b'\n'):
                fragment = conn.recv(1024)
                if not fragment:
                    return
                data += fragment
            wiadomosc = data.decode().strip()
            if wiadomosc == "READY":
                with ready_lock:
                    gotowi.append((conn, nick))
        except Exception as e:
            print(f"Błąd (READY) u gracza {nick}: {e}")

    def start_server(self):
        print(f"Serwer turniejowy oczekuje na {self.ILOSC_GRACZY} graczy...")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.HOST, self.PORT))
            s.listen(self.ILOSC_GRACZY)
            while len(self.gracze) < self.ILOSC_GRACZY:
                conn, addr = s.accept()
                try:
                    nick = conn.recv(1024).decode().strip()
                except:
                    conn.close()
                    continue
                print(f"Połączono: {addr}, nick: {nick}")
                self.gracze.append(conn)
                self.nicki.append(nick)
                self.wszyscy_gracze.append(conn)
            aktualni = list(zip(self.gracze, self.nicki))
            runda = 1
            drabinka_historii = []
            while len(aktualni) > 1:
                pary = self.losuj_pary(list(range(len(aktualni))))
                wyniki_thread = [None] * len(pary)
                threads = []

                def pojedynek_watek(idx, a, b):
                    conn1, nick1 = aktualni[a]
                    conn2, nick2 = aktualni[b]
                    wynik, wygrany_nick, przegrany_nick, para_nicki = self.graj_pojedynek(conn1, nick1, conn2, nick2)
                    wyniki_thread[idx] = (wynik, wygrany_nick, przegrany_nick, para_nicki)

                for idx, (a, b) in enumerate(pary):
                    t = threading.Thread(target=pojedynek_watek, args=(idx, a, b))
                    t.start()
                    threads.append(t)
                for t in threads:
                    t.join()
                zwyciezcy = []
                opis_par = []
                for wynik, wygrany_nick, przegrany_nick, para_nicki in wyniki_thread:
                    if wygrany_nick:
                        zwyciezcy.append(wygrany_nick)
                    opis_par.append(f"{para_nicki[0]} vs {para_nicki[1]}  -> wygrał: {wygrany_nick if wygrany_nick else 'Remis'}")
                    # Możesz printować tu na potrzeby debugowania:
                    print("Mecz:", para_nicki[0], "vs", para_nicki[1], "Wygrał:", wygrany_nick)

                drabinka_historii.append(f"Runda {runda}:\n" + "\n".join(opis_par))
                drab_txt = "\n\n".join(drabinka_historii)
                print("Wysyłam drabinkę:", drab_txt)  # Debug info!
                runda += 1
                for c in self.wszyscy_gracze:
                    try:
                        c.sendall(f"DRABINKA|{drab_txt}\n".encode())
                    except:
                        pass

                nowi_aktualni = []
                ready_threads = []
                gotowi = []
                ready_lock = threading.Lock()
                for wygrany in zwyciezcy:
                    for c, n in aktualni:
                        if n == wygrany:
                            nowi_aktualni.append((c, n))
                            t = threading.Thread(target=self.czekaj_na_ready, args=(c, n, gotowi, ready_lock))
                            t.start()
                            ready_threads.append(t)
                            break
                for t in ready_threads:
                    t.join()
                aktualni = nowi_aktualni

            if len(aktualni) == 1:
                conn, nick = aktualni[0]
                try:
                    conn.sendall("WYGRANA|Wygrałeś cały turniej! Gratulacje!\n".encode())
                    dodaj_punkty(nick, 10, tryb="turniej")
                except:
                    pass
            for c in self.gracze:
                try:
                    c.close()
                except:
                    pass

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ilosc_graczy = int(sys.argv[1])
    else:
        ilosc_graczy = 2
    TicTacToeTournamentServer(ilosc_graczy=ilosc_graczy)
