from scipy import signal

from encje.kolejka import Kolejka
from encje.obiekt_silnika import ObiektSilnika

wejscie = None


class Symulacja:
    """
    Klasa, która ma za zadanie symulować pracę silnika
    w czasie rzeczywistym
    """

    def __init__(self):
        self.__czas_probkowania = 0.002
        self.__silnik = ObiektSilnika().transmitancja
        # [czas, wejście, wyjście]
        self.dane = {"czas": Kolejka(), "wejscie": Kolejka(), "wyjscie": Kolejka()}

    def aktualizacja_symulacji(self):
        """
        Aktualizuje symulacje
        """
        if wejscie is None:
            return
        self.dane["czas"].dodanie_do_kolejki(self.dane['czas'].ostatnia_wartosc() + self.__czas_probkowania)
        self.dane['wejscie'].dodanie_do_kolejki(wejscie)
        _, y, _ = signal.lsim(self.__silnik, U=self.dane['wejscie'].aktualna_kolejka(),
                              T=self.dane['czas'].aktualna_kolejka())
        self.dane['wyjscie'].dodanie_do_kolejki(y[-1])

    def aktualne_wartosci(self):
        """
        Zwraca aktualne wartosci
        """
        return self.dane

def thread_job():
    global wejscie
    wejscie = 1
    sym = Symulacja()
    while True:
        sym.aktualizacja_symulacji()
        plt.plot(sym.dane["czas"].aktualna_kolejka(), sym.dane["wyjscie"].aktualna_kolejka())
        plt.xlabel("Czas")
        plt.ylabel("Wyjście")
        plt.title("Odpowiedź obiektu w czasie rzeczywistym")
        plt.show(block=False)
        plt.pause(0.1)

if __name__ == "__main__":
    sym = Symulacja()
    from matplotlib import pyplot as plt
    import threading
    t = threading.Thread(target=thread_job)
    t.start()
    try:
        while True:
            wejscie = float(input("Podaj wejście: "))
    except KeyboardInterrupt:
        plt.close()
        exit(0)

