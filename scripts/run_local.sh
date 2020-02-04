#!/usr/bin/env bash

set -Eeuo pipefail

# ----------------------------------------
# install requirements in virtual env
# ----------------------------------------
pip3 install -q --upgrade virtualenv --user
rm -rf ./venv
virtualenv -p python3 ./venv

source ./venv/bin/activate

pip3 install -q --upgrade pip
pip3 install -q --upgrade -r converter/conf/pip/requirements.txt

chmod +x ./converter/trivago_converter.py