import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailReset:
    def __init__(self, host='smtp.gmail.com', port=587, login='', password=''):
        # Tutaj wpisz swoje dane (albo pobierz z pliku/kodu środowiskowego)
        self.smtp_host = host
        self.smtp_port = port
        self.smtp_login = login or "TWOJ_EMAIL@gmail.com"   # <-- tu podaj swój e-mail
        self.smtp_pass = password or "TWOJE_HASLO"          # <-- tu podaj swoje hasło

    def wyslij_mail_reset(self, adres_email, token):
        msg = MIMEMultipart()
        msg['From'] = self.smtp_login
        msg['To'] = adres_email
        msg['Subject'] = 'Kod resetu hasła'
        body = f"Twój kod resetu hasła to:\n\n{token}\n\nWpisz go w oknie aplikacji, by ustawić nowe hasło."
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            server.starttls()
            server.login(self.smtp_login, self.smtp_pass)
            server.send_message(msg)
            server.quit()
            print("E-mail z kodem resetu został wysłany.")
            return True
        except Exception as e:
            print("Błąd wysyłania e-maila:", e)
            return False

# Przykładowe użycie:
if __name__ == "__main__":
    # W produkcji nie trzymaj jawnie loginu/hasła! Użyj zmiennych środowiskowych.
    mailer = EmailReset(login="twoj_email@gmail.com", password="twoje_haslo")
    mailer.wyslij_mail_reset("adres@przyklad.pl", "ABC123")
