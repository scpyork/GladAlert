'''
Lets get all the shape files and convert them into accesible geojson files.
The original conversion script does not appear to work well regarding encodings.

Creator: Dan Ellis
'''

import glob,os
import geopandas as gpd



loc = './shapefiles'
files = glob.glob(loc+'/G*/*.shp')
print (files)

#create the processed directory
if not os.path.isdir(loc+'/processed'):os.mkdir(loc+'/processed')



for f in files:
    split = f.split('/')
    shape = gpd.read_file(f)

    to_name = '%s/processed/%s_%s'%('/'.join(split[:-2]),split[-2],split[-1].replace('shp','geojson'))

    shape.to_file(to_name, driver="GeoJSON")

    print( f,'\n -converted-> \n', to_name )
