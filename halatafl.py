import copy
import time
import sys
import math
import pygame

ADANCIME_MAX = 2


def distEuclid(p0, p1):
    """
    Distanta intre doua puncte
    """
    (x0, y0) = p0
    (x1, y1) = p1
    return math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)


def mean(values):
    """
    Media
    """
    if len(values):
        return sum(values) / len(values)
    return 0


def median(values):
    """
    Mediana
    """
    n = len(values)
    if n == 0:
        return 0
    s = sorted(values)

    if n % 2:
        return s[n // 2]

    return (s[n // 2 - 1] + s[n // 2]) / 2


class Graph:
    # coordonatele nodurilor ()
    noduri = [
        (2, 0), (3, 0), (4, 0),  # 0   1    2
        (2, 1), (3, 1), (4, 1),  # 3   4    5
        (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2),  # 6   7    8   9   10  11  12
        (0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3),  # 13  14   15  16   17  18  19
        (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4),  # 20  21   22  23   24  25  26
        (2, 5), (3, 5), (4, 5),  # 27  28   29
        (2, 6), (3, 6), (4, 6)  # 30  31   32
        # 0   1    2
        # 3   4    5
        # 6   7    8   9   10  11  12
        # 13  14   15  16   17  18  19
        # 20  21   22  23   24  25  26
        # 27  28   29
        # 30  31   32
    ]
    muchii = [(0, 1), (0, 3), (0, 4), (1, 2), (1, 4), (2, 5), (2, 4), (3, 4), (3, 8), (4, 5), (8, 9), (9, 10), (9, 4),
              (8, 4), (4, 10), (10, 5), (6, 7), (7, 8), (10, 11), (11, 12),
              (13, 14), (14, 15), (15, 16), (16, 17), (17, 18), (18, 19),
              (20, 21), (21, 22), (22, 23), (23, 24), (24, 25), (25, 26),
              (27, 28), (28, 29), (30, 31), (31, 32), (6, 13), (13, 20), (7, 14), (14, 21), (8, 15), (15, 22), (9, 16),
              (16, 23), (10, 17), (17, 24), (11, 18), (18, 25), (12, 19), (19, 26),
              (22, 27), (27, 30), (23, 28), (28, 31), (24, 29), (29, 32), (6, 14), (20, 14), (14, 22), (14, 8), (8, 16),
              (22, 16), (16, 10), (16, 24), (10, 18), (24, 18), (18, 26), (18, 12),
              (22, 28), (30, 28), (28, 32), (28, 24)]
    listaAdiacenta = {0: [1, 3, 4],
                      1: [0, 2, 4],
                      2: [1, 5, 4],
                      3: [0, 4, 8],
                      4: [0, 1, 2, 3, 5, 9, 8, 10],
                      5: [2, 4, 10],
                      6: [7, 13, 14],
                      7: [6, 8, 14],
                      8: [3, 9, 4, 7, 15, 14, 16],
                      9: [8, 10, 4, 16],
                      10: [9, 4, 5, 11, 17, 16, 18],
                      11: [10, 12, 18],
                      12: [11, 19, 18],
                      13: [14, 6, 20],
                      14: [13, 15, 7, 21, 6, 20, 22, 8],
                      15: [14, 16, 8, 22],
                      16: [15, 17, 9, 23, 8, 22, 10, 24],
                      17: [16, 18, 10, 24],
                      18: [17, 19, 11, 25, 10, 24, 26, 12],
                      19: [18, 12, 26],
                      20: [21, 13, 14],
                      21: [20, 22, 14],
                      22: [21, 23, 15, 27, 14, 16, 28],
                      23: [22, 24, 16, 28],
                      24: [23, 25, 17, 29, 16, 18, 28],
                      25: [24, 26, 18],
                      26: [25, 19, 18],
                      27: [28, 22, 30],
                      28: [27, 29, 23, 31, 22, 30, 32, 24],
                      29: [28, 24, 32],
                      30: [31, 27, 28],
                      31: [30, 32, 28],
                      32: [31, 29, 28]}
    scalare = 100
    translatie = 20
    razaPct = 10
    razaPiesa = 20


class Buton:
    def __init__(self, display=None, left=0, top=0, w=0, h=0, culoareFundal=(53, 80, 115),
                 culoareFundalSel=(89, 134, 194), text="", font="arial", fontDimensiune=16, culoareText=(255, 255, 255),
                 valoare=""):
        self.display = display
        self.culoareFundal = culoareFundal
        self.culoareFundalSel = culoareFundalSel
        self.text = text
        self.font = font
        self.w = w
        self.h = h
        self.selectat = False
        self.fontDimensiune = fontDimensiune
        self.culoareText = culoareText
        # creez obiectul font
        fontObj = pygame.font.SysFont(self.font, self.fontDimensiune)
        self.textRandat = fontObj.render(self.text, True, self.culoareText)
        self.dreptunghi = pygame.Rect(left, top, w, h)
        # aici centram textul
        self.dreptunghiText = self.textRandat.get_rect(center=self.dreptunghi.center)
        self.valoare = valoare

    def selecteaza(self, sel):
        self.selectat = sel
        self.deseneaza()

    def selecteazaDupacoord(self, coord):
        if self.dreptunghi.collidepoint(coord):
            self.selecteaza(True)
            return True
        return False

    def updateDreptunghi(self):
        self.dreptunghi.left = self.left
        self.dreptunghi.top = self.top
        self.dreptunghiText = self.textRandat.get_rect(center=self.dreptunghi.center)

    def deseneaza(self):
        culoareF = self.culoareFundalSel if self.selectat else self.culoareFundal
        pygame.draw.rect(self.display, culoareF, self.dreptunghi)
        self.display.blit(self.textRandat, self.dreptunghiText)


class GrupButoane:
    def __init__(self, listaButoane=[], indiceSelectat=0, spatiuButoane=10, left=0, top=0):
        self.listaButoane = listaButoane
        self.indiceSelectat = indiceSelectat
        self.listaButoane[self.indiceSelectat].selectat = True
        self.top = top
        self.left = left
        leftCurent = self.left
        for b in self.listaButoane:
            b.top = self.top
            b.left = leftCurent
            b.updateDreptunghi()
            leftCurent += (spatiuButoane + b.w)

    def selecteazaDupacoord(self, coord):
        for ib, b in enumerate(self.listaButoane):
            if b.selecteazaDupacoord(coord):
                self.listaButoane[self.indiceSelectat].selecteaza(False)
                self.indiceSelectat = ib
                return True
        return False

    def deseneaza(self):
        # atentie, nu face wrap
        for b in self.listaButoane:
            b.deseneaza()

    def getValoare(self):
        return self.listaButoane[self.indiceSelectat].valoare


pygame.display.set_caption("Boghiu Alexandra-Adriana - Vulpi si Oi")
ecran = pygame.display.set_mode(size=(800, 800))
pygame.init()

culoareEcran = (255, 255, 255)
culoareLinii = (0, 0, 0)
piesaAlba = pygame.image.load(r'piesa-alba.png')
diametruPiesa = 2 * Graph.razaPiesa
piesaAlba = pygame.transform.scale(piesaAlba, (diametruPiesa, diametruPiesa))
piesaNeagra = pygame.image.load(r'piesa-neagra.png')
piesaNeagra = pygame.transform.scale(piesaNeagra, (diametruPiesa, diametruPiesa))
piesaSelectata = pygame.image.load(r'piesa-rosie.png')
piesaSelectata = pygame.transform.scale(piesaSelectata, (diametruPiesa, diametruPiesa))
nodPiesaSelectata = False
coordonateNoduri = [[Graph.translatie + Graph.scalare * x for x in nod] for nod in Graph.noduri]
timpi_JMIN = []
timpi_JMAX = []
timp_start = 0
nr_noduri_gen = 0
noduri_minmax = []
noduri_alphabeta = []


def manancaOi(jocuri):  # generez tablele unde vulpea mananca oi, nu muta in spatiu liber
    l_mutari = set()
    for joc in jocuri:
        for vulpe in joc.pieseVulpi: #iau o vulpe
            index_vecini_vulpe = vecini_piesa(vulpe)
            for vecin in index_vecini_vulpe: #caut vecinii ei
                if coordonateNoduri[vecin] in joc.pieseOi:  # am gasit o oaie
                    index_vecini_oaie = vecini_piesa(coordonateNoduri[vecin])  # caut vecinii oii ca sa vad daca am spatiu liber
                    directie_mutare = [vulpe[0] - coordonateNoduri[vecin][0],
                                       vulpe[1] - coordonateNoduri[vecin][1]] # ceva gen [0, 100], [-100, 0] etc
                    for vecin_oaie in index_vecini_oaie: #acum caut in vecinii oii, verific daca e loc liber dupa oaie sa pot muta vulpea
                        if (coordonateNoduri[vecin_oaie] not in joc.pieseVulpi + joc.pieseOi and
                                directie_mutare == [coordonateNoduri[vecin][0] - coordonateNoduri[vecin_oaie][0],
                                                    coordonateNoduri[vecin][1] - coordonateNoduri[vecin_oaie][
                                                        1]]):  # pot sa mananc oaia si sa mut  vulpea pe locul liber de dupa oaia mancata

                            pieseOiCopie = copy.deepcopy(joc.pieseOi)
                            pieseVulpiCopie = copy.deepcopy(joc.pieseVulpi)
                            pieseOiCopie[:] = [x for x in pieseOiCopie if
                                               x != coordonateNoduri[vecin]]  # scot oaia de pe pozitia veche
                            pieseVulpiCopie[:] = [x for x in pieseVulpiCopie if
                                                  x != vulpe]  # scot vulpea de pe pozitia veche
                            pieseVulpiCopie.append(coordonateNoduri[vecin_oaie])  # mut vulpea pe pozitia noua
                            jn = Joc(pieseOiCopie, pieseVulpiCopie)
                            l_mutari.add(jn)  # am salvat mutarea curenta
    return l_mutari


def continuaManancaOi(jocuri):
    while manancaOi(jocuri):
        jocuri = manancaOi(jocuri)  # mananc cate oi pot runda curenta
    return jocuri


def vecini_piesa_index(index_nod):
    """
    Caut vecinii dupa indexul unei piese
    """
    vec = []
    for (a, b) in Graph.muchii:
        if a == index_nod:
            vec.append(b)
        if b == index_nod:
            vec.append(a)
    return vec


def cautaOi(vulpe, pieseOi, pieseVulpi):
    """
    Returnez o lista de oi pe care le poate manca vulpea
    """
    index_vecini = vecini_piesa_index(vulpe)
    oi_de_mancat = []
    for vecin in index_vecini:
        if coordonateNoduri[vecin] in pieseOi:
            directie = [coordonateNoduri[vulpe][0] - coordonateNoduri[vecin][0],
                        coordonateNoduri[vulpe][1] - coordonateNoduri[vecin][1]]
            index_vecini_oaie = vecini_piesa(coordonateNoduri[vecin])
            for vecin_oaie in index_vecini_oaie:
                directie2 = [coordonateNoduri[vecin][0] - coordonateNoduri[vecin_oaie][0],
                             coordonateNoduri[vecin][1] - coordonateNoduri[vecin_oaie][1]]
                if coordonateNoduri[
                    vecin_oaie] not in pieseOi + pieseVulpi and directie == directie2:  # vecinul oii e liber si pe directia corecta, deci vulpea poate sa manance oaia
                    oi_de_mancat.append((vecin, vecin_oaie))  # trimit oaia de mancat si pozitia noua a vulpii
    return oi_de_mancat


class Joc:
    """
    Clasa care defineste jocul. Se va schimba de la un joc la altul.
    """
    JMIN = None
    JMAX = None
    pieseOi = [coordonateNoduri[i] for i in range(13, 33)]
    pieseVulpi = [coordonateNoduri[0], coordonateNoduri[2]]
    scor_maxim = 0
    j_curent = "O"

    def __init__(self, pieseOi=None, pieseVulpi=None):
        if pieseOi:  # am initializat tabla deja
            self.pieseOi = pieseOi
            self.pieseVulpi = pieseVulpi

        else:
            self.__class__.scor_maxim = 1000

    def setDisplay(self, ecran):
        self.display = ecran

    def sirAfisare(self):
        sir = f"Sunt {len(self.pieseOi)} oi la pozitiile {[coordonateNoduri.index(nod) for nod in self.pieseOi]}\n"
        sir += f"Sunt  {len(self.pieseVulpi)} vulpi la pozitiile {[coordonateNoduri.index(nod) for nod in self.pieseVulpi]}\n"
        return sir

    def __str__(self):
        return self.sirAfisare()

    def deseneaza_grid(self, nodPiesaSelectata=None):
        """
        Functie care deseneaza tabla
        """
        ecran.fill(culoareEcran)
        for nod in coordonateNoduri:
            pygame.draw.circle(surface=ecran, color=culoareLinii, center=nod, radius=Graph.razaPct,
                               width=0)  # width=0 face un cerc plin

        for muchie in Graph.muchii:
            p0 = coordonateNoduri[muchie[0]]
            p1 = coordonateNoduri[muchie[1]]
            pygame.draw.line(surface=ecran, color=culoareLinii, start_pos=p0, end_pos=p1, width=5)
        for nod in self.pieseOi:
            ecran.blit(piesaAlba, (nod[0] - Graph.razaPiesa, nod[1] - Graph.razaPiesa))
        for nod in self.pieseVulpi:
            ecran.blit(piesaNeagra, (nod[0] - Graph.razaPiesa, nod[1] - Graph.razaPiesa))
        if nodPiesaSelectata:
            ecran.blit(piesaSelectata, (nodPiesaSelectata[0] - Graph.razaPiesa, nodPiesaSelectata[1] - Graph.razaPiesa))
        pygame.display.update()

    def deseneaza_castigator(self):
        """
        Functie care coloreaza piesele castigatoare
        """
        global piesaAlba, piesaNeagra
        ecran.fill(culoareEcran)
        castigator = self.final()
        if castigator == "V":
            piesaNeagra = piesaSelectata
        else:
            piesaAlba = piesaSelectata
        for nod in coordonateNoduri:
            pygame.draw.circle(surface=ecran, color=culoareLinii, center=nod, radius=Graph.razaPct,
                               width=0)  # width=0 face un cerc plin
        for muchie in Graph.muchii:
            p0 = coordonateNoduri[muchie[0]]
            p1 = coordonateNoduri[muchie[1]]
            pygame.draw.line(surface=ecran, color=culoareLinii, start_pos=p0, end_pos=p1, width=5)
        for nod in self.pieseOi:
            ecran.blit(piesaAlba, (nod[0] - Graph.razaPiesa, nod[1] - Graph.razaPiesa))
        for nod in self.pieseVulpi:
            ecran.blit(piesaNeagra, (nod[0] - Graph.razaPiesa, nod[1] - Graph.razaPiesa))
        if nodPiesaSelectata:
            ecran.blit(piesaSelectata, (nodPiesaSelectata[0] - Graph.razaPiesa, nodPiesaSelectata[1] - Graph.razaPiesa))
        pygame.display.update()

    def final(self):
        """
        Verific daca sunt in stare finala. Daca sunt mai putini de 9 oi, au castigat vulpile. Daca am oi pe pozitiile  [0, 1, 2, 3, 4, 5, 8, 9, 10],
        au castigat oile. Altfel, nu e stare finala
        """
        if len(self.pieseOi) < 9:  # daca am mai putin de 9 oi, au castigat vulpile
            return "V"
        if all(coordonateNoduri[i] in self.pieseOi for i in
               [0, 1, 2, 3, 4, 5, 8, 9, 10]):  # daca pe pozitiile din patratul de sus se afla numai oi, oile castiga
            return "O"
        return False  # nu e stare finala

    @classmethod
    def jucator_opus(cls, jucator):
        """
        Schimb jucatorul
        """
        return cls.JMAX if jucator == cls.JMIN else cls.JMIN

    def mutari(self, jucator):  # jucator = simbolul jucatorului care muta
        """
        Generez mutarile posibile
        """
        l_mutari = []

        if jucator == "O":
            for oaie in self.pieseOi:  # iau fiecare oaie (coordonatele ei)
                index_oaie = coordonateNoduri.index(oaie)  # indexul oii
                index_vecini_oaie = vecini_piesa(oaie)  # primesc indecsii vecinilor oii curente
                for vecin in index_vecini_oaie:
                    if not (vecin < index_oaie or (
                            abs(index_oaie - vecin) == 1)):  # daca vecinul e mai jos sau prea in dreapta/stanga, trec peste el
                        continue
                    if (oaie, vecin) in [(2, 3), (5, 6), (12, 13), (19, 20), (26, 27),
                                         (29, 30)]:  # mutari interzise pe care nu le acopera conditia de sus
                        continue
                    if coordonateNoduri[vecin] not in self.pieseOi + self.pieseVulpi:  # daca locul vecinului e liber
                        pieseOiCopie = copy.deepcopy(self.pieseOi)
                        pieseVulpiCopie = copy.deepcopy(self.pieseVulpi)
                        pieseOiCopie[:] = [x for x in pieseOiCopie if x != oaie]  # scot oaia de pozitia veche
                        pieseOiCopie.append(coordonateNoduri[vecin])  # mut oaia pe pozitia noua
                        jn = Joc(pieseOiCopie, pieseVulpiCopie)
                        l_mutari.append(jn)  # am salvat mutarea curenta
        else:  # cu vulpile
            table_noi = continuaManancaOi({self})  # vreau toate miscarile ca sa pot mananca mai multe oi in lant
            table_noi -= {self}
            if len(table_noi) > 0:
                l_mutari.extend(table_noi)  # jocurile in care am mancat oi

            else:  # caut sa mut vulpea intr-un loc liber
                for vulpe in self.pieseVulpi:  # iau fiecare vulpe (coordonatele ei)
                    index_vulpe = coordonateNoduri.index(vulpe)  # indexul vulpii
                    index_vecini_vulpe = vecini_piesa(vulpe)  # primesc indecsii vecinilor vulpii curente
                    for vecin in index_vecini_vulpe:
                        if coordonateNoduri[
                            vecin] not in self.pieseOi + self.pieseVulpi:  # daca locul vecinului e liber
                            pieseOiCopie = copy.deepcopy(self.pieseOi)
                            pieseVulpiCopie = copy.deepcopy(self.pieseVulpi)
                            pieseVulpiCopie[:] = [x for x in pieseVulpiCopie if
                                                  x != vulpe]  # scot vulpea de pozitia veche
                            pieseVulpiCopie.append(coordonateNoduri[vecin])  # mut vulpea pe pozitia noua
                            jn = Joc(pieseOiCopie, pieseVulpiCopie)
                            l_mutari.append(jn)  # am salvat mutarea curenta

        return l_mutari

    def estimeaza_scor(self, adancime, nr_estimare="1"):
        global timpi_JMAX, timpi_JMIN
        t_final = self.final()
        nr_oi = len(self.pieseOi)
        if nr_estimare == "1":
            if t_final == self.__class__.JMAX:  #calculatorul
                if self.__class__.JMAX == "V":  #cu vulpile
                    return self.__class__.scor_maxim - adancime
                else:  #oile
                    return self.__class__.scor_maxim - adancime + nr_oi

            elif t_final == self.__class__.JMIN:  #jucatorul
                if self.__class__.JMAX == "V":  #cu vulpile
                    return -self.__class__.scor_maxim + adancime
                else:  # cu oile
                    return -self.__class__.scor_maxim + adancime - nr_oi

            else:  # daca nu e final, tin cont de cate oi sunt pe pozitia finala
                nr_oi_final = len([coordonateNoduri[i] in self.pieseOi for i in
                                   [0, 1, 2, 3, 4, 5, 8, 9, 10]])  # verific cate oi am pe pozitii finale
                nr_oi_mancate = 20 - nr_oi  # numar oile mancate
                if self.__class__.JMAX == "V":  # daca calculatorul joaca cu vulpile
                    return nr_oi_mancate - nr_oi_final  # vreau sa fie cat mai putine oi
                else:  # cu oile, vreau sa fie cat mai multe
                    return nr_oi_final - nr_oi_mancate

        else:  # Estimarea 2 - la starea intermediara folosesc distanta Manhattan
            if t_final == self.__class__.JMAX:
                if self.__class__.JMAX == "V":
                    return self.__class__.scor_maxim - adancime
                else:
                    return self.__class__.scor_maxim - adancime + nr_oi
            elif t_final == self.__class__.JMIN:
                if self.__class__.JMAX == "V":
                    return -self.__class__.scor_maxim + adancime
                else:
                    return -self.__class__.scor_maxim + adancime - nr_oi

            else:  # Daca nu e final
                distantaTotala = 0
                if nr_oi:
                    distantaTotala = sum(abs(coordonateNoduri.index(nod) - val2) for nod, val2 in
                                         zip(self.pieseOi, [0, 1, 2, 3, 4, 5, 6, 7, 8]))
                nr_oi_mancate = 20 - nr_oi
                if self.__class__.JMAX == "V":  # daca calculatorul joaca cu vulpile
                    return 3 * nr_oi_mancate + distantaTotala  # vreau sa fie cat mai mare distanta
                else:  # cu oile, vreau sa fie cat mai mica
                    return -distantaTotala - nr_oi_mancate

    def __repr__(self):
        return self.sirAfisare()


def vecini_piesa(nod):
    """
    Cauta vecinii unei piese
    :return: lista de vecini
    """
    index_piesa_curenta = coordonateNoduri.index(nod)
    vecini = []
    for (x, y) in Graph.muchii:  # caut muchii cu o extremitate = index piesa curenta
        if x == index_piesa_curenta:
            vecini.append(y)
        if y == index_piesa_curenta:
            vecini.append(x)
    return vecini


class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta
    Are ca proprietate tabla de joc
    Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
    De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari() care ofera lista cu configuratiile posibile in urma mutarii unui jucator
    """

    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, scor=None):
        self.tabla_joc = tabla_joc
        self.j_curent = j_curent
        # adancimea in arborele de stari
        self.adancime = adancime
        # scorul starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.scor = scor
        # lista de mutari posibile din starea curenta
        self.mutari_posibile = []
        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        self.stare_aleasa = None

    def mutari(self):
        l_mutari = self.tabla_joc.mutari(self.j_curent)
        juc_opus = Joc.jucator_opus(self.j_curent)
        l_stari_mutari = [Stare(mutare, juc_opus, self.adancime - 1, parinte=self) for mutare in l_mutari]
        if len(l_stari_mutari) == 0:
            print("Remiza")
            exit()
        return l_stari_mutari

    def __str__(self):
        sir = str(self.tabla_joc) + "(Juc curent:" + self.j_curent + ")\n"
        return sir


def deseneaza_moduri_joc(display):
    """
    Alegerea modului de joc (j vs j, c vs j, c vs c)
    """
    btn_alg = GrupButoane(
        top=30,
        left=30,
        listaButoane=[
            Buton(display=display, w=80, h=30, text="J vs J", valoare="jvj"),
            Buton(display=display, w=80, h=30, text="C vs J", valoare="cvj"),
            Buton(display=display, w=80, h=30, text="C vs C", valoare="cvc")
        ],
        indiceSelectat=1)
    ok = Buton(display=display, top=310, left=30, w=40, h=30, text="ok", culoareFundal=(155, 0, 55))
    btn_alg.deseneaza()
    ok.deseneaza()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not btn_alg.selecteazaDupacoord(pos):
                    if ok.selecteazaDupacoord(pos):
                        display.fill((0, 0, 0))  # stergere ecran
                        return btn_alg.getValoare()
        pygame.display.update()


def deseneaza_alegeri(display, tabla_curenta):
    """
    Functie care deseneaza butoanele pt alegerea algoritmului, estimarii, piesei, jucatorul care incepe si nivelul de dificultate
    """
    btn_alg = GrupButoane(
        top=30,
        left=30,
        listaButoane=[
            Buton(display=display, w=80, h=30, text="minimax", valoare="minimax"),
            Buton(display=display, w=80, h=30, text="alphabeta", valoare="alphabeta")
        ],
        indiceSelectat=1)
    btn_estimare = GrupButoane(
        top=100,
        left=30,
        listaButoane=[
            Buton(display=display, w=100, h=30, text="Estimarea 1", valoare="1"),
            Buton(display=display, w=100, h=30, text="Estimarea 2", valoare="2")
        ],
        indiceSelectat=0)
    btn_juc = GrupButoane(
        top=170,
        left=30,
        listaButoane=[
            Buton(display=display, w=35, h=30, text="vulpi", valoare="V"),
            Buton(display=display, w=35, h=30, text="oi", valoare="O")
        ],
        indiceSelectat=0)
    btn_ordine = GrupButoane(
        top=240,
        left=30,
        listaButoane=[
            Buton(display=display, w=50, h=30, text="primul", valoare="1"),
            Buton(display=display, w=50, h=30, text="al doilea", valoare="2")
        ],
        indiceSelectat=0)
    btn_dificultate = GrupButoane(
        top=310,
        left=30,
        listaButoane=[
            Buton(display=display, w=70, h=30, text="Incepator", valoare="1"),
            Buton(display=display, w=70, h=30, text="Mediu", valoare="2"),
            Buton(display=display, w=70, h=30, text="Avansat", valoare="3")
        ],
        indiceSelectat=0)
    ok = Buton(display=display, top=380, left=30, w=40, h=30, text="ok", culoareFundal=(155, 0, 55))
    btn_alg.deseneaza()
    btn_estimare.deseneaza()
    btn_juc.deseneaza()
    btn_ordine.deseneaza()
    btn_dificultate.deseneaza()
    ok.deseneaza()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not btn_alg.selecteazaDupacoord(pos):
                    if not btn_estimare.selecteazaDupacoord(pos):
                        if not btn_juc.selecteazaDupacoord(pos):
                            if not btn_ordine.selecteazaDupacoord(pos):
                                if not btn_dificultate.selecteazaDupacoord(pos):
                                    if ok.selecteazaDupacoord(pos):
                                        display.fill((0, 0, 0))  # stergere ecran
                                        tabla_curenta.deseneaza_grid()
                                        return btn_juc.getValoare(), btn_alg.getValoare(), btn_estimare.getValoare(), btn_ordine.getValoare(), btn_dificultate.getValoare()
        pygame.display.update()


def afis_daca_final(stare_curenta):
    """
    Afisez in consola cine a castigat sau daca este remiza
    """
    final = stare_curenta.tabla_joc.final()
    if (final):
        if (final == "remiza"):
            print("Remiza")
        else:
            print("A castigat " + final)
            stare_curenta.tabla_joc.deseneaza_castigator()
            afisare_sfarsit()
        return True
    return False


def main():
    global ADANCIME_MAX, nr_noduri_generate, noduri_alphabeta, noduri_minmax, stare_actualizata
    global timpi_JMAX, timpi_JMIN
    tabla_curenta = Joc()
    tabla_curenta.setDisplay(ecran)
    alegere_pion, algoritm_ales, estimare, cine_incepe, dificultate = deseneaza_alegeri(ecran, tabla_curenta)

    if dificultate == 1:
        ADANCIME_MAX = 2
    elif dificultate == 2:
        ADANCIME_MAX = 3
    else:
        ADANCIME_MAX = 4
    print(tabla_curenta)
    Joc.JMIN = alegere_pion
    Joc.JMAX = 'V' if Joc.JMIN == 'O' else 'O'
    stare_curenta = Stare(tabla_curenta, Joc.JMIN if cine_incepe == "1" else Joc.JMAX, ADANCIME_MAX)
    tabla_curenta.deseneaza_grid()

    nodPiesaSelectata = False
    while True:
        if stare_curenta.j_curent == Joc.JMIN:
            timp_start = round(time.time() * 1000)  # timp
            # muta jucatorul
            # [MOUSEBUTTONDOWN, MOUSEMOTION,....]
            # l=pygame.event.get()
            facut_mutare = False
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    afisare_sfarsit()
                if event.type == pygame.QUIT:
                    afisare_sfarsit()
                    pygame.quit()  # inchide fereastra
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:  # click
                    pos = pygame.mouse.get_pos()  # coordonatele clickului

                    for nod in coordonateNoduri:
                        if distEuclid(pos, nod) <= Graph.razaPct:  # daca am dat click pe o piesa
                            if Joc.JMIN == "V":  # Joaca cu vulpile
                                piesa = piesaNeagra
                                pieseCurente = stare_curenta.tabla_joc.pieseVulpi  # piesele jucatorului
                                pieseOpuse = stare_curenta.tabla_joc.pieseOi  # piesele calculatorului
                                # print("vulpe 1")
                                if nod not in stare_curenta.tabla_joc.pieseVulpi:  # daca am apasat fie pe un spatiu liber sau pe o oaie
                                    index_vulpe1 = coordonateNoduri.index(stare_curenta.tabla_joc.pieseVulpi[0])
                                    index_vulpe2 = coordonateNoduri.index(stare_curenta.tabla_joc.pieseVulpi[1])

                                    oi_vulpe1 = cautaOi(index_vulpe1, stare_curenta.tabla_joc.pieseOi,
                                                        stare_curenta.tabla_joc.pieseVulpi)
                                    oi_vulpe2 = cautaOi(index_vulpe2, stare_curenta.tabla_joc.pieseOi,
                                                        stare_curenta.tabla_joc.pieseVulpi)  # caut daca pot manca oi
                                    # print("vulpe 2")
                                    if nodPiesaSelectata:  # a selectat o vulpe
                                        index_nod = coordonateNoduri.index(nod)
                                        if (len(oi_vulpe1) and index_nod not in map(lambda x: x[0],
                                                                                    oi_vulpe1)) or (
                                                len(oi_vulpe2) and index_nod not in map(lambda x: x[0],
                                                                                        oi_vulpe2)):
                                            break  # daca am oi de mancat si nu am selectat o oaie (nod)

                                        vulpe_selectata = coordonateNoduri.index(nodPiesaSelectata)
                                        oi_vulpe_selectata = cautaOi(vulpe_selectata, stare_curenta.tabla_joc.pieseOi,
                                                                     stare_curenta.tabla_joc.pieseVulpi)
                                        print(oi_vulpe_selectata)
                                        if len(oi_vulpe_selectata) == 0:  # mut vulpea in spatiu gol pt ca nu am oi de mancat
                                            if ((index_nod, vulpe_selectata) in Graph.muchii or (
                                                    vulpe_selectata,
                                                    index_nod) in Graph.muchii) and nod not in stare_curenta.tabla_joc.pieseOi:
                                                pieseCurente.remove(nodPiesaSelectata)
                                                pieseCurente.append(nod)
                                            else:
                                                break
                                        if len(oi_vulpe_selectata) > 1:  # are mai multe oi de mancat, deci trebuie sa aleaga 1
                                            if index_nod in map(lambda x: x[0],
                                                                oi_vulpe_selectata):  # daca pozitia selectata e o oaie pe care vulpea poate sa o manance
                                                pieseCurente.remove(nodPiesaSelectata)  # mut vulpea
                                                pieseOpuse.remove(coordonateNoduri[index_nod])  # mananca oaia
                                                pieseCurente.append(coordonateNoduri[oi_vulpe_selectata[index_nod][
                                                    1]])  # adaug pozitia noua a vulpii
                                                oi_vulpe_selectata = cautaOi(oi_vulpe_selectata[index_nod][1],
                                                                             pieseOpuse,
                                                                             pieseCurente)  # caut daca din pozitia noua vulpea poate sa continue sa manance oi
                                        while oi_vulpe_selectata == 1:
                                            pieseCurente.remove(nodPiesaSelectata)  # mut vulpea
                                            pieseOpuse.remove(
                                                coordonateNoduri[oi_vulpe_selectata[0][0]])  # mananca oaia
                                            pieseCurente.append(coordonateNoduri[oi_vulpe_selectata[0][
                                                1]])  # adaug pozitia noua a vulpii
                                            oi_vulpe_selectata = cautaOi(oi_vulpe_selectata[index_nod][1], pieseOpuse,
                                                                         pieseCurente)  # caut daca din pozitia noua vulpea poate sa continue sa manance oi
                                        facut_mutare = True
                                        stare_curenta.j_curent = Joc.jucator_opus(
                                            stare_curenta.j_curent)  # schimb jucatorul
                                        nodPiesaSelectata = False  # deselectez piesa

                                else:
                                    if nod in pieseCurente:
                                        if nodPiesaSelectata == nod:
                                            nodPiesaSelectata = False
                                        else:
                                            nodPiesaSelectata = nod
                            if Joc.JMIN == "O":  # Joaca cu oile
                                piesa = piesaAlba
                                pieseCurente = stare_curenta.tabla_joc.pieseOi
                                pieseOpuse = stare_curenta.tabla_joc.pieseVulpi
                                if nod not in stare_curenta.tabla_joc.pieseOi + stare_curenta.tabla_joc.pieseVulpi:  # daca am dat click pe un spatiu gol (unde pot sa mut)
                                    if nodPiesaSelectata:  # daca am selectat ce piesa sa mut
                                        coordonate_nod = coordonateNoduri.index(nod)
                                        coordonate_piesaSelectata = coordonateNoduri.index(nodPiesaSelectata)
                                        directie = [nodPiesaSelectata[0] - nod[0], nodPiesaSelectata[1] - nod[1]]
                                        if not (coordonate_piesaSelectata > coordonate_nod or abs(
                                                coordonate_nod - coordonate_piesaSelectata) == 1):  # daca fac o mutare nepermisa
                                            break

                                        if (coordonate_nod, coordonate_piesaSelectata) in Graph.muchii or (
                                                coordonate_piesaSelectata,
                                                coordonate_nod) in Graph.muchii:  # daca am cum sa ajung la nod
                                            pieseCurente.remove(nodPiesaSelectata)
                                            pieseCurente.append(nod)

                                            stare_curenta.j_curent = Joc.jucator_opus(
                                                stare_curenta.j_curent)  # am mutat, schimb jucatorul
                                            nodPiesaSelectata = False  # deselectez piesa
                                            facut_mutare = True
                                else:
                                    if nod in pieseCurente:
                                        if nodPiesaSelectata == nod:  # trebuie sa selectez ce sa mut
                                            nodPiesaSelectata = False
                                        else:  # e in regula
                                            nodPiesaSelectata = nod

                            if facut_mutare:
                                timp_mutare = round(time.time() * 1000) - timp_start
                                timpi_JMIN.append(timp_mutare)  # adaug in lista timpul pt mutarea actuala
                                print("Muta jucatorul")
                                print(f"Scor estimat: {stare_curenta.scor}")
                                print(f"Jucatorul a gandit timp de {timp_mutare} ms")
                                print("Tabla dupa mutarea jucatorului:")
                                print(str(stare_curenta))
                            if nodPiesaSelectata:
                                stare_curenta.tabla_joc.deseneaza_grid(nodPiesaSelectata)
                            else:
                                stare_curenta.tabla_joc.deseneaza_grid()
                            if afis_daca_final(stare_curenta):
                                return
            # -------------------------------- CAZ PT JMAX (MUTA CALCULATOR)
        else:
            print("Muta calculatorul")
            # preiau timpul in milisecunde de dinainte de mutare
            timp_start = (round(time.time() * 1000))
            nr_noduri_generate = 0
            if algoritm_ales == 'minimax':
                stare_actualizata = min_max(stare_curenta, estimare)
                noduri_minmax.append(nr_noduri_generate)
            else:  # tip_algoritm=="alphabeta"
                stare_actualizata = alpha_beta(-5000, 5000, stare_curenta, estimare)
                noduri_alphabeta.append(nr_noduri_generate)
            timp_mutare = (round(time.time() * 1000)) - timp_start
            timpi_JMAX.append(timp_mutare)
            print(f"Nr de noduri generate {nr_noduri_generate}. Scor estimat: {stare_actualizata.scor}")
            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
            print("Tabla dupa mutarea calculatorului\n" + str(stare_curenta))
            print("Calculatorul a \"gandit\" timp de " + str(timp_mutare) + " ms.")

            stare_curenta.tabla_joc.deseneaza_grid()
            if afis_daca_final(stare_curenta):
                return
            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)


def min_max(stare, tip_estimare="1"):
    """
    Algoritmul min_max
    """
    global nr_noduri_generate
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime, tip_estimare)
        nr_noduri_generate += 1
        return stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutari_scor = [min_max(mutare, tip_estimare) for mutare in stare.mutari_posibile]

    if stare.j_curent == Joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu scorul maxim
        stare.stare_aleasa = max(mutari_scor, key=lambda x: x.scor)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu scorul minim
        stare.stare_aleasa = min(mutari_scor, key=lambda x: x.scor)
    stare.scor = stare.stare_aleasa.scor
    return stare


def alpha_beta(alpha, beta, stare, tip_estimare="1"):
    """
    Algoritmul alphabeta
    """
    global nr_noduri_generate
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime, tip_estimare)
        nr_noduri_generate += 1
        return stare

    if alpha > beta:
        return stare  # este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()

    if stare.j_curent == Joc.JMAX:
        scor_curent = float('-inf')
        stare.mutari_posibile.sort(key=lambda x: x.tabla_joc.estimeaza_scor(stare.adancime, tip_estimare))
        for mutare in stare.mutari_posibile:
            # calculeaza scorul
            stare_noua = alpha_beta(alpha, beta, mutare, tip_estimare)

            if (scor_curent < stare_noua.scor):
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor
            if (alpha < stare_noua.scor):
                alpha = stare_noua.scor
                if alpha >= beta:
                    break

    elif stare.j_curent == Joc.JMIN:
        scor_curent = float('inf')
        stare.mutari_posibile.sort(key=lambda x: -x.tabla_joc.estimeaza_scor(stare.adancime, tip_estimare))
        for mutare in stare.mutari_posibile:

            stare_noua = alpha_beta(alpha, beta, mutare, tip_estimare)

            if (scor_curent > stare_noua.scor):
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor

            if (beta > stare_noua.scor):
                beta = stare_noua.scor
                if alpha >= beta:
                    break
    stare.scor = stare.stare_aleasa.scor

    return stare


def afisare_sfarsit():
    """
    Functie de afisare pt timpul total de rulare, numarul de mutari al jucatorului si al calculatorului, timpul maxim, minim, mediu, mediana
    :return:
    """
    global timpi_JMIN, timpi_JMAX
    print(f"Programul a rulat timp de {round(1000 * (time.time() - timp_inceput))}ms")
    print(f"JMIN a facut {len(timpi_JMIN)} mutari, iar JMAX a facut {len(timpi_JMAX)} mutari")
    print(
        f"Pt JMIN: Max: {max(timpi_JMIN)} ms, Min: {min(timpi_JMIN)}ms, Media: {mean(timpi_JMIN)}ms, Mediana: {median(timpi_JMIN)}ms")
    print(
        f"Pt JMAX: Max: {max(timpi_JMAX)} ms, Min: {min(timpi_JMAX)}ms, Media: {mean(timpi_JMAX)}ms, Mediana: {median(timpi_JMAX)}ms")
    if len(noduri_minmax):
        print(
            f"Alg minmax: Max: {max(noduri_minmax)}, Min: {min(noduri_minmax)}, Media: {mean(noduri_minmax)}, Mediana: {median(noduri_minmax)}ms")
    if len(noduri_alphabeta):
        print(
            f"Alg alphabeta: Max: {max(noduri_alphabeta)}, Min: {min(noduri_alphabeta)}, Media: {mean(noduri_alphabeta)}, Mediana: {median(noduri_alphabeta)}ms")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:  # daca apas din nou pe buton, continui jocul
                return


if __name__ == "__main__":
    timp_inceput = time.time()
    mod = deseneaza_moduri_joc(ecran)
    main()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
