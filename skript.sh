#!/bin/bash

TILESIZE=224
bigrasterfilename=$1

SIZE=$(gdalinfo $bigrasterfilename | grep "Size is")

X="$(cut -d' ' -f3 <<<$SIZE)"
X=${X::-1}

Y="$(cut -d' ' -f4 <<<$SIZE)"

for (( x=0; x<$X; x+=$TILESIZE )); do
	for (( y=0; y<$Y; y+=$TILESIZE )); do
		smallrasterfilename=$x"_"$y".tif"

		gdal_translate -of GTiff -srcwin $x $y $TILESIZE $TILESIZE -co COMPRESS=NONE $bigrasterfilename $smallrasterfilename


		# now we need corresponding land cover information
		# therefore, derive outer extent of tif file with gdalinfo


		hm=$(gdalinfo $smallrasterfilename | grep "Upper Left")
		step1=$(echo "${hm#*  (  }")
		xmin=$(echo "${step1%%,*}")

		step1=$(echo "${hm#*[0-9], }")
		ymax=$(echo "${step1%%)*}")

		hm=$(gdalinfo $smallrasterfilename | grep "Lower Right")
		step1=$(echo "${hm#* ( }")
		xmax=$(echo "${step1%%,*}")

		step1=$(echo "${hm#*[0-9], }")
		ymin=$(echo "${step1%%)*}")

		coords=$(python conv.py $xmin $ymin $xmax $ymax)

		osmname=$x"_"$y.osm
		wget -O $osmname http://www.overpass-api.de/api/xapi_meta?*[bbox=$coords]

		sqlname=$x"_"$y.sqlite
		ogr2ogr -f SQLite -dsco SPATIALITE=YES $sqlname $osmname

		python rasterize.py $smallrasterfilename $sqlname

		rm $sqlname $osmname
	done
done
