'''
Check for any new alerts in the google cloud storage repo

Must have gsutil installed (pip install gsutil)
'''
import os,datetime

bucket = 'earthenginepartners-hansen'
location = 'gs://%s/GLADalert/%d'%(bucket,datetime.datetime.now().year)

days = os.popen('gsutil ls %s'%location).read().split()


files =  os.popen('gsutil ls %s'%days[-1]).read().split()


print files
