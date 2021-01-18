# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['whatchamacallit', 'whatchamacallit.examples']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.9"': ['importlib-resources>=3.0,<4.0']}

setup_kwargs = {
    'name': 'whatchamacallit',
    'version': '0.0.4',
    'description': 'Use web resources the pythonic way, import JavaScript modules like you do with Python modules.',
    'long_description': '# whatchamacallit\n\nUse web resources the pythonic way, import JavaScript modules like you do with Python modules.\nSpecify Javascript modules, HTML, CSS as bare URLs and rewrite on the fly.\n\n# Example\n\n(A) Install the desired package, in this example [gridchen](https://github.com/decatur/grid-chen)\n````shell script\npip install gridchen\n````\n\n(B) From HTML/JavaScript\n````HTML\n<!DOCTYPE html>\n<h1>Hello World</h1>\n<script type="module">\n    import * as utils from "gridchen/utils.js";\n    const tm = utils.createTransactionManager();\n</script>\n````\n\n(C) Register your FastAPI app (see also module whatchamacallit.examples.fastapi_server.py)\n````Python\nfrom fastapi import FastAPI\nfrom whatchamacallit.fastapi import register\n\napp = FastAPI()\nregister(app)\n````\n\nor Flask app (see also module whatchamacallit.examples.flask_server.py)\n````Python\nimport flask\nfrom whatchamacallit.flask import register\n\n# Important: Do not use the evil static_url_path\napp = flask.Flask(__name__, static_folder=None)\nregister(app)\n````\n\n\n# Working\n\nUltimately, the `import * as utils from "gridchen/utils.js"` must be mapped to its physical location, for example\n`/C/projects/myproject/venv/Lib/site-packages/gridchen/utils.js`.\nThis is done in two steps.\n\n## Remap bare import specifier\n\nThe `import * as utils from "gridchen/utils.js"` is **not** valid JavaScript. So at HTML/JavaScript load time the\nimport is remapped to `import * as utils from "/@gridchen/utils.js"`\n\n## Route resource to Python module\n\nWhen the server now gets the request for `/@gridchen/utils.js`, then it resolves to the package `gridchen`\nand serve its resource `utils.js`.\n\n# Contribute\n\n## Package\n\n````shell script\nvi pyproject.toml\ngit add pyproject.toml\ngit commit -m\'bumped version\'\ngit tag x.y.z\npoetry build\n\n## Publishing\n\n````shell script\npoetry publish\n````\n\n# Previous Work\n\n## Bundlers\nUnpkg.com, rollup, webpack, babel, pika, assetgraph, Browserify, gulp, JSPM\n\n## In Place Handlers\n* [Snowpack](https://github.com/pikapkg/snowpack)\n* [Browsersync](https://browsersync.io)\n* [ES Module Shims](https://github.com/guybedford/es-module-shims)\n\n## References\n* http://dplatz.de/blog/2019/es6-bare-imports.html\n* https://jakearchibald.com/2017/es-modules-in-browsers/\n* https://medium.com/@dmnsgn/in-2020-go-bundler-free-eb29c1f05fc9\n* https://wicg.github.io/import-maps/\n* https://medium.com/@dmnsgn/es-modules-in-the-browser-almost-now-3638ffafdc68\n* https://github.com/fanstatic/fanstatic\n* Packages on [PyPI starting with js.](https://pypi.org/search/?q=%22js.%22&o=)\n',
    'author': 'Wolfgang Kühn',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/decatur/whatchamacallit',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
