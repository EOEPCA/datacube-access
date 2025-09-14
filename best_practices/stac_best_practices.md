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

When loading raster data into datacubes, the following considerations and recommendations should be implemented.

Generally, if different choices of strategies are possible, the implemented strategy should be documented in the metadata.
The generation of the datacubes should be predictable.

Ensure homogeneous data types for the values in the datacube, choosing the most precise data type of the data types present (e.g. float over int).

#### Horizontal Spatial Dimensions

- **Labels**: The labels for the x and y dimensions should be the center coordinates of the pixels.
- **Coordinate Reference System (CRS)**: Use the `proj:code`/`proj:projjson`/`proj:wkt2` properties to identify the CRS.
  If multiple items have different CRS, either create a CRS dimension or reproject to a common target CRS before loading.
- **Resolution**: When items have different spatial resolutions:
  - Choose the finest common resolution, prefer upsampling lower resolution data over downsampling higher resolution data
  - Use `gsd`/`raster:spatial_resolution` properties to determine native resolution

#### Temporal Dimensions

Generally, keep the temporal granularity as-is, i.e. don't combine data from a day to a single label
unless indicated differently by the user or metadata. When combining data and overlap exists,
the user must indicate the methodology unless indicated in the metadata.

- **Labels**: Create labels in the following priority:
  - Use the `datetime` property if not `null`.
  - Otherwise, use `start_datetime` and `end_datetime` and encode it as a single value through ISO8601 time intervals

#### Band Dimensions

Use the `bands` array to identify band information, keep the order as identified in the array.

- **Labels**: Use the `name` property, if provided. Alternatively, use `eo:common_name`. As a last resort, use the array indices.
- **Data Types**: Ensure homogeneous data types across bands, choosing the most precise one.

#### Other Dimensions

For other dimensions, the datacube extension must be provided.

### Storing

When converting datacubes back to raster files, follow these recommendations:

To destruct a datacube into (multiple) raster files, the following is recommended:

> [!NOTE]
> Details will be provided in the next iteration.

## Vector data

For vector data that is not stored in a datacube format (e.g. GeoParquet) the following is recommended to transform the geometries and their properties into datacubes and vice-versa.

> [!NOTE]
> Details will be provided in the next iteration.
