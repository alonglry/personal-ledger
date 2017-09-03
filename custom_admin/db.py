#!/home/alonglry/.virtualenvs/django18/bin/python

##########################################################
#                                                        #
# file name: /custome_admin/db.py                        #
# description:                                           #
#                                                        #
##########################################################
#                                                        #
# version date       by              change              #
# 1.0     19/04/2016 Awai            initial release     #
#                                                        #
##########################################################


import MySQLdb
import sys

sys.path.append('/home/alonglry/personal_finance/personal_finance')

from settings import DATABASES

def sqlexecute(sql):
	try:
		db = MySQLdb.connect(host = DATABASES['default']['HOST'],
							 user = DATABASES['default']['USER'],
						   passwd = DATABASES['default']['PASSWORD'],
							   db = DATABASES['default']['NAME'])
		cur = db.cursor()
		cur.execute(sql)
		db.commit()
		db.close()
		return cur.fetchall()
		
	except MySQLdb.ProgrammingError, e:
		raise ValueError(e,sql)
	except MySQLdb.OperationalError, e:
		raise ValueError(e,sql)
	except MySQLdb.IntegrityError, e:
		raise ValueError(e,sql)