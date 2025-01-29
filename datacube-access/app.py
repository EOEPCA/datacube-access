import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from pydantic_settings import BaseSettings, SettingsConfigDict

app = FastAPI()
load_dotenv()

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="GDC_")

    id: str
    title: str
    description: str
    stac_api: str

settings = Settings()

@app.get("/")
def root(request: Request):
    return {
        "gdc_version": "1.0.0-beta",
        "backend_version": "2.0.0-beta",
        "stac_version": "1.0.0",
        "api_version": "1.0.0",
        "type": "Catalog",
        "id": settings.id,
        "title": settings.title,
        "description": settings.description,
        "conformsTo": [
            "https://m-mohr.github.io/geodatacube-api",
            "https://api.stacspec.org/v1.0.0/core",
            "https://api.stacspec.org/v1.0.0/collections",
            "https://api.stacspec.org/v1.0.0/ogcapi-features",
            "http://www.opengis.net/spec/ogcapi-common-1/1.0/conf/core",
            "http://www.opengis.net/spec/ogcapi-common-1/1.0/conf/json",
            "http://www.opengis.net/spec/ogcapi-common-1/1.0/conf/oas30",
            "http://www.opengis.net/spec/ogcapi-common-2/1.0/conf/collections",
            "http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/core",
            "http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/oas30",
            "http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/geojson",
            "http://www.opengis.net/spec/ogcapi-coverages-1/1.0/conf/geodata-coverage",
            "http://www.opengis.net/spec/ogcapi-coverages-1/1.0/conf/cisjson",
            "http://www.opengis.net/spec/ogcapi-coverages-1/1.0/conf/coverage-subset",
            "http://www.opengis.net/spec/ogcapi-coverages-1/1.0/conf/oas30",
        ],
        "endpoints": [
            {"path": "/collections", "methods": ["GET"]},
            {"path": "/collections/{collection_id}", "methods": ["GET"]},
            {"path": "/collections/{collection_id}/queryables", "methods": ["GET"]},
        ],
        "links": [
            {
                "href": request.headers["host"],
                "rel": "self",
                "type": "application/json",
                "title": "This document",
            },
        ],
    }


@app.get("/conformance")
def conformance():
    return {
        "conformsTo": [
            "https://m-mohr.github.io/geodatacube-api",
            "https://api.stacspec.org/v1.0.0/core",
            "https://api.stacspec.org/v1.0.0/collections",
            "https://api.stacspec.org/v1.0.0/ogcapi-features",
            "http://www.opengis.net/spec/ogcapi-common-1/1.0/conf/core",
            "http://www.opengis.net/spec/ogcapi-common-1/1.0/conf/json",
            "http://www.opengis.net/spec/ogcapi-common-1/1.0/conf/oas30",
            "http://www.opengis.net/spec/ogcapi-common-2/1.0/conf/collections",
            "http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/core",
            "http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/oas30",
            "http://www.opengis.net/spec/ogcapi-features-1/1.0/conf/geojson",
            "http://www.opengis.net/spec/ogcapi-coverages-1/1.0/conf/geodata-coverage",
            "http://www.opengis.net/spec/ogcapi-coverages-1/1.0/conf/cisjson",
            "http://www.opengis.net/spec/ogcapi-coverages-1/1.0/conf/coverage-subset",
            "http://www.opengis.net/spec/ogcapi-coverages-1/1.0/conf/oas30",
        ]
    }

@app.get("/collections", tags=["Data Discovery"])
def collections(limit: int = 10):
    response = httpx.get(f"{settings.stac_api}/collections", params={"limit": limit})
    return JSONResponse(response.json(), response.status_code)

@app.get("/collections/{collection_id}", tags=["Data Discovery"])
def collection(collection_id: str):
    response = httpx.get(f"{settings.stac_api}/collections/{collection_id}")
    return JSONResponse(response.json(), response.status_code)

@app.get("/collections/{collection_id}/queryables", tags=["Data Discovery"])
def queryables(collection_id: str):
    response = httpx.get(f"{settings.stac_api}/collections/{collection_id}/queryables")
    return JSONResponse(response.json(), response.status_code)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
