#!/bin/bash

set -e

rm -rf dist && mkdir dist

echo "Installing dependencies"
pdm install --prod
cp -r .venv/lib/python3.*/site-packages/* dist/

echo "Copying source code"
cp -r src/* dist/

echo "Zipping the Lambda code"
cd dist
zip -rq lambda.zip ./*

function get_folder_size() {
    du -sh "$1" | awk '{print $1}'
}

echo
echo "Build complete: lambda.zip ($(get_folder_size lambda.zip))"
