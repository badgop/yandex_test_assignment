#!/bin/bash


CAN_PORT="vcan0"

sudo modprobe vcan
sudo ip link add dev $CAN_PORT type vcan
sudo ip link set up $CAN_PORT
