import socket
import tkinter as tk
import threading
import sys
import subprocess
from tkinter import simpledialog, messagebox

class TournamentClient:
    def __init__(self):
        self.HOST, self.PORT, self.LOGIN = self.parse_args()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.HOST, self.PORT))
        self.client_socket.sendall(self.LOGIN.encode())
        symbol_info = self.client_socket.recv(1024).decode().strip().split('\n')
        self.symbol = symbol_info[0]
        self.start_symbol = 'X'
        if len(symbol_info) > 1 and symbol_info[1].startswith("START:"):
            self.start_symbol = symbol_info[1].split(":")[1]
        self.przeciwnik_symbol = 'O' if self.symbol == 'X' else 'X'
        messagebox.showinfo("Twój symbol", f"Jesteś graczem: {self.symbol}\nGrę zaczyna: {self.start_symbol}")

        self.root = tk.Tk()
        self.root.title(f"Kółko i Krzyżyk - Turniej (Gracz {self.LOGIN} {self.symbol})")
        self.root.protocol("WM_DELETE_WINDOW", self.koniec_i_menu)
        self.setup_gui()
        threading.Thread(target=self.odbierz_i_odswiez, daemon=True).start()
        self.root.mainloop()
        self.client_socket.close()

    def parse_args(self):
        if len(sys.argv) > 3:
            HOST = sys.argv[1]
            PORT = int(sys.argv[2])
            LOGIN = sys.argv[3]
        elif len(sys.argv) > 2:
            HOST = sys.argv[1]
            PORT = int(sys.argv[2])
            LOGIN = sys.argv[3]("Nick", "Podaj swój nick (login):")
        elif len(sys.argv) > 1:
            HOST = sys.argv[1]
            PORT = 65436
            LOGIN = sys.argv[3]("Nick", "Podaj swój nick (login):")
        else:
            HOST = 'localhost'
            PORT = 65436
            LOGIN = simpledialog.askstring("Nick", "Podaj swój nick (login):")
        if not LOGIN:
            LOGIN = "Anonim"
        return HOST, PORT, LOGIN

    def setup_gui(self):
        self.plansza_frame = tk.Frame(self.root)
        self.plansza_frame.pack(side=tk.LEFT, padx=10, pady=10)
        self.przyciski = []
        self.plansza_klient = [['.' for _ in range(5)] for _ in range(5)]
        self.tura = self.start_symbol
        self.gra_zakonczona = False
        self.ready_btn = None

        for i in range(5):
            wiersz = []
            for j in range(5):
                button = tk.Button(self.plansza_frame, text='', width=5, height=2,
                                   font=('Helvetica', 24),
                                   command=lambda x=i, y=j: self.wyslij_ruch(x, y))
                button.grid(row=i, column=j)
                wiersz.append(button)
            self.przyciski.append(wiersz)

        # Chat log (okno tekstowe na górze)
        self.chat_log = tk.Text(self.root, height=6, width=40, font=('Consolas', 10), state=tk.DISABLED)
        self.chat_log.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(15, 0))

        # Ramka na wpisywanie wiadomości i przycisk
        chat_entry_frame = tk.Frame(self.root)
        chat_entry_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(0, 10))

        self.chat_entry = tk.Entry(chat_entry_frame, width=32)
        self.chat_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.chat_entry.bind("<Return>", self.wyslij_czat)
        chat_btn = tk.Button(chat_entry_frame, text="Wyślij", command=self.wyslij_czat)
        chat_btn.pack(side=tk.LEFT, padx=5)

        # Utworzenie ramki drabinki
        drabinka = tk.LabelFrame(self.root, text="Drabinka turniejowa", padx=10, pady=10)
        drabinka.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        self.drabinka_text = tk.Text(drabinka, height=15, width=40, font=('Consolas', 10), wrap="word")
        self.drabinka_text.pack(fill=tk.BOTH, expand=True)
        self.drabinka_text.config(state=tk.DISABLED)

        scrollbar = tk.Scrollbar(drabinka, command=self.drabinka_text.yview)
        self.drabinka_text.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def wyslij_ruch(self, i, j):
        if self.gra_zakonczona or self.przyciski[i][j]["text"] != "":
            return
        self.client_socket.sendall(f"RUCH {i},{j}\n".encode())

    def wyslij_czat(self, event=None):
        msg = self.chat_entry.get().strip()
        if msg:
            self.client_socket.sendall(f"CHAT|{msg}\n".encode())
            self.chat_entry.delete(0, tk.END)

    def kliknij_ready(self):
        if self.ready_btn:
            self.ready_btn.destroy()
            self.ready_btn = None
        self.client_socket.sendall(b"READY\n")

    def odbierz_i_odswiez(self):
        while True:
            try:
                data = self.client_socket.recv(4096).decode()
                print("ODEBRANE DANE:", repr(data))
                if not data:
                    break
            except Exception:
                break

            for linia in data.split('\n'):
                linia = linia.strip()
                if not linia:
                    continue

                if linia.startswith("READY_BTN"):
                    print("ODEBRANO READY_BTN od serwera!")
                    if not self.ready_btn:
                        self.ready_btn = tk.Button(self.root, text="Jestem gotowy na kolejną rundę", bg="orange",
                                                   fg="black",
                                                   font=('Helvetica', 14), command=self.kliknij_ready)
                        self.ready_btn.pack(pady=30)
                    self.gra_zakonczona = False
                    for row in self.przyciski:
                        for btn in row:
                            btn['state'] = 'disabled'
                    continue

            # Obsługa symbolu i startu
            if data.startswith("X\nSTART:") or data.startswith("O\nSTART:"):
                lines = data.strip().split("\n")
                self.symbol = lines[0]
                self.start_symbol = lines[1].split(":")[1] if len(lines) > 1 else 'X'
                self.root.title(f"Kółko i Krzyżyk - Turniej (Gracz {self.LOGIN} {self.symbol})")
                messagebox.showinfo("Twój symbol", f"Jesteś graczem: {self.symbol}\nGrę zaczyna: {self.start_symbol}")
                for i in range(5):
                    for j in range(5):
                        self.plansza_klient[i][j] = '.'
                        self.przyciski[i][j].config(text='', state='disabled')
                self.tura = self.start_symbol
                self.gra_zakonczona = False
                continue

            if "READY_BTN|" in data:
                print("ODEBRANO READY_BTN od serwera!")
                if not self.ready_btn:
                    self.ready_btn = tk.Button(self.root, text="Jestem gotowy na kolejną rundę", bg="orange", fg="black",
                                               font=('Helvetica', 14), command=self.kliknij_ready)
                    self.ready_btn.pack(pady=30)
                self.gra_zakonczona = False
                for row in self.przyciski:
                    for btn in row:
                        btn['state'] = 'disabled'

            if "DRABINKA|" in data:
                idx = data.find("DRABINKA|")
                if idx != -1:
                    tresc = data[idx + len("DRABINKA|"):].strip()
                    self.drabinka_text.config(state=tk.NORMAL)
                    self.drabinka_text.delete(1.0, tk.END)
                    self.drabinka_text.insert(tk.END, tresc)
                    self.drabinka_text.config(state=tk.DISABLED)
                    print("ODEBRANO DRABINKA:", repr(tresc))

            if data.startswith("KONIEC"):
                self.gra_zakonczona = True
                messagebox.showinfo("Koniec gry", data)
                for row in self.przyciski:
                    for btn in row:
                        btn['state'] = 'disabled'
                continue

            if data.startswith("WYGRALES|"):
                messagebox.showinfo("Turniej", "Wygrałeś! Kliknij przycisk, by przejść dalej.")
                self.gra_zakonczona = True
                for row in self.przyciski:
                    for btn in row:
                        btn['state'] = 'disabled'
                self.root.after(0, self.koniec_i_menu)

                return
                #continue

            if data.startswith("PRZEGRALES|"):
                messagebox.showinfo("Turniej", "Przegrałeś, odpadasz z turnieju. Poczekaj na zwycięzce turnieju.")
                self.gra_zakonczona = True
                for row in self.przyciski:
                    for btn in row:
                        btn['state'] = 'disabled'
                self.root.after(0, self.koniec_i_menu)

                return
                #continue

            if data.startswith("REMIS|"):
                messagebox.showinfo("Turniej", "Remis — obaj odpadacie z turnieju. Poczekaj na zwycięzce turniej.")
                self.gra_zakonczona = True
                for row in self.przyciski:
                    for btn in row:
                        btn['state'] = 'disabled'
                self.root.after(0, self.koniec_i_menu)

                return
                #continue

            if data.startswith("WYGRANA|"):
                messagebox.showinfo("Turniej", "Wygrałeś cały turniej! Gratulacje!")
                self.gra_zakonczona = True
                for row in self.przyciski:
                    for btn in row:
                        btn['state'] = 'disabled'
                self.root.title(f"Kółko i Krzyżyk - Turniej (Gracz {self.LOGIN} {self.symbol} WYGRANA!)")
                self.root.after(0, self.koniec_i_menu)

                return
                # continue
                # self.koniec_i_menu()

            if data.startswith("PLANSZA"):
                linie = data.strip().split("\n")[1:6]
                tura_line = data.strip().split("\n")[-1]
                if tura_line.startswith("TURA:"):
                    self.tura = tura_line.split(":")[1]
                for i in range(5):
                    pola = linie[i].split()
                    for j in range(5):
                        self.plansza_klient[i][j] = pola[j]
                        self.przyciski[i][j].config(text='' if pola[j] == '.' else pola[j])

                blokuj = (self.tura != self.symbol or self.gra_zakonczona)
                for i in range(5):
                    for j in range(5):
                        stan_pola = self.plansza_klient[i][j]
                        self.przyciski[i][j]['state'] = ('normal' if not blokuj and stan_pola == '.' else 'disabled')

            if data.startswith('X') or data.startswith('O'):
                lines = data.strip().split('\n')
                if lines[0] in ['X', 'O']:
                    self.symbol = lines[0]
                    if len(lines) > 1 and lines[1].startswith('START:'):
                        self.tura = lines[1].split(':')[1]
                continue

            if data.startswith("CHAT|"):
                tresc = data.split("|", 1)[1]
                self.chat_log.config(state=tk.NORMAL)
                self.chat_log.insert(tk.END, tresc + "\n")
                self.chat_log.config(state=tk.DISABLED)
                self.chat_log.see(tk.END)
                continue

    # def koniec_i_menu(self):
    #     import subprocess, sys
    #     try:
    #         self.root.destroy()
    #     except Exception:
    #         pass
    #     try:
    #         # Uruchom menu z przekazanym nickiem
    #         subprocess.Popen(['python', 'menu.py', self.LOGIN])
    #     except Exception as e:
    #         print(f"Nie udało się uruchomić menu: {e}")
    #     sys.exit()

    def koniec_i_menu(self):
        try:
            self.root.destroy()
        except Exception:
            pass
        try:
            subprocess.Popen(['python', 'menu.py', self.LOGIN])
        except Exception as e:
            print(f"Nie udało się uruchomić menu: {e}")
        sys.exit()

if __name__ == "__main__":
    TournamentClient()
