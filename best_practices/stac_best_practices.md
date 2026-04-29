# STAC Best Practices (for Datacube Access in EOEPCA) <!-- omit in toc -->

This best practice defines how to load data from various source (e.g., a list of GeoTIFF files) into a datacube (e.g. xarray [Python], stars [R], rasdaman, etc.) for processing purposes and how to store it after processing. It recommends how to create STAC metadata to make loading data of various types into a datacube easy and predictable. All processed results should also conform to the given best practice.

> [!WARNING]
> This document is an early draft. Please provide feedback.

- [General Best Practices](#general-best-practices)
- [Datacubes](#datacubes)
- [Raster Data](#raster-data)
  - [Loading](#loading)
    - [Horizontal Spatial Dimensions](#horizontal-spatial-dimensions)
    - [Temporal Dimensions](#temporal-dimensions)
    - [Vertical Dimensions (Z-Axis)](#vertical-dimensions-z-axis)
    - [Band Dimensions](#band-dimensions)
    - [Other Dimensions](#other-dimensions)
  - [Storing](#storing)
    - [File Formats](#file-formats)
      - [Multi-Layer Raster Files (COG, JPEG2000, etc.)](#multi-layer-raster-files-cog-jpeg2000-etc)
      - [Datacube Formats (netCDF, ZARR)](#datacube-formats-netcdf-zarr)
        - [netCDF / HDF5](#netcdf--hdf5)
        - [Zarr](#zarr)
        - [GRIB / GRIB2](#grib--grib2)
    - [Dimension Handling](#dimension-handling)
      - [Horizontal Spatial Dimensions](#horizontal-spatial-dimensions-1)
      - [Temporal Dimensions](#temporal-dimensions-1)
      - [Band Dimensions](#band-dimensions-1)
      - [Other Dimensions](#other-dimensions-1)
- [Vector Data](#vector-data)

## General Best Practices

For general STAC best practices, please see <https://github.com/radiantearth/stac-best-practices/blob/main/metadata.md>.

## Datacubes

If loading from or storing to a datacube format (e.g. netCDF, ZARR, GRIB), the following is recommended:

- **Datacube Extension** (v2.x)
  - For a single variable: `cube:dimensions` only
  - For multiple variables: `cube:variables` and `cube:dimensions`
  
    Each variable should be a separate datacube, no attempt should be made to combine variables automatically.
- **STAC Item Granularity**: Consider whether a monolithic datacube store (e.g., one large Zarr) should be represented as a single STAC Item, or if temporal slices should be distinct Items using assets that index into the store via path subsets or byte-ranges.
- **Virtual Datacubes**: Reference recipes (e.g., Kerchunk for HDF5/netCDF) or GDAL VRT files could be registered as STAC Assets with specific roles and media types ([tbd](https://github.com/stac-extensions/datacube/issues/37)). This enables cloud-native reads over legacy, unoptimized formats without data duplication.

Example: A variable can be bands in EO data or meteorological variables like rain or temperature in meteorological data sets.

## Raster Data

For raster data that is not stored in a datacube format (e.g. GeoTiff, JPEG2000) the following is recommended to transform the imagery into datacubes and vice-versa.

### Loading

When loading raster data into datacubes, the following considerations and recommendations should be implemented.

Generally, if different choices of strategies are possible, the implemented strategy should be documented in the metadata.
The generation of the datacubes should be predictable.

Ensure homogeneous data types for the values in the datacube, choosing the most precise data type of the data types present.

#### Horizontal Spatial Dimensions

- **Labels**: The labels for the x and y dimensions should be the center coordinates of the pixels unless specified otherwise in metadata.
- **Coordinate Reference System (CRS)**: Use the `proj:code`/`proj:projjson`/`proj:wkt2` properties to identify the CRS.
  If multiple items have different CRS, either create a CRS dimension or reproject to a common target CRS before loading.
- **Resolution**: When items have different spatial resolutions:
  - Choose the finest common resolution, prefer upsampling lower resolution data over downsampling higher resolution data to avoid a loss of information.
  - Use the CRS (if a projected CRS in meters) and other projection properties (`proj:bbox` and `proj:shape`, or `proj:transform`) to determine the projected resolution. It is also the native resolution if no resampling has occurred.
  - The `gsd` or `raster:spatial_resolution` properties are usually average resolution values and as such can only be used indicative.
  - **Pyramids / Multi-resolution**: If an underlying format supports internal overviews (e.g., COG) or explicit multi-scales (Zarr), loading processes should allow the user to specify a target resolution. The processing engine should match the target with the closest available overview to optimize data transfer.

#### Temporal Dimensions

Generally, keep the temporal granularity as-is, i.e., don't combine data from a day to a single label
unless indicated differently by the user or metadata. When combining data and overlap exists,
the user must indicate the methodology unless indicated in the metadata.

- **Labels**: Create labels in the following priority:
  - Use the `datetime` property if not `null`
  - Otherwise, use `start_datetime` and `end_datetime` and encode it as a single value through ISO8601 time intervals

#### Vertical Dimensions (Z-Axis)

- **Labels**: For 3D or 4D datacubes (e.g., atmospheric or oceanographic data), represent the vertical axis as a dedicated spatial dimension (e.g., `z`, `elevation`, or `pressure`).
- Use the STAC property `unit` in the data cube extension to define the unit of measurement (e.g., meters for depth, hPa for atmospheric pressure)
- Use the `reference_system` in the data cube extension to specify the reference datum.

#### Band Dimensions

Use the `bands` array to identify band information, keep the order as identified in the array.

- **Labels**: Use the `name` property, if provided. Alternatively, use `eo:common_name`. As a last resort, use the array indices.
- **Data Types**: Ensure homogeneous data types across bands, choosing the most precise one.
  - If bands represent discrete classes (e.g., Land Cover, QA bands), map them to integer types and preserve the Classification extension metadata or colormaps (e.g., GDAL color tables, CF-convention flag meanings) to retain categorical semantic meaning.

#### Other Dimensions

For other dimensions, the datacube extension must be provided.

### Storing

To destruct a datacube into (multiple) raster files, the following considerations and recommendations should be implemented.

All files should be encompanied by corresponding STAC files that implement the
[STAC Metadata and Extension Best Practices](https://github.com/radiantearth/stac-best-practices/blob/main/metadata.md).

Prefer cloud-optimized formats (e.g. COG or ZARR) for better remote access performance.

Generally, if different choices of strategies are possible, the implemented strategy should be documented in the metadata.
The generation of the raster files should be predictable.

#### File Formats

##### Multi-Layer Raster Files (COG, JPEG2000, etc.)

- Bands should be created as one file per band (or all in a single file if the file format supports it efficiently)
- Use the layers for bands only, i.e. create separate files for each timestamp

##### Datacube Formats (netCDF, ZARR)

- Map original bands/variables directly to data variables within the file.
- Preserve all dimensions and their attributes, including the names.
- Apply chunking strategies that align with the expected access patterns (e.g., spatial vs. temporal subsetting).

###### netCDF / HDF5

netCDF is widely used format for multi-dimensional data, but it's not cloud-optimized unless using specialized mechanisms (like HDF5 chunking with byte-range requests). Can store all STAC dimensions natively as netCDF dimensions. Follow CF Conventions for mapping coordinates and variables. 

Be aware that many EO sources (e.g., Sentinel Level-1/2, NASA swath data) may be delivered as non-projected swath grids relying on 2D tie-point arrays rather than 1D coordinate indices; loading these requires explicit resampling/geolocation workflows.

###### Zarr

Zarr is recommended over netCDF as it offers cloud-native storage and streaming of multidimensional arrays efficiently in chunked, object-based storage.

Zarrs should follow the [GeoZarr specification](https://github.com/zarr-developers/geozarr-spec) and implement at least:

- the [geo-proj](https://github.com/zarr-conventions/geo-proj) convention for proper coordinate reference system definitions
- the [multiscales](https://github.com/zarr-conventions/multiscales) convention for more efficient pyramid-based processing depending on the level of detail
- the [spatial](https://github.com/zarr-conventions/spatial) convention for defining spatial dimensions and coordinates

The generated STAC metadata should follow the [STAC Zarr Best Practices](https://github.com/radiantearth/stac-best-practices/blob/main/best-practices-zarr.md).

###### GRIB / GRIB2

GRIB files for metorological data frequently encode multi-dimensional grids (parameter, time, vertical pressure level). These should be parsed into standard datacube dimensions (`x`, `y`, `t`, `z`, and `band`/`variable`) upon loading, or converted to Zarr for cloud-native workflows. Difficulties could occur with multiple "no data" values.

#### Dimension Handling

##### Horizontal Spatial Dimensions

- Maintain original pixel grid alignment when possible
- Include spatial reference system information in all formats
- Tiling Strategy: Use a common tiling scheme if the data size requires it (e.g. WGS84 1° or UTM).
- For larger regions, an equal-area CRS should be preferred.

##### Temporal Dimensions

- Convert dimension labels to `datetime` (instance) or `start_datetime` and `end_datetime` (interval) per STAC Item
- Timestamps / Intervals with a precision of less then a second (e.g. `2025-01-01`) need to be provided as interval

##### Band Dimensions

- Preserve band order from original datacube if applicable
- Retain band names when possible

##### Other Dimensions

- If a CRS dimension is present, retain the CRS when storing the files.
  Document the variability of the CRS in the collection metadata (`summaries`).

## Vector Data

For vector data that is not stored in a datacube format (e.g. GeoParquet) the following is recommended to transform the geometries and their properties into datacubes and vice-versa.

> [!NOTE]
> Details will be provided in the next iteration.
