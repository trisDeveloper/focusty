<template>
  <nav class="navbar">
    <button class="menu-button" @click="toggleSidebar">
      menu
    </button>

    <img class="profile-icon" :src="profileImage" alt="Profile" />
    <div class="sidebar" :class="{ active: isSidebarActive }">
      <ul class="sidebar-menu">
        <li>
          <a href="/">Home</a>
        </li>
        <li>
          <a href="/about">About</a>
        </li>
        <li>
          <a href="/settings">Settings</a>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script>
export default {
  data() {
    return {
      profileImage: "path/to/profile.png",
      isSidebarActive: false,
    };
  },
  methods: {
    toggleSidebar() {
      this.isSidebarActive = !this.isSidebarActive;
    },
  },
};
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  height: 60px;
  padding: 10px;
  align-items: center;
}

.menu-button {
  border: none;
  background: none;
  padding: 0;
  cursor: pointer;
}

.profile-icon {
  border-radius: 50%;
  height: 40px;
  width: 40px;
}

.sidebar {
  position: fixed;
  top: 60px;
  left: 0;
  width: 250px;
  height: 100vh;
  background-color: #040028;
  box-shadow: 0px 7px 20px rgba(134, 145, 204, 0.15);
  z-index: 10;
  transition: transform 0.3s cubic-bezier(0.46, 0.03, 0.52, 0.96);
  transform: translateX(-100%);
}

.sidebar.active {
  transform: translateX(0);
}
</style>
