<script setup>
import { useStore } from '@/stores'
import axios from 'axios'
import { onMounted } from 'vue'
import { RouterView } from 'vue-router'
import NavMenu from './components/nav-menu.vue'

const store = useStore()

onMounted(async () => {
  if (localStorage.getItem('userId')) {
    await fetchUser()
  }
})
const fetchUser = async () => {
  try {
    const response = await axios.get(`/api/users/${localStorage.getItem('userId')}`)
    const userData = response.data
    store.setUser({
      id: userData.id,
      username: userData.username,
      email: userData.email,
      pic: userData.profile_picture,
      country: userData.country,
      birthday: userData.birthday,
      join: userData.join_date
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
