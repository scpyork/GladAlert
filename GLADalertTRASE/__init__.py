__name__ = 'GladAlert'
__author__='Dan Ellis'


def view(h5file):
    import os
    print (os.popen('h5dump --contents=1 %s'%h5file).read())
