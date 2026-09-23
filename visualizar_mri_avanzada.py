import sys
from pathlib import Path

import matplotlib
import numpy as np
import SimpleITK as sitk
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QMainWindow, QSlider, QVBoxLayout, QWidget

matplotlib.use("Qt5Agg")


class VentanaMRI(QMainWindow):
    def __init__(self, ruta_archivo: str):
        super().__init__()
        self.setWindowTitle("Visualizador 3D de MRI con sliders")
        self.resize(1200, 800)

        self.archivo = Path(ruta_archivo)
        self.img = sitk.ReadImage(str(self.archivo))
        self.data = sitk.GetArrayFromImage(self.img)

        self.data = self.data.astype(np.float32)
        self.data_norm = self.normalizar(self.data)

        self.slices = self.data_norm.shape
        self.slice_x = self.slices[0] // 2
        self.slice_y = self.slices[1] // 2
        self.slice_z = self.slices[2] // 2

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QHBoxLayout(self.central_widget)

        self.left_panel = QWidget()
        self.left_layout = QVBoxLayout(self.left_panel)

        self.label_info = QLabel(
            f"Archivo: {self.archivo.name}\n"
            f"Forma: {self.data.shape}\n"
            f"Rango: {self.data.min():.2f} - {self.data.max():.2f}"
        )
        self.left_layout.addWidget(self.label_info)

        self.slider_x = self.crear_slider(0, self.slices[0] - 1, self.slice_x, "Corte X")
        self.slider_y = self.crear_slider(0, self.slices[1] - 1, self.slice_y, "Corte Y")
        self.slider_z = self.crear_slider(0, self.slices[2] - 1, self.slice_z, "Corte Z")

        self.left_layout.addWidget(self.slider_x)
        self.left_layout.addWidget(self.slider_y)
        self.left_layout.addWidget(self.slider_z)

        self.left_layout.addStretch()
        self.layout.addWidget(self.left_panel, 1)

        self.figure = Figure(figsize=(8, 8), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas, 4)

        self.actualizar_visualizacion()

    def normalizar(self, arr: np.ndarray) -> np.ndarray:
        arr_min = np.min(arr)
        arr_max = np.max(arr)
        if arr_max - arr_min == 0:
            return np.zeros_like(arr, dtype=np.float32)
        return ((arr - arr_min) / (arr_max - arr_min)).astype(np.float32)

    def crear_slider(self, min_value: int, max_value: int, valor_inicial: int, texto: str):
        container = QWidget()
        layout = QVBoxLayout(container)

        label = QLabel(texto)
        slider = QSlider()
        slider.setOrientation(1)
        slider.setMinimum(min_value)
        slider.setMaximum(max_value)
        slider.setValue(valor_inicial)
        slider.valueChanged.connect(self.actualizar_visualizacion)

        layout.addWidget(label)
        layout.addWidget(slider)

        if texto == "Corte X":
            slider.setObjectName("slider_x")
            self.slider_x_widget = slider
        elif texto == "Corte Y":
            slider.setObjectName("slider_y")
            self.slider_y_widget = slider
        elif texto == "Corte Z":
            slider.setObjectName("slider_z")
            self.slider_z_widget = slider

        return container

    def actualizar_visualizacion(self):
        self.slice_x = self.slider_x_widget.value() if hasattr(self, "slider_x_widget") else self.slice_x
        self.slice_y = self.slider_y_widget.value() if hasattr(self, "slider_y_widget") else self.slice_y
        self.slice_z = self.slider_z_widget.value() if hasattr(self, "slider_z_widget") else self.slice_z

        corte_x = self.data_norm[self.slice_x, :, :]
        corte_y = self.data_norm[:, self.slice_y, :]
        corte_z = self.data_norm[:, :, self.slice_z]

        self.ax.clear()
        self.ax.imshow(corte_x, cmap="gray", aspect="auto")
        self.ax.set_title(f"Corte X = {self.slice_x}")
        self.ax.axis("off")

        self.canvas.draw()


def main():
    if len(sys.argv) != 2:
        print("Uso: python visualizar_mri_avanzada.py <archivo.nii>")
        sys.exit(1)

    app = QApplication(sys.argv)
    ventana = VentanaMRI(sys.argv[1])
    ventana.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
