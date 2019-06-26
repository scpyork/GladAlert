# GladAlert
Reporcess the glad alert data to match the TRASE shapefiles.

### Insatll
`pip install gsutil`
`pip install pillow`
`pip install geopandas`

### Setting up the shapefiles
These can be at any location, although the processed files remain within that directory.

It is easiest to create a shapefiles folder in the main repository, and add all your relevant `*.shp *.dbf *.prj *.shx` files in a new folder containing the country's name. This will later be used to identify to where each file corresponds.

These files are converted into geojson files -it does not matter if these are available since the preformatted Trase ones cause issues, and placed in the `processed` folder of your shapefile directory.

Processed files are then read, and turned into masks fitting the GLAD alert tiles. 


## Todo
