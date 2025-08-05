# STAC Best Practices (for Datacube Access in EOEPCA)

This best practice defines how to load data from various source into a datacube (e.g. xarray [Python], stars [R], rasdaman, etc.) for processing purposes and how to store it after processing. It recommends how to create STAC metadata to make loading data of various types into a datacube easy and predictable. All processed results should also conform to the given best practice.

## General best practices

For general STAC best practices, please see <https://github.com/radiantearth/stac-best-practices/blob/main/metadata.md>.

## Datacubes

If loading from or storing to a datacube format (e.g. netCDF, ZARR, GRIB), the following is recommended:

- **Datacube Extension** (v2.x)
  
  - For a single variable: `cube:dimensions` only
  - For multiple variables: `cube:variables` and `cube:dimensions`
  
    Each variable should be a separate datacube, no attempt should be made to combine variables automatically.

## Raster data

For raster data that is not stored in a datacube format (e.g. GeoTiff, JPEG2000) the following is recommended to transform the imagery into datacubes and vice-versa.

### Loading

> [!NOTE]  
> This section is incomplete and just a list of ideas.

For satellite imagery (e.g. Sentinel-2 L2A), it may happen that ...

- ... sparse data
- ... overlap
- resolution: if different resolutions are available, which resolution to pick? upsample? downsample?
- creating horizontal spatial dimensions
- creating vertical spatial dimension
- creating time dimensions (intended step/interval?)
- creating bands dimension (homogeneous data types?)
- creating other dimensions (homogeneous data types?)

...

### Storing

To destruct a datacube into (multiple) raster files, the following is recommended:

> [!NOTE]
> Details will be provided in the next iteration.

## Vector data

For vector data that is not stored in a datacube format (e.g. GeoParquet) the following is recommended to transform the geometries and their properties into datacubes and vice-versa.

> [!NOTE]
> Details will be provided in the next iteration.
