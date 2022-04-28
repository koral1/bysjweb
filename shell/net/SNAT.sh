#!/bin/bash
#外部网络若访问tcp的8088端口,则就转发到"+Bridgename+"的80端口。"+"地址为"+ipVeth+":80

BRIDGE_NAME=$1
DEVICE_IP=$2

sudo iptables -t nat -A PREROUTING  ! -i ${BRIDGE_NAME} -p tcp -m tcp --dport 8088 -j DNAT --to-destination ${DEVICE_IP}:80