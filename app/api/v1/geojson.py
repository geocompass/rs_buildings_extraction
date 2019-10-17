from flask import request, Response, jsonify
from app.models.base import queryBySQL
from app.libs.redprint import Redprint
from app.config import setting
api = Redprint('geojson')


@api.route('', methods=['GET'])
def geojson():
    extent = request.args.get("extent")
    if not extent:
        return jsonify("")
    extentArr = extent.split(',')
    if len(extentArr) != 4:
        return jsonify("")
    if float(extentArr[2]) - float(extentArr[0]) > 0.05 or float(extentArr[3]) - float(extentArr[1]) > 0.04:
        return jsonify("")

    sql = '''SELECT
        jsonb_build_object ( 'type', 'FeatureCollection', 'features', jsonb_agg ( features.feature ) ) 
            FROM
                (
                SELECT
                    jsonb_build_object ( 'type', 'Feature', 'id', gid, 'geometry', ST_AsGeoJSON ( geom ) :: jsonb, 'properties', to_jsonb ( inputs ) - 'geom' ) AS feature 
                FROM
                    (
                    SELECT gid,geom AS geom 
                    FROM "{buildings_table}" WHERE
                        geom @
                    ST_MakeEnvelope ( {extent}, {srid} )) inputs 
                ) features; '''
    queryData = queryBySQL(sql.format(
        buildings_table=setting.BUILDINGS_TABLE, extent=extent, srid=4326))
    row = queryData.fetchone()
    return jsonify(row["jsonb_build_object"])
