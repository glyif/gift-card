"""
main gift card to cash endpoint
"""

from flask import jsonify, request, abort
from api.v1.views import app_views


@app_views.route("/gift", methods=['POST'], strict_slashes=False)
def gift_to_cash():
    """
    main gift card to cash endpoint
    :return:
    """
    required_body = ["card_number", "pin", "balance"]

    body_json = request.get_json(silent=True)
    if body_json is None:
        abort(400, 'Not a JSON')

    for req in required_body:
        if req not in body_json:
            abort(400, 'Missing ' + req)

    resp = jsonify({"OK"})
    resp.status_code = 2010

    return resp
