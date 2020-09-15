import pathlib
import importlib.util

from starlette.exceptions import HTTPException
from starlette.responses import HTMLResponse, Response

from whatchamacallit import make
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


class JavascriptResponse(Response):
    media_type = "text/javascript"


app = FastAPI()


@app.get(r"/{file_path:path}\.js", response_class=JavascriptResponse)
def read_js(file_path: str):
    source = pathlib.Path(file_path + '.js')
    if len(source.parts) > 1:
        prefix = source.parts[0].replace('@', '')
        spec = importlib.util.find_spec(prefix)
        if spec:
            origin = pathlib.Path(spec.origin)
            source = origin.parent.parent / source

    return make.read_file(source, {'gridchen/': '/gridchen/'})


@app.get(r"/{file_path:path}\.html", response_class=HTMLResponse)
def read_root(file_path: str):
    source = pathlib.Path(file_path + '.html')
    if not source.is_file():
        raise HTTPException(status_code=404, detail="Item not found")
    return make.read_file(source, {'gridchen/': '/gridchen/'})


app.mount("/", StaticFiles(directory="."), name="static")
