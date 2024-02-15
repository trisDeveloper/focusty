<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useStore } from '@/stores'
const store = useStore()
const password = ref(null)
const errormsg = ref(null)
const updateProfile = async () => {
  try {
    let formData = new FormData()
    formData.append('username', store.user.username)
    formData.append('email', store.user.email)
    formData.append('country', store.user.country)
    formData.append('birthday', store.user.birthday)
    if (typeof store.user.pic == 'object') {
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
        join: response.data.join_date
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
}
const uploadPicture = (event) => {
  const file = event.target.files[0]
  store.user.pic = file
  updateProfile()
}
</script>

<template>
  <div class="profile">
    <div class="intro">
      <h1>Hello {{ store.user.username }}</h1>
      <div class="image">
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
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="store.user.email" />

        <label for="username">username:</label>
        <input type="text" id="username" v-model="store.user.username" />

        <label for="password">New Password:</label>
        <input type="password" id="password" v-model="password" />

        <label for="birthday">Birthday:</label>
        <input type="birthday" id="birthday" v-model="store.user.birthday" />

        <label for="country">Country:</label>
        <input type="text" id="country" v-model="store.user.country" />
        <button type="submit">Update Profile</button>
      </form>
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
    background: #10102b;
    padding: 10px 7px;
    min-width: 270px;
    margin: 5px;
    border-radius: 15px;
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
      color: #06061c;
      background: #fff897;
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
        border: 3px solid #fff897;
        border-radius: inherit;
      }
    }
    .change-pic {
      color: #fff897;
      text-decoration: none;
      padding: 7px 10px;
      border: 2px solid #fff897;
      border-radius: 7px;
      margin-bottom: 15px;
      &:hover {
        background: rgba(245, 222, 179, 0.15);
      }
      &:active {
        border: 2px solid transparent;
      }
    }
  }
}
.edition {
  flex: 2;
  form {
    display: flex;
    flex-direction: column;
    input {
      border: none;
      background-color: #101027;
      color: white;
      margin: 10px 0;
      padding: 7px 5px;
      font-size: 20px;
      border-bottom: 1px solid transparent;
    }
  }
}
</style>
