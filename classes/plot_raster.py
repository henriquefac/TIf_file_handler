import matplotlib.pyplot as plt
import numpy as np

# Classe com métodos para plotar mapa de alturas dos objetos raster
class PlotRaster:
    def __init__(self) -> None:
        pass

    # Recebe a banda para plotagem
    @staticmethod
    def plot_raster_band(banda: np.ndarray, title: str = "Mapa de Alturas", cmap: str = "viridis"):
        """
        Plota a matriz de uma banda de um arquivo TIFF.

        :param banda: Matriz da banda a ser plotada (2D).
        :param title: Título do gráfico.
        :param cmap: Colormap a ser utilizado para o plot.
        """
        plt.figure(figsize=(10, 8))
        plt.imshow(banda, cmap=cmap, aspect='auto')
        plt.colorbar(label='Altura')
        plt.title(title)
        plt.xlabel('Coluna')
        plt.ylabel('Linha')
        plt.grid(False)
        plt.show()

# Exemplo de uso:
# plot = PlotRaster()
# plot.plot_raster_band(matriz_alturas)
