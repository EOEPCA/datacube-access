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

**1.** Register External Data and apply STAC Best Practices: [S5P Cloud Fraction](https://github.com/EOEPCA/demo/blob/main/demoroot/notebooks/08-1%20E2E%20External%20Data%20Registration%20CF.ipynb)

![End-to-end workflow cf](https://raw.githubusercontent.com/EOEPCA/demo/main/demoroot/notebooks/img/end2end_workflow_cf.png)

**2.** Register External Data and apply STAC Best Practices: [S5P NO2 (WIP)](https://github.com/EOEPCA/demo/blob/main/demoroot/notebooks/08-2%20E2E%20External%20Data%20Registration%20NO2.ipynb)

![End-to-end workflow no2](https://raw.githubusercontent.com/EOEPCA/demo/main/demoroot/notebooks/img/end2end_workflow_no2.png)

**3.** Process the two data sets together and register the Results: [Cloud Free Monthly NO2 Means (WIP)](https://github.com/EOEPCA/demo/blob/main/demoroot/notebooks/08-3%20E2E%20Process%20Data%20Jointly.ipynb)

![End-to-end workflow proc](https://raw.githubusercontent.com/EOEPCA/demo/main/demoroot/notebooks/img/end2end_workflow_proc.png)

