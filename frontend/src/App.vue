<template>
  <div id="app">
    <NavMenu />
    <router-view />
  </div>
</template>

<script>
import NavMenu from "./components/nav-menu.vue";
export default {
  components: {
    NavMenu,
  },
};
</script>
<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  margin: 0;
  padding: 0;
}
</style>
