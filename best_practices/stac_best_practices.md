**1. Single Spatial Extent (e.g. global ERA5, dims: x, y, t, band)**

| Metadata level | Minimum requirements                                                | Optimal Requirements               | Example datasets                                                                                 |
|---------------------------|----------------------------------------------------------------------|-------------------------------------|--------------------------------------------------------------------------------------------------|
| Collection                | STAC extensions: - Datacube (spatial & temporal extent)             | STAC extensions: To be determined   | [ERA5 Planetary Computer](https://planetarycomputer.microsoft.com/api/stac/v1/collections/era5-pds) |
| Item                      | STAC extensions: - Datacube (spatial & temporal extent)**[?]**      |                                     |                                                                                                  |
| Asset                     |                                                                      |                                     |                                                                                                  |

**2. Tiled Spatial Extent (e.g. Sentinel-2, dims: x, y, t, band)**

| Metadata level | Minimum requirements                                                | Optimal Requirements                                                | Example datasets                                                                                 |
|---------------------------|----------------------------------------------------------------------|----------------------------------------------------------------------|--------------------------------------------------------------------------------------------------|
| Collection                | [OpenDataCube Best Practices](https://odc-stac.readthedocs.io/en/latest/stac-best-practice.html) | CDSE approach (Exact extensions to be determined) + summaries        | [CDSE Sentinel 2 L2A](https://stac.dataspace.copernicus.eu/v1/collections/sentinel-2-l2a)        |
| Item                      | [OpenDataCube Best Practices](https://odc-stac.readthedocs.io/en/latest/stac-best-practice.html) | CDSE + Datacube                                                     |                                                                                                  |
| Asset                     | File metadata                                                        | File metadata                                                        |                                                                                                  |

**3. Higher Dimensionality (dims > 4, dims: x, y, t, variable, height/z, ...)**

| Use Case / Metadata level | Minimum requirements                          | Optimal Requirements                                      | Example datasets                                                                                 |
|---------------------------|------------------------------------------------|------------------------------------------------------------|--------------------------------------------------------------------------------------------------|
| Collection                | Datacube X/Y and variable structure           | describe higher dimensions (e.g., altitude, ensemble)       | [ERA5 Planetary Computer](https://planetarycomputer.microsoft.com/api/stac/v1/collections/era5-pds) |
| Item                      |                                                |                                                            |                                                                                                  |
| Asset                     |                                                |                                                            |                                                                                                  |
