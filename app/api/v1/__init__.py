
from flask import Blueprint
from app.api.v1 import test, predict_buildings, buia


def create_blueprint_v1():
    bp_v1 = Blueprint('v1', __name__)

    test.api.register(bp_v1)
    predict_buildings.api.register(bp_v1)
    buia.api.register(bp_v1)

    return bp_v1
