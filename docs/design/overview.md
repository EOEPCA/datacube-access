# Architecture

## Design Overview
The Datacube Access Building Block combines existing Building Blocks to allow users to discover and access datacubes efficiently.

Workspace BB
- Workspace: Is used to store intermediate data, especially adapted STAC metadata to comply to the STAC Best Practices.

Data Access BB
- Resource Registration: Allows to register external data sources to the EOEPCA STAC API. This is crucial to make data available via EOEPCA.
- STAC API: Allows searching for data sets and querrying them by spatial, temporal and thematic filters.
- Visualization: Allows quick visualization of data cube slices. It relies on the openEO- implementation.

Processing BB
- Data Cube Access: openEO allows to slice and dice the data cube to the relevant extent and to receive only the relevant information.
- Processing: Furthermore, openEO and OGC API Processes allow to process data cubes to create new information, either using and chaining predefined processes (openEO) or by creating custom pipelines (OGC API Processes)
- STAC Best Practices: Results obtained with openEO and OGC API Processes aim at following the STAC Best Practices wherever possible.

flowchart LR
    classDef center fill:#e3f2fd,stroke:#1e88e5,stroke-width:2px;

    W["Workspace BB"] --- DA["Datacube Access BB"]
    D["Data Access BB"] --- DA
    P["Processing BB"] --- DA

    class DA center;

## STAC Best Practices
To enable the interoperability between multiple Building Blocks, such as passing data from the STAC API (Data Access BB) to the openEO Processing API (Processing BB), conventions need to be in place on how to pass on data.
Therefore, STAC Best Practices need to be followed and further developed:
 - Official STAC Best Practices
 - STAC Best Practices for Data Cubes made of arbitrary files
 - STAC Best Practices for Data Cubes made of Zarr files

The Datacube Access Building Block is developing, applying and testing the STAC Best Practices within the EOEPCA Context, to ensure the interoperability between Building Blocks.

