'''
Check for any new alerts in the google cloud storage repo

Must have gsutil installed (pip install gsutil)
'''
import os,datetime


location = 'gs://earthenginepartners-hansen/GLADalert/%d'%datetime.datetime.now().year

files = os.popen('gsutil ls %s'%location).read()

print files
