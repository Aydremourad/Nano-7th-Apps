#!/bin/bash
cd "$(dirname "$0")" || exit 1
if ! command -v python3 >/dev/null 2>&1; then echo 'Install Python 3 first.'; exit 1; fi
python3 nano7_mac.py --self-test
code=$?
read -r -p 'Press Return to close this window...' _
exit "$code"
