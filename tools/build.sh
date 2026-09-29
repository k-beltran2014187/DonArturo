#!/usr/bin/env bash
# Builds the installable child-theme zip (dist/donarturo.zip) and regenerates
# the Elementor template JSON files from tools/build_elementor.py.
set -euo pipefail
cd "$(dirname "$0")/.."

python3 tools/build_elementor.py

mkdir -p dist
rm -f dist/donarturo.zip
cd theme
zip -rq ../dist/donarturo.zip . -x '.*'
cd ..
echo "Built dist/donarturo.zip"
