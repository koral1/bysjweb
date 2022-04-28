#!/bin/bash


sh CreateNetns.sh net1
sh CreateBr.sh br1
sh CreateVethPair.sh veth1 veth1_p
sh VethToNetns.sh veth1 net1
sh MasterBr.sh veth1_p br1
sh AddIP.sh veth1 192.168.1.1/24 net1 
sh AddIP.sh br1 192.168.1.2/24
sh Setup.sh veth1 net1 
sh Setup.sh veth1_p
sh Setup.sh br1


# 查看ip 命令为 ip a

