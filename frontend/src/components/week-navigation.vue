<script setup>
import { useStore } from '@/stores'
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'
const store = useStore()
const route = useRoute()

const isCalendarView = computed(() => route.path.includes('/calendar'))
const isWideScreen = ref(window.innerWidth >= 1075 || window.innerWidth <= 600)
let daysNum = isWideScreen.value ? 7 : 4
const next7Days = () => {
  let date = new Date(store.weekStart).setDate(new Date(store.weekStart).getDate() + daysNum)
  store.setWeekStart(date)
}
const prev7Days = () => {
  let date = new Date(store.weekStart).setDate(new Date(store.weekStart).getDate() - daysNum)
  store.setWeekStart(date)
}
const resetToToday = () => {
  store.setWeekStart(new Date())
}
</script>

<template>
  <div class="week-nav" v-if="isCalendarView">
    <div class="chevrons">
      <div @click="prev7Days" title="Previous week">
        <font-awesome-icon icon="fa-solid fa-chevron-left" />
      </div>
      <div @click="next7Days" title="Next week">
        <font-awesome-icon icon="fa-solid fa-chevron-right" />
      </div>
    </div>
    <button @click="resetToToday" title="Today" class="today">Today</button>
  </div>
</template>

<style lang="scss" scoped>
.week-nav {
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 0 25px;
  .chevrons {
    display: flex;
    flex-direction: row;
    align-items: center;
    div {
      border-radius: 4px;
      padding: 6px 10px;
      margin-right: 2px;
      cursor: pointer;
      &:hover {
        background: #ffffff14;
      }
    }
  }
  .today {
    margin-left: 8px;
    background: transparent;
    color: #eee;
    border: 1px solid #ffffff14;
    cursor: pointer;
    padding: 6px 10px;
    font-size: 16px;
    border-radius: 4px;
    &:hover {
      background: #ffffff14;
      color: white;
    }
  }
}
</style>
