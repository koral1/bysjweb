#!/bin/bash

if [ $# -eq 1 ]; then
    DEVICE_NAME=$1

    sudo ip link set ${DEVICE_NAME} up 
elif [ $# -eq 2 ];then
    DEVICE_NAME=$1
    NETNS_NAME=$2

    sudo ip netns exec ${NETNS_NAME} ip link set ${DEVICE_NAME} up
fi

