from flask import Flask, request, jsonify
from http import HTTPStatus
from threading import Thread
from logging import getLogger, ERROR
from common.app.data_models.message import Message
from common.app.constants.TextConstants import TextConstants
from common.app.core.tools.api.adapter import QtAdapter
import click


app = Flask(__name__)
getLogger('werkzeug').setLevel(ERROR)


# The click module methods rewriting to avoid Flask output to the console
click.echo = lambda _: ...
click.secho = lambda _: ...


@app.route("/api/docs", methods=["GET"])
def get_documents():
    return TextConstants.HELLO_MESSAGE, HTTPStatus.OK


@app.route("/api/transactions", methods=["POST"])
def create_transaction():
    message: Message = Message.parse_obj(request.json)
    adapter: QtAdapter = QtAdapter()
    adapter.emit_message_ready(message)
    return message.json()


@app.route("/api/transactions/<string:trans_id>", methods=["GET"])
def get_transaction(trans_id):
    return trans_id, HTTPStatus.OK


@app.route("/api/transactions/<string:trans_id>/reverse", methods=["POST"])
def reverse_transaction(trans_id):
    return f"{trans_id}_R", HTTPStatus.OK


@app.route("/api/test-cases/<string:ips>/<string:case>", methods=["POST"])
def send_default_purchase(case, ips):
    if ips.lower() not in ("visa", "mastercard"):
        return jsonify({"error": f"IPS {ips} was not found. Supported IPS: visa, mastercard"}), HTTPStatus.NOT_FOUND

    if case.lower() not in ("purchase", "payout"):
        return jsonify({"error": f"Case {case} was not found. Supported cases: purchase, payout"}), HTTPStatus.NOT_FOUND

    return case, HTTPStatus.OK


@app.route("/off", methods=["POST"])
def shutdown():
    print(request.environ.get("werkzeug.server"))
    return "OK"


def r():
    app.run()


# def run_api(host, port):
from multiprocessing import Process
p = Process(target=r)
p.start()
# app.run()

    # from time import sleep
    # from multiprocessing import Process
    # p = Process(target=app.run)
    # p.start()

    # thread = Thread(target=lambda: app.run(host=host, port=port))
    # thread.start()
    # sleep(1)
    # import requests
    # requests.get("http://localhost:5001/off")


