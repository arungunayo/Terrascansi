# Example usage
# remove after use im the end after final product
from  utils.ndvi import get_ndvi
from utils.tiff import disp_tiff
output_dir = "C:/Users/aroha/terrariscan/data"
get_ndvi(
    output_dir,
    start_date="2025-01-01",
    end_date="2025-12-31",
    scale=60,
    project_id="terrariscan",
)

disp_tiff(output_dir,
          "delhi_ndvi_2025.tif")