from app.libs.redprint import Redprint
from flask import jsonify, request
from robosat_geoc import RSPpredict

api = Redprint('predict')


@api.route('', methods=['GET'])
def predict():
    result = {
        "code": 1,
        "data": None,
        "msg": "ok"
    }
    extent = request.args.get("extent")
    if not extent:
        result["code"] = 0
        result["msg"] = "参数有误"
        return jsonify(result)
    coords = extent.split(',')
    if len(coords) != 4:
        result["code"] = 0
        result["msg"] = "参数有误"
        return jsonify(result)
    # 获取geojson数据

    geojson = RSPpredict.main(extent)
    result["data"] = geojson
    return result
