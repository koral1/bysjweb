#!/bin/bash
NETNS_NAME=$1

sudo ip netns del ${NETNS_NAME}