#!/bin/bash

pip install -r requirements.txt
npm install

ORIGIN="./static/styles/origin"
DIST="./static/styles/dist"

mkdir -p "$DIST"

for file in "$ORIGIN"/*.css; do
  filename=$(basename "$file")
  npx tailwindcss -i "$file" -o "$DIST/$filename" --minify
  echo "Compilado: $filename"
done