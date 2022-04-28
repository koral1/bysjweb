#!/bin/bash
NETNS_NAME=$1

sudo ip netns add "$NETNS_NAME"