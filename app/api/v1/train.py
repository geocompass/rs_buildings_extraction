import time
from app.libs.redprint import Redprint
from flask import jsonify, request
from robosat_pink.geoc import RSPtrain
from app.api.v1 import tools
from app.config import setting as SETTING
api = Redprint('train')


@api.route('', methods=['GET'])
def train():
    # check extent
    extent = request.args.get("extent")
    result = tools.check_extent(extent, "train")
    print(result)
    if result["code"] == 0:
        return jsonify(result)

    # 通过robosat_pink训练
    dataPath = SETTING.ROBOSAT_DATA_PATH
    datasetPath = SETTING.ROBOSAT_DATASET_PATH
    ts = time.time()
    dsTrainPath = datasetPath+"/train_"+str(ts)
    trainResult = RSPtrain.main(extent, dataPath, dsTrainPath, 1, map="tdt")
    result["data"] = trainResult
    return jsonify(result)
