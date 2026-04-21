import tkinter as tk
import subprocess
import mysql.connector
from tkinter import messagebox
from baza import inicjalizuj_baze, dodaj_uzytkownika, znajdz_email, generuj_token_reset, ustaw_nowe_haslo
from email_reset import EmailReset

class LogowanieApp:
    def __init__(self):
        inicjalizuj_baze()
        self.root = tk.Tk()
        self.root.title("Logowanie")
        self.root.geometry("350x180")
        self.setup_gui()
        self.center_window(self.root)

    def center_window(self, win):
        win.update_idletasks()
        width = win.winfo_width()
        height = win.winfo_height()
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry(f"{width}x{height}+{x}+{y}")

    def setup_gui(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True)

        tk.Label(main_frame, text="Login:").grid(row=0, column=0, sticky='e', pady=5)
        self.entry_login = tk.Entry(main_frame)
        self.entry_login.grid(row=0, column=1, pady=5)
        self.entry_login.bind("<Return>", lambda event: self.logowanie())

        tk.Label(main_frame, text="Hasło:").grid(row=1, column=0, sticky='e', pady=5)
        self.entry_haslo = tk.Entry(main_frame, show="*")
        self.entry_haslo.grid(row=1, column=1, pady=5)
        self.entry_haslo.bind("<Return>", lambda event: self.logowanie())

        btn_frame = tk.Frame(main_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)

        tk.Button(btn_frame, text="Zaloguj", width=13, command=self.logowanie).pack(side=tk.LEFT, padx=3)
        tk.Button(btn_frame, text="Nowy gracz", width=13, command=self.otworz_rejestracje).pack(side=tk.LEFT, padx=3)
        tk.Button(btn_frame, text="Resetuj hasło", width=13, command=self.otworz_reset_hasla).pack(side=tk.LEFT, padx=3)

    def logowanie(self):
        login = self.entry_login.get().strip()
        haslo = self.entry_haslo.get().strip()
        if not (login and haslo):
            messagebox.showerror("Błąd", "Uzupełnij login i hasło")
            return
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="kik"
        )
        c = conn.cursor()
        c.execute("SELECT * FROM uzytkownicy WHERE login=%s AND haslo=%s", (login, haslo))
        row = c.fetchone()
        conn.close()
        if row:
            messagebox.showinfo("Logowanie", "Zalogowano pomyślnie!")
            self.root.destroy()
            subprocess.Popen(['python', 'menu.py', login])
        else:
            messagebox.showerror("Błąd", "Błędny login lub hasło")

    def otworz_rejestracje(self):
        okno = tk.Toplevel(self.root)
        okno.title("Rejestracja")
        self.center_window(okno)
        frame = tk.Frame(okno)
        frame.pack(padx=10, pady=10)

        tk.Label(frame, text="Login:").grid(row=0, column=0, sticky='e', pady=2)
        entry_login_r = tk.Entry(frame)
        entry_login_r.grid(row=0, column=1, pady=2)

        tk.Label(frame, text="Hasło:").grid(row=1, column=0, sticky='e', pady=2)
        entry_haslo_r = tk.Entry(frame, show="*")
        entry_haslo_r.grid(row=1, column=1, pady=2)

        tk.Label(frame, text="Email:").grid(row=2, column=0, sticky='e', pady=2)
        entry_email_r = tk.Entry(frame)
        entry_email_r.grid(row=2, column=1, pady=2)

        tk.Label(frame, text="Zespół:").grid(row=3, column=0, sticky='e', pady=2)
        entry_zespol_r = tk.Entry(frame)
        entry_zespol_r.grid(row=3, column=1, pady=2)

        def zapisz_gracza():
            login = entry_login_r.get().strip()
            haslo = entry_haslo_r.get().strip()
            email = entry_email_r.get().strip()
            zespol = entry_zespol_r.get().strip()
            if not (login and haslo and email and zespol):
                messagebox.showerror("Błąd", "Uzupełnij wszystkie pola!")
                return
            if dodaj_uzytkownika(login, haslo, email, zespol):
                messagebox.showinfo("Sukces", "Konto założone!")
                okno.destroy()
            else:
                messagebox.showerror("Błąd", "Login lub email już istnieje!")

        tk.Button(frame, text="Zarejestruj", width=20, command=zapisz_gracza).grid(row=4, column=0, columnspan=2, pady=8)

    mailer = EmailReset(
        login="twoj_email@gmail.com",  # <-- Twój e-mail
        password="twoje_haslo"  # <-- Twoje hasło
    )

    def otworz_reset_hasla(self):
        okno = tk.Toplevel(self.root)
        okno.title("Reset hasła")
        self.center_window(okno)
        frame = tk.Frame(okno)
        frame.pack(padx=10, pady=10)

        tk.Label(frame, text="Login lub email:").grid(row=0, column=0, sticky='e')
        entry_id = tk.Entry(frame)
        entry_id.grid(row=0, column=1, pady=5)

        def wyslij_reset():
            user = entry_id.get().strip()
            email = znajdz_email(user)
            if not email:
                messagebox.showerror("Błąd", "Nie znaleziono użytkownika.")
                return
            token = generuj_token_reset(user)
            mailer = EmailReset()  # lub podaj login i hasło jeśli trzeba
            mailer.wyslij_mail_reset(email, token)
            messagebox.showinfo("Reset hasła", f"Wysłano kod resetu na {email}.\nPrzepisz kod w kolejnym oknie.")
            okno.destroy()
            self.otworz_potwierdzenie_reset(user)

        tk.Button(frame, text="Wyślij kod resetu", command=wyslij_reset).grid(row=1, column=0, columnspan=2, pady=8)

    def otworz_potwierdzenie_reset(self, user):
        okno = tk.Toplevel(self.root)
        okno.title("Ustaw nowe hasło")
        self.center_window(okno)
        frame = tk.Frame(okno)
        frame.pack(padx=10, pady=10)

        tk.Label(frame, text="Kod resetu:").grid(row=0, column=0, sticky='e')
        entry_token = tk.Entry(frame)
        entry_token.grid(row=0, column=1, pady=4)

        tk.Label(frame, text="Nowe hasło:").grid(row=1, column=0, sticky='e')
        entry_new = tk.Entry(frame, show="*")
        entry_new.grid(row=1, column=1, pady=4)

        def potwierdz():
            token = entry_token.get().strip()
            nowe_haslo = entry_new.get().strip()
            if not (token and nowe_haslo):
                messagebox.showerror("Błąd", "Uzupełnij wszystkie pola!")
                return
            if ustaw_nowe_haslo(user, token, nowe_haslo):
                messagebox.showinfo("Sukces", "Hasło zostało zmienione!")
                okno.destroy()
            else:
                messagebox.showerror("Błąd", "Kod niepoprawny lub wygasł.")

        tk.Button(frame, text="Zmień hasło", width=20, command=potwierdz).grid(row=2, column=0, columnspan=2, pady=8)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    LogowanieApp().run()
