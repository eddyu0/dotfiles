#!/usr/bin/env bash

set -euo pipefail

cat $(dirname $0)/extensions | grep -v '^#' | xargs -L1 code --install-extension