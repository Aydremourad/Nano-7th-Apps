#!/bin/bash
# No sudo, no firmware flashing, no internet requests.
cd "$(dirname "$0")" || exit 1
printf '\n  iPod nano 7G — Community Mac App Kit\n  -----------------------------------\n'
if ! command -v python3 >/dev/null 2>&1; then
  echo 'Python 3 is missing. Install Python 3 from https://www.python.org/downloads/macos/ and run this again.'
  echo 'No files on your iPod were changed.'
  read -r -p 'Press Return to close...' _
  exit 1
fi
python3 nano7_mac.py
code=$?
if [ "$code" -ne 0 ]; then
  echo "Launcher stopped (exit $code); see message above."
fi
read -r -p 'Press Return to close this window...' _
exit "$code"
