import re
from typing import Annotated, Protocol

import httpx
from fastapi import Depends, HTTPException

from .config import Config, get_config

limits = httpx.Limits(max_keepalive_connections=5, max_connections=20)
timeout = httpx.Timeout(10.0, connect=60.0)

CLIENT = httpx.AsyncClient(timeout=timeout, limits=limits)


class DataBackend(Protocol):
    @property
    def endpoints(self) -> list[dict]: ...

    def get_endpoints(self) -> list[dict]: ...

    def get_version(self) -> str: ...

    def get_links(self) -> list[dict]: ...

    def get_conformance(self) -> list[str]: ...

    async def get_data(self, path: str, *args, **kwargs) -> dict: ...

    def filter(self, data: dict) -> dict: ...


class STACAPIBackend:
    datacube_regex = "https://stac-extensions.github.io/datacube/v2.\d.\d/schema.json"

    def __init__(self, url: str, response_data: dict):
        self.url = url
        self.response_data = response_data

    @property
    def endpoints(self) -> list[dict]:
        return [
            {
                "path": "/collections",
                "methods": ["GET"],
                "regex": "/collections/?",
            },
            {
                "path": "/collections/{collection_id}",
                "methods": ["GET"],
                "regex": "/collections/[^/]+",
            },
            {
                "path": "/collections/{collection_id}/queryables",
                "methods": ["GET"],
                "regex": "/collections/[^/]+/queryables",
            },
        ]

    def get_endpoints(self) -> list[dict]:
        endpoints = []
        for endpoint in self.endpoints:
            endpoints.append(
                {
                    "path": endpoint["path"],
                    "methods": endpoint["methods"],
                }
            )
        return endpoints

    def get_version(self) -> str:
        return self.response_data["stac_version"]

    def get_links(self) -> list[dict]:
        links = self.response_data["links"]

        return [
            link for link in links if link["rel"] != "self" and link["rel"] != "root"
        ]

    def get_conformance(self) -> list[str]:
        return self.response_data["conformsTo"]

    async def get_data(self, path: str, *args, **kwargs) -> dict:
        is_path_found = False
        for endpoint in self.endpoints:
            if re.fullmatch(endpoint["regex"], path):
                is_path_found = True
                break

        if not is_path_found:
            raise HTTPException(status_code=404, detail="Path not found")

        response = await CLIENT.get(f"{self.url}{path}", *args, params=kwargs)
        while 300 <= response.status_code < 400:
            # Handle redirects
            if "location" not in response.headers:
                raise HTTPException(
                    status_code=500, detail="Redirect without location header"
                )
            response = await CLIENT.get(
                response.headers["location"], *args, params=kwargs
            )

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code, detail=e.response.text
            )

        return response.json()

    def filter(self, data: dict) -> dict:
        """Filter STAC best practices from the data."""
        if "collections" in data:
            # filtering collections
            best_practice_collections = []
            for collection in data["collections"]:
                for extension in collection.get("stac_extensions", []):
                    if re.fullmatch(self.datacube_regex, extension) and (
                        collection.get("cube:variables")
                        or collection.get("cube:dimensions")
                    ):
                        best_practice_collections.append(collection)
                        break

            filtered_data = {
                "links": data.get("links", []),
                "collections": best_practice_collections,
            }
        elif "type" in data and data["type"] == "Collection":
            # filtering single collection
            if (
                "stac_extensions" in data
                and any(
                    re.fullmatch(self.datacube_regex, ext)
                    for ext in data["stac_extensions"]
                )
                and ("cube:variables" in data or "cube:dimensions" in data)
            ):
                filtered_data = data
            else:
                raise HTTPException(
                    status_code=400, detail="Collection does not follow best practices"
                )
            filtered_data = data
        elif "type" in data and data["type"] == "FeatureCollection":
            # filtering list of items
            filtered_data = data
        elif "type" in data and data["type"] == "Item":
            # filtering single item
            filtered_data = data

        return filtered_data


async def get_data_backend(
    config: Annotated[Config, Depends(get_config)],
) -> DataBackend:
    response = await CLIENT.get(config.data_backend)
    response.raise_for_status()

    endpoint_data: dict = response.json()

    if endpoint_data.get("stac_version"):
        return STACAPIBackend(config.data_backend, endpoint_data)

    raise NotImplementedError("Unsupported data backend")
