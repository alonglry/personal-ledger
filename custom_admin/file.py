#!/home/alonglry/.virtualenvs/django18/bin/python

##########################################################
#                                                        #
# file name: /custome_admin/file.py                      #
# description:                                           #
#                                                        #
##########################################################
#                                                        #
# version date       by              change              #
# 1.0     19/04/2016 Awai            initial release     #
#                                                        #
##########################################################

import os.path

def getfile(project,file):
	dir = '/home/alonglry/personal_finance/' + project.replace(' ','_') + '/models/'
	file = str(file).replace(' ','_')
	
	if os.path.isfile(dir + file):
		f = open(dir + file, 'r')
		s = f.read()
		return s
		f.close()
	else:
		f = open(dir + file, 'w')
		f.write('#models here')
		return ''
		f.close()
		
def writefile(project,file,content):
	dir = '/home/alonglry/personal_finance/' + project.replace(' ','_') + '/models/'
	file = file.replace(' ','_')
	
	f = open(dir + file, 'w')
	f.write(content)
	f.close()