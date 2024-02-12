<template>
  <form @submit.prevent="signup">
    <input type="text" v-model="username" required placeholder="Username" />
    <input type="email" v-model="email" required placeholder="Email" />
    <input type="password" v-model="password" required placeholder="Password" />
    <button type="submit">Sign Up</button>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useStore } from '@/stores'
const router = useRouter()
const store = useStore()

const username = ref('')
const email = ref('')
const password = ref('')
const error = ref(null)
const signup = async () => {
  try {
    const response = await axios.post('/api/users/', {
      username: username.value,
      email: email.value,
      password: password.value
    })
    // Handle successful signup
    localStorage.setItem('userId', response.data.id)
    store.setUser({
      id: response.data.id,
      username: response.data.username,
      email: response.data.email
    })
    router.push('/')
  } catch (err) {
    console.error('Sign up failed:', err)
    error.value = err.response.data.message || 'Sign up failed. Please try again.'
  }
}
</script>
