import os
import traceback
import requests

from flask import request, jsonify
from app.app import nl_app
from app.logging_util import get_logger

log = get_logger()


@nl_app.route("/pod/a/", methods=['GET'])
def get_pod_a():
    try:
        headers = request.headers
        log.info("POD-A, headers: %s", headers)
        args = dict(request.args)
        log.info("POD-A, args: %s", args)
        pod_b_route = os.environ.get("POD_B_ROUTE")
        log.info("POD-A, POD_B_ROUTE: %s", pod_b_route)
        resp = requests.get(pod_b_route)
        log.debug("POD-A, POD-B Response: %s", resp.json())
        return jsonify({"source": "POD-A", "response": resp})
    except Exception as e:
        log.error("POD-A, Error calling pod B : %s", traceback.format_exc())
        return jsonify({"source": "POD-A", "Error": str(e)})


@nl_app.route("/pod/b/", methods=['GET'])
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

