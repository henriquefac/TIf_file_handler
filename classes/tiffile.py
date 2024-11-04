from osgeo import gdal, ogr

# Classe responsável por lidar com arquivos do tipo TIFF
class TifHandler:
    def __init__(self, path):
        # Caminho do arquivo TIFF
        self.path = path
        # Objeto raster do arquivo TIFF
        self.raster_obj = self._load_tif_file()
        # Recorte da banda (armazenado após o recorte)
        self.banda_recorte = None

    # Carrega o arquivo TIFF como um objeto raster
    def _load_tif_file(self):
        return gdal.Open(self.path)

    # Retorna informações principais do arquivo TIFF
    def get_info(self):
        geo_transform = self.raster_obj.GetGeoTransform()
        return {
            'Largura': self.raster_obj.RasterXSize,
            'Altura': self.raster_obj.RasterYSize,
            'Número de Bandas': self.raster_obj.RasterCount,
            "Coordenadas Reais": {
                "Origem X": geo_transform[0],
                "Largura do Pixel": geo_transform[1],
                "Origem Y": geo_transform[3],
                "Altura do Pixel": geo_transform[5],
            },
            "Projeção": self.raster_obj.GetProjection(),
            "Metadados": self.raster_obj.GetMetadata()
        }

    # Realiza o recorte do arquivo TIFF a partir de coordenadas geográficas
    def recortar_por_limites(self, norte, sul, oeste, leste):
        geo_transform = self.raster_obj.GetGeoTransform()
        inv_geo_transform = gdal.InvGeoTransform(geo_transform)

        # Converte as coordenadas geográficas para coordenadas de pixel
        x_min, y_max = gdal.ApplyGeoTransform(inv_geo_transform, oeste, norte)
        x_max, y_min = gdal.ApplyGeoTransform(inv_geo_transform, leste, sul)

        # Garante que os índices são inteiros
        x_min, x_max = int(x_min), int(x_max)
        y_min, y_max = int(y_min), int(y_max)

        # Recorta a primeira banda do TIFF com base nos limites
        banda = self.raster_obj.GetRasterBand(1)
        self.banda_recorte = banda.ReadAsArray(x_min, y_min, x_max - x_min, y_max - y_min)
        return self.banda_recorte

    # Salva o recorte em um novo arquivo TIFF
    def salvar_novo_tif(self, caminho_saida):
        if self.banda_recorte is None:
            raise ValueError("Não há recorte para salvar. Execute o método de recorte primeiro.")

        # Cria um novo dataset TIFF com as dimensões do recorte
        driver = gdal.GetDriverByName("GTiff")
        out_raster = driver.Create(
            caminho_saida,
            self.banda_recorte.shape[1],  # largura
            self.banda_recorte.shape[0],  # altura
            1,                            # número de bandas
            gdal.GDT_Float32              # tipo de dados (ajuste conforme necessário)
        )

        # Define a transformação geoespacial para o novo arquivo
        geo_transform = self.raster_obj.GetGeoTransform()
        out_raster.SetGeoTransform(geo_transform)
        out_raster.SetProjection(self.raster_obj.GetProjection())

        # Grava o recorte na nova banda
        out_band = out_raster.GetRasterBand(1)
        out_band.WriteArray(self.banda_recorte)

        # Salva e fecha o novo arquivo
        out_band.FlushCache()
        out_raster = None

    # Recorta o arquivo TIFF com base em um shapefile (limite do Ceará)
    def recortar_por_shapefile(self, path_shapefile):
        # Abre o shapefile usando OGR
        shapefile = ogr.Open(path_shapefile)
        layer = shapefile.GetLayer()

        # Cria uma máscara a partir das geometrias do shapefile
        mask_ds = gdal.Warp(
            '', self.raster_obj, format='MEM', cutlineDSName=path_shapefile,
            cropToCutline=True
        )

        # Extrai a primeira banda da máscara
        self.banda_recorte = mask_ds.GetRasterBand(1).ReadAsArray()
        mask_ds = None
        return self.banda_recorte

    # Imprime informações do arquivo TIFF formatadas
    def __str__(self):
        info = self.get_info()
        return "\n".join(f"{k}: {v}" if not isinstance(v, dict) else f"{k}:\n" + 
                         "\n".join(f"  {sub_k}: {sub_v}" for sub_k, sub_v in v.items()) 
                         for k, v in info.items())
