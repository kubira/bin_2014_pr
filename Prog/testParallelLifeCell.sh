#!/bin/bash

################################################################################
#  Soubor:    testParallelLifeCell.sh                                          #
#  Autor:     Radim KUBIŠ, xkubis03                                            #
#  Vytvořeno: 8. května 2014                                                   #
#                                                                              #
#  Projekt do předmětu Biologií inspirované počítače (BIN).                    #
#                                                                              #
#  SKRIPT SPOUŠTÍ SADU TESTŮ PARALELNÍHO (BUNĚČNÉHO) VÝPOČTU CA HRY LIFE       #
#                                                                              #
#  Skript má jeden nepovinný parametr, kterým je počet paralelních procesorů.  #
#  Test je spuštěn  na  základě  níže nastavených  konstant/proměnných, popř.  #
#  zadaného počtu paralelních procesorů jako argumentu skriptu.                #
#                                                                              #
################################################################################

# Počet kroků výpočtu CA
steps_of_ca=100
# Počet běhů pro každý rozměr CA
measurements=10
# Startovní rozměr CA
actual_size=10
# Konečný rozměr CA
max_size=500
# Krok zvýšení rozměru CA
size_step=10

# Počet MPI procesorů (defaultní)
processors=8

# Pokud byl zadán nějaký parametr
if [ $# -gt 0 ]; then
    # První parametr je počet paralelních procesorů,
    # další parametry jsou ignorovány
    processors=$1
fi

# Kontrola počtu paralelních procesorů
if [ $processors -lt 3 ]; then
    # Výpis chyby
    echo "# of processors is not suitable for parallel run: '$processors'"
    # Ukončení skriptu s chybou
    exit 1
fi

# Tisk informace o počtu MPI procesorů
echo "# of processors: $processors"

# Cyklus zvyšujícího se rozměru CA
while [ $actual_size -le $max_size ]
do
    # Cyklus počtu měření
    for meas in $(seq 1 $measurements)
    do
        # Spuštění jednoho měření
        mpiexec -n $processors ./parallelLifeCell.py $actual_size $steps_of_ca
    done

    # Zvýšení rozměru CA
    actual_size=$((actual_size+size_step))
done
