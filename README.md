# osmref

Simple script to download and rasterize OSM data at the location of any
remote sensing image. In addition, the output is split into subsets of size
$TILESIZE to allow for better handling.

Requires work with the homogeneization of OSM classes, which are right now
taken arbitrarily from the *landuse* field. Data from other fields should
also be integrated.
