import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401


def normalizar(img: np.ndarray) -> np.ndarray:
    """Normaliza una imagen a rango [0, 1]."""
    img_min = np.min(img)
    img_max = np.max(img)
    if img_max - img_min == 0:
        return np.zeros_like(img, dtype=np.float32)
    return ((img - img_min) / (img_max - img_min)).astype(np.float32)


def extraer_roi(data: np.ndarray, margen: float = 0.25):
    """Extrae una ROI centrada del volumen."""
    if data.ndim < 3:
        raise ValueError("La imagen debe tener al menos 3 dimensiones.")

    x0 = int(data.shape[0] * margen)
    x1 = int(data.shape[0] * (1 - margen))
    y0 = int(data.shape[1] * margen)
    y1 = int(data.shape[1] * (1 - margen))
    z0 = int(data.shape[2] * margen)
    z1 = int(data.shape[2] * (1 - margen))

    return data[x0:x1, y0:y1, z0:z1]


def mostrar_cortes_2d(img_norm: np.ndarray):
    """Muestra cortes centrales en los ejes X, Y y Z."""
    x_idx = img_norm.shape[0] // 2
    y_idx = img_norm.shape[1] // 2
    z_idx = img_norm.shape[2] // 2

    corte_x = img_norm[x_idx, :, :]
    corte_y = img_norm[:, y_idx, :]
    corte_z = img_norm[:, :, z_idx]

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    axes[0].imshow(corte_x, cmap="gray")
    axes[0].set_title("Corte X")
    axes[1].imshow(corte_y, cmap="gray")
    axes[1].set_title("Corte Y")
    axes[2].imshow(corte_z, cmap="gray")
    axes[2].set_title("Corte Z")

    for ax in axes:
        ax.axis("off")

    plt.tight_layout()
    plt.show()


def mostrar_3d(img_norm: np.ndarray, umbral: float = 0.8):
    """Muestra un volumen 3D usando un umbral de intensidad."""
    mask = img_norm > umbral
    x, y, z = np.where(mask)

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(x, y, z, c=z, cmap="jet", s=8, alpha=0.6)
    ax.set_title("Volumen 3D")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.show()


def main():
    parser = argparse.ArgumentParser(description="Visualizar imagen médica NIfTI.")
    parser.add_argument("archivo", type=str, help="Ruta al archivo NIfTI (.nii o .nii.gz)")
    args = parser.parse_args()

    path = Path(args.archivo)
    if not path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {path}")

    img = nib.load(str(path))
    data = img.get_fdata(dtype=np.float32)

    print("Forma de la imagen:", data.shape)
    print("Tipo de dato:", data.dtype)
    print("Rango de intensidades:", float(np.min(data)), float(np.max(data)))
    print("Voxel size (mm):", img.header.get_zooms()[:3])

    img_norm = normalizar(data)

    roi = extraer_roi(data)
    print("ROI shape:", roi.shape)
    print("Rango ROI:", float(np.min(roi)), float(np.max(roi)))

    roi_slice = roi[:, :, roi.shape[2] // 2]
    plt.figure(figsize=(6, 5))
    plt.imshow(roi_slice, cmap="gray")
    plt.title("ROI - Corte central")
    plt.axis("off")
    plt.show()

    mostrar_cortes_2d(img_norm)
    mostrar_3d(img_norm, umbral=0.8)


if __name__ == "__main__":
    main()
