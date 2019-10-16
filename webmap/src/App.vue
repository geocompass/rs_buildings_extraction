<template>
  <div id="app">
    <HomeMap class="homeMap" />
  </div>
</template>

<script>
import HomeMap from "./components/HomeMap.vue";

export default {
  name: "app",
  components: {
    HomeMap
  }
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  position: absolute;
  top: 0;
  bottom: 0;
  width: 100%;
}
.homeMap {
  width: 100%;
  height: 100%;
}
body {
  margin: 0;
  padding: 0;
}
</style>
