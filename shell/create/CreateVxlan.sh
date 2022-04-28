#!/bin/bash

VXLAN_NAME=$1
GROUP_IP=$2
LOCAL_IP=$3
ETH0=$4

sudo ip link add "$VXLAN_NAME" type vxlan id 42 dstport 4789 group ${GROUP_IP} local ${LOCAL_IP} dev ${ETH0} 
