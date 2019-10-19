import requests
from flask import request, Response
from app.libs.redprint import Redprint
from app.config import setting as SETTING
api = Redprint('wmts')


@api.route('/<z>/<x>/<y>', methods=['GET'])
def wmts(x, y, z):
    map = request.args.get("map")
    if not x or not y or not z:
        return None
    if map and (map != "tdt" or map != "google"):
        return "地图类型设置错误"
    url = SETTING.URL_TDT
    url_google = SETTING.URL_GOOGLE
    if map == 'google':
        url = url_google
    print(url.format(x=x, y=y, z=z))
    image = requests.get(url.format(x=x, y=y, z=z))

    return Response(image, mimetype='image/jpeg')
