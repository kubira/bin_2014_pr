#!/usr/bin/env python3.4

################################################################################
#  Soubor:    parallelBylCell.py                                               #
#  Autor:     Radim KUBIŠ, xkubis03                                            #
#  Vytvořeno: 8. května 2014                                                   #
#                                                                              #
#  Projekt do předmětu Biologií inspirované počítače (BIN).                    #
#                                                                              #
#  PARALELNÍ VÝPOČET CA BYLOVY SMYČKY (PO JEDNÉ BUŇCE)                         #
#                                                                              #
#  Skript provede JEDNO měření délky trvání  paralelního výpočtu  nových stavů #
#  CA. Paralelní procesory zpracovávají nové hodnoty po jedné  buňce a  každou #
#  novou buňku odesílají root procesoru. Parametr SIZE velikosti CA je jediným #
#  POVINNÝM parametrem příkazové řádky. Další NEPOVINNÝ parametr  STEPS určuje #
#  počet vypočtených kroků CA  pro jeden běh  (defaultní hodnota  je nastavena #
#  konstantou/proměnnou STEPS_OF_CA).                                          #
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
# Import modulu MPI pro paralelní výpočty
from mpi4py import MPI
# Import funkcí pro CA
from ca.functions import getNewBylLoopValue
# Import konstant pro CA
from ca.constants import bylLoop

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

# Získání komunikátoru z MPI
comm = MPI.COMM_WORLD
# Získání ID paralelního procesoru
rank = comm.Get_rank()
# Získání celkového počtu paralelních procesorů
numberOfProcessors = comm.Get_size()

# Kontrola, zda je skript spuštěn paralelně
if numberOfProcessors < 3:
    # Root procesor vypíše chybu
    if rank == 0:
        # Tisk chyby
        sys.stderr.write("ERROR: Script is not start as parallel\n")
    # Ukončení všech procesorů s chybou
    sys.exit(1)

# Pokud bylo zadáno více argumentů, než je očekáváno
if len(sys.argv) > 3:
    # Root procesor vypíše chybu a způsob použití
    if rank == 0:
        # Výpis chyby
        sys.stderr.write("ERROR: Too many arguments\n")
        # Vyprázdnění chybového výstupního bufferu
        sys.stderr.flush()
        # Výpis způsobu použití
        printUsage(sys.argv[0])
    # Každý procesor končí s chybou
    sys.exit(1)

# ZÍSKÁNÍ ROZMĚRU POLE CA PRO BĚH
try:
    # Uložení rozměru
    numberOfRows = int(sys.argv[1])

# Pokud nebyl parametr rozměru zadán
except IndexError:
    # Root procesor vypíše chybu a způsob použití
    if rank == 0:
        # Výpis chyby
        sys.stderr.write("ERROR: Required argument SIZE is not set\n")
        # Vyprázdnění chybového výstupního bufferu
        sys.stderr.flush()
        # Výpis způsobu použití
        printUsage(sys.argv[0])
    # Každý procesor končí s chybou
    sys.exit(1)

# Pokud argument rozměru neobsahuje pouze číslice
except ValueError:
    # Root procesor vypíše chybu a způsob použití
    if rank == 0:
        # Výpis chyby
        sys.stderr.write("ERROR: Required argument SIZE is not a number: '%s'\n" % sys.argv[1])
        # Vyprázdnění chybového výstupního bufferu
        sys.stderr.flush()
        # Výpis způsobu použití
        printUsage(sys.argv[0])
    # Každý procesor končí s chybou
    sys.exit(1)

# Pokud má program zadané oba argumenty
if len(sys.argv) == 3:
    # Získání počtu kroků výpočtu CA
    try:
        # Uložení počtu kroků
        STEPS_OF_CA = int(sys.argv[2])
    
    # Pokud argument počtu kroků neobsahuje pouze číslice
    except ValueError:
        # Root procesor vypíše chybu a způsob použití
        if rank == 0:
            # Výpis chyby
            sys.stderr.write("ERROR: Optional argument STEPS is not a number: '%s'\n" % sys.argv[2])
            # Vyprázdnění chybového výstupního bufferu
            sys.stderr.flush()
            # Výpis způsobu použití
            printUsage(sys.argv[0])
        # Každý procesor končí s chybou
        sys.exit(1)

# Počet sloupců je stejný jako počet řádků
numberOfCols = numberOfRows

# Pokud jsem root procesor
if rank == 0:
    # První/A pomocné pole reprezentující CA,
    # s rozměry numberOfRows a numberOfCols,
    # naplnění nulami
    fieldA = numpy.zeros((numberOfRows, numberOfCols), dtype=numpy.int)

    # ULOŽENÍ BYLOVY SMYČKY DO STŘEDU POLE
    # Výpočet levého horního rohu počátku smyčky
    topLeftRowIndex = (int(numberOfRows/2)-2) # Číslo řádku
    topLeftColIndex = (int(numberOfCols/2)-2) # Číslo sloupce
    # Výpočet čísla sloupce za smyčkou
    colBehindLoopIndex = (int(numberOfCols/2)+2)
    # Výpočet řádku pod smyčkou
    rowUnderLoopIndex = topLeftRowIndex+4
    # Index do Bylovy smyčky
    loopIndex = 0
    # Uložení hodnot smyčky
    for rowIndex in range(topLeftRowIndex, rowUnderLoopIndex):
        # Uložení jednoho řádku smyčky
        fieldA[rowIndex][topLeftColIndex:colBehindLoopIndex] = bylLoop[loopIndex]
        # Inkrementace řádku smyčky
        loopIndex += 1

    # Zkopírování pole CA pro nové hodnoty
    fieldB = numpy.copy(fieldA)

    # Výpis CA na standardní výstup
    # os.system('clear')
    # print(fieldA)
    # time.sleep(1)

    # Čekání na bariéře pro synchronizaci všech procesorů
    comm.Barrier()

    # Uložení počátečního času algoritmu
    startTime = time.time()

    # Cyklus počtu kroků CA
    for step in range(0, STEPS_OF_CA):
        # Odeslání aktuálního stavu CA všem výpočetním procesorům
        comm.bcast(fieldA, root=0)

        # Příjem vypočtených nových buněk (po jedné)
        for cellIndex in range(0, numberOfRows*numberOfCols):
            # Výpočet souřadnic buňky
            rowIndex = int(cellIndex/numberOfRows)
            colIndex = cellIndex%numberOfCols
            # Buffer pro novou hodnotu
            newCell = None
            # Příjem nové buňky
            fieldB[rowIndex][colIndex] = comm.recv(newCell, source=MPI.ANY_SOURCE, tag=cellIndex)

        # Prohození nového a starého pole CA
        fieldA, fieldB = fieldB, fieldA

        # Výpis CA na standardní výstup
        # os.system('clear')
        # print(fieldA)
        # time.sleep(1)

    # Čekání na bariéře pro synchronizaci všech procesorů
    comm.Barrier()

    # Uložení koncového času algoritmu
    endTime = time.time()

    # Tisk rozměru CA a čas trvání algoritmu
    print("%d;%5.3f" % (numberOfRows, (endTime-startTime)))
    # Vyprázdnění bufferu standardního výstupu
    sys.stdout.flush()

else:
    # Nastavení posunu na další řádek
    increment = (numberOfProcessors - 1)
    
    # Proměnná pro hodnotu nové buňky
    newCell = None
    
    # Čekání na bariéře pro synchronizaci všech procesorů
    comm.Barrier()

    # Cyklus počtu kroků CA
    for step in range(0, STEPS_OF_CA):
        # Vyprázdnění proměnné pro pole CA
        fieldCA = None
        # Příjem aktuálního stavu CA
        fieldCA = comm.bcast(fieldCA, root=0)

        # Nastavení indexu buňky,
        # od které se bude provádět výpočet
        cellIndex = (rank - 1)

        # Cyklus výpočtu nových hodnot buněk přidělených procesoru
        while cellIndex < (numberOfRows*numberOfCols):
            # Výpočet souřadnic buňky
            rowIndex = int(cellIndex/numberOfRows)
            colIndex = cellIndex%numberOfCols

            # Výpočet a uložení jedné nové hodnoty buňky
            newCell = getNewBylLoopValue(fieldCA, rowIndex, colIndex, numberOfCols, numberOfRows)

            # Odeslání nového řádku root procesoru
            comm.send(newCell, dest=0, tag=cellIndex)

            # Posun na další řádek ke zpracování
            cellIndex += increment

    # Čekání na bariéře pro synchronizaci všech procesorů
    comm.Barrier()
