# imports
from osgeo import gdal
import matplotlib.pyplot as plt
import numpy as np
from classes.tiffile import TifHandler
from classes.plot_raster import PlotRaster as pr
# path
path = r"tif_file\recorte_ceara.tif"

tif = TifHandler(path)
pr.plot_raster_band(tif.recorte(-5, -40, -58, -30)[0])


# fazer recorte a partir deshape file: FEITO

# fazer recorte nos dados das bacias: PRÓXIMO   

# achar pontos de máximo e mínimo

# pegar outliers 

# realizar algoritmos de achatamento

# ver no que dá 