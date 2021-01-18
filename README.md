# whatchamacallit

Use web resources the pythonic way, import JavaScript modules like you do with Python modules.
Specify Javascript modules, HTML, CSS as bare URLs and rewrite on the fly.

# Example

(A) Install the desired package, in this example [gridchen](https://github.com/decatur/grid-chen)
````shell script
pip install gridchen
````

(B) From HTML/JavaScript
````HTML
<!DOCTYPE html>
<h1>Hello World</h1>
<script type="module">
    import * as utils from "gridchen/utils.js";
    const tm = utils.createTransactionManager();
</script>
````

(C) Register your FastAPI app (see also module whatchamacallit.examples.fastapi_server.py)
````Python
from fastapi import FastAPI
from whatchamacallit.fastapi import register

app = FastAPI()
register(app)
````

or Flask app (see also module whatchamacallit.examples.flask_server.py)
````Python
import flask
from whatchamacallit.flask import register

# Important: Do not use the evil static_url_path
app = flask.Flask(__name__, static_folder=None)
register(app)
````


# Working

Ultimately, the `import * as utils from "gridchen/utils.js"` must be mapped to its physical location, for example
`/C/projects/myproject/venv/Lib/site-packages/gridchen/utils.js`.
This is done in two steps.

## Remap bare import specifier

The `import * as utils from "gridchen/utils.js"` is **not** valid JavaScript. So at HTML/JavaScript load time the
import is remapped to `import * as utils from "/@gridchen/utils.js"`

## Route resource to Python module

When the server now gets the request for `/@gridchen/utils.js`, then it resolves to the package `gridchen`
and serve its resource `utils.js`.

# Contribute

## Package

````shell script
vi pyproject.toml
git add pyproject.toml
git commit -m'bumped version'
git tag x.y.z
git push & git push --tags
python3 setup.py sdist bdist_wheel

## Publishing

````shell script
python3 -m twine upload --repository testpypi dist/*
````

# Previous Work

## Bundlers
Unpkg.com, rollup, webpack, babel, pika, assetgraph, Browserify, gulp, JSPM

## In Place Handlers
* [Snowpack](https://github.com/pikapkg/snowpack)
* [Browsersync](https://browsersync.io)
* [ES Module Shims](https://github.com/guybedford/es-module-shims)

## References
* http://dplatz.de/blog/2019/es6-bare-imports.html
* https://jakearchibald.com/2017/es-modules-in-browsers/
* https://medium.com/@dmnsgn/in-2020-go-bundler-free-eb29c1f05fc9
* https://wicg.github.io/import-maps/
* https://medium.com/@dmnsgn/es-modules-in-the-browser-almost-now-3638ffafdc68
* https://github.com/fanstatic/fanstatic
* Packages on [PyPI starting with js.](https://pypi.org/search/?q=%22js.%22&o=)
