#!/usr/bin/env bash
# render-build.sh: Build script for Render deployment
set -e

# Install Python dependencies
pip install --upgrade pip
pip install -r bus_tracking/requirements.txt

# Collect static files
python bus_tracking/manage.py collectstatic --noinput

# Apply migrations
python bus_tracking/manage.py migrate --noinput

# (Optional) Seed initial data
# python bus_tracking/manage.py loaddata initial_data.json

# Print success message
echo "Build completed successfully."
