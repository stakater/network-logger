import os
import traceback
import requests

from flask import request, jsonify
from app.nl_app import nlapp
from app.logging_util import get_logger

log = get_logger()


@nlapp.route("/pod/a", methods=['GET'])
def get_pod_a():
    try:
        headers = request.headers
        log.info("POD-A, headers: %s", headers)
        args = dict(request.args)
        log.info("POD-A, args: %s", args)
        pod_b_route = os.environ.get("POD_B_ROUTE")
        log.info("POD-A, POD_B_ROUTE: %s", pod_b_route)
        pod_b_route = f"{pod_b_route}/pod/b"

        query_string = ""
        if args:
            for k, v in args.items():
                if query_string:
                    query_string = query_string+f"&{k}={v}"
                else:
                    query_string = f"?{k}={v}"
        pod_b_route = f"{pod_b_route}{query_string}"
        log.info("POD-A, Query String: %s", query_string)
        log.info("POD-A, POD_B_ROUTE: %s", pod_b_route)
        resp = requests.get(pod_b_route)
        log.debug("POD-A, POD-B Response: %s", resp.json())
        return jsonify({"source": "POD-A", "response": resp.json()})
    except Exception as e:
        log.error("POD-A, Error calling pod B : %s", traceback.format_exc())
        return jsonify({"source": "POD-A", "Error": str(e)})


@nlapp.route("/pod/b", methods=['GET'])
def get_pod_b():
    try:
        headers = request.headers
        log.info("POD-B, headers: %s", headers)
        args = dict(request.args)
        log.debug("POD-B, args: %s", args)
        return jsonify({"source": "POD-B", "response": args})
    except Exception as e:
        log.error("POD-B, Error: %s", traceback.format_exc())
        return jsonify({"source": "POD-B", "Error": str(e)})

