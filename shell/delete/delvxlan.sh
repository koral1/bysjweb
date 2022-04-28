#!/bin/bash
VXLAN_NAME=$1

sudo ip link delete ${VXLAN_NAME}