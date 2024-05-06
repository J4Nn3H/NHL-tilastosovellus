import json

class Pelaaja:
    def __init__(self, name: str, nationality: str, assists: int, goals: int, penalties: int, team: str, games: int):
        self.name = name
        self.nationality = nationality
        self.assists = assists
        self.goals = goals
        self.penalties = penalties
        self.team = team
        self.games = games

    def __str__(self):
        return f"{self.name.ljust(20)} {self.team.ljust(4)} {str(self.goals).rjust(2)} + {str(self.assists).rjust(2)} = {str(self.goals + self.assists).rjust(3)}"


class Pelaajat:

    montako_pelaajaa = 0

    def __init__(self):
        self.pelaajat = []

    def lisaa_pelaaja(self, pelaaja: Pelaaja):
        self.pelaajat.append(pelaaja)
        Pelaajat.montako_pelaajaa += 1

    def hae_pelaaja(self, nimi: str):
        for p in self.pelaajat:
            if p.name == nimi:
                return p
        return None

    def __str__(self):
        if len(self.pelaajat) == 0:
            return "ei pelaajia"
        return "\n".join([str(p) for p in self.pelaajat])


class Joukkueet:
    def __init__(self):
        self.joukkueet = []

    def lisaa_joukkue(self, joukkue: str):
        if joukkue not in self.joukkueet:
            self.joukkueet.append(joukkue)

    def __str__(self):
        if len(self.joukkueet) == 0:
            return "ei joukkueita"
        return "\n".join(sorted(self.joukkueet))


class Maat:
    def __init__(self):
        self.maat = []

    def lisaa_maa(self, maa: str):
        if maa not in self.maat:
            self.maat.append(maa)

    def __str__(self):
        if len(self.maat) == 0:
            return "ei maita"
        return "\n".join(sorted(self.maat))


class Tiedoston_kasittelija:
    def __init__(self, tiedosto: str):
        self.tiedosto = tiedosto

    def lataa_tiedosto(self):
        with open(self.tiedosto) as tiedosto:
            data = json.load(tiedosto)
            return data


class NHL_TilastoSovellus:
    def __init__(self):
        self.pelaajat = Pelaajat()
        self.joukkueet = Joukkueet()
        self.maat = Maat()
        self.tiedoston_kasittelija = Tiedoston_kasittelija("")

    def ohje(self):
        print()
        print("komennot:")
        print("0 lopeta")
        print("1 hae pelaaja")
        print("2 joukkueet")
        print("3 maat")
        print("4 joukkueen pelaajat")
        print("5 maan pelaajat")
        print("6 eniten pisteitä")
        print("7 eniten maaleja")

    def suorita(self):
        tiedosto = input("tiedosto: ")
        self.tiedoston_kasittelija.tiedosto = tiedosto
        data = self.tiedoston_kasittelija.lataa_tiedosto()

        for pelaaja_data in data:
            pelaaja = Pelaaja(pelaaja_data["name"], pelaaja_data["nationality"], pelaaja_data["assists"], pelaaja_data["goals"], pelaaja_data["penalties"], pelaaja_data["team"], pelaaja_data["games"])
            self.pelaajat.lisaa_pelaaja(pelaaja)
            self.joukkueet.lisaa_joukkue(pelaaja.team)
            self.maat.lisaa_maa(pelaaja.nationality)

        print(f"luettiin {Pelaajat.montako_pelaajaa} pelaajan tiedot")

        self.ohje()

        while True:
            print()
            komento = input("komento: ")
            if komento == "0":
                break
            elif komento == "1":
                self.hae_pelaajan_tiedot()
            elif komento == "2":
                self.nayta_joukkueet()
            elif komento == "3":
                self.nayta_maat()
            elif komento == "4":
                self.hae_joukkueen_pelaajat_paremmuusjarjestyksessa()
            elif komento == "5":
                self.hae_maan_pelaajat_paremmuusjarjestyksessa()
            elif komento == "6":
                self.eniten_pisteita()
            elif komento == "7":
                self.eniten_maaleja()

    def hae_pelaajan_tiedot(self): # toiminto 1
        nimi = input("nimi: ")
        print()
        pelaaja = self.pelaajat.hae_pelaaja(nimi)
        if pelaaja is not None:
            print(pelaaja)
        else:
            print("pelaajaa ei löytynyt")

    def nayta_joukkueet(self): # toiminto 2
        print(self.joukkueet)

    def nayta_maat(self): # toiminto 3
        print(self.maat)

    def hae_joukkueen_pelaajat_paremmuusjarjestyksessa(self): # toiminto 4
        joukkue = input("joukkue: ")
        print()
        pelaajat_joukkueessa = [p for p in self.pelaajat.pelaajat if p.team == joukkue]
        if not pelaajat_joukkueessa:
            print("Joukkuetta ei löytynyt tai sillä ei ole pelaajia.")
            return

        pelaajat_joukkueessa.sort(key=lambda x: x.goals + x.assists, reverse=True)
        for pelaaja in pelaajat_joukkueessa:
            print(pelaaja)

    def hae_maan_pelaajat_paremmuusjarjestyksessa(self): # toiminto 5
        maa = input("maa: ")
        print()
        pelaajat_maa = [p for p in self.pelaajat.pelaajat if p.nationality == maa]
        if not pelaajat_maa:
            print("Maata ei löytynyt tai sillä ei ole pelaajia.")
            return

        pelaajat_maa.sort(key=lambda x: x.goals + x.assists, reverse=True)
        for pelaaja in pelaajat_maa:
            print(pelaaja)

    def eniten_pisteita(self): # toiminto 6
        montako = int(input("kuinka monta: "))
        print()
        pelaajat = self.pelaajat.pelaajat
        if not pelaajat:
            print("Ei pelaajia.")
            return
    
        pelaajat.sort(key=lambda x: x.goals + x.assists, reverse=True)
        parhaat_pelaajat = pelaajat[:montako]
        for pelaaja in parhaat_pelaajat:
            print(pelaaja)


    def eniten_maaleja(self): # toiminto 7
        montako = int(input("kuinka monta: "))
        print()
        pelaajat = self.pelaajat.pelaajat
        if not pelaajat:
            print("Ei pelaajia.")
            return

        pelaajat.sort(key=lambda x: (x.goals, -x.games), reverse=True)
        parhaat_pelaajat = pelaajat[:montako]
        for pelaaja in parhaat_pelaajat:
            print(pelaaja)


suorita = NHL_TilastoSovellus()
suorita.suorita()
