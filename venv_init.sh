# source me, don't execute me

virtualenv --version || { echo "You need virtualenv!"; return 1; }
virtualenv --distribute venv
. venv/bin/activate
pip install -r requirements.txt
