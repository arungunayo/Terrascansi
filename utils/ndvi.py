import ee
import geemap
import os


def get_ndvi(
    output_dir,
    start_date="2025-01-01",
    end_date="2025-12-31",
    scale=60,
    project_id="terrariscan",
):
    """
    Computes Sentinel-2 NDVI for Delhi and downloads it locally.

    Parameters
    ----------
    output_dir : str
        Local directory to save the NDVI GeoTIFF
    start_date : str
        Start date (YYYY-MM-DD)
    end_date : str
        End date (YYYY-MM-DD)
    scale : int
        Spatial resolution in meters (30 recommended for city-scale)
    project_id : str
        Google Cloud project ID linked to Earth Engine

    Returns
    -------
    str
        Path to downloaded NDVI file
    """

    # ------------------ AUTH ------------------
    try:
        ee.Initialize(project=project_id)
    except Exception:
        ee.Authenticate()
        ee.Initialize(project=project_id)

    # ------------------ DELHI ROI ------------------
    states = ee.FeatureCollection("FAO/GAUL/2015/level1")
    delhi = states.filter(ee.Filter.eq("ADM1_NAME", "Delhi"))
    roi = delhi.geometry().simplify(100)

    # ------------------ CLOUD MASK ------------------
    def mask_s2_clouds(image):
        qa = image.select("QA60")
        cloud = 1 << 10
        cirrus = 1 << 11
        mask = qa.bitwiseAnd(cloud).eq(0).And(
               qa.bitwiseAnd(cirrus).eq(0))
        return image.updateMask(mask).divide(10000)

    # ------------------ LOAD SENTINEL-2 ------------------
    s2 = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterBounds(roi)
        .filterDate(start_date, end_date)
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20))
        .map(mask_s2_clouds)
    )

    # ------------------ NDVI ------------------
    ndvi = (
        s2.median()
        .normalizedDifference(["B8", "B4"])
        .rename("NDVI")
        .clip(roi)
    )

    # ------------------ EXPORT ------------------
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(
        output_dir, f"delhi_ndvi_{start_date[:4]}.tif"
    )

    geemap.ee_export_image(
        ndvi,
        filename=output_path,
        scale=scale,
        region=roi,
        file_per_band=False,
    )

    return output_path
