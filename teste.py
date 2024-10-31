import geopandas as gpd
import rasterio
from rasterio.mask import mask
from shapely.geometry import box
import os
import matplotlib.pyplot as plt
from classes.tiffile import TifHandler as th

# Caminho para o shapefile dos municípios do Ceará
spath = r"C:\Users\henri\Documents\pythonProjcs\titf_tutorial_proj\shape_file\CE_Municipios_2022.shp"

# Caminho para o arquivo raster (.tif)
raster_path = r'C:\Users\henri\Documents\pythonProjcs\titf_tutorial_proj\tif_file'
ceara = 'recorte_ceara.tif'
raster_file = "gebco_2024_n0.0_s-90.0_w-90.0_e0.0.tif"
raster = os.path.join(raster_path, ceara)


tif = th(raster)
# Carregar o shapefile
gdf = gpd.read_file(spath)

# Unir todas as geometrias para criar uma única geometria do estado
state_geometry = gdf.unary_union

# Obter a bounding box do estado (xmin, ymin, xmax, ymax)
bounds = state_geometry.bounds

# Criar um polígono da bounding box usando shapely
bbox_polygon = [box(*bounds)]  # Cria um polígono a partir dos limites da bounding box

# Abrir o arquivo raster
with rasterio.open(raster) as src:
    # Recortar o raster usando a geometria da bounding box
    out_image, out_transform = mask(src, bbox_polygon, crop=True)
    print(out_image[0].shape)
    print(tif.get_matrix().shape)
    # Plotar o raster recortado
    plt.figure(figsize=(10, 10))
    
    # O raster pode ter várias bandas, então vamos plotar apenas a primeira banda (banda 1)
    plt.imshow(out_image[0], cmap='viridis')  # Use o cmap que preferir, como 'gray', 'viridis', etc.
    
    plt.title("Recorte do Ceará usando Bounding Box")
    plt.colorbar(label="Elevação (m)")  # Supondo que seja um raster de elevação
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.show()

    plt.imshow(tif.get_matrix(), cmap='viridis')  # Use o cmap que preferir, como 'gray', 'viridis', etc.
    
    plt.title("Recorte do Ceará usando Bounding Box")
    plt.colorbar(label="Elevação (m)")  # Supondo que seja um raster de elevação
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.show()
