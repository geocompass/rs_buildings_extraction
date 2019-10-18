import os
from app.libs.redprint import Redprint
api = Redprint('tools')


@api.route('/log', methods=['GET'])
def get_test():
    logPath = r"robosat_geoc/data/model/log"
    if not os.path.isfile(logPath):
        return "未找到日志文件！，路径为："+logPath
    with open(logPath) as f:
        f = f.readlines()
    logContent = ["这个是日志文件，路径为："+logPath, "", ""]
    for line in f:
        logContent.append("<p>"+line+"</p>")
    logStr = " ".join(logContent)
    return logStr
