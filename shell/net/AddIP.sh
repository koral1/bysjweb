#!/bin/bash

if [ $# -eq 3 ]; then
    DEVICE_NAME=$1
    DEVICE_IP=$2
    NETNS_NAME=$3
sudo ip netns exec ${NETNS_NAME} ip addr add ${DEVICE_IP} dev ${DEVICE_NAME}

elif [ $# -eq 2 ];then
    DEVICE_NAME=$1
    DEVICE_IP=$2
sudo ip addr add ${DEVICE_IP} dev ${DEVICE_NAME}
fi