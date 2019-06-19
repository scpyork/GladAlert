'''
Check for any new alerts in the google cloud storage repo

Must have gsutil installed (pip install gsutil)
'''
import os,datetime


location = 'gs://earthenginepartners-hansen/GLADalert/%d'%datetime.datetime.now().year

days = os.popen('gsutil ls %s'%location).read().split()


files =  os.popen('gsutil ls %s'%days[-1]).read().split()


print files
