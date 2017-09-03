#!/usr/bin/env python2.7
activate_this = '/home/alonglry/.virtualenvs/django18/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys

# explicitly set package path
path = '/home/alonglry/personal_finance/custom_admin/'
if path not in sys.path:
    sys.path.append(path)

import subprocess

subprocess.Popen(['python', '/home/alonglry/personal_finance/custom_admin/model_online.py'] + sys.argv[1:])