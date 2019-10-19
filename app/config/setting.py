TOKEN_EXPIRATION = 30 * 24 * 3600

# building outline PostGIS data table using by training label
BUILDINGS_TABLE = "BUIA"

# tianditu and google map remote sensing wmts url
URL_TDT = '''https://t1.tianditu.gov.cn/DataServer?T=img_w&x={x}&y={y}&l={z}&tk=8971e4c7b3640d506c2dc111221af6a0'''
URL_GOOGLE = '''http://ditu.google.cn/maps/vt/lyrs=s&x={x}&y={y}&z={z}'''

# config.toml and checkpoint.pth files path
ROBOSAT_DATA_PATH = "data"

# dataset to training or predicting
ROBOSAT_DATASET_PATH = "dataset"
