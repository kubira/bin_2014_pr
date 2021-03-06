#!/bin/bash

################################################################################
#  Soubor:    testSequenceLife.sh                                              #
#  Autor:     Radim KUBIŠ, xkubis03                                            #
#  Vytvořeno: 22. dubna 2014                                                   #
#                                                                              #
#  Projekt do předmětu Biologií inspirované počítače (BIN).                    #
#                                                                              #
#  SKRIPT PRO SPUŠTĚNÍ SADY TESTŮ SEKVENČNÍHO VÝPOČTU CA HRY LIFE              #
#                                                                              #
#  Test je spuštěn na základě níže nastavených konstant/proměnných.            #
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

# Cyklus zvyšujícího se rozměru CA
while [ $actual_size -le $max_size ]
do
    # Cyklus počtu měření
    for meas in $(seq 1 $measurements)
    do
        # Spuštění jednoho měření
        ./sequenceLife.py $actual_size $steps_of_ca
    done

    # Zvýšení rozměru CA
    actual_size=$((actual_size+size_step))
done
