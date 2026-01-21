#!/bin/bash

GPIO_SHUTDOWN=5

REBOOT_MIN=200
REBOOT_MAX=600

echo "$GPIO_SHUTDOWN" > /sys/class/gpio/export
echo "in" > /sys/class/gpio/gpio$GPIO_SHUTDOWN/direction

while true; do
  val=$(cat /sys/class/gpio/gpio$GPIO_SHUTDOWN/value)

  if [ "$val" = "1" ]; then
    start=$(date +%s%3N)

    while [ "$(cat /sys/class/gpio/gpio$GPIO_SHUTDOWN/value)" = "1" ]; do
      sleep 0.05
    done

    duration=$(( $(date +%s%3N) - start ))

    if [ $duration -gt $REBOOT_MAX ]; then
      poweroff
    elif [ $duration -gt $REBOOT_MIN ]; then
      reboot
    fi
  fi

  sleep 0.1
done
