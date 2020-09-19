import mimetypes
import pathlib
from typing import Dict

from flask import Flask, request, Response, redirect
from werkzeug.exceptions import NotFound

from whatchamacallit import make


spec_mapping: Dict[str, str] = {'gridchen/': '/gridchen/'}


def import_remap(path: pathlib.Path):
    if path.suffix not in {'.js', '.html', '.css'}:
        return

    source = make.resolve_package_resource(path)
    if not source.is_file():
        raise NotFound()

    return Response(make.read_file(source, spec_mapping), mimetype=mimetypes.guess_type(source.name)[0])


# Important: Do not use the evil static_url_path
app = Flask(__name__, static_folder=None)
app.before_request(lambda: import_remap(pathlib.Path(request.path[1:])))


@app.route('/', methods=['GET'])
def get_home():
    return redirect("/index.html", code=302)


app.run('localhost', 8082)
