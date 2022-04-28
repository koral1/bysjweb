#!/bin/bash

BRIDGE_NAME=$1

sudo brctl addbr "$BRIDGE_NAME"