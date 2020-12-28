import mimetypes
import pathlib
from typing import Dict

from flask import Flask, request, Response
from werkzeug.exceptions import NotFound

from whatchamacallit import make
from whatchamacallit.make import ImportToPackageMapper


def import_remap(path: pathlib.Path, spec_mapping: Dict[str, str]):
    if path.suffix not in {'.js', '.html', '.css'}:
        return

    source = make.resolve_package_resource(path)
    if not source.is_file():
        raise NotFound()

    return Response(make.read_file(source, spec_mapping), mimetype=mimetypes.guess_type(source.name)[0])


def register(app: Flask, root_path: str = ''):
    spec_mapping = ImportToPackageMapper(root_path)
    app.before_request(lambda: import_remap(pathlib.Path(request.path[1:]), spec_mapping))
