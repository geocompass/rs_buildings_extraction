from sqlalchemy import or_, text
from app.libs.redprint import Redprint
from app.models.buia import BUIA
from app.models.base import queryBySQL
from flask import jsonify, request
import json

api = Redprint('buia')


@api.route("", methods=['GET'])
def onegeojson():
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
    # coords = extent.split(',')
    sql = '''SELECT
        jsonb_build_object ( 'type', 'FeatureCollection', 'features', jsonb_agg ( features.feature ) ) 
            FROM
                (
                SELECT
                    jsonb_build_object ( 'type', 'Feature', 'id', gid, 'geometry', ST_AsGeoJSON ( geom ) :: jsonb, 'properties', to_jsonb ( inputs ) - 'geom' ) AS feature 
                FROM
                    (
                    SELECT gid,"CNAME",geom AS geom 
                    FROM "BUIA" WHERE
                        geom @
                    ST_MakeEnvelope ( {extent}, {srid} )) inputs 
                ) features; '''
    queryData = queryBySQL(sql.format(extent=extent, srid=4326))
    if not queryData:
        result["code"] = 0
        result["msg"] = "查询语句有问题"
        return jsonify(result)
    row = queryData.fetchone()
    result["data"] = row

    return jsonify(result)


@api.route("/<gid>", methods=['GET'])
def get(gid):
    result = {
        "code": 1,
        "data": None,
        "msg": "ok"
    }
    sql = '''select st_asgeojson(geom) as geojson from "BUIA" where gid ={gid}'''
    queryData = queryBySQL(sql.format(gid=gid))
    if not queryData:
        result["code"] = 0
        result["msg"] = "查询语句有问题"
        return jsonify(result)
    if queryData.rowcount == 0:
        result["code"] = 0
        result["msg"] = "未查询到内容"
        return jsonify(result)
    row = queryData.fetchone()
    result["data"] = json.loads(row["geojson"])
    return jsonify(result)
