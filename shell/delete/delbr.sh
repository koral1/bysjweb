#!/bin/bash
BRIDGE_NAME=$1

# sudo brctl delbr ${BRIDGE_NAME}
sudo ip link delete ${BRIDGE_NAME}