#!/usr/bin/env bash

echo "Running pre-push commands..."
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" > /dev/null && pwd )"
ROOT_DIR="$SCRIPT_DIR/../.."
source "$ROOT_DIR/scripts/setup_variables.sh"
$ROOT_DIR/scripts/run-unittests.sh
if [ $? -ne 0 ]; then
  exit 1
fi
