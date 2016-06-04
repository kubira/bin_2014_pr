################################################################################
#  Soubor:    functions.py                                                     #
#  Autor:     Radim KUBIŠ, xkubis03                                            #
#  Vytvořeno: 22. dubna 2014                                                   #
#                                                                              #
#  Projekt do předmětu Biologií inspirované počítače (BIN).                    #
#                                                                              #
#  MODUL S FUNKCEMI PRO CA                                                     #
#                                                                              #
#  Modul obsahuje společné funkce pro několik samostatných skriptů s CA.       #
#                                                                              #
################################################################################

# Import modulu numerických výpočtů
import numpy
# Import tabulky pravidel Langtonovy smyčky
from ca.constants import langtonLoopRulesTable, bylLoopRulesTable

# ---------------------------------------------------------------------------- #
# Funkce vracející novou hodnotu buňky CA hry Life                             #
#                                                                              #
# CAField - pole polí reprezentující CA                                        #
# rowId   - číslo řádku buňky                                                  #
# colId   - číslo sloupce buňky                                                #
# nRows   - počet řádků CA                                                     #
# mCols   - počet sloupců CA                                                   #
# ---------------------------------------------------------------------------- #
def getNewLifeValue(CAField, rowId, colId, nRows, mCols):
    # Navrácení součtu sousedů 8-okolí
    numberOfAliveNeighbors = numpy.sum([
        CAField[rowId-1][colId-1],                # Soused vlevo nahoře
        CAField[rowId-1][colId],                  # Soused nahoře
        CAField[rowId-1][(colId+1)%mCols],        # Soused vpravo nahoře
        CAField[rowId][colId-1],                  # Soused vlevo
        CAField[rowId][(colId+1)%mCols],          # Soused vpravo
        CAField[(rowId+1)%nRows][colId-1],        # Soused vlevo dole
        CAField[(rowId+1)%nRows][colId],          # Soused dole
        CAField[(rowId+1)%nRows][(colId+1)%mCols] # Soused vpravo dole
    ])

    # Pokud je buňka živá
    if CAField[rowId][colId] == 1:
        # Pokud má méně než 2 živé sousedy
        if numberOfAliveNeighbors < 2:
            # Umírá
            return 0

        # Pokud má 2 nebo 3 živé sousedy
        elif numberOfAliveNeighbors == 2 or numberOfAliveNeighbors == 3:
            # Zůstává živá
            return 1

        # Pokud má více než 3 žívé sousedy
        elif numberOfAliveNeighbors > 3:
            # Umírá
            return 0

    # Pokud je buňka mrtvá a má právě 3 živé sousedy
    elif numberOfAliveNeighbors == 3:
        # Ožívá
        return 1
    
    # Jinak
    else:
        # Zůstává mrtvá
        return 0

# ---------------------------------------------------------------------------- #
# Funkce vracející novou hodnotu buňky CA pro Langtonovu smyčku                #
#                                                                              #
# CAField - pole polí reprezentující CA                                        #
# rowId   - číslo řádku buňky                                                  #
# colId   - číslo sloupce buňky                                                #
# nRows   - počet řádků CA                                                     #
# mCols   - počet sloupců CA                                                   #
# ---------------------------------------------------------------------------- #
def getNewLangtonLoopValue(CAField, rowId, colId, nRows, mCols):
    # Pokud se jedná o hraniční buňku
    if rowId == 0 or colId == 0 or rowId == (nRows-1) or colId == (mCols-1):
        # Zůstává v buňce stará hodnota
        return CAField[rowId][colId]
    # Vytvoření klíče do tabulky pravidel ze 4-okolí buňky
    neighbors = str(CAField[rowId-1][colId])+str(CAField[rowId][(colId+1)%mCols])+str(CAField[(rowId+1)%nRows][colId])+str(CAField[rowId][colId-1])
    try:
        # Navrácení nové hodnoty buňky dle tabulky pravidel
        return langtonLoopRulesTable[CAField[rowId][colId]][neighbors]
    except KeyError:
        # Pokud neexistuje pravidlo, vrací se aktuální hodnota
        return CAField[rowId][colId]

# ---------------------------------------------------------------------------- #
# Funkce vracející novou hodnotu buňky CA pro Bylovu smyčku                    #
#                                                                              #
# CAField - pole polí reprezentující CA                                        #
# rowId   - číslo řádku buňky                                                  #
# colId   - číslo sloupce buňky                                                #
# nRows   - počet řádků CA                                                     #
# mCols   - počet sloupců CA                                                   #
# ---------------------------------------------------------------------------- #
def getNewBylLoopValue(CAField, rowId, colId, nRows, mCols):
    # Vytvoření klíče do tabulky pravidel ze 4-okolí buňky
    neighbors = str(CAField[rowId-1][colId])+str(CAField[rowId][(colId+1)%mCols])+str(CAField[(rowId+1)%nRows][colId])+str(CAField[rowId][colId-1])

    try:
        # Navrácení nové hodnoty buňky dle tabulky pravidel
        return bylLoopRulesTable[CAField[rowId][colId]][neighbors]
    except KeyError:
        # Pokud neexistuje pravidlo, hodnota zůstává
        return CAField[rowId][colId]
