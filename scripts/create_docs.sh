#!/usr/bin/env bash

# if any command inside script returns error, exit and return that error
set -e

# magic line to ensure that we're always inside the root of our application,
cd "${0%/*}/.."
source scripts/setup_variables.sh
cd docs
make html
if [ $? -ne 0 ]; then
  echo "Failed to build docs, please check the error"
  exit 1
fi
cd _build/html
zip -r -D docs_out.zip .
mv docs_out.zip ../../../
cd ../../..
version="0.1.0"
version=$version-$(git symbolic-ref --short -q HEAD | tr / - )
curl -X POST -F filedata=@docs_out.zip \
  -F name="ServiceFlow StackStorm" \
  -F version="$version" \
  -F description="ServiceFlow StackStorm Modules" \
  -k \
  https://serviceflow-docs.default.abattery.appbattery.nss1.tn.akamai.com/hmfd
  # Need to change this later
exit 0
