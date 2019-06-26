import json,glob,re,os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

loc = './shapefiles'
files = glob.glob(loc+'/processed/*.geojson')
#masks folder
if not os.path.isdir(loc+'/masks'):os.mkdir(loc+'/masks')


for this in files:
    with open(this,'r') as f:
        j = json.loads(f.read())['features']


        country = re.findall(r'/([^/]+)_[^/]+\.geojson',this)[0]
        #output folder create
        if not os.path.isdir(loc+'/masks/'+country):os.mkdir(loc+'/masks/'+country)

        properties = {}

        #for each region
        for region in j:

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

            x = poly[:,0]
            y = poly[:,1]

            '''
            Check overlap with tiles

            and get dpi
            '''


            plt.figure(figsize=(8, 8))
            plt.axis('equal')
            plt.fill(x, y)
            plt.axis('off')
            plt.savefig(loc+'/masks/'+country+'/%s.tiff'%area)
            plt.clf()
            plt.close()

            ##plt.show()











#d = np.array(j['features'][1]['geometry']['coordinates']
