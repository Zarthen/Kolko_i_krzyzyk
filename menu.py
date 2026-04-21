import re
import tkinter as tk
import subprocess
from tkinter import simpledialog, messagebox
from baza import pobierz_punkty

class MenuApp:
    def __init__(self, user_login=None):
        self.root = tk.Tk()
        self.root.title("Menu główne")
        self.user_login = user_login
        self.setup_gui()  # najpierw dodajesz wszystkie widgety
        # online = pobierz_punkty(login, tryb="online")
        # turniej = pobierz_punkty(login, tryb="turniej")
        lokalne = pobierz_punkty(login, tryb="lokalne")
        online = pobierz_punkty(login, tryb="online")
        turniej = pobierz_punkty(login, tryb="turniej")
        self.punkty_label.config(
            text=f"Punkty lokalne: {lokalne}\nPunkty online: {online}\nPunkty turniej: {turniej}"
        )
        self.center_window()  # potem dopiero centrowanie, po update_idletasks

    def setup_gui(self):
        label = tk.Label(self.root, text=f"Witaj {self.user_login}!\nWybierz tryb gry:", font=("Arial", 16))
        label.pack(pady=5, padx=30)

        self.punkty_label = tk.Label(self.root, text="Punkty...", font=("Arial", 8))
        self.punkty_label.pack(pady=5)

        btn_local = tk.Button(self.root, text="Graj lokalnie",width=20 , command=self.graj)
        btn_local.pack(pady=5)

        btn_local = tk.Button(self.root, text="Stwórz serwer",width=20 , command=self.stworz_serwer)
        btn_local.pack(pady=5)

        btn_online = tk.Button(self.root, text="Gra sieciowa",width=20 , command=self.gra_sieciowa)
        btn_online.pack(pady=5)

        btn_local = tk.Button(self.root, text="Stwórz serwer turniejowy",width=20 , command=self.utworz_serwer_turniejowy)
        btn_local.pack(pady=5)

        btn_turniej = tk.Button(self.root, text="Tryb turniejowy",width=20 , command=self.dolacz_do_turnieju)
        btn_turniej.pack(pady=5)

        btn_exit = tk.Button(self.root, text="Wyjście",width=20 , command=self.root.destroy)
        btn_exit.pack(pady=20)

        self.root.update_idletasks()

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def graj(self):
        subprocess.Popen(['python', 'gui_tictactoe.py', self.user_login])
        self.root.destroy()

    def stworz_serwer(self):
        messagebox.showinfo("Serwer",  "Serwer został uruchomiony.\nMożesz teraz połączyć się jako gracz na tym komputerze lub z innego po IP.")
        subprocess.Popen(['python', 'serwer.py'])

    def gra_sieciowa(self):
        # messagebox.showinfo("Online", "Tryb online uruchomi się (tu wstaw kod uruchamiania klienta).")
        while True:

            adres = simpledialog.askstring(
                "Gra sieciowa",
                "Podaj adres serwera (przykład:\n7.tcp.eu.ngrok.io:18507\nlub tcp://7.tcp.eu.ngrok.io:18507\nlub samo IP):",
                initialvalue="localhost:65436"
            )
            if adres is None:
                return  # Anulowano

            adres = adres.strip()
            # Usuwamy tcp:// jeśli ktoś wkleił cały link ngrok
            if adres.startswith("tcp://"):
                adres = adres[6:]

            # Rozpoznajemy host i port, np. 7.tcp.eu.ngrok.io:18507
            match = re.match(r'^([a-zA-Z0-9\.\-]+)(?::([0-9]+))?$', adres)
            if match:
                ip = match.group(1)
                port = match.group(2)
                if port is None:
                    # Jeśli portu nie było, zapytaj jeszcze o port
                    port = simpledialog.askinteger("Port serwera", "Podaj port serwera (1-65535):", initialvalue=65436)
                    if not port or not (1 <= int(port) <= 65532):
                        messagebox.showerror("Błąd", "Port musi być liczbą całkowitą z zakresu 1-65535!")
                        continue
                else:
                    port = int(port)
                    if not (1 <= port <= 65532):
                        messagebox.showerror("Błąd", "Port musi być liczbą całkowitą z zakresu 1-65535!")
                        continue

                if ip == "":
                    messagebox.showerror("Błąd", "IP/host nie może być puste!")
                    continue

                # subprocess.Popen(['python', 'klient.py', str(ip), str(port)])
                subprocess.Popen(['python', 'klient.py', ip, str(port), self.user_login])
                self.root.destroy()
                break

            else:
                messagebox.showerror("Błąd", "Nieprawidłowy format adresu!")
                continue

    def utworz_serwer_turniejowy(self):
        # messagebox.showinfo("Turniej", "Tryb turniejowy uruchomi się (tu wstaw kod uruchamiania klienta turniejowego).")
        # subprocess.Popen(['python', 'Serwer_turniejowy.py'])
        ilosc = simpledialog.askinteger("Turniej", "Podaj liczbę graczy (parzysta, np. 4, 6, 8):", minvalue=2)
        if ilosc and ilosc % 2 == 0:
            subprocess.Popen(['python', 'serwer_turniejowy.py', str(ilosc)])
            messagebox.showinfo("Serwer turniejowy", f"Serwer turniejowy został uruchomiony na {ilosc} graczy.\nPrzekaż innym adres i port!")
        else:
            messagebox.showerror("Błąd", "Liczba graczy musi być parzysta i większa niż 1!")

    def dolacz_do_turnieju(self):
        # messagebox.showinfo("Turniej", "Tryb turniejowy uruchomi się (tu wstaw kod uruchamiania klienta turniejowego).")
        # subprocess.Popen(['python', 'klient_turniejowy.py'])
        adres = simpledialog.askstring("Turniej", "Podaj adres serwera turniejowego (np. 7.tcp.eu.ngrok.io:18507):", initialvalue="localhost:65436")
        if adres:
            adres = adres.strip()
            # Usuwamy tcp:// jeśli ktoś wkleił cały link ngrok
            if adres.startswith("tcp://"):
                adres = adres[6:]
            # Rozpoznajemy host i port, np. 7.tcp.eu.ngrok.io:18507
            match = re.match(r'^([a-zA-Z0-9\.\-]+)(?::([0-9]+))?$', adres)
            if match:
                ip = match.group(1)
                port = match.group(2)
                if port is None:
                    port = simpledialog.askinteger("Port serwera", "Podaj port serwera (1-65535):", initialvalue=65436)
                    if not port or not (1 <= int(port) <= 65535):
                        messagebox.showerror("Błąd", "Port musi być liczbą całkowitą z zakresu 1-65535!")
                        return
                else:
                    port = int(port)
                    if not (1 <= port <= 65535):
                        messagebox.showerror("Błąd", "Port musi być liczbą całkowitą z zakresu 1-65535!")
                        return

                # subprocess.Popen(['python', 'klient_turniejowy.py', str(ip), str(port)])
                subprocess.Popen(['python', 'klient_turniejowy.py', ip, str(port), self.user_login])

            self.root.destroy()
        else:

            messagebox.showerror("Błąd", "Nieprawidłowy format adresu!")

    def run(self):
        self.root.mainloop()
        #subprocess.Popen(['python', 'menu.py', self.user_login])  # Otwórz menu na nowo z nickiem
if __name__ == "__main__":
    import sys
    login = sys.argv[1] if len(sys.argv) > 1 else "Anonim"
    app = MenuApp(login)
    app.run()
    sys.exit()