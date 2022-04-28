#!/bin/bash

if [ $# -eq 2 ]; then
    ORIGINAL_NAME=$1
    CHANGED_NAME=$2

    sudo ip link set ${ORIGINAL_NAME} name "$CHANGED_NAME"
elif [ $# -eq 3 ];then
    ORIGINAL_NAME=$1
    CHANGED_NAME=$2
    NETNS_NAME=$3

    sudo ip netns exec ${NETNS_NAME} ip link set ${ORIGINAL_NAME} name "$CHANGED_NAME"
fi

