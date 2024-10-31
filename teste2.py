import geopandas as gpd
import rasterio
from rasterio.mask import mask
import matplotlib.pyplot as plt
import os
from classes.plot_raster import PlotRaster as pr

# Caminho para o shapefile
spath = r"C:\Users\henri\Documents\pythonProjcs\titf_tutorial_proj\shape_file\CE_Municipios_2022.shp"

# Caminho para o arquivo raster (.tif)
path = 'tif_file'
file = 'gebco_2024_n0.0_s-90.0_w-90.0_e0.0.tif'
raster = os.path.join(path, file)

# Diretório de output
output_dir = "/storage/henrique/output"

# Carregar o shapefile
gdf = gpd.read_file(spath)

# Unir todas as geometrias dos municípios para criar uma única geometria
state_geometry = gdf.unary_union

# Abrir o arquivo raster
with rasterio.open(raster) as src:
    # Certifique-se de que o valor nodata está correto
    nodata_value = src.nodata

    # Aplicar a máscara (recorte) usando a geometria do estado
    out_image, out_transform = mask(src, [state_geometry], crop=True, nodata=nodata_value)

    # Verificar o tipo de dado
    print(f"Tipo de dado original: {src.dtypes[0]}")

pr.plot_raster_band(out_image[0])
    
