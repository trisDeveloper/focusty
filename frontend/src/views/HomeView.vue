<script setup>
import { useStore } from '@/stores'
import { ref, watch } from 'vue'
import TodayTasks from './CalendarView.vue'
import Pomodoro from './pomodoroView.vue'
const store = useStore()
const msg = ref('')

msg.value = 'welcome ' + (store.user.username || '')
watch(
  () => store.user.id,
  () => {
    msg.value = 'welcome ' + store.user.username
  }
)
</script>

<template>
  <div class="home">
    <p v-if="!store.user.id">you should log in to use the app</p>
    <h1>{{ msg }}</h1>
    <main>
      <div class="today-tasks">
        <TodayTasks :filterdays="true" />
      </div>
      <div class="pomo">
        <Pomodoro />
      </div>
    </main>
  </div>
</template>

<style lang="scss">
.home {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 10px;
  main {
    display: grid;
    grid-template-columns: calc(50% - 7px) calc(50% - 7px);
    gap: 14px;
  }
  h1 {
    padding: 10px 0;
  }
  .today-tasks {
    width: 100%;
    .calendar {
      min-height: calc(100vh - 120px);
      .day {
        width: 100%;
        border-radius: 10px;
      }
    }
  }
  .pomo {
    width: 100%;
    .pomodoro-timer {
      margin: 0;
      width: 100%;
    }
  }
  @media (max-width: 650px) {
    main {
      display: grid;
      grid-template-columns: 100%;
      gap: 14px;
      justify-items: center;
      .today-tasks {
        .calendar {
          min-height: fit-content;
        }
      }
    }
  }
}
</style>
