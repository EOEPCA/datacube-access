# EOEPCA Datacube Access Best Practices for STAC

This best practice defines how to load data from various source into a datacube (e.g. xarray [Python], stars [R], rasdaman, etc.) for processing purposes and how to store it after processing. It recommends how to create STAC metadata to make loading data of various types into a datacube easy and predictable. All processed results should also conform to the given best practice.

Note: The following document is written based on the version numbers specified in the list below. The recommendations can mostly be backported to other versions of STAC and other versions of extensions. We recommend to implement the versions below though.

- [STAC v1.1](https://github.com/radiantearth/stac-spec/tree/v1.1.0) with [common metadata](https://github.com/radiantearth/stac-spec/blob/v1.1.0/commons/common-metadata.md)
- [Classification extension v2.x](https://github.com/stac-extensions/classification)
- [Datacube extension v2.x](https://github.com/stac-extensions/datacube)
- [Electro Optical (EO) Extension v2.x](https://github.com/stac-extensions/eo)
- [Projection Extension v2.x](https://github.com/stac-extensions/projection)
- [Raster Extension v2.x](https://github.com/stac-extensions/raster)
- [SAR Extension v1.x](https://github.com/stac-extensions/sar)

## General STAC best practices

The following definitions is based on the [Open Data Cube](https://odc-stac.readthedocs.io/en/latest/stac-best-practice.html) and [GDAL inspired best practices in the projection extension](https://github.com/stac-extensions/projection?tab=readme-ov-file#best-practices).

Fields should be provided in the granularity that's required for the data without duplicating information. For for example, if the data type differs per band, you'd want to provide the data type per band. If the data type is the same across all bands, provide the data type per asset.

### Items

Items should be generated so that each item reflects a specific timestamp that is identified in `datetime`.

- **Common metadata**
  - `datetime` set to a non-null value
- **Raster Extension** (v2.x)
  - `raster:spatial_resolution` (if the item has a single resolution, otherwise in the Asset)

### Assets

Each asset that points to measurements should provide the fields defined below. 

- **Common metadata**
  
  - `data_type`
  - `nodata` (if applicable)
  - `unit` (if applicable)
  
- **Projection Extension** (v2.x)
  
  - `proj:code`, or alternatively `proj:wkt2` or `proj:projjson` if no code is available for the CRS.
    
    `proj:code` can be set to `null` if one of the other two fields is provided. `proj:wkt2` and `proj:projjson` should never be set to `null`.
  - Two of the following: `proj:shape`, `proj:transform`, `proj:bbox`.
    
    `proj:bbox` should be omitted if the values match `bbox` property exactly (i.e. if `proj:code` "is a geographic coordinate reference system, using the World Geodetic System 1984 (WGS 84) datum, with longitude and latitude units of decimal degrees" (see [RFC 7946, ch. 4](https://datatracker.ietf.org/doc/html/rfc7946#section-4)).
  
- **Raster Extension** (v2.x)

  - `raster:spatial_resolution` (if multiple resolutions are provided in the item, otherwise specify it in the Item)
  - `raster:scale`
  - `raster:offset`

   **CAUTION:** The scale and offset should only be provided if the processing software explicitly has to apply the scale and the offset, e.g. for Sentinel-2 digital numbers. For netCDF files - where the scale and offset is applied automatically according to the netCDF specification - the scale and offset should **not** be provided.

- **Classification Extension** (v2.x)

  The Classification Extension should only be provided for **categorical data**.
  
  - `classification:classes`
  - `classification:bitfields` (if applicable)

#### Spectral data

- Common metadata
  - `bands` (in the order as they should appear in the datacube)
- Electro Optical (EO) Extension (v2.x)
  - `name`
    
     For users of the datacube extension, the names should also be provided as the `values` for the band dimension.
  - `eo:common_name` (if applicable)
  - `eo:center_wavelength` and `eo:full_width_half_max`

#### SAR data

- SAR Extension (v1.x)
  - `sar:polarizations` (in the order as they should appear in the datacube)

#### Other types of measurements

> [!NOTE] 
> This will be detailed once use cases come up. We welcome contributions to this section.
> 
> Generally speaking, users should follow any STAC best practices that exist for their types of measurements. The bands concept of STAC could be reused as well.

### Collections

Collections should contain as much information as possible to allow datacubes to be initiated before the items get loaded. As such the following information should be provided:

- Exact spatial and temporal extents (if not provided through the datacube extension)
- Datacube extension
  
  The datacube extension can be used to indicate how to construct the datacube even for non-datacube data. 
  *Note: Usually only extents can be provided but no specific dimension labels.*
- Bands (`bands`, providing the union of all available bands)
- Item Assets (`item_assets`)


> [!CAUTION]
> Unless the properties summarize the Item Properties, the properties (e.g. bands or the datacube fields) should be provided on the top-level and **not** in summaries.

## Datacubes

If loading from or storing to a datacube format (e.g. netCDF, ZARR, GRIB), the following is recommended:

- Datacube Extension (v2.x)
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
