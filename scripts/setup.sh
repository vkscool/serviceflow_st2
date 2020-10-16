#!/usr/bin/env bash

GIT_DIR=$(git rev-parse --git-dir)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" > /dev/null && pwd )"

echo "Setting up virtual environment.."
python3 -m venv venv

if [ $? -ne 0 ]; then
  echo "Error creating virtual environment. Please make sure you have python3-vent package installed"
  echo "Refer this doc https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/"
  echo "Run this script again after the package is installed"
  exit 1
fi

echo "Activating virtual environment.."
source venv/bin/activate

echo "Installing all the requirements.."
pip install -r dev-requirements.txt
if [ $? -ne 0 ]; then
  echo "Error installing all requirements, Please check the errors."
  exit 1
fi

echo "Installing hooks..."
ln -sf "$SCRIPT_DIR/pre-push.sh" "$GIT_DIR/hooks/pre-push"
chmod +x "$GIT_DIR/hooks/pre-push"
echo "Done initializing hooks!"
source "$ROOT_DIR/scripts/setup_variables.sh"
echo "===================================================================================="
echo "|| Setup is complete if there were no errors in the above script.                 ||"
echo "===================================================================================="
