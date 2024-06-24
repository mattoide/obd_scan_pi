#!/bin/bash
#obdAdapter="B8:27:EB:EE:AD:D5" #Address of obdAdapter
obdAdapter=$1
sudo rfcomm bind 0 $obdAdapter
echo "Trying to pair to: " $obdAdapter


obdAdapterDetected ()
{
   # Search for OBD-II
   hcitool rssi $obdAdapter &>/dev/null
   ret=$?

   # If search was unsuccessful,
   if [ $ret -ne 0 ]
   then
      #
      # if Bluetooth is disabled, this should re-enable it
      ###echo "Unblocking bluetooth which should re-enable it"
      ###sudo rfkill unblock bluetooth

      # Add it
      echo "Could not find the adapter. Trying rfcomm to connect to channel 1"
      sudo rfcomm release rfcomm0
      sudo rfcomm connect rfcomm0 $obdAdapter 1 &>/dev/null

      # Note: the return code of rfcomm will almost always be 0,
      # so don't rely on it if you are looking for failed connections,
      # instead wait 5 seconds for rfcomm to connect, then check
      # connection again. Note this is not fool proof as an rfcomm
      # command taking longer than 5 seconds could break this program,
      # however, it generally only takes 2 seconds.
      sleep 5
      hcitool rssi $obdAdapter &>/dev/null
      ret=$?
   fi;
}

# run an infinite loop
while :
do
   obdAdapterDetected $obdAdapter
done
echo "FINITO"

python3 start_obd.py