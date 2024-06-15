#!/bin/bash

#update and install required system packages
sudo apt update && sudo apt upgrade && sudo apt install python3-pip python3.10-venv install bluetooth bluez python-bluez &&

#mkdir ~/obd/obd_scan && cd ~/obd/obd_scan
#sudo scarica programma python da github &&
#python3 -m venv .venv &&
#source .venv/bin/activate

# obd device name
TARGET_NAME="NomeDispositivoOBD"

#
TARGET_MAC_ADDRESS=""

#
echo "Scanning for Bluetooth devices..."
# Inizializza il comando bluetoothctl per cercare i dispositivi
bluetoothctl scan on &
SCAN_PID=$!
# Aspetta per un periodo di tempo per raccogliere i dispositivi (modificabile)
sleep 10
# Termina la scansione
kill $SCAN_PID
# Ottieni la lista dei dispositivi trovati
devices=$(bluetoothctl devices)

# Trova l'indirizzo MAC del dispositivo con il nome specificato
while IFS= read -r line; do
    if [[ "$line" == *"$TARGET_NAME"* ]]; then
        TARGET_MAC_ADDRESS=$(echo "$line" | awk '{print $2}')
        break
    fi
done <<< "$devices"

if [ -z "$TARGET_MAC_ADDRESS" ]; then
    echo "Device with name $TARGET_NAME not found."
    exit 1
else
    echo "Found device $TARGET_NAME with MAC address $TARGET_MAC_ADDRESS."
fi



# Se il dispositivo è stato trovato, esegui la connessione
if [ -n "$TARGET_MAC_ADDRESS" ]; then
# pairing and connecting to bt
echo -e "power on\nscan off\npair $TARGET_MAC_ADDRESS\ntrust $TARGET_MAC_ADDRESS\nconnect $TARGET_MAC_ADDRESS\nquit" | bluetoothctl
fi
