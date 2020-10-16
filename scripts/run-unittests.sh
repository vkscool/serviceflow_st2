#!/usr/bin/env bash

# if any command inside script returns error, exit and return that error
set -e

# magic line to ensure that we're always inside the root of our application,
# `./scripts/run-unittest.bash`
cd "${0%/*}/.."
source scripts/setup_variables.sh
echo "Running unit tests.."
python -m unittest -v
if [ $? -ne 0 ]; then
 echo "Some tests failed, please ensure all tests pass before pushing the code"
 exit 1
fi
exit 0
