#!/usr/bin/bash
OUTPUT=$(date +"%s").jpg
echo "${OUTPUT}"
raspistill -o ${OUTPUT} ; scp ${OUTPUT} jp@JP-3.local:~/