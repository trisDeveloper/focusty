<template>
  <div>
    <div class="error">
      <p v-if="error">{{ error }}</p>
    </div>
    <form @submit.prevent="signup">
      <h1>Start Productivity Today!</h1>
      <p>Sign up and try focusty for free</p>
      <input type="text" v-model="username" autofocus required placeholder="Username" />
      <input type="email" v-model="email" required placeholder="Email" />
      <input type="password" v-model="password" required placeholder="Password" />
      <button class="signup-btn" type="submit">Sign Up</button>
    </form>
  </div>
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
const error = ref('')
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
  } catch (error) {
    let data = error.response.data
    if (data) {
      for (const key in data) {
        if (Array.isArray(data[key]) && data[key].length > 0) {
          error.value = data[key][0]
          break
        }
      }
    }
    console.log(error.value)
  }
}
</script>

<style lang="scss">
.error {
  min-height: 40px;
}
form {
  width: 100%;
  min-height: calc(100vh - 65px);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 5px;
  * {
    transition: all 0.3s ease-in;
  }
  h1 {
    font-weight: bold;
    padding: 0 0 15px;
  }
  p {
    color: #647381;
    padding: 0 0 25px;
    letter-spacing: 3px;
  }
  input {
    border: none;
    background-color: #101027;
    color: white;
    margin: 10px 0;
    padding: 7px 5px;
    font-size: 20px;
    border-bottom: 1px solid transparent;
    &:focus-visible {
      outline: none;
      border-bottom: 1px solid white;
    }
    &:hover {
      border-bottom: 1px solid white;
    }
  }
  .signup-btn {
    color: wheat;
    font-size: 20px;
    background: transparent;
    text-decoration: none;
    padding: 7px 10px;
    border: 1px solid wheat;
    margin: 15px 0;
    &:hover {
      background: rgba(245, 222, 179, 0.15);
    }
    &:active {
      border: none;
    }
  }
}
</style>
