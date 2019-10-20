import time
from app.libs.redprint import Redprint
from flask import jsonify, request
from robosat_pink.geoc import RSPtrain
from app.config import setting as SETTING
api = Redprint('train')


@api.route('', methods=['GET'])
def train():
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

    # 通过robosat_pink训练
    dataPath = SETTING.ROBOSAT_DATA_PATH
    datasetPath = SETTING.ROBOSAT_DATASET_PATH
    pthPath = dataPath + "/model/checkpoint-00010.pth"
    ts = time.time()
    dsTrainPath = datasetPath+"/train_"+str(ts)
    RSPtrain.main(extent, dataPath, dsTrainPath, pthPath, map="tdt")
    return extent
