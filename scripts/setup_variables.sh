#!/usr/bin/env bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" > /dev/null && pwd )" # Gets the script directory
ROOT_DIR="$(dirname "$SCRIPT_DIR")" # Gets the parent of script directory

# Setup dependency variables
source "$ROOT_DIR/venv/bin/activate"
export PYTHONPATH=$ROOT_DIR

# Setup project specific variables
