<script setup>
import { ref } from 'vue'
import Cookies from 'js-cookie'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useStore } from '@/stores'
const router = useRouter()
const store = useStore()

const username = ref('')
const email = ref('')
const password = ref('')
const errormsg = ref(null)
const signup = async () => {
  try {
    const response = await axios.post('/api/register/', {
      username: username.value,
      email: email.value,
      password: password.value
    })
    // Handle successful signup
    localStorage.setItem('userId', response.data.id)
    const [access, refresh] = [response.data.access, response.data.refresh]
    if (access && refresh) {
      Cookies.set('access', access, { expires: 60 / 1440, secure: true, sameSite: 'Strict' })
      Cookies.set('refresh', refresh, { expires: 60, secure: true, sameSite: 'Strict' })
    }
    store.setUser({
      id: response.data.id,
      username: response.data.username,
      email: response.data.email,
      pic: response.data.profile_picture,
      country: response.data.country,
      join: response.data.date_joined.split('T')[0]
    })
    router.push('/')

    window.location.href = '/focusty/'
  } catch (error) {
    let data = error.response.data
    console.log(data)
    if (data) {
      for (const key in data) {
        if (Array.isArray(data[key]) && data[key].length > 0) {
          errormsg.value = `${key} :${data[key][0]}`
          break
        }
      }
    }
    console.log(errormsg.value)
  }
}
</script>
<template>
  <div style="text-align: center">
    <div class="error">
      <p v-if="errormsg">{{ errormsg }}</p>
    </div>
    <form @submit.prevent="signup">
      <h1>Start Productivity Today!</h1>
      <p>Sign up and try focusty for free</p>
      <input type="text" v-model="username" autofocus required placeholder="Username" />
      <input type="email" v-model="email" required placeholder="Email" />
      <input type="password" v-model="password" required placeholder="Password" />
      <button class="signup-btn" type="submit">Sign Up</button>
      <div class="login">
        Already have an account! <router-link to="/login">Log In.</router-link>
      </div>
    </form>
  </div>
</template>
<style lang="scss">
.error {
  min-height: 70px;
  color: #e15555;
  display: flex;
  justify-content: center;
  padding: 15px;
  p {
    padding: 10px;
    border: 1px solid #e15555;
  }
}
.login {
  color: #bbb;
  padding: 10px 0;
  a {
    color: rgba(255, 255, 255, 0.8);
    text-decoration: none;
    font-weight: bold;
    &:hover {
      color: #eee;
    }
  }
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
    background-color: #16181a82;
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
    color: #ffffffef;
    font-size: 20px;
    background: transparent;
    text-decoration: none;
    padding: 7px 10px;
    border: 1px solid #ffffffef;
    margin: 15px 0;
    &:hover {
      background: rgba(253, 253, 253, 0.15);
    }
    &:active {
      border: none;
    }
  }
}
</style>
