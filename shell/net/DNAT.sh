#!/bin/bash

#内部虚拟网络访问外网时,将namespace请求中的IP换成外部网络认识的ip,进而达到正常访问外部网络的效果
DEVICE_IP=$1
BRIDGE_NAME=$2

sudo iptables -t nat -A POSTROUTING -s ${DEVICE_IP} ! -o ${BRIDGE_NAME} -j MASQUERADE