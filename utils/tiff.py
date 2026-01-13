import rasterio
import matplotlib.pyplot as plt
import os


def disp_tiff(
    output_dir,
    name="local.tif"
):
    with rasterio.open(os.path.join(output_dir, name)) as src:
        band = src.read(1)
        bounds = src.bounds

    plt.imshow(
        band,
        extent=[bounds.left, bounds.right, bounds.bottom, bounds.top],
        cmap="inferno"
    )
    plt.colorbar()
    plt.title("Geo-referenced TIFF")
    plt.show()