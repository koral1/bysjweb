#!/bin/bash

VETH_NAME=$1
NETNS_NAME=$2

sudo ip link set ${VETH_NAME} netns ${NETNS_NAME}