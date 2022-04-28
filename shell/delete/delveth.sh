#!/bin/bash
VETH_NAME=$1

sudo ip link delete ${VETH_NAME}
