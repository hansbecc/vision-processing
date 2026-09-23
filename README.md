# Visualización de imágenes médicas NIfTI

Este proyecto muestra cómo cargar, normalizar, extraer una región de interés (ROI) y visualizar imágenes médicas en formato NIfTI utilizando Python.

Incluye dos versiones:

- `visualizar_mri_basica.py`: versión sencilla para cargar la imagen, normalizar intensidades y mostrar cortes.
- `visualizar_mri_avanzada.py`: versión con interfaz gráfica usando PyQt y sliders para navegar por los cortes X, Y y Z.

## Requisitos

- Python 3.10+
- `nibabel`
- `matplotlib`
- `SimpleITK`
- `PyQt5`

## Instalación

Se recomienda crear un entorno virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecución

### Versión básica

```bash
python visualizar_mri_basica.py MR_Gd.nii
```

### Versión avanzada

```bash
python visualizar_mri_avanzada.py MR_Gd.nii
```

## Archivos incluidos

- `MR_Gd.nii`: imagen médica de ejemplo.
- `MR_Gd.nii.gz`: versión comprimida del mismo archivo.
- `visualizar_mri_basica.py`: visualización básica de la imagen.
- `visualizar_mri_avanzada.py`: visualización avanzada con interfaz gráfica.

## Descripción breve

La imagen se carga con `nibabel` y se transforma a un arreglo NumPy. Luego:

- se normaliza la intensidad para mejorar su visualización,
- se extrae una ROI central,
- se muestran cortes 2D en los ejes X, Y y Z,
- y en la versión avanzada se puede navegar por los cortes con sliders.

## Licencia

Este proyecto se distribuye con fines educativos y de investigación.
