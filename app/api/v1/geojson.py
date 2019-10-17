from flask import request, Response, jsonify
from app.models.base import queryBySQL
from app.libs.redprint import Redprint

api = Redprint('geojson')


@api.route('', methods=['GET'])
def wmts():
    extent = request.args.get("extent")
    if not extent:
        return None

    sql = '''SELECT
        jsonb_build_object ( 'type', 'FeatureCollection', 'features', jsonb_agg ( features.feature ) ) 
            FROM
                (
                SELECT
                    jsonb_build_object ( 'type', 'Feature', 'id', gid, 'geometry', ST_AsGeoJSON ( geom ) :: jsonb, 'properties', to_jsonb ( inputs ) - 'geom' ) AS feature 
                FROM
                    (
                    SELECT gid,geom AS geom 
                    FROM "buildings" WHERE
                        geom @
                    ST_MakeEnvelope ( {extent}, {srid} )) inputs 
                ) features; '''
    queryData = queryBySQL(sql.format(extent=extent, srid=4326))
    row = queryData.fetchone()
    print(row)
    return jsonify(row["jsonb_build_object"])
