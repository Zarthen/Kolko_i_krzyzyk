import tkinter as tk
from Liczenie_punktów import Punktacja
from baza import dodaj_punkty
import sys
import subprocess

class TicTacToeGUI:
    def __init__(self, master, rozmiar=5, nick="Anonim"):
        self.master = master
        self.rozmiar = rozmiar
        self.nick = nick  # Nick użytkownika
        self.symbol = 'X'
        self.gra_zakonczona = False
        self.plansza = [['.' for _ in range(self.rozmiar)] for _ in range(self.rozmiar)]
        self.przyciski = []
        self.build_gui()
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

    def build_gui(self):
        self.master.title(f"Kółko i Krzyżyk - Lokalnie ({self.nick})")
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        for i in range(self.rozmiar):
            row = []
            for j in range(self.rozmiar):
                btn = tk.Button(self.frame, text='', width=4, height=2, font=('Helvetica', 22),
                                command=lambda x=i, y=j: self.ruch(x, y))
                btn.grid(row=i, column=j)
                row.append(btn)
            self.przyciski.append(row)
        self.status = tk.Label(self.master, text="Tura: X", font=("Arial", 14))
        self.status.pack(pady=10)
        self.reset_btn = tk.Button(self.master, text="Koniec Gry", command=self.resetuj)
        self.reset_btn.pack(pady=5)

    def ruch(self, i, j):
        if self.gra_zakonczona or self.przyciski[i][j]['text']:
            return
        self.przyciski[i][j]['text'] = self.symbol
        self.plansza[i][j] = self.symbol
        if self.czy_koniec():
            self.gra_zakonczona = True
            pkt = Punktacja(self.plansza)
            x = pkt.punkty_gracza('X')
            o = pkt.punkty_gracza('O')
            if x > o:
                self.status['text'] = f"Koniec gry! Wygrywa X ({x}:{o})"
                dodaj_punkty(self.nick, 2,'lokalne')
            elif o > x:
                self.status['text'] = f"Koniec gry! Wygrywa O ({x}:{o})"
                dodaj_punkty(self.nick, 2,'lokalne')
            else:
                self.status['text'] = f"Koniec gry! Remis ({x}:{o})"
            return
        # Zmień turę
        self.symbol = 'O' if self.symbol == 'X' else 'X'
        self.status['text'] = f"Tura: {self.symbol}"

    def czy_koniec(self):
        return all(self.plansza[i][j] != '.' for i in range(self.rozmiar) for j in range(self.rozmiar))
        subprocess.Popen(['python', 'menu.py', self.nick])  # Otwórz menu na nowo z nickiem
        self.master.destroy()   # zamyka planszę!
        sys.exit()

    def resetuj(self):
        self.gra_zakonczona = False
        self.symbol = 'X'
        self.status['text'] = "Tura: X"
        self.plansza = [['.' for _ in range(self.rozmiar)] for _ in range(self.rozmiar)]
        for i in range(self.rozmiar):
            for j in range(self.rozmiar):
                self.przyciski[i][j]['text'] = ''

        subprocess.Popen(['python', 'menu.py', self.nick])  # Otwórz menu na nowo z nickiem
        self.master.destroy()  # Zamknij planszę!
        sys.exit()

    def on_close(self):
        subprocess.Popen(['python', 'menu.py', self.nick])
        self.master.destroy()
        sys.exit()

if __name__ == "__main__":
    root = tk.Tk()
    nick = sys.argv[1] if len(sys.argv) > 1 else "Anonim"
    app = TicTacToeGUI(root, nick=nick)
    root.mainloop()
