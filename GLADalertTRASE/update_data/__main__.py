import numpy as np
import os,datetime,sys,h5py
from new_alerts import gettif

args = sys.argv
print(args ,__file__)

ncores = 80
year = None

now = datetime.datetime.now()
if not year: year = str(now.year)
if not os.path.isdir('./data/'):os.mkdir('./data/')
try:
    with h5py.File('data/glad_data_%s.h5'%year,'r') as hf:
        names = hf.keys()
except:
    names = []
try: hf.close()
except: None
print names

print ('Getting available datasets for the year')
files = gettif(int(year))
daymonths = list(set([i.split('/')[-2] for i in files]))

diff = set(daymonths)-set(names)


print ('Running for %s days - 115 tiles each'%len(diff))

for select in diff:
    print select
    filtered_urls = filter(lambda x: select in x, files)

    if len(filtered_urls)<ncores:
        runcores = len(filtered_urls)
    else:
        runcores = ncores

    links = ','.join(filtered_urls)
    os.system('mpirun -np %d python %s %s %s'%(runcores,__file__.replace('__main__','mpi_init'),select,links
))
