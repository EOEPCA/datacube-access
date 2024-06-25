# Introduction

The documentation for the `Datacube Access` building block is organised as follows

<!-- * **Introduction**<br>
  Introduction to the BB - including summary of purpose and capabilities.
* **Getting Started**<br>
  Quick start instructions - including installation, e.g. of a local instance.
* **Design**<br>
  Description of the BB design - including its subcomponent architecture and interfaces.
* **Usage**<br>
  Tutorials, How-tos, etc. to communicate usage of the BB.
* **Administration**<br>
  Configuration and maintenance of the BB.
* **API**<br>
  Details of APIs provided by the BB - including endpoints, usage descriptions and examples etc. -->

## About `Datacube Access`

The Data Cube Access BB describes the possibility to access multi-dimensional
data in relation to the OGC GeoDataCube API. Although the API specification
is still in an early draft, it combines currently developed OGC API
Coverages, OGC API Features, and STAC API for data discovery and access.
Those can be combined in a single API and combined with processing APIs, such
as OGC API Processes or OpenEO API. Components from the Data Access BB and
Resource Discovery BB can be reused and combined in this building block.

The Data Cube Access interface shall be able to act as data access interface
of the openEO processing building block. As such, it shall be designed in a
way that it can be integrated as an embedded capability within the APIs of
other building blocks.

The building block shall support a variety of data storage formats, such as
S3 object storage, HTTP, and file system. This can be fulfilled by reusing
the components from the data access building block. In addition, the API
implemented shall be demonstrated for the usage of the pangeo libraries. As
an example, it can be demonstrated using STAC API for data discovery together
with a conversion to an xarray-based virtual data cube. This is useful to
demonstrate the capabilities of the combination of those APIs as part of the
OGC GeoDataCube API.

## Capabilities

Summary of the capabilities of the BB.
