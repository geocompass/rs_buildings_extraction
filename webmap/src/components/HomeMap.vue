<template>
  <div style="height:100%;width:100%;">
    <div ref="basicMapbox" :style="mapSize"></div>
    <div class="mapboxgl-ctrl-group mapboxgl-ctrl tdtIcon">
      <button
        class="mapbox-gl-draw_ctrl-draw-btn mapbox-gl-draw_uncombine"
        title="点击切换底图"
        v-on:click="changeRSMap"
      >
        {{ rsMap }}
      </button>
    </div>
    <div class="buildIcon">
      <input type="checkbox" id="checkbox" v-model="isShowBUIA" />
      <label>天地图建筑物</label>
    </div>
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
    <div class="mapboxgl-ctrl-group mapboxgl-ctrl logIcon">
      <!-- <a target="_blank" src> -->
      <button
        class="mapbox-gl-draw_ctrl-draw-btn mapbox-gl-draw_uncombine"
        title="日志"
        v-on:click="checkLogBtn"
      >
        日志
      </button>
    </div>
    <div class="mapboxgl-ctrl-group mapboxgl-ctrl logClearIcon">
      <button
        class="mapbox-gl-draw_ctrl-draw-btn mapbox-gl-draw_trash"
        title="清空"
        v-on:click="clearLogBtn"
      >
        清空
      </button>
      <!-- </a> -->
    </div>
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
      msg: "请选择左侧相应的工具执行训练或预测！",
      isShowBUIA: true,
      rsMap: "天地图"
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
    },
    isShowBUIA: function(newValue) {
      if (newValue) {
        this.addBUIA();
      } else {
        let geojsonData = {
          type: "FeatureCollection",
          features: []
        };
        let source = this.map.getSource("tempbuild");
        if (source) {
          source.setData(geojsonData);
        }
      }
    }
  },
  methods: {
    //初始化地图
    initMap() {
      mapboxgl.accessToken =
        "pk.eyJ1Ijoid3VjYW5nZW8iLCJhIjoiY2oxNGQ1ZDdsMDA0djJxbzdzdGU4NWpqMiJ9.iaTLldYv7GNfxWhN42h__g";
      const map = new mapboxgl.Map({
        container: this.$refs.basicMapbox,
        style: CONFIG.HOST + "/style.json",
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
      //地图事件
      var that = this;
      this.map.on("moveend", async function() {
        that.addBUIA();
      });
      this.addBUIA();
    },
    async addBUIA() {
      let bounds = this.map.getBounds();
      let extentArr = [
        bounds._sw.lng,
        bounds._sw.lat,
        bounds._ne.lng,
        bounds._ne.lat
      ];
      let extent = extentArr.join(",");
      let result = await axios({
        method: "get",
        url: CONFIG.SERVER + "/v1/geojson",
        params: {
          extent: extent
        }
      });
      let geojsonData = result.data;
      if (!result.data || !this.isShowBUIA) {
        geojsonData = {
          type: "FeatureCollection",
          features: []
        };
      }
      let source = this.map.getSource("tempbuild");
      if (source) {
        source.setData(geojsonData);
      } else {
        //添加geojson图层
        this.map.addSource("tempbuild", {
          /* addSource()函数添加资源,资源ID是route */
          type: "geojson",
          data: geojsonData
        });
        this.map.addLayer(CONFIG.BUILDING_STYLE);
      }
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
    //切换遥感影像底图
    changeRSMap() {
      if (this.rsMap === "天地图") {
        let style = this.map.getStyle();
        style.sources["raster-tiles"] = CONFIG.GOOGLE_TILE;
        this.map.setStyle(style);
        this.rsMap = "谷歌";
      } else if (this.rsMap === "谷歌") {
        let style = this.map.getStyle();
        style.sources["raster-tiles"] = CONFIG.TDT_TILE;
        this.map.setStyle(style);
        this.rsMap = "天地图";
      }
    },
    //打开日志文件
    async checkLogBtn() {
      let url = CONFIG.SERVER + "/v1/tools/log";
      window.open(url, "_blank");
    },
    async clearLogBtn() {
      let url = CONFIG.SERVER + "/v1/tools/log/clear";
      let response = await axios.get(url).catch(() => {
        this.msg = "clear log faild!";
      });
      if (response && response.data) {
        this.msg = "clear log success";
      }
    },
    //开始训练
    async train(feature) {
      let extent = this.getExtentStr(feature);
      this.msg = extent;
      let spendSeconds = 0;
      let trainInterval = setInterval(() => {
        spendSeconds += 0.1;
        this.msg = `training...,it spends ${spendSeconds.toFixed(2)} seconds`;
      }, 100);
      let response = await axios
        .get(CONFIG.SERVER + "/v1/train", {
          params: {
            extent: extent,
            map: "tdt"
          }
        })
        .catch(error => {
          clearInterval(trainInterval);
          this.msg =
            "training faild, please check log in backend！" +
            JSON.stringify(error);
        });
      if (trainInterval) {
        clearInterval(trainInterval);
      }
      if (response && response.data) {
        let result = response.data;
        if (result.code === 1) {
          this.msg = `training finished，it spends ${spendSeconds.toFixed(
            2
          )} seconds！`;
        } else {
          this.msg = result.msg;
        }
      }
    },
    //开始预测
    async predict(feature) {
      let extent = this.getExtentStr(feature);
      this.msg = extent;
      let spendSeconds = 0;
      let predictInterval = setInterval(() => {
        spendSeconds += 0.1;
        this.msg = `predicting，it spends${spendSeconds.toFixed(2)} seconds！`;
      }, 100);
      let response = await axios
        .get(CONFIG.SERVER + "/v1/predict", {
          params: {
            extent: extent,
            map: "tdt"
          }
        })
        .catch(error => {
          clearInterval(predictInterval);
          this.msg =
            "predicting faild, please check log in backend！" +
            JSON.stringify(error);
        });
      if (predictInterval) {
        clearInterval(predictInterval);
      }
      if (response && response.data) {
        let result = response.data;
        if (result.code === 0) {
          this.msg = result.msg;
          return;
        } else {
          this.msg = `predicting finished，it spends${spendSeconds.toFixed(
            2
          )} seconds！`;
          this.draw.add(result.data);
        }
      }
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
      let minx = 180,
        miny = 180;
      let maxx = -180,
        maxy = -180;
      coordinates.forEach(coord => {
        if (coord[0] > maxx) {
          maxx = coord[0];
        }
        if (coord[0] < minx) {
          minx = coord[0];
        }
        if (coord[1] > maxy) {
          maxy = coord[1];
        }
        if (coord[1] < miny) {
          miny = coord[1];
        }
      });
      let extentStr = [minx, miny, maxx, maxy].join(",");
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
  background-color: rgba(255, 255, 255, 0.7);
  padding: 3px;
}
.buildIcon {
  position: absolute;
  top: 23px;
  left: 250px;
}
.buildIcon label {
  background-color: rgba(255, 255, 255, 0.7);
  padding: 3px;
}
.tdtIcon {
  position: absolute;
  top: 20px;
  left: 150px;
}
.tdtIcon button {
  background-position: left;
  width: 60px;
  text-align: right;
  padding: 4px;
}

.logIcon {
  position: absolute;
  top: 20px;
  right: 130px;
}
.logIcon button {
  background-position: left;
  width: 50px;
  text-align: right;
  padding: 4px;
}
.logClearIcon {
  position: absolute;
  top: 20px;
  right: 75px;
}
.logClearIcon button {
  background-position: left;
  width: 50px;
  text-align: right;
  padding: 4px;
}
</style>
