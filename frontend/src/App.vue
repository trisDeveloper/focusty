<script setup>
import { RouterLink, RouterView } from 'vue-router'
import NavMenu from "./components/nav-menu.vue"
</script>

<template>
    <NavMenu />
    <!-- eslint-disable-next-line -->
    <RouterView />
</template>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  margin: 0;
  padding: 0;
}
</style>
