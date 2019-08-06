#! /usr/bin/python
# coding=utf-8

import json,glob,re,os,h5py,itertools
#import pandas as pd
import numpy as np
from numba import jit

#import matplotlib.pyplot as plt

### Input variables

#print __file__
year = 2019

__location__ = './shapefiles'
__files__ = filter(lambda x: 'Global' not in x, glob.glob(__location__+'/processed/*.geojson'))
__alertFile__ = h5py.File('data/glad_data_%s.h5'%year,'r')

# use false otherwise state matches
__testRegion__ = u'Formosa do Rio Preto,Nova Ubiratã'.split(',')#False
__testCountries__ = ['brazil']

# Names used to identify regions in various geojson files
__geoNameKeys__ = ['dept','NAME']

@jit(nopython=True)
def ray_tracing(x,y,poly):
    '''
    Check if points are within polygon - compiled
    '''
    n = len(poly)
    inside = False
    p2x = 0.0
    p2y = 0.0
    xints = 0.0
    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside

print ('Available dates: ',__alertFile__.keys() )
if __testRegion__: print('Only running on : ',__testRegion__)
if __testCountries__: print('For : ',__testCountries__)

### merge subboundaries
import geopandas

world = geopandas.read_file('data/naturalearth.geojson')
world = world[['ADMIN', 'geometry']]
world['geometry'] = world.buffer(0.01)
world = world.dissolve(by='ADMIN',aggfunc='sum')
world.index = [i.lower() for i in world.index]
world = world.bounds
#world.to_file("data/merged_countries.geojson", driver='GeoJSON')
#world.plot()

'''
items like fronts from https://www.globalforestwatch.org/embed/dashboards/country/BRA/5/136?gladAlerts=eyJsYXRlc3REYXRlIjoiMjAxOS0wNy0yOSJ9&trase=true&widget=gladAlerts


https://production-api.globalforestwatch.org/query/efaf9e27-a9bd-4b94-b489-c562b4b4d085?sql=SELECT%20iso,%20adm1,%20adm2,%20week,%20year,%20alerts%20as%20count,%20area_ha,%20polyname%20FROM%20data%20WHERE%20iso%20=%20%27BRA%27%20AND%20adm1%20=%205%20AND%20adm2%20=%20136%20AND%20polyname%20=%20%27admin%27


'''


#############
## Main code
#############

for this in __files__: # __files__ are all procecpoussed geojson __files__ from inputs.

    ## get current country name
    country = re.findall(r'/([^/_]+)_[^/]+\.geojson',this)[0]
    print('reading',this, country)
    if __testCountries__:
        if country not in __testCountries__:
            continue

    bounds = world.loc[country] #bounding box for country




    store = {} # information we wish to save
    with open(this,'r') as f:

        jsn = json.loads(f.read())#['features']
        properties = {}

        # iterate through every date.
        for date in __alertFile__.keys():

            data = __alertFile__[date]['data']
            print (date)


            ### Only selelect data which falls within the bounding box area

            cslice = data[:,np.searchsorted(data[0],bounds.minx,side='left') :
                           np.searchsorted(data[0],bounds.maxx,side='right')+1]
            #cslice = cslice[:,np.searchsorted(cslice[1],bounds.miny,side='left') :
                          # np.searchsorted(cslice[1],bounds.maxy,side='right')+1]

            ### Select regions within the chosen country


            for region in jsn['features']:


                #  [i['properties']['NAME'] for i in jsn['features']]



                ### Get area name
                area = False
                while not area:
                    for a in __geoNameKeys__:
                        try:area = region['properties'][a]
                        except:None
                    if not area:
                        print ('skipping', region['properties'] )
                        continue

                if __testRegion__:
                    if area not in __testRegion__:
                        continue

                print area

                properties[area] = region['properties']


                ## get region polygon, and then coordinates.
                poly = np.array(region['geometry']['coordinates'][0]).astype(float)

                if len(poly.shape) == 3: poly = poly[0]# bug fix - not sure why this happens

                x = poly[:,0] #lat
                y = poly[:,1] #lon





                xm = x.min()
                xx = x.max()
                ym = y.min()
                yx = y.max()

                print area, xm,xx, ym,yx


                try: store[region] # if it exists
                except: store[area] = {'name':region['properties']['NAME'],'properties':properties[area],'alerts':{},'potential':{},'polygon':poly.tolist()}



                slice = cslice[:,np.searchsorted(cslice[0],xm,side='left') :
                               np.searchsorted(cslice[0],xx,side='right')+1]

                sliced = slice[:,np.where(slice[1]>=ym)][:,0,:]

                #sliced = slice[:,np.searchsorted(slice[1],ym,side='left') :
                    #           np.searchsorted(slice[1],yx,side='right')+1]



                sliced = sliced[:,np.where(sliced[1]<=yx)][:,0,:].astype(float)

                print 'shp', cslice.shape, slice.shape,sliced.shape

                if sliced.shape[1]>0:

                    res = np.array([z for z in sliced.T if ray_tracing(z[0],z[1],poly)])

                    if len(res) > 0 :
                            print 'match', ym, yx , data[1].min(),data[1].max(),area
                            print slice.shape,sliced.shape,res.shape,area,res[:,2].sum(),sum(res[:,2]==2),sum(res[:,2]==3),'\n', properties[area]

                            store[area]['potential'][date] = res[res[:,2]==2].tolist()
                            store[area]['alerts'][date] = res[res[:,2]==3].tolist()



        # ### write the results of store to json file.
        ### Filter out muncipalities with no alerts (ever) - these contain no new information.
        vals = filter(lambda x: store[x]['alerts']!={},store)

        print(len(vals),'values')
        with open('data/%s_results.json'%country, 'w') as file:
            file.write(json.dumps(dict(zip(vals,[store[i] for i in vals]))))


__alertFile__.close()






#d = np.array(j['features'][1]['geometry']['coordinates']
