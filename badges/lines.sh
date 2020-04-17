#!/bin/bash

if ! hash anybadge &> /dev/null; then
  echo "anybadge not installed! did you forget to source a virtualenv?"
  echo "To install anybadge, run 'pip install anybadge'"
  exit 1
fi

lines=$(find . -type f -name '*.py' -not -path '*venv*' -not -path '*testing*' -not -path '*badges*' -not -path '*blueweather-old*' -print0 | xargs -0 cat | wc -l)

echo Lines: $lines

mkdir -p badges
rm -f badges/lines.svg
anybadge -l 'lines' -v $lines -c lightgrey -f badges/lines.svg
