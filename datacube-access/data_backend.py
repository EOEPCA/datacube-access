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


class STACAPIBackend:
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
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code, detail=e.response.text
            )
        return response.json()


async def get_data_backend(
    config: Annotated[Config, Depends(get_config)],
) -> DataBackend:
    response = await CLIENT.get(config.data_backend)
    response.raise_for_status()

    endpoint_data: dict = response.json()

    if endpoint_data.get("stac_version"):
        return STACAPIBackend(config.data_backend, endpoint_data)

    raise NotImplementedError("Unsupported data backend")
