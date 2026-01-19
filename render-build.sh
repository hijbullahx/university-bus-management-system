#!/usr/bin/env bash
# render-build.sh: Build script for Render deployment
set -e


# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt



# Collect static files
if [ -f bus_tracking/manage.py ]; then
	python bus_tracking/manage.py collectstatic --noinput
	python bus_tracking/manage.py migrate --noinput
	# (Optional) Seed initial data
	# python bus_tracking/manage.py loaddata initial_data.json
else
	python manage.py collectstatic --noinput
	python manage.py migrate --noinput
	# (Optional) Seed initial data
	# python manage.py loaddata initial_data.json
fi

# Print success message
echo "Build completed successfully."
