#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: ./generate_route.sh <chemin_vers_fichier_gpx> <distance_cible_km> <denivele_max_m>"
    exit 1
fi

python3 scripts/generate_route.py "$1" "$2"
