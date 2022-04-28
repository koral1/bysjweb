#!/bin/bash

NETNS_NAME=$1

sudo ip netns exec ${NETNS_NAME} nc -lp 80