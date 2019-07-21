import json,glob,re,os,h5py,itertools
#import pandas as pd
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt




print __file__
loc = './shapefiles'
files = glob.glob(loc+'/processed/*.geojson')

plot = True
#masks folder
if not os.path.isdir(loc+'/masks'):os.mkdir(loc+'/masks')


hf      = h5py.File('glad_data.h5','r')
box = [np.array(i.split('|')).astype(int) for i in hf.keys()]


# store locations and values
cells = np.zeros((180,360))
for i,c in enumerate(box):#im[(-1*c[3])+90:(-1*c[1])+90 , c[0]+180:c[2]+180] = 200-i
    cells[(c[1])+90:(c[3]-1)+90 , c[0]+180:c[2]-1+180] = 100+i*1# add 100 mainly for diagnostic plot contrast.

if plot:
    im = np.array(Image.open('worldmap.png').resize((360,180)),dtype='i2')[:,:,-1]
    plt.imshow(im+np.roll((cells[::-1,:]),5,axis=0),cmap='viridis')
    plt.tight_layout()
    plt.savefig('cells.png')



for this in files:

    print(this)
    with open(this,'r') as f:
        jsn = json.loads(f.read())['features']

        country = re.findall(r'/([^/]+)_[^/]+\.geojson',this)[0]
        #output folder create
        if not os.path.isdir(loc+'/masks/'+country):os.mkdir(loc+'/masks/'+country)

        properties = {}
        print(this)
        #for each region
        for region in jsn:

            #get area name from many keys
            area = False
            while not area:
                for a in ['dept','NAME']:
                    try:
                        area = region['properties'][a]
                    except:
                        None

                if not area:
                    print ('skipping', region['properties'] )
                    continue

            properties[area] = region['properties']

            ## get polygon
            poly = np.array(region['geometry']['coordinates'][0])

            x = poly[:,0] #lat
            y = poly[:,1] #lon

            min_x = x.min()
            min_y = y.min()
            max_x = x.max()
            max_y = y.max()

            #which cells do we exist within  - int should do a floor division, if python 3 has broken this feature correct.
            matches = set([int(cells[int(pt[1])+90,int(pt[0])+180]-100) for pt in ([x,y] for y in [min_y,max_y] for x in [min_x,max_x]) ])


            '''
            Check overlap with tiles
            '''

            for match in matches:



            fig = plt.figure(frameon=False)
            plt.axis('equal')
            plt.fill(x, y)
            plt.axis('off')
            plt.savefig(loc+'/masks/'+country+'/%s.tiff'%area)
            plt.clf()
            plt.close()
            break
            ##plt.show()




hf.close()






#d = np.array(j['features'][1]['geometry']['coordinates']
