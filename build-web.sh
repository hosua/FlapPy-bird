#!/bin/bash

set -e

# Build script for creating web-embeddable version of FlapPy Bird
# Usage: ./build-web.sh [port]
# If port is not specified, defaults to 8000

PORT=${1:-8000}

echo "Building web version..."
python -m pygbag --build main.py

echo "Build complete! The game files are in the 'build/web' directory."
echo ""
echo "To serve the game locally, run:"
echo "  cd build/web && python -m http.server $PORT"
echo ""
echo "Or use pygbag's built-in server:"
echo "  python -m pygbag --port $PORT main.py"
echo ""
echo "The game will be available at http://localhost:$PORT"
