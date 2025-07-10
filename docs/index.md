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

The Data Cube Access BB describes the possibility to discover and access multi-dimensional data as data cubes and enable their functionalities. The focus lies on fast lightweight operations and interactivity.
The STAC API supports data discovery and access. In combination with the pangeo ecosystem (i.e., odc_stac and xarray) partial access and prototyping of processing tasks is enabled. A variety of data storage formats, such as S3 object storage, HTTP, and file system is supported. This is fulfilled by reusing the components from the data access building block. 
The Data Cube Access BB acts as an interface to the Processing BB by adhering to STAC Best Practices which ensure data cube ready collections are exposed to the Processing APIs such as OGC API Processes or OpenEO API. As such, it is designed in a way that it builds upon and can be integrated as an embedded capability within the APIs of other building blocks (Data Access, Resource Discovery, Processing).

## Capabilities
A typical user journey includes 

- Data Discovery
Users want to interactively discover and filter EO data from different Data Cubes as well as their queryables (e.g., band names, valid time range) using a browser. They also want to be able to do this programmatically with a straightforward API. So that queries can be quickly generated to access spatial and temporal extents of the data cube to discover patterns, trends, and anomalies without downloading massive datasets.

- Data Cube Access
Users want to, programmatically partially access (subset) small-scale spatiotemporal data cubes. So that it is possible to (a) extract data for sanity checks and (b) do lightweight processing efficiently without manually handling raw satellite data (e.g. ndvi time series over a region). This especially valuable for prototyping before movig to large scale processing using the Processing BB.

- Data Visualization
Users want to visualize EO data easily and quickly.
Therefore, they want to seamlessly and programatically generate lightweight online maps and plots from (a) Data Cubes and (b) Data Cube queries,
So that intuitive interpretation of (a) satellite imagery and (b) derived analytics is facilitated.
