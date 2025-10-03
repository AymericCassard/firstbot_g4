#!/bin/bash

# Vérifier qu'un argument a été fourni
if [ -z "$1" ]; then
    echo "Usage: $0 <nom>"
    exit 1
fi

NOM="$1"

case "$NOM" in
    "suivi_ligne")
        echo "Lancement du suivi de ligne"
        python3 suivi_ligne.py follow_line
        ;;
    "free_ride")
        echo "Lancement du suivi de ligne"
        python3 suivi_ligne.py free_ride
        ;;
    "goto")
        echo "Lancement du goto"
        python3 goto.py
        ;;
    "affichage_plot")
        echo "Affichage dans un plot en cours..."
        python3 affichage_plot.py
        ;;
    "affichage_map")
        echo "Affichage de la map en cours..."
        python3 affichage_map.py
        ;;
    *)
        echo "Nom non reconnu: $NOM"
        ;;
esac
