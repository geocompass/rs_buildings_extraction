<template>
  <div style="height:100%;width:100%;">
    <div ref="basicMapbox" :style="mapSize"></div>
    <div class="mapboxgl-ctrl-group mapboxgl-ctrl xunlianIcon">
      <button
        class="mapbox-gl-draw_ctrl-draw-btn mapbox-gl-draw_polygon"
        title="训练"
        v-on:click="trainBtn"
      >
        训练
      </button>
    </div>
    <div class="mapboxgl-ctrl-group mapboxgl-ctrl yuceIcon">
      <button
        class="mapbox-gl-draw_ctrl-draw-btn mapbox-gl-draw_polygon"
        title="预测"
        v-on:click="predictBtn"
      >
        预测
      </button>
    </div>
    <div class="mapboxgl-ctrl-group mapboxgl-ctrl qingkongIcon">
      <button
        class="mapbox-gl-draw_ctrl-draw-btn mapbox-gl-draw_trash"
        title="清空"
        v-on:click="clearBtn"
      >
        清空
      </button>
    </div>
    <div class="msg">{{ msg }}</div>
  </div>
</template>

<script>
import mapboxgl from "mapbox-gl";
import MapboxLanguage from "@mapbox/mapbox-gl-language";
import "mapbox-gl/dist/mapbox-gl.css";
import DrawRectangle from "mapbox-gl-draw-rectangle-mode";
import "@mapbox/mapbox-gl-draw/dist/mapbox-gl-draw.css";
import MapboxDraw from "@mapbox/mapbox-gl-draw";
import axios from "axios";

export default {
  name: "HelloWorld",
  props: {
    mapWidth: {
      type: String
    },
    mapHeight: {
      type: String
    }
  },
  data() {
    return {
      draw: null,
      map: null,
      feature: null,
      msg: "请选择左侧相应的工具执行训练或预测！"
    };
  },
  computed: {
    mapSize() {
      let styleObj = {
        width: this.mapWidth,
        height: this.mapHeight
      };
      return styleObj;
    }
  },
  watch: {
    feature: function(newFeature, oldFeature) {
      if (newFeature === "train") {
        this.msg = "正在绘制待训练的区域";
        return;
      } else if (newFeature === "predict") {
        this.msg = "正在绘制待预测的区域";
        return;
      } else if (
        !newFeature ||
        !newFeature.features ||
        newFeature.features.length === 0
      ) {
        this.msg = "图形未绘制成功！";
        return;
      }
      let rectangle = newFeature.features[0];
      if (oldFeature === "train") {
        this.train(rectangle);
      } else if (oldFeature === "predict") {
        this.predict(rectangle);
      }
    }
  },
  methods: {
    //初始化地图
    initMap() {
      mapboxgl.accessToken =
        "pk.eyJ1Ijoid3VjYW5nZW8iLCJhIjoiY2oxNGQ1ZDdsMDA0djJxbzdzdGU4NWpqMiJ9.iaTLldYv7GNfxWhN42h__g";
      // 英文标注转换为中文
      mapboxgl.setRTLTextPlugin(
        "https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-rtl-text/v0.1.0/mapbox-gl-rtl-text.js"
      );
      const map = new mapboxgl.Map({
        container: this.$refs.basicMapbox,
        style: "mapbox://styles/mapbox/streets-v9",
        center: [116.295, 39.945],
        zoom: 16
      });
      // 设置语言
      var language = new MapboxLanguage({ defaultLanguage: "zh" });
      map.addControl(language);

      // 地图导航
      var nav = new mapboxgl.NavigationControl();
      map.addControl(nav, "top-left");
      // 比例尺
      var scale = new mapboxgl.ScaleControl({
        maxWidth: 80,
        unit: "imperial"
      });
      map.addControl(scale);
      scale.setUnit("metric");
      // 全图
      map.addControl(new mapboxgl.FullscreenControl());
      // 定位
      map.addControl(
        new mapboxgl.GeolocateControl({
          positionOptions: {
            enableHighAccuracy: true
          },
          trackUserLocation: true
        })
      );
      //添加绘制功能
      var modes = MapboxDraw.modes;
      modes.draw_rectangle = DrawRectangle;

      var draw = new MapboxDraw({
        modes: modes
      });
      map.addControl(draw);

      map.on("draw.create", feature => {
        this.feature = feature;
      });
      //设置为全局变量
      this.draw = draw;
      this.map = map;
    },
    //训练按钮
    trainBtn() {
      this.clearBtn();
      this.feature = "train";
      this.draw.changeMode("draw_rectangle");
    },
    //预测按钮
    predictBtn() {
      this.clearBtn();
      this.feature = "predict";
      this.draw.changeMode("draw_rectangle");
    },
    //清空按钮
    clearBtn() {
      this.draw.deleteAll();
    },
    //开始训练
    async train(feature) {
      let extent = this.getExtentStr(feature);
      this.msg = extent;
      await axios({
        method: "get",
        url: CONFIG.HOST + "/v1/train",
        params: {
          extent: extent,
          map: "tdt"
        }
      });
      this.msg = "正在训练中，请再系统后台查看进度...";
    },
    //开始预测
    async predict(feature) {
      let extent = this.getExtentStr(feature);
      this.msg = extent;
      this.msg = "正在预测中，请稍后...";
      let response = await axios({
        method: "get",
        url: CONFIG.HOST + "/v1/predict",
        // url: "http://localhost:8080/test.json",
        params: {
          extent: extent,
          map: "tdt"
        }
      });
      if (response.status != 200 || !response.data) {
        this.msg = "预测失败！，status code:" + response.status;
        return;
      }
      let result = response.data;
      if (result.code === 0) {
        this.msg = result.msg;
        return;
      }
      this.draw.add(result.data);
    },
    //将矩形的geojson提取extent为string类型
    getExtentStr(geojson) {
      if (
        !geojson ||
        !geojson.geometry ||
        !geojson.geometry.coordinates ||
        geojson.geometry.coordinates.length != 1 ||
        geojson.geometry.coordinates[0].length != 5
      ) {
        this.msg = "绘制的图形不是四边形！";
        return;
      }
      let coordinates = geojson.geometry.coordinates[0];
      let startPoint = coordinates[0];
      let endPoint = coordinates[3];
      let extentStr = startPoint.concat(endPoint).join(",");
      return extentStr;
    }
  },
  mounted() {
    this.initMap();
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
/* @import url("https://api.tiles.mapbox.com/mapbox-gl-js/v1.4.1/mapbox-gl.css"); */
.mapboxgl-map {
  height: 100%;
  width: 100%;
}
.xunlianIcon {
  position: absolute;
  top: 20px;
  left: 400px;
}
.xunlianIcon button {
  background-position: left;
  width: 50px;
  text-align: right;
  padding: 4px;
}
.yuceIcon {
  position: absolute;
  top: 20px;
  left: 480px;
}
.yuceIcon button {
  background-position: left;
  width: 50px;
  text-align: right;
  padding: 4px;
}

.qingkongIcon {
  position: absolute;
  top: 20px;
  left: 560px;
}
.qingkongIcon button {
  background-position: left;
  width: 50px;
  text-align: right;
  padding: 4px;
}
.msg {
  position: absolute;
  top: 23px;
  left: 650px;
  max-width: 500px;
  text-align: left;
}
</style>
