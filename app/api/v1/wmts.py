import requests
from flask import request, Response
from app.libs.redprint import Redprint

api = Redprint('wmts')


@api.route('/<z>/<x>/<y>', methods=['GET'])
def wmts(x, y, z):
    map = request.args.get("map")
    if not x or not y or not z:
        return None
    if map and (map != "tdt" or map != "google"):
        return "地图类型设置错误"
    url = '''https://t4.tianditu.gov.cn/DataServer?T=img_w&x={x}&y={y}&l={z}&tk=2ce94f67e58faa24beb7cb8a09780552'''
    url_google = '''http://ditu.google.cn/maps/vt/lyrs=s&x={x}&y={y}&z={z}'''
    if map == 'google':
        url = url_google
    image = requests.get(url.format(x=x, y=y, z=z))

    return Response(image, mimetype='image/jpeg')
