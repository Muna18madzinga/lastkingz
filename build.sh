#!/usr/bin/env bash
# Build script for Render

set -o errexit

pip install -r requirements.txt

# Initialize database if it doesn't exist
python -c "from database import Database; db = Database(); print('Database initialized')"
