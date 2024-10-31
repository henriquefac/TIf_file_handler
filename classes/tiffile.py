from osgeo import gdal
import rasterio
from rasterio.windows import from_bounds
from rasterio.transform import from_origin

# Classe responsável por lidar com arquivos do tipo tif
class TifHandler:
    def __init__(self, path) -> None:
        # Caminho do arquivo referenciado
        self.path: str = path
        # Objeto raster do arquivo tif
        self.raster_obj: gdal.Dataset = self.getTifFile()
        # Recorte
        self.banda_recorte = None

    # Pegar arquivo como objeto raster
    def getTifFile(self) -> gdal.Dataset:
        return gdal.Open(self.path)

    # Informações principais
    def getInforTif(self) -> dict:
        raster: gdal.Dataset = self.raster_obj
        info = {
            'RasterXSize': raster.RasterXSize,
            'RasterYSize': raster.RasterYSize,
            'BandsCount': raster.RasterCount,
            "coordenadas reais": {
                "OrigemX": raster.GetGeoTransform()[0],
                "PixelWidth": raster.GetGeoTransform()[1],
                "OrigemY": raster.GetGeoTransform()[3],
                "PixelHeight": raster.GetGeoTransform()[5],
            },
            "WKT": raster.GetProjection(),
            "meta": raster.GetMetadata()
        }
        return info

    # Recorte do arquivo tif
    def recorte(self, limite_norte, limite_sul, limite_oeste, limite_leste):
        # Abrir o arquivo TIFF
        with rasterio.open(self.path) as src:
            # Definir a janela de recorte com base nas coordenadas
            janela = from_bounds(limite_oeste, limite_sul, limite_leste, limite_norte, src.transform)

            # Verificar se a janela é válida
            if janela.height <= 0 or janela.width <= 0:
                raise ValueError("Coordenadas de recorte resultam em uma janela inválida.")

            # Fazer a leitura do recorte
            recorte = src.read(window=janela)

            # Printar o shape da matriz recortada (bandas, altura, largura)
            self.banda_recorte = recorte
            return recorte

    # Cria novo arquivo tif se houver recorte
    def getNewTif(self, path):
        if self.banda_recorte is None:
            return
        
        # Obtenha a matriz e suas dimensões
        matrix = self.banda_recorte
        nrows, ncols = matrix.shape[1], matrix.shape[2]  # shape é (bands, height, width)
        
        # Obtém a transformação do arquivo original
        with rasterio.open(self.path) as src:
            transform = src.transform
            # Cria um novo arquivo TIFF com as mesmas configurações
            new_transform = from_origin(transform[0], transform[3], transform[1], transform[5])

            with rasterio.open(
                path,
                'w',
                driver='GTiff',
                height=nrows,
                width=ncols,
                count=1,  # Número de bandas
                dtype=matrix.dtype,
                crs=src.crs,
                transform=new_transform
            ) as dst:
                dst.write(matrix, 1)  # Escreve a matriz na primeira banda

    def get_matrix(self):
        banda = self.raster_obj.GetRasterBand(1)
        matriz_alturas = banda.ReadAsArray()
        return matriz_alturas

    # a partir de um arquivo shapefile, fazer o recorte do tif
    


    # Printar informações do raster do arquivo tif formatado
    def __str__(self) -> str:
        info = self.getInforTif()

        def string_list(list_: list, space_heranca=""):
            if len(list_) == 0:
                return "[]"
            string = "[\n"
            space = "   " + space_heranca
            for elemento in list_:
                if isinstance(elemento, list):
                    string += string_list(elemento, space)
                elif isinstance(elemento, dict):
                    string += string_dict(elemento, space)
                else:
                    string += f"{elemento}"
                string += ",\n"
            string += space_heranca + "]\n"
            return string

        def string_dict(dict_: dict, space_heranca=""):
            if len(list(dict_.keys())) == 0:
                return "{}"
            string = "{\n"
            space = "   " + space_heranca
            for key, value in dict_.items():
                string += space + f"{key} : "
                if isinstance(value, list):
                    string += string_list(value, space)
                elif isinstance(value, dict):
                    string += string_dict(value, space)
                else:
                    string += f"{value}"
                string += ",\n"
            string += space_heranca + "}"
            return string

        return string_dict(info)
