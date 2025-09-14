#!/bin/bash

echo "✨ Cleaning up Python project clutter... ✨"

# Function to remove safely
remove() {
  if [ -e "$1" ]; then
    echo "🧹 Removing $1"
    rm -rf "$1"
  fi
}

# Remove Python cache files and folders
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.py[co]" -delete
find . -type f -name "*.pyd" -delete

# Remove egg-info, build artifacts
remove "./build"
remove "./dist"
find . -type d -name "*.egg-info" -exec rm -rf {} +

# Remove testing and typing caches
remove "./.pytest_cache"
remove "./.mypy_cache"
remove "./.ruff_cache"

# Remove Jupyter notebook checkpoints
find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} +

# Remove Sphinx build artifacts
remove "./docs/_build"
find ./docs -type f -name "*.doctree" -delete
find ./docs -type d -name ".doctrees" -exec rm -rf {} +

# Remove OS cruft
find . -type f -name ".DS_Store" -delete
find . -type f -name "Thumbs.db" -delete
find . -type f -name "._*" -delete

# Removing ".Trashes" that MAC generates
find . -type d -name ".Trashes" -exec rm -rf {} +

# Remove backup/editor swap files
find . -type f -name "*~" -delete
find . -type f -name "*.swp" -delete
find . -type f -name "*.bak" -delete

# Optional: clean up compiled extensions (e.g., Cython)
find . -type f -name "*.so" -delete

echo "Everything is done under the sun."