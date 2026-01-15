# End to End Use Case

The Data Cube Access Building Block elaborates an end-to-end use case that shows how EOEPCA Building Blocks are used together to solve a real world problem covering the following steps:

- **Get external data sets**: Ingest arbitrary STAC Collections into EOEPCA, so that users have alle relevant data available at one single point.
- **Apply STAC Best Practices**: Adapt the STAC metadata so that it conforms to the STAC Best Practices. This ensures best quality metadata and transition from one Building Block to another.
- **Save metadata**: Save the adapted metadata on a storage bucket that is accessible to other users and other Building Blocks.
- **Register updated metadata to the STAC API**: Make the updated metadata available through teh EOEPCA STAC API.
- **Access and Process the registered data sets**: Use the data by processing new information from it.
- **Register the results to the STAC API**: Make the results findable, accessible, interoperable and reusable by registering them to the STAC API.

![End-to-end workflow](https://raw.githubusercontent.com/EOEPCA/demo/main/demoroot/notebooks/img/end2end_workflow.png)

The notebooks that make up the end-to-end use case can be found here:

- Register External Data and apply STAC Best Practices: [S5P Cloud Fraction](https://github.com/EOEPCA/demo/blob/main/demoroot/notebooks/08%20Use%20Case%20External%20Data%20Registration.ipynb)
- Register External Data and apply STAC Best Practices: S5P NO2 (WIP)
- Process the two data sets together and register the Results: Cloud Free Monthly NO2 Means (WIP)
