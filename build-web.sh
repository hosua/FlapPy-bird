#!/bin/bash

set -e

echo "Building web version..."
python -m pygbag --build .
echo "Build complete! The game files are in the 'build/web' directory."
