#!/home/alonglry/.virtualenvs/django18/bin/python

##########################################################
#                                                        #
# file name: /custome_admin/manage.py                    #
# description:                                           #
#                                                        #
##########################################################
#                                                        #
# version date       by              change              #
# 1.0     19/04/2016 Awai            initial release     #
#                                                        #
##########################################################


import sys
import os

sys.path.append('/home/alonglry/personal_finance')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "personal_finance.settings")

import django

django.setup()

from django.core.management import call_command

def manage(*args):
	call_command(*args)
