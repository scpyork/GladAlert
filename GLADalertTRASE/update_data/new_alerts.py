'''
Check for any new alerts in the google cloud storage repo

Must have gsutil installed (pip install gsutil)
'''
import os


def gettif(year):

    __bucket__ = 'earthenginepartners-hansen'
    __location__ = 'gs://%s/GLADalert/%d'%(__bucket__,year)

    return os.popen('gsutil ls -d %s/*/alertDate%s_*'%(__location__,str(year)[-2:])).read().split()




def getdates(year,par=False):
    ''' Use gsutil to read files for a specific year'''

    __bucket__ = 'earthenginepartners-hansen'
    __location__ = 'gs://%s/GLADalert/%d'%(__bucket__,year)

    dates = os.popen('gsutil ls %s'%__location__).read().split()

    print('number of dates: ',len(dates))

    ret = []

    if par:
        from pathos.multiprocessing import ProcessPool
        pool = ProcessPool(nodes=25)
        def pl (i):
            return os.popen('gsutil ls %s'%i).read().split()

        dates = pool.imap(pl,dates)

    else:
        (os.popen('gsutil ls %s'%i).read().split() for i in dates)


    for i in dates:
        ret.extend(i)

    return ret


def direction(d):
    '''Determine the grid cells numerical latlon'''
    if d[-1] in ['W','S']:return -int(d[:-1])
    else: return int(d[:-1])
