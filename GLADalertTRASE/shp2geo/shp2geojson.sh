## A script to convert shape files to geojson files for plotting

## Author: daniel.ellis

#sudo apt-get install gdal-bin

#run ./shp2geojson */*.shp

#You need .shp,.shx,.prj, and .dbf files with the same name. If the shape files are a zip these need to be extracted.


#for all args
for var in "$@"
do
    file=$(basename ${var} .shp);
    echo "$file";
    ogr2ogr -f GeoJSON "${file}.geojson" "${file}.shp"
done


cp ./*/*.geojson ./
