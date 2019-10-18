const CONFIG = {
  SERVER: "http://127.0.0.1:5000",
  HOST: "http://127.0.0.1:5000",

  // SERVER: "http://127.0.0.1:5000",
  // HOST: "http://127.0.0.1:8080",
  BUILDING_STYLE: {
    /* 为地图添加layer */
    id: "tempbuild" /* layer id是route */,
    type: "fill" /* line类型layer*/,
    source: "tempbuild" /* 资源引用的是上面定义的source*/,
    paint: {
      "fill-color": "rgba(194,186,62,0.4)",
      "fill-outline-color": "rgba(255,0,0,0.5)"
    }
  },
  TDT_TILE: {
    "type": "raster",
    "tiles": [
      "http://t0.tianditu.gov.cn/DataServer?T=img_w&x={x}&y={y}&l={z}&tk=fb1bfb9e06cd7681813a42f4c934e1ea"
    ],
    "tileSize": 256
  },
  GOOGLE_TILE: {
    "type": "raster",
    "tiles": [
      "http://ditu.google.cn/maps/vt/lyrs=s&x={x}&y={y}&z={z}"
    ],
    "tileSize": 256
  },
};
