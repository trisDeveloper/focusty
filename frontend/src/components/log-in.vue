<template>
  <form @submit.prevent="login">
    <input type="text" v-model="username" required placeholder="Username" />
    <input type="password" v-model="password" required placeholder="Password" />
    <button type="submit">Login</button>
  </form>
</template>

<script>
import { ref } from 'vue'
import api from '../services/api'

export default {
  setup() {
    const username = ref('')
    const password = ref('')

    const login = async () => {
      try {
        const response = await api.post('login/', {
          username: username.value,
          password: password.value
        })
        // Handle successful login
      } catch (error) {
        console.error('Login failed:', error)
        // Handle login failure
      }
    }

    return { username, password, login }
  }
}
</script>
