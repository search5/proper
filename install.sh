#!/usr/bin/env bash
python3 -m venv ./venv
source ./venv/bin/activate
pip install -r ./requirements.txt
nodeenv -n 12.13.1 -p
npm install -g typescript @vue/cli @vue/cli-service-global

echo "Successfully Proper"
