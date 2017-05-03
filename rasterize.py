from osgeo import gdal, ogr
import sys

referencerasterloc = sys.argv[1]
shapeloc = sys.argv[2]

# a very simple key just addressing land use-field.
# needs to be extended to homogeneize building, leisure, natural

key = {'allotments': 1, 'basin': 2, 'brownfield': 3, 'cemetery': 4, 'commercial': 5, 'conservation': 6, 'construction': 7, 'depot': 8, 'farmland': 9, 'farmyard': 10, 'forest': 11, 'garages': 12, 'greenfield': 13, 'greenhouse_horticulture': 14, 'industrial': 15, 'landfill': 16, 'meadow': 17, 'military': 18, 'orchard': 19, 'pasture': 20, 'plant_nursery': 21, 'port': 22, 'quarry': 23, 'railway': 24, 'recreation_ground': 25, 'reservoir': 26, 'residential': 27, 'retail': 28, 'salt_pond': 29, 'village_green': 30, 'vineyard': 31}

fieldname = 'cid'
outputname = referencerasterloc[:-4] + '_c.tif'

Src = ogr.Open(shapeloc, 1)
layer = Src.GetLayer('multipolygons')

idField = ogr.FieldDefn(fieldname, ogr.OFTInteger)
layer.CreateField(idField)

for i in range(1, layer.GetFeatureCount() + 1):
    feat = layer.GetFeature(i)
    try:
        class_to_set = key[feat.GetField('landuse')]
#        class_to_set_2 = key2[feat.GetField('building')] #extend on that
#        class_to_set_3 = key3[feat.GetField('leisure')]
#        class_to_set_4 = key4[feat.GetField('natural')]
    except:
        class_to_set = 99
    feat.SetField('cid', class_to_set)
    layer.SetFeature(feat)

Ras_src = gdal.Open(referencerasterloc)
rasterdriver = gdal.GetDriverByName('GTiff')
new_raster = rasterdriver.Create(outputname, Ras_src.GetRasterBand(1).XSize, Ras_src.GetRasterBand(1).YSize, 1, gdal.GDT_Byte)
new_raster.SetProjection(Ras_src.GetProjection())
new_raster.SetGeoTransform(Ras_src.GetGeoTransform())
gdal.RasterizeLayer(new_raster, [1], layer , None, None, [1], ['ATTRIBUTE='+fieldname])
