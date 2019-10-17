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
  }
};
