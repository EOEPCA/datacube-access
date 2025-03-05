from typing import Annotated

import httpx
import uvicorn
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Request

from .config import Config, get_config
from .data_backend import DataBackend, get_data_backend

VERSION = "0.0.1"

app = FastAPI()
load_dotenv()


timeout = httpx.Timeout(10.0, connect=60.0)
limits = httpx.Limits(max_keepalive_connections=5, max_connections=20)

CLIENT = httpx.AsyncClient(timeout=timeout, limits=limits)


@app.get("/")
async def root(
    request: Request,
    config: Annotated[Config, Depends(get_config)],
    data_backend: Annotated[DataBackend, Depends(get_data_backend)],
):

    conformance = ["https://m-mohr.github.io/geodatacube-api"]
    conformance.extend(data_backend.get_conformance())
    links = [
        {
            "href": request.headers["host"],
            "rel": "self",
            "type": "application/json",
            "title": "This document",
        },
        {
            "href": request.headers["host"],
            "rel": "root",
            "type": "application/json",
            "title": "This document",
        },
    ]
    links.extend(data_backend.get_links())
    return {
        "gdc_version": "1.0.0-beta",
        "backend_version": VERSION,
        "stac_version": data_backend.get_version(),
        "api_version": "1.0.0",
        "type": "Catalog",
        "id": config.id,
        "title": config.title,
        "description": config.description,
        "conformsTo": conformance,
        "endpoints": data_backend.get_endpoints(),
        "links": links,
    }


@app.get("/conformance")
async def conformance(
    data_backend: Annotated[DataBackend, Depends(get_data_backend)],
):
    conformance = ["https://m-mohr.github.io/geodatacube-api"]
    conformance.extend(data_backend.get_conformance())

    return {"conformsTo": conformance}


@app.get("/collections{rest_of_path:path}", tags=["Data Discovery"])
async def collections(
    data_backend: Annotated[DataBackend, Depends(get_data_backend)],
    rest_of_path: str,
):
    full_path = f"/collections{rest_of_path}"
    data = await data_backend.get_data(full_path)
    return data


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
