"""
main gift card to cash endpoint
"""

from flask import jsonify, request, abort
from api.v1.views import app_views

from integrations.assembly.assembly_integration import AssemblyItem
from integrations.marqeta.marqeta_integration import Marqeta
from integrations.capitol_one.verify import Verify

@app_views.route("/verify/button", methods=['GET'], strict_slashes=False)
def get_button():
    v = Verify()

    return v.get_button()

@app_views.route("/verify/", methods=['GET'], strict_slashes=False)
def verify_identity():
    v = Verify()
    v.get_second_access()

    status = v.verify()

    if status != 204:
        abort(400, "Something went wrong")

    resp = jsonify({"status": status})
    resp.status_code = 204

    return resp


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

    # create escrow for gift card hold, makes transactions and attempts to pay
    escrow = AssemblyItem()

    if escrow.state != "payment_deposited":
        abort(401, "Payment Error: " + escrow.state)

    money = Marqeta(escrow.item_id)

    resp = jsonify({"payment": "OK"})
    resp.status_code = 200

    return resp
