#!/usr/bin/env python3.4

################################################################################
#  Soubor:    sequenceLife.py                                                  #
#  Autor:     Radim KUBIŠ, xkubis03                                            #
#  Vytvořeno: 21. dubna 2014                                                   #
#                                                                              #
#  Projekt do předmětu Biologií inspirované počítače (BIN).                    #
#                                                                              #
#  SEKVENČNÍ VÝPOČET CA HRY LIFE                                               #
#                                                                              #
#  Skript provede JEDNO měření délky trvání  sekvenčního výpočtu nových stavů  #
#  CA.  Parametr SIZE velikosti CA  je  jediným POVINNÝM parametrem příkazové  #
#  řádky.  Další NEPOVINNÝ parametr STEPS  určuje počet vypočtených  kroků CA  #
#  pro  jeden  běh  (defaultní  hodnota  je   nastavena  konstantou/proměnnou  #
#  STEPS_OF_CA).                                                               #
#                                                                              #
#  Výstup je ve formátu CSV:                                                   #
#      <rozměr_CA>;<délka_trvání_výpočtu>                                      #
#                                                                              #
################################################################################

# Import modulu OS
import os
# Import systémového modulu
import sys
# Import modulu času
import time
# Import numerického modulu
import numpy
# Import funkcí pro CA
from ca.functions import getNewLifeValue

# Počet kroků CA (defaultní)
STEPS_OF_CA = 100

# ---------------------------------------------------------------------------- #
# Funkce pro výpis způsobu použití programu                                    #
# ---------------------------------------------------------------------------- #
def printUsage(program):
    # Výpis způsobu použití
    print("Usage: %s SIZE [STEPS]\n" % program)
    print("\tSIZE  - number of rows and columns for CA (required)")
    print("\tSTEPS - number of steps for CA (optional, default: %d)\n" % STEPS_OF_CA)

# Pokud bylo zadáno více argumentů, než je očekáváno
if len(sys.argv) > 3:
    # Výpis chyby
    sys.stderr.write("ERROR: Too many arguments\n")
    # Vyprázdnění chybového výstupního bufferu
    sys.stderr.flush()
    # Výpis způsobu použití
    printUsage(sys.argv[0])
    # Skript končí s chybou
    sys.exit(1)

# ZÍSKÁNÍ ROZMĚRU POLE CA PRO BĚH
try:
    # Uložení rozměru
    numberOfRows = int(sys.argv[1])

# Pokud nebyl parametr rozměru zadán
except IndexError:
    # Výpis chyby
    sys.stderr.write("ERROR: Required argument SIZE is not set\n")
    # Vyprázdnění chybového výstupního bufferu
    sys.stderr.flush()
    # Výpis způsobu použití
    printUsage(sys.argv[0])
    # Skript končí s chybou
    sys.exit(1)

# Pokud argument rozměru neobsahuje pouze číslice
except ValueError:
    # Výpis chyby
    sys.stderr.write("ERROR: Required argument SIZE is not a number: '%s'\n" % sys.argv[1])
    # Vyprázdnění chybového výstupního bufferu
    sys.stderr.flush()
    # Výpis způsobu použití
    printUsage(sys.argv[0])
    # Skript končí s chybou
    sys.exit(1)

# Pokud má program zadané oba argumenty
if len(sys.argv) == 3:
    # Získání počtu kroků výpočtu CA
    try:
        # Uložení počtu kroků
        STEPS_OF_CA = int(sys.argv[2])
    
    # Pokud argument počtu kroků neobsahuje pouze číslice
    except ValueError:
        # Výpis chyby
        sys.stderr.write("ERROR: Optional argument STEPS is not a number: '%s'\n" % sys.argv[2])
        # Vyprázdnění chybového výstupního bufferu
        sys.stderr.flush()
        # Výpis způsobu použití
        printUsage(sys.argv[0])
        # Skript končí s chybou
        sys.exit(1)

# Počet sloupců je stejný jako počet řádků
numberOfCols = numberOfRows

# První/A pomocné pole reprezentující CA,
# s rozměry numberOfRows a numberOfCols,
# naplnění náhodnými hodnotami 0/1
fieldA = numpy.random.randint(2, size=(numberOfRows, numberOfCols))
# Druhé/B pomocné pole reprezentující CA,
# kopie prvního
fieldB = numpy.copy(fieldA)

# Uložení počátečního času běhu
startTime = time.process_time()

# Cyklus počtu kroků CA
for step in range(0, STEPS_OF_CA):
    # Výpis CA na standardní výstup
    # os.system('clear')
    # print(fieldA)
    # time.sleep(1)

    # Cyklus řádků
    for row in range(0, numberOfRows):
        # Cyklus sloupců
        for col in range(0, numberOfCols):
            # Uložení nové hodnoty jedné buňky
            fieldB[row][col] = getNewLifeValue(fieldA, row, col, numberOfCols, numberOfRows)

    # Prohození pomocných polí A/B
    fieldA, fieldB = fieldB, fieldA

# Uložení koncového času jednoho běhu
endTime = time.process_time()

# Tisk rozměru CA a času trvání běhu
print("%d;%5.3f" % (numberOfRows, (endTime-startTime)))
# Vyprázdnění bufferu standardního výstupu
sys.stdout.flush()
