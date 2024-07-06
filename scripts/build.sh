#!/bin/bash

set -e

rm -rf dist && mkdir dist

echo "::group::Build dependencies"
pdm install --prod
mv .venv/lib/python3.*/site-packages/* dist/
echo "::endgroup::"

echo "::group::Zipping the Lambda code"
cp -r src/* dist/
cd dist
zip -r lambda.zip ./*
echo "::endgroup::"

function get_directory_size() {
    du -sh "$1" | awk '{print $1}'
}

echo
echo "Build complete:"
echo "- lambda.zip size: $(get_directory_size lambda.zip)"
