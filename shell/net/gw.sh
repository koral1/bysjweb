#!/bin/bash
#默认网关

NETNS_NAME=$1
IP_BR=$2
VETH_NAME=$3

sudo ip netns exec ${NETNS_NAME} route add default gw ${IP_BR} ${VETH_NAME}