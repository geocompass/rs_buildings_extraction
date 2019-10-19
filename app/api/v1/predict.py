import time
from app.libs.redprint import Redprint
from flask import jsonify, request
from app.config import setting as SETTING
from robosat_pink.geoc import RSPpredict

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

    # 使用robosat_geoc开始预测
    dataPath = SETTING.ROBOSAT_DATA_PATH
    datasetPath = SETTING.ROBOSAT_DATASET_PATH
    ts = time.time()
    dsPredictPath = datasetPath+"/predict_"+str(ts)
    geojson = RSPpredict.main(extent, dataPath, dsPredictPath, map="tdt")

    if not geojson:
        result["code"] = 0
        result["msg"] = "预测失败"
        return jsonify(result)
    # 给geojson添加properties
    for feature in geojson["features"]:
        feature["properties"] = {}

    result["data"] = geojson
    return result
