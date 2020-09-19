import mimetypes
import pathlib
from typing import Dict

import uvicorn
from fastapi import FastAPI
from starlette.exceptions import HTTPException
from starlette.responses import Response, RedirectResponse
from whatchamacallit import make


spec_mapping: Dict[str, str] = {'gridchen/': '/gridchen/'}


def import_remap(path: pathlib.Path):
    source = make.resolve_package_resource(path)

    if not source.is_file():
        raise HTTPException(status_code=404, detail="Item not found")

    return Response(content=make.read_file(source, spec_mapping), media_type=mimetypes.guess_type(source.name)[0])


app = FastAPI()


@app.get(r"/{file_path:path}\.js")
def read_js(file_path: str):
    return import_remap(pathlib.Path(file_path + '.js'))


@app.get(r"/{file_path:path}\.html")
def read_html(file_path: str):
    return import_remap(pathlib.Path(file_path + '.html'))


@app.get(r"/{file_path:path}\.css")
def read_css(file_path: str):
    return import_remap(pathlib.Path(file_path + '.css'))


@app.get("/")
async def get_home():
    return RedirectResponse(url='/index.html')


# app.mount("/", StaticFiles(directory="."), name="static")

uvicorn.run(app, host="0.0.0.0", port=8081, access_log=True, log_level="trace", workers=1, debug=False)
