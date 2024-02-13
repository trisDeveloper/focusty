<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
const router = useRouter()

const email = ref('')
const password = ref('')
const errormsg = ref(null)
const login = async () => {
  try {
    const response = await axios.post('/api/login/', {
      email: email.value,
      password: password.value
    })
    // Handle successful login
    localStorage.setItem('userId', response.data.id)
    router.push('/')
    window.reload()
  } catch (error) {
    let data = error.response.data.message
    errormsg.value = data
  }
}
</script>
<template>
  <div>
    <div class="error">
      <p v-if="errormsg">{{ errormsg }}</p>
    </div>
    <form @submit.prevent="login">
      <h1>Welcome back!</h1>
      <input type="email" v-model="email" required placeholder="Email" />
      <input type="password" v-model="password" required placeholder="Password" />
      <button class="login-btn" type="submit">Log In</button>
      <div class="login">
        Don't have an account! <router-link to="/signup">Sign Up.</router-link>
      </div>
    </form>
  </div>
</template>
<style lang="scss">
.login {
  color: #bbb;
  padding: 10px 0;
  a {
    color: rgba(245, 222, 179, 0.8);
    text-decoration: none;
    font-weight: bold;
    &:hover {
      color: #ffcb6a;
    }
  }
}
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
  .login-btn {
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
