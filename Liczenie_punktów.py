class Punktacja:
    def __init__(self, plansza, rozmiar=5):
        self.plansza = plansza
        self.rozmiar = rozmiar
        self.punkty_za_grupy = {2: 1, 3: 3, 4: 7, 5: 15}

    def licz_grupy(self, linia, symbol):
        suma = 0
        cnt = 0
        for v in linia:
            if v == symbol:
                cnt += 1
            else:
                if cnt in self.punkty_za_grupy:
                    suma += self.punkty_za_grupy[cnt]
                cnt = 0
        if cnt in self.punkty_za_grupy:
            suma += self.punkty_za_grupy[cnt]
        return suma

    def punkty_gracza(self, symbol):
        N = self.rozmiar
        wynik = 0
        # Wiersze
        for i in range(N):
            wynik += self.licz_grupy(self.plansza[i], symbol)
        # Kolumny
        for j in range(N):
            wynik += self.licz_grupy([self.plansza[i][j] for i in range(N)], symbol)
        # Wszystkie przekątne ↘ (z lewej do prawej)
        for k in range(-N+2, N-1):
            przekatna = [self.plansza[i][i-k] for i in range(max(k, 0), min(N, N+k))]
            if len(przekatna) >= 2:
                wynik += self.licz_grupy(przekatna, symbol)
        # Wszystkie przekątne ↗ (z lewej do prawej w dół)
        for k in range(1, 2*N-2):
            przekatna = [self.plansza[i][k-i] for i in range(max(0, k-N+1), min(N, k+1)) if 0 <= k-i < N]
            if len(przekatna) >= 2:
                wynik += self.licz_grupy(przekatna, symbol)
        return wynik

# Przykładowe użycie:
if __name__ == "__main__":
    testowa_plansza = [
        ['X', 'O', 'X', 'O', 'X'],
        ['O', 'X', 'O', 'O', 'O'],
        ['X', 'X', 'X', 'O', 'X'],
        ['O', 'O', 'X', 'X', 'O'],
        ['O', 'X', 'X', 'O', 'O']
    ]
    punktacja = Punktacja(testowa_plansza)
    print("Punkty X:", punktacja.punkty_gracza('X'))
    print("Punkty O:", punktacja.punkty_gracza('O'))

