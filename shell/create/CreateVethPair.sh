#!/bin/bash
VETH_1=$1
VETH_p=$2

sudo ip link add "$VETH_1" type veth peer name "$VETH_p"