import os
import json
import traceback
import requests

from flask import request, jsonify

from app.json_logger import get_logger
from app.nl_app import nlapp

log = get_logger()


@nlapp.route("/pod/a", methods=['GET'])
def get_pod_a():
    try:
        headers = request.headers
        # log.info("POD-A, headers: %s", headers)
        args = dict(request.args)
        pod_b_route = os.environ.get("POD_B_ROUTE")
        pod_b_route = f"{pod_b_route}/pod/b"
        query_string = ""
        if args:
            for k, v in args.items():
                if query_string:
                    query_string = query_string+f"&{k}={v}"
                else:
                    query_string = f"?{k}={v}"
        pod_b_route = f"{pod_b_route}{query_string}"
        log.info({"sender": "pod-A", "podBRoute": pod_b_route})
        resp = requests.get(pod_b_route)
        log.info({"sender": "pod-A", "podBResponse": resp.json(), "statusCode": resp.status_code})
        return jsonify({"sender": "POD-A", "response": resp.json()["response"]})
    except Exception as e:
        log.error("POD-A, Error calling pod B : %s", traceback.format_exc())
        return jsonify({"sender": "POD-A", "Error": str(e)})


@nlapp.route("/pod/b", methods=['GET'])
def get_pod_b():
    try:
        headers = request.headers
        # log.info("POD-B, headers: %s", headers)
        args = dict(request.args)
        log.info({"receiver": "pod-B", "args": args})
        return jsonify({"receiver": "POD-B", "response": args})
    except Exception as e:
        log.error("POD-B, Error: %s", traceback.format_exc())
        return jsonify({"receiver": "POD-B", "Error": str(e)})

