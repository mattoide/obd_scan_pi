#!/bin/bash

#update and install required system packages
sudo apt update && sudo apt upgrade && sudo apt install python3-pip python3.10-venv install bluetooth bluez python-bluez expect &&

sudo mkdir -p /etc/systemd/system/getty@tty1.service.d/ &&

sudo su
echo "[Service]" >> /etc/systemd/system/getty@tty1.service.d/autologin.conf &&
echo "ExecStart=" >> /etc/systemd/system/getty@tty1.service.d/autologin.conf &&
echo "ExecStart=-/sbin/agetty --autologin obd --noclear %I $TERM" >> /etc/systemd/system/getty@tty1.service.d/autologin.conf && 
exit

sudo systemctl daemon-reload &&
sudo systemctl restart getty@tty1.service



#mkdir ~/obd/obd_scan && cd ~/obd/obd_scan
#sudo scarica programma python da github &&


python3 -m venv .venv &&
source .venv/bin/activate
