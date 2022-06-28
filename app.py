import logging

from flask import Flask, jsonify, current_app

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)


@app.route("/")
def hello():
    config_json = {k: str(v) for k, v in current_app.config.items()}
    return jsonify(config_json)


@app.route("/raise")
def raise_exception():
    raise Exception("Exception message")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
