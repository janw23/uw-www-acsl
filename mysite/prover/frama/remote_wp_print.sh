#!/bin/bash
# Executes `frama-c -wp -wp-print <filename.c>` on students as it doesn't work locally
fp=$1
base=$(basename "$fp")

scp -q "${fp}" students:~/frama_service/
ssh students "cd ~/frama_service && frama-c -wp -wp-print ${base}"
ssh students "rm ~/frama_service/${base}"

# uncomment this and comment above for local version
# frama-c -wp -wp-print $fp