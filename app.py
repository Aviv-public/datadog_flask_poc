import os
from flask import Flask, abort, jsonify, current_app


class Config:
    DEBUG = os.environ.get('FLASK_DEBUG', False)
    ENV = os.environ.get('FLASK_ENV', "dev")


app = Flask(__name__)
app.config.from_object(Config)


@app.route("/")
def hello():
    config_json = {k: str(v) for k, v in current_app.config.items()}
    return jsonify(config_json)


@app.route("/raise")
def raise_exception():
    raise Exception("Exception message")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
