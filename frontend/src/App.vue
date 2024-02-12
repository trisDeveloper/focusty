<script setup>
import { onMounted } from 'vue'
import { useStore } from '@/stores'
import { RouterView } from 'vue-router'
import NavMenu from './components/nav-menu.vue'
import axios from 'axios'
const store = useStore()
onMounted(async () => {
  await fetchUser()
})

const fetchUser = async () => {
  try {
    const response = await axios.get(`/api/users/${localStorage.getItem('userId')}`)
    const userData = response.data
    store.setUser({
      id: userData.id,
      username: userData.username,
      email: userData.email
    })
  } catch (error) {
    console.error('Error fetching user data:', error)
  }
}
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
