import flask
from whatchamacallit.flask import register

# Important: Do not use the evil static_url_path
app = flask.Flask(__name__, static_folder=None)
register(app)


@app.route('/', methods=['GET'])
def get_home():
    return flask.redirect("/index.html", code=302)


app.run('localhost', 8082)
