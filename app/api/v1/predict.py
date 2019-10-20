import time
from app.libs.redprint import Redprint
from flask import jsonify, request
from app.config import setting as SETTING
from robosat_pink.geoc import RSPpredict
from app.api.v1 import tools

api = Redprint('predict')


@api.route('', methods=['GET'])
def predict():
    # check extent
    extent = request.args.get("extent")
    result = tools.check_extent(extent, "predict")
    if result["code"] == 0:
        return jsonify(result)

    # 使用robosat_geoc开始预测
    dataPath = SETTING.ROBOSAT_DATA_PATH
    datasetPath = SETTING.ROBOSAT_DATASET_PATH
    ts = time.time()
    dsPredictPath = datasetPath+"/predict_"+str(ts)
    geojson = RSPpredict.main(
        extent, dataPath, dsPredictPath, map="tdt")

    if not geojson:
        result["code"] = 0
        result["msg"] = "预测失败"
        return jsonify(result)
    # 给geojson添加properties
    for feature in geojson["features"]:
        feature["properties"] = {}

    result["data"] = geojson
    return jsonify(result)
