# source me, don't execute me

virtualenv --version >/dev/null 2>&1 || ( echo "You need virtualenv!" && return 1 )
virtualenv --distribute venv
. venv/bin/activate
pip install -r requirements.txt
