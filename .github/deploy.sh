#!/bin/bash

Instances=("34.165.37.58" "34.165.102.32")


for ip in ${Instances[@]}; do
  ssh ubuntu@$ip uptime
done


# pushd personegenerator

# git pull origin main

# docker compose up -d --build

