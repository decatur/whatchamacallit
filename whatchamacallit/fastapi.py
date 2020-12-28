import mimetypes
import pathlib
from typing import Dict

from fastapi import FastAPI
from starlette.exceptions import HTTPException
from starlette.responses import Response

from whatchamacallit import make
from whatchamacallit.make import ImportToPackageMapper


def import_remap(path: pathlib.Path, spec_mapping: Dict[str, str]):
    source = make.resolve_package_resource(path)

    if not source.is_file():
        raise HTTPException(status_code=404, detail="Item not found")

    return Response(content=make.read_file(source, spec_mapping), media_type=mimetypes.guess_type(source.name)[0])


def register(app: FastAPI, root_path: str = ''):
    spec_mapping = ImportToPackageMapper(root_path)

    @app.get(r"/{file_path:path}\.js")
    def read_js(file_path: str):
        return import_remap(pathlib.Path(file_path + '.js'), spec_mapping)

    @app.get(r"/{file_path:path}\.html")
    def read_html(file_path: str):
        return import_remap(pathlib.Path(file_path + '.html'), spec_mapping)

    @app.get(r"/{file_path:path}\.css")
    def read_css(file_path: str):
        return import_remap(pathlib.Path(file_path + '.css'), spec_mapping)