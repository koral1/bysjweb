#!/bin/bash

DEVICE_NAME=$1
BRIDGE_NAME=$2

sudo ip link set dev ${DEVICE_NAME} master ${BRIDGE_NAME}