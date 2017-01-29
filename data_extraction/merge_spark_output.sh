#!/bin/bash

if [[ $# -ne 1 ]]; then
  echo "Syntax: $(basename $0) <directory>"
else
  for dir in "$1"/*; do
    if [[ -d "$dir" ]]; then
      out=$(basename "$dir")
      cat "$dir/part"* > "./$out"
    fi
  done
fi