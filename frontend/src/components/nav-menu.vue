<template>
  <nav class="navbar">
    <div class="nav">
      <button class="menu-button" @click="toggleSidebar($event)">
        <font-awesome-icon icon="bars" />
      </button>
      <div class="date">{{ today }}</div>
      <weekNavigation />
    </div>
    <div v-if="store.user.id !== null" class="profile-icon">
      <router-link to="/profile/">
        <img v-if="store.user.pic !== null" :src="store.user.pic" alt="profile picture" />
        <span v-else>
          {{ store.user.username[0].toUpperCase() }}
        </span>
      </router-link>
    </div>
    <router-link v-else to="/signup" class="signup-btn">Sign Up</router-link>
    <div class="sidebar" :class="{ active: isSidebarActive }" id="sidebar">
      <ul class="sidebar-menu">
        <li>
          <router-link
            class="menu-items"
            @click="toggleSidebar"
            style="display: inline-block; width: 100%"
            to="/"
            ><font-awesome-icon icon="home" />Home</router-link
          >
        </li>
        <li>
          <router-link
            class="menu-items"
            @click="toggleSidebar"
            style="display: inline-block; width: 100%"
            to="/calendar"
            ><font-awesome-icon icon="fa-regular fa-calendar-check" />Calendar</router-link
          >
        </li>
        <li>
          <router-link
            class="menu-items"
            @click="toggleSidebar"
            style="display: inline-block; width: 100%"
            to="/pomodoro"
            ><font-awesome-icon icon="hourglass" />Pomodoro</router-link
          >
        </li>
        <li>
          <router-link
            class="menu-items"
            @click="toggleSidebar"
            style="display: inline-block; width: 100%"
            to="/journey"
            ><font-awesome-icon icon="fa-solid fa-chart-line" />Journey</router-link
          >
        </li>
      </ul>
    </div>
  </nav>
</template>
<script setup>
import weekNavigation from './week-navigation.vue'
import { ref, onMounted, onUnmounted } from 'vue'
import { useStore } from '@/stores'
const store = useStore()

const isSidebarActive = ref(false)
const today = new Date().toLocaleDateString('en-US', {
  weekday: 'short',
  day: 'numeric',
  month: 'long'
})

const toggleSidebar = (event) => {
  event.stopPropagation()
  store.setIsOpenCard(false)
  isSidebarActive.value = !isSidebarActive.value
  if (isSidebarActive.value) {
    window.addEventListener('click', closeSidebar)
  } else {
    window.removeEventListener('click', closeSidebar)
  }
}

const closeSidebar = (event) => {
  if (!document.getElementById('sidebar').contains(event.target)) {
    isSidebarActive.value = false
    window.removeEventListener('click', closeSidebar)
  }
}

onMounted(() => {
  window.addEventListener('click', closeSidebar)
})

onUnmounted(() => {
  window.removeEventListener('click', closeSidebar)
})
</script>

<style lang="scss" scoped>
@use '@/styles.scss' as *;
.navbar {
  display: flex;
  justify-content: space-between;
  height: 60px;
  padding: 5px;
  align-items: center;
  border-bottom: 2px solid #ffffff08;
}
.nav {
  display: flex;
  align-items: center;
  .menu-button {
    border: none;
    background: none;
    color: #ddd;
    font-size: 23px;
    padding: 10px;
    cursor: pointer;
  }
  .date {
    padding: 0 5px;
    font-size: 21px;
    color: #ddd;
  }
}

.profile-icon {
  border-radius: 50%;
  margin-right: 10px;
  height: 40px;
  width: 40px;
  background: #9eff86;
  overflow: hidden;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  a {
    text-decoration: none;
    position: relative;
    color: #0b0c0d;
    width: 100%;
    height: 100%;
    font-weight: bold;
    font-size: 26px;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center;
  }
}

.sidebar {
  position: fixed;
  top: 60px;
  left: 0;
  width: 250px;
  height: calc(100vh - 60px);
  border-right: 2px solid #ffffff08;
  background-color: $dark-back;
  z-index: 999;
  transition: transform 0.3s cubic-bezier(0.46, 0.03, 0.52, 0.96);
  transform: translateX(-100%);
  &.active {
    transform: translateX(0);
  }
  @media (max-width: 425px) {
    width: 100%;
  }
  .sidebar-menu {
    height: 100%;
    display: flex;
    flex-direction: column;
    .menu-items {
      list-style: none;
      padding: 15px;
      border-left: 2px solid transparent;
      transition: 0.3s all ease-out;
      text-decoration: none;
      color: #ddd;
      svg {
        padding-right: 10px;
      }
      &:hover {
        background-color: #25252580;
        border-left: 2px solid white;
        svg {
          color: #dadada;
        }
      }
    }
  }
}
.signup-btn {
  color: #fcfcfc;
  text-decoration: none;
  padding: 7px 10px;
  border: 1px solid #e2e2e2;
  border-radius: 7px;
  margin-right: 10px;
  &:hover {
    background: rgba(219, 219, 219, 0.15);
  }
  &:active {
    border: none;
  }
}
@media (max-width: 300px) {
  .date {
    font-size: 18px !important;
  }
}
</style>
