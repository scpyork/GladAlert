# GladAlert
Reporcess the glad alert data to match the TRASE shapefiles.







### Install
`pip install gsutil`
`pip install pillow`
`pip install geopandas`


### Order of running
1. Download shapefiles and convert into geojson (stored under a `shapefiles` directory)
2. Save region polynomials into `glad_shapes.h5`
3. Download the latest data into `glad_data_<year>.h5`


### example code for accomplishing above.
```


```



### Setting up the shapefiles
These can be at any location, although the processed files remain within that directory.

It is easiest to create a shapefiles folder in the main repository, and add all your relevant `*.shp *.dbf *.prj *.shx` files in a new folder containing the country's name. This will later be used to identify to where each file corresponds.

These files are converted into geojson files -it does not matter if these are available since the preformatted Trase ones cause issues, and placed in the `processed` folder of your shapefile directory.

Processed files are then read, and turned into masks fitting the GLAD alert tiles.


## Todo
write properties files
