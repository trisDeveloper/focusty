<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useStore } from '@/stores'
import { useRouter } from 'vue-router'
import Cookies from 'js-cookie'
const router = useRouter()
const store = useStore()
const password = ref(null)
const errormsg = ref(null)
const updateProfile = async () => {
  try {
    let formData = new FormData()
    formData.append('username', store.user.username)
    formData.append('email', store.user.email)
    if (store.user.country) {
      formData.append('country', store.user.country)
    }

    if (store.user.birthday) {
      formData.append('birthday', store.user.birthday)
    }
    if (store.user.pic && typeof store.user.pic == 'object') {
      formData.append('profile_picture', store.user.pic)
    }

    if (password.value) {
      formData.append('password', password.value)
    }

    const response = await axios.patch(`/api/users/${store.user.id}/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    if (response.status === 200) {
      store.setUser({
        id: response.data.id,
        username: response.data.username,
        email: response.data.email,
        pic: response.data.profile_picture,
        birthday: response.data.birthday,
        country: response.data.country,
        join: response.data.date_joined.split('T')[0]
      })
    } else {
      alert('Failed to update profile.')
    }
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
  }
  window.location.reload()
}
const uploadPicture = (event) => {
  const file = event.target.files[0]
  store.user.pic = file
  updateProfile()
}
const deleteAccount = () => {
  if (confirm('Are you sure you want to delete your account?')) {
    axios
      .delete(`/api/users/${store.user.id}/`)
      .then(() => {
        //window.reload()
        localStorage.clear()
        Cookies.remove('access')
        Cookies.remove('refresh')
        store.setUser(null)
        router.push('/')
        window.location.href = '/focusty/'
      })
      .catch((error) => {
        console.error('Error deleting account:', error)
        errormsg.value = 'Failed to delete your account. Please try again later.'
      })
  }
}
const logout = () => {
  if (confirm('Are you sure you want to log out?')) {
    store.setUser(null)
    localStorage.clear()
    Cookies.remove('access')
    Cookies.remove('refresh')
    router.push('/')

    window.location.href = '/'
  }
}
const deleteImage = async () => {
  try {
    const payload = {
      profile_picture: null
    }
    store.user.pic = null
    await axios.patch(`/api/users/${store.user.id}/`, payload, {
      headers: {
        'Content-Type': 'application/json'
      }
    })
  } catch (error) {
    console.log(error)
  }
}
</script>

<template>
  <div class="profile">
    <div class="intro">
      <h1>Hello {{ store.user.username }}</h1>
      <div class="image">
        <font-awesome-icon
          v-if="store.user.pic !== null"
          icon="fa-regular fa-trash-can"
          class="trash"
          @click="deleteImage()"
        />
        <img v-if="store.user.pic !== null" :src="store.user.pic" alt="profile picture" />
        <span v-else>
          {{ store.user.username[0].toUpperCase() }}
        </span>
      </div>
      <label for="upload" class="change-pic">Change Picture</label>
      <input
        id="upload"
        type="file"
        @change="uploadPicture"
        style="display: none"
        accept="image/*"
      />

      <p>Join Date: {{ store.user.join }}</p>
    </div>
    <div class="edition">
      <h1>Edit Profile</h1>
      <div class="error">
        <p v-if="errormsg">{{ errormsg }}</p>
      </div>
      <form @submit.prevent="updateProfile">
        <div>
          <label for="email">Email:</label>
          <input placeholder="Email" type="email" id="email" v-model="store.user.email" />
        </div>
        <div>
          <label for="username">username:</label>
          <input placeholder="Username" type="text" id="username" v-model="store.user.username" />
        </div>
        <div>
          <label for="password">New Password:</label>
          <input placeholder="Password" type="password" id="password" v-model="password" />
        </div>
        <div>
          <label for="birthday">Birthday:</label>
          <input
            placeholder="Birthday"
            type="birthday"
            id="birthday"
            v-model="store.user.birthday"
          />
        </div>
        <div>
          <label for="country">Country:</label>
          <input placeholder="Country" type="text" id="country" v-model="store.user.country" />
        </div>
        <button type="submit" class="change-pic">Update Profile</button>
      </form>
      <div class="logout">
        <h2>Log Out</h2>
        <p>
          If you log out, you can access your account, profile, Todos and data at any time after
          logging in again.
        </p>
        <button @click="logout">Log Out</button>
      </div>
      <div class="delete">
        <h2>Delete Account</h2>
        <p>
          When you delete your account, your profile, Todos, Data will be removed. And you will not
          be able to sign in until you create a new account. If you still want to delete the
          account, click on delete account
        </p>
        <button @click="deleteAccount">Delete Account</button>
      </div>
    </div>
  </div>
</template>

<style lang="scss">
.error {
  min-height: 50px;
  color: #e15555;
  display: flex;
  padding: 5px;
  p {
    padding: 10px;
    border: 1px solid #e15555;
  }
}
.profile {
  margin: 20px auto;
  display: flex;
  max-width: 1000px;
  justify-content: center;
  flex-wrap: wrap;
  .intro,
  .edition {
    background: #16181a82;
    padding: 10px 7px;
    min-width: 270px;
    margin: 5px;
    border-radius: 8px;
  }
  .intro {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    h1 {
      font-size: 32px;
      font-weight: bold;
      max-width: 98%;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    .image {
      height: 150px;
      position: relative;
      color: #0b0c0d;
      background: #eee;
      width: 150px;
      border-radius: 8%;
      margin: 15px;
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
      span {
        font-size: 70px;
        font-weight: bold;
      }
      img {
        max-width: 100%;
        width: 100%;
        height: 100%;
        object-fit: cover;
        border: 3px solid #eee;
        border-radius: inherit;
      }
      .trash {
        position: absolute;
        color: #fff;
        font-size: 18px;
        background: rgb(0 0 0 / 60%);
        padding: 3px;
        border-radius: 4px;
        top: 5px;
        right: 5px;
        &:hover {
          color: #ff3f3b;
        }
      }
    }
  }
}
.change-pic {
  color: #eee;
  text-decoration: none;
  text-align: center;
  background: transparent;
  width: 200px;
  padding: 7px 10px;
  border: 2px solid #eee;
  border-radius: 4px;
  margin-bottom: 15px;
  font-size: 18px;
  &:hover {
    background: rgba(231, 231, 231, 0.15);
    cursor: pointer;
  }
  &:active {
    border: 2px solid transparent;
  }
}
.edition {
  flex: 2;
  form {
    display: flex;
    flex-direction: column;
  }
  label {
    display: block;
  }
  input {
    border: none;
    background-color: #16181a82;
    color: white;
    margin: 0 0 15px 0;
    padding: 7px 5px;
    font-size: 20px;
    width: 100%;
    border-radius: 4px;
    border-bottom: 1px solid transparent;
    &:focus-visible {
      outline: none;
      border-bottom: 1px solid white;
    }
  }
}
.logout,
.delete {
  h2 {
    margin: 15px 0;
  }
  p {
    color: #ffffff8c;
    line-height: 20px;
  }
  button {
    color: #ff889c;
    text-decoration: none;
    text-align: center;
    background: #ff889c18;
    padding: 7px 10px;
    transition: all 0.3s ease-in-out;
    border-radius: 4px;
    margin: 15px 0;
    border: 2px solid transparent;
    font-size: 18px;
    &:hover {
      background: #ff5f792d;
    }
    &:active {
      border: 2px solid #ff889c;
    }
  }
}
.delete {
  button {
    color: #ff3131;
    background: #ff313115;
    &:hover {
      background: #ff313131;
    }
    &:active {
      border: 2px solid #ff3131;
    }
  }
}
</style>
