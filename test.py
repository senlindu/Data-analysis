import shapefile
import shapely
import geopandas
import fiona
import seaborn as sns
from fiona.crs import from_epsg, from_string
import matplotlib.pyplot as plt
import geopandas

# w = shapefile.Writer('shapefiles/test/polygon')
# w.field('name', 'C')

# w.poly([[[122, 37], [117, 36], [115, 32], [118, 20], [113, 24]],  # poly 1
#         [[15, 2], [17, 6], [22, 7]],  # hole 1
#         [[122, 37], [117, 36], [115, 32]]  # poly 2
#         ])
# w.record('polygon1')

# w.close()
# tpath = 'e:/Data-analysis/shapefiles/test/polygon.shp'
# shp_df = geopandas.GeoDataFrame.from_file(tpath)
# shp_df.head()

# print(shp_df.head())
# shp_df.plot()
# plt.show()


print(geopandas.datasets.available)
