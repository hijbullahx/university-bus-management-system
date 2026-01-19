pip install -r bus_tracking/backend/requirements.txt
python bus_tracking/backend/manage.py collectstatic --noinput
python bus_tracking/backend/manage.py migrate --noinput