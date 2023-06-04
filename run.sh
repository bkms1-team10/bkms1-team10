#export SETTINGS=$(pwd)/settings.py
#export FLASK_DEBUG=True
#export FLASK_APP=adapi/__init__.py
#export FLASK_ENV=development
#flask run --host=0.0.0.0
# export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
# venv/bin/gunicorn "adapi:app"  -w 3  --preload -b 127.0.0.1:5000 --log-level INFO --access-logfile logs/access.log --error-logfile logs/error.log --reload --limit-request-field_size 8190 --limit-request-line 8192
# venv/bin/gunicorn "adapi:app"  -w 3  -b 127.0.0.1:5000 --log-level DEBUG --access-logfile logs/access.log --error-logfile logs/error.log --reload --limit-request-field_size 8190 --limit-request-line 8192 --timeout=300

venv/bin/gunicorn "server:app"   -b 127.0.0.1:4050 --log-level DEBUG --access-logfile logs/access.log --error-logfile logs/error.log --reload --limit-request-field_size 8190 --limit-request-line 8192 --timeout=300
